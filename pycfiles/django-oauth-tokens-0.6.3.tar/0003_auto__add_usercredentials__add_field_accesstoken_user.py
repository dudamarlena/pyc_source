# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/migrations/0003_auto__add_usercredentials__add_field_accesstoken_user.py
# Compiled at: 2015-01-25 03:14:29
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('oauth_tokens_usercredentials', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'username', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'password', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'additional', self.gf('django.db.models.fields.CharField')(max_length=100)),
         (
          'provider', self.gf('django.db.models.fields.CharField')(max_length=100))))
        db.send_create_signal('oauth_tokens', ['UserCredentials'])
        db.add_column('oauth_tokens_accesstoken', 'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth_tokens.UserCredentials'], null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.delete_table('oauth_tokens_usercredentials')
        db.delete_column('oauth_tokens_accesstoken', 'user_id')

    models = {'oauth_tokens.accesstoken': {'Meta': {'ordering': "('-granted',)", 'object_name': 'AccessToken'}, 'access_token': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '200'}), 
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
       'oauth_tokens.usercredentials': {'Meta': {'object_name': 'UserCredentials'}, 'additional': (
                                                     'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                        'password': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'provider': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                        'username': (
                                                   'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'oauth_tokens']