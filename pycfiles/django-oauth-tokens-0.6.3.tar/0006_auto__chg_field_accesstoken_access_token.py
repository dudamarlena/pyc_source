# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/migrations/0006_auto__chg_field_accesstoken_access_token.py
# Compiled at: 2015-01-25 03:14:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('oauth_tokens_accesstoken', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=500))

    def backwards(self, orm):
        db.alter_column('oauth_tokens_accesstoken', 'access_token', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'oauth_tokens.accesstoken': {'Meta': {'ordering': "('-granted',)", 'object_name': 'AccessToken'}, 'access_token': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                    'expires': (
                                              'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                    'granted': (
                                              'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'provider': (
                                               'django.db.models.fields.CharField', [], {'max_length': '20'}), 
                                    'refresh_token': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'scope': (
                                            'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'token_type': (
                                                 'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'user': (
                                           'django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth_tokens.UserCredentials']", 'null': 'True', 'blank': 'True'})}, 
       'oauth_tokens.usercredentials': {'Meta': {'object_name': 'UserCredentials'}, 'active': (
                                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                        'additional': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                        'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                        'name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'password': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'provider': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '20'}), 
                                        'username': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'taggit.tag': {'Meta': {'object_name': 'Tag'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                      'slug': (
                             'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})}, 
       'taggit.taggeditem': {'Meta': {'object_name': 'TaggedItem'}, 'content_type': (
                                            'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'object_id': (
                                         'django.db.models.fields.IntegerField', [], {'db_index': 'True'}), 
                             'tag': (
                                   'django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})}}
    complete_apps = [
     'oauth_tokens']