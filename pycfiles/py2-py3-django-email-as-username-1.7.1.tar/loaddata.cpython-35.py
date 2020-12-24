# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/management/commands/loaddata.py
# Compiled at: 2015-10-23 08:44:12
# Size of source mod 2**32: 497 bytes
from django.core.management.commands import loaddata
from emailusernames.models import unmonkeypatch_user, monkeypatch_user

class Command(loaddata.Command):
    __doc__ = '\n    Override the built-in loaddata command to un-monkeypatch the User\n    model before loading, to allow usernames to be loaded correctly\n    '

    def handle(self, *args, **kwargs):
        unmonkeypatch_user()
        ret = super(Command, self).handle(*args, **kwargs)
        monkeypatch_user()
        return ret