# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/migrations/0002_auto_20190920_1058.py
# Compiled at: 2020-04-02 04:48:24
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin_tools_stats', '0001_initial')]
    operations = [
     migrations.AddField(model_name='dashboardstats', name='user_field_name', field=models.CharField(blank=True, help_text='ex. owner, invitation__owner', max_length=90, null=True, verbose_name='user field name')),
     migrations.AlterField(model_name='dashboardstats', name='date_field_name', field=models.CharField(help_text='ex. date_joined, invitation__invitation_date', max_length=90, verbose_name='date field name')),
     migrations.AlterField(model_name='dashboardstats', name='graph_key', field=models.CharField(help_text='it needs to be one word unique. ex. auth, mygraph', max_length=90, unique=True, verbose_name='graph identifier')),
     migrations.AlterField(model_name='dashboardstats', name='operation_field_name', field=models.CharField(blank=True, help_text='The field you want to aggregate, ex. amount, salaries__total_income', max_length=90, null=True, verbose_name='Operate field name')),
     migrations.AlterField(model_name='dashboardstats', name='type_operation_field_name', field=models.CharField(blank=True, choices=[('DistinctCount', 'DistinctCount'), ('Count', 'Count'), ('Sum', 'Sum'), ('Avg', 'Avg'), ('Max', 'Max'), ('Min', 'Min'), ('StdDev', 'StdDev'), ('Variance', 'Variance')], help_text='choose the type operation what you want to aggregate, ex. Sum', max_length=90, null=True, verbose_name='Choose Type operation')),
     migrations.AlterField(model_name='dashboardstatscriteria', name='criteria_dynamic_mapping', field=jsonfield.fields.JSONField(blank=True, help_text='a JSON dictionary of key-value pairs that will be used for the criteria Ex. "{\'false\': \'Inactive\', \'true\': \'Active\'}"', null=True, verbose_name='dynamic criteria / value'))]