# flask_testing/test_base.py
import unittest
from app import app, db
from models import User


class BaseTestCase(unittest.TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        usuario = User('adalsa', 'adalsa@correo.ugr.es', 'Adrian')
        db.session.add(usuario)
        db.session.commit()
        usuarios = User.query.all()
        assert usuario in usuarios

if __name__ == '__main__':
    unittest.main()
