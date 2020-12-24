# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/affect/migrations/0001_initial.py
# Compiled at: 2013-05-13 18:17:38
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('affect_flag', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
         (
          'active', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
         (
          'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now))))
        db.send_create_signal('affect', ['Flag'])
        db.create_table('affect_flag_conflicts', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'from_flag', models.ForeignKey(orm['affect.flag'], null=False)),
         (
          'to_flag', models.ForeignKey(orm['affect.flag'], null=False))))
        db.create_unique('affect_flag_conflicts', ['from_flag_id', 'to_flag_id'])
        db.create_table('affect_criteria', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
         (
          'persistent', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'everyone', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
         (
          'percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=1, blank=True)),
         (
          'testing', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'superusers', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'authenticated', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'device_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
         (
          'entry_url', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
         (
          'referrer', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
         (
          'query_args', self.gf('django.db.models.fields.TextField')(default='{}', null=True, blank=True)),
         (
          'max_cookie_age', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
         (
          'note', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
         (
          'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now))))
        db.send_create_signal('affect', ['Criteria'])
        db.create_table('affect_criteria_flags', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'criteria', models.ForeignKey(orm['affect.criteria'], null=False)),
         (
          'flag', models.ForeignKey(orm['affect.flag'], null=False))))
        db.create_unique('affect_criteria_flags', ['criteria_id', 'flag_id'])
        db.create_table('affect_criteria_groups', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'criteria', models.ForeignKey(orm['affect.criteria'], null=False)),
         (
          'group', models.ForeignKey(orm['auth.group'], null=False))))
        db.create_unique('affect_criteria_groups', ['criteria_id', 'group_id'])
        db.create_table('affect_criteria_users', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'criteria', models.ForeignKey(orm['affect.criteria'], null=False)),
         (
          'user', models.ForeignKey(orm['auth.user'], null=False))))
        db.create_unique('affect_criteria_users', ['criteria_id', 'user_id'])

    def backwards(self, orm):
        db.delete_table('affect_flag')
        db.delete_table('affect_flag_conflicts')
        db.delete_table('affect_criteria')
        db.delete_table('affect_criteria_flags')
        db.delete_table('affect_criteria_groups')
        db.delete_table('affect_criteria_users')

    models = {'affect.criteria': {'Meta': {'object_name': 'Criteria'}, 'authenticated': (
                                           'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'created': (
                                     'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}), 
                           'device_type': (
                                         'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                           'entry_url': (
                                       'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                           'everyone': (
                                      'django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}), 
                           'flags': (
                                   'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['affect.Flag']", 'null': 'True', 'blank': 'True'}), 
                           'groups': (
                                    'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}), 
                           'id': (
                                'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                           'max_cookie_age': (
                                            'django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}), 
                           'modified': (
                                      'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                           'name': (
                                  'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}), 
                           'note': (
                                  'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                           'percent': (
                                     'django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}), 
                           'persistent': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'query_args': (
                                        'django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}), 
                           'referrer': (
                                      'django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}), 
                           'staff': (
                                   'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'superusers': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                           'testing': (
                                     'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                           'users': (
                                   'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})}, 
       'affect.flag': {'Meta': {'object_name': 'Flag'}, 'active': (
                                'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                       'conflicts': (
                                   'django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conflicts_rel_+'", 'null': 'True', 'to': "orm['affect.Flag']"}), 
                       'created': (
                                 'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}), 
                       'id': (
                            'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                       'modified': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                       'name': (
                              'django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}), 
                       'priority': (
                                  'django.db.models.fields.IntegerField', [], {'default': '0'})}, 
       'auth.group': {'Meta': {'object_name': 'Group'}, 'id': (
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
       'auth.user': {'Meta': {'object_name': 'User'}, 'date_joined': (
                                   'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'email': (
                             'django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}), 
                     'first_name': (
                                  'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'groups': (
                              'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'id': (
                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                     'is_active': (
                                 'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                     'is_staff': (
                                'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'is_superuser': (
                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                     'last_login': (
                                  'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                     'last_name': (
                                 'django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}), 
                     'password': (
                                'django.db.models.fields.CharField', [], {'max_length': '128'}), 
                     'user_permissions': (
                                        'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}), 
                     'username': (
                                'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})}, 
       'contenttypes.contenttype': {'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"}, 'app_label': (
                                                'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'id': (
                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                    'model': (
                                            'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                                    'name': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'affect']