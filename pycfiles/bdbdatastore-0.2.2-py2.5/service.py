# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/service.py
# Compiled at: 2009-12-02 20:07:05
"""Declares the RPC service interfaces.

This module declares the abstract interfaces underlying proto2 RPC
services.  These are intented to be independent of any particular RPC
implementation, so that proto2 services can be used on top of a variety
of implementations.
"""
__author__ = 'petar@google.com (Petar Petrov)'

class Service(object):
    """Abstract base interface for protocol-buffer-based RPC services.

  Services themselves are abstract classes (implemented either by servers or as
  stubs), but they subclass this base interface. The methods of this
  interface can be used to call the methods of the service without knowing
  its exact type at compile time (analogous to the Message interface).
  """

    def GetDescriptor(self):
        """Retrieves this service's descriptor."""
        raise NotImplementedError

    def CallMethod(self, method_descriptor, rpc_controller, request, done):
        """Calls a method of the service specified by method_descriptor.

    Preconditions:
    * method_descriptor.service == GetDescriptor
    * request is of the exact same classes as returned by
      GetRequestClass(method).
    * After the call has started, the request must not be modified.
    * "rpc_controller" is of the correct type for the RPC implementation being
      used by this Service.  For stubs, the "correct type" depends on the
      RpcChannel which the stub is using.

    Postconditions:
    * "done" will be called when the method is complete.  This may be
      before CallMethod() returns or it may be at some point in the future.
    """
        raise NotImplementedError

    def GetRequestClass(self, method_descriptor):
        """Returns the class of the request message for the specified method.

    CallMethod() requires that the request is of a particular subclass of
    Message. GetRequestClass() gets the default instance of this required
    type.

    Example:
      method = service.GetDescriptor().FindMethodByName("Foo")
      request = stub.GetRequestClass(method)()
      request.ParseFromString(input)
      service.CallMethod(method, request, callback)
    """
        raise NotImplementedError

    def GetResponseClass(self, method_descriptor):
        """Returns the class of the response message for the specified method.

    This method isn't really needed, as the RpcChannel's CallMethod constructs
    the response protocol message. It's provided anyway in case it is useful
    for the caller to know the response type in advance.
    """
        raise NotImplementedError


class RpcController(object):
    """An RpcController mediates a single method call.

  The primary purpose of the controller is to provide a way to manipulate
  settings specific to the RPC implementation and to find out about RPC-level
  errors. The methods provided by the RpcController interface are intended
  to be a "least common denominator" set of features which we expect all
  implementations to support.  Specific implementations may provide more
  advanced features (e.g. deadline propagation).
  """

    def Reset(self):
        """Resets the RpcController to its initial state.

    After the RpcController has been reset, it may be reused in
    a new call. Must not be called while an RPC is in progress.
    """
        raise NotImplementedError

    def Failed(self):
        """Returns true if the call failed.

    After a call has finished, returns true if the call failed.  The possible
    reasons for failure depend on the RPC implementation.  Failed() must not
    be called before a call has finished.  If Failed() returns true, the
    contents of the response message are undefined.
    """
        raise NotImplementedError

    def ErrorText(self):
        """If Failed is true, returns a human-readable description of the error."""
        raise NotImplementedError

    def StartCancel(self):
        """Initiate cancellation.

    Advises the RPC system that the caller desires that the RPC call be
    canceled.  The RPC system may cancel it immediately, may wait awhile and
    then cancel it, or may not even cancel the call at all.  If the call is
    canceled, the "done" callback will still be called and the RpcController
    will indicate that the call failed at that time.
    """
        raise NotImplementedError

    def SetFailed(self, reason):
        """Sets a failure reason.

    Causes Failed() to return true on the client side.  "reason" will be
    incorporated into the message returned by ErrorText().  If you find
    you need to return machine-readable information about failures, you
    should incorporate it into your response protocol buffer and should
    NOT call SetFailed().
    """
        raise NotImplementedError

    def IsCanceled(self):
        """Checks if the client cancelled the RPC.

    If true, indicates that the client canceled the RPC, so the server may
    as well give up on replying to it.  The server should still call the
    final "done" callback.
    """
        raise NotImplementedError

    def NotifyOnCancel(self, callback):
        """Sets a callback to invoke on cancel.

    Asks that the given callback be called when the RPC is canceled.  The
    callback will always be called exactly once.  If the RPC completes without
    being canceled, the callback will be called after completion.  If the RPC
    has already been canceled when NotifyOnCancel() is called, the callback
    will be called immediately.

    NotifyOnCancel() must be called no more than once per request.
    """
        raise NotImplementedError


class RpcChannel(object):
    """Abstract interface for an RPC channel.

  An RpcChannel represents a communication line to a service which can be used
  to call that service's methods.  The service may be running on another
  machine. Normally, you should not use an RpcChannel directly, but instead
  construct a stub {@link Service} wrapping it.  Example:

  Example:
    RpcChannel channel = rpcImpl.Channel("remotehost.example.com:1234")
    RpcController controller = rpcImpl.Controller()
    MyService service = MyService_Stub(channel)
    service.MyMethod(controller, request, callback)
  """

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        """Calls the method identified by the descriptor.

    Call the given method of the remote service.  The signature of this
    procedure looks the same as Service.CallMethod(), but the requirements
    are less strict in one important way:  the request object doesn't have to
    be of any specific class as long as its descriptor is method.input_type.
    """
        raise NotImplementedError