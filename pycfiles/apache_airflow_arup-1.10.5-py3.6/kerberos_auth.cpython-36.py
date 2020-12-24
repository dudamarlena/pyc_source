# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/auth/backends/kerberos_auth.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5312 bytes
"""Kerberos authentication module"""
import logging, flask_login
from airflow.exceptions import AirflowConfigException
from flask_login import current_user
from flask import flash
from wtforms import Form, PasswordField, StringField
from wtforms.validators import InputRequired
import kerberos, airflow.security.utils as utils
from flask import url_for, redirect
from airflow import models
from airflow import configuration
from airflow.utils.db import provide_session
from airflow.utils.log.logging_mixin import LoggingMixin
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.login_view = 'airflow.login'
LOGIN_MANAGER.login_message = None

class AuthenticationError(Exception):
    __doc__ = 'Error raised when authentication error occurs'


class KerberosUser(models.User, LoggingMixin):
    __doc__ = 'User authenticated with Kerberos'

    def __init__(self, user):
        self.user = user

    @staticmethod
    def authenticate(username, password):
        service_principal = '%s/%s' % (
         configuration.conf.get('kerberos', 'principal'),
         utils.get_fqdn())
        realm = configuration.conf.get('kerberos', 'default_realm')
        try:
            user_realm = configuration.conf.get('security', 'default_realm')
        except AirflowConfigException:
            user_realm = realm

        user_principal = utils.principal_from_username(username, user_realm)
        try:
            if not kerberos.checkPassword(user_principal, password, service_principal, realm, True):
                raise AuthenticationError()
        except kerberos.KrbError as e:
            logging.error('Password validation for user %s in realm %s failed %s', user_principal, realm, e)
            raise AuthenticationError(e)

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
        return self.user.get_id()

    def data_profiling(self):
        """Provides access to data profiling tools"""
        return True

    def is_superuser(self):
        """Access all the things"""
        return True


@LOGIN_MANAGER.user_loader
@provide_session
def load_user(userid, session=None):
    if not userid or userid == 'None':
        return
    else:
        user = session.query(models.User).filter(models.User.id == int(userid)).first()
        return KerberosUser(user)


@provide_session
def login(self, request, session=None):
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(url_for('index'))
    else:
        username = None
        password = None
        form = LoginForm(request.form)
        if request.method == 'POST':
            if form.validate():
                username = request.form.get('username')
                password = request.form.get('password')
        if not username or not password:
            return self.render('airflow/login.html', title='Airflow - Login',
              form=form)
    try:
        KerberosUser.authenticate(username, password)
        user = session.query(models.User).filter(models.User.username == username).first()
        if not user:
            user = models.User(username=username,
              is_superuser=False)
        session.merge(user)
        session.commit()
        flask_login.login_user(KerberosUser(user))
        session.commit()
        return redirect(request.args.get('next') or url_for('admin.index'))
    except AuthenticationError:
        flash('Incorrect login details')
        return self.render('airflow/login.html', title='Airflow - Login',
          form=form)


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])