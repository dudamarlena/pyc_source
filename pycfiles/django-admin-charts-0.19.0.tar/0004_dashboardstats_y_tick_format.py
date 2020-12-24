# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/petr/.local/share/virtualenvs/blenderhub_server-izvs0qj4/src/django-admin-charts/admin_tools_stats/migrations/0004_dashboardstats_y_tick_format.py
# Compiled at: 2020-04-02 04:48:24
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('admin_tools_stats', '0003_auto_20191007_0950')]
    operations = [
     migrations.AddField(model_name='dashboardstats', name='y_axis_format', field=models.CharField(blank=True, default=None, help_text="Format of Y axis. <a href='https://github.com/d3/d3-format'>See description of possible values</a>.", max_length=90, null=True, verbose_name='Y axis format'))]