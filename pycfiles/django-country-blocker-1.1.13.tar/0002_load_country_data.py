# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mghantous/workspace/AgainFaster/country_block/migrations/0002_load_country_data.py
# Compiled at: 2013-06-19 11:17:03
import datetime
from django.core.management import call_command
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """Write your forwards methods here."""
        call_command('loaddata', 'country.json')

    def backwards(self, orm):
        """Write your backwards methods here."""
        pass

    models = {'country_block.country': {'Meta': {'object_name': 'Country'}, 'country_code': (
                                                'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}), 
                                 'country_name': (
                                                'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}), 
                                 'id': (
                                      'django.db.models.fields.AutoField', [], {'primary_key': 'True'})}, 
       'country_block.settings': {'Meta': {'object_name': 'Settings'}, 'allowed_countries': (
                                                      'django.db.models.fields.related.ManyToManyField', [], {'to': "orm['country_block.Country']", 'symmetrical': 'False'}), 
                                  'free_geo_ip_enabled': (
                                                        'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'local_ip_user_country': (
                                                          'django.db.models.fields.related.ForeignKey', [], {'related_name': "'local_ip_user_settings'", 'to': "orm['country_block.Country']"}), 
                                  'location': (
                                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}), 
                                  'maxmind_enabled': (
                                                    'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                  'maxmind_local_db_enabled': (
                                                             'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                  'staff_user_country': (
                                                       'django.db.models.fields.related.ForeignKey', [], {'related_name': "'staff_user_settings'", 'to': "orm['country_block.Country']"})}}
    complete_apps = [
     'country_block']
    symmetrical = True