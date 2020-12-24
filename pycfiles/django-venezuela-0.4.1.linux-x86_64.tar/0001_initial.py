# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/proyectos/django_venezuela/venezuela/migrations/0001_initial.py
# Compiled at: 2014-01-23 10:01:33
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('venezuela_estado', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'estado', self.gf('django.db.models.fields.CharField')(max_length=50))))
        db.send_create_signal('venezuela', ['Estado'])

    def backwards(self, orm):
        db.delete_table('venezuela_estado')

    models = {'venezuela.estado': {'Meta': {'object_name': 'Estado'}, 'estado': (
                                     'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}}
    complete_apps = [
     'venezuela']