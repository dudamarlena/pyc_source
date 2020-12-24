# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0002_date_joined_auto_now_add.py
# Compiled at: 2019-12-09 12:37:18
# Size of source mod 2**32: 442 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='user',
       name='date_joined',
       field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='join date'))]