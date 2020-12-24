# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/migrations/0007_auto__add_unique_user_facebook_id.py
# Compiled at: 2015-12-28 07:16:58
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_unique('fandjango_user', ['facebook_id'])

    def backwards(self, orm):
        db.delete_unique('fandjango_user', ['facebook_id'])

    models = {'fandjango.oauthtoken': {'Meta': {'object_name': 'OAuthToken'}, 'expires_at': (
                                             'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'issued_at': (
                                            'django.db.models.fields.DateTimeField', [], {}), 
                                'token': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'fandjango.user': {'Meta': {'object_name': 'User'}, 'authorized': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                          'birthday': (
                                     'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}), 
                          'created_at': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                          'facebook_id': (
                                        'django.db.models.fields.BigIntegerField', [], {'unique': 'True'}), 
                          'facebook_username': (
                                              'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'first_name': (
                                       'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'last_name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'last_seen_at': (
                                         'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                          'middle_name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'oauth_token': (
                                        'django.db.models.fields.related.OneToOneField', [], {'to': "orm['fandjango.OAuthToken']", 'unique': 'True'}), 
                          'verified': (
                                     'django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'fandjango']