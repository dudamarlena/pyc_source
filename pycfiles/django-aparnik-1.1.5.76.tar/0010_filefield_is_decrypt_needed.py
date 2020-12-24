# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0010_filefield_is_decrypt_needed.py
# Compiled at: 2019-05-11 04:06:28
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0009_auto_20190511_1212')]
    operations = [
     migrations.AddField(model_name=b'filefield', name=b'is_decrypt_needed', field=models.BooleanField(default=False, verbose_name=b'Is decrypt needed?'))]