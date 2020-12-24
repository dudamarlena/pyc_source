# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/proyectos/django_venezuela/venezuela/migrations/0004_auto__add_parroquia.py
# Compiled at: 2014-01-23 10:11:42
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.create_table('venezuela_parroquia', (
         (
          'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
         (
          'municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['venezuela.Municipio'])),
         (
          'parroquia', self.gf('django.db.models.fields.CharField')(max_length=100))))
        db.send_create_signal('venezuela', ['Parroquia'])

    def backwards(self, orm):
        db.delete_table('venezuela_parroquia')

    models = {'venezuela.ciudad': {'Meta': {'object_name': 'Ciudad'}, 'capital': (
                                      'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                            'ciudad': (
                                     'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                            'estado': (
                                     'django.db.models.fields.related.ForeignKey', [], {'to': "orm['venezuela.Estado']"}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}, 
       'venezuela.estado': {'Meta': {'object_name': 'Estado'}, 'estado': (
                                     'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}, 
       'venezuela.municipio': {'Meta': {'object_name': 'Municipio'}, 'estado': (
                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['venezuela.Estado']"}), 
                               'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'municipio': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}, 
       'venezuela.parroquia': {'Meta': {'object_name': 'Parroquia'}, 'id': (
                                    'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                               'municipio': (
                                           'django.db.models.fields.related.ForeignKey', [], {'to': "orm['venezuela.Municipio']"}), 
                               'parroquia': (
                                           'django.db.models.fields.CharField', [], {'max_length': '100'})}}
    complete_apps = [
     'venezuela']