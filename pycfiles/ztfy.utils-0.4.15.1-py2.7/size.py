# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/size.py
# Compiled at: 2013-04-22 09:21:25
from zope.i18n import translate
from ztfy.utils.request import queryRequest
from ztfy.utils import _

def getHumanSize(value, request=None):
    """Convert given bytes value in human readable format"""
    if request is None:
        request = queryRequest()
    if request is not None:
        formatter = request.locale.numbers.getFormatter('decimal')
    else:
        formatter = None
    if value < 1024:
        return translate(_('%d bytes'), context=request) % value
    else:
        value = value / 1024.0
        if value < 1024:
            if formatter is None:
                return translate(_('%.1f Kb'), context=request) % value
            else:
                return translate(_('%s Kb'), context=request) % formatter.format(value, '0.0')

        value = value / 1024.0
        if value < 1024:
            if formatter is None:
                return translate(_('%.2f Mb'), context=request) % value
            else:
                return translate(_('%s Mb'), context=request) % formatter.format(value, '0.00')

        value = value / 1024.0
        if formatter is None:
            return translate(_('%.3f Gb'), context=request) % value
        return translate(_('%s Gb'), context=request) % formatter.format(value, '0.000')
        return