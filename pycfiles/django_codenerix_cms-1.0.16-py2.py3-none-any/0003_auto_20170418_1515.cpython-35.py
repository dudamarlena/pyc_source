# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0003_auto_20170418_1515.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 624 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0002_auto_20170327_1021')]
    operations = [
     migrations.AlterField(model_name='staticheader', name='num_elements', field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)], verbose_name='Number of columns'))]