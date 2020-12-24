# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/grnhse/exceptions.py
# Compiled at: 2018-11-10 02:30:47
"""
    Generic exceptions for the Greenhouse APIs
"""

class InvalidAPIVersion(Exception):
    pass


class InvalidAPICallError(Exception):
    pass


class HTTPError(Exception):
    pass


class EndpointNotFound(Exception):
    pass