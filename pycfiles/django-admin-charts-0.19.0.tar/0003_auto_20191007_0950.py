# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/migrations/0003_auto_20191007_0950.py
# Compiled at: 2020-04-02 04:48:24
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin_tools_stats', '0002_auto_20190920_1058')]
    operations = [
     migrations.AddField(model_name='dashboardstats', name='default_chart_type', field=models.CharField(choices=[('discreteBarChart', 'Bar'), ('lineChart', 'Line'), ('multiBarChart', 'Multi Bar'), ('pieChart', 'Pie'), ('stackedAreaChart', 'Stacked Area'), ('multiBarHorizontalChart', 'Multi Bar Horizontal'), ('linePlusBarChart', 'Line Plus Bar'), ('scatterChart', 'Scatter'), ('cumulativeLineChart', 'Cumulative Line'), ('lineWithFocusChart', 'Line With Focus')], default='discreteBarChart', max_length=90, verbose_name='Default chart type')),
     migrations.AddField(model_name='dashboardstats', name='default_time_period', field=models.PositiveIntegerField(default=31, help_text='Number of days', verbose_name='Default period')),
     migrations.AddField(model_name='dashboardstats', name='default_time_scale', field=models.CharField(choices=[('hours', 'Hours'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default='days', max_length=90, verbose_name='Default time scale')),
     migrations.AddField(model_name='dashboardstatscriteria', name='use_as', field=models.CharField(choices=[('chart_filter', 'Chart filter'), ('multiple_series', 'Multiple series')], default='chart_filter', max_length=90, verbose_name='Use dynamic criteria as')),
     migrations.AlterField(model_name='dashboardstatscriteria', name='criteria_dynamic_mapping', field=jsonfield.fields.JSONField(blank=True, help_text='a JSON dictionary with records in two following possible formats:<br/>"key_value": "name"<br/>"key": [value, "name"]<br/>use blank key for no filter<br/>Example:<br/><pre>{<br/>  "": [null, "All"],<br/>  "True": [true, "True"],<br/>  "False": [false, "False"]<br/>}</pre><br/>Left blank to exploit all choices of CharField with choices', null=True, verbose_name='dynamic criteria / value'))]