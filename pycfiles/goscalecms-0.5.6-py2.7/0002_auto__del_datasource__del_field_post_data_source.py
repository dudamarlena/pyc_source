# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/migrations/0002_auto__del_datasource__del_field_post_data_source.py
# Compiled at: 2013-01-03 03:12:19
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table('goscale_datasource')
        db.delete_column('goscale_post', 'data_source_id')

    def backwards(self, orm):
        db.create_table('goscale_datasource', (
         (
          'url', self.gf('django.db.models.fields.URLField')(max_length=200)),
         (
          'source_id', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
         (
          'attributes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
         (
          'type', self.gf('django.db.models.fields.CharField')(max_length=250)),
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))))
        db.send_create_signal('goscale', ['DataSource'])
        db.add_column('goscale_post', 'data_source', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['goscale.DataSource']), keep_default=False)
        return

    models = {'goscale.post': {'Meta': {'object_name': 'Post'}, 'attributes': (
                                     'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                        'author': (
                                 'django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'categories': (
                                     'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'content_type': (
                                       'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'description': (
                                      'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'link': (
                               'django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                        'permalink': (
                                    'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'published': (
                                    'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                        'slug': (
                               'django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'summary': (
                                  'django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}), 
                        'updated': (
                                  'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'goscale']