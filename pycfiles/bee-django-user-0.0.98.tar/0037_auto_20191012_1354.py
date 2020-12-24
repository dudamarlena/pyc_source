# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0037_auto_20191012_1354.py
# Compiled at: 2019-10-12 01:54:41
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0036_userprofile_live_mins')]
    operations = [
     migrations.RemoveField(model_name=b'userclass', name=b'lecturer'),
     migrations.AddField(model_name=b'userprofile', name=b'lecturer', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'lecturer_user', to=b'bee_django_user.UserProfile', verbose_name=b'讲师'))]