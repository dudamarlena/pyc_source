# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0052_auto_20191213_1503.py
# Compiled at: 2019-12-13 02:03:51
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0051_auto_20191122_1324')]
    operations = [
     migrations.AlterField(model_name=b'userlevel', name=b'after_group', field=models.ForeignKey(blank=True, help_text=b'（不可多选）', null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'user_after_group', to=b'auth.Group', verbose_name=b'升级后的用户组'))]