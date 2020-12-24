# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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