# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/plugins/feeds/migrations/0005_auto__add_tumblr__add_blogger.py
# Compiled at: 2013-01-15 02:41:16
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('cmsplugin_tumblr', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
         (
          'url', self.gf('django.db.models.fields.URLField')(max_length=250)),
         (
          'page_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
         (
          'show_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'external_links', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'label', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True))))
        db.send_create_signal('feeds', ['Tumblr'])
        db.create_table('feeds_tumblr_posts', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'tumblr', models.ForeignKey(orm['feeds.tumblr'], null=False)),
         (
          'post', models.ForeignKey(orm['goscale.post'], null=False))))
        db.create_unique('feeds_tumblr_posts', ['tumblr_id', 'post_id'])
        db.create_table('cmsplugin_blogger', (
         (
          'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
         (
          'template', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'updated', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
         (
          'url', self.gf('django.db.models.fields.URLField')(max_length=250)),
         (
          'page_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
         (
          'show_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'external_links', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'label', self.gf('django.db.models.fields.URLField')(max_length=250, null=True, blank=True))))
        db.send_create_signal('feeds', ['Blogger'])
        db.create_table('feeds_blogger_posts', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'blogger', models.ForeignKey(orm['feeds.blogger'], null=False)),
         (
          'post', models.ForeignKey(orm['goscale.post'], null=False))))
        db.create_unique('feeds_blogger_posts', ['blogger_id', 'post_id'])

    def backwards(self, orm):
        db.delete_table('cmsplugin_tumblr')
        db.delete_table('feeds_tumblr_posts')
        db.delete_table('cmsplugin_blogger')
        db.delete_table('feeds_blogger_posts')

    models = {'cms.cmsplugin': {'Meta': {'object_name': 'CMSPlugin'}, 'changed_date': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                         'creation_date': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 15, 0, 0)'}), 
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
       'feeds.blogger': {'Meta': {'object_name': 'Blogger', 'db_table': "'cmsplugin_blogger'"}, 'cmsplugin_ptr': (
                                         'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                         'external_links': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'label': (
                                 'django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}), 
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
                         'updated': (
                                   'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                         'url': (
                               'django.db.models.fields.URLField', [], {'max_length': '250'})}, 
       'feeds.feed': {'Meta': {'object_name': 'Feed', 'db_table': "'cmsplugin_feed'"}, 'cmsplugin_ptr': (
                                      'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                      'external_links': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
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
                      'updated': (
                                'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                      'url': (
                            'django.db.models.fields.URLField', [], {'max_length': '250'})}, 
       'feeds.tumblr': {'Meta': {'object_name': 'Tumblr', 'db_table': "'cmsplugin_tumblr'"}, 'cmsplugin_ptr': (
                                        'django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}), 
                        'external_links': (
                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                        'label': (
                                'django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}), 
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
                        'updated': (
                                  'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
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