# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/migrations/0002_auto_20181220_0803.py
# Compiled at: 2018-12-20 03:03:15
# Size of source mod 2**32: 401 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('preferences', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='preferences',
       name='sites',
       field=models.ManyToManyField(blank=True, to='sites.Site'))]