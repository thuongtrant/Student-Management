from datetime import datetime
from math import ceil

import bcrypt
from flask import jsonify
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from password_strength import PasswordPolicy
from sqlalchemy import and_

from StudentManagement import app, db
from dao import load_students
from models import Student, Rule
from models import User, UserRole
from send_email import send_mail
from utils import (check_login, get_all_subjects, get_subject_by_id, add_subject, update_subject,
                   delete_subject
, get_all_classes, get_all_teachers, add_class, get_class_by_id, update_class_by_id, delete_class_by_id)

# Khởi tạo LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bạn cần phải đăng nhập để truy cập trang này.'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        # Điều hướng dựa trên vai trò của người dùng
        if current_user.user_role == UserRole.ADMIN:
            return redirect(url_for('admin_dashboard'))
        elif current_user.user_role == UserRole.TEACHER:
            return redirect(url_for('teacher_dashboard'))
        elif current_user.user_role == UserRole.EMPLOYEE:
            return redirect(url_for('employee_dashboard'))
    return render_template('login.html')


# Start Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Xác thực người dùng
        user = check_login(username, password)

        if user:
            # Kiểm tra xem người dùng có quyền truy cập tương ứng không
            if user.user_role.name.lower() == role.lower():
                login_user(user, remember=True)
                # Chuyển hướng đến trang dashboard dựa trên vai trò
                if role.upper() == 'ADMIN':
                    return redirect(url_for('admin_dashboard'))
                elif role.upper() == 'TEACHER':
                    return redirect(url_for('teacher_dashboard'))
                elif role.upper() == 'EMPLOYEE':
                    return redirect(url_for('employee_dashboard'))
            else:
                flash('Sai quyền người dùng!', 'error')
        else:
            flash('Tài khoản hoặc mật khẩu sai!', 'error')

    return render_template('login.html')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    return render_template('teacher_dashboard.html')


@app.route('/employee_dashboard')
@login_required
def employee_dashboard():
    return render_template('employee_dashboard.html')


# End login

# Xem thông tin cá nhân người dùng
@app.route('/user_info')
@login_required
def user_info():
    # Truy cập thông tin người dùng đã đăng nhập
    user = current_user
    # Định dạng lại chỗi ngày sinh lấy từ CSDL
    formatted_date = user.birth_day.strftime("%d/%m/%Y")
    return render_template('user_info.html', user=user, formatted_date=formatted_date)


# Trả về trang cập nhật mật khẩu
@app.route('/change_password')
@login_required
def change_password():
    return render_template('change_password.html')


# Kiểm tra mật khẩu mới
@app.route('/test_password', methods=['GET', 'POST'])
@login_required
def test_password():
    if request.method == 'POST':
        old_pw = request.form.get('old_password')
        new_pw = request.form.get('new_password')
        new_pw_test = request.form.get('new_password_test')
        if bcrypt.checkpw(old_pw.encode(), current_user.password.encode()):
            if new_pw.encode() == new_pw_test.encode():
                if is_valid_password(new_pw):
                    hashed_pw = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())
                    current_user.password = hashed_pw.decode()
                    db.session.commit()
                    flash("Đổi mật khẩu thành công", 'success')
                else:
                    flash("Mật khẩu mới không đúng định dạng", 'error')
            else:
                flash("Mật khẩu không khớp", 'error')
        else:
            flash("Nhập sai mật khẩu cũ", 'error')
    return redirect(url_for('change_password'))


# Trả về trang quản lý học sinh
@app.route('/student_management')
@login_required
def student_management():
    return render_template('student_management.html')


# Thêm học sinh mới
@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date = request.form.get('birth_date')

        # Kiểm tra học sinh đã tồn tại hay chưa
        existing_student = db.session.query(Student).filter(
            and_(
                Student.first_name == first_name,
                Student.last_name == last_name,
                Student.birth_day == birth_date
            )
        ).first()

        if existing_student:
            flash("Học sinh đã tồn tại!", 'error')
        else:
            # Lấy năm hiện tại (int)
            current_year = int(datetime.now().year)

            # Lấy năm từ birth_date (int)
            birth_year = int(birth_date.split('-')[0])  # Tách năm từ chuỗi "yyyy-mm-dd"
            if current_year - birth_year < 15:
                flash("Học sinh chưa đạt độ tuổi yêu cầu!", 'error')
            else:
                phone = request.form.get('phone')
                gender = request.form.get('gender')
                email = request.form.get('email')
                address = request.form.get('address')
                file = request.files['photo']
                grade = request.form.get('grade')
                new_student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    birth_day=birth_date,
                    phone=phone,
                    gender=gender,
                    email=email,
                    address=address,
                    image_link=file.filename,
                    grade=grade
                )
                db.session.add(new_student)
                db.session.commit()
                flash("Thêm thành công!", 'success')
                send_mail(email, last_name, first_name)
    return redirect(url_for('student_management'))


