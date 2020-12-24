# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/choices.py
# Compiled at: 2020-05-06 18:55:43
# Size of source mod 2**32: 902 bytes
from django.utils.translation import gettext_lazy as _
TOKENS = [
 ('erc20_usdt', 'ERC-20 USDT', '0xdAC17F958D2ee523a2206206994597C13D831ec7', 6, 4),
 ('erc20_bcz', 'ERC-20 BECAZ', '0x08399ab5eBBE96870B289754A7bD21E7EC8c6FCb', 18, 0)]
TOKEN_DICT = {t[0]:t for t in TOKENS}
COINS = [
 ('btc', 'Bitcoin'),
 ('eth', 'Ethereum'),
 ('bch', 'Bitcoin Cash'),
 ('ltc', 'Litecoin'),
 ('iota', 'IOTA'),
 ('xmr', 'Monero')] + [(t[0], t[1]) for t in TOKENS]
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
COIN_MULTIPLIERS = {**{'btc':100000000, 
 'bch':100000000, 
 'ltc':100000000, 
 'eth':1000000000000000000, 
 'iota':1000000, 
 'xmr':1000000000000}, **{t[0]:10 ** t[3] for t in TOKENS}}