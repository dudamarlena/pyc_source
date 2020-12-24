# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PyWhatCounts/exceptions.py
# Compiled at: 2009-05-13 06:43:54
"""A few custom exceptions to delineate the difference between a bad value being
passed to WC and an unexpected response from WC."""

class WCAuthError(EnvironmentError):
    """Used only in instances where realm or api key seem to be invalid"""
    pass


class WCUserError(EnvironmentError):
    """Used to describe an error with info going into WC (usually indicated by
        a message returned by WC starting with FAILURE:"""
    pass


class WCSystemError(EnvironmentError):
    """Used to indicate an unexpected response from WC"""
    pass