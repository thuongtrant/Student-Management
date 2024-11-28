from StudentManagement import db
from datetime import date
import bcrypt
from sqlalchemy.exc import IntegrityError
from models import User

# Hàm mã hóa mật khẩu và lưu vào cơ sở dữ liệu
def add_user(user_role, username, password, code, last_name, first_name, phone, email, image_link, gender, birth_year):

        # Kiểm tra xem người dùng đã tồn tại trong bảng user
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            return "User already exists"  # Dừng thêm nếu đã tồn tại

        # Mã hóa mật khẩu bằng bcrypt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Tạo đối tượng User mới và thêm vào cơ sở dữ liệu
        new_user = User(
            user_role=user_role,
            username=username,
            password=hashed_password.decode('utf-8'),
            code=code,
            last_name=last_name,
            first_name=first_name,
            phone=phone,
            email=email,
            image_link=image_link,
            gender=gender,
            birth_year=birth_year
        )

        db.session.add(new_user)
        db.session.commit()  # Xác nhận thay đổi trong cơ sở dữ liệu
        return "User added successfully"

