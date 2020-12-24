# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\workspace\apps\news\news\app\news\migrations\0001_initial.py
# Compiled at: 2015-04-16 09:44:23
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
          'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
         (
          'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
         (
          'published', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['Category'])
        db.create_table('news_tag', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255)),
         (
          'name_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
         (
          'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['Tag'])
        db.create_table('news_author', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(default=None, max_length=255)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['Author'])
        db.create_table('news_news', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
         (
          'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
         (
          'author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='authors', null=True, to=orm['news.Author'])),
         (
          'summary', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
         (
          'summary_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
         (
          'content', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
         (
          'content_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True)),
         (
          'category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='news_category', to=orm['news.Category'])),
         (
          'source_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
         (
          'highlight', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'published', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['News'])
        m2m_table_name = db.shorten_name('news_news_tag')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'news', models.ForeignKey(orm['news.news'], null=False)),
         (
          'tag', models.ForeignKey(orm['news.tag'], null=False))))
        db.create_unique(m2m_table_name, ['news_id', 'tag_id'])
        db.create_table('news_gallery', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'news', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='news_gallery', null=True, blank=True, to=orm['news.News'])),
         (
          'title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
         (
          'title_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255)),
         (
          'slug_en', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True)),
         (
          'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['Gallery'])
        db.create_table('news_attachment', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'news', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='news_attachments', null=True, blank=True, to=orm['news.News'])),
         (
          'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
         (
          'name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
         (
          'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255)),
         (
          'slug_en', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True)),
         (
          'attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('news', ['Attachment'])
        return

    def backwards(self, orm):
        db.delete_table('news_category')
        db.delete_table('news_tag')
        db.delete_table('news_author')
        db.delete_table('news_news')
        db.delete_table(db.shorten_name('news_news_tag'))
        db.delete_table('news_gallery')
        db.delete_table('news_attachment')

    models = {'news.attachment': {'Meta': {'object_name': 'Attachment'}, 'attachment': (
                                        'django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                           'created_at': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}), 
                           'name_en': (
                                     'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'news': (
                                  'django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'news_attachments'", 'null': 'True', 'blank': 'True', 'to': "orm['news.News']"}), 
                           'slug': (
                                  'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255'}), 
                           'slug_en': (
                                     'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'updated_at': (
                                        'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'news.author': {'Meta': {'object_name': 'Author'}, 'created_at': (
                                    'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                       'id': (
                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                       'name': (
                              'django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}), 
                       'slug': (
                              'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                       'updated_at': (
                                    'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'news.category': {'Meta': {'object_name': 'Category'}, 'created_at': (
                                      'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'name': (
                                'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                         'name_en': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                         'published': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'slug': (
                                'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                         'slug_en': (
                                   'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                         'updated_at': (
                                      'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'news.gallery': {'Meta': {'object_name': 'Gallery'}, 'created_at': (
                                     'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                        'id': (
                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                        'image': (
                                'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                        'news': (
                               'django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'news_gallery'", 'null': 'True', 'blank': 'True', 'to': "orm['news.News']"}), 
                        'slug': (
                               'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255'}), 
                        'slug_en': (
                                  'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}), 
                        'title_en': (
                                   'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'updated_at': (
                                     'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'news.news': {'Meta': {'object_name': 'News'}, 'author': (
                              'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authors'", 'null': 'True', 'to': "orm['news.Author']"}), 
                     'category': (
                                'django.db.models.fields.related.ForeignKey', [], {'related_name': "'news_category'", 'to': "orm['news.Category']"}), 
                     'content': (
                               'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'content_en': (
                                  'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'created_at': (
                                  'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                     'highlight': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'id': (
                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                     'published': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'slug': (
                            'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                     'slug_en': (
                               'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                     'source_url': (
                                  'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                     'summary': (
                               'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'summary_en': (
                                  'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'tag': (
                           'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'news_tags'", 'default': 'None', 'to': "orm['news.Tag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}), 
                     'title': (
                             'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                     'title_en': (
                                'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                     'updated_at': (
                                  'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'news.tag': {'Meta': {'object_name': 'Tag'}, 'created_at': (
                                 'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                    'id': (
                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                    'name': (
                           'django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255'}), 
                    'name_en': (
                              'django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                    'slug': (
                           'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                    'slug_en': (
                              'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                    'updated_at': (
                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'news']