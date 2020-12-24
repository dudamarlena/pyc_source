# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0001_initial.py
# Compiled at: 2018-04-10 06:23:19
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'CoinType', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'名称类型')),
      (
       b'coin', models.IntegerField(verbose_name=b'数量')),
      (
       b'info', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'说明'))], options={b'ordering': [
                    b'id'], 
        b'db_table': b'bee_django_coin_type'}),
     migrations.CreateModel(name=b'UserCoinRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'coin', models.IntegerField(verbose_name=b'数量')),
      (
       b'reason', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'原因')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'coin_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_coin.CoinType')),
      (
       b'created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'created_by_user', to=settings.AUTH_USER_MODEL)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'coin_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_coin_record'})]