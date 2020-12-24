# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/metrics/migrations/0002_auto__add_field_metric_query__add_unique_metric_object_id_name_content.py
# Compiled at: 2015-03-25 12:20:02
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('metrics_metric', 'query', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)
        db.create_unique('metrics_metric', ['object_id', 'name', 'content_type_id', 'tags'])

    def backwards(self, orm):
        db.delete_unique('metrics_metric', ['object_id', 'name', 'content_type_id', 'tags'])
        db.delete_column('metrics_metric', 'query')

    models = {'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'metrics.metric': {'Meta': {'unique_together': "(('name', 'tags', 'content_type', 'object_id'),)", 'object_name': 'Metric'}, 'added': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 23, 0, 0)'}), 
                          'content_type': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}), 
                          'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '75'}), 
                          'object_id': (
                                      'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                          'query': (
                                  'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                          'tags': (
                                 'jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}), 
                          'updated': (
                                    'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 23, 0, 0)'})}}
    complete_apps = [
     'metrics']