# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/misc/_formatstr.py
# Compiled at: 2013-12-08 21:45:16


def indent(s, tag):
    lines = s.splitlines()
    lines = [ '%s%s' % (tag, l) for l in lines ]
    return ('\n').join(lines)