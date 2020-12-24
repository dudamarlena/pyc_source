# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/migrations/0010_auto_20200401_1452.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 759 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0009_auto_20200331_2041')]
    operations = [
     migrations.AddField(model_name='activity',
       name='data',
       field=models.TextField(blank=True, null=True)),
     migrations.AddField(model_name='activity',
       name='object_class',
       field=models.CharField(blank=True, max_length=255, null=True)),
     migrations.AddField(model_name='activity',
       name='object_id',
       field=models.BigIntegerField(blank=True, default=None, null=True))]