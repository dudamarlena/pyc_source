# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/config_templates/default_webserver_config.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 4498 bytes
"""Default configuration for the Airflow webserver"""
import os
from flask_appbuilder.security.manager import AUTH_DB
from airflow import configuration as conf
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')
CSRF_ENABLED = True
AUTH_TYPE = AUTH_DB