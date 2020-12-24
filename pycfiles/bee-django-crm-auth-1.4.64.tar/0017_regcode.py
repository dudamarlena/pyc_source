# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0017_regcode.py
# Compiled at: 2019-04-22 01:46:09
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0016_auto_20190111_1554')]
    operations = [
     migrations.CreateModel(name=b'RegCode', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'reg_code', models.CharField(max_length=50, verbose_name=b'注册卡密')),
      (
       b'reg_name', models.CharField(max_length=180, verbose_name=b'注册卡号')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now))])]