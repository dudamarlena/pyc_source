# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/migrations/0002_auto__add_field_whatsnew_released.py
# Compiled at: 2014-04-02 14:28:33
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('whatsnew_whatsnew', 'released', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

    def backwards(self, orm):
        db.delete_column('whatsnew_whatsnew', 'released')

    models = {'whatsnew.whatsnew': {'Meta': {'object_name': 'WhatsNew'}, 'content': (
                                       'django.db.models.fields.TextField', [], {}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'released': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                             'version': (
                                       'django.db.models.fields.CharField', [], {'max_length': '30'})}}
    complete_apps = [
     'whatsnew']