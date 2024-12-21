from datetime import datetime

import bcrypt
from flask import flash
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError

from StudentManagement import db
from models import User, Subject, Teacher, SchoolClass, Rule, Semester, Grade, Student, Student_Schoolclass


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
    return db.session.query(Teacher, User) \
        .join(User, Teacher.user_id == User.id) \
        .filter(Teacher.subject_id == None) \
        .all()


def get_teacher_with_subject(subject_id=None):
    return db.session.query(Teacher, User) \
        .join(User, Teacher.user_id == User.id) \
        .filter(Teacher.subject_id == subject_id) \
        .all()


# Lấy tất cả giáo viên
def get_all_teachers():
    return db.session.query(Teacher, User) \
        .join(User, Teacher.user_id == User.id) \
        .all()


# Hàm lấy danh sách tất cả lớp học
def get_all_classes():
    return db.session.query(SchoolClass, Grade, Teacher, User) \
        .join(Grade, SchoolClass.grade_id == Grade.id) \
        .join(Teacher, SchoolClass.homeroom_teacher_id == Teacher.id) \
        .join(User, Teacher.user_id == User.id) \
        .all()


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


# # Lấy danh sách học sinh theo khối
# def get_student_in_grade(grade_id):
#     return db.session.query(Student).filter(grade_id=grade_id).all()
#
# # Lấy danh sách lớp theo học kì
# def get_classes_in_semester(semester_id):
#     return db.session.query(SchoolClass).filter(semester_id=semester_id).all()
#
# # Lấy danh sách học sinh của khối chưa được phân lớp
# def get_student_in_grade_nullclass(grade_id):
#     current_date = datetime.now()
#     semester = db.session.query(Semester).filter(
#         and_(
#             Semester.start_day < current_date,
#             Semester.end_day > current_date
#         )
#     ).first()
#     return db.session.query(Student) \
#         .outerjoin(Student_Schoolclass, Student.id == Student_Schoolclass.student_id) \
#         .outerjoin(SchoolClass, Student_Schoolclass.class_id == SchoolClass.id) \
#         .outerjoin(Semester, SchoolClass.semester_id == Semester.id) \
#         .filter((Semester.id == None) | (Semester.id != semester)) \
#         .all()
#
# # Lấy danh sách lớp chưa full
# def get_classes_not_full(grade_id):
#     current_date = datetime.now()
#     semester = db.session.query(Semester).filter(
#         and_(
#             Semester.start_day <= current_date,
#             Semester.end_day >= current_date
#         )
#     ).first()
#     return db.session.query(SchoolClass).filter(
#         and_(
#             SchoolClass.grade_id == grade_id,
#             SchoolClass.semester_id == semester.id,
#             SchoolClass.student_count < db.session.query(Rule).first().si_so_toi_da  # So sánh sĩ số hiện tại
#         )
#     ).all()
#
# # Lấy danh sách giáo viên chưa chủ nhiệm lớp nào
# def get_teacher_nonehr():
#
#
#     return db.session.query(Teacher, User) \
#         .outerjoin(User, Teacher.user_id == User.id) \
#         .outerjoin(SchoolClass, SchoolClass.homeroom_teacher_id == Teacher.id) \
#         .filter(SchoolClass.homeroom_teacher_id == None) \
#         .all()
#

# Lấy danh sách giáo viên chưa chủ nhiệm lớp nào trong kì
def get_teacher_nonehr():
    present_semester = get_present_semester()
    return db.session.query(Teacher, User) \
        .outerjoin(User, Teacher.user_id == User.id) \
        .outerjoin(SchoolClass, SchoolClass.homeroom_teacher_id == Teacher.id) \
        .filter(
        and_(
            SchoolClass.homeroom_teacher_id == None,
            #SchoolClass.semester_id == present_semester.id
        )
    ) \
        .all()

# Lấy học kì hiện tại
def get_present_semester():
    current_date = datetime.now()  # Lấy ngày hiện tại
    return db.session.query(Semester).filter(
        and_(
            Semester.start_day < current_date,
            Semester.end_day > current_date
        )
    ).first()


# Lấy học kì vừa rồi
def get_previous_semester():
    present_semester = get_present_semester()
    return db.session.query(Semester).filter(
        Semester.end_day < present_semester.start_day
    ).order_by(Semester.end_day.desc()).first()


