# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/plugins/feeds/migrations/0002_auto__add_field_feed_title__add_field_feed_page_size__add_field_feed_s.py
# Compiled at: 2013-01-04 01:48:06
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('cmsplugin_feed', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('cmsplugin_feed', 'page_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10), keep_default=False)
        db.add_column('cmsplugin_feed', 'show_date', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

    def backwards(self, orm):
        db.delete_column('cmsplugin_feed', 'title')
        db.delete_column('cmsplugin_feed', 'page_size')
        db.delete_column('cmsplugin_feed', 'show_date')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'changed_date': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'creation_date': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 4, 0, 0)'}), 
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
       'feeds.feed': {'Meta': {'object_name': 'Feed', 'db_table': "'cmsplugin_feed'"}, 'cmsplugin_ptr': (
                                      'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                      'page_size': (
                                  'django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}), 
                      'posts': (
                              'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['goscale.Post']", 'symmetrical': 'False'}), 
                      'show_date': (
                                  'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                      'template': (
                                 'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                      'title': (
                              'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                      'url': (
                            'django.db.models.fields.URLField', [], {'max_length': '250'})}, 
       'goscale.post': {'Meta': {'object_name': 'Post'}, 'attributes': (
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
     'feeds']