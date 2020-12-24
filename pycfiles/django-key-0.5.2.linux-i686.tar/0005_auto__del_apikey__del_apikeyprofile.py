# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/key/migrations/0005_auto__del_apikey__del_apikeyprofile.py
# Compiled at: 2011-08-10 12:37:44
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table('key_apikey')
        db.delete_table('key_apikeyprofile')

    def backwards(self, orm):
        db.create_table('key_apikey', (
         (
          'profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_keys', to=orm['key.ApiKeyProfile'])),
         (
          'last_used', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
         (
          'logged_ip', self.gf('django.db.models.fields.CharField')(default=None, max_length=32, null=True, blank=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
         (
          'key', self.gf('django.db.models.fields.CharField')(default=None, max_length=16, unique=True, blank=True)),
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))))
        db.send_create_signal('key', ['ApiKey'])
        db.create_table('key_apikeyprofile', (
         (
          'max_keys', self.gf('django.db.models.fields.IntegerField')(default=-1)),
         (
          'last_access', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='key_profile', unique=True, to=orm['auth.User']))))
        db.send_create_signal('key', ['ApiKeyProfile'])
        return

    models = {}
    complete_apps = [
     'key']