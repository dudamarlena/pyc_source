# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/dev/tur/yandex_maps/migrations/0001_initial.py
# Compiled at: 2009-09-03 17:19:45
from south.db import db
from django.db import models
from yandex_maps.models import *

class Migration:

    def forwards(self, orm):
        db.create_table('yandex_maps_mapandaddress', (
         (
          'id', orm['yandex_maps.MapAndAddress:id']),
         (
          'address', orm['yandex_maps.MapAndAddress:address']),
         (
          'longtitude', orm['yandex_maps.MapAndAddress:longtitude']),
         (
          'latitude', orm['yandex_maps.MapAndAddress:latitude'])))
        db.send_create_signal('yandex_maps', ['MapAndAddress'])

    def backwards(self, orm):
        db.delete_table('yandex_maps_mapandaddress')

    models = {'yandex_maps.mapandaddress': {'address': (
                                               'django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}), 
                                     'id': (
                                          'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                     'latitude': (
                                                'django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}), 
                                     'longtitude': (
                                                  'django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})}}
    complete_apps = [
     'yandex_maps']