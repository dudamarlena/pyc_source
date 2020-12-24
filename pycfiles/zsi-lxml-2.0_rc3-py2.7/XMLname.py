# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/wstools/XMLname.py
# Compiled at: 2006-10-25 20:34:29
"""Translate strings to and from SOAP 1.2 XML name encoding

Implements rules for mapping application defined name to XML names
specified by the w3 SOAP working group for SOAP version 1.2 in
Appendix A of "SOAP Version 1.2 Part 2: Adjuncts", W3C Working Draft
17, December 2001, <http://www.w3.org/TR/soap12-part2/#namemap>

Also see <http://www.w3.org/2000/xp/Group/xmlp-issues>.

Author: Gregory R. Warnes <Gregory.R.Warnes@Pfizer.com>
Date::  2002-04-25
Version 0.9.0

"""
ident = '$Id: XMLname.py 954 2005-02-16 14:45:37Z warnes $'
from re import *

def _NCNameChar(x):
    return x.isalpha() or x.isdigit() or x == '.' or x == '-' or x == '_'


def _NCNameStartChar(x):
    return x.isalpha() or x == '_'


def _toUnicodeHex(x):
    hexval = hex(ord(x[0]))[2:]
    hexlen = len(hexval)
    if hexlen == 1:
        hexval = '000' + hexval
    elif hexlen == 2:
        hexval = '00' + hexval
    elif hexlen == 3:
        hexval = '0' + hexval
    elif hexlen == 4:
        hexval = '' + hexval
    elif hexlen == 5:
        hexval = '000' + hexval
    elif hexlen == 6:
        hexval = '00' + hexval
    elif hexlen == 7:
        hexval = '0' + hexval
    elif hexlen == 8:
        hexval = '' + hexval
    else:
        raise Exception, 'Illegal Value returned from hex(ord(x))'
    return '_x' + hexval + '_'


def _fromUnicodeHex(x):
    return eval('u"\\u' + x[2:-1] + '"')


def toXMLname(string):
    """Convert string to a XML name."""
    if string.find(':') != -1:
        prefix, localname = string.split(':', 1)
    else:
        prefix = None
        localname = string
    T = unicode(localname)
    N = len(localname)
    X = []
    for i in range(N):
        if i < N - 1 and T[i] == '_' and T[(i + 1)] == 'x':
            X.append('_x005F_')
        elif i == 0 and N >= 3 and (T[0] == 'x' or T[0] == 'X') and (T[1] == 'm' or T[1] == 'M') and (T[2] == 'l' or T[2] == 'L'):
            X.append('_xFFFF_' + T[0])
        elif not _NCNameChar(T[i]) or i == 0 and not _NCNameStartChar(T[i]):
            X.append(_toUnicodeHex(T[i]))
        else:
            X.append(T[i])

    if prefix:
        return '%s:%s' % (prefix, ('').join(X))
    else:
        return ('').join(X)


def fromXMLname(string):
    """Convert XML name to unicode string."""
    retval = sub('_xFFFF_', '', string)

    def fun(matchobj):
        return _fromUnicodeHex(matchobj.group(0))

    retval = sub('_x[0-9A-Za-z]+_', fun, retval)
    return retval