# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/news/migrations/0001_initial.py
# Compiled at: 2014-03-27 09:47:06
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('news_category', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
         (
          'order', self.gf('django.db.models.fields.IntegerField')(default=0))))
        db.send_create_signal('news', ['Category'])
        db.create_table('news_article', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
         (
          'category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['news.Category'])),
         (
          'content', self.gf('django.db.models.fields.TextField')()),
         (
          'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
         (
          'publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'publish_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
         (
          'created_on', self.gf('django.db.models.fields.DateTimeField')()),
         (
          'updated_on', self.gf('django.db.models.fields.DateTimeField')())))
        db.send_create_signal('news', ['Article'])

    def backwards(self, orm):
        db.delete_table('news_category')
        db.delete_table('news_article')

    models = {'news.article': {'Meta': {'ordering': "['-publish_on']", 'object_name': 'Article'}, 'category': (
                                   'django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['news.Category']"}), 
                        'content': (
                                  'django.db.models.fields.TextField', [], {}), 
                        'created_on': (
                                     'django.db.models.fields.DateTimeField', [], {}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'image': (
                                'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                        'publish': (
                                  'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'publish_on': (
                                     'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                        'slug': (
                               'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                        'updated_on': (
                                     'django.db.models.fields.DateTimeField', [], {})}, 
       'news.category': {'Meta': {'ordering': "['order', 'title']", 'object_name': 'Category'}, 'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'order': (
                                 'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                         'slug': (
                                'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}), 
                         'title': (
                                 'django.db.models.fields.CharField', [], {'max_length': '255'})}}
    complete_apps = [
     'news']