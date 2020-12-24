# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0006_cosalepayment.py
# Compiled at: 2019-03-15 07:32:52
from __future__ import unicode_literals
import aparnik.utils.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bankaccounts', '0002_auto_20190215_1916'),
     ('basemodels', '0010_basemodel_visit_count'),
     ('cosales', '0005_auto_20190315_1347')]
    operations = [
     migrations.CreateModel(name=b'CoSalePayment', fields=[
      (
       b'basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'basemodels.BaseModel')),
      (
       b'price', aparnik.utils.fields.PriceField(decimal_places=0, max_digits=20, verbose_name=b'Price')),
      (
       b'tracking_number', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Tracking Number')),
      (
       b'status', models.CharField(choices=[('CL', 'Cleared'), ('RSHBR', 'The request for settlement has been received'), ('C', 'Cancel')], default=b'RSHBR', max_length=10, verbose_name=b'Status')),
      (
       b'user_bank_account_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bankaccounts.BankAccount', verbose_name=b'User Bank Account'))], options={b'verbose_name': b'Co Sale Payment', 
        b'manager_inheritance_from_future': True, 
        b'verbose_name_plural': b'Co Sale Payments'}, bases=('basemodels.basemodel', ))]