# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_postfix/migrations/0001_initial.py
# Compiled at: 2012-06-04 12:04:47
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('domains', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
         (
          'description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
         (
          'active', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'aliases', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'mailboxes', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'backupmx', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'transport', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('django_postfix', ['Domain'])
        db.create_table('mailboxes', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_postfix.Domain'])),
         (
          'username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
         (
          'password', self.gf('django.db.models.fields.CharField')(max_length=128)),
         (
          'maildir', self.gf('django.db.models.fields.CharField')(max_length=128)),
         (
          'quote', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('django_postfix', ['Mailbox'])
        db.create_unique('mailboxes', ['domain_id', 'username'])
        db.create_table('aliases', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'alias', self.gf('django.db.models.fields.CharField')(max_length=128)),
         (
          'mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_postfix.Mailbox'])),
         (
          'domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_postfix.Domain'], null=True, blank=True)),
         (
          'active', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True))))
        db.send_create_signal('django_postfix', ['Alias'])
        db.create_unique('aliases', ['alias', 'mailbox_id'])

    def backwards(self, orm):
        db.delete_unique('aliases', ['alias', 'mailbox_id'])
        db.delete_unique('mailboxes', ['domain_id', 'username'])
        db.delete_table('domains')
        db.delete_table('mailboxes')
        db.delete_table('aliases')

    models = {'django_postfix.alias': {'Meta': {'unique_together': "(('alias', 'mailbox'),)", 'object_name': 'Alias', 'db_table': "'aliases'"}, 'active': (
                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                'alias': (
                                        'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                                'created': (
                                          'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                'domain': (
                                         'django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_postfix.Domain']", 'null': 'True', 'blank': 'True'}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'mailbox': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_postfix.Mailbox']"}), 
                                'modified': (
                                           'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'django_postfix.domain': {'Meta': {'object_name': 'Domain', 'db_table': "'domains'"}, 'active': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'aliases': (
                                           'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'backupmx': (
                                            'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'created': (
                                           'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                 'description': (
                                               'django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}), 
                                 'domain': (
                                          'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                 'mailboxes': (
                                             'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                 'modified': (
                                            'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                 'transport': (
                                             'django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})}, 
       'django_postfix.mailbox': {'Meta': {'unique_together': "(('domain', 'username'),)", 'object_name': 'Mailbox', 'db_table': "'mailboxes'"}, 'created': (
                                            'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                  'domain': (
                                           'django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_postfix.Domain']"}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'maildir': (
                                            'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                                  'modified': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                  'password': (
                                             'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                                  'quote': (
                                          'django.db.models.fields.PositiveIntegerField', [], {'default': '0'}), 
                                  'username': (
                                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})}}
    complete_apps = [
     'django_postfix']