# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-pages-statistic/facebook_pages_statistic/migrations/0001_initial.py
# Compiled at: 2015-03-06 07:16:08
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('facebook_pages_statistic_pagestatistic', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statistics', to=orm['facebook_pages.Page'])),
         (
          'likes_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
         (
          'talking_about_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('facebook_pages_statistic', ['PageStatistic'])

    def backwards(self, orm):
        db.delete_table('facebook_pages_statistic_pagestatistic')

    models = {'facebook_pages.page': {'Meta': {'object_name': 'Page'}, 'about': (
                                       'django.db.models.fields.TextField', [], {}), 
                               'can_post': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                               'category': (
                                          'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'checkins_count': (
                                                'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                               'company_overview': (
                                                  'django.db.models.fields.TextField', [], {}), 
                               'cover': (
                                       'annoying.fields.JSONField', [], {'null': 'True'}), 
                               'description': (
                                             'django.db.models.fields.TextField', [], {}), 
                               'graph_id': (
                                          'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'is_published': (
                                              'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                               'likes_count': (
                                             'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                               'link': (
                                      'django.db.models.fields.URLField', [], {'max_length': '1000'}), 
                               'location': (
                                          'annoying.fields.JSONField', [], {'null': 'True'}), 
                               'name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                               'phone': (
                                       'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'picture': (
                                         'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                               'posts_count': (
                                             'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                               'products': (
                                          'django.db.models.fields.TextField', [], {}), 
                               'talking_about_count': (
                                                     'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                               'username': (
                                          'django.db.models.fields.CharField', [], {'max_length': '200'}), 
                               'website': (
                                         'django.db.models.fields.CharField', [], {'max_length': '1000'})}, 
       'facebook_pages_statistic.pagestatistic': {'Meta': {'object_name': 'PageStatistic'}, 'id': (
                                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                  'likes_count': (
                                                                'django.db.models.fields.PositiveIntegerField', [], {}), 
                                                  'page': (
                                                         'django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'to': "orm['facebook_pages.Page']"}), 
                                                  'talking_about_count': (
                                                                        'django.db.models.fields.PositiveIntegerField', [], {}), 
                                                  'updated_at': (
                                                               'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})}}
    complete_apps = [
     'facebook_pages_statistic']