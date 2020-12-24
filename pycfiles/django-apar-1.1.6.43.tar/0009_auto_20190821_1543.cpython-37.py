# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0009_auto_20190821_1543.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 410 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0008_auto_20190810_1836')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='description',
       field=models.TextField(verbose_name='Message'))]