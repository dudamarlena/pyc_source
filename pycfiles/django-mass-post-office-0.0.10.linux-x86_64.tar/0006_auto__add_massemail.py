# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/migrations/0006_auto__add_massemail.py
# Compiled at: 2015-03-06 05:08:58
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)
user_ptr_name = '%s_ptr' % User._meta.object_name.lower()

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('mass_post_office_massemail', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'mailing_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mass_post_office.MailingList'])),
         (
          'template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_office.EmailTemplate'])),
         (
          'scheduled_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
         (
          'priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True))))
        db.send_create_signal('mass_post_office', ['MassEmail'])
        db.create_table('mass_post_office_massemail_emails', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'massemail', models.ForeignKey(orm['mass_post_office.massemail'], null=False)),
         (
          'email', models.ForeignKey(orm['post_office.email'], null=False))))
        db.create_unique('mass_post_office_massemail_emails', ['massemail_id', 'email_id'])

    def backwards(self, orm):
        db.delete_table('mass_post_office_massemail')
        db.delete_table('mass_post_office_massemail_emails')

    models = {user_model_label: {}, 'mass_post_office.mailinglist': {'Meta': {'object_name': 'MailingList'}, 'additional_users': (
                                                           'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['%s']" % user_orm_label, 'null': 'True', 'symmetrical': 'False'}), 
                                        'all_users': (
                                                    'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                        'id': (
                                             'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                        'name': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                        'or_list': (
                                                  'django.db.models.fields.TextField', [], {'default': "''"}), 
                                        'user_should_be_agree': (
                                                               'django.db.models.fields.BooleanField', [], {'default': 'True'})}, 
       'mass_post_office.massemail': {'Meta': {'object_name': 'MassEmail'}, 'emails': (
                                               'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['post_office.Email']", 'null': 'True', 'blank': 'True'}), 
                                      'id': (
                                           'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                      'mailing_list': (
                                                     'django.db.models.fields.related.ForeignKey', [], {'to': "orm['mass_post_office.MailingList']"}), 
                                      'priority': (
                                                 'django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                      'scheduled_time': (
                                                       'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                                      'template': (
                                                 'django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_office.EmailTemplate']"})}, 
       'mass_post_office.subscriptionsettings': {'Meta': {'object_name': 'SubscriptionSettings'}, 'id': (
                                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                 'subscribed': (
                                                              'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                                 'user': (
                                                        'django.db.models.fields.related.OneToOneField', [], {'to': "orm['%s']" % user_orm_label, 'unique': 'True'})}, 
       'post_office.email': {'Meta': {'ordering': "('-created',)", 'object_name': 'Email'}, 'created': (
                                       'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}), 
                             'from_email': (
                                          'django.db.models.fields.CharField', [], {'max_length': '254'}), 
                             'headers': (
                                       'jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}), 
                             'html_message': (
                                            'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'last_updated': (
                                            'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}), 
                             'message': (
                                       'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                             'priority': (
                                        'django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                             'scheduled_time': (
                                              'django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                             'status': (
                                      'django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}), 
                             'subject': (
                                       'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}), 
                             'to': (
                                  'django.db.models.fields.EmailField', [], {'max_length': '254'})}, 
       'post_office.emailtemplate': {'Meta': {'ordering': "('name',)", 'object_name': 'EmailTemplate'}, 'content': (
                                               'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                     'created': (
                                               'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                     'html_content': (
                                                    'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                                     'id': (
                                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                     'last_updated': (
                                                    'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}), 
                                     'name': (
                                            'django.db.models.fields.CharField', [], {'max_length': '255'}), 
                                     'subject': (
                                               'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})}}
    complete_apps = [
     'mass_post_office']