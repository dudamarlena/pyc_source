# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/exceptions.py
# Compiled at: 2011-01-27 11:10:56


class OoyalaParameterException(Exception):

    def __init__(self, param_name):
        self.parameter = param_name

    def __str__(self):
        return 'Parameter %s is required but is None' % repr(self.parameter)