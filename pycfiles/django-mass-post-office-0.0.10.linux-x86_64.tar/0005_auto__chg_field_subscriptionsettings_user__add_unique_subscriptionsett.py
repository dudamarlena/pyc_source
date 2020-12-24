# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/migrations/0005_auto__chg_field_subscriptionsettings_user__add_unique_subscriptionsett.py
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
        db.alter_column('mass_post_office_subscriptionsettings', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm[user_orm_label], unique=True))
        db.create_unique('mass_post_office_subscriptionsettings', ['user_id'])

    def backwards(self, orm):
        db.delete_unique('mass_post_office_subscriptionsettings', ['user_id'])
        db.alter_column('mass_post_office_subscriptionsettings', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label]))

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
                                                 'user': (
                                                        'django.db.models.fields.related.OneToOneField', [], {'to': "orm['%s']" % user_orm_label, 'unique': 'True'})}}
    complete_apps = [
     'mass_post_office']