# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/migrations/0001_initial.py
# Compiled at: 2014-04-02 11:18:41
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('whatsnew_whatsnew', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'version', self.gf('django.db.models.fields.CharField')(max_length=30)),
         (
          'content', self.gf('django.db.models.fields.TextField')())))
        db.send_create_signal('whatsnew', ['WhatsNew'])

    def backwards(self, orm):
        db.delete_table('whatsnew_whatsnew')

    models = {'whatsnew.whatsnew': {'Meta': {'object_name': 'WhatsNew'}, 'content': (
                                       'django.db.models.fields.TextField', [], {}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'version': (
                                       'django.db.models.fields.CharField', [], {'max_length': '30'})}}
    complete_apps = [
     'whatsnew']