# Tra cứu học sinh
@app.route('/student_searching')
@login_required
def student_searching():
    page = request.args.get('page', 1)
    kw = request.args.get('kw')
    students = load_students(kw=kw, page=int(page))

    page_size = 10
    total = Student.query.count()

    return render_template("student_searching.html", students=students, pages=ceil(total / page_size))


# Xem hồ sơ cá nhân học sinh
@app.route('/student_info')
@login_required
def student_info():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    formatted_date = student.birth_day.strftime("%d/%m/%Y")
    return render_template("student_info.html", student=student, formatted_date=formatted_date)


# Chỉnh sửa thông tin học sinh
@app.route('/student_update_info')
@login_required
def student_update_info():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    formatted_date = student.birth_day.strftime('%Y-%m-%d')
    return render_template("student_update_info.html", student=student, formatted_date=formatted_date)


# Cập nhật thông tin trong cơ sở dữ liệu
@app.route('/student_update_process', methods=['GET', 'POST'])
@login_required
def student_update_process():
    if request.method == 'POST':
        student_id = request.args.get('student_id', type=int)
        student = Student.query.get(student_id)

        # Xử lý ngày sinh
        birth_date = request.form.get('birth_date')
        if birth_date:
            current_year = int(datetime.now().year)
            birth_year = int(birth_date.split('-')[0])  # Tách năm từ "yyyy-mm-dd"
            if current_year - birth_year < 15:
                flash("Học sinh chưa đạt độ tuổi yêu cầu!", 'error')
                return redirect(url_for('student_update_info', student_id=student_id))
            else:
                student.birth_day = birth_date  # Cập nhật ngày sinh nếu hợp lệ

        # Cập nhật thông tin khác
        student.first_name = request.form.get('first_name') or student.first_name
        student.last_name = request.form.get('last_name') or student.last_name
        student.phone = request.form.get('phone') or student.phone
        student.gender = request.form.get('gender') or student.gender
        student.email = request.form.get('email') or student.email
        student.address = request.form.get('address') or student.address
        student.image_link = request.files.get('photo').filename or student.image_link

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        flash("Cập nhật thành công!", 'success')
        return redirect(url_for('student_info', student_id=student_id))


# Xác thực trước khi xóa hồ sơ học sinh
@app.route('/delete_student_confirm')
@login_required
def delete_student_confirm():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    return render_template("delete_student.html", student=student)


# Xóa hồ sơ học sinh
@app.route('/delete_student', methods=['GET', 'POST'])
@login_required
def delete_student():
    if request.method == 'POST':
        password_check = request.form.get('password_check')
        student_id = request.args.get('student_id', type=int)
        student = Student.query.get(student_id)
        if bcrypt.checkpw(password_check.encode(), current_user.password.encode()):
            db.session.delete(student)
            db.session.commit()
            flash("Xóa thành công!", 'success')
        else:
            flash("Sai mật khẩu!", 'error')
            return redirect(url_for('delete_student_confirm', student_id=student_id))
    return redirect(url_for('student_searching'))


# Định nghĩa yêu cầu mật khẩu
policy = PasswordPolicy.from_names(
    length=8,  # ít nhất 8 ký tự
    uppercase=1,  # ít nhất 1 chữ hoa
    numbers=1,  # ít nhất 1 chữ số
    special=1,  # ít nhất 1 ký tự đặc biệt
)


# Hàm kiểm tra định dạng mật khẩu
def is_valid_password(password):
    if len(policy.test(password)) == 0:
        return True
    return False


# Start Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('login'))


# End logout

