# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Exceptions.py
# Compiled at: 2008-10-19 12:19:52
"""===========================
General Kamaelia Exceptions
===========================

This module defines a set of standard exceptions generally useful in Kamaelia.
They are all based on the Axon.AxonExceptions.AxonException base class.

The exceptions
--------------

* **BadRequest(request, innerexception)** - signalling that a request caused an
  exception``self.request`` is the original request and ``self.exception`` is
  the exception that it caused to be thrown
  
* **socketSendFailure()** - signalling that a socket failed trying to send

* **connectionClosedown()** - singalling that a connection closed down

* **connectionDied()** - signalling that a connection died
  * connectionDiedSending()
  * connectionDiedReceiving()
  * connectionServerShutdown()

"""
from Axon.AxonExceptions import AxonException as _AxonException

class socketSendFailure(_AxonException):
    pass


class connectionClosedown(_AxonException):
    pass


class connectionDied(connectionClosedown):
    pass


class connectionDiedSending(connectionDied):
    pass


class connectionDiedReceiving(connectionDied):
    pass


class connectionServerShutdown(connectionClosedown):
    pass


class BadRequest(_AxonException):
    """Thrown when parsing a request fails"""

    def __init__(self, request, innerexception):
        self.request = request
        self.exception = innerexception