# Lấy học sinh chưa được phân lớp trong kì theo khối
def get_unassigned_students(grade_id):
    semester = get_present_semester()
    return (db.session.query(Student)
            .outerjoin(Student_Schoolclass, Student.id == Student_Schoolclass.student_id)
            .outerjoin(SchoolClass, Student_Schoolclass.class_id == SchoolClass.id)
            .outerjoin(Grade, Grade.id == Student.grade_id)
            .filter(
        or_(
            Student_Schoolclass.class_id == None,
            SchoolClass.semester_id != semester.id
        )
    ).all())


# Lấy danh sách lớp chưa full trong kì
def get_classes_not_full(grade_id):
    semester = get_present_semester()
    return db.session.query(SchoolClass).filter(
        and_(
            SchoolClass.grade_id == grade_id,
            SchoolClass.semester_id == semester.id,
            SchoolClass.student_count < db.session.query(Rule).first().si_so_toi_da  # So sánh sĩ số hiện tại
        )
    ).all()


# Phân lớp từ dữ liệu lớp cũ
def set_class_from_old(grade_id):
    present_semester = get_present_semester()
    if present_semester.name==2:
        new_grade_id=grade_id
    else:
        new_grade_id=grade_id+1

    previous_semester = get_previous_semester()
    if not previous_semester:
        return "Không tìm thấy học kỳ trước!"

    # Lấy danh sách lớp từ học kỳ 1
    previous_classes = db.session.query(SchoolClass).filter(
        SchoolClass.semester_id == previous_semester.id,
        SchoolClass.grade_id == grade_id
    ).all()

    # Tạo lại lớp nếu chưa tồn tại ở kỳ hiện tại
    for cls in previous_classes:
        if present_semester.name == 2:
            new_teacher_id = cls.homeroom_teacher_id
        else:
            teachers=get_teacher_nonehr()
            if teachers:  # Kiểm tra nếu danh sách không rỗng
                new_teacher_id = teachers[0].id
            else:
                # Xử lý trường hợp danh sách rỗng (ví dụ: thông báo lỗi hoặc gán giá trị mặc định)
                new_teacher_id = None  # Hoặc giá trị mặc định khác tùy nhu cầu
        existing_class = db.session.query(SchoolClass).filter(
            SchoolClass.name == cls.name,
            SchoolClass.grade_id == new_grade_id,
            SchoolClass.semester_id == present_semester.id
        ).first()
        if not existing_class:
            new_class = SchoolClass(
                name=cls.name,
                grade_id=cls.grade_id,
                semester_id=present_semester.id,
                homeroom_teacher_id=new_teacher_id,
                student_count=cls.student_count
            )
            db.session.add(new_class)
            db.session.commit()

    # Lấy danh sách học sinh chưa được phân lớp
    unassigned_students = get_unassigned_students(grade_id)

    for student in unassigned_students:
        # Kiểm tra lịch sử lớp cũ
        previous_class = db.session.query(Student_Schoolclass).join(
            SchoolClass, SchoolClass.id == Student_Schoolclass.class_id
        ).filter(
            Student_Schoolclass.student_id == student.id,
            SchoolClass.semester_id == previous_semester.id
        ).first()

        if previous_class:
            # Thêm học sinh vào lớp tương ứng
            present_class = db.session.query(SchoolClass).filter(
                SchoolClass.name == previous_class.schoolclass.name,
                SchoolClass.grade_id == previous_class.schoolclass.grade_id,
                SchoolClass.semester_id == present_semester.id
            ).first()
        else:
            # Thêm học sinh vào lớp chưa đủ sĩ số
            present_class = get_classes_not_full(grade_id)[0]

        # Cập nhật học sinh vào lớp
        if present_class:
            new_student_schoolclass = Student_Schoolclass(
                student_id=student.id,
                class_id=present_class.id
            )
            db.session.add(new_student_schoolclass)
            db.session.commit()
            if not present_class:
                present_class.student_count+=1
                db.session.commit()
        else:
            flash("Không còn lớp để thêm học sinh, hãy tiến hành tạo thủ công hoặc thay đổi quy định!", 'error')
    flash("Đã thêm các lớp thành công!", 'success')


# Phân lớp mới
def set_new_classes(grade_id):
    return


# Tạo lớp tự động
def add_classes_auto(grade_id):
    present_semester = get_present_semester()
    if present_semester.name == 2 or (present_semester.name == 1
                                     and db.session.query(Grade).filter(Grade.id==grade_id).first().name != 10):
        if get_unassigned_students(grade_id):
            set_class_from_old(grade_id)
        else:
            flash("Tất cả học sinh đều đã được thêm vào lớp!", 'error')
    else:
        set_new_classes(grade_id)