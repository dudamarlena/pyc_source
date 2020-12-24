# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/cli/admin/user.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 3119 bytes
from __future__ import print_function
import click
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL
from chisubmit.client.exceptions import UnknownObjectException
from chisubmit.cli.common import catch_chisubmit_exceptions, require_config

@click.group(name='user')
@click.pass_context
def admin_user(ctx):
    pass


@click.command(name='add')
@click.argument('username', type=str)
@click.argument('first_name', type=str)
@click.argument('last_name', type=str)
@click.argument('email', type=str)
@catch_chisubmit_exceptions
@require_config
@click.pass_context
def admin_user_add(ctx, username, first_name, last_name, email):
    try:
        user = ctx.obj['client'].get_user(username=username)
        print('ERROR: Cannot create user.')
        print('       Username with user_id = %s already exists.' % username)
        ctx.exit(CHISUBMIT_FAIL)
    except UnknownObjectException as uoe:
        user = ctx.obj['client'].create_user(username=username, first_name=first_name, last_name=last_name, email=email)

    return CHISUBMIT_SUCCESS


@click.command(name='remove')
@click.argument('user_id', type=str)
@catch_chisubmit_exceptions
@require_config
@click.pass_context
def admin_user_remove(ctx, user_id):
    print('NOT IMPLEMENTED')
    return CHISUBMIT_SUCCESS


admin_user.add_command(admin_user_add)
admin_user.add_command(admin_user_remove)