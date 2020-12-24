# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andermic/Development/django-custom-auth/custom_auth/migrations/0001_initial.py
# Compiled at: 2014-06-23 21:28:03
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('custom_auth_user', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'password', self.gf('django.db.models.fields.CharField')(max_length=128)),
         (
          'last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
         (
          'email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75, db_index=True)),
         (
          'first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now))))
        db.send_create_signal('custom_auth', ['User'])
        m2m_table_name = db.shorten_name('custom_auth_user_groups')
        db.create_table(m2m_table_name, (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'user', models.ForeignKey(orm['custom_auth.user'], null=False)),
         (
          'group', models.ForeignKey(orm['auth.group'], null=False))))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

    def backwards(self, orm):
        db.delete_table('custom_auth_user')
        db.delete_table(db.shorten_name('custom_auth_user_groups'))

    models = {'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                      'name': (
                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}), 
                      'permissions': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'auth.permission': {'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'}, 'codename': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                           'content_type': (
                                          'django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '50'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'custom_auth.user': {'Meta': {'object_name': 'User'}, 'date_joined': (
                                          'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                            'email': (
                                    'django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}), 
                            'first_name': (
                                         'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                            'groups': (
                                     'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'is_active': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                            'is_admin': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                            'last_login': (
                                         'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                            'last_name': (
                                        'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                            'password': (
                                       'django.db.models.fields.CharField', [], {'max_length': '128'})}}
    complete_apps = [
     'custom_auth']