# flask_testing/test_base.py
import unittest
import os
import shutil
from app import app, db
from models import User
from flask_login import current_user


class ApyeTestCase(unittest.TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        self.app = app.test_client()
        if not os.path.exists('users/'):
            os.makedirs('users/')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        shutil.rmtree('users')

    def test_adduser(self):
        usuario = User('adrian', 'adalsa@correo.ugr.es',
                       'password', 'Adrian', True)
        db.session.add(usuario)
        db.session.commit()
        usuarios = User.query.all()
        assert usuario in usuarios
        print("[OK] Usuario creado satisfactoriamente\n")

    def test_home_user(self):
        if not os.path.exists('users/' + 'adrian'):
            os.makedirs('users/' + 'adrian')
        f = open('users/adrian/Welcome', 'w+')
        f.write('Welcome!')
        f.seek(0)
        assert f.read() == 'Welcome!'
        f.close()
        print("[OK] Entorno de usuario creado correctamente\n")

    def test_login_logout(self):
        usuario = User('jorge', 'jorge@correo.ugr.es',
                       'password', 'Jorge Nitales', True)
        db.session.add(usuario)
        db.session.commit()

        with self.app:
            # Login
            response = self.app.post(
                '/login', data={'username': 'jorge', 'password': 'password'},
                follow_redirects=True)
            assert current_user.username == 'jorge'
            assert b'Success' in response.data

            # Logout
            response = self.app.post(
                '/logout', follow_redirects=True)
            assert current_user.is_anonymous

        print("[OK] Usuarios registrados pueden identificarse correctamente")

if __name__ == '__main__':
    unittest.main()
