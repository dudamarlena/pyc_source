# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/FoneAstra-3.0.0.1-py2.7.egg/fa/migrations/0001_initial.py
# Compiled at: 2012-11-11 16:40:31
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('fa_incomingmessage', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'sender', self.gf('django.db.models.fields.CharField')(max_length=25)),
         (
          'content', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'send_time', self.gf('django.db.models.fields.DateTimeField')()),
         (
          'transport', self.gf('django.db.models.fields.CharField')(max_length=255))))
        db.send_create_signal('fa', ['IncomingMessage'])
        db.create_table('fa_outgoingmessage', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'target', self.gf('django.db.models.fields.CharField')(max_length=20)),
         (
          'content', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'transport', self.gf('django.db.models.fields.CharField')(max_length=255))))
        db.send_create_signal('fa', ['OutgoingMessage'])

    def backwards(self, orm):
        db.delete_table('fa_incomingmessage')
        db.delete_table('fa_outgoingmessage')

    models = {'fa.incomingmessage': {'Meta': {'object_name': 'IncomingMessage'}, 'content': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'send_time': (
                                          'django.db.models.fields.DateTimeField', [], {}), 
                              'sender': (
                                       'django.db.models.fields.CharField', [], {'max_length': '25'}), 
                              'transport': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'fa.outgoingmessage': {'Meta': {'object_name': 'OutgoingMessage'}, 'content': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'target': (
                                       'django.db.models.fields.CharField', [], {'max_length': '20'}), 
                              'transport': (
                                          'django.db.models.fields.CharField', [], {'max_length': '255'})}}
    complete_apps = [
     'fa']