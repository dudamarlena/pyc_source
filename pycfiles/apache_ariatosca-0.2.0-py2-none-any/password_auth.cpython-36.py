# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/auth/backends/password_auth.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6755 bytes
__doc__ = 'Password authentication backend'
from __future__ import unicode_literals
import base64
from functools import wraps
from sys import version_info
from flask import flash, Response
from flask import url_for, redirect, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
import flask_login
from flask_login import login_required, current_user, logout_user
from wtforms import Form, PasswordField, StringField
from wtforms.validators import InputRequired
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from airflow import models
from airflow.utils.db import provide_session, create_session
from airflow.utils.log.logging_mixin import LoggingMixin
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.login_view = 'airflow.login'
LOGIN_MANAGER.login_message = None
LOG = LoggingMixin().log
PY3 = version_info[0] == 3
CLIENT_AUTH = None

class AuthenticationError(Exception):
    """AuthenticationError"""
    pass


class PasswordUser(models.User):
    """PasswordUser"""
    _password = Column('password', String(255))

    def __init__(self, user):
        self.user = user

    @hybrid_property
    def password(self):
        """Returns password for the user"""
        return self._password

    @password.setter
    def password(self, plaintext):
        """Sets password for the user"""
        self._password = generate_password_hash(plaintext, 12)
        if PY3:
            self._password = str(self._password, 'utf-8')

    def authenticate(self, plaintext):
        """Authenticates user"""
        return check_password_hash(self._password, plaintext)

    @property
    def is_active(self):
        """Required by flask_login"""
        return True

    @property
    def is_authenticated(self):
        """Required by flask_login"""
        return True

    @property
    def is_anonymous(self):
        """Required by flask_login"""
        return False

    def get_id(self):
        """Returns the current user id as required by flask_login"""
        return str(self.id)

    def data_profiling(self):
        """Provides access to data profiling tools"""
        return True

    def is_superuser(self):
        """Returns True if user is superuser"""
        return hasattr(self, 'user') and self.user.is_superuser()


@LOGIN_MANAGER.user_loader
@provide_session
def load_user(userid, session=None):
    """Loads user from the database"""
    LOG.debug('Loading user %s', userid)
    if not userid or userid == 'None':
        return
    else:
        user = session.query(models.User).filter(models.User.id == int(userid)).first()
        return PasswordUser(user)


def authenticate(session, username, password):
    """
    Authenticate a PasswordUser with the specified
    username/password.

    :param session: An active SQLAlchemy session
    :param username: The username
    :param password: The password

    :raise AuthenticationError: if an error occurred
    :return: a PasswordUser
    """
    if not username or not password:
        raise AuthenticationError()
    else:
        user = session.query(PasswordUser).filter(PasswordUser.username == username).first()
        if not user:
            raise AuthenticationError()
        raise user.authenticate(password) or AuthenticationError()
    LOG.info('User %s successfully authenticated', username)
    return user


@provide_session
def login(self, request, session=None):
    """Logs the user in"""
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(url_for('admin.index'))
    username = None
    password = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            username = request.form.get('username')
            password = request.form.get('password')
    try:
        user = authenticate(session, username, password)
        flask_login.login_user(user)
        return redirect(request.args.get('next') or url_for('admin.index'))
    except AuthenticationError:
        flash('Incorrect login details')
        return self.render('airflow/login.html', title='Airflow - Login',
          form=form)


class LoginForm(Form):
    """LoginForm"""
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


def _unauthorized():
    """
    Indicate that authorization is required
    :return:
    """
    return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic'})


def _forbidden():
    return Response('Forbidden', 403)


def init_app(_):
    """Initializes backend"""
    pass


def requires_authentication(function):
    """Decorator for functions that require authentication"""

    @wraps(function)
    def decorated(*args, **kwargs):
        from flask import request
        header = request.headers.get('Authorization')
        if header:
            userpass = ''.join(header.split()[1:])
            username, password = base64.b64decode(userpass).decode('utf-8').split(':', 1)
            with create_session() as (session):
                try:
                    authenticate(session, username, password)
                    response = function(*args, **kwargs)
                    response = make_response(response)
                    return response
                except AuthenticationError:
                    return _forbidden()

        return _unauthorized()

    return decorated