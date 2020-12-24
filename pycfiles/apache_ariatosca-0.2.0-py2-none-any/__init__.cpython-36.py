# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/__init__.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3152 bytes
__doc__ = '\nAuthentication is implemented using flask_login and different environments can\nimplement their own login mechanisms by providing an `airflow_login` module\nin their PYTHONPATH. airflow_login should be based off the\n`airflow.www.login`\n'
from builtins import object
from typing import Any
from airflow import version
from airflow.utils.log.logging_mixin import LoggingMixin
__version__ = version.version
import sys
from airflow import settings, configuration as conf
from airflow.models import DAG
from flask_admin import BaseView
from importlib import import_module
from airflow.exceptions import AirflowException
settings.initialize()
login = None

def load_login():
    global login
    log = LoggingMixin().log
    auth_backend = 'airflow.default_login'
    try:
        if conf.getboolean('webserver', 'AUTHENTICATE'):
            auth_backend = conf.get('webserver', 'auth_backend')
    except conf.AirflowConfigException:
        if conf.getboolean('webserver', 'AUTHENTICATE'):
            log.warning('auth_backend not found in webserver config reverting to *deprecated*  behavior of importing airflow_login')
            auth_backend = 'airflow_login'

    try:
        login = import_module(auth_backend)
        if hasattr(login, 'login_manager'):
            if not hasattr(login, 'LOGIN_MANAGER'):
                login.LOGIN_MANAGER = login.login_manager
    except ImportError as err:
        log.critical('Cannot import authentication module %s. Please correct your authentication backend or disable authentication: %s', auth_backend, err)
        if conf.getboolean('webserver', 'AUTHENTICATE'):
            raise AirflowException('Failed to import authentication backend')


class AirflowViewPlugin(BaseView):
    pass


class AirflowMacroPlugin(object):

    def __init__(self, namespace):
        self.namespace = namespace


from airflow import operators
from airflow import sensors
from airflow import hooks
from airflow import executors
from airflow import macros
operators._integrate_plugins()
sensors._integrate_plugins()
hooks._integrate_plugins()
executors._integrate_plugins()
macros._integrate_plugins()