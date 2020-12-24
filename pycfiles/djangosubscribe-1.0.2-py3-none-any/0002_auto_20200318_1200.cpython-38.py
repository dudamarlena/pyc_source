# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangosubscribe\src\djangosubscribe\migrations\0002_auto_20200318_1200.py
# Compiled at: 2020-03-18 02:30:58
# Size of source mod 2**32: 693 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('djangosubscribe', '0001_initial')]
    operations = [
     migrations.AddField(model_name='subscribermodel',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AddField(model_name='subscribermodel',
       name='updated_at',
       field=models.DateTimeField(auto_now=True))]