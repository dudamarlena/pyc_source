# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cmsplugin_googleform/migrations/0002_add_dimensions.py
# Compiled at: 2012-06-05 11:09:10
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('cmsplugin_googleformsplugin', 'template')
        db.add_column('cmsplugin_googleformsplugin', 'height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True), keep_default=False)
        db.add_column('cmsplugin_googleformsplugin', 'width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.add_column('cmsplugin_googleformsplugin', 'template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.delete_column('cmsplugin_googleformsplugin', 'height')
        db.delete_column('cmsplugin_googleformsplugin', 'width')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'creation_date': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'language': (
                                    'django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}), 
                         'level': (
                                 'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'lft': (
                               'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'parent': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}), 
                         'placeholder': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}), 
                         'plugin_type': (
                                       'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}), 
                         'position': (
                                    'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                         'rght': (
                                'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}), 
                         'tree_id': (
                                   'django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})}, 
       'cms.placeholder': {'Meta': {'object_name': 'Placeholder'}, 'default_width': (
                                           'django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'slot': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})}, 
       'cmsplugin_googleform.googleformsplugin': {'Meta': {'object_name': 'GoogleFormsPlugin', 'db_table': "'cmsplugin_googleformsplugin'", '_ormbases': ['cms.CMSPlugin']}, 'cmsplugin_ptr': (
                                                                  'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                                                  'form_id': (
                                                            'django.db.models.fields.CharField', [], {'max_length': '64'}), 
                                                  'height': (
                                                           'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                                                  'width': (
                                                          'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'cmsplugin_googleform']