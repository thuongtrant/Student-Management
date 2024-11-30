from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager
from StudentManagement import app, db
from models import User, UserRole
from utils import check_login  # Thêm import check_login từ utils.py
from StudentManagement.models import QuyDinh, Subject
from flask import jsonify


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
                login_user(user)
                # Chuyển hướng đến trang dashboard dựa trên vai trò
                if role.upper() == 'ADMIN':
                    return redirect(url_for('admin_dashboard'))
                elif role.upper() == 'TEACHER':
                    return redirect(url_for('teacher_dashboard'))
                elif role.upper() == 'EMPLOYEE':
                    return redirect(url_for('employee_dashboard'))
            else:
                flash('Sai quyền người dùng!', 'danger')
        else:
            flash('Tài khoản hoặc mật khẩu sai!', 'danger')

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
def user_info():
    return render_template('user_info.html')

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

        quidinh = QuyDinh.query.first()

        if quidinh:  # Nếu đã có quy định trong CSDL
            quidinh.so_tuoi_toi_thieu = so_tuoi_toi_thieu
            quidinh.so_tuoi_toi_da = so_tuoi_toi_da
            quidinh.si_so_toi_da = si_so_toi_da
            err_mgs = 'Cập nhật quy định thành công!', 'success'
        else:  # Nếu chưa có, tạo mới
            quidinh = QuyDinh(so_tuoi_toi_thieu=so_tuoi_toi_thieu, so_tuoi_toi_da=so_tuoi_toi_da, si_so_toi_da=si_so_toi_da)
            db.session.add(quidinh)

        db.session.commit()  # Lưu thay đổi vào CSDL

    quidinh = QuyDinh.query.first()
    return render_template('change_of_rules.html', quidinh=quidinh, err_mgs = err_mgs)

# Môn học
@app.route('/subject_management', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        subject_name = request.form.get('subject_name')
        subject_code = request.form.get('subject_code')
        description = request.form.get('description')
        teacher = request.form.get('teacher')

        # Thêm môn học vào cơ sở dữ liệu
        new_subject = Subject(name=subject_name, code=subject_code, description=description, teacher=teacher)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('manage_subjects'))

    subjects = Subject.query.all()  # Lấy tất cả môn học từ DB
    return render_template('subject_management.html', subjects=subjects)
    # return render_template('subject_management.html')

@app.route('/edit_subject/<int:subject_id>', methods=['GET'])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Môn học không tồn tại!', 'danger')
        return redirect(url_for('manage_subjects'))

    return render_template('edit_subject.html', subject=subject)
@app.route('/update_subject/<int:subject_id>', methods=['POST'])
def update_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash('Môn học không tồn tại!', 'danger')
        return redirect(url_for('manage_subjects'))

    # Lấy dữ liệu từ form
    subject.name = request.form.get('subject_name')
    subject.code = request.form.get('subject_code')
    subject.description = request.form.get('description')
    subject.teacher = request.form.get('teacher')

    try:
        db.session.commit()
        flash('Cập nhật môn học thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Có lỗi xảy ra khi cập nhật môn học!', 'danger')

    return redirect(url_for('manage_subjects'))

if __name__ == "__main__":
    app.run(debug=True)
