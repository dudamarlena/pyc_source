# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0049_auto_20191121_1419.py
# Compiled at: 2019-11-21 01:19:11
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0048_auto_20191115_1607')]
    operations = [
     migrations.AlterField(model_name=b'userleveluprecord', name=b'level', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'bee_django_user_level', to=b'bee_django_user.UserLevel', verbose_name=b'升级标题'))]