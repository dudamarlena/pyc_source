# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-applications/facebook_applications/migrations/0001_initial.py
# Compiled at: 2015-03-06 07:16:36
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('facebook_applications_application', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'graph_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=200)),
         (
          'namespace', self.gf('django.db.models.fields.CharField')(max_length=100))))
        db.send_create_signal('facebook_applications', ['Application'])

    def backwards(self, orm):
        db.delete_table('facebook_applications_application')

    models = {'facebook_applications.application': {'Meta': {'ordering': "['name']", 'object_name': 'Application'}, 'graph_id': (
                                                        'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
                                             'id': (
                                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                             'name': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                             'namespace': (
                                                         'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'facebook_applications']