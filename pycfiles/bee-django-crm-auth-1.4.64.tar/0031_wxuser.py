# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0031_wxuser.py
# Compiled at: 2019-11-27 04:15:23
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0030_auto_20191122_1324')]
    operations = [
     migrations.CreateModel(name=b'WXUser', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'nickname', models.CharField(max_length=180, verbose_name=b'微信昵称')),
      (
       b'open_id', models.CharField(max_length=180, verbose_name=b'微信openid')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'db_table': b'bee_django_crm_wx_user'})]