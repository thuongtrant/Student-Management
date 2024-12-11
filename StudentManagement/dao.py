from sqlalchemy import func

from models import Student


def load_students(kw=None, page=1):
    query = Student.query

    if kw:
        query = query.filter(
            func.concat(Student.last_name, " ", Student.first_name).contains(kw)
            # Tạo chuỗi họ tên học sinh để dò kw từ đó
        )

    # Sắp xếp tăng dần theo cột first_name
    query = query.order_by(Student.first_name)

    page_size = 10
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()
