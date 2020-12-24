# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/otherfakeapp/migrations/0001_first.py
# Compiled at: 2018-07-11 18:15:31
from south.db import db
from django.db import models

class Migration:
    depends_on = (('fakeapp', '0001_spam'), )

    def forwards(self):
        pass

    def backwards(self):
        pass