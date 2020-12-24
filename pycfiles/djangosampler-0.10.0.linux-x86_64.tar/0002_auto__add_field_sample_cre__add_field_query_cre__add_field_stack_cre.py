# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/migrations/0002_auto__add_field_sample_cre__add_field_query_cre__add_field_stack_cre.py
# Compiled at: 2015-11-17 05:08:04
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('djangosampler_sample', 'created_dt', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)
        db.add_column('djangosampler_query', 'created_dt', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)
        db.add_column('djangosampler_stack', 'created_dt', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

    def backwards(self, orm):
        db.delete_column('djangosampler_sample', 'created_dt')
        db.delete_column('djangosampler_query', 'created_dt')
        db.delete_column('djangosampler_stack', 'created_dt')

    models = {'djangosampler.query': {'Meta': {'object_name': 'Query'}, 'count': (
                                       'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                               'created_dt': (
                                            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                               'hash': (
                                      'django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}), 
                               'query': (
                                       'django.db.models.fields.TextField', [], {}), 
                               'query_type': (
                                            'django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}), 
                               'total_cost': (
                                            'django.db.models.fields.FloatField', [], {'default': '0'}), 
                               'total_duration': (
                                                'django.db.models.fields.FloatField', [], {'default': '0'})}, 
       'djangosampler.sample': {'Meta': {'object_name': 'Sample'}, 'cost': (
                                       'django.db.models.fields.FloatField', [], {}), 
                                'created_dt': (
                                             'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                                'duration': (
                                           'django.db.models.fields.FloatField', [], {}), 
                                'id': (
                                     'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                'params': (
                                         'django.db.models.fields.TextField', [], {}), 
                                'query': (
                                        'django.db.models.fields.TextField', [], {}), 
                                'stack': (
                                        'django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangosampler.Stack']"})}, 
       'djangosampler.stack': {'Meta': {'object_name': 'Stack'}, 'count': (
                                       'django.db.models.fields.IntegerField', [], {'default': '0'}), 
                               'created_dt': (
                                            'django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}), 
                               'hash': (
                                      'django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}), 
                               'query': (
                                       'django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangosampler.Query']"}), 
                               'stack': (
                                       'django.db.models.fields.TextField', [], {}), 
                               'total_cost': (
                                            'django.db.models.fields.FloatField', [], {'default': '0'}), 
                               'total_duration': (
                                                'django.db.models.fields.FloatField', [], {'default': '0'})}}
    complete_apps = [
     'djangosampler']