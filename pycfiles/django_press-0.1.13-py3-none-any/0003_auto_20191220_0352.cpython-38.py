# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0003_auto_20191220_0352.py
# Compiled at: 2019-12-19 18:56:48
# Size of source mod 2**32: 414 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0002_auto_20191220_0223')]
    operations = [
     migrations.AlterField(model_name='contactcontent',
       name='form',
       field=models.CharField(max_length=100))]