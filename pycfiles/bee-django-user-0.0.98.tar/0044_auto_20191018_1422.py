# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0044_auto_20191018_1422.py
# Compiled at: 2019-10-18 02:22:49
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0043_auto_20191018_1404')]
    operations = [
     migrations.AlterModelOptions(name=b'userlevel', options={b'ordering': [b'number'], b'permissions': (('view_level_list', '可以查看用户升级列表'), )}),
     migrations.RemoveField(model_name=b'userlevel', name=b'level'),
     migrations.AddField(model_name=b'userlevel', name=b'number', field=models.IntegerField(default=0, verbose_name=b'顺序')),
     migrations.AlterField(model_name=b'userleveluprecord', name=b'level', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'bee_django_user_level', to=b'bee_django_user.UserLevel', verbose_name=b'顺序'))]