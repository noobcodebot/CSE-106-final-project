import os.path
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import hashlib
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
import models

app = Flask(__name__)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
db = SQLAlchemy(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)

db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep secret'  # placeholder
salt = '$aggrontyranitar$'.encode('utf-8')

@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(user_id)


def encrypt_password(password):
    encoded_password = password.encode('utf-8')
    return hashlib.sha256(encoded_password + salt).hexdigest()


def check_password(plain, password):
    encoded_plain = plain.encode('utf-8')
    valid = (hashlib.sha256(encoded_plain + salt).hexdigest() == password)
    return valid


def add_user(username, password):
    new_password = encrypt_password(password)
    user = models.Users(username=username, password=new_password)
    db.session.add(user)
    db.session.commit()


def add_student(fname, lname, user_id):
    student = models.Students(first_name=fname, last_name=lname, user_id=user_id)
    db.session.add(student)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        if username != ' ' and password != ' ' and fname != ' ' and lname != ' ':
            if not models.Users.query.filter_by(username=username).first():
                add_user(username, password)
                user = models.Users.query.filter_by(username=username).first()
                add_student(fname, lname, user.id)
                return redirect(url_for('login'))
            else:
                return render_template('register.html',
                                       error='Username already exists. Please try using a different username.')
        else:
            return render_template('register.html', error='Please enter valid credentials!')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        student = models.Students.query.filter_by(user_id=current_user.id).first()
        return render_template('user_page.html', name=student.first_name)
    if request.method == 'POST':
        user = models.Users.query.filter_by(username=request.form['username']).first()
        if user is None or not check_password(request.form['password'], user.password):
            return render_template('login.html', error='Please enter valid Username/Password')
        login_user(user)
        student = models.Students.query.filter_by(user_id=user.id).first()
        return redirect(url_for('user_page', student_id=student.id))
    return render_template('login.html', error='')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<student_id>', methods=['GET', 'POST'])
@login_required
def user_page(student_id):
    name = models.Students.query.filter_by(id=student_id).first().first_name
    classes = models.Enrollment.query.filter_by(student_id=student_id).all()
    student_classes = []
    for c in classes:
        enrolled = models.Classes.query.filter_by(id=c.class_id).first()
        student_classes.append(enrolled.class_name)
    return render_template('user_page.html', name=name, classes=student_classes)



if __name__ == "__main__":
    app.run()