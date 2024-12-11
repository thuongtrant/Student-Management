import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(receive_email, last_name, first_name):
    sender_email = 'studentmanagementOU@gmail.com'
    sender_password = 'npke bvgb dyvi lmrv'

    # Tạo đối tượng MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receive_email
    msg['Subject'] = 'Thông báo kết quả tiếp nhận hồ sơ nhập học'

    # Nội dung email
    body = f"""
Hồ sơ nhập học của học sinh {last_name} {first_name} đã được tiếp nhận thành công!

- Phụ huynh và học sinh vui lòng liên hệ trực tiếp Trung tâm Quản lý Hệ thống thông tin khi có nhu cầu chỉnh sửa thông tin.
- Thông tin danh sách lớp và tài khoản vietschool sẽ được gửi đến email này từ ngày 20/08, xin để ý mail.

Đây là email tự động, vui lòng không reply!
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receive_email, msg.as_string())
        print(f'Email đã gửi thành công tới {receive_email}')
    except Exception as e:
        print(f'Lỗi khi gửi email: {e}')
    finally:
        server.quit()
