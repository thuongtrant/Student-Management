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

    # Danh sách giáo viên
    add_user('TEACHER', 'teacher_huy', 'Trần Thanh', 'Huy',
             '0909090906', 'tranthanhhuy@ou.edu.vn', 'images/user_image/user_3.jpg', 'Nam', '20011995')

    add_user('TEACHER', 'teacher_mai', 'Nguyễn Thị', 'Mai',
             '0909090905', 'nguyenthimai@ou.edu.vn', 'images/user_image/user_4.jpg', 'Nữ', '14081988')

    add_user('TEACHER', 'teacher_long', 'Phạm Hoàng', 'Long',
             '0909090904', 'phamhoanglong@ou.edu.vn', 'images/user_image/user_5.jpg', 'Nam', '23071992')

    add_user('TEACHER', 'teacher_anh', 'Đỗ Minh', 'Anh',
             '0909090903', 'dominhanh@ou.edu.vn', 'images/user_image/user_6.jpg', 'Nam', '10042000')

    add_user('TEACHER', 'teacher_thao', 'Lê Thị', 'Thảo',
             '0909090902', 'lethithao@ou.edu.vn', 'images/user_image/user_7.jpg', 'Nữ', '01101985')

    add_user('TEACHER', 'teacher_khanh', 'Nguyễn Phương', 'Khánh',
             '0909090901', 'nguyenphuongkhanh@ou.edu.vn', 'images/user_image/user_8.jpg', 'Nữ', '15071990')

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