# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/migrations/0005_auto_20200203_1537.py
# Compiled at: 2020-04-02 04:48:24
from django.db import migrations, models

def transform_distinct_count(apps, schema_editor):
    DashboardStats = apps.get_model('admin_tools_stats', 'DashboardStats')
    DashboardStats.objects.filter(type_operation_field_name='DistinctCount').update(type_operation_field_name='Count', distinct=True)


def transform_distinct_count_reverse(apps, schema_editor):
    DashboardStats = apps.get_model('admin_tools_stats', 'DashboardStats')
    DashboardStats.objects.filter(type_operation_field_name='Count', distinct=True).update(type_operation_field_name='DistinctCount')


class Migration(migrations.Migration):
    dependencies = [
     ('admin_tools_stats', '0004_dashboardstats_y_tick_format')]
    operations = [
     migrations.AddField(model_name='dashboardstats', name='distinct', field=models.BooleanField(blank=True, default=False, help_text="Note: Distinct is supported only for Count, Sum, Avg and 'Avgerage count per active model instance'.<br/>Django>=3.0 is needed for distinct Sum and Avg.")),
     migrations.AlterField(model_name='dashboardstats', name='type_operation_field_name', field=models.CharField(blank=True, choices=[('Count', 'Count'), ('Sum', 'Sum'), ('Avg', 'Avgerage'), ('AvgCountPerInstance', 'Avgerage count per active model instance'), ('Max', 'Max'), ('Min', 'Min'), ('StdDev', 'StdDev'), ('Variance', 'Variance')], help_text='choose the type operation what you want to aggregate, ex. Sum', max_length=90, null=True, verbose_name='Choose Type operation')),
     migrations.AlterField(model_name='dashboardstats', name='y_axis_format', field=models.CharField(blank=True, default=None, help_text="Format of Y axis.<a href='https://github.com/d3/d3-format' target='_blank'>See description of possible values</a>.", max_length=90, null=True, verbose_name='Y axis format')),
     migrations.RunPython(transform_distinct_count, reverse_code=transform_distinct_count_reverse)]