# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0020_auto_20190319_1753.py
# Compiled at: 2019-03-19 10:23:01
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0019_auto_20190319_1747')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'username_mention', field=models.CharField(default=b'a', max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code=b'invalid_username', message=b'Username must be Alphanumeric', regex=b'^[a-zA-Z_\\-0-9]+$')], verbose_name=b'Username for mention'))]