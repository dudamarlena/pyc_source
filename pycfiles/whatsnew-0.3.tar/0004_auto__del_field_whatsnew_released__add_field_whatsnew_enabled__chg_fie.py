# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/migrations/0004_auto__del_field_whatsnew_released__add_field_whatsnew_enabled__chg_fie.py
# Compiled at: 2014-04-03 13:40:21
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('whatsnew_whatsnew', 'released')
        db.add_column('whatsnew_whatsnew', 'enabled', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
        db.alter_column('whatsnew_whatsnew', 'version', self.gf('whatsnew.fields.VersionField')(max_length=50))

    def backwards(self, orm):
        db.add_column('whatsnew_whatsnew', 'released', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)
        db.delete_column('whatsnew_whatsnew', 'enabled')
        db.alter_column('whatsnew_whatsnew', 'version', self.gf('semantic_version.django_fields.VersionField')(max_length=200))

    models = {'whatsnew.whatsnew': {'Meta': {'object_name': 'WhatsNew'}, 'content': (
                                       'django.db.models.fields.TextField', [], {}), 
                             'enabled': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                             'id': (
                                  'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                             'version': (
                                       'whatsnew.fields.VersionField', [], {'max_length': '50'})}}
    complete_apps = [
     'whatsnew']