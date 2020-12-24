# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/josvanvelzen/django/cmsplugin-fbgallery/cmsplugin_fbgallery/migrations/0002_rename_table.py
# Compiled at: 2016-10-05 14:54:08
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, connection

class Migration(SchemaMigration):

    def forwards(self, orm):
        table_names = connection.introspection.table_names()
        if 'cmsplugin_facebookgallery' in table_names:
            db.rename_table('cmsplugin_facebookgallery', 'cmsplugin_fbgallery_facebookgallery')

    def backwards(self, orm):
        db.rename_table('cmsplugin_fbgallery_facebookgallery', 'cmsplugin_facebookgallery')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'changed_date': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'creation_date': (
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
       'cmsplugin_fbgallery.facebookgallery': {'Meta': {'object_name': 'FacebookGallery', '_ormbases': ['cms.CMSPlugin']}, 'album_id': (
                                                          'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                               'album_name': (
                                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                               'cmsplugin_ptr': (
                                                               'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})}}
    complete_apps = [
     'cmsplugin_fbgallery']