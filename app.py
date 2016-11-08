import os
import flask_login
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# This will redirect users to the login view whenever they are required to
# be logged in.
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object,
    return None if does not exist

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(int(user_id))


@app.route('/signup/<username>', methods=['GET', 'POST'])
def signup(username):
    if not os.path.exists('users/' + username):
        os.makedirs('users/' + username)
    return 'Created'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form. For POSTS,
    login the current user by processing the form."""
    login_form = LoginForm(request.form)
    signup_form = SignUpForm(request.form)
    if request.method == 'POST':
        if 'email' not in request.form and login_form.validate():
            usuario = db.session.query(User).filter_by(
                username=str(login_form.username.data)).first()
            if usuario:
                print('Usuario existe')
                if login_form.password.data == usuario.password:
                    print("Success")
            else:
                print('Usuario no existe')
        elif signup_form.validate():
            db.session.add(
                User(signup_form.username.data, signup_form.email.data,
                     signup_form.password.data, signup_form.name.data, True)
            )
            db.session.commit()

    return render_template('login.html', login_form=login_form,
                           signup_form=signup_form)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
