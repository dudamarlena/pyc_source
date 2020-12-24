# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0006_auto_20191218_1404.py
# Compiled at: 2019-12-21 15:55:51
# Size of source mod 2**32: 558 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0005_auto_20191218_1402')]
    operations = [
     migrations.RemoveField(model_name='user',
       name='date_register'),
     migrations.AddField(model_name='user',
       name='date_verify',
       field=models.DateTimeField(blank=True, null=True, verbose_name='verify date'))]