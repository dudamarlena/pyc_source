# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/migrations/0004_auto_20190729_1132.py
# Compiled at: 2020-05-04 20:02:30
# Size of source mod 2**32: 1053 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cryptapi', '0003_auto_20181112_1939')]
    operations = [
     migrations.AddField(model_name='payment',
       name='pending',
       field=models.BooleanField(default=True)),
     migrations.AlterField(model_name='provider',
       name='coin',
       field=models.CharField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('bch', 'Bitcoin Cash'), ('ltc', 'Litecoin'), ('iota', 'IOTA'), ('xmr', 'Monero')], max_length=8, unique=True, verbose_name='Coin')),
     migrations.AlterField(model_name='request',
       name='status',
       field=models.CharField(choices=[('created', 'Created'), ('pending', 'Pending'), ('insufficient', 'Payment Insufficient'), ('received', 'Received'), ('done', 'Done')], default='', max_length=16, null=True, verbose_name='Status'))]