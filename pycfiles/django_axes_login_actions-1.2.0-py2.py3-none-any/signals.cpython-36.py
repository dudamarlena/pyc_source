# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/titschendorf.de/axes_login_actions/signals.py
# Compiled at: 2017-04-17 12:53:17
# Size of source mod 2**32: 1265 bytes
from axes.models import AccessAttempt
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from importlib import import_module
DEFAULT_ACTION = 'axes_login_actions.actions.email.notify'
ACTIONS = getattr(settings, 'AXES_LOGIN_ACTIONS', [DEFAULT_ACTION])

def import_dotted_path(path):
    """
    Takes a dotted path to a member name in a module, and returns
    the member after importing it.
    """
    try:
        module_path, member_name = path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, member_name)
    except (ValueError, ImportError, AttributeError) as e:
        raise ImportError('Could not import the name: {}: {}'.format(path, e))


@receiver(post_save, sender=AccessAttempt, dispatch_uid='axes_login_actions_post_save')
def access_attempt_handler(sender, instance, **kwargs):
    for action_path in ACTIONS:
        action = import_dotted_path(action_path)
        action(instance, **kwargs)