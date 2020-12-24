# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0001_initial.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Activity', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'活动名称')),
      (
       b'source_name', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'渠道名称')),
      (
       b'start_date', models.DateTimeField(blank=True, null=True, verbose_name=b'开始时间')),
      (
       b'end_date', models.DateTimeField(blank=True, null=True, verbose_name=b'结束时间')),
      (
       b'detail', models.TextField(blank=True, null=True, verbose_name=b'活动说明')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'分享说明')),
      (
       b'explain', models.TextField(blank=True, null=True, verbose_name=b'规则解释')),
      (
       b'qrcode_width', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'二维码宽度')),
      (
       b'qrcode_height', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'二维码高度')),
      (
       b'qrcode_pos_x', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'二维码x轴坐标')),
      (
       b'qrcode_pos_y', models.IntegerField(blank=True, default=0, null=True, verbose_name=b'二维码y轴坐标')),
      (
       b'qrcode_color', models.CharField(default=b'#000000', max_length=8, null=True, verbose_name=b'二维码颜色')),
      (
       b'qrcode_bg', models.ImageField(blank=True, null=True, upload_to=b'bee_django_referral/qrcode/bg', verbose_name=b'二维码')),
      (
       b'qrcode_thumb', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'二维码预览图')),
      (
       b'qrcode_url', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'二维码地址'))], options={b'db_table': b'bee_django_referral_activity'}),
     migrations.CreateModel(name=b'UserShareImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'qrcode', models.ImageField(upload_to=b'bee_django_referral/user_qrcode/', verbose_name=b'二维码')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'生成时间')),
      (
       b'status', models.IntegerField(default=0, verbose_name=b'状态')),
      (
       b'activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_referral.Activity')),
      (
       b'user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={b'db_table': b'bee_django_referral_image'})]