# Start Change_of_rules
@app.route('/change_of_rules', methods=['GET', 'POST'])
def change_of_rules():
    err_mgs = ''

    if request.method == 'POST':
        so_tuoi_toi_thieu = request.form.get('so_tuoi_toi_thieu')
        so_tuoi_toi_da = request.form.get('so_tuoi_toi_da')
        si_so_toi_da = request.form.get('si_so_toi_da')

        quidinh = Rule.query.first()

        if quidinh:  # Nếu đã có quy định trong CSDL
            quidinh.so_tuoi_toi_thieu = so_tuoi_toi_thieu
            quidinh.so_tuoi_toi_da = so_tuoi_toi_da
            quidinh.si_so_toi_da = si_so_toi_da
            err_mgs = 'Cập nhật quy định thành công!', 'success'
        else:  # Nếu chưa có, tạo mới
            quidinh = Rule(so_tuoi_toi_thieu=so_tuoi_toi_thieu, so_tuoi_toi_da=so_tuoi_toi_da,
                           si_so_toi_da=si_so_toi_da)
            db.session.add(quidinh)

        db.session.commit()  # Lưu thay đổi vào CSDL

    quidinh = Rule.query.first()
    return render_template('change_of_rules.html', quidinh=quidinh, err_mgs=err_mgs)


# Môn học
# Thêm mới môn học, hiển thị danh sách
@app.route('/subject_management', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        subject_name = request.form.get('subject_name')
        subject_code = request.form.get('subject_code')
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')

        # Thêm môn học
        if add_subject(subject_name, subject_code, description, teacher_id):
            return redirect(url_for('manage_subjects'))

    subjects = get_all_subjects()
    teachers = get_all_teachers()
    return render_template('subject_management.html', subjects=subjects, teachers=teachers)


@app.route('/edit_subject/<int:subject_id>', methods=['GET'])
def edit_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        flash('Môn học không tồn tại!', 'danger')
        return redirect(url_for('manage_subjects'))

    # Lấy danh sách giáo viên
    available_teachers = get_all_teachers()
    return render_template('edit_subject.html', subject=subject, teachers=available_teachers)


@app.route('/update_subject/<int:subject_id>', methods=['POST'])
def update_subject_route(subject_id):
    # Lấy dữ liệu từ form
    subject_name = request.form.get('subject_name')
    subject_code = request.form.get('subject_code')
    description = request.form.get('description')
    teacher_id = request.form.get('teacher_id')

    # Cập nhật môn học
    if update_subject(subject_id, subject_name, subject_code, description, teacher_id):
        return redirect(url_for('manage_subjects'))


@app.route('/api/delete-subject/<int:subject_id>', methods=['DELETE'])
def delete_subject_route(subject_id):
    success, message = delete_subject(subject_id)
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message}), 404


# Lớp học
@app.route('/class_management', methods=['GET', 'POST'])
def class_management():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        class_name = request.form.get('class_name')
        class_code = request.form.get('class_code')
        grade = request.form.get('class_grade')
        student_count = int(request.form.get('student_count'))
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')

        success, message = add_class(class_name, class_code, grade, student_count, description, teacher_id)
        if not success:
            flash(message, 'danger')
        else:
            flash(message, 'success')
        return redirect(url_for('class_management'))

    classes = get_all_classes()
    teachers = get_all_teachers()
    return render_template('class_management.html', classes=classes, teachers=teachers)


# Lấy dữ liệu để hiện thị trong trang sửa lớp học
@app.route('/edit_class/<int:class_id>', methods=['GET'])
def edit_class(class_id):
    classById = get_class_by_id(class_id)
    if not classById:
        flash('Lớp học không tồn tại!', 'danger')
        return redirect(url_for('class_management'))
    available_teachers = get_all_teachers()

    return render_template('edit_class.html', classById=classById, teachers=available_teachers)


# Tiến hành sửa lớp học
@app.route('/update_class/<int:class_id>', methods=['POST'])
def update_class(class_id):
    class_name = request.form.get('class_name')
    class_code = request.form.get('class_code')
    grade = request.form.get('class_grade')
    student_count = int(request.form.get('student_count'))
    description = request.form.get('description')
    teacher_id = request.form.get('teacher_id')

    success, message = update_class_by_id(class_id, class_name, class_code, grade, student_count, description,
                                          teacher_id)
    if not success:
        flash(message, 'danger')
    else:
        flash(message, 'success')

    return redirect(url_for('class_management'))


@app.route('/api/delete-class/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    success, message = delete_class_by_id(class_id)
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})


if __name__ == "__main__":
    app.run(debug=True)
