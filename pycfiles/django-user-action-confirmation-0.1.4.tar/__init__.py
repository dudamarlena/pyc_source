# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alekam/Documents/Workspace/elitsy/env/src/django-user-action-confirmation/user_action_confirmation/__init__.py
# Compiled at: 2014-04-27 15:42:56
VERSION = (0, 1, 4)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    return version


def create_ticket(action, user=None):
    from user_action_confirmation.models import Confirmation
    return Confirmation.objects.create(user=user, action=action).token