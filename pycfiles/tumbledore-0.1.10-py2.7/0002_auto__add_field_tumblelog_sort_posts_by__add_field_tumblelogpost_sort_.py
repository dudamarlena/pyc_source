# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-intel/egg/tumbledore/migrations/0002_auto__add_field_tumblelog_sort_posts_by__add_field_tumblelogpost_sort_.py
# Compiled at: 2012-09-18 18:32:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('tumbledore_tumblelog', 'sort_posts_by', self.gf('django.db.models.fields.CharField')(default='D', max_length=1), keep_default=False)
        db.add_column('tumbledore_tumblelogpost', 'sort_order', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)
        db.add_column('tumbledore_tumblelogpost', 'custom_data', self.gf('jsonfield.fields.JSONField')(default='{}'), keep_default=False)

    def backwards(self, orm):
        db.delete_column('tumbledore_tumblelog', 'sort_posts_by')
        db.delete_column('tumbledore_tumblelogpost', 'sort_order')
        db.delete_column('tumbledore_tumblelogpost', 'custom_data')

    models = {'tumbledore.tumblelog': {'Meta': {'object_name': 'Tumblelog'}, 'created_at': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                'description': (
                                              'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                'extra_scripts': (
                                                'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                'extra_styles': (
                                               'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'is_active': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                'mount_on': (
                                           'django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '200', 'db_index': 'True', 'blank': 'True'}), 
                                'name': (
                                       'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                'posts_per_page': (
                                                 'django.db.models.fields.IntegerField', [], {'default': '10'}), 
                                'sort_posts_by': (
                                                'django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}), 
                                'theme': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                'updated_at': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                'widgets': (
                                          'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tumbledore.TumblelogWidget']", 'through': "orm['tumbledore.TumblelogWidgetPlacement']", 'symmetrical': 'False'})}, 
       'tumbledore.tumblelogpost': {'Meta': {'ordering': "('-is_sticky', '-published_at')", 'unique_together': "(('slug', 'tumblelog'),)", 'object_name': 'TumblelogPost'}, 'author': (
                                             'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}), 
                                    'content': (
                                              'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                    'created_at': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}), 
                                    'custom_data': (
                                                  'jsonfield.fields.JSONField', [], {'default': "'{}'"}), 
                                    'excerpt': (
                                              'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                    'has_permalink': (
                                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'is_published': (
                                                   'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                    'is_sticky': (
                                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                    'published_at': (
                                                   'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                    'slug': (
                                           'django.db.models.fields.SlugField', [], {'max_length': '200'}), 
                                    'sort_order': (
                                                 'django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}), 
                                    'title': (
                                            'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                    'tumblelog': (
                                                'django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['tumbledore.Tumblelog']"}), 
                                    'updated_at': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'tumbledore.tumblelogwidget': {'Meta': {'object_name': 'TumblelogWidget'}, 'content': (
                                                'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                      'created_at': (
                                                   'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                      'description': (
                                                    'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                      'name': (
                                             'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                                      'slug': (
                                             'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}), 
                                      'updated_at': (
                                                   'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'tumbledore.tumblelogwidgetplacement': {'Meta': {'ordering': "('order',)", 'object_name': 'TumblelogWidgetPlacement'}, 'id': (
                                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                               'order': (
                                                       'django.db.models.fields.IntegerField', [], {'default': '1'}), 
                                               'tumblelog': (
                                                           'django.db.models.fields.related.ForeignKey', [], {'related_name': "'placement_set'", 'to': "orm['tumbledore.Tumblelog']"}), 
                                               'widget': (
                                                        'django.db.models.fields.related.ForeignKey', [], {'related_name': "'placement_set'", 'to': "orm['tumbledore.TumblelogWidget']"})}}
    complete_apps = [
     'tumbledore']