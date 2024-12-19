import bcrypt
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from StudentManagement import db
from models import User, Subject, Teacher, SchoolClass, Rule


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


# Lấy môn học theo ID
def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)


def get_all_subjects():
    """Lấy tất cả môn học kèm thông tin giáo viên"""
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        # Lấy tất cả giáo viên của môn học này
        teachers = Teacher.query.filter_by(subject_id=subject.id).all()

        subject_info = {
            'id': subject.id,
            'code': subject.code,
            'name': subject.name,
            'description': subject.description,
            'teachers': teachers
        }
        result.append(subject_info)
    return result

# Thêm môn học mới
def add_subject(subject_name, subject_code, description, teacher_ids):
    new_subject = Subject(name=subject_name, code=subject_code, description=description)
    try:
        db.session.add(new_subject)
        db.session.commit()
        if teacher_ids:
            for teacher_id in teacher_ids:
                teacher = Teacher.query.get(teacher_id)
                if teacher:
                    teacher.subject_id = new_subject.id
                    db.session.add(teacher)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Lỗi khi thêm môn học: {str(e)}", "danger")
        return False
    # CHỖ NÀY SỬA THÀNH GỌI ADD_SUBJECT XONG TRUYỀN MẤY GIÁ TRỊ VÀO THEO MẪU add_subject(code,name,des) BÊN HTML CŨN ĐƯỢC

def update_subject(subject_id, subject_name, subject_code, description, teacher_ids):
    try:
        # Kiểm tra môn học tồn tại
        subject = Subject.query.get(subject_id)
        if not subject:
            return False, 'Môn học không tồn tại!'

        # Cập nhật thông tin môn học
        db.session.execute(
            db.update(Subject)
            .where(Subject.id == subject_id)
            .values(
                name=subject_name,
                code=subject_code,
                description=description
            )
        )

        # # Reset tất cả giáo viên cũ
        # db.session.execute(
        #     db.update(Teacher)
        #     .where(Teacher.subject_id == subject_id)
        #     .values(subject_id=None)
        # )

        # Cập nhật giáo viên mới
        if teacher_ids:
            for teacher_id in teacher_ids:
                db.session.execute(
                    db.update(Teacher)
                    .where(Teacher.id == int(teacher_id))
                    .values(subject_id=subject_id)
                )

        # Commit các thay đổi
        db.session.commit()
        return True, 'Cập nhật môn học thành công!'

    except Exception as e:
        db.session.rollback()
        return False, f"Lỗi khi cập nhật môn học: {str(e)}"

# Xóa môn học
def delete_subject(subject_id):
    subject = get_subject_by_id(subject_id)
    if subject:
        try:
            Teacher.query.filter_by(subject_id=subject_id).update({Teacher.subject_id: None})

            db.session.delete(subject)
            db.session.commit()
            return True, 'Môn học đã được xóa thành công!'
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Lỗi khi xóa môn học: {str(e)}"
    else:
        return False, 'Không tìm thấy môn học!'



def get_available_teachers():
    """Lấy danh sách giáo viên chưa được phân công môn học"""
    return db.session.query(Teacher, User)\
        .join(User, Teacher.user_id == User.id)\
        .filter(Teacher.subject_id == None)\
        .all()

def get_teacher_with_subject(subject_id = None):
    return  db.session.query(Teacher, User)\
            .join(User, Teacher.user_id == User.id)\
            .filter(Teacher.subject_id == subject_id)\
            .all()

# Lấy tất cả giáo viên
def get_all_teachers():
    return db.session.query(Teacher, User) \
        .join(User, Teacher.user_id == User.id) \
        .all()

# Hàm lấy danh sách tất cả lớp học
def get_all_classes():
    return SchoolClass.query.all()


# Hàm thêm lớp học mới
def add_class(class_name, class_code, grade, student_count, description, teacher_id):
    try:
        quy_dinh = Rule.query.first()
        if student_count > quy_dinh.si_so_toi_da:
            return False, f'Sĩ số lớp không được vượt quá {quy_dinh.si_so_toi_da}'

        # Kiểm tra giáo viên có đang chủ nhiệm lớp khác không
        teacher = Teacher.query.filter_by(id=teacher_id).first()
        if teacher and teacher.class_id:
            return False, 'Giáo viên này đã chủ nhiệm một lớp khác!'

        new_class = SchoolClass(name=class_name, code=class_code, grade=grade,
                                student_count=student_count, description=description,
                                teacher_id=teacher_id)
        db.session.add(new_class)
        # Cập nhật thông tin giáo viên chủ nhiệm
        if teacher:
            teacher.class_id = new_class.id
            db.session.add(teacher)
        db.session.commit()
        return True, 'Lớp học đã được thêm thành công!'
    except Exception as e:
        db.session.rollback()
        return False, f'Có lỗi xảy ra: {str(e)}'


# Hàm lấy thông tin lớp học theo ID
def get_class_by_id(class_id):
    return SchoolClass.query.get(class_id)


# Hàm cập nhật lớp học
def update_class_by_id(class_id, class_name, class_code, grade, student_count, description, teacher_id):
    try:
        classById = SchoolClass.query.get(class_id)
        if not classById:
            return False, 'Lớp học không tồn tại!'
            # Kiểm tra sĩ số có vượt quá quy định không
        quy_dinh = Rule.query.first()
        if student_count > quy_dinh.si_so_toi_da:
            return False, f'Sĩ số lớp không được vượt quá {quy_dinh.si_so_toi_da}'

            # Kiểm tra giáo viên có đang chủ nhiệm lớp khác không
        teacher = Teacher.query.filter_by(id=teacher_id).first()
        if teacher and teacher.class_id and teacher.class_id != class_id:
            return False, 'Giáo viên này đã chủ nhiệm một lớp khác!'

        classById.name = class_name
        classById.code = class_code
        classById.grade = grade
        classById.student_count = student_count
        classById.description = description
        classById.teacher_id = teacher_id
        if teacher:
            teacher.class_id = classById.id
            db.session.add(teacher)

        db.session.commit()
        return True, 'Cập nhật lớp học thành công!'
    except Exception as e:
        db.session.rollback()
        return False, f'Có lỗi xảy ra khi cập nhật lớp học: {str(e)}'


# Hàm xóa lớp học
def delete_class_by_id(class_id):
    try:
        classById = SchoolClass.query.get(class_id)
        if classById:
            # Nếu lớp học có giáo viên chủ nhiệm, cần set lại class_id cho giáo viên đó
            teacher = Teacher.query.filter_by(class_id=class_id).first()
            if teacher:
                teacher.class_id = None  # Set lại giáo viên không còn chủ nhiệm lớp này
                db.session.add(teacher)

            # Xóa lớp học
            db.session.delete(classById)
            db.session.commit()
            return True, 'Lớp học đã được xóa thành công!'
        else:
            return False, 'Không tìm thấy lớp học!'
    except Exception as e:
        db.session.rollback()
        return False, f'Có lỗi xảy ra khi xóa lớp học: {str(e)}'
