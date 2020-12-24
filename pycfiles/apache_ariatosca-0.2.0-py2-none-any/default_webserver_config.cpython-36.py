# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/config_templates/default_webserver_config.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 4498 bytes
__doc__ = 'Default configuration for the Airflow webserver'
import os
from flask_appbuilder.security.manager import AUTH_DB
from airflow import configuration as conf
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')
CSRF_ENABLED = True
AUTH_TYPE = AUTH_DB