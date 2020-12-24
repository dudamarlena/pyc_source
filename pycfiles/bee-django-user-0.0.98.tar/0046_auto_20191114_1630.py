# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0046_auto_20191114_1630.py
# Compiled at: 2019-11-14 03:30:26
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0045_auto_20191023_1531')]
    operations = [
     migrations.RemoveField(model_name=b'userprofile', name=b'agent'),
     migrations.RemoveField(model_name=b'userprofile', name=b'lecturer'),
     migrations.AddField(model_name=b'userclass', name=b'agent', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'agent_user', to=settings.AUTH_USER_MODEL)),
     migrations.AddField(model_name=b'userclass', name=b'lecturer', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'lecturer_user', to=settings.AUTH_USER_MODEL, verbose_name=b'讲师')),
     migrations.AlterField(model_name=b'userclass', name=b'assistant', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'assistant_user', to=settings.AUTH_USER_MODEL, verbose_name=b'助教'))]