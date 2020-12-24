# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/south_migrations/0001_initial.py
# Compiled at: 2020-04-17 10:46:24
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('data_importer_filehistory', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
         (
          'active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
         (
          'content', self.gf('django.db.models.fields.files.FileField')(max_length=100))))
        db.send_create_signal('data_importer', ['FileHistory'])

    def backwards(self, orm):
        db.delete_table('data_importer_filehistory')

    models = {'data_importer.filehistory': {'Meta': {'object_name': 'FileHistory'}, 'active': (
                                              'django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}), 
                                     'content': (
                                               'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                                     'created_at': (
                                                  'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                     'id': (
                                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                     'updated_at': (
                                                  'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'data_importer']