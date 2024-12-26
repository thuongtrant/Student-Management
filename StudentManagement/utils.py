from datetime import datetime

import bcrypt
from flask import flash
from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError

from StudentManagement import db
from models import User, Subject, Teacher, SchoolClass, Rule, Semester, Grade, Student, Student_Schoolclass, \
    Teacher_Schoolclass


def check_login(username, password):
    if username and password:
        # Tìm người dùng trong cơ sở dữ liệu
        user = User.query.filter_by(username=username.strip()).first()

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user  # Trả về đối tượng người dùng nếu mật khẩu hợp lệ
    return None


# Trả về danh sách học sinh kèm lớp
def load_students(kw=None, page=1):
    query = (
        Student.query
        .join(Student_Schoolclass, Student.id == Student_Schoolclass.student_id)
        .join(SchoolClass, SchoolClass.id == Student_Schoolclass.class_id)
        .join(Grade, Grade.id == SchoolClass.grade_id)
        .filter(SchoolClass.semester_id == get_present_semester().id)
    )

    # Lọc theo từ khóa nếu có
    if kw:
        query = query.filter(
            func.concat(Student.last_name, " ", Student.first_name).contains(kw)
        )

    # Sắp xếp theo tên học sinh
    query = query.order_by(Student.first_name)

    # Phân trang
    page_size = 10
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    # Lấy danh sách học sinh, lớp và khối
    return query.with_entities(
        Student.id,
        Student.first_name,
        Student.last_name,
        SchoolClass.name.label('class_name'),  # Tên lớp
        Grade.name.label('grade_name')  # Tên khối
    ).all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# Lấy môn học theo ID
def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)


def get_all_subjects_only():
    return db.session.query(Subject).all()


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


# Lay danh sach hoc sinh ma giao vien chu nhiem
def get_students_by_teacherid(teacher_id):
    return db.session.query(Student) \
        .join(Student_Schoolclass, Student_Schoolclass.student_id == Student.id) \
        .join(SchoolClass, Student_Schoolclass.class_id == SchoolClass.id) \
        .filter(teacher_id == SchoolClass.homeroom_teacher_id, SchoolClass.semester_id == get_present_semester().id) \
        .order_by(Student.first_name).all()


# Hàm lấy danh sách tất cả lớp học trong học kì
def get_all_classes_this_semester():
    return db.session.query(SchoolClass, Grade, Teacher, User) \
        .join(Grade, SchoolClass.grade_id == Grade.id) \
        .join(Teacher, SchoolClass.homeroom_teacher_id == Teacher.id) \
        .join(User, Teacher.user_id == User.id) \
        .filter(SchoolClass.semester_id == get_present_semester().id) \
        .all()


# Lấy danh sách học sinh theo lớp
def get_student_by_classid(class_id):
    return db.session.query(Student) \
        .outerjoin(Student_Schoolclass, Student_Schoolclass.student_id == Student.id) \
        .filter(Student_Schoolclass.class_id == class_id) \
        .order_by(Student.first_name).all()


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


# Lấy danh sách giáo viên chưa chủ nhiệm lớp nào trong kì
def get_teacher_nonehr():
    present_semester = get_present_semester()  # Lấy học kỳ hiện tại

    # Lấy tất cả giáo viên
    teachers = db.session.query(Teacher, User).join(User, Teacher.user_id == User.id).all()

    # Lấy danh sách giáo viên đã làm chủ nhiệm trong học kỳ hiện tại
    teachers_assigned_to_class = db.session.query(Teacher, User) \
        .join(SchoolClass, SchoolClass.homeroom_teacher_id == Teacher.id) \
        .join(User, Teacher.user_id == User.id) \
        .filter(SchoolClass.semester_id == present_semester.id).all()

    # Lọc danh sách giáo viên chưa làm chủ nhiệm (tất cả giáo viên - giáo viên đã làm chủ nhiệm)
    teachers_without_class = [teacher_user for teacher_user in teachers if
                              teacher_user not in teachers_assigned_to_class]

    # Trả về danh sách giáo viên chưa làm chủ nhiệm dưới dạng đối tượng Teacher và User
    return teachers_without_class


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
    semester = get_present_semester()  # Lấy học kỳ hiện tại

    # Lấy tất cả học sinh của khối
    all_students = db.session.query(Student).filter(Student.grade_id == grade_id).all()

    # Lấy danh sách học sinh đã phân lớp trong học kỳ hiện tại
    students_assigned_to_class = db.session.query(Student) \
        .join(Student_Schoolclass, Student.id == Student_Schoolclass.student_id) \
        .join(SchoolClass, Student_Schoolclass.class_id == SchoolClass.id) \
        .filter(SchoolClass.semester_id == semester.id, Student.grade_id == grade_id).all()

    # Lọc danh sách học sinh chưa phân lớp (tất cả học sinh - học sinh đã phân lớp)
    unassigned_students = [student for student in all_students if student not in students_assigned_to_class]

    # Trả về danh sách học sinh chưa phân lớp
    return unassigned_students


# Hàm thêm lớp học mới
def create_new_class(grade_id, homeroom_teacher_id, student_count, description):
    try:
        quy_dinh = Rule.query.first()
        if student_count > quy_dinh.si_so_toi_da or student_count < quy_dinh.si_so_toi_thieu:
            flash(f'Sĩ số lớp không được vượt quá {quy_dinh.si_so_toi_da} hay nhỏ hơn {quy_dinh.si_so_toi_thieu}',
                  'error')
        else:
            semester = get_present_semester()

            # Lấy danh sách các lớp hiện tại trong học kỳ và kiểm tra tên lớp đã tồn tại
            existing_classes = db.session.query(SchoolClass).filter(
                and_(
                    SchoolClass.grade_id == grade_id,
                    SchoolClass.semester_id == semester.id
                )
            ).all()

            # Lấy danh sách tên lớp hiện tại
            existing_class_numbers = set([cls.name for cls in existing_classes])

            # Tạo tên lớp mới bằng cách tìm số lớp chưa tồn tại
            class_number = 1  # Bắt đầu từ lớp 1
            while class_number in existing_class_numbers:
                class_number += 1  # Tăng tên lớp lên nếu lớp này đã tồn tại

            # Tạo lớp mới
            new_class = SchoolClass(
                name=str(class_number),  # Tên lớp là số nguyên
                grade_id=grade_id,
                semester_id=semester.id,
                homeroom_teacher_id=homeroom_teacher_id,
                student_count=student_count,
                description=description
            )
            db.session.add(new_class)
            db.session.commit()

            # Thêm giáo viên chủ nhiệm vào lớp
            new_teacher_schoolclass = Teacher_Schoolclass(
                teacher_id=homeroom_teacher_id,
                class_id=new_class.id,
                semester_id=semester.id,
                subject_id=db.session.query(Teacher).filter(Teacher.id == homeroom_teacher_id).first().subject_id
            )
            db.session.add(new_teacher_schoolclass)
            db.session.commit()

            flash('Lớp học đã được thêm thành công!')
            return new_class
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra: {str(e)}', 'error')
        return False


def create_new_classes(grade_id, total_classes_needed):
    present_semester = get_present_semester()
    existing_classes = db.session.query(SchoolClass).filter(
        SchoolClass.semester_id == present_semester.id,
        SchoolClass.grade_id == grade_id
    ).all()

    # Kiểm tra số lượng học sinh chưa được phân lớp
    unassigned_students = get_unassigned_students(grade_id)
    rules = db.session.query(Rule).first()
    min_students = rules.si_so_toi_thieu
    max_students = rules.si_so_toi_da

    # Tính tổng số slot trống trong các lớp hiện tại
    total_available_slots = sum(max_students - cls.student_count for cls in existing_classes)

    if len(unassigned_students) <= total_available_slots:
        flash(f"Chỉ còn {len(unassigned_students)} học sinh chưa phân lớp. Sẽ phân bổ đều vào các lớp hiện có.", 'info')
        return existing_classes  # Không tạo thêm lớp mới, trả về danh sách lớp hiện tại

    # Tiếp tục tạo lớp nếu số slot hiện tại không đủ
    class_numbers = set([cls.name for cls in existing_classes])  # Lấy danh sách tên lớp hiện tại
    new_class_number = 1  # Bắt đầu từ lớp 1
    created_classes = []

    for _ in range(total_classes_needed):
        # Kiểm tra lớp có tên đã tồn tại chưa, nếu có thì tăng tên lớp lên
        while new_class_number in class_numbers:
            new_class_number += 1  # Bỏ qua các lớp đã tồn tại

        # Kiểm tra số lượng giáo viên chủ nhiệm còn lại
        unassigned_teachers_count = len(get_teacher_nonehr())
        if total_classes_needed > unassigned_teachers_count:
            flash(f"Không đủ giáo viên chủ nhiệm để tạo {total_classes_needed} lớp!", 'error')
            return existing_classes  # Không tạo thêm lớp nếu thiếu giáo viên

        # Lấy giáo viên chủ nhiệm từ danh sách (trích xuất Teacher từ tuple)
        teacher_user = get_teacher_nonehr().pop(0)  # Trả về (Teacher, User)
        homeroom_teacher = teacher_user[0]  # Teacher là phần tử đầu tiên của tuple

        # Tạo lớp mới
        new_class = SchoolClass(
            name=new_class_number,
            grade_id=grade_id,
            semester_id=present_semester.id,
            homeroom_teacher_id=homeroom_teacher.id,
            student_count=0
        )
        db.session.add(new_class)
        created_classes.append(new_class)
        class_numbers.add(new_class_number)  # Thêm tên lớp vào danh sách đã có
        new_class_number += 1  # Tăng tên lớp cho lần sau
        db.session.commit()

        # Thêm giáo viên chủ nhiệm vào lớp
        new_teacher_schoolclass = Teacher_Schoolclass(
            teacher_id=homeroom_teacher.id,
            class_id=new_class.id,
            semester_id=present_semester.id,
            subject_id=db.session.query(Teacher).filter(Teacher.id == homeroom_teacher.id).first().subject_id
        )
        db.session.add(new_teacher_schoolclass)
        db.session.commit()

    db.session.commit()  # Lưu các lớp mới vào cơ sở dữ liệu
    return existing_classes + created_classes  # Trả về danh sách lớp cũ + lớp mới


def assign_students_to_class(class_id, student_ids):
    try:
        # Tìm lớp học
        school_class = db.session.query(SchoolClass).filter(SchoolClass.id == class_id).first()
        if not school_class:
            return False

        # Kiểm tra sĩ số lớp trước khi gán
        quy_dinh = Rule.query.first()
        if school_class.student_count + len(student_ids) > quy_dinh.si_so_toi_da:
            return False

        # Gán học sinh vào lớp
        for student_id in student_ids:
            new_assignment = Student_Schoolclass(student_id=student_id, class_id=class_id)
            db.session.add(new_assignment)
            school_class.student_count += 1
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash(f"Đã xảy ra lỗi khi gán học sinh vào lớp: {str(e)}", 'error')
        return False


# Thêm học sinh vào các lớp đã tạo
def add_students_to_classes(grade_id, unassigned_students, created_classes, max_students, min_students):
    remaining_students = unassigned_students[:]
    active_classes = created_classes[:]  # Danh sách các lớp có thể nhận thêm học sinh

    print(f"Initial unassigned students: {len(remaining_students)}")
    print(f"Initial classes: {[cls.name for cls in active_classes]}")

    student_idx = 0  # Chỉ số học sinh
    while remaining_students and active_classes:
        # Tìm lớp hiện tại để gán học sinh
        current_class_idx = student_idx % len(active_classes)
        school_class = active_classes[current_class_idx]

        # Kiểm tra nếu lớp đạt sĩ số tối đa
        if school_class.student_count >= max_students:
            print(
                f"Class {school_class.name} reached max_students ({school_class.student_count}). Removing from active_classes.")
            active_classes.pop(current_class_idx)  # Loại bỏ lớp khỏi danh sách
            continue

        # Gán học sinh vào lớp
        student = remaining_students.pop(0)  # Lấy học sinh từ đầu danh sách
        assign_students_to_class(school_class.id, [student.id])

        # Ghi log thông tin gán học sinh
        print(
            f"Assigned student {student.id} to class {school_class.name}. Current count: {school_class.student_count}")

        # Chuyển sang học sinh tiếp theo
        student_idx += 1

    # Ghi log sau khi vòng lặp kết thúc
    print(f"Remaining students after loop: {len(remaining_students)}")
    print(f"Classes status after loop:")
    for cls in created_classes:
        print(f"  - Class {cls.name}: {cls.student_count} students")

    # Nếu vẫn còn học sinh chưa được phân lớp
    if remaining_students:
        print(f"Warning: {len(remaining_students)} students remain unassigned.")


# Tạo lớp và phân học sinh cho khối 10 học kỳ 1
def set_class_from_new(grade_id):
    unassigned_students = get_unassigned_students(grade_id)
    rules = db.session.query(Rule).first()
    min_students = rules.si_so_toi_thieu
    max_students = rules.si_so_toi_da

    # Tính số lớp cần tạo
    unassigned_students_count = len(unassigned_students)
    total_classes_needed = unassigned_students_count // min_students  # Số lớp cần thiết theo min_students

    # Sắp xếp danh sách học sinh
    unassigned_students = sorted(unassigned_students, key=lambda x: x.first_name)

    # Tạo các lớp mới
    created_classes = create_new_classes(grade_id, total_classes_needed)

    # Phân học sinh vào các lớp đã tạo
    add_students_to_classes(grade_id, unassigned_students, created_classes, max_students, min_students)


# Tạo lớp mới và phân toàn bộ học sinh
def add_classes_auto(grade_id):
    present_semester = get_present_semester()
    grade = db.session.query(Grade).filter(Grade.id == grade_id).first()

    # Lấy danh sách học sinh chưa được phân lớp
    unassigned_students = get_unassigned_students(grade_id)

    if not unassigned_students:
        flash("Tất cả học sinh đã được phân lớp!", 'success')
        return

    # Xử lý theo logic học kỳ và khối
    if present_semester.name == 2:
        # Học kỳ 2: Tạo lớp mới dựa trên dữ liệu cũ
        # set_class_from_old(grade_id)
        return
    elif (present_semester.name == 1 and (grade.name == 11 or grade.name == 12)):
        # set_class_from_old(grade_id)
        return
    else:
        # Khối 10 hoặc học sinh mới, tạo lớp hoàn toàn mới
        set_class_from_new(grade_id)

    # Nếu còn học sinh chưa được phân lớp, thêm vào các lớp chưa đầy
    unassigned_students = get_unassigned_students(grade_id)
    if unassigned_students:
        flash("Có học sinh chưa được phân lớp, kiểm tra quy định hoặc tạo thêm lớp thủ công!", 'error')
    else:
        flash("Đã phân lớp cho tất cả học sinh", 'success')
