from StudentManagement import app
from StudentManagement.create_base import add_subject
from create_base import add_user

with app.app_context():
    # Code tạo account mới
    add_user('ADMIN', 'admin_tu', 'Võ Minh Cẩm', 'Tú',
             '0909090909', '2251052132tu@ou.edu.vn', 'images/user_image/user_1.jpg', 'Nữ', '10052004')

    add_user('TEACHER', 'teacher', 'Nguyễn Văn', 'A',
             '0909090908', 'nguyenvana@ou.edu.vn', 'images/user_image/user_2.jpg', 'Nam', '01122000')

    add_user('EMPLOYEE', 'employee', 'Lê Thị', 'B',
             '0909090907', 'lethib@ou.edu.vn', 'images/user_image/user_1.jpg', 'Nữ', '29101997')

    # Code tạo subject mới
    add_subject('MATH','Toán','')
    add_subject('LITE','Ngữ Văn','')
    add_subject('ENG','Anh Văn','')
    add_subject('HIS','Lịch Sử','')
    add_subject('PHYS','Vật Lí','')
    add_subject('CHEM','Hóa Học','')
    add_subject('CE','Giáo Dục Công Dân','')
    add_subject('BIO','Sinh Học','')
    add_subject('PE','Thể Dục','')
    add_subject('GEO','Địa Lí','')
    add_subject('IFM','Tin Học','')
    add_subject('TECH','Công Nghệ','')