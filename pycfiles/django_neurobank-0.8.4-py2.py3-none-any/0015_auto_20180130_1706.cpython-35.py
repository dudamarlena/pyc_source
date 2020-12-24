# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0015_auto_20180130_1706.py
# Compiled at: 2018-01-30 17:26:12
# Size of source mod 2**32: 671 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0014_auto_20170712_1018')]
    operations = [
     migrations.AddField(model_name='resource', name='id', field=models.AutoField(primary_key=True, serialize=False), preserve_default=False),
     migrations.AlterField(model_name='resource', name='name', field=models.SlugField(max_length=64, unique=True))]