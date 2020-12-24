# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/usr0/projects/the-giant/thegiant/helpers.py
# Compiled at: 2013-02-18 18:16:14
OK = '+OK\r\n'

def reply(v):
    """
        formats the value as a redis reply
        """
    return '$%s\r\n%s\r\n' % (len(v), v)