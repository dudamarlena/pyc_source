# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/toonlib/toonlibexceptions.py
# Compiled at: 2018-11-03 13:01:06
"""
Main module Exceptions file

Put your exception classes here
"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'plaintext'
__date__ = '13-03-2017'

class InvalidCredentials(Exception):
    """The username and password combination was not accepted as valid"""
    pass


class UnableToGetSession(Exception):
    """Could not refresh session"""
    pass


class IncompleteResponse(Exception):
    """Vital information is missing from the response"""
    pass


class InvalidThermostatState(Exception):
    """Vital information is missing from the response"""
    pass