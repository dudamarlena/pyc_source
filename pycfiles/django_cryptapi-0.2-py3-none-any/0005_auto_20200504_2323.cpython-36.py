# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/migrations/0005_auto_20200504_2323.py
# Compiled at: 2020-05-04 20:02:30
# Size of source mod 2**32: 617 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cryptapi', '0004_auto_20190729_1132')]
    operations = [
     migrations.AlterField(model_name='provider',
       name='coin',
       field=models.CharField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('bch', 'Bitcoin Cash'), ('ltc', 'Litecoin'), ('iota', 'IOTA'), ('xmr', 'Monero'), ('erc20_usdt', 'ERC-20 USDT'), ('erc20_bcz', 'ERC-20 BECAZ')], max_length=16, unique=True, verbose_name='Coin'))]