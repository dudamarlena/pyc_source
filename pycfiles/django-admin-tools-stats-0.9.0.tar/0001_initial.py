# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/public_html/django/MyProjects/newfies-dialer/newfies/admin_tools_stats/migrations/0001_initial.py
# Compiled at: 2015-12-13 06:16:54
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'DashboardStats', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'graph_key', models.CharField(help_text=b'it needs to be one word unique. ex. auth, mygraph', max_length=90, unique=True, verbose_name=b'graph key')),
      (
       b'graph_title', models.CharField(db_index=True, help_text=b'heading title of graph box', max_length=90, verbose_name=b'graph title')),
      (
       b'model_app_name', models.CharField(help_text=b'ex. auth / dialer_cdr', max_length=90, verbose_name=b'app name')),
      (
       b'model_name', models.CharField(help_text=b'ex. User', max_length=90, verbose_name=b'model name')),
      (
       b'date_field_name', models.CharField(help_text=b'ex. date_joined', max_length=90, verbose_name=b'date field name')),
      (
       b'operation_field_name', models.CharField(blank=True, help_text=b'The field you want to aggregate, ex. amount', max_length=90, null=True, verbose_name=b'Operate field name')),
      (
       b'type_operation_field_name', models.CharField(blank=True, choices=[('Count', 'Count'), ('Sum', 'Sum'), ('Avg', 'Avg'), ('Max', 'Max'), ('Min', 'Min'), ('StdDev', 'StdDev'), ('Variance', 'Variance')], help_text=b'choose the type operation what you want to aggregate, ex. Sum', max_length=90, null=True, verbose_name=b'Choose Type operation')),
      (
       b'is_visible', models.BooleanField(default=True, verbose_name=b'visible')),
      (
       b'created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date')),
      (
       b'updated_date', models.DateTimeField(auto_now=True))], options={b'db_table': b'dashboard_stats', 
        b'verbose_name': b'dashboard stats', 
        b'verbose_name_plural': b'dashboard stats'}),
     migrations.CreateModel(name=b'DashboardStatsCriteria', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'criteria_name', models.CharField(db_index=True, help_text=b'it needs to be one word unique. Ex. status, yesno', max_length=90, verbose_name=b'criteria name')),
      (
       b'criteria_fix_mapping', jsonfield.fields.JSONField(blank=True, help_text=b'a JSON dictionary of key-value pairs that will be used for the criteria', null=True, verbose_name=b'fixed criteria / value')),
      (
       b'dynamic_criteria_field_name', models.CharField(blank=True, help_text=b'ex. for call records - disposition', max_length=90, null=True, verbose_name=b'dynamic criteria field name')),
      (
       b'criteria_dynamic_mapping', jsonfield.fields.JSONField(blank=True, help_text=b'a JSON dictionary of key-value pairs that will be used for the criteria', null=True, verbose_name=b'dynamic criteria / value')),
      (
       b'created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date')),
      (
       b'updated_date', models.DateTimeField(auto_now=True))], options={b'db_table': b'dash_stats_criteria', 
        b'verbose_name': b'dashboard stats criteria', 
        b'verbose_name_plural': b'dashboard stats criteria'}),
     migrations.AddField(model_name=b'dashboardstats', name=b'criteria', field=models.ManyToManyField(blank=True, null=True, to=b'admin_tools_stats.DashboardStatsCriteria'))]