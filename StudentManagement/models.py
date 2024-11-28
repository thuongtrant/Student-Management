from sqlalchemy import Column, Integer, String, Float, Boolean, DATETIME, ForeignKey, Enum, DateTime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum, UNIQUE
from StudentManagement import db, app

class BaseModel(db.Model):
    __abstract__ = True  # Để đánh dấu đây là lớp trừu tượng
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False, unique=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    image_link = Column(String(255), nullable=True)
    gender = Column(String(10), nullable=True)
    birth_year = Column(Integer, nullable=True)

class UserRole(UserEnum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    EMPLOYEE = "EMPLOYEE"

# Ví dụ model cho bảng User
class User(BaseModel, UserMixin):
    user_role = Column(Enum(UserRole), default=UserRole.TEACHER)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)  # Lưu mật khẩu đã hash

    def __repr__(self):
        return f'<User {self.username}>'


if __name__ == '__main__':
    with app.app_context():
        pass
        db.create_all()