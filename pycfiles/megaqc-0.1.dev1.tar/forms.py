# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewels/GitHub/MegaQC/megaqc/user/forms.py
# Compiled at: 2018-07-06 11:43:42
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import User
import sqlalchemy as sa

class AdminForm(Form):
    user_id = HiddenField('id')
    username = StringField('Username', validators=[
     DataRequired(), Length(min=3, max=25)])
    first_name = StringField('First Name', validators=[
     Length(min=1, max=80)])
    last_name = StringField('Last Name', validators=[
     Length(min=1, max=80)])
    email = StringField('Email', validators=[
     DataRequired(), Email(), Length(min=6, max=40)])
    active = BooleanField('Active')
    is_admin = BooleanField('Admin')

    def validate(self):
        """Validate the form."""
        initial_validation = super(AdminForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user and user.user_id != self.user_id.data:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user and user.user_id != self.user_id.data:
            self.email.errors.append('Email already registered')
            return False
        return True

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AdminForm, self).__init__(*args, **kwargs)
        self.user = None
        return


class PasswordChangeForm(Form):
    password = PasswordField('Password', validators=[
     DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [
     DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = None
        return

    def validate(self):
        """Validate the form."""
        return super(PasswordChangeForm, self).validate()


class RegisterForm(Form):
    """Register form."""

    class Meta:
        csrf = False

    username = StringField('Username', validators=[
     DataRequired(), Length(min=3, max=25)])
    first_name = StringField('First Name', validators=[
     Length(min=1, max=80)])
    last_name = StringField('Last Name', validators=[
     Length(min=1, max=80)])
    email = StringField('Email', validators=[
     DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[
     DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password', [
     DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None
        return

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True