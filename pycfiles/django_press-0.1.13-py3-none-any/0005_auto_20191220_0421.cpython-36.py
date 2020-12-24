# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\migrations\0005_auto_20191220_0421.py
# Compiled at: 2019-12-19 18:56:48
# Size of source mod 2**32: 476 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_press', '0004_auto_20191220_0400')]
    operations = [
     migrations.AlterField(model_name='contactcontent',
       name='form',
       field=models.CharField(choices=[('Contact', 'django_press.models.Inquiry.contact')], max_length=100))]