# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0042_auto_20191212_1436.py
# Compiled at: 2019-12-12 01:36:51
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0041_auto_20191210_1346')]
    operations = [
     migrations.AlterModelOptions(name=b'campaignrecord', options={b'ordering': [b'-created_at']}),
     migrations.RemoveField(model_name=b'wxuser', name=b'source_mkuser_id'),
     migrations.AlterField(model_name=b'campaignrecord', name=b'status', field=models.IntegerField(choices=[(1, '进行中'), (2, '已完成'), (3, '已消费')], default=1)),
     migrations.AlterField(model_name=b'wxuser', name=b'user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'来源缦客id'))]