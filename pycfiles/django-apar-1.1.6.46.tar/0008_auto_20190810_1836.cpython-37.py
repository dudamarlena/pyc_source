# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0008_auto_20190810_1836.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 418 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0007_auto_20190622_0842')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='title',
       field=models.CharField(max_length=255, verbose_name='Title'))]