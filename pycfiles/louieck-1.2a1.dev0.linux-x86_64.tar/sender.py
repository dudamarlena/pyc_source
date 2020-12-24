# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/louieck/sender.py
# Compiled at: 2018-05-31 10:36:55
"""Sender classes."""

class _SENDER(type):
    """Base metaclass for sender classes."""

    def __str__(cls):
        return ('<Sender: {0}>').format(cls.__name__)


class Any(object):
    """Used to represent either 'any sender'.

    The Any class can be used with connect, disconnect, send, or
    sendExact to denote that the sender paramater should react to any
    sender, not just a particular sender.
    """
    __metaclass__ = _SENDER


class Anonymous(object):
    """Singleton used to signal 'anonymous sender'.

    The Anonymous class is used to signal that the sender of a message
    is not specified (as distinct from being 'any sender').
    Registering callbacks for Anonymous will only receive messages
    sent without senders.  Sending with anonymous will only send
    messages to those receivers registered for Any or Anonymous.

    Note: The default sender for connect is Any, while the default
    sender for send is Anonymous.  This has the effect that if you do
    not specify any senders in either function then all messages are
    routed as though there was a single sender (Anonymous) being used
    everywhere.
    """
    __metaclass__ = _SENDER