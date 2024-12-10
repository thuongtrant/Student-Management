from models import User, Subject, Teacher
from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from StudentManagement import db
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


def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)


# Lấy tất cả môn học
def get_all_subjects():
    return Subject.query.all()

# Trả về danh sách các giáo viên chưa dạy môn học nào
def get_teachers_without_subject():
    return Teacher.query.filter(~Teacher.id.in_(db.session.query(Subject.teacher_id).filter(Subject.teacher_id.isnot(None)))).all()

# Lấy tất cả giáo viên
def get_all_teachers():
    return Teacher.query.all()

# Lấy môn học theo ID
def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)

# Thêm môn học mới
def add_subject(subject_name, subject_code, description, teacher_id):
    new_subject = Subject(name=subject_name, code=subject_code, description=description, teacher_id=teacher_id)
    try:
        db.session.add(new_subject)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Lỗi khi thêm môn học: {str(e)}", "danger")
        return False

# Cập nhật thông tin môn học
def update_subject(subject_id, subject_name, subject_code, description, teacher_id):
    subject = get_subject_by_id(subject_id)
    if not subject:
        flash('Môn học không tồn tại!', 'danger')
        return False

    try:
        subject.name = subject_name
        subject.code = subject_code
        subject.description = description
        subject.teacher_id = teacher_id if teacher_id else None
        db.session.commit()
        flash('Cập nhật môn học thành công!', 'success')
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Có lỗi xảy ra khi cập nhật môn học: {str(e)}", 'danger')
        return False

# Xóa môn học
def delete_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    if subject:
        try:
            db.session.delete(subject)
            db.session.commit()
            return True, 'Môn học đã được xóa thành công!'
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Lỗi khi xóa môn học: {str(e)}"
    else:
        return False, 'Không tìm thấy môn học!'