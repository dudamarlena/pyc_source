# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/tests/fakeapp/migrations/0002_eggs.py
# Compiled at: 2018-07-11 18:15:31
from south.db import db
from django.db import models

class Migration:

    def forwards(self):
        Spam = db.mock_model(model_name='Spam', db_table='southtest_spam', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField)
        db.create_table('southtest_eggs', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'size', models.FloatField()),
         (
          'quantity', models.IntegerField()),
         (
          'spam', models.ForeignKey(Spam))))

    def backwards(self):
        db.delete_table('southtest_eggs')