from create_user_base import add_user
from StudentManagement import app

with app.app_context():
    add_user('ADMIN', 'admin_tu', 'Võ Minh Cẩm', 'Tú',
             '0909090909', '2251052132tu@ou.edu.vn', 'images/user_image/user_1.jpg', 'Nữ', '10052004')

    add_user('TEACHER', 'teacher', 'Nguyễn Văn', 'A',
             '0909090908', 'nguyenvana@ou.edu.vn', 'images/user_image/user_2.jpg', 'Nam', '01122000')

    add_user('EMPLOYEE', 'employee', 'Lê Thị', 'B',
             '0909090907', 'lethib@ou.edu.vn', 'images/user_image/user_1.jpg', 'Nữ', '29101997')
