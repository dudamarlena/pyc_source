# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0019_auto_20190319_1747.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 490 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0018_auto_20190319_1745')]
    operations = [
     migrations.AlterField(model_name='user',
       name='username_mention',
       field=models.CharField(default='a', max_length=100, unique=True, verbose_name='Username for mention'))]