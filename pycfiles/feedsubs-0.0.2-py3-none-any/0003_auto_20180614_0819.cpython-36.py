# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0003_auto_20180614_0819.py
# Compiled at: 2018-06-14 04:19:51
# Size of source mod 2**32: 404 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0002_auto_20180613_1758')]
    operations = [
     migrations.AlterField(model_name='article',
       name='published_at',
       field=models.DateTimeField(blank=True, null=True))]