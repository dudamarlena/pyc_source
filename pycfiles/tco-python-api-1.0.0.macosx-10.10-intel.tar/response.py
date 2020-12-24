# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/twocheckout/response.py
# Compiled at: 2015-10-07 15:00:49


class Response(object):

    def __init__(self, *args):
        for key, value in args[0].iteritems():
            setattr(self, key, value)