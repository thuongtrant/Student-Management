from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DATETIME, ForeignKey, Enum, DateTime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum, UNIQUE
from StudentManagement import db, app

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
class UserRole(UserEnum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    EMPLOYEE = "EMPLOYEE"
# Ví dụ model cho bảng User
class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.TEACHER)

    def __repr__(self):
        return f'<User {self.username}>'


if __name__ == '__main__':
    with app.app_context():
        pass
        # db.create_all()