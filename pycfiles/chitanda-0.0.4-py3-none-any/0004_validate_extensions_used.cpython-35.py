# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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