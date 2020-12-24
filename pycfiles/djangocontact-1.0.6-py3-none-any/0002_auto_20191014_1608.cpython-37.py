# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangocontact\src\djangocontact\migrations\0002_auto_20191014_1608.py
# Compiled at: 2019-10-14 06:38:24
# Size of source mod 2**32: 695 bytes
from django.db import migrations, models
import djangocontact.validators

class Migration(migrations.Migration):
    dependencies = [
     ('djangocontact', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='emailmodel',
       name='phone_number',
       field=models.IntegerField(blank=True, null=True)),
     migrations.AlterField(model_name='emailmodel',
       name='subject',
       field=models.CharField(blank=True, max_length=30, null=True, validators=[djangocontact.validators.validate_subject]))]