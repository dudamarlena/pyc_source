# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/news/migrations/0003_auto_20170726_1350.py
# Compiled at: 2019-04-03 22:56:31
# Size of source mod 2**32: 545 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0002_auto_20170717_1642')]
    operations = [
     migrations.AlterField(model_name='newsitem',
       name='publicationDate',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='Publication date'))]