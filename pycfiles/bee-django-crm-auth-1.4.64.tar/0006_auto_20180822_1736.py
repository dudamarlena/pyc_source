# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0006_auto_20180822_1736.py
# Compiled at: 2018-08-22 05:36:02
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_crm', '0005_auto_20180708_1503')]
    operations = [
     migrations.CreateModel(name=b'PreUserFee', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'price', models.FloatField(verbose_name=b'实收金额')),
      (
       b'paid_at', models.DateTimeField(verbose_name=b'缴费日期')),
      (
       b'study_at', models.DateTimeField(blank=True, null=True, verbose_name=b'开课日期')),
      (
       b'pay_status', models.IntegerField(choices=[(1, '全款'), (2, '分期头款'), (3, '分期中'), (4, '分期尾款')], default=1, verbose_name=b'缴费类型')),
      (
       b'is_checked', models.BooleanField(default=False, verbose_name=b'审核')),
      (
       b'checked_at', models.DateTimeField(null=True)),
      (
       b'after_checked_at', models.DateTimeField(null=True)),
      (
       b'info', models.TextField(blank=True, null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'checked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
      (
       b'preuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.PreUser'))], options={b'ordering': [
                    b'-paid_at', b'-created_at'], 
        b'db_table': b'bee_django_crm_preuser_fee', 
        b'permissions': (('view_crm_preuser_fee', '可以查看用户缴费'), )}),
     migrations.AlterModelOptions(name=b'preusercontract', options={b'ordering': [b'-created_at'], b'permissions': (('view_crm_preuser_contract', '可以查看用户合同'), )}),
     migrations.AddField(model_name=b'contract', name=b'agreement', field=models.TextField(null=True, verbose_name=b'须知')),
     migrations.AddField(model_name=b'preusercontract', name=b'is_migrate', field=models.BooleanField(default=False)),
     migrations.AddField(model_name=b'preusercontract', name=b'is_user_agree', field=models.BooleanField(default=False, verbose_name=b'用户是否同意')),
     migrations.AlterField(model_name=b'preusercontract', name=b'paid_at', field=models.DateTimeField(null=True, verbose_name=b'缴费日期')),
     migrations.AlterField(model_name=b'preusercontract', name=b'price', field=models.FloatField(verbose_name=b'应收金额')),
     migrations.AddField(model_name=b'preuserfee', name=b'preuser_contract', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.PreUserContract'))]