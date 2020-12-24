# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/migrations/0002_auto__add_subscriptionsettings.py
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
        db.create_table('mass_post_office_subscriptionsettings', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[user_orm_label])),
         (
          'subscribed', self.gf('django.db.models.fields.BooleanField')(default=True))))
        db.send_create_signal('mass_post_office', ['SubscriptionSettings'])

    def backwards(self, orm):
        db.delete_table('mass_post_office_subscriptionsettings')

    models = {user_model_label: {}, 'mass_post_office.subscriptionsettings': {'Meta': {'object_name': 'SubscriptionSettings'}, 'id': (
                                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                 'subscribed': (
                                                              'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                                 'user': (
                                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})}}
    complete_apps = [
     'mass_post_office']