from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import login_manager, LoginManager

app = Flask(__name__)
app.secret_key = '@#$%styifhd*^f&*($%^s&*32R'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abc123@localhost/student_management?charset=utf8mb4'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Think!7688@localhost/student_management?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)
#
# cloudinary.config(
#     cloud_name = 'dxedz1icn',
#     api_key = '652251899769451',
#     api_secret = 'tJpmpfsHYxmjehBFFObwHPHGkP8'
# )
#
# login = LoginManager(app=app)
