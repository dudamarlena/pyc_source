# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/migrations/0002_auto__add_unique_pageauthgroup_page_group.py
# Compiled at: 2013-11-30 05:18:24
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_unique('mezzanine_page_auth_pageauthgroup', ['page_id', 'group_id'])

    def backwards(self, orm):
        db.delete_unique('mezzanine_page_auth_pageauthgroup', ['page_id', 'group_id'])

    models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'generic.assignedkeyword': {'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'}, '_order': (
                                            'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                                   'content_type': (
                                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                                   'id': (
                                        'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                   'keyword': (
                                             'django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': "orm['generic.Keyword']"}), 
                                   'object_pk': (
                                               'django.db.models.fields.IntegerField', [], {})}, 
       'generic.keyword': {'Meta': {'object_name': 'Keyword'}, 'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'site': (
                                  'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                           'slug': (
                                  'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                           'title': (
                                   'django.db.models.fields.CharField', [], {'max_length': '500'})}, 
       'mezzanine_page_auth.pageauthgroup': {'Meta': {'ordering': "('group',)", 'unique_together': "(('page', 'group'),)", 'object_name': 'PageAuthGroup'}, 'group': (
                                                     'django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': "orm['auth.Group']"}), 
                                             'id': (
                                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                             'page': (
                                                    'django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"})}, 
       'pages.page': {'Meta': {'ordering': "('titles',)", 'object_name': 'Page'}, '_meta_title': (
                                    'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}), 
                      '_order': (
                               'django.db.models.fields.IntegerField', [], {'null': 'True'}), 
                      'content_model': (
                                      'django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}), 
                      'created': (
                                'django.db.models.fields.DateTimeField', [], {'null': 'True'}), 
                      'description': (
                                    'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                      'expiry_date': (
                                    'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                      'gen_description': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                      'groups': (
                               'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'through': "orm['mezzanine_page_auth.PageAuthGroup']", 'blank': 'True'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'in_menus': (
                                 'mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3)', 'max_length': '100', 'null': 'True', 'blank': 'True'}), 
                      'in_sitemap': (
                                   'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                      'keywords': (
                                 'mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': "orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}), 
                      'keywords_string': (
                                        'django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}), 
                      'login_required': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                      'parent': (
                               'django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['pages.Page']"}), 
                      'publish_date': (
                                     'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                      'short_url': (
                                  'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                      'site': (
                             'django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}), 
                      'slug': (
                             'django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}), 
                      'status': (
                               'django.db.models.fields.IntegerField', [], {'default': '2'}), 
                      'title': (
                              'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                      'titles': (
                               'django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}), 
                      'updated': (
                                'django.db.models.fields.DateTimeField', [], {'null': 'True'})}, 
       'sites.site': {'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"}, 'domain': (
                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '50'})}}
    complete_apps = [
     'mezzanine_page_auth']