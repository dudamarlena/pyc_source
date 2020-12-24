# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Converters.py
# Compiled at: 2015-07-18 19:38:10
from ZCurrency import ZCurrency
from cgi import escape

def field2currency(v):
    try:
        v = ZCurrency(v)
    except Exception as e:
        raise ValueError, 'Cannot convert <strong>%s (%s)</strong> to ZCurrency: %s' % (type(v), v, escape(str(e)))

    return v