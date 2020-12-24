# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghorz/Desktop/works/django3/user_proj/user_app/migrations/0002_auto_20200319_1317.py
# Compiled at: 2020-03-19 09:17:05
# Size of source mod 2**32: 445 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('user_app', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='customuserprofile',
       name='date_joined',
       field=models.DateTimeField(default=(django.utils.timezone.now)))]