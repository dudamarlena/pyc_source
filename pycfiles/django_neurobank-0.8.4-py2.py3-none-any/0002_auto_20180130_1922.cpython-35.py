# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0002_auto_20180130_1922.py
# Compiled at: 2018-01-30 19:22:58
# Size of source mod 2**32: 513 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import neurobank.tools

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='resource', name='name', field=models.SlugField(default=neurobank.tools.random_id, max_length=64, unique=True))]