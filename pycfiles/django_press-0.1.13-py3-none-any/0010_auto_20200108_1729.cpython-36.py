# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0010_auto_20200108_1729.py
# Compiled at: 2020-01-08 03:29:44
# Size of source mod 2**32: 408 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0009_page_publish')]
    operations = [
     migrations.AlterField(model_name='tab',
       name='name',
       field=models.CharField(default='', max_length=50))]