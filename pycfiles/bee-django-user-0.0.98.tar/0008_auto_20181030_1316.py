# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0008_auto_20181030_1316.py
# Compiled at: 2018-10-30 01:16:11
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0007_auto_20181026_1751')]
    operations = [
     migrations.AddField(model_name=b'userleaverecord', name=b'created_by', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name=b'create_user', to=settings.AUTH_USER_MODEL), preserve_default=False),
     migrations.AlterField(model_name=b'userleaverecord', name=b'check_by', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'check_user', to=settings.AUTH_USER_MODEL))]