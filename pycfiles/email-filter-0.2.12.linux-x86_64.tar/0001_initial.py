# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/email_filter/migrations/0001_initial.py
# Compiled at: 2013-08-19 12:39:31
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('email_filter_emailredirect', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'email_in', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=250)),
         (
          'email_redirect', self.gf('django.db.models.fields.EmailField')(max_length=250))))
        db.send_create_signal('email_filter', ['EmailRedirect'])
        db.create_table('email_filter_emaillog', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'sender', self.gf('django.db.models.fields.EmailField')(max_length=250)),
         (
          'recipient', self.gf('django.db.models.fields.CharField')(max_length=750)),
         (
          'subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'raw_body', self.gf('django.db.models.fields.TextField')()),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))))
        db.send_create_signal('email_filter', ['EmailLog'])

    def backwards(self, orm):
        db.delete_table('email_filter_emailredirect')
        db.delete_table('email_filter_emaillog')

    models = {'email_filter.emaillog': {'Meta': {'object_name': 'EmailLog'}, 'created': (
                                           'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'raw_body': (
                                            'django.db.models.fields.TextField', [], {}), 
                                 'recipient': (
                                             'django.db.models.fields.CharField', [], {'max_length': '750'}), 
                                 'sender': (
                                          'django.db.models.fields.EmailField', [], {'max_length': '250'}), 
                                 'sent': (
                                        'django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}), 
                                 'subject': (
                                           'django.db.models.fields.CharField', [], {'max_length': '255'})}, 
       'email_filter.emailredirect': {'Meta': {'object_name': 'EmailRedirect'}, 'email_in': (
                                                 'django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '250'}), 
                                      'email_redirect': (
                                                       'django.db.models.fields.EmailField', [], {'max_length': '250'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}}
    complete_apps = [
     'email_filter']