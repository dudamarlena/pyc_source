# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/dashboard/migrations/0002_auto_20160519_1705.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 859 bytes
from django.db import migrations
from django.core.management import call_command

def update_stats(apps, schema_editor):
    DashboardStatType = apps.get_model('dashboard', 'DashboardStatType')
    if not DashboardStatType.objects.filter(name='events_upcoming').exists():
        try:
            call_command('update_dashboard_stats')
        except:
            pass


class Migration(migrations.Migration):
    dependencies = [
     ('dashboard', '0001_initial')]
    operations = []