# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spielmann/prog/bitchest/server/env/src/django-sparkle/sparkle/migrations/0001_initial.py
# Compiled at: 2013-07-22 10:41:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('sparkle_application', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=50))))
        db.send_create_signal('sparkle', ['Application'])
        db.create_table('sparkle_version', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sparkle.Application'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
         (
          'short_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
         (
          'dsa_signature', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
         (
          'length', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
         (
          'release_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
         (
          'minimum_system_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
         (
          'published', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'update', self.gf('django.db.models.fields.files.FileField')(max_length=100))))
        db.send_create_signal('sparkle', ['Version'])
        db.create_table('sparkle_systemprofilereport', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
         (
          'added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('sparkle', ['SystemProfileReport'])
        db.create_table('sparkle_systemprofilereportrecord', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sparkle.SystemProfileReport'])),
         (
          'key', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'value', self.gf('django.db.models.fields.CharField')(max_length=80))))
        db.send_create_signal('sparkle', ['SystemProfileReportRecord'])

    def backwards(self, orm):
        db.delete_table('sparkle_application')
        db.delete_table('sparkle_version')
        db.delete_table('sparkle_systemprofilereport')
        db.delete_table('sparkle_systemprofilereportrecord')

    models = {'sparkle.application': {'Meta': {'object_name': 'Application'}, 'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'sparkle.systemprofilereport': {'Meta': {'object_name': 'SystemProfileReport'}, 'added': (
                                               'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                       'id': (
                                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                       'ip_address': (
                                                    'django.db.models.fields.IPAddressField', [], {'max_length': '15'})}, 
       'sparkle.systemprofilereportrecord': {'Meta': {'object_name': 'SystemProfileReportRecord'}, 'id': (
                                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                             'key': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                             'report': (
                                                      'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sparkle.SystemProfileReport']"}), 
                                             'value': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '80'})}, 
       'sparkle.version': {'Meta': {'object_name': 'Version'}, 'application': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sparkle.Application']"}), 
                           'dsa_signature': (
                                           'django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'length': (
                                    'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}), 
                           'minimum_system_version': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}), 
                           'published': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                           'release_notes': (
                                           'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                           'short_version': (
                                           'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}), 
                           'title': (
                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'update': (
                                    'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                           'version': (
                                     'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'sparkle']