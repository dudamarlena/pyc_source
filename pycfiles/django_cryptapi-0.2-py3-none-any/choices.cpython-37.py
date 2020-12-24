# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/choices.py
# Compiled at: 2020-05-04 13:07:58
# Size of source mod 2**32: 689 bytes
import django.utils.translation as _
COINS = (('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('bch', 'Bitcoin Cash'), ('ltc', 'Litecoin'),
         ('iota', 'IOTA'), ('xmr', 'Monero'), ('erc20_usdt', 'ERC-20 USDT'), ('erc20_bcz', 'ERC-20 BECAZ'))
STATUS = (
 (
  'created', _('Created')),
 (
  'pending', _('Pending')),
 (
  'insufficient', _('Payment Insufficient')),
 (
  'received', _('Received')),
 (
  'done', _('Done')))
COIN_MULTIPLIERS = {'btc':100000000, 
 'bch':100000000, 
 'ltc':100000000, 
 'eth':1000000000000000000, 
 'iota':1000000, 
 'xmr':1000000000000}