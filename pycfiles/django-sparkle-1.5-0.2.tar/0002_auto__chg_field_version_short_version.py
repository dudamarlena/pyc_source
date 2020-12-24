# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spielmann/prog/bitchest/server/env/src/django-sparkle/sparkle/migrations/0002_auto__chg_field_version_short_version.py
# Compiled at: 2013-07-22 10:41:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('sparkle_version', 'short_version', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):
        db.alter_column('sparkle_version', 'short_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

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
                                           'django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}), 
                           'title': (
                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'update': (
                                    'django.db.models.fields.files.FileField', [], {'max_length': '100'}), 
                           'version': (
                                     'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'sparkle']