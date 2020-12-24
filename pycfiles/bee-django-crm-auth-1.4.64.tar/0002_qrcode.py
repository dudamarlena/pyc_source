# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0002_qrcode.py
# Compiled at: 2018-05-02 03:54:30
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'QrCode', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'qrcode_width', models.IntegerField(default=0, null=True, verbose_name=b'二维码宽度')),
      (
       b'qrcode_height', models.IntegerField(default=0, null=True, verbose_name=b'二维码高度')),
      (
       b'qrcode_pos_x', models.IntegerField(default=0, null=True, verbose_name=b'二维码x轴坐标')),
      (
       b'qrcode_pos_y', models.IntegerField(default=0, null=True, verbose_name=b'二维码y轴坐标')),
      (
       b'qrcode_color', models.CharField(default=b'#000000', max_length=8, null=True, verbose_name=b'二维码颜色')),
      (
       b'photo', models.ImageField(null=True, upload_to=b'bee_django_referral/qrcode/', verbose_name=b'二维码'))], options={b'db_table': b'bee_django_crm_poster'})]