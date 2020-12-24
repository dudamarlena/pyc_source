# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/user_groups/apps.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 435 bytes
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UserGroupsConfig(AppConfig):
    name = 'tendenci.apps.user_groups'
    verbose_name = 'User Groups'

    def ready(self):
        super(UserGroupsConfig, self).ready()
        from tendenci.apps.user_groups.signals import init_signals, create_notice_types
        init_signals()
        post_migrate.connect(create_notice_types, sender=self)