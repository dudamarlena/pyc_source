# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0028_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 459 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0027_auto_20190526_1212')]
    operations = [
     migrations.AlterField(model_name='user',
       name='sex',
       field=models.CharField(choices=[('M', 'مرد'), ('F', 'زن')], default='M', max_length=1, verbose_name='Sex'))]