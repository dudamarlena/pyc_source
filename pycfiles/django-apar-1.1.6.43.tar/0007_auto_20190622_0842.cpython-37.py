# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/notifications/migrations/0007_auto_20190622_0842.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 653 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0006_auto_20190615_1430')]
    operations = [
     migrations.AddField(model_name='notification',
       name='description_for_admin',
       field=models.TextField(blank=True, null=True, verbose_name='Description for admin')),
     migrations.AddField(model_name='notification',
       name='sent_result',
       field=models.TextField(blank=True, null=True, verbose_name='Sent result'))]