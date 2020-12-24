# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0027_auto_20190526_1212.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 698 bytes
import aparnik.contrib.users.models
from django.db import migrations
import django_enumfield.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0026_auto_20190526_1210')]
    operations = [
     migrations.RemoveField(model_name='devicelogin',
       name='device_type_temp'),
     migrations.AlterField(model_name='devicelogin',
       name='device_type',
       field=django_enumfield.db.fields.EnumField(default=0, enum=(aparnik.contrib.users.models.DeviceType), verbose_name='Device Type'))]