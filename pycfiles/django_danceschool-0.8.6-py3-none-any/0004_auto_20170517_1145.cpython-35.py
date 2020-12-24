# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0004_auto_20170517_1145.py
# Compiled at: 2018-03-26 19:55:26
# Size of source mod 2**32: 2248 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0003_auto_20170516_0056')]
    operations = [
     migrations.RemoveField(model_name='series', name='dropinPrice'),
     migrations.AddField(model_name='pricingtier', name='dropinPrice', field=models.FloatField(default=0, help_text='If students are allowed to drop in, then this price will be applied per class.', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Single class drop-in price')),
     migrations.AlterField(model_name='pricingtier', name='doorGeneralPrice', field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='At-the-door price')),
     migrations.AlterField(model_name='pricingtier', name='doorStudentPrice', field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='At-the-door price for HS/college/university students')),
     migrations.AlterField(model_name='pricingtier', name='expired', field=models.BooleanField(default=False, help_text='If this box is checked, then this pricing tier will not show up as an option when creating new series.  Use this for old prices or custom pricing that will not be repeated.', verbose_name='Expired')),
     migrations.AlterField(model_name='pricingtier', name='onlineGeneralPrice', field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Online price')),
     migrations.AlterField(model_name='pricingtier', name='onlineStudentPrice', field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Online price for HS/college/university students'))]