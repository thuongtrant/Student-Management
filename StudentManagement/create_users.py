from create_user_base import add_user
from StudentManagement import app

with app.app_context():
    add_user('ADMIN','admin_tu','Abc123','admin1','Võ Minh Cẩm','Tú',
             '0909090909','2251052132tu@ou.edu.vn','images/user_image/user_1.jpg','Female',2004)

    add_user('TEACHER', 'teacher', 'Abc123', 'teacher1', 'Nguễn Văn', 'A',
             '0909090908', 'nguyenvana@ou.edu.vn', 'images/user_image/user_2.jpg', 'Male', 2000)

    add_user('EMPLOYEE', 'employee', 'Abc123', 'employee1', 'Lê Thị', 'B',
             '0909090907', 'lethib@ou.edu.vn', 'images/user_image/user_1.jpg', 'Female', 1997)