from models import User
import bcrypt

def check_login(username, password):
    if username and password:
        # Tìm người dùng trong cơ sở dữ liệu
        user = User.query.filter_by(username=username.strip()).first()

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user  # Trả về đối tượng người dùng nếu mật khẩu hợp lệ
    return None


def get_user_by_id(user_id):
    return User.query.get(user_id)
