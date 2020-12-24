# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acs/devel/prosoul/django-prosoul/prosoul/migrations/0004_auto_20181003_1029.py
# Compiled at: 2018-10-03 06:29:50
# Size of source mod 2**32: 561 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('prosoul', '0003_metricdata_params')]
    operations = [
     migrations.AlterField(model_name='attribute', name='name', field=models.CharField(max_length=200, unique=True)),
     migrations.AlterField(model_name='goal', name='name', field=models.CharField(max_length=200, unique=True))]