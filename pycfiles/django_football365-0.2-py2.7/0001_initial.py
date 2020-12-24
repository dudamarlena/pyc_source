# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football365/migrations/0001_initial.py
# Compiled at: 2013-05-21 11:00:49
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('football365_call', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=256)),
         (
          'call_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
         (
          'football365_service_id', self.gf('django.db.models.fields.PositiveIntegerField')())))
        db.send_create_signal('football365', ['Call'])

    def backwards(self, orm):
        db.delete_table('football365_call')

    models = {'football365.call': {'Meta': {'ordering': "('title',)", 'object_name': 'Call'}, 'call_type': (
                                        'django.db.models.fields.CharField', [], {'max_length': '32'}), 
                            'football365_service_id': (
                                                     'django.db.models.fields.PositiveIntegerField', [], {}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'title': (
                                    'django.db.models.fields.CharField', [], {'max_length': '256'})}}
    complete_apps = [
     'football365']