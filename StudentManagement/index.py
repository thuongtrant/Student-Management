from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask import render_template, request, redirect, url_for, flash, session
from StudentManagement import app, db
from models import User, UserRole
from utils import check_login, get_all_subjects, get_all_teachers, get_subject_by_id, add_subject, update_subject, delete_subject
from StudentManagement.models import Rule, Subject, SchoolClass, Teacher
from flask import jsonify
import bcrypt
from password_strength import PasswordPolicy

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

@app.route('/user_info')
@login_required
def user_info():
    # Truy cập thông tin người dùng đã đăng nhập
    user = current_user
    # Định dạng lại chỗi ngày sinh lấy từ CSDL
    formatted_date = user.birth_day.strftime("%d/%m/%Y")
    return render_template('user_info.html', user=user, formatted_date=formatted_date)


@app.route('/change_password')
@login_required
def change_password():
    return render_template('change_password.html')


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
import pdb

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
        teacher = request.form.get('teacher')

        # Lấy quy định về sĩ số tối đa
        quy_dinh = Rule.query.first()  # Giả định chỉ có một bản ghi quy định
        if student_count > quy_dinh.si_so_toi_da:
            flash(f'Sĩ số lớp không được vượt quá {quy_dinh.si_so_toi_da}', 'danger')
            return redirect(url_for('class_management'))
        # Thêm môn học vào cơ sở dữ liệu
        new_class = SchoolClass(name=class_name, code=class_code, grade=grade,
                                student_count=student_count, description=description,
                                teacher=teacher)
        db.session.add(new_class)
        db.session.commit()
        flash('Lớp học đã được thêm thành công!', 'success')
        return redirect(url_for('class_management'))

    classes = SchoolClass.query.all()  # Lấy tất cả môn học từ DB
    return render_template('class_management.html', classes=classes)
    # return render_template('class_management.html')


# Lấy dữ liệu để hiện thị trong trang sửa lớp học
@app.route('/edit_class/<int:class_id>', methods=['GET'])
def edit_class(class_id):
    classById = SchoolClass.query.get(class_id)
    if not classById:
        flash('Lớp học không tồn tại!', 'danger')
        return redirect(url_for('class_management'))

    return render_template('edit_class.html', classById=classById)


# Tiến hành sửa lớp học
@app.route('/update_class/<int:class_id>', methods=['POST'])
def update_class(class_id):
    classById = SchoolClass.query.get(class_id)
    if not classById:
        flash('Lớp học không tồn tại!', 'danger')
        return redirect(url_for('class_management'))

    # Lấy dữ liệu từ form
    classById.name = request.form.get('class_name')
    classById.code = request.form.get('class_code')
    classById.grade = request.form.get('class_grade')
    classById.description = request.form.get('description')
    classById.teacher = request.form.get('teacher')

    try:
        db.session.commit()
        flash('Cập nhật lớp học thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi cập nhật lớp học!', 'danger')

    return redirect(url_for('class_management'))


@app.route('/api/delete-class/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    classById = SchoolClass.query.get(class_id)

    if classById:
        db.session.delete(classById)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Lớp học đã được xóa thành công!'})
    else:
        return jsonify({'success': False, 'message': 'Không tìm thấy lớp học!'}), 404


if __name__ == "__main__":
    app.run(debug=True)
