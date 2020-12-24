# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/users.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import router
from django.db.models.signals import post_syncdb
from sentry.models import User

def create_first_user(created_models, verbosity, db, app=None, **kwargs):
    if app and app.__name__ != 'sentry.models':
        return
    if User not in created_models:
        return
    if hasattr(router, 'allow_migrate'):
        if not router.allow_migrate(db, User):
            return
    elif not router.allow_syncdb(db, User):
        return
    if not kwargs.get('interactive', True):
        return
    import click
    if not click.confirm('\nWould you like to create a user account now?', default=True):
        click.echo('\nRun `sentry createuser` to do this later.\n')
        return
    from sentry.runner import call_command
    call_command('sentry.runner.commands.createuser.createuser', superuser=True)


post_syncdb.connect(create_first_user, dispatch_uid='create_first_user', weak=False)