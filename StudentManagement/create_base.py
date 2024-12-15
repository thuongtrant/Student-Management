import random
import string
from datetime import datetime

import bcrypt

from StudentManagement import db
from models import User, Teacher, Subject


# Hàm mã hóa mật khẩu và lưu vào cơ sở dữ liệu
def add_user(user_role, username, last_name, first_name, phone, email, image_link, gender, birth_day_s):
    # Kiểm tra xem người dùng đã tồn tại trong bảng user
    existing_user = db.session.query(User).filter_by(username=username).first()
    if existing_user:
        return "User already exists"  # Dừng thêm nếu đã tồn tại

    # Gọi hàm tạo mật khẩu ngẫu nhiên khi tạo account mới
    password = random_password()

    # Mã hóa mật khẩu bằng bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Chuyển chuỗi thành ngày tháng năm
    birth_day = datetime.strptime(birth_day_s, "%d%m%Y")

    # Tạo đối tượng User mới và thêm vào cơ sở dữ liệu
    new_user = User(
        user_role=user_role,
        username=username,
        password=hashed_password.decode('utf-8'),
        code=password,
        last_name=last_name,
        first_name=first_name,
        phone=phone,
        email=email,
        image_link=image_link,
        gender=gender,
        birth_day=birth_day
    )

    db.session.add(new_user)
    db.session.commit()  # Xác nhận thay đổi trong cơ sở dữ liệu

    # Nếu vai trò là TEACHER, tự động thêm vào bảng teacher
    if user_role.upper() == "TEACHER":
        new_teacher = Teacher(user_id=new_user.id)
        db.session.add(new_teacher)
        db.session.commit()

    return "User added successfully"


# Hàm random mật khẩu ngẫu nhiên:
def random_password():
    # Danh sách ký tự
    special_chars = "#@.!$&"
    letters_lower = string.ascii_lowercase  # Chữ thường
    letters_upper = string.ascii_uppercase  # Chữ hoa
    digits = string.digits  # Số

    # Đảm bảo mỗi yêu cầu được đáp ứng
    password = [
        random.choice(letters_upper),  # 1 ký tự hoa
        random.choice(special_chars),  # 1 ký tự đặc biệt
        random.choice(digits)  # 1 số
    ]

    # Thêm các ký tự còn lại từ tập chữ thường
    password += random.choices(letters_lower, k=5)  # 5 ký tự ngẫu nhiên khác

    # Trộn thứ tự các ký tự
    random.shuffle(password)

    return ''.join(password)


# Hàm thêm môn học
def add_subject(code, name, description):
    existing_subject = db.session.query(Subject).filter_by(name=name).first()
    if existing_subject:
        return "Subject already exists"
    code = code + datetime.now().strftime("%d%m")
    new_subject = Subject(
        code=code,
        name=name,
        description=description
    )
    db.session.add(new_subject)
    db.session.commit()
    return "Subject added successfully"