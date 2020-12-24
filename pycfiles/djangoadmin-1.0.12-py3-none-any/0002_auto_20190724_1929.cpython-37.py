# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoadmin\src\djangoadmin\migrations\0002_auto_20190724_1929.py
# Compiled at: 2019-07-24 09:59:15
# Size of source mod 2**32: 490 bytes
from django.db import migrations, models
import djangoadmin.models

class Migration(migrations.Migration):
    dependencies = [
     ('djangoadmin', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='usermodel',
       name='image',
       field=models.ImageField(blank=True, null=True, upload_to=(djangoadmin.models.image_upload_destination)))]