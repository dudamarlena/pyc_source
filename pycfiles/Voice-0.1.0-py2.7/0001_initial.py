# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/voice/migrations/0001_initial.py
# Compiled at: 2011-09-20 01:00:28
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('voice_request', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'state', self.gf('django.db.models.fields.CharField')(max_length=1)),
         (
          'title', self.gf('django.db.models.fields.CharField')(max_length=50)),
         (
          'description', self.gf('django.db.models.fields.TextField')(max_length=140)),
         (
          'votes_needed', self.gf('django.db.models.fields.IntegerField')()),
         (
          'created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True))))
        db.send_create_signal('voice', ['Request'])
        db.create_table('voice_vote', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voice.Request'])),
         (
          'voter', self.gf('django.db.models.fields.EmailField')(max_length=75)),
         (
          'used_twitter', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'used_facebook', self.gf('django.db.models.fields.BooleanField')(default=False))))
        db.send_create_signal('voice', ['Vote'])

    def backwards(self, orm):
        db.delete_table('voice_request')
        db.delete_table('voice_vote')

    models = {'voice.request': {'Meta': {'object_name': 'Request'}, 'created': (
                                   'django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                         'description': (
                                       'django.db.models.fields.TextField', [], {'max_length': '140'}), 
                         'id': (
                              'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'state': (
                                 'django.db.models.fields.CharField', [], {'max_length': '1'}), 
                         'title': (
                                 'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                         'votes_needed': (
                                        'django.db.models.fields.IntegerField', [], {})}, 
       'voice.vote': {'Meta': {'object_name': 'Vote'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'request': (
                                'django.db.models.fields.related.ForeignKey', [], {'to': "orm['voice.Request']"}), 
                      'used_facebook': (
                                      'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                      'used_twitter': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                      'voter': (
                              'django.db.models.fields.EmailField', [], {'max_length': '75'})}}
    complete_apps = [
     'voice']