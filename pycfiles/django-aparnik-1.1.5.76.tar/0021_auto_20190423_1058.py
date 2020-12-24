# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0021_auto_20190423_1058.py
# Compiled at: 2019-04-23 02:28:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0020_auto_20190319_1753')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'company_national_number', field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Company national number')),
     migrations.AddField(model_name=b'user', name=b'company_registration_number', field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Company registeration number'))]