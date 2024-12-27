from StudentManagement import app
from create_base import add_user, add_subject, add_grade, add_semester, add_student_db, class_db, student_class_db

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
    add_user('TEACHER', 'teacher_hieu', 'Lê Thanh', 'Hiếu',
             '0909090918', 'lethanhhieu@ou.edu.vn', 'images/user_image/user_20.jpg', 'Nam', '02021996')
    add_user('TEACHER', 'teacher_tien', 'Trần Thiện', 'Tiến',
             '0909090919', 'tranthientien@ou.edu.vn', 'images/user_image/user_21.jpg', 'Nam', '13031995')
    add_user('TEACHER', 'teacher_phu', 'Nguyễn Phúc', 'Phú',
             '0909090920', 'nguyenphucphu@ou.edu.vn', 'images/user_image/user_22.jpg', 'Nam', '22011993')
    add_user('TEACHER', 'teacher_dan', 'Bùi Minh', 'Dân',
             '0909090921', 'buiminhdan@ou.edu.vn', 'images/user_image/user_23.jpg', 'Nam', '17041993')
    add_user('TEACHER', 'teacher_yen', 'Lê Thu', 'Yến',
             '0909090922', 'lethuyen@ou.edu.vn', 'images/user_image/user_24.jpg', 'Nữ', '11051992')
    add_user('TEACHER', 'teacher_tuoi', 'Đoàn Văn', 'Tuổi',
             '0909090923', 'doanvantuoi@ou.edu.vn', 'images/user_image/user_25.jpg', 'Nam', '21031991')
    add_user('TEACHER', 'teacher_van', 'Nguyễn Phan', 'Vân',
             '0909090924', 'nguyenphanvan@ou.edu.vn', 'images/user_image/user_26.jpg', 'Nữ', '07071990')
    add_user('TEACHER', 'teacher_mai1', 'Phạm Lan', 'Mai',
             '0909090925', 'phamlanmai@ou.edu.vn', 'images/user_image/user_27.jpg', 'Nữ', '14081994')
    add_user('TEACHER', 'teacher_bao', 'Trần Thiên', 'Bảo',
             '0909090926', 'tranthienbao@ou.edu.vn', 'images/user_image/user_28.jpg', 'Nam', '18091989')
    add_user('TEACHER', 'teacher_tri', 'Lê Quang', 'Trí',
             '0909090927', 'lequangtri@ou.edu.vn', 'images/user_image/user_29.jpg', 'Nam', '25051993')
    add_user('TEACHER', 'teacher_quang', 'Nguyễn Minh', 'Quang',
             '0909090928', 'nguyenminhquang@ou.edu.vn', 'images/user_image/user_30.jpg', 'Nam', '12041992')
    add_user('TEACHER', 'teacher_thien', 'Trương Hữu', 'Thiện',
             '0909090929', 'truonghuuthiện@ou.edu.vn', 'images/user_image/user_31.jpg', 'Nam', '19031991')
    add_user('TEACHER', 'teacher_ngoc', 'Phan Minh', 'Ngọc',
             '0909090930', 'phanminhngoc@ou.edu.vn', 'images/user_image/user_32.jpg', 'Nữ', '04041994')
    add_user('TEACHER', 'teacher_thao1', 'Nguyễn Thị', 'Thảo',
             '0909090931', 'nguyenthithao@ou.edu.vn', 'images/user_image/user_33.jpg', 'Nữ', '21081990')
    add_user('TEACHER', 'teacher_dung', 'Nguyễn Bảo', 'Dũng',
             '0909090932', 'nguyenbaodung@ou.edu.vn', 'images/user_image/user_34.jpg', 'Nam', '06061992')
    add_user('TEACHER', 'teacher_hien', 'Trần Hữu', 'Hiền',
             '0909090933', 'tranhuuhien@ou.edu.vn', 'images/user_image/user_35.jpg', 'Nam', '25081991')
    add_user('TEACHER', 'teacher_kim', 'Nguyễn Thi', 'Kim',
             '0909090934', 'nguyenthikim@ou.edu.vn', 'images/user_image/user_36.jpg', 'Nữ', '13061994')
    add_user('TEACHER', 'teacher_quyen', 'Lê Thanh', 'Quyên',
             '0909090935', 'lethanhquyen@ou.edu.vn', 'images/user_image/user_37.jpg', 'Nữ', '09091991')
    add_user('TEACHER', 'teacher_hieu1', 'Trần Quang', 'Hiếu',
             '0909090936', 'tranquanghieu@ou.edu.vn', 'images/user_image/user_38.jpg', 'Nam', '20031990')

    # Code tạo subject mới
    add_subject('MATH', 'Toán', '')
    add_subject('LITE', 'Ngữ Văn', '')
    add_subject('ENG', 'Anh Văn', '')
    add_subject('HIS', 'Lịch Sử', '')
    add_subject('PHYS', 'Vật Lí', '')
    add_subject('CHEM', 'Hóa Học', '')
    add_subject('CE', 'Giáo Dục Công Dân', '')
    add_subject('BIO', 'Sinh Học', '')
    add_subject('PE', 'Thể Dục', '')
    add_subject('GEO', 'Địa Lí', '')
    add_subject('IFM', 'Tin Học', '')
    add_subject('TECH', 'Công Nghệ', '')

    # Code tạo khối
    add_grade('10')
    add_grade('11')
    add_grade('12')

    # Code tạo học kì
    add_semester('1', '20230905', '20240125')
    add_semester('2', '20240210', '20240601')
    add_semester('1', '20240901', '20250202')

    # Tạo sẵn cơ sở dữ liệu
    # Khối 10
    add_student_db('An', 'Nguyễn Văn', '20090915', 'Nam', '0900000001', 'vanan1@example.com', '123 Đường A', 1,
                   'user_1.jpg')
    add_student_db('Bích', 'Trần Thị', '20090512', 'Nữ', '0900000002', 'thibich2@example.com', '123 Đường B', 1,
                   'user_2.jpg')
    add_student_db('Cường', 'Lê Hữu', '20090625', 'Nam', '0900000003', 'huucuong3@example.com', '123 Đường C', 1,
                   'user_1.jpg')
    add_student_db('Diễm', 'Phạm Ngọc', '20090407', 'Nữ', '0900000004', 'ngocdiem4@example.com', '123 Đường D', 1,
                   'user_2.jpg')
    add_student_db('Dũng', 'Hoàng Anh', '20090720', 'Nam', '0900000005', 'anhdung5@example.com', '123 Đường E', 1,
                   'user_1.jpg')
    add_student_db('Hiển', 'Vũ Thế', '20090218', 'Nam', '0900000006', 'thehien6@example.com', '123 Đường F', 1,
                   'user_2.jpg')
    add_student_db('Hòa', 'Bùi Minh', '20090904', 'Nam', '0900000007', 'minhhoa7@example.com', '123 Đường G', 1,
                   'user_1.jpg')
    add_student_db('Hương', 'Đặng Thu', '20090530', 'Nữ', '0900000008', 'thuhuong8@example.com', '123 Đường H', 1,
                   'user_2.jpg')
    add_student_db('Huy', 'Đỗ Gia', '20090815', 'Nam', '0900000009', 'giahuy9@example.com', '123 Đường I', 1,
                   'user_1.jpg')
    add_student_db('Kiên', 'Ngô Chí', '20090310', 'Nam', '0900000010', 'chikien10@example.com', '123 Đường J', 1,
                   'user_2.jpg')
    add_student_db('Bảo', 'Vũ Quốc', '20090715', 'Nam', '0900000061', 'quocbao61@example.com', '123 Đường F', 1,
                   'user_1.jpg')
    add_student_db('Châu', 'Bùi Minh', '20090518', 'Nữ', '0900000062', 'minhchau62@example.com', '123 Đường G', 1,
                   'user_2.jpg')
    add_student_db('Công', 'Đặng Chí', '20090602', 'Nam', '0900000063', 'chicong63@example.com', '123 Đường H', 1,
                   'user_1.jpg')
    add_student_db('Hân', 'Đỗ Gia', '20090414', 'Nữ', '0900000064', 'giah64@example.com', '123 Đường I', 1,
                   'user_2.jpg')
    add_student_db('Hoàng', 'Ngô Huy', '20090819', 'Nam', '0900000065', 'huyhoang65@example.com', '123 Đường J', 1,
                   'user_1.jpg')
    add_student_db('Lan', 'Nguyễn Thị', '20090508', 'Nữ', '0900000066', 'thilan66@example.com', '123 Đường K', 1,
                   'user_2.jpg')
    add_student_db('Mạnh', 'Trần Văn', '20090725', 'Nam', '0900000067', 'vanmanh67@example.com', '123 Đường L', 1,
                   'user_1.jpg')
    add_student_db('Nga', 'Lê Ngọc', '20090422', 'Nữ', '0900000068', 'ngocnga68@example.com', '123 Đường M', 1,
                   'user_2.jpg')
    add_student_db('Tuấn', 'Phạm Anh', '20090903', 'Nam', '0900000069', 'anhtuan69@example.com', '123 Đường N', 1,
                   'user_1.jpg')
    add_student_db('Việt', 'Hoàng Văn', '20090613', 'Nam', '0900000070', 'vanviet70@example.com', '123 Đường O', 1,
                   'user_2.jpg')
    add_student_db('Anh', 'Nguyễn Phương', '20090811', 'Nữ', '0900000121', 'phuonganh121@example.com', '123 Đường K',
                   1, 'user_1.jpg')
    add_student_db('Đăng', 'Trần Hải', '20090504', 'Nam', '0900000122', 'haidang122@example.com', '123 Đường L', 1,
                   'user_2.jpg')
    add_student_db('Duyên', 'Lê Mỹ', '20090723', 'Nữ', '0900000123', 'myduyen123@example.com', '123 Đường M', 1,
                   'user_1.jpg')
    add_student_db('Phát', 'Nguyễn Tấn', '20090615', 'Nam', '0900000124', 'tanphat124@example.com', '123 Đường N', 1,
                   'user_2.jpg')
    add_student_db('Minh', 'Hoàng Ngọc', '20090930', 'Nữ', '0900000125', 'ngocminh125@example.com', '123 Đường O', 1,
                   'user_1.jpg')
    add_student_db('Bình', 'Vũ Huy', '20090701', 'Nam', '0900000126', 'huybinh126@example.com', '123 Đường P', 1,
                   'user_2.jpg')
    add_student_db('Hà', 'Bùi Thu', '20090818', 'Nữ', '0900000127', 'thuha127@example.com', '123 Đường Q', 1,
                   'user_1.jpg')
    add_student_db('Khôi', 'Đặng Văn', '20090510', 'Nam', '0900000128', 'vankhoi128@example.com', '123 Đường R', 1,
                   'user_2.jpg')
    add_student_db('Lâm', 'Đỗ Ngọc', '20090915', 'Nam', '0900000129', 'ngoclam129@example.com', '123 Đường S', 1,
                   'user_1.jpg')
    add_student_db('Minh', 'Ngô Bảo', '20090425', 'Nữ', '0900000130', 'baominh130@example.com', '123 Đường T', 1,
                   'user_2.jpg')
    add_student_db('Trung', 'Nguyễn Văn', '20090910', 'Nam', '0900000131', 'vantrung131@example.com', '123 Đường A', 1,
                   'user_1.jpg')
    add_student_db('Hải', 'Trần Minh', '20090912', 'Nam', '0900000132', 'minhhai132@example.com', '123 Đường B', 1,
                   'user_2.jpg')
    add_student_db('Ly', 'Phạm Thị', '20090914', 'Nữ', '0900000133', 'thily133@example.com', '123 Đường C', 1,
                   'user_1.jpg')
    add_student_db('Khang', 'Lê Hữu', '20090916', 'Nam', '0900000134', 'huukhang134@example.com', '123 Đường D', 1,
                   'user_2.jpg')
    add_student_db('Thảo', 'Hoàng Anh', '20090918', 'Nữ', '0900000135', 'anhthao135@example.com', '123 Đường E', 1,
                   'user_1.jpg')
    add_student_db('Quang', 'Vũ Thế', '20090920', 'Nam', '0900000136', 'thequang136@example.com', '123 Đường F', 1,
                   'user_2.jpg')
    add_student_db('Trang', 'Bùi Thu', '20090922', 'Nữ', '0900000137', 'thutrang137@example.com', '123 Đường G', 1,
                   'user_1.jpg')
    add_student_db('Tú', 'Đặng Văn', '20090924', 'Nam', '0900000138', 'vantuu138@example.com', '123 Đường H', 1,
                   'user_2.jpg')
    add_student_db('Hùng', 'Đỗ Gia', '20090926', 'Nam', '0900000139', 'giahung139@example.com', '123 Đường I', 1,
                   'user_1.jpg')
    add_student_db('Mai', 'Ngô Chí', '20090928', 'Nữ', '0900000140', 'chimai140@example.com', '123 Đường J', 1,
                   'user_2.jpg')
    add_student_db('Vy', 'Nguyễn Lan', '20090902', 'Nữ', '0900000141', 'lanvy141@example.com', '123 Đường K', 1,
                   'user_1.jpg')
    add_student_db('Dương', 'Trần Thị', '20090904', 'Nam', '0900000142', 'thiduong142@example.com', '123 Đường L', 1,
                   'user_2.jpg')
    add_student_db('Lợi', 'Phạm Ngọc', '20090906', 'Nam', '0900000143', 'ngocloi143@example.com', '123 Đường M', 1,
                   'user_1.jpg')
    add_student_db('Tâm', 'Lê Thị', '20090908', 'Nữ', '0900000144', 'thitam144@example.com', '123 Đường N', 1,
                   'user_2.jpg')
    add_student_db('Hạnh', 'Hoàng Minh', '20090930', 'Nữ', '0900000145', 'minhhanh145@example.com', '123 Đường O', 1,
                   'user_1.jpg')
    add_student_db('Đức', 'Vũ Quốc', '20090905', 'Nam', '0900000146', 'quocduc146@example.com', '123 Đường P', 1,
                   'user_2.jpg')
    add_student_db('Phúc', 'Bùi Thế', '20090907', 'Nam', '0900000147', 'thephuc147@example.com', '123 Đường Q', 1,
                   'user_1.jpg')
    add_student_db('Linh', 'Đặng Thu', '20090909', 'Nữ', '0900000148', 'thulinh148@example.com', '123 Đường R', 1,
                   'user_2.jpg')
    add_student_db('Ngọc', 'Đỗ Thị', '20090911', 'Nữ', '0900000149', 'thingoc149@example.com', '123 Đường S', 1,
                   'user_1.jpg')
    add_student_db('Thanh', 'Ngô Bảo', '20090913', 'Nam', '0900000150', 'baothanh150@example.com', '123 Đường T', 1,
                   'user_2.jpg')
    add_student_db('Yến', 'Nguyễn Hoàng', '20090915', 'Nữ', '0900000151', 'hoangyen151@example.com', '123 Đường U', 1,
                   'user_1.jpg')
    add_student_db('Văn', 'Trần Văn', '20090917', 'Nam', '0900000152', 'vanvan152@example.com', '123 Đường V', 1,
                   'user_2.jpg')
    add_student_db('Quỳnh', 'Phạm Thu', '20090919', 'Nữ', '0900000153', 'thuquynh153@example.com', '123 Đường W', 1,
                   'user_1.jpg')
    add_student_db('Thành', 'Lê Văn', '20090921', 'Nam', '0900000154', 'vanthanh154@example.com', '123 Đường X', 1,
                   'user_2.jpg')
    add_student_db('Đan', 'Hoàng Ngọc', '20090923', 'Nữ', '0900000155', 'ngocdan155@example.com', '123 Đường Y', 1,
                   'user_1.jpg')
    add_student_db('Nhật', 'Vũ Huy', '20090925', 'Nam', '0900000156', 'huynhat156@example.com', '123 Đường Z', 1,
                   'user_2.jpg')
    add_student_db('Hà', 'Bùi Quốc', '20090927', 'Nữ', '0900000157', 'quocha157@example.com', '123 Đường AA', 1,
                   'user_1.jpg')
    add_student_db('Sơn', 'Đặng Văn', '20090929', 'Nam', '0900000158', 'vanson158@example.com', '123 Đường BB', 1,
                   'user_2.jpg')
    add_student_db('Tấn', 'Đỗ Minh', '20090903', 'Nam', '0900000159', 'minhtan159@example.com', '123 Đường CC', 1,
                   'user_1.jpg')
    add_student_db('Ngân', 'Ngô Bảo', '20090905', 'Nữ', '0900000160', 'baongan160@example.com', '123 Đường DD', 1,
                   'user_2.jpg')
    add_student_db('Tú', 'Nguyễn Quang', '20090920', 'Nam', '0909999301', 'quangtuvt1@example.com', '456 Đường A',
                   1, 'user_1.jpg')
    add_student_db('Vi', 'Lê Thị', '20091102', 'Nữ', '0909999302', 'thivi2@example.com', '456 Đường B', 1,
                   'user_2.jpg')
    add_student_db('Cảnh', 'Trần Thiên', '20091012', 'Nam', '0909999303', 'thiencanh3@example.com', '456 Đường C',
                   1, 'user_1.jpg')
    add_student_db('Chí', 'Nguyễn Thế', '20091215', 'Nam', '0909999304', 'thechi4@example.com', '456 Đường D', 1,
                   'user_2.jpg')
    add_student_db('Kiều', 'Phạm Thị', '20091128', 'Nữ', '0909999305', 'thikieu5@example.com', '456 Đường E', 1,
                   'user_1.jpg')
    add_student_db('Bảo', 'Trần Thị', '20090630', 'Nữ', '0909999306', 'thibao6@example.com', '456 Đường F', 1,
                   'user_2.jpg')
    add_student_db('Thanh', 'Lê Văn', '20091207', 'Nam', '0909999307', 'vathanh7@example.com', '456 Đường G', 1,
                   'user_1.jpg')
    add_student_db('Lan', 'Nguyễn Thị', '20090925', 'Nữ', '0909999308', 'thilan8@example.com', '456 Đường H', 1,
                   'user_2.jpg')
    add_student_db('Bình', 'Trần Hoàng', '20090605', 'Nam', '0909999309', 'hoangbinh9@example.com', '456 Đường I',
                   1, 'user_1.jpg')
    add_student_db('Sơn', 'Đỗ Minh', '20090822', 'Nam', '0909999310', 'minhson10@example.com', '456 Đường J', 1,
                   'user_1.jpg')
    add_student_db('Tâm', 'Nguyễn Minh', '20091116', 'Nữ', '0909999311', 'minhtam11@example.com', '456 Đường K', 1,
                   'user_1.jpg')
    add_student_db('Hòa', 'Phạm Quang', '20090701', 'Nam', '0909999312', 'quanghoa12@example.com', '456 Đường L',
                   1, 'user_2.jpg')
    add_student_db('Tuân', 'Trần Quốc', '20091001', 'Nam', '0909999313', 'quoctuan13@example.com', '456 Đường M',
                   1, 'user_1.jpg')
    add_student_db('Bích', 'Lê Minh', '20090610', 'Nữ', '0909999314', 'minhbich14@example.com', '456 Đường N', 1,
                   'user_1.jpg')
    add_student_db('Thi', 'Nguyễn Thanh', '20091204', 'Nữ', '0909999315', 'thanhthi15@example.com', '456 Đường O',
                   1, 'user_1.jpg')
    add_student_db('Duy', 'Hoàng Quang', '20091113', 'Nam', '0909999316', 'quangduy16@example.com', '456 Đường P',
                   1, 'user_1.jpg')
    add_student_db('Lâm', 'Đỗ Thanh', '20090813', 'Nam', '0909999317', 'thanhlam17@example.com', '456 Đường Q', 1,
                   'user_1.jpg')
    add_student_db('Mỹ', 'Nguyễn Hồng', '20091121', 'Nữ', '0909999318', 'hongmy18@example.com', '456 Đường R', 1,
                   'user_1.jpg')
    add_student_db('Ngọc', 'Lê Quốc', '20091202', 'Nữ', '0909999319', 'quocngoc19@example.com', '456 Đường S', 1,
                   'user_1.jpg')
    add_student_db('An', 'Nguyễn Thi', '20090930', 'Nam', '0909999320', 'thian20@example.com', '456 Đường T', 1,
                   'user_2.jpg')
    add_student_db('Quang', 'Trần Đăng', '20090718', 'Nam', '0909999321', 'dangquang21@example.com',
                   '456 Đường U', 1, 'user_1.jpg')
    add_student_db('Mai', 'Phạm Minh', '20090628', 'Nữ', '0909999322', 'minhmai22@example.com', '456 Đường V', 1,
                   'user_2.jpg')
    add_student_db('Vân', 'Nguyễn Thị', '20090916', 'Nữ', '0909999323', 'thivan23@example.com', '456 Đường W', 1,
                   'user_2.jpg')
    add_student_db('Khôi', 'Đặng Hoàng', '20090818', 'Nam', '0909999324', 'hoangkhoi24@example.com', '456 Đường X',
                   1, 'user_2.jpg')
    add_student_db('Vĩnh', 'Lê Thanh', '20090704', 'Nam', '0909999325', 'thanhvinh25@example.com', '456 Đường Y',
                   1, 'user_2.jpg')
    add_student_db('Thủy', 'Trần Mỹ', '20090923', 'Nữ', '0909999326', 'mythuy26@example.com', '456 Đường Z', 1,
                   'user_2.jpg')
    add_student_db('Cường', 'Nguyễn Phúc', '20091005', 'Nam', '0909999327', 'phuccuong27@example.com',
                   '456 Đường AA', 1, 'user_2.jpg')
    add_student_db('Hân', 'Lê Ngọc', '20090912', 'Nữ', '0909999328', 'ngochan28@example.com', '456 Đường AB', 1,
                   'user_2.jpg')
    add_student_db('Tính', 'Nguyễn Quốc', '20090623', 'Nam', '0909999329', 'quoctinh29@example.com',
                   '456 Đường AC', 1, 'user_2.jpg')
    add_student_db('Khoa', 'Trần Nhật', '20091210', 'Nam', '0909999330', 'nhatkhoa30@example.com', '456 Đường AD',
                   1, 'user_1.jpg')

    # Khối 11
    add_student_db('Quân', 'Nguyễn Văn', '20080910', 'Nam', '0900000161', 'vanquan161@example.com', '456 Đường A', 2,
                   'user_1.jpg')
    add_student_db('Vân', 'Trần Thị', '20080912', 'Nữ', '0900000162', 'thivan162@example.com', '456 Đường B', 2,
                   'user_2.jpg')
    add_student_db('Thành', 'Phạm Minh', '20080914', 'Nam', '0900000163', 'minhthanh163@example.com', '456 Đường C', 2,
                   'user_1.jpg')
    add_student_db('Lan', 'Lê Ngọc', '20080916', 'Nữ', '0900000164', 'ngoclan164@example.com', '456 Đường D', 2,
                   'user_2.jpg')
    add_student_db('Hùng', 'Hoàng Quốc', '20080918', 'Nam', '0900000165', 'quochung165@example.com', '456 Đường E', 2,
                   'user_1.jpg')
    add_student_db('Trang', 'Vũ Thị', '20080920', 'Nữ', '0900000166', 'thitrang166@example.com', '456 Đường F', 2,
                   'user_2.jpg')
    add_student_db('Duy', 'Bùi Minh', '20080922', 'Nam', '0900000167', 'minhduy167@example.com', '456 Đường G', 2,
                   'user_1.jpg')
    add_student_db('Nhung', 'Đặng Thị', '20080924', 'Nữ', '0900000168', 'thingnhung168@example.com', '456 Đường H', 2,
                   'user_2.jpg')
    add_student_db('Khánh', 'Đỗ Gia', '20080926', 'Nam', '0900000169', 'giakh169@example.com', '456 Đường I', 2,
                   'user_1.jpg')
    add_student_db('Bảo', 'Ngô Chí', '20080928', 'Nam', '0900000170', 'chibao170@example.com', '456 Đường J', 2,
                   'user_2.jpg')
    add_student_db('Yến', 'Nguyễn Hoàng', '20080902', 'Nữ', '0900000171', 'hoangyen171@example.com', '456 Đường K', 2,
                   'user_1.jpg')
    add_student_db('Tùng', 'Trần Văn', '20080904', 'Nam', '0900000172', 'vantung172@example.com', '456 Đường L', 2,
                   'user_2.jpg')
    add_student_db('Quỳnh', 'Phạm Thu', '20080906', 'Nữ', '0900000173', 'thuquynh173@example.com', '456 Đường M', 2,
                   'user_1.jpg')
    add_student_db('Thanh', 'Lê Bảo', '20080908', 'Nam', '0900000174', 'baothanh174@example.com', '456 Đường N', 2,
                   'user_2.jpg')
    add_student_db('Đan', 'Hoàng Ngọc', '20080930', 'Nữ', '0900000175', 'ngocdan175@example.com', '456 Đường O', 2,
                   'user_1.jpg')
    add_student_db('Đức', 'Vũ Quốc', '20080905', 'Nam', '0900000176', 'quocduc176@example.com', '456 Đường P', 2,
                   'user_2.jpg')
    add_student_db('Phúc', 'Bùi Hữu', '20080907', 'Nam', '0900000177', 'huuphuc177@example.com', '456 Đường Q', 2,
                   'user_1.jpg')
    add_student_db('Linh', 'Đặng Thu', '20080909', 'Nữ', '0900000178', 'thulinh178@example.com', '456 Đường R', 2,
                   'user_2.jpg')
    add_student_db('Ngọc', 'Đỗ Minh', '20080911', 'Nữ', '0900000179', 'minhngoc179@example.com', '456 Đường S', 2,
                   'user_1.jpg')
    add_student_db('Sơn', 'Ngô Bảo', '20080913', 'Nam', '0900000180', 'baoson180@example.com', '456 Đường T', 2,
                   'user_2.jpg')
    add_student_db('Ly', 'Nguyễn Văn', '20080915', 'Nữ', '0900000181', 'vanly181@example.com', '456 Đường U', 2,
                   'user_1.jpg')
    add_student_db('Vĩnh', 'Trần Minh', '20080917', 'Nam', '0900000182', 'minhvinh182@example.com', '456 Đường V', 2,
                   'user_2.jpg')
    add_student_db('Nguyệt', 'Phạm Thị', '20080919', 'Nữ', '0900000183', 'thinguyet183@example.com', '456 Đường W', 2,
                   'user_1.jpg')
    add_student_db('Trường', 'Lê Hữu', '20080921', 'Nam', '0900000184', 'huutruong184@example.com', '456 Đường X', 2,
                   'user_2.jpg')
    add_student_db('Bình', 'Hoàng Minh', '20080923', 'Nam', '0900000185', 'minhbinh185@example.com', '456 Đường Y', 2,
                   'user_1.jpg')
    add_student_db('Hằng', 'Vũ Thu', '20080925', 'Nữ', '0900000186', 'thuhang186@example.com', '456 Đường Z', 2,
                   'user_2.jpg')
    add_student_db('Giang', 'Bùi Quốc', '20080927', 'Nữ', '0900000187', 'quocgiang187@example.com', '456 Đường AA', 2,
                   'user_1.jpg')
    add_student_db('Trâm', 'Đặng Ngọc', '20080929', 'Nữ', '0900000188', 'ngoctram188@example.com', '456 Đường BB', 2,
                   'user_2.jpg')
    add_student_db('Quang', 'Đỗ Văn', '20080903', 'Nam', '0900000189', 'vanquang189@example.com', '456 Đường CC', 2,
                   'user_1.jpg')
    add_student_db('Hậu', 'Ngô Huy', '20080905', 'Nam', '0900000190', 'huyhau190@example.com', '456 Đường DD', 2,
                   'user_2.jpg')
    add_student_db('Vy', 'Nguyễn Thu', '20080901', 'Nữ', '0900000191', 'thuvy191@example.com', '456 Đường EE', 2,
                   'user_1.jpg')
    add_student_db('Chí', 'Trần Văn', '20080902', 'Nam', '0900000192', 'vanchi192@example.com', '456 Đường FF', 2,
                   'user_2.jpg')
    add_student_db('Phượng', 'Phạm Ngọc', '20080903', 'Nữ', '0900000193', 'ngocphuong193@example.com', '456 Đường GG',
                   2, 'user_1.jpg')
    add_student_db('Tiến', 'Lê Hữu', '20080904', 'Nam', '0900000194', 'huutien194@example.com', '456 Đường HH', 2,
                   'user_2.jpg')
    add_student_db('Hạnh', 'Hoàng Minh', '20080905', 'Nữ', '0900000195', 'minhhanh195@example.com', '456 Đường II', 2,
                   'user_1.jpg')
    add_student_db('Phú', 'Vũ Bảo', '20080906', 'Nam', '0900000196', 'baophu196@example.com', '456 Đường JJ', 2,
                   'user_2.jpg')
    add_student_db('Khoa', 'Bùi Quốc', '20080907', 'Nam', '0900000197', 'quockhoa197@example.com', '456 Đường KK', 2,
                   'user_1.jpg')
    add_student_db('Oanh', 'Đặng Thị', '20080908', 'Nữ', '0900000198', 'thioanh198@example.com', '456 Đường LL', 2,
                   'user_2.jpg')
    add_student_db('Bích', 'Đỗ Thùy', '20080909', 'Nữ', '0900000199', 'thuybich199@example.com', '456 Đường MM', 2,
                   'user_1.jpg')
    add_student_db('Hoài', 'Ngô Phương', '20080910', 'Nữ', '0900000200', 'phuonghoai200@example.com', '456 Đường NN',
                   2, 'user_2.jpg')
    add_student_db('Cường', 'Nguyễn Đình', '20080911', 'Nam', '0900000201', 'dinhcuong201@example.com', '456 Đường OO',
                   2, 'user_1.jpg')
    add_student_db('Hòa', 'Trần Hữu', '20080912', 'Nam', '0900000202', 'huuhoa202@example.com', '456 Đường PP', 2,
                   'user_2.jpg')
    add_student_db('Tâm', 'Phạm Ngọc', '20080913', 'Nam', '0900000203', 'ngoctam203@example.com', '456 Đường QQ', 2,
                   'user_1.jpg')
    add_student_db('Hưng', 'Lê Minh', '20080914', 'Nam', '0900000204', 'minhhung204@example.com', '456 Đường RR', 2,
                   'user_2.jpg')
    add_student_db('Nguyên', 'Hoàng Văn', '20080915', 'Nam', '0900000205', 'vannguyen205@example.com', '456 Đường SS',
                   2, 'user_1.jpg')
    add_student_db('Thảo', 'Vũ Bích', '20080916', 'Nữ', '0900000206', 'bichthao206@example.com', '456 Đường TT', 2,
                   'user_2.jpg')
    add_student_db('Liên', 'Bùi Hồng', '20080917', 'Nữ', '0900000207', 'honglien207@example.com', '456 Đường UU', 2,
                   'user_1.jpg')
    add_student_db('Lộc', 'Đặng Minh', '20080918', 'Nam', '0900000208', 'minhloc208@example.com', '456 Đường VV', 2,
                   'user_2.jpg')
    add_student_db('Vinh', 'Đỗ Thành', '20080919', 'Nam', '0900000209', 'thanhvinh209@example.com', '456 Đường WW', 2,
                   'user_1.jpg')
    add_student_db('Hải', 'Ngô Thái', '20080920', 'Nam', '0900000210', 'thaihai210@example.com', '456 Đường XX', 2,
                   'user_2.jpg')
    add_student_db('Hương', 'Nguyễn Ánh', '20080921', 'Nữ', '0900000211', 'anhhuong211@example.com', '456 Đường YY', 2,
                   'user_1.jpg')
    add_student_db('Tú', 'Trần Đức', '20080922', 'Nam', '0900000212', 'ductu212@example.com', '456 Đường ZZ', 2,
                   'user_2.jpg')
    add_student_db('Trang', 'Phạm Thùy', '20080923', 'Nữ', '0900000213', 'thuytrang213@example.com', '456 Đường AA', 2,
                   'user_1.jpg')
    add_student_db('Hiếu', 'Lê Hùng', '20080924', 'Nam', '0900000214', 'hunghieu214@example.com', '456 Đường BB', 2,
                   'user_2.jpg')
    add_student_db('Khánh', 'Hoàng Thái', '20080925', 'Nam', '0900000215', 'thaikhanh215@example.com', '456 Đường CC',
                   2, 'user_1.jpg')
    add_student_db('Mai', 'Vũ Ngọc', '20080926', 'Nữ', '0900000216', 'ngocmai216@example.com', '456 Đường DD', 2,
                   'user_2.jpg')
    add_student_db('Trí', 'Bùi Đức', '20080927', 'Nam', '0900000217', 'ductri217@example.com', '456 Đường EE', 2,
                   'user_1.jpg')
    add_student_db('Vy', 'Đặng Linh', '20080928', 'Nữ', '0900000218', 'linhvy218@example.com', '456 Đường FF', 2,
                   'user_2.jpg')
    add_student_db('Đan', 'Đỗ Minh', '20080929', 'Nữ', '0900000219', 'minhdan219@example.com', '456 Đường GG', 2,
                   'user_1.jpg')
    add_student_db('Hoài', 'Ngô Đức', '20080930', 'Nữ', '0900000220', 'duchoai220@example.com', '456 Đường HH', 2,
                   'user_2.jpg')
    # Khối 12
    add_student_db('Tuệ', 'Nguyễn Thanh', '20070101', 'Nữ', '0900000221', 'thanhtuet221@example.com', '789 Đường JJ',
                   3, 'user_1.jpg')
    add_student_db('Quân', 'Trần Thắng', '20070102', 'Nam', '0900000222', 'thangquan222@example.com', '789 Đường KK',
                   3, 'user_2.jpg')
    add_student_db('Kiên', 'Phạm Anh', '20070103', 'Nam', '0900000223', 'anhkien223@example.com', '789 Đường LL', 3,
                   'user_1.jpg')
    add_student_db('Đan', 'Lê Minh', '20070104', 'Nữ', '0900000224', 'minhdan224@example.com', '789 Đường MM', 3,
                   'user_2.jpg')
    add_student_db('Lâm', 'Hoàng Quốc', '20070105', 'Nam', '0900000225', 'quoclam225@example.com', '789 Đường NN', 3,
                   'user_1.jpg')
    add_student_db('Hải', 'Vũ Bình', '20070106', 'Nam', '0900000226', 'binhhai226@example.com', '789 Đường OO', 3,
                   'user_2.jpg')
    add_student_db('Ánh', 'Nguyễn Thị', '20070107', 'Nữ', '0900000227', 'thianh227@example.com', '789 Đường PP', 3,
                   'user_1.jpg')
    add_student_db('Dũng', 'Trần Hoàng', '20070108', 'Nam', '0900000228', 'hoangdung228@example.com', '789 Đường QQ',
                   3, 'user_2.jpg')
    add_student_db('Hương', 'Bùi Hồng', '20070109', 'Nữ', '0900000229', 'honghuong229@example.com', '789 Đường RR', 3,
                   'user_1.jpg')
    add_student_db('Hậu', 'Phạm Thị', '20070110', 'Nam', '0900000230', 'thihau230@example.com', '789 Đường SS', 3,
                   'user_2.jpg')
    add_student_db('Chí', 'Vũ Quốc', '20070111', 'Nam', '0900000231', 'quocchi231@example.com', '789 Đường TT', 3,
                   'user_1.jpg')
    add_student_db('Tú', 'Hoàng Nam', '20070112', 'Nữ', '0900000232', 'namtu232@example.com', '789 Đường UU', 3,
                   'user_2.jpg')
    add_student_db('Bảo', 'Nguyễn Hữu', '20070113', 'Nam', '0900000233', 'huubao233@example.com', '789 Đường VV', 3,
                   'user_1.jpg')
    add_student_db('Lan', 'Trần Thị', '20070114', 'Nữ', '0900000234', 'thilan234@example.com', '789 Đường WW', 3,
                   'user_2.jpg')
    add_student_db('Việt', 'Bùi Đức', '20070115', 'Nam', '0900000235', 'ducviet235@example.com', '789 Đường XX', 3,
                   'user_1.jpg')
    add_student_db('Duy', 'Phạm Thế', '20070116', 'Nam', '0900000236', 'theduy236@example.com', '789 Đường YY', 3,
                   'user_2.jpg')
    add_student_db('Bích', 'Ngô Ánh', '20070117', 'Nữ', '0900000237', 'anhbich237@example.com', '789 Đường ZZ', 3,
                   'user_1.jpg')
    add_student_db('Châu', 'Lê Tấn', '20070118', 'Nữ', '0900000238', 'tantuanchau238@example.com', '789 Đường AA', 3,
                   'user_2.jpg')
    add_student_db('Trí', 'Nguyễn Lệ', '20070119', 'Nam', '0900000239', 'letrit239@example.com', '789 Đường BB', 3,
                   'user_1.jpg')
    add_student_db('Quang', 'Trần Đức', '20070120', 'Nam', '0900000240', 'ductran240@example.com', '789 Đường CC', 3,
                   'user_2.jpg')
    add_student_db('Linh', 'Đặng Mai', '20070121', 'Nữ', '0900000241', 'mailinh241@example.com', '789 Đường DD', 3,
                   'user_1.jpg')
    add_student_db('Mỹ', 'Vũ Minh', '20070122', 'Nữ', '0900000242', 'minhmy242@example.com', '789 Đường EE', 3,
                   'user_2.jpg')
    add_student_db('Nam', 'Lê Ngọc', '20070123', 'Nam', '0900000243', 'ngocnam243@example.com', '789 Đường FF', 3,
                   'user_1.jpg')
    add_student_db('Khánh', 'Phạm Thiện', '20070124', 'Nam', '0900000244', 'thienkhanh244@example.com', '789 Đường GG',
                   3, 'user_2.jpg')
    add_student_db('Duy', 'Nguyễn Thái', '20070125', 'Nam', '0900000245', 'thaiduy245@example.com', '789 Đường HH', 3,
                   'user_1.jpg')
    add_student_db('Thu', 'Hoàng Thanh', '20070126', 'Nữ', '0900000246', 'thanhthu246@example.com', '789 Đường II', 3,
                   'user_2.jpg')
    add_student_db('Tâm', 'Vũ Lê', '20070127', 'Nam', '0900000247', 'lemtam247@example.com', '789 Đường JJ', 3,
                   'user_1.jpg')
    add_student_db('Tuân', 'Trần Anh', '20070128', 'Nam', '0900000248', 'anhxuan248@example.com', '789 Đường KK', 3,
                   'user_2.jpg')
    add_student_db('Hằng', 'Nguyễn Thị', '20070129', 'Nữ', '0900000249', 'thihang249@example.com', '789 Đường LL', 3,
                   'user_1.jpg')
    add_student_db('Quyền', 'Phạm Chí', '20070130', 'Nam', '0900000250', 'chiquyen250@example.com', '789 Đường MM', 3,
                   'user_2.jpg')
    add_student_db('Thảo', 'Đặng Quỳnh', '20070131', 'Nữ', '0900000251', 'quynhthao251@example.com', '789 Đường NN', 3,
                   'user_1.jpg')
    add_student_db('Tình', 'Lê Thanh', '20070131', 'Nữ', '0900000252', 'thanhthinh252@example.com', '789 Đường OO', 3,
                   'user_2.jpg')
    add_student_db('Trường', 'Nguyễn Tâm', '20070123', 'Nam', '0900000253', 'tamttruong253@example.com', '789 Đường PP',
                   3, 'user_1.jpg')
    add_student_db('Sơn', 'Trần Tấn', '20070124', 'Nam', '0900000254', 'tantson254@example.com', '789 Đường QQ', 3,
                   'user_2.jpg')
    add_student_db('Ngọc', 'Phạm Vũ', '20070125', 'Nữ', '0900000255', 'vungoc255@example.com', '789 Đường RR', 3,
                   'user_1.jpg')
    add_student_db('Bình', 'Vũ Khánh', '20070126', 'Nam', '0900000256', 'khanhbinh256@example.com', '789 Đường SS', 3,
                   'user_2.jpg')
    add_student_db('Vi', 'Nguyễn Thiết', '20070127', 'Nữ', '0900000257', 'thietvi257@example.com', '789 Đường TT', 3,
                   'user_1.jpg')
    add_student_db('Khánh', 'Đặng Hồng', '20070128', 'Nam', '0900000258', 'hongkhanh258@example.com', '789 Đường UU',
                   3, 'user_2.jpg')
    add_student_db('An', 'Lê An', '20070129', 'Nữ', '0900000259', 'anle259@example.com', '789 Đường VV', 3,
                   'user_1.jpg')
    add_student_db('Thịnh', 'Hoàng Ngọc', '20070120', 'Nam', '0900000260', 'ngocthinh260@example.com', '789 Đường WW',
                   3, 'user_2.jpg')
    add_student_db('Trâm', 'Phạm Quỳnh', '20070121', 'Nữ', '0900000261', 'quynhtram261@example.com', '789 Đường XX', 3,
                   'user_1.jpg')
    add_student_db('Tuấn', 'Nguyễn Ánh', '20070122', 'Nam', '0900000262', 'anhxuantuan262@example.com', '789 Đường YY',
                   3, 'user_2.jpg')
    add_student_db('Hòa', 'Đặng Hoàng', '20070123', 'Nữ', '0900000263', 'hoanghoa263@example.com', '789 Đường ZZ', 3,
                   'user_1.jpg')
    add_student_db('Mai', 'Trần Thị', '20070124', 'Nữ', '0900000264', 'thimai264@example.com', '789 Đường AA', 3,
                   'user_2.jpg')
    add_student_db('Như', 'Nguyễn Thị', '20070125', 'Nữ', '0900000265', 'thinhunh265@example.com', '789 Đường BB', 3,
                   'user_1.jpg')
    # Lớp
    class_db(1, 1, 2, 1, 30)
    class_db(2, 1, 2, 2, 30)
    class_db(1, 2, 2, 3, 23)
    class_db(2, 2, 2, 4, 22)
    # Học sinh học lớp
    for i in range(91, 121):
        student_class_db(i, 1)
    for i in range(121, 151):
        student_class_db(i, 2)
    for i in range(151, 174):
        student_class_db(i, 3)
    for i in range(174, 196):
        student_class_db(i, 4)
    #     for i in range(91, 121):
    #         student_class_db(i, 14)
