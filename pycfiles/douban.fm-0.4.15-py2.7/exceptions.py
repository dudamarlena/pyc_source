# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/exceptions.py
# Compiled at: 2016-06-22 17:23:26
import os, sys
from termcolor import colored

class GenericError(Exception):
    message = 'an error occurred'

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if not message:
            message = self.message % kwargs
        super(GenericError, self).__init__(colored(message, 'red'))


class APIError(GenericError):
    pass


class ConfigError(GenericError):
    pass


class MplayerError(GenericError):
    message = 'Mplayer error, check if install mplayer'


class Success(object):

    def __init__(self, s):
        print >> sys.stderr, 'OK:\n', s


class Warn(object):

    def __init__(self, s):
        print >> sys.stderr, 'WARN:\n', s


class Error(object):

    def __init__(self, s):
        print >> sys.stderr, 'ERROR:\n', s


class Fatal(object):

    def __init__(self, s, code=111):
        print >> sys.stderr, 'FATAL:\n', s
        sys.exit(code)