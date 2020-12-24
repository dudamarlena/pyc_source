# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0013_user_username_mention.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 498 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0012_auto_20190211_1416')]
    operations = [
     migrations.AddField(model_name='user',
       name='username_mention',
       field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Username for mention'))]