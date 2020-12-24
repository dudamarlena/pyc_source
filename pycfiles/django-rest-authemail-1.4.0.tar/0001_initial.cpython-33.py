# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Celia/python/django-rest-authemail/authemail/migrations/0001_initial.py
# Compiled at: 2014-08-23 12:50:37
# Size of source mod 2**32: 5812 bytes
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('authemail_signupcode', (
         (
          'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MyUser'])),
         (
          'code', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
         (
          'ipaddr', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39))))
        db.send_create_signal('authemail', ['SignupCode'])
        db.create_table('authemail_passwordresetcode', (
         (
          'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MyUser'])),
         (
          'code', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
         (
          'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True))))
        db.send_create_signal('authemail', ['PasswordResetCode'])

    def backwards(self, orm):
        db.delete_table('authemail_signupcode')
        db.delete_table('authemail_passwordresetcode')

    models = {'accounts.myuser': {'Meta': {'object_name': 'MyUser'},  'date_joined': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'date_of_birth': (
                                           'django.db.models.fields.DateField', [], {'null': 'True',  'blank': 'True'}), 
                         'email': (
                                   'django.db.models.fields.EmailField', [], {'unique': 'True',  'max_length': '255'}), 
                         'first_name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '30',  'blank': 'True'}), 
                         'groups': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False',  'related_name': "u'user_set'",  'blank': 'True',  'to': "orm['auth.Group']"}), 
                         'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'is_active': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                         'is_staff': (
                                      'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'is_superuser': (
                                          'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'is_verified': (
                                         'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                         'last_login': (
                                        'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                         'last_name': (
                                       'django.db.models.fields.CharField', [], {'max_length': '30',  'blank': 'True'}), 
                         'password': (
                                      'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                         'user_permissions': (
                                              'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False',  'related_name': "u'user_set'",  'blank': 'True',  'to': "orm['auth.Permission']"})}, 
     'auth.group': {'Meta': {'object_name': 'Group'},  'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                    'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True',  'max_length': '80'}), 
                    'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']",  'symmetrical': 'False',  'blank': 'True'})}, 
     'auth.permission': {'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",  'unique_together': "((u'content_type', u'codename'),)",  'object_name': 'Permission'},  'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                         'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                         'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                         'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
     'authemail.passwordresetcode': {'Meta': {'object_name': 'PasswordResetCode'},  'code': (
                                              'django.db.models.fields.CharField', [], {'max_length': '40',  'primary_key': 'True'}), 
                                     'created_at': (
                                                    'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True',  'blank': 'True'}), 
                                     'user': (
                                              'django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.MyUser']"})}, 
     'authemail.signupcode': {'Meta': {'object_name': 'SignupCode'},  'code': (
                                       'django.db.models.fields.CharField', [], {'max_length': '40',  'primary_key': 'True'}), 
                              'created_at': (
                                             'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True',  'blank': 'True'}), 
                              'ipaddr': (
                                         'django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}), 
                              'user': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.MyUser']"})}, 
     'contenttypes.contenttype': {'Meta': {'ordering': "('name',)",  'unique_together': "(('app_label', 'model'),)",  'object_name': 'ContentType',  'db_table': "'django_content_type'"},  'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                  'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                  'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'authemail']