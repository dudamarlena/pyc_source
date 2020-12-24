# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scottblevins/git/old impression/impression/forms.py
# Compiled at: 2016-07-20 22:28:21
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators

class LoginForm(Form):
    username = StringField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.optional()])

    def validate(self):
        from impression.models import User
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True