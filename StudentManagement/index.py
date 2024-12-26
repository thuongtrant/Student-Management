from datetime import datetime
from math import ceil

import bcrypt
from flask import jsonify
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from password_strength import PasswordPolicy
from sqlalchemy import and_

from StudentManagement import app, db
from StudentManagement.utils import get_unassigned_students
from models import Student, Rule, User, UserRole, Grade, SchoolClass, Student_Schoolclass, Teacher_Schoolclass, Teacher, \
    Score_Board
from send_email import send_mail
from utils import (check_login, get_all_subjects, get_subject_by_id, add_subject, update_subject,
                   delete_subject, get_teacher_with_subject, get_available_teachers, get_teacher_nonehr
, get_all_classes_this_semester, get_all_teachers, load_students, create_new_class, get_students_by_teacherid,
                   add_classes_auto, get_student_by_classid, get_all_subjects_only)

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
    teacher = Teacher.query.get(current_user.id)
    students = get_students_by_teacherid(teacher.id)
    return render_template('teacher_dashboard.html', students=students)


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


# Thêm học sinh mới
@app.route('/student_management', methods=['GET', 'POST'])
@login_required
def student_management():
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
                grade_id = request.form.get('grade')
                new_student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    birth_day=birth_date,
                    phone=phone,
                    gender=gender,
                    email=email,
                    address=address,
                    image_link=file.filename,
                    grade_id=grade_id
                )
                db.session.add(new_student)
                db.session.commit()
                flash("Thêm thành công!", 'success')
                send_mail(email, last_name, first_name)
    return render_template('student_management.html')


# Tra cứu học sinh
@app.route('/student_searching')
@login_required
def student_searching():
    page = request.args.get('page', 1, type=int)  # Chuyển page về kiểu int
    kw = request.args.get('kw')
    page_size = 10
    students = load_students(kw=kw, page=page)

    total = Student.query.count()
    pages = ceil(total / page_size)

    # Tính toán range trang hiển thị (max và min)
    start_page = max(page - 2, 1)
    end_page = min(page + 3, pages + 1)

    return render_template("student_searching.html",
                           students=students, pages=pages, current_page=page, start_page=start_page, end_page=end_page)


# Xem hồ sơ cá nhân học sinh
@app.route('/student_info')
@login_required
def student_info():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    formatted_date = student.birth_day.strftime("%d/%m/%Y")
    return render_template("student_info.html",
                           student=student, formatted_date=formatted_date, current_user=current_user)


# Chỉnh sửa thông tin học sinh
@app.route('/student_update', methods=['GET', 'POST'])
@login_required
def student_update():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    formatted_date = student.birth_day.strftime('%Y-%m-%d')
    if request.method == 'POST':
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
    return render_template("student_update_info.html", student=student, formatted_date=formatted_date)


# Xóa hồ sơ học sinh
@app.route('/delete_student', methods=['GET', 'POST'])
@login_required
def delete_student():
    student_id = request.args.get('student_id', type=int)
    student = Student.query.get(student_id)
    if request.method == 'POST':
        password_check = request.form.get('password_check')
        if bcrypt.checkpw(password_check.encode(), current_user.password.encode()):
            db.session.query(Student_Schoolclass).filter(Student_Schoolclass.student_id == student_id).delete()
            db.session.delete(student)
            db.session.commit()
            flash("Xóa thành công!", 'success')
            return redirect(url_for('student_searching'))
        else:
            flash("Sai mật khẩu!", 'error')
    return render_template("delete_student.html", student=student)


# Phân lớp tự động
@app.route('/automatic_class_management', methods=['GET', 'POST'])
@login_required
def automatic_class_management():
    if request.method == 'POST':
        grade_id = int(request.form.get('class_grade_auto'))
        add_classes_auto(grade_id)
    grades = db.session.query(Grade).all()
    classes = get_all_classes_this_semester()
    teachers = get_teacher_nonehr()
    return render_template("class_management.html", classes=classes, teachers=teachers, grades=grades)


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
        teacher_ids = request.form.getlist('teacher_ids[]')
        teacher_ids = [int(id) for id in teacher_ids if id]

        # Thêm môn học
        if add_subject(subject_name, subject_code, description, teacher_ids):
            return redirect(url_for('manage_subjects'))

    subjects = get_all_subjects()
    teachers = get_available_teachers()
    return render_template('subject_management.html', subjects=subjects, teachers=teachers)


@app.route('/edit_subject/<int:subject_id>', methods=['GET'])
def edit_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        flash('Môn học không tồn tại!', 'danger')
        return redirect(url_for('manage_subjects'))

    # Lấy danh sách giáo viên
    teachers_available = get_all_teachers()
    teacher_with_subject = get_teacher_with_subject(subject_id)
    return render_template('edit_subject.html', subject=subject, teachers=teachers_available,
                           teacher_with_subject=teacher_with_subject)


@app.route('/update_subject/<int:subject_id>', methods=['POST'])
def update_subject_route(subject_id):
    # Lấy dữ liệu từ form
    subject_name = request.form.get('subject_name')
    subject_code = request.form.get('subject_code')
    description = request.form.get('description')
    teacher_ids = request.form.getlist('teacher_ids[]')
    teacher_ids = [int(id) for id in teacher_ids if id]

    # Cập nhật môn học
    if update_subject(subject_id, subject_name, subject_code, description, teacher_ids):
        return redirect(url_for('manage_subjects'))
    else:
        flash('Cập nhật môn học thất bại!', 'danger')
        return redirect(url_for('edit_subject', subject_id=subject_id))


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
        grade = request.form.get('class_grade')
        student_count = int(request.form.get('student_count'))
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')

        create_new_class(grade, teacher_id, student_count, description)
        return redirect(url_for('class_management'))
    grades = db.session.query(Grade).all()
    classes = get_all_classes_this_semester()
    teachers = get_teacher_nonehr()
    return render_template('class_management.html', classes=classes, teachers=teachers, grades=grades)


# Tiến hành sửa lớp học
@app.route('/class_update', methods=['GET', 'POST'])
@login_required
def class_update():
    class_id = request.args.get('class_id', type=int)
    cls = db.session.query(SchoolClass).filter(SchoolClass.id == class_id).first()
    students = get_student_by_classid(class_id)
    grade = db.session.query(Grade).filter(cls.grade_id == Grade.id).first()
    subjects = get_all_subjects_only()
    teachers = get_all_teachers()
    students_nullclass = get_unassigned_students(grade.id)

    homeroom_teacher_id = cls.homeroom_teacher_id
    teacher_assignments = db.session.query(Teacher_Schoolclass).filter(Teacher_Schoolclass.class_id == class_id).all()
    teacher_map = {assignment.subject_id: assignment.teacher_id for assignment in teacher_assignments}

    if request.method == 'POST':
        for s in subjects:
            selected_teacher_id = request.form.get(f'teacher_id_{s.id}')
            if selected_teacher_id:
                selected_teacher_id = int(selected_teacher_id)

                # Kiểm tra xem giáo viên được chọn có phải là giáo viên chủ nhiệm
                if selected_teacher_id == homeroom_teacher_id:
                    flash(f"Giáo viên được chọn cho môn {s.name} là giáo viên chủ nhiệm. Vui lòng xác nhận.", "warning")
                    return render_template(
                        'class_update.html',
                        cls=cls,
                        students=students,
                        grade=grade.name,
                        subjects=subjects,
                        teachers=teachers,
                        students_nullclass=students_nullclass,
                        teacher_map=teacher_map,
                        confirm_teacher_change=True,
                        subject_name=s.name,
                        teacher_id=selected_teacher_id,
                        subject_id=s.id
                    )

                # Cập nhật hoặc tạo mới phân công giáo viên cho môn học
                existing_assignment = db.session.query(Teacher_Schoolclass).filter(
                    Teacher_Schoolclass.class_id == class_id,
                    Teacher_Schoolclass.subject_id == s.id
                ).first()

                if existing_assignment:
                    existing_assignment.teacher_id = selected_teacher_id
                else:
                    new_assignment = Teacher_Schoolclass(
                        teacher_id=selected_teacher_id,
                        class_id=class_id,
                        semester_id=cls.semester_id,
                        subject_id=s.id
                    )
                    db.session.add(new_assignment)
                    existing_assignment = new_assignment  # Cập nhật lại `existing_assignment` với assignment mới

                # Thêm bảng điểm cho học sinh nếu chưa có
                for student in students:
                    existing_score_board = db.session.query(Score_Board).filter(
                        Score_Board.student_id == student.id,
                        Score_Board.teacher_schoolclass_id == existing_assignment.id
                    ).first()

                    if not existing_score_board:
                        new_score_board = Score_Board(
                            student_id=student.id,
                            teacher_schoolclass_id=existing_assignment.id
                        )
                        db.session.add(new_score_board)

        # Commit các thay đổi vào cơ sở dữ liệu
        db.session.commit()
        flash("Thông tin giáo viên và bảng điểm đã được cập nhật thành công.", "success")
        return redirect(url_for('class_update', class_id=class_id))

    # Render lại trang
    return render_template(
        'class_update.html',
        cls=cls,
        students=students,
        grade=grade.name,
        subjects=subjects,
        teachers=teachers,
        students_nullclass=students_nullclass,
        teacher_map=teacher_map,
        confirm_teacher_change=False
    )



@app.route('/delete_class', methods=['GET', 'POST'])
def delete_class():
    class_id = request.args.get('class_id', type=int)
    cls = db.session.query(SchoolClass).filter(SchoolClass.id == class_id).first()
    grade_name = db.session.query(Grade).filter(cls.grade_id == Grade.id).first().name
    if request.method == 'POST':
        password_check = request.form.get('password_check')
        if bcrypt.checkpw(password_check.encode(), current_user.password.encode()):
            # Xóa các bản ghi liên quan trong các bảng khác nếu cần
            db.session.query(Student_Schoolclass).filter(Student_Schoolclass.class_id == class_id).delete()
            db.session.query(Teacher_Schoolclass).filter(Teacher_Schoolclass.class_id == class_id).delete()

            # Xóa lớp khỏi bảng SchoolClass
            db.session.delete(cls)
            db.session.commit()
            flash("Xóa thành công!", 'success')
            return redirect(url_for('class_management'))
        else:
            flash("Sai mật khẩu!", 'error')
    return render_template("delete_class.html", cls=cls, grade=grade_name)


if __name__ == "__main__":
    app.run(debug=True)
