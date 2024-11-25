from StudentManagement.models import User
import hashlib
def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter_by(username=username.strip(), password=password).first()
def get_user_by_id(user_id):
    return User.query.get(user_id)