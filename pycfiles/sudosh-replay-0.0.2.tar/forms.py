# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/log/bin/release/sudosh/app/forms.py
# Compiled at: 2014-06-03 11:14:08
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('UserName: ', validators=[Required()])
    password = TextField('Password: ', validators=[Required()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login')


class SearchForm(Form):
    username = TextField('UserName: ', validators=[Required()])
    password = TextField('Password: ', validators=[Required()])
    submit = SubmitField('Login')