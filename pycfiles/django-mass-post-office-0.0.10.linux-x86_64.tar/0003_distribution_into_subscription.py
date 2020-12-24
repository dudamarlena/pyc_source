# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/migrations/0003_distribution_into_subscription.py
# Compiled at: 2015-03-06 05:08:58
import datetime
from south.db import db
from south.v2 import DataMigration
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

class Migration(DataMigration):

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass

    models = {user_model_label: {}, 'mass_post_office.subscriptionsettings': {'Meta': {'object_name': 'SubscriptionSettings'}, 'id': (
                                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                 'subscribed': (
                                                              'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                                 'user': (
                                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_orm_label})}}
    complete_apps = [
     'externalsite', 'mass_post_office']
    symmetrical = True