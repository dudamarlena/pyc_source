# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/vouchers/migrations/0001_initial.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1743 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('basemodels', '0004_auto_20181103_2233'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('orders', '0002_auto_20181026_1301')]
    operations = [
     migrations.CreateModel(name='Voucher',
       fields=[
      (
       'basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='basemodels.BaseModel')),
      (
       'quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
      (
       'expire_at', models.DateTimeField(blank=True, null=True, verbose_name='Expire at')),
      (
       'is_active', models.BooleanField(default=True, verbose_name='Is Active')),
      (
       'is_spent', models.BooleanField(default=False, verbose_name='Is spent')),
      (
       'order_item_obj', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), related_name='voucher_order_item', to='orders.OrderItem', verbose_name='OrderItem')),
      (
       'user_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='voucher_user', to=(settings.AUTH_USER_MODEL), verbose_name='User'))],
       options={'verbose_name':'Voucher', 
      'manager_inheritance_from_future':True, 
      'verbose_name_plural':'Vouchers'},
       bases=('basemodels.basemodel', ))]