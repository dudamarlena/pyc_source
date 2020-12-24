# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0002_auto_20180613_1758.py
# Compiled at: 2018-06-13 13:58:55
# Size of source mod 2**32: 658 bytes
import django.contrib.postgres.fields
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='article',
       name='content',
       field=models.TextField(blank=True)),
     migrations.AlterField(model_name='subscription',
       name='tags',
       field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), blank=True, default=list, size=100))]