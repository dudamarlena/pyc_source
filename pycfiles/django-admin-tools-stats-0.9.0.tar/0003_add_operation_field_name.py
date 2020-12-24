# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-admin-tools-stats/admin_tools_stats/migrations/0003_add_operation_field_name.py
# Compiled at: 2014-05-30 17:44:50
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_column('dashboard_stats', 'sum_field_name')
        db.add_column('dashboard_stats', 'operation_field_name', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True), keep_default=False)
        db.add_column('dashboard_stats', 'type_operation_field_name', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True), keep_default=False)

    def backwards(self, orm):
        db.add_column('dashboard_stats', 'sum_field_name', self.gf('django.db.models.fields.CharField')(max_length=90, null=True, blank=True), keep_default=False)
        db.delete_column('dashboard_stats', 'operation_field_name')
        db.delete_column('dashboard_stats', 'type_operation_field_name')

    models = {'admin_tools_stats.dashboardstats': {'Meta': {'object_name': 'DashboardStats', 'db_table': "u'dashboard_stats'"}, 'created_date': (
                                                           'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                            'criteria': (
                                                       'django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['admin_tools_stats.DashboardStatsCriteria']", 'null': 'True', 'blank': 'True'}), 
                                            'date_field_name': (
                                                              'django.db.models.fields.CharField', [], {'max_length': '90'}), 
                                            'graph_key': (
                                                        'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '90'}), 
                                            'graph_title': (
                                                          'django.db.models.fields.CharField', [], {'max_length': '90', 'db_index': 'True'}), 
                                            'id': (
                                                 'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                            'is_visible': (
                                                         'django.db.models.fields.BooleanField', [], {'default': 'True'}), 
                                            'model_app_name': (
                                                             'django.db.models.fields.CharField', [], {'max_length': '90'}), 
                                            'model_name': (
                                                         'django.db.models.fields.CharField', [], {'max_length': '90'}), 
                                            'operation_field_name': (
                                                                   'django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}), 
                                            'type_operation_field_name': (
                                                                        'django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}), 
                                            'updated_date': (
                                                           'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}, 
       'admin_tools_stats.dashboardstatscriteria': {'Meta': {'object_name': 'DashboardStatsCriteria', 'db_table': "u'dash_stats_criteria'"}, 'created_date': (
                                                                   'django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}), 
                                                    'criteria_dynamic_mapping': (
                                                                               'jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}), 
                                                    'criteria_fix_mapping': (
                                                                           'jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}), 
                                                    'criteria_name': (
                                                                    'django.db.models.fields.CharField', [], {'max_length': '90', 'db_index': 'True'}), 
                                                    'dynamic_criteria_field_name': (
                                                                                  'django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True', 'blank': 'True'}), 
                                                    'id': (
                                                         'django.db.models.fields.AutoField', [], {'primary_key': 'True'}), 
                                                    'updated_date': (
                                                                   'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})}}
    complete_apps = [
     'admin_tools_stats']