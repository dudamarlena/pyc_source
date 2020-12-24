# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0004_auto_20180620_1845.py
# Compiled at: 2018-06-20 07:06:22
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0003_usercoincount')]
    operations = [
     migrations.AlterModelOptions(name=b'cointype', options={b'ordering': [b'id'], b'permissions': (('can_manage_coin', '可以进入M币管理页'), )}),
     migrations.AlterField(model_name=b'cointype', name=b'identity', field=models.CharField(help_text=b'此字段唯一', max_length=180, null=True, unique=True, verbose_name=b'标识符')),
     migrations.AlterField(model_name=b'usercoinrecord', name=b'coin', field=models.IntegerField(help_text=b'扣除填入负数', verbose_name=b'数量')),
     migrations.AlterField(model_name=b'usercoinrecord', name=b'coin_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_coin.CoinType', verbose_name=b'类型'))]