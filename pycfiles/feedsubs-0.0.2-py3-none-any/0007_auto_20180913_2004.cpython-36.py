# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0007_auto_20180913_2004.py
# Compiled at: 2018-09-13 16:04:14
# Size of source mod 2**32: 382 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0006_auto_20180906_1202')]
    operations = [
     migrations.AlterField(model_name='article',
       name='title',
       field=models.TextField(blank=True))]