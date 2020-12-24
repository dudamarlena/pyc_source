# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-users/facebook_users/migrations/0002_auto__chg_field_user_name.py
# Compiled at: 2015-03-06 07:15:54
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('facebook_users_user', 'name', self.gf('django.db.models.fields.CharField')(max_length=300))

    def backwards(self, orm):
        db.alter_column('facebook_users_user', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {'facebook_users.user': {'Meta': {'ordering': "['name']", 'object_name': 'User'}, 'graph_id': (
                                          'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '300'})}}
    complete_apps = [
     'facebook_users']