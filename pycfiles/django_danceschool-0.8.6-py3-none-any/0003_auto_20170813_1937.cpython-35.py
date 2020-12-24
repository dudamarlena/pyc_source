# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/prerequisites/migrations/0003_auto_20170813_1937.py
# Compiled at: 2018-03-26 19:55:31
# Size of source mod 2**32: 761 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('prerequisites', '0002_auto_20170717_1642')]
    operations = [
     migrations.AlterField(model_name='requirementitem', name='concurrentRule', field=models.CharField(choices=[('P', 'Must have previously taken'), ('1', 'May register/begin with one class remaining'), ('1', 'May register/begin with two classes remaining'), ('A', 'Concurrent registration allowed'), ('R', 'Concurrent registration required')], default='P', max_length=1, verbose_name='Concurrency Rule'))]