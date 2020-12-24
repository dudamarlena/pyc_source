# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0022_user_company_economical_number.py
# Compiled at: 2019-04-23 02:36:43
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0021_auto_20190423_1058')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'company_economical_number', field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Company economical number'))]