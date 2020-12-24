# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangosubscribe\src\djangosubscribe\migrations\0003_auto_20200318_1242.py
# Compiled at: 2020-03-18 03:12:51
# Size of source mod 2**32: 432 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangosubscribe', '0002_auto_20200318_1200')]
    operations = [
     migrations.AlterField(model_name='subscribermodel',
       name='email',
       field=models.EmailField(max_length=75, unique=True))]