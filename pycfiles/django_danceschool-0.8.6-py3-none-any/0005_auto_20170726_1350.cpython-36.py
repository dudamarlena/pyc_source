# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0005_auto_20170726_1350.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 712 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0004_auto_20170717_1642')]
    operations = [
     migrations.AlterField(model_name='expenseitem',
       name='submissionDate',
       field=models.DateTimeField(auto_now_add=True, verbose_name='Submission date')),
     migrations.AlterField(model_name='revenueitem',
       name='submissionDate',
       field=models.DateTimeField(auto_now_add=True, verbose_name='Submission date'))]