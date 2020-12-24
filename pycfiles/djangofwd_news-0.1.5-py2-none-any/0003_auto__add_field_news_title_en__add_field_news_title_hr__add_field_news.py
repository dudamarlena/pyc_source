# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\workspace\apps\testin\testnews-env\lib\site-packages\news\migrations\0003_auto__add_field_news_title_en__add_field_news_title_hr__add_field_news.py
# Compiled at: 2015-04-21 10:56:23
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('news_news', 'title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'title_hr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'slug_hr', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'summary_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'summary_hr', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'content_en', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True), keep_default=False)
        db.add_column('news_news', 'content_hr', self.gf('djangocms_text_ckeditor.fields.HTMLField')(null=True, blank=True), keep_default=False)
        db.add_column('news_category', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_category', 'name_hr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_category', 'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_category', 'slug_hr', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_attachment', 'name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_attachment', 'name_hr', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_attachment', 'slug_en', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_attachment', 'slug_hr', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_gallery', 'title_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_gallery', 'title_hr', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_gallery', 'slug_en', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_gallery', 'slug_hr', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_tag', 'name_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_tag', 'name_hr', self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_tag', 'slug_en', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('news_tag', 'slug_hr', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True), keep_default=False)
        return

    def backwards(self, orm):
        db.delete_column('news_news', 'title_en')
        db.delete_column('news_news', 'title_hr')
        db.delete_column('news_news', 'slug_en')
        db.delete_column('news_news', 'slug_hr')
        db.delete_column('news_news', 'summary_en')
        db.delete_column('news_news', 'summary_hr')
        db.delete_column('news_news', 'content_en')
        db.delete_column('news_news', 'content_hr')
        db.delete_column('news_category', 'name_en')
        db.delete_column('news_category', 'name_hr')
        db.delete_column('news_category', 'slug_en')
        db.delete_column('news_category', 'slug_hr')
        db.delete_column('news_attachment', 'name_en')
        db.delete_column('news_attachment', 'name_hr')
        db.delete_column('news_attachment', 'slug_en')
        db.delete_column('news_attachment', 'slug_hr')
        db.delete_column('news_gallery', 'title_en')
        db.delete_column('news_gallery', 'title_hr')
        db.delete_column('news_gallery', 'slug_en')
        db.delete_column('news_gallery', 'slug_hr')
        db.delete_column('news_tag', 'name_en')
        db.delete_column('news_tag', 'name_hr')
        db.delete_column('news_tag', 'slug_en')
        db.delete_column('news_tag', 'slug_hr')

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
                           'name_hr': (
                                     'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'news': (
                                  'django.db.models.fields.related.ForeignKey', [], {'default': "''", 'related_name': "'news_attachments'", 'null': 'True', 'blank': 'True', 'to': "orm['news.News']"}), 
                           'slug': (
                                  'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255'}), 
                           'slug_en': (
                                     'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                           'slug_hr': (
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
                         'name_hr': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                         'published': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'slug': (
                                'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                         'slug_en': (
                                   'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                         'slug_hr': (
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
                        'slug_hr': (
                                  'django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'title': (
                                'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}), 
                        'title_en': (
                                   'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                        'title_hr': (
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
                     'content_hr': (
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
                     'slug_hr': (
                               'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                     'source_url': (
                                  'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                     'summary': (
                               'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'summary_en': (
                                  'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'summary_hr': (
                                  'djangocms_text_ckeditor.fields.HTMLField', [], {'null': 'True', 'blank': 'True'}), 
                     'tag': (
                           'django.db.models.fields.related.ManyToManyField', [], {'related_name': "'news_tags'", 'default': 'None', 'to': "orm['news.Tag']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}), 
                     'title': (
                             'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                     'title_en': (
                                'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                     'title_hr': (
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
                    'name_hr': (
                              'django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                    'slug': (
                           'django.db.models.fields.SlugField', [], {'max_length': '255'}), 
                    'slug_en': (
                              'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                    'slug_hr': (
                              'django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                    'updated_at': (
                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'news']