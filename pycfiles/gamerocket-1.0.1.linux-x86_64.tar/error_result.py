# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/result/error_result.py
# Compiled at: 2013-08-06 10:45:36


class ErrorResult(object):

    def __init__(self, attributes):
        self.error = attributes['error']
        self.error_description = attributes['error_description']

    def __repr__(self):
        return "<%s: '%s'>" % (self.error, self.error_description)

    @property
    def is_success(self):
        return False