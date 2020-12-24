# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0040_auto_20191206_1705.py
# Compiled at: 2019-12-06 04:05:01
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0039_wxuser_source_mkuser_id')]
    operations = [
     migrations.AddField(model_name=b'campaignrecord', name=b'bind_preuser', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.PreUser', verbose_name=b'红包发放新peruser账号')),
     migrations.AddField(model_name=b'campaignrecord', name=b'bind_user', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'红包发放用户账号')),
     migrations.AddField(model_name=b'campaignrecord', name=b'is_mk', field=models.BooleanField(default=False, verbose_name=b'是否是老缦客')),
     migrations.AddField(model_name=b'wxuser', name=b'city', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'微信城市')),
     migrations.AddField(model_name=b'wxuser', name=b'country', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'微信国家')),
     migrations.AddField(model_name=b'wxuser', name=b'gender', field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], null=True, verbose_name=b'微信性别')),
     migrations.AddField(model_name=b'wxuser', name=b'province', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'微信省份')),
     migrations.AddField(model_name=b'wxuser', name=b'tel', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'微信电话'))]