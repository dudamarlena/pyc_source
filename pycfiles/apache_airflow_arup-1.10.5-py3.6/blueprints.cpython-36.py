# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/blueprints.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 980 bytes
from flask import Blueprint, redirect, url_for
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return redirect(url_for('Airflow.index'))