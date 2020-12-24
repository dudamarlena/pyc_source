# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/simple/proj/cli/shell_ipython.py
# Compiled at: 2020-03-11 03:42:34
# Size of source mod 2**32: 430 bytes
import click
from flask import current_app
from flask.cli import with_appcontext

@click.command('shell', short_help='Starts an interactive shell in an app context.')
@with_appcontext
def shell_command():
    ctx = current_app.make_shell_context()
    try:
        from IPython import start_ipython
        start_ipython(argv=(), user_ns=ctx)
    except ImportError:
        from code import interact
        interact(local=ctx)