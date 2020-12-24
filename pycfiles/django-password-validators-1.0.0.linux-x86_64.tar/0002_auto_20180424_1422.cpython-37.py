# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/password_history/migrations/0002_auto_20180424_1422.py
# Compiled at: 2020-01-08 09:44:25
# Size of source mod 2**32: 508 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('password_history', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='passwordhistory',
       name='password',
       field=models.CharField(editable=False, max_length=255, verbose_name='Password hash'))]