# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0005_auto_20190830_1413.py
# Compiled at: 2019-08-30 02:13:43
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_report', '0004_auto_20190711_1718')]
    operations = [
     migrations.AddField(model_name=b'classweek', name=b'live_commented_count', field=models.IntegerField(default=0)),
     migrations.AddField(model_name=b'classweek', name=b'live_watched_count', field=models.IntegerField(default=0)),
     migrations.AddField(model_name=b'classweek', name=b'live_watched_days', field=models.IntegerField(default=0)),
     migrations.AlterField(model_name=b'classweek', name=b'feed_count', field=models.IntegerField(default=0)),
     migrations.AlterField(model_name=b'classweek', name=b'live_count', field=models.IntegerField(default=0)),
     migrations.AlterField(model_name=b'classweek', name=b'live_days', field=models.IntegerField(default=0)),
     migrations.AlterField(model_name=b'classweek', name=b'live_mins', field=models.IntegerField(default=0))]