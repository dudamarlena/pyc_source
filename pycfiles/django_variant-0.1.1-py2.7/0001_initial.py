# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/migrations/0001_initial.py
# Compiled at: 2014-08-25 19:08:08
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('variant_experiment', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
         (
          'description', self.gf('django.db.models.fields.TextField')(blank=True)),
         (
          'active', self.gf('django.db.models.fields.BooleanField')(default=False)),
         (
          'variants', self.gf('django.db.models.fields.TextField')())))
        db.send_create_signal('variant', ['Experiment'])

    def backwards(self, orm):
        db.delete_table('variant_experiment')

    models = {'variant.experiment': {'Meta': {'object_name': 'Experiment'}, 'active': (
                                       'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                              'description': (
                                            'django.db.models.fields.TextField', [], {'blank': 'True'}), 
                              'id': (
                                   'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                              'name': (
                                     'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}), 
                              'variants': (
                                         'django.db.models.fields.TextField', [], {})}}
    complete_apps = [
     'variant']