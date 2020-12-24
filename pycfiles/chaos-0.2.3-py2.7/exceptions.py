# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/amqp/exceptions.py
# Compiled at: 2015-02-17 11:50:32


class MessageNotDelivered(IOError):
    """
    Exception to be raised when an AMQP message could not be queued.
    """
    pass


class MessageDeliveryTimeout(IOError):
    """
    Exception to be raised when an AMQP message could not be delivered in the specified period.
    """
    pass