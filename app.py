import os.path
from flask import render_template, redirect, request, url_for
from sqlalchemy import create_engine
import hashlib
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import Users, Classes, Students, Enrollment, app, db


db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)

map_files = []
classes= Classes.query.all()

db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep secret'  # placeholder
salt = '$aggrontyranitar$'.encode('utf-8')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


def encrypt_password(password):
    encoded_password = password.encode('utf-8')
    return hashlib.sha256(encoded_password + salt).hexdigest()


def check_password(plain, password):
    encoded_plain = plain.encode('utf-8')
    valid = (hashlib.sha256(encoded_plain + salt).hexdigest() == password)
    return valid


def add_user(username, password):
    new_password = encrypt_password(password)
    user = Users(username=username, password=new_password)
    db.session.add(user)
    db.session.commit()


def add_student(fname, lname, user_id):
    student = Students(first_name=fname, last_name=lname, user_id=user_id)
    db.session.add(student)
    db.session.commit()


def add_class(student_id, class_id):
    class_to_add = Classes.query.filter(Classes.id == class_id).first()
    db.session.add(Enrollment(student_id=student_id, class_id=class_id))
    db.session.commit()


def is_enrolled(class_id, student_id):
    student = Students.query.filter_by(id=student_id).first()
    classes = student.classes
    for entry in classes:
        if entry.id == class_id:
            return True
    return False


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
            if not Users.query.filter_by(username=username).first():
                add_user(username, password)
                user = Users.query.filter_by(username=username).first()
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
        student = Students.query.filter_by(user_id=current_user.id).first()
        return render_template('user_page.html', name=student.first_name)
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['username']).first()
        if user is None or not check_password(request.form['password'], user.password):
            return render_template('login.html', error='Please enter valid Username/Password')
        login_user(user)
        student = Students.query.filter_by(user_id=user.id).first()
        return redirect(url_for('home'))
    return render_template('login.html', error='')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user/<student_id>', methods=['GET', 'POST'])
@login_required
def user_page(student_id):
    name = Students.query.filter_by(id=student_id).first().first_name
    classes = Enrollment.query.filter_by(student_id=student_id).all()
    student_classes = []
    for c in classes:
        enrolled = Classes.query.filter_by(id=c.class_id).first()
        student_classes.append(enrolled.class_name)
    return render_template('user_page.html', name=name, classes=student_classes)


@app.route('/classes/', methods=['GET', 'POST'])
@login_required
def load_class():
    class_name = request.form['class']
    class_to_load = Classes.query.filter_by(class_name=class_name).first()
    return render_template('classes.html', id=class_to_load.id)


@app.route('/class/1/map', methods=['GET', 'POST'])
@login_required
def class_map():
    map_files.clear()
    map_files.append("maps/COB1-1.svg")
    map_files.append("maps/COB1-2.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/class/add_class', methods=['GET', 'POST'])
@login_required
def add_class_to_user():
    user = Users.query.filter_by(id=current_user.id).first()
    student = Students.query.filter(Students.user_id == user.id).first()

    if request.method == 'POST':
        class_id = int(request.form['reg_button'])
        student = Students.query.filter(Students.user_id == current_user.id).first()
        if not is_enrolled(class_id, student.id):
            add_class(student.id, class_id)
            return redirect(url_for('user_page'), student_id=student.id)
        else:
            return render_template('class_registration.html', classes=classes,
                                   error='You are currently enrolled in this class!')
    return render_template('class_registration.html', classes=classes)


@app.route('/building/cob1/map', methods=['GET', 'POST'])
def get_cob_map():
    map_files.clear()
    map_files.append("maps/COB1-1.svg")
    map_files.append("maps/COB1-2.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/cob2/map', methods=['GET', 'POST'])
def get_cob2_map():
    map_files.clear()
    map_files.append("maps/COB2-1.svg")
    map_files.append("maps/COB2-2.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/admin/map', methods=['GET', 'POST'])
def get_admin_map():
    map_files.clear()
    map_files.append("maps/admin-1.svg")
    map_files.append("maps/admin-2.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/acs/map', methods=['GET', 'POST'])
def get_acs_map():
    map_files.clear()
    map_files.append("maps/acs.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/gran/map', methods=['GET', 'POST'])
def get_gran_map():
    map_files.clear()
    map_files.append("maps/gran.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/glcr/map', methods=['GET', 'POST'])
def get_glcr_map():
    map_files.clear()
    map_files.append("maps/glcr.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/se1/map', methods=['GET', 'POST'])
def get_se1_map():
    map_files.clear()
    map_files.append("maps/s_e1.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/se2/map', methods=['GET', 'POST'])
def get_se2_map():
    map_files.clear()
    map_files.append("maps/se2.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/ssm/map', methods=['GET', 'POST'])
def get_ssm_map():
    map_files.clear()
    map_files.append("maps/ssm.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/ssb/map', methods=['GET', 'POST'])
def get_ssb_map():
    map_files.clear()
    map_files.append("maps/ssb.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/sre/map', methods=['GET', 'POST'])
def get_sre_map():
    map_files.clear()
    map_files.append("maps/sre.svg")
    return render_template('class_map.html', src=map_files)


@app.route('/building/kl/map', methods=['GET', 'POST'])
def get_kl_map():
    map_files.clear()
    map_files.append("maps/kl-1.svg")
    map_files.append("maps/kl-2.svg")
    return render_template('class_map.html', src=map_files)


if __name__ == "__main__":
    app.run()
