# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0045_auto_20191220_1903.py
# Compiled at: 2019-12-20 06:03:32
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0044_auto_20191220_1754')]
    operations = [
     migrations.AddField(model_name=b'preuserfee', name=b'created_by', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'fee_created_by', to=settings.AUTH_USER_MODEL)),
     migrations.AlterField(model_name=b'preuserfee', name=b'checked_by', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'checked_by', to=settings.AUTH_USER_MODEL))]