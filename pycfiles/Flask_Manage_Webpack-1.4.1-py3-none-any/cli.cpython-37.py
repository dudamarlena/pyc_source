# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/me/PycharmProjects/Flask-Manage-Webpack/flask_manage_webpack/cli.py
# Compiled at: 2019-11-15 03:22:42
# Size of source mod 2**32: 196 bytes
import click
from flask.cli import with_appcontext
from . import utils

@click.command()
@click.option('--app')
@with_appcontext
def init(app='app'):
    utils.init_webpack_config(app_name=app)