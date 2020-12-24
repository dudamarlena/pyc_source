# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/erp.juanmitaboada.com/codenerix_payments/migrations/0002_auto_20180526_1515.py
# Compiled at: 2018-05-26 09:15:05
# Size of source mod 2**32: 423 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_payments', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='currency', name='symbol', field=models.CharField(max_length=5, unique=True, verbose_name='Symbol'))]