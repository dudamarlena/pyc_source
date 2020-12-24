# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyutrack/cli/update.py
# Compiled at: 2017-10-28 23:27:23
# Size of source mod 2**32: 2853 bytes
import click
from click import get_current_context
from pyutrack import Issue, User, Group, Role
from pyutrack.cli.util import admin_command
from pyutrack.errors import InputError, CliError
from . import cli

@cli.group()
@click.pass_context
def update(_):
    """
    update existing youtrack resources
    """
    pass


@update.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@update.command()
@click.pass_context
@click.argument('id')
@click.option('--summary')
@click.option('--description')
@click.option('--command', help='command to apply to issue.')
@click.option('--comment', help='comment to add to issue')
def issue(ctx, id, summary, description, command, comment):
    """update an issue"""
    issue = Issue(ctx.obj.connection, hydrate=False, id=id)
    if command or comment:
        issue.command(command, comment)
    else:
        issue.update(summary=summary, description=description)
    return issue


@update.command()
@click.pass_context
@click.argument('login')
@click.option('--name', default=None)
@click.option('--email', default=None)
@click.option('--password', default=None)
@click.option('add_groups', '+group', multiple=True, help='add user to group')
@click.option('remove_groups', '-group', multiple=True, help='remove user from group')
@admin_command
def user(ctx, login, name, email, password, add_groups, remove_groups):
    """update a user"""
    user = User(ctx.obj.connection, hydrate=True, login=login)
    if name or email or password:
        user.update(full_name=name, email=email, password=password)
    user.groups += add_groups
    user.groups -= remove_groups
    return user


@update.command()
@click.pass_context
@click.argument('name')
@admin_command
def group(ctx, name):
    """update a group"""
    group = Group(ctx.obj.connection, hydrate=True, name=name)
    return group


@update.command()
@click.pass_context
@click.argument('name')
@click.option('add_permissions', '+permission', multiple=True, help='add permission')
@click.option('remove_permissions', '-permission', multiple=True, help='remove permission')
@admin_command
def role(ctx, name, add_permissions, remove_permissions):
    """update a role"""
    role = Role(ctx.obj.connection, hydrate=False, name=name)
    role.permissions += add_permissions
    role.permissions -= remove_permissions