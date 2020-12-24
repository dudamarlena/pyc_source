# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0003_auto_20190128_1056.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 909 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cosales', '0002_cosale_status')]
    operations = [
     migrations.AlterField(model_name='cosale',
       name='status',
       field=models.CharField(choices=[('C', 'Cleared'), ('NC', 'Not Cleared'), ('RSHBR', 'The request for settlement has been received'), ('OC', 'Order Cancel')], default='NC', max_length=10, verbose_name='Status')),
     migrations.AlterField(model_name='cosalehistory',
       name='status',
       field=models.CharField(choices=[('C', 'Cleared'), ('NC', 'Not Cleared'), ('RSHBR', 'The request for settlement has been received'), ('OC', 'Order Cancel')], default='NC', max_length=10, verbose_name='Status'))]