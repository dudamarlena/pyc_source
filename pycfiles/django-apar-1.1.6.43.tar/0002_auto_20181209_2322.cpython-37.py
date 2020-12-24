# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0002_auto_20181209_2322.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 550 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='news',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u062a\\u0634\\u0627\\u0631'))]