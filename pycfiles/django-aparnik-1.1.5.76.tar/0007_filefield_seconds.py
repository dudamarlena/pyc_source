# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0007_filefield_seconds.py
# Compiled at: 2019-05-01 08:40:22
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0006_auto_20190501_1142')]
    operations = [
     migrations.AddField(model_name=b'filefield', name=b'seconds', field=models.BigIntegerField(default=0, verbose_name=b'زمان'))]