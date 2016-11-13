import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User


login_manager = LoginManager()
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
                if login_form.password.data == usuario.password:
                    login_user(usuario)
                    usuario.authenticated = True
                    db.session.commit()

                    # 'next = flask.request.args.get('next')
                    # next_is_valid should check if the user has valid
                    # permission to access the `next` url
                    # if not next_is_valid(next):
                    #    return flask.abort(400)

                    # return flask.redirect(next or flask.url_for('index'))
                    return "Success"
                else:
                    return "Contraseña incorrecta"
            else:
                return "Usuario no existe"
        elif signup_form.validate():
            db.session.add(
                User(signup_form.username.data, signup_form.email.data,
                     signup_form.password.data, signup_form.name.data, True)
            )
            db.session.commit()

    return render_template('login.html', login_form=login_form,
                           signup_form=signup_form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    user.authenticated = False
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return current_user.username


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
