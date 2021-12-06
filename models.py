from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Classes(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(100), nullable=False)
    timeslot = db.Column(db.String(100), nullable=False)
    students = db.relationship('Students', secondary='enrollment')
    building = db.Column(db.String(10), nullable=False)
    room_no = db.Column(db.String(5), nullable=False)


class Students(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    classes = db.relationship('Classes', secondary='enrollment')


# joint table for M:M relationships
class Enrollment(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
    student_id = db.Column('student_id', db.Integer, db.ForeignKey('students.id'))
