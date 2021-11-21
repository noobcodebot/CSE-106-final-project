from app import db
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def check_password(self, password):
        return self.password == password


class Classes(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(100), nullable=False)
    timeslot = db.Column(db.String(100), nullable=False)
    students = db.relationship('Students', secondary='enrollment')


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
    building = db.Column(db.String(10), nullable=False)
    room_no = db.Column(db.String(5), nullable=False)