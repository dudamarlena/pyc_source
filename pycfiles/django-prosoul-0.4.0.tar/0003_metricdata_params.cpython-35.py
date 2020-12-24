# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acs/devel/prosoul/django-prosoul/prosoul/migrations/0003_metricdata_params.py
# Compiled at: 2018-04-25 00:15:50
# Size of source mod 2**32: 413 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('prosoul', '0002_auto_20180307_2051')]
    operations = [
     migrations.AddField(model_name='metricdata', name='params', field=models.CharField(blank=True, max_length=1024, null=True))]