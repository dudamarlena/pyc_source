# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/news/migrations/0003_auto_20170726_1350.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 545 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0002_auto_20170717_1642')]
    operations = [
     migrations.AlterField(model_name='newsitem', name='publicationDate', field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date'))]