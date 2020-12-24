# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\migrations\0002_auto_20190724_1927.py
# Compiled at: 2019-07-24 09:57:52
# Size of source mod 2**32: 511 bytes
from django.db import migrations, models
import djangoarticle.models

class Migration(migrations.Migration):
    dependencies = [
     ('djangoarticle', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='articlemodelscheme',
       name='cover_image',
       field=models.ImageField(blank=True, null=True, upload_to=(djangoarticle.models.image_upload_destination)))]