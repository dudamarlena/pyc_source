# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/amqp/exceptions.py
# Compiled at: 2015-02-17 11:50:32


class MessageNotDelivered(IOError):
    """
    Exception to be raised when an AMQP message could not be queued.
    """


class MessageDeliveryTimeout(IOError):
    """
    Exception to be raised when an AMQP message could not be delivered in the specified period.
    """