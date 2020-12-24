# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0010_auto_20200228_1052.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 526 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0009_auto_20190821_1543')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='type',
       field=models.CharField(choices=[('i', 'اطلاعات'), ('ch', 'Chat'), ('s', 'موفقیت'), ('w', 'هشدار'), ('e', 'خطا')], max_length=2, verbose_name='Type'))]