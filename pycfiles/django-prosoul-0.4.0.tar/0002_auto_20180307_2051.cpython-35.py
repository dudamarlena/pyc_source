# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acs/devel/prosoul/django-prosoul/prosoul/migrations/0002_auto_20180307_2051.py
# Compiled at: 2018-03-07 15:51:41
# Size of source mod 2**32: 592 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('prosoul', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='attribute', name='name', field=models.CharField(max_length=200)),
     migrations.AlterField(model_name='goal', name='name', field=models.CharField(max_length=200))]