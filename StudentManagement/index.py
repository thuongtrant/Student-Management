from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager
from StudentManagement import app, db
from StudentManagement.models import User, UserRole
from StudentManagement.utils import check_login  # Thêm import check_login từ utils.py

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

@app.route('/user_info')
def user_info():
    return render_template('user_info.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
