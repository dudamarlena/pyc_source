# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/fakeapp/migrations/0001_spam.py
# Compiled at: 2018-07-11 18:15:31
from south.db import db
from django.db import models

class Migration:

    def forwards(self):
        db.create_table('southtest_spam', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'weight', models.FloatField()),
         (
          'expires', models.DateTimeField()),
         (
          'name', models.CharField(max_length=255))))

    def backwards(self):
        db.delete_table('southtest_spam')