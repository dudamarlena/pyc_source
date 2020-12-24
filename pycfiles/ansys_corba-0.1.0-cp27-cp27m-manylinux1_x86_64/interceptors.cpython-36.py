# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./interceptors.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 2486 bytes
"""omniORB.interceptors

Interceptor registration functions:

  addClientSendRequest
  addClientReceiveReply
  addServerReceiveRequest
  addServerSendReply
  addServerSendException

To register an interceptor function, call the relevant registration
function with a callable argument. The callable will be called with
two or three arguments. The first argument is the name of the
operation being invoked; the second is the set of service contexts to
be retrieved or filled in. ServerSendException has a third argument,
the repository id of the exception being thrown.

When receiving service contexts (ClientReceiveReply,
ServerReceiveRequest), the second argument is a tuple of 2-tuples. In
each 2-tuple, the first item is the service context id and the second
item is the CDR encapsulation of the service context. The
encapsulation can be decoded with omniORB.cdrUnmarshal() (but only if
you know the type to decode it to).

When sending service contexts (ClientSendRequest, ServerSendReply,
ServerSendException), the second argument is an empty list. The
interceptor function can choose to add one or more service context
tuples, with the same form described above, by appending to the list.
Encapsulations are created with omniORB.cdrMarshal().

Interceptor registration functions may only be called before the ORB
is initialised. Attempting to call them later results in a
BAD_INV_ORDER exception.
"""
from _omnipy.interceptor_func import *