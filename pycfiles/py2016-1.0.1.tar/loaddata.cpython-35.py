# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/1T/home/Projects/django-email-as-username/emailusernames/management/commands/loaddata.py
# Compiled at: 2015-10-23 08:44:12
# Size of source mod 2**32: 497 bytes
from django.core.management.commands import loaddata
from emailusernames.models import unmonkeypatch_user, monkeypatch_user

class Command(loaddata.Command):
    """Command"""

    def handle(self, *args, **kwargs):
        unmonkeypatch_user()
        ret = super(Command, self).handle(*args, **kwargs)
        monkeypatch_user()
        return ret