# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twod/wsgi/exc.py
# Compiled at: 2011-06-28 10:17:42
"""
Exceptions raised by :mod:`twod.wsgi.`

"""

class TwodWSGIException(Exception):
    """Base class for exceptions raised by :mod:`twod.wsgi`."""
    pass


class ApplicationCallError(TwodWSGIException):
    """
    Exception raised when an embedded WSGI application was not called properly.
    
    """
    pass