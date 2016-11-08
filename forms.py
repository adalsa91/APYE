#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wtforms import Form, StringField, PasswordField, validators


class SignUpForm(Form):
    username = StringField('Usuario:', [validators.InputRequired(message='El campo Usuario es obligatorio.'), validators.Length(
        min=4, max=20, message='El nombre de usuario debe tener una longitud de entre 4 y 20 caracteres.')])

    name = StringField('Nombre:', [validators.InputRequired(message='El campo Nombre es obligatorio.'), validators.Length(
        min=4, max=25, message='El nombre debe tener entre 4 y 100 caracteres.')])

    email = StringField('Email:', [validators.InputRequired(message='El campo Email es obligatorio'), validators.Regexp(
        r'^[\w]+@([\w]+\.)+[a-z]+$', message='Debe introducir un email válido.'),  validators.Length(min=4, max=25, message='El nombre debe tener entre 4 y 100 caracteres.')])

    password = PasswordField('Contraseña:', [validators.InputRequired(message='El campo Contraseña es obligatorio.'), validators.Length(
        min=7, max=25, message='La contraseña debe de tener una longitud de entre 7 y 25 caracteres.'), validators.EqualTo('repeat_password', message='Las contraseñas no coinciden.')])

    repeat_password = PasswordField('Repetir contraseña:')


class LoginForm(Form):
    username = StringField('Usuario', [validators.InputRequired(
        message='Introduzca un nombre de usuario..'), validators.Length(min=4, max=20)])
    password = PasswordField('Contraseña', [validators.InputRequired(
        message='Introduzca la contraseña.'), validators.Length(min=4, max=25)])
