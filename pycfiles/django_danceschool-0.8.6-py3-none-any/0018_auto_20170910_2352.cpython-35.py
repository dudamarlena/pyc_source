# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0018_auto_20170910_2352.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 2231 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0017_auto_20170909_0024')]
    operations = [
     migrations.AlterField(model_name='invoice', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data')),
     migrations.AddField(model_name='invoice', name='email', field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Recipient email address')),
     migrations.AddField(model_name='invoice', name='firstName', field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Recipient first name')),
     migrations.AddField(model_name='invoice', name='lastName', field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Recipient last name')),
     migrations.AlterField(model_name='customer', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data')),
     migrations.AlterField(model_name='eventregistration', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data')),
     migrations.AlterField(model_name='registration', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data')),
     migrations.AlterField(model_name='temporaryeventregistration', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data')),
     migrations.AlterField(model_name='temporaryregistration', name='data', field=jsonfield.fields.JSONField(blank=True, default={}, verbose_name='Additional data'))]