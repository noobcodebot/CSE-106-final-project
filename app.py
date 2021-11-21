import os.path
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# app.secret_key = 'keep secret'  # placeholder


db.create_all()
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
