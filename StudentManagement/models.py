from enum import Enum as UserEnum

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DATETIME, Enum, ForeignKey

from StudentManagement import db, app


class BaseModel(db.Model):
    __abstract__ = True  # Để đánh dấu đây là lớp trừu tượng
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
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


class Teacher(BaseModel):
    __tablename__ = 'teacher'
    __table_args__ = {'extend_existing': True}

    class_id = db.Column(db.Integer, db.ForeignKey('schoolclass.id'), nullable=True,
                         unique=True)
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Tạo bảng môn học
class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    teacher_id = db.Column(Integer, ForeignKey('teacher.id'), nullable = True)

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
    teacher_id = db.Column(Integer, ForeignKey('teacher.id'), nullable = True, unique=True)

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

        # Subject.__table__.create(db.engine)
        # subjects = [
        #     {   "id": 1,
        #         'code': 'MH001',
        #         'name': 'Toán',
        #         'description': 'Môn học về toán học cơ bản và nâng cao'
        #     },
        #     {
        #         "id": 2,
        #         'code': 'MH002',
        #         'name': 'Vật lý',
        #         'description': 'Môn học về các định luật vật lý'
        #     },
        #     {
        #         "id": 3,
        #         'code': 'MH003',
        #         'name': 'Hóa học',
        #         'description': 'Môn học về các hợp chất hóa học và phản ứng'
        #     },
        #     {
        #         "id": 4,
        #         'code': 'MH004',
        #         'name': 'Sinh học',
        #         'description': 'Môn học về sinh vật và các hệ thống sinh học'
        #     }
        # ]
        # for subject_data in subjects:
        #     new_subject = Subject(
        #         id = subject_data['id'],
        #         code=subject_data['code'],
        #         name=subject_data['name'],
        #         description=subject_data['description']
        #     )
        #
        #     # Thêm vào phiên làm việc (session)
        #     db.session.add(new_subject)
        #
        # # Lưu tất cả thay đổi vào cơ sở dữ liệu
        # db.session.commit()
        #
        # SchoolClass.__table__.create(db.engine)

        # Teacher.__table__.create(db.engine)


        # teachers = [
        #     {
        #         "code": "GV001",
        #         "first_name": "Văn A",
        #         "last_name": "Nguyễn",
        #         "phone": "0912345678",
        #         "email": "nguyenvana@example.com",
        #         "gender": "Nam",
        #         "birth_day": "1980-05-15"
        #     },
        #     {
        #         "code": "GV002",
        #         "first_name": "Thị B",
        #         "last_name": "Trần",
        #         "phone": "0987654321",
        #         "email": "tranthib@example.com",
        #         "gender": "Nữ",
        #         "birth_day": "1985-03-20"
        #     },
        #     {
        #         "code": "GV003",
        #         "first_name": "Văn C",
        #         "last_name": "Lê",
        #         "phone": "0977888999",
        #         "email": "levanc@example.com",
        #         "gender": "Nam",
        #         "birth_day": "1982-12-10"
        #     }
        # ]
        #
        # for teacher_data in teachers:
        #     teacher = Teacher(
        #         code=teacher_data['code'],
        #         first_name=teacher_data['first_name'],
        #         last_name=teacher_data['last_name'],
        #         phone=teacher_data['phone'],
        #         email=teacher_data['email'],
        #         gender=teacher_data['gender'],
        #         birth_day=teacher_data['birth_day']
        #     )
        #     db.session.add(teacher)
        #
        # db.session.commit()
