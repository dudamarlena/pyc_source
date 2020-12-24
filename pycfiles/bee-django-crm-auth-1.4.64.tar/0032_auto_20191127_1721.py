# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0032_auto_20191127_1721.py
# Compiled at: 2019-11-27 04:21:34
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0031_wxuser')]
    operations = [
     migrations.AlterField(model_name=b'wxuser', name=b'nickname', field=models.CharField(max_length=180, null=True, verbose_name=b'微信昵称')),
     migrations.AlterField(model_name=b'wxuser', name=b'user', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]