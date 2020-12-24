# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/payjp/example.py
# Compiled at: 2018-06-22 04:34:12
# Size of source mod 2**32: 365 bytes
import payjp
payjp.api_key = 'sk_test_c62fade9d045b54cd76d7036'
print('Attempting charge...')
resp = payjp.Charge.create(amount=10,
  currency='jpy',
  card={'number':'4242424242424242', 
 'exp_month':12, 
 'exp_year':2018},
  description='a TIROL Choco')
print(resp)
print('Success: %r' % (resp,))