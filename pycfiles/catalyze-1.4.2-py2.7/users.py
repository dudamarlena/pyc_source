# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/users.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import click
from catalyze import cli, client, project, output
from catalyze.helpers import environments

@cli.command(short_help='Retrieve your user ID')
def whoami():
    """Prompts for login, and prints out your ID so that you can be added to an environment by someone else."""
    session = client.acquire_session()
    output.write('user ID = ' + session.user_id)


@cli.command(short_help='Add a user to the environment')
@click.argument('user_id')
def adduser(user_id):
    """Adds another user to the associated environment. The ID required is found via 'catalyze whoami'."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    environments.add_user(session, settings['environmentId'], user_id)
    output.write('Added.')


@cli.command(short_help='Remove a user from the environment')
@click.argument('user_id')
def rmuser(user_id):
    """Removes another user from the associated environment. The ID required is found via 'catalyze whoami'."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    environments.remove_user(session, settings['environmentId'], user_id)
    output.write('Removed.')


@cli.command(short_help='List users for the environment')
def users():
    """Lists users in the associated environment."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    for user in environments.list_users(session, settings['environmentId'])['users']:
        if user == settings['user_id']:
            output.write('%s (you)' % (user,))
        else:
            output.write(user)