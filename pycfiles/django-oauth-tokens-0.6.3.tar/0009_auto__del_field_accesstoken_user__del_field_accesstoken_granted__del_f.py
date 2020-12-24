# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/migrations/0009_auto__del_field_accesstoken_user__del_field_accesstoken_granted__del_f.py
# Compiled at: 2015-01-25 03:14:29
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('oauth_tokens_accesstoken', 'user_id')
        db.delete_column('oauth_tokens_accesstoken', 'granted')
        db.delete_column('oauth_tokens_accesstoken', 'expires')
        db.add_column('oauth_tokens_accesstoken', 'granted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 12, 22, 0, 0), blank=True), keep_default=False)
        db.add_column('oauth_tokens_accesstoken', 'expires_in', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True), keep_default=False)
        db.add_column('oauth_tokens_accesstoken', 'expires_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True), keep_default=False)
        db.add_column('oauth_tokens_accesstoken', 'user_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True), keep_default=False)
        db.add_column('oauth_tokens_accesstoken', 'user_credentials', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth_tokens.UserCredentials'], null=True, blank=True), keep_default=False)
        db.alter_column('oauth_tokens_accesstoken', 'scope', self.gf('annoying.fields.JSONField')(max_length=200, null=True))
        db.add_column('oauth_tokens_usercredentials', 'exception', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

    def backwards(self, orm):
        db.add_column('oauth_tokens_accesstoken', 'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth_tokens.UserCredentials'], null=True, blank=True), keep_default=False)
        raise RuntimeError("Cannot reverse this migration. 'AccessToken.granted' and its values cannot be restored.")
        db.add_column('oauth_tokens_accesstoken', 'granted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True), keep_default=False)
        db.add_column('oauth_tokens_accesstoken', 'expires', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True), keep_default=False)
        db.delete_column('oauth_tokens_accesstoken', 'granted_at')
        db.delete_column('oauth_tokens_accesstoken', 'expires_in')
        db.delete_column('oauth_tokens_accesstoken', 'expires_at')
        db.delete_column('oauth_tokens_accesstoken', 'user_id')
        db.delete_column('oauth_tokens_accesstoken', 'user_credentials_id')
        db.alter_column('oauth_tokens_accesstoken', 'scope', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))
        db.delete_column('oauth_tokens_usercredentials', 'exception')

    models = {'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'oauth_tokens.accesstoken': {'Meta': {'ordering': "('-granted_at',)", 'object_name': 'AccessToken'}, 'access_token': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '500'}), 
                                    'expires_at': (
                                                 'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                    'expires_in': (
                                                 'django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}), 
                                    'granted_at': (
                                                 'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'provider': (
                                               'django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}), 
                                    'refresh_token': (
                                                    'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'scope': (
                                            'annoying.fields.JSONField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'token_type': (
                                                 'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}), 
                                    'user_credentials': (
                                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth_tokens.UserCredentials']", 'null': 'True', 'blank': 'True'}), 
                                    'user_id': (
                                              'django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})}, 
       'oauth_tokens.usercredentials': {'Meta': {'object_name': 'UserCredentials'}, 'active': (
                                                 'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                        'additional': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}), 
                                        'exception': (
                                                    'django.db.models.fields.TextField', [], {}), 
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
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}), 
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