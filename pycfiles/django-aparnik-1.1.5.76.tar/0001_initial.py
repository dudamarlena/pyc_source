# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/zarinpals/migrations/0001_initial.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('payments', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Bank', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'status', models.IntegerField(default=-2, verbose_name=b'Status')),
      (
       b'authority_id', models.CharField(max_length=255, verbose_name=b'Authority ID')),
      (
       b'ref_id', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Bank Reference ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
      (
       b'update_at', models.DateTimeField(auto_now=True, verbose_name=b'Update At')),
      (
       b'payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'payments.Payment', verbose_name=b'Payment'))], options={b'ordering': [
                    b'created_at'], 
        b'verbose_name': b'Bank', 
        b'verbose_name_plural': b'Banks'})]