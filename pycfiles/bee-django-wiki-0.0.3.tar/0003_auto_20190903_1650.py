# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_wiki/migrations/0003_auto_20190903_1650.py
# Compiled at: 2019-09-03 04:50:30
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_wiki', '0002_auto_20190903_1645')]
    operations = [
     migrations.AlterField(model_name=b'topic', name=b'tag', field=models.CharField(blank=True, max_length=180, null=True, verbose_name=b'标签'))]