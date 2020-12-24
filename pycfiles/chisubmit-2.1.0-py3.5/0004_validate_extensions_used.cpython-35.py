# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0004_validate_extensions_used.py
# Compiled at: 2017-09-19 13:56:43
# Size of source mod 2**32: 533 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0003_add_grace_period')]
    operations = [
     migrations.AlterField(model_name='submission', name='extensions_used', field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]))]