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
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này
    user_role = Column(Enum(UserRole), default=UserRole.TEACHER)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)  # Lưu mật khẩu đã hash

    def __repr__(self):
        return f'<User {self.username}>'

# #Tạo bảng học sinh
# class Student(BaseModel):
#     __tablename__ = 'student'
#
#     # Các trường riêng của Student, có thể kế thừa từ BaseModel
#     student_id = Column(Integer, nullable=False)
#
#     def __repr__(self):
#         return f'<Student {self.first_name} {self.last_name}>'

#Tạo bảng môn học
class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    teacher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Subject {self.name}>'

# Tạo bảng lớp học
class SchoolClass(db.Model):
    __tablename__ = 'schoolclass'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    student_count = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    description = db.Column(db.String(255))
    teacher = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<SchoolClass {self.name}>'

# Tạo bảng quidinh
class Rule(db.Model):
    __tablename__ = 'rule'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_tuoi_toi_thieu = Column(Integer, nullable=False, default=6)
    so_tuoi_toi_da = Column(Integer, nullable=False, default=18)
    si_so_toi_da = Column(Integer, nullable=False, default=30)

    def __repr__(self):
        return f'<Rule (Min Age: {self.so_tuoi_toi_thieu}, Max Age: {self.so_tuoi_toi_da}, Max Class Size: {self.si_so_toi_da})>'


if __name__ == '__main__':
    with app.app_context():
        pass
        # db.create_all()

        # Rule.__table__.create(db.engine)
        # qd = Rule(so_tuoi_toi_thieu=15,so_tuoi_toi_da=20,si_so_toi_da=40)
        # db.session.add(qd)
        # db.session.commit()

        # Subject.__table__.create(db.engine)
        # SchoolClass.__table__.create(db.engine)
