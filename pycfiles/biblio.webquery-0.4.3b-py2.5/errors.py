# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/errors.py
# Compiled at: 2009-05-04 13:01:45
"""
Various errors thrown by the the module.

"""
__docformat__ = 'restructuredtext en'
import exceptions
__all__ = [
 'ParseError',
 'QueryThrottleError',
 'QueryError']

class QueryError(exceptions.ValueError):
    """
        Raised when there is an problem with a queries reply.
        """

    def __init__(self, msg):
        """
                C'tor.
                """
        exceptions.ValueError.__init__(self, msg)


class ParseError(exceptions.ValueError):
    """
        Thrown when parsing webservice formats.
        """

    def __init__(self, msg):
        """
                C'tor.
                """
        exceptions.ValueError.__init__(self, msg)


class QueryThrottleError(exceptions.RuntimeError):
    """
        An exception to throw when a query limit has been exceeded.
        
        It serves little purpose except to distinguish failures caused by exceeding
        query limits.
        
        """

    def __init__(self, msg=None):
        msg = msg or 'query limit exceeded'
        RuntimeError.__init__(self, msg)


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()