# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/migrations/0007_auto_20200205_1054.py
# Compiled at: 2020-04-02 04:48:24
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('admin_tools_stats', '0006_auto_20200205_0944')]
    operations = [
     migrations.RemoveField(model_name='dashboardstats', name='criteria'),
     migrations.AlterField(model_name='criteriatostatsm2m', name='criteria', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_tools_stats.DashboardStatsCriteria')),
     migrations.AlterField(model_name='criteriatostatsm2m', name='stats', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_tools_stats.DashboardStats')),
     migrations.AlterField(model_name='dashboardstats', name='criteria_new', field=models.ManyToManyField(blank=True, through='admin_tools_stats.CriteriaToStatsM2M', to='admin_tools_stats.DashboardStatsCriteria')),
     migrations.RenameField(model_name='dashboardstats', old_name='criteria_new', new_name='criteria'),
     migrations.RemoveField(model_name='dashboardstatscriteria', name='use_as'),
     migrations.AlterField(model_name='criteriatostatsm2m', name='prefix', field=models.CharField(blank=True, default='', help_text='prefix, that will be added befor all lookup paths of criteria', max_length=255, verbose_name='criteria field prefix'))]