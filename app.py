import os.path
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import bcrypt
from bcrypt import gensalt

import models

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# app.secret_key = 'keep secret'  # placeholder
salt = '$aggronblaziken$'


db.create_all()
db.session.commit()


def encrypt_password(password):
    return bcrypt.hashpw(password, gensalt(12))


def check_password(plaintext, hashed):
    return bcrypt.checkpw(plaintext, hashed)


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
            add_user(username, password)
            user = models.Users.query.filter_by(username=username).first()
            add_student(fname, lname, user.id)
        else:
            return render_template('register.html', error='Please enter valid credentials!')
    return render_template('register.html')


if __name__ == "__main__":
    app.run()
