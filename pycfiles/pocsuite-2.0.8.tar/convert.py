# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/convert.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import sys
from pocsuite.lib.core.settings import IS_WIN, UNICODE_ENCODING

def singleTimeWarnMessage(message):
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()


def stdoutencode(data):
    retVal = None
    try:
        data = data or ''
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, 'replace')
            if '?' in output and '?' not in data:
                warnMsg = 'cannot properly display Unicode characters '
                warnMsg += 'inside Windows OS command prompt '
                warnMsg += '(http://bugs.python.org/issue1602). All '
                warnMsg += 'unhandled occurances will result in '
                warnMsg += "replacement with '?' character. Please, find "
                warnMsg += 'proper character representation inside '
                warnMsg += 'corresponding output files. '
                singleTimeWarnMessage(warnMsg)
            retVal = output
        else:
            retVal = data.encode(sys.stdout.encoding)
    except:
        retVal = data.encode(UNICODE_ENCODING) if isinstance(data, unicode) else data

    return retVal