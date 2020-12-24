# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/urb/Dropbox/dev/django-warp/django_warp/migrations/0002_auto_20170727_0821.py
# Compiled at: 2017-07-27 04:21:46
# Size of source mod 2**32: 962 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_warp', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='datasets', name='extentBottom', field=models.FloatField(default='-8000000.00')),
     migrations.AlterField(model_name='datasets', name='extentLeft', field=models.FloatField(default='-18000000.00')),
     migrations.AlterField(model_name='datasets', name='extentRight', field=models.FloatField(default='2000000.00')),
     migrations.AlterField(model_name='datasets', name='extentTop', field=models.FloatField(default='15000000.00'))]