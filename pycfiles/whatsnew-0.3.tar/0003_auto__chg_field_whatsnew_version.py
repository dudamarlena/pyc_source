# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/migrations/0003_auto__chg_field_whatsnew_version.py
# Compiled at: 2014-04-03 04:58:04
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('whatsnew_whatsnew', 'version', self.gf('semantic_version.django_fields.VersionField')(max_length=200))

    def backwards(self, orm):
        db.alter_column('whatsnew_whatsnew', 'version', self.gf('django.db.models.fields.CharField')(max_length=30))

    models = {'whatsnew.whatsnew': {'Meta': {'object_name': 'WhatsNew'}, 'content': (
                                       'django.db.models.fields.TextField', [], {}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'released': (
                                        'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                             'version': (
                                       'semantic_version.django_fields.VersionField', [], {'max_length': '200'})}}
    complete_apps = [
     'whatsnew']