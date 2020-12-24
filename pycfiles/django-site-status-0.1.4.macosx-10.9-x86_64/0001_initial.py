# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mvid/Development/changetip/site_status/migrations/0001_initial.py
# Compiled at: 2014-02-18 14:37:17
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('site_status_status', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
         (
          'start_time', self.gf('django.db.models.fields.DateTimeField')()),
         (
          'end_time', self.gf('django.db.models.fields.DateTimeField')()),
         (
          'body', self.gf('django.db.models.fields.TextField')())))
        db.send_create_signal('site_status', ['Status'])

    def backwards(self, orm):
        db.delete_table('site_status_status')

    models = {'site_status.status': {'Meta': {'object_name': 'Status'}, 'body': (
                                     'django.db.models.fields.TextField', [], {}), 
                              'end_time': (
                                         'django.db.models.fields.DateTimeField', [], {}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'level': (
                                      'django.db.models.fields.PositiveSmallIntegerField', [], {}), 
                              'start_time': (
                                           'django.db.models.fields.DateTimeField', [], {})}}
    complete_apps = [
     'site_status']