# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/proyectos/django_venezuela/venezuela/migrations/0006_auto__chg_field_ciudad_capital.py
# Compiled at: 2014-01-23 11:05:38
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column('venezuela_ciudad', 'capital', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):
        db.alter_column('venezuela_ciudad', 'capital', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {'venezuela.ciudad': {'Meta': {'object_name': 'Ciudad'}, 'capital': (
                                      'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                            'ciudad': (
                                     'django.db.models.fields.CharField', [], {'max_length': '100'}), 
                            'estado': (
                                     'django.db.models.fields.related.ForeignKey', [], {'to': "orm['venezuela.Estado']"}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}, 
       'venezuela.estado': {'Meta': {'object_name': 'Estado'}, 'estado': (
                                     'django.db.models.fields.CharField', [], {'max_length': '50'}), 
                            'id': (
                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                            'iso_3166_2': (
                                         'django.db.models.fields.CharField', [], {'max_length': '5'})}, 
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