# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/taskqueue/errors.py
# Compiled at: 2007-07-24 13:08:31
"""
Custom Exceptions
"""
from zope.interface import Invalid

class QueueRunError(Exception):
    """
    An attempt was made to dispatch tasks when the dispatcher isn't running.
    """
    __module__ = __name__


class ImplementationError(Exception):
    """
    There was a problem implementing the required interface.
    """
    __module__ = __name__


class InvariantError(Invalid):
    """
    An invariant of the IWorker provider did not meet requirements.
    """
    __module__ = __name__

    def __repr__(self):
        return 'InvariantError(%r)' % self.args