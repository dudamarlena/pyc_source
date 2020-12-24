# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mghantous/workspace/AgainFaster/country_block/migrations/0004_auto__add_request_timeouts.py
# Compiled at: 2014-01-02 15:40:49
import datetime
from django.core.cache import cache
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        cache.delete('country_block_settings')
        cache.delete('country_block_allowed_countries')
        db.add_column('country_block_settings', 'free_geo_ip_timeout', self.gf('django.db.models.fields.FloatField')(default=2.0), keep_default=False)
        db.add_column('country_block_settings', 'maxmind_timeout', self.gf('django.db.models.fields.FloatField')(default=6.0), keep_default=False)

    def backwards(self, orm):
        cache.delete('country_block_settings')
        cache.delete('country_block_allowed_countries')
        db.delete_column('country_block_settings', 'free_geo_ip_timeout')
        db.delete_column('country_block_settings', 'maxmind_timeout')

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
                                  'free_geo_ip_timeout': (
                                                        'django.db.models.fields.FloatField', [], {'default': '2.0'}), 
                                  'id': (
                                       'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                  'local_ip_user_country': (
                                                          'django.db.models.fields.related.ForeignKey', [], {'related_name': "'local_ip_user_settings'", 'to': "orm['country_block.Country']"}), 
                                  'location': (
                                             'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}), 
                                  'maxmind_enabled': (
                                                    'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                  'maxmind_license_key': (
                                                        'django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}), 
                                  'maxmind_local_db_enabled': (
                                                             'django.db.models.fields.BooleanField', [], {'default': 'False'}), 
                                  'maxmind_timeout': (
                                                    'django.db.models.fields.FloatField', [], {'default': '8.0'}), 
                                  'staff_user_country': (
                                                       'django.db.models.fields.related.ForeignKey', [], {'related_name': "'staff_user_settings'", 'to': "orm['country_block.Country']"})}}
    complete_apps = [
     'country_block']