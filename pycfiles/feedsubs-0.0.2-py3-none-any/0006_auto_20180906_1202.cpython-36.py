# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0006_auto_20180906_1202.py
# Compiled at: 2018-09-06 08:13:11
# Size of source mod 2**32: 541 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0005_feed_last_failure')]
    operations = [
     migrations.AlterField(model_name='article',
       name='id_in_feed',
       field=models.CharField(max_length=400)),
     migrations.AlterField(model_name='article',
       name='uri',
       field=models.URLField(max_length=400))]