# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0004_filefield_title.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 491 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0003_auto_20181026_1745')]
    operations = [
     migrations.AddField(model_name='filefield',
       name='title',
       field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\\u0639\\u0646\\u0648\\u0627\\u0646'))]