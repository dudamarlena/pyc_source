# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/louieck/signal.py
# Compiled at: 2018-05-31 10:36:55
"""Signal class.

This class is provided as a way to consistently define and document
signal types.  Signal classes also have a useful string
representation.

Louie does not require you to use a subclass of Signal for signals.
"""

class _SIGNAL(type):
    """Base metaclass for signal classes."""

    def __str__(cls):
        return ('<Signal: {0}>').format(cls.__name__)


class Signal(object):
    __metaclass__ = _SIGNAL


class All(Signal):
    """Used to represent 'all signals'.

    The All class can be used with connect, disconnect, send, or
    sendExact to denote that the signal should react to all signals,
    not just a particular signal.
    """
    pass