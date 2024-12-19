from enum import Enum as UserEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DATETIME, Enum, ForeignKey

from StudentManagement import db, app


class BaseModel(db.Model):
    __abstract__ = True  # Để đánh dấu đây là lớp trừu tượng
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=True, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    image_link = Column(String(255), nullable=True)
    gender = Column(String(10), nullable=True)
    birth_day = Column(DATETIME, nullable=True)


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
    code = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'


# Tạo bảng học sinh
class Student(BaseModel):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}
    address = Column(String(255), nullable=True)
    grade = Column(Integer, nullable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Tạo bản khối
class Grade(db.Model):
    __tablename__ = 'grade'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=False)


# Tạo bảng giáo viên
class Teacher(db.Model):
    __tablename__ = 'teacher'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Tạo bảng môn học
class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

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
    description = db.Column(db.String(255))

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
        # User.__table__.create(db.engine)

        # Rule.__table__.create(db.engine)
        # qd = Rule(so_tuoi_toi_thieu=15,so_tuoi_toi_da=20,si_so_toi_da=40)
        # db.session.add(qd)
        # db.session.commit()


