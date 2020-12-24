# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nathan/code/plone4.3/zinstance/src/wildcard.readonly/wildcard/readonly/mail.py
# Compiled at: 2014-02-27 00:18:14


def send(self, *args, **kwargs):
    if 'immediate' not in kwargs:
        kwargs['immediate'] = True
    return self._old_send(*args, **kwargs)