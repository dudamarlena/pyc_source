# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/constant.py
# Compiled at: 2016-06-25 09:00:55
# Size of source mod 2**32: 436 bytes
import enum

class PriceType(enum.Enum):
    open = 'open'
    low = 'low'
    high = 'high'
    close = 'close'


DEFAULT_ROLLING_MEAN_RATIO = 5
DATE_FORMATS = [
 '%Y/%m/%d', '%Y-%m-%d']
MAP_PRICE_COLUMNS = {}
for v in ['open', 'close', 'high', 'low']:
    p = 'price'
    keys = [v, v.title(), '%s %s' % (v, p), '%s %s' % (v.title(), p.title()), '%s%s' % (v.title(), p.title())]
    for k in keys:
        MAP_PRICE_COLUMNS[k] = v