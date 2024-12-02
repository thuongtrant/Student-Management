from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from StudentManagement import app, db
from StudentManagement.models import User, UserRole
from StudentManagement.utils import check_login  # Thêm import check_login từ utils.py
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
