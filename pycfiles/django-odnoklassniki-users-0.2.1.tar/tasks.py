# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-users/odnoklassniki_users/tasks.py
# Compiled at: 2015-03-21 09:06:49
from celery.task import Task
from odnoklassniki_users.models import User

class OdnoklassnikiUsersFetchUsers(Task):

    def run(self, ids, only_expired, *args, **kwargs):
        return User.remote.fetch(ids=ids)