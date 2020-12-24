# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\demo_site\migrations\0002_auto_20181003_1634.py
# Compiled at: 2018-10-03 10:34:54
# Size of source mod 2**32: 451 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('demo_site', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='accesstoken',
       name='success_url',
       field=models.CharField(default='/demo/', max_length=50, verbose_name='Success url'))]