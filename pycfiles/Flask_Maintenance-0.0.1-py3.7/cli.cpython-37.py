# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flask_maintenance\cli.py
# Compiled at: 2019-07-07 21:46:48
# Size of source mod 2**32: 1265 bytes
import os, click
from flask import current_app
from flask.cli import with_appcontext

@click.group()
def maintenance():
    """Enable or disable Maintenance mode."""
    pass


@maintenance.command()
@with_appcontext
def enable():
    """
    Enable Maintenance mode.
    """
    result = False
    ins_path = current_app.instance_path
    if not os.path.exists(ins_path):
        try:
            os.makedirs(ins_path)
        except Exception as e:
            try:
                click.echo(e)
                return False
            finally:
                e = None
                del e

    try:
        open(os.path.join(ins_path, 'under_maintenance'), 'w').close()
        result = True
    except Exception as e:
        try:
            click.echo(e)
        finally:
            e = None
            del e

    if result:
        click.echo('maintenance mode enabled.')
        return True
    return False


@maintenance.command()
@with_appcontext
def disable():
    """
    Disable Maintenance mode.
    """
    ins_path = current_app.instance_path
    main_file = os.path.join(ins_path, 'under_maintenance')
    if os.path.exists(main_file):
        if os.path.isfile(main_file):
            try:
                os.remove(main_file)
            except Exception as e:
                try:
                    click.echo(e)
                    return False
                finally:
                    e = None
                    del e

    click.echo('maintenance mode disabled.')