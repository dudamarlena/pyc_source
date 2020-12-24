# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\temp\sandbox\app\commands.py
# Compiled at: 2020-02-04 02:27:42
# Size of source mod 2**32: 432 bytes
"""
Created on 2020-02-04 15:27:42.

@app: fabadmin
"""
import click, logging
from . import appbuilder
from fab_admin.console import cli_app
log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])

@cli_app.command('hello')
def say_hi():
    """Sample customization app command."""
    click.echo('Sample command')
    with appbuilder.get_app.app_context():
        click.echo('Hi, have fun!')