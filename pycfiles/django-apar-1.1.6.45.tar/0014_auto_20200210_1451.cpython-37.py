# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0014_auto_20200210_1451.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 459 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0013_auto_20190714_1639')]
    operations = [
     migrations.AlterField(model_name='filefield',
       name='password',
       field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='رمز عبور'))]