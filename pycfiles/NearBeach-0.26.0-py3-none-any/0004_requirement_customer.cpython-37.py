# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/migrations/0004_requirement_customer.py
# Compiled at: 2020-03-01 01:12:02
# Size of source mod 2**32: 1251 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('NearBeach', '0003_requirement_organisation')]
    operations = [
     migrations.CreateModel(name='requirement_customer',
       fields=[
      (
       'requirement_customer_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'date_created', models.DateTimeField(auto_now_add=True)),
      (
       'date_modified', models.DateTimeField(auto_now=True)),
      (
       'is_deleted', models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=5)),
      (
       'change_user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='requirement_customer_change_user', to=(settings.AUTH_USER_MODEL))),
      (
       'customer', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='NearBeach.customer'))],
       options={'db_table': 'requirement_customer'})]