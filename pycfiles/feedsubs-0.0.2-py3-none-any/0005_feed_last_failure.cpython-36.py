# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0005_feed_last_failure.py
# Compiled at: 2018-09-06 07:29:22
# Size of source mod 2**32: 384 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0004_auto_20180614_1808')]
    operations = [
     migrations.AddField(model_name='feed',
       name='last_failure',
       field=models.TextField(blank=True))]