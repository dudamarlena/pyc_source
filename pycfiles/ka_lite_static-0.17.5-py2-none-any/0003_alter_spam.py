# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/fakeapp/migrations/0003_alter_spam.py
# Compiled at: 2018-07-11 18:15:31
from south.db import db
from django.db import models

class Migration:

    def forwards(self):
        db.alter_column('southtest_spam', 'weight', models.FloatField(null=True))

    def backwards(self):
        db.alter_column('southtest_spam', 'weight', models.FloatField())

    models = {'fakeapp.bug135': {'date': (
                                 'models.DateTimeField', [], {'default': 'datetime.datetime(2009, 5, 6, 15, 33, 15, 780013)'})}}