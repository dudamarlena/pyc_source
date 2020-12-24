# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/migrations/0001_initial.py
# Compiled at: 2015-12-28 07:16:58
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('fandjango_user', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'facebook_id', self.gf('django.db.models.fields.BigIntegerField')()),
         (
          'first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'profile_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'gender', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
         (
          'oauth_token', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fandjango.OAuthToken'], unique=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'last_seen_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('fandjango', ['User'])
        db.create_table('fandjango_oauthtoken', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'token', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'issued_at', self.gf('django.db.models.fields.DateTimeField')()),
         (
          'expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))))
        db.send_create_signal('fandjango', ['OAuthToken'])

    def backwards(self, orm):
        db.delete_table('fandjango_user')
        db.delete_table('fandjango_oauthtoken')

    models = {'fandjango.oauthtoken': {'Meta': {'object_name': 'OAuthToken'}, 'expires_at': (
                                             'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'issued_at': (
                                            'django.db.models.fields.DateTimeField', [], {}), 
                                'token': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'fandjango.user': {'Meta': {'object_name': 'User'}, 'created_at': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                          'facebook_id': (
                                        'django.db.models.fields.BigIntegerField', [], {}), 
                          'first_name': (
                                       'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'gender': (
                                   'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'id': (
                               'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                          'last_name': (
                                      'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}), 
                          'last_seen_at': (
                                         'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                          'oauth_token': (
                                        'django.db.models.fields.related.OneToOneField', [], {'to': "orm['fandjango.OAuthToken']", 'unique': 'True'}), 
                          'profile_url': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'fandjango']