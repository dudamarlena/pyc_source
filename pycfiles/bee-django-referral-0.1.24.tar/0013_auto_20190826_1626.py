# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0013_auto_20190826_1626.py
# Compiled at: 2019-08-26 04:26:06
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0012_auto_20190821_1315')]
    operations = [
     migrations.AlterModelOptions(name=b'useractivity', options={b'permissions': (('view_user_activity', '可以查看学生转介活动'), )}),
     migrations.AlterField(model_name=b'usershareimage', name=b'qrcode', field=models.ImageField(null=True, upload_to=b'bee_django_referral/user_qrcode/', verbose_name=b'二维码')),
     migrations.AlterField(model_name=b'usershareimage', name=b'status', field=models.IntegerField(choices=[(1, '未使用'), (2, '已注册'), (4, '已缴费')], default=0, verbose_name=b'状态'))]