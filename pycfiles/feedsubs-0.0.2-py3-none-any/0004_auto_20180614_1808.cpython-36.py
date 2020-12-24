# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0004_auto_20180614_1808.py
# Compiled at: 2018-06-14 14:08:20
# Size of source mod 2**32: 515 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0003_auto_20180614_0819')]
    operations = [
     migrations.AlterField(model_name='feed',
       name='name',
       field=models.CharField(max_length=100)),
     migrations.AlterUniqueTogether(name='article',
       unique_together={
      ('feed', 'id_in_feed')})]