# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mikhail/.virtualenvs/django-robokassa/lib/python3.5/site-packages/robokassa/migrations/0001_initial.py
# Compiled at: 2018-04-26 08:33:44
# Size of source mod 2**32: 1507 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='SuccessNotification', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'InvId', models.IntegerField(db_index=True, verbose_name='Номер заказа')),
      (
       'OutSum', models.CharField(max_length=15, verbose_name='Сумма')),
      (
       'created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время получения уведомления'))], options={'verbose_name': 'Уведомление об успешном платеже', 
      'verbose_name_plural': 'Уведомления об успешных платежах (ROBOKASSA)'})]