# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0003_user_verify_mobile.py
# Compiled at: 2018-10-16 22:51:53
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0002_user_passwd')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'verify_mobile', field=models.BooleanField(default=False, verbose_name=b'Verify Mobile'))]