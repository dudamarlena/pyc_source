# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/user_groups/signals.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 1036 bytes
from django.db.models.signals import post_delete
import django.utils.translation as _
import tendenci.apps.notifications as notification

def create_notice_types(sender, **kwargs):
    verbosity = kwargs.get('verbosity', 2)
    notification.create_notice_type('group_added', (_('Group Added')),
      (_('A group has been added.')),
      verbosity=verbosity)
    notification.create_notice_type('group_deleted', (_('Group Deleted')),
      (_('A group has been deleted')),
      verbosity=verbosity)


def init_signals():
    from tendenci.apps.user_groups.models import Group

    def delete_auth_group(sender, **kwargs):
        group = kwargs['instance']
        auth_group = group.group
        if auth_group:
            auth_group.delete()

    post_delete.connect(delete_auth_group, sender=Group, weak=False)