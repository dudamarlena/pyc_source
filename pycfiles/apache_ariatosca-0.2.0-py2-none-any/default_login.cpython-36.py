# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/default_login.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2646 bytes
__doc__ = '\nOverride this file to handle your authenticating / login.\n\nCopy and alter this file and put in your PYTHONPATH as airflow_login.py,\nthe new module will override this one.\n'
import flask_login
from flask_login import login_required, current_user, logout_user
from flask import url_for, redirect
from airflow import settings
from airflow import models
from airflow.utils.db import provide_session
DEFAULT_USERNAME = 'airflow'
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.login_view = 'airflow.login'
LOGIN_MANAGER.login_message = None

class DefaultUser(object):

    def __init__(self, user):
        self.user = user

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

    def data_profiling(self):
        """Provides access to data profiling tools"""
        return True

    def is_superuser(self):
        """Access all the things"""
        return True


@LOGIN_MANAGER.user_loader
@provide_session
def load_user(userid, session=None):
    user = session.query(models.User).filter(models.User.id == userid).first()
    return DefaultUser(user)


@provide_session
def login(self, request, session=None):
    user = session.query(models.User).filter(models.User.username == DEFAULT_USERNAME).first()
    if not user:
        user = models.User(username=DEFAULT_USERNAME,
          is_superuser=True)
    session.merge(user)
    session.commit()
    flask_login.login_user(DefaultUser(user))
    session.commit()
    return redirect(request.args.get('next') or url_for('index'))