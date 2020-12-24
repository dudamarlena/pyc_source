# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/exceptions.py
# Compiled at: 2016-11-22 15:08:24
from __future__ import print_function
import logging, sys
__author__ = 'alforbes'

class OrloError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        return

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidUsage(OrloError):
    status_code = 400


class DatabaseError(OrloError):
    status_code = 500


class OrloWorkflowError(OrloError):
    status_code = 400


class OrloAuthError(OrloError):
    status_code = 401


class OrloStartupError(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        print('Startup Error: ' + message)


class OrloConfigError(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        print('Configuration Error: ' + message)


class OrloDeployError(OrloError):
    status_code = 500