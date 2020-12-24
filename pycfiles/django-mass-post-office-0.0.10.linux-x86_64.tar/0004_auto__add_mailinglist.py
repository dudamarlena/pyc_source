# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/migrations/0004_auto__add_mailinglist.py
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
user_ptr_name = '%s_ptr' % User._meta.module_name
user_id_name = '%s_id' % User._meta.module_name

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('mass_post_office_mailinglist', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(max_length=255)),
         (
          'user_should_be_agree', self.gf('django.db.models.fields.BooleanField')(default=True)),
         (
          'all_users', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'or_list', self.gf('django.db.models.fields.TextField')(default=''))))
        db.send_create_signal('mass_post_office', ['MailingList'])
        db.create_table('mass_post_office_mailinglist_additional_users', (
         (
          'id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
         (
          'mailinglist', models.ForeignKey(orm['mass_post_office.mailinglist'], null=False)),
         (
          User._meta.module_name, models.ForeignKey(orm[user_model_label], null=False))))
        db.create_unique('mass_post_office_mailinglist_additional_users', ['mailinglist_id', user_id_name])

    def backwards(self, orm):
        db.delete_table('mass_post_office_mailinglist')
        db.delete_table('mass_post_office_mailinglist_additional_users')

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
       'mass_post_office.subscriptionsettings': {'Meta': {'object_name': 'SubscriptionSettings'}, 'id': (
                                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                 'subscribed': (
                                                              'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                                 User._meta.object_name: (
                                                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})}}
    complete_apps = [
     'mass_post_office']