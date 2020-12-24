# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/interfaces/face/face.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 39704 bytes
"""Interfaces defining the Face layer of RPC Framework."""
import abc, collections, enum, six
from grpc.framework.common import cardinality
from grpc.framework.common import style
from grpc.framework.foundation import abandonment
from grpc.framework.foundation import future
from grpc.framework.foundation import stream

class NoSuchMethodError(Exception):
    __doc__ = 'Raised by customer code to indicate an unrecognized method.\n\n  Attributes:\n    group: The group of the unrecognized method.\n    name: The name of the unrecognized method.\n  '

    def __init__(self, group, method):
        super(NoSuchMethodError, self).__init__()
        self.group = group
        self.method = method

    def __repr__(self):
        return 'face.NoSuchMethodError(%s, %s)' % (
         self.group,
         self.method)


class Abortion(collections.namedtuple('Abortion', ('kind', 'initial_metadata', 'terminal_metadata',
                                    'code', 'details'))):
    __doc__ = 'A value describing RPC abortion.\n\n  Attributes:\n    kind: A Kind value identifying how the RPC failed.\n    initial_metadata: The initial metadata from the other side of the RPC or\n      None if no initial metadata value was received.\n    terminal_metadata: The terminal metadata from the other side of the RPC or\n      None if no terminal metadata value was received.\n    code: The code value from the other side of the RPC or None if no code value\n      was received.\n    details: The details value from the other side of the RPC or None if no\n      details value was received.\n  '

    @enum.unique
    class Kind(enum.Enum):
        __doc__ = 'Types of RPC abortion.'
        CANCELLED = 'cancelled'
        EXPIRED = 'expired'
        LOCAL_SHUTDOWN = 'local shutdown'
        REMOTE_SHUTDOWN = 'remote shutdown'
        NETWORK_FAILURE = 'network failure'
        LOCAL_FAILURE = 'local failure'
        REMOTE_FAILURE = 'remote failure'


class AbortionError(six.with_metaclass(abc.ABCMeta, Exception)):
    __doc__ = 'Common super type for exceptions indicating RPC abortion.\n\n    initial_metadata: The initial metadata from the other side of the RPC or\n      None if no initial metadata value was received.\n    terminal_metadata: The terminal metadata from the other side of the RPC or\n      None if no terminal metadata value was received.\n    code: The code value from the other side of the RPC or None if no code value\n      was received.\n    details: The details value from the other side of the RPC or None if no\n      details value was received.\n  '

    def __init__(self, initial_metadata, terminal_metadata, code, details):
        super(AbortionError, self).__init__()
        self.initial_metadata = initial_metadata
        self.terminal_metadata = terminal_metadata
        self.code = code
        self.details = details

    def __str__(self):
        return '%s(code=%s, details="%s")' % (self.__class__.__name__,
         self.code, self.details)


class CancellationError(AbortionError):
    __doc__ = 'Indicates that an RPC has been cancelled.'


class ExpirationError(AbortionError):
    __doc__ = 'Indicates that an RPC has expired ("timed out").'


class LocalShutdownError(AbortionError):
    __doc__ = 'Indicates that an RPC has terminated due to local shutdown of RPCs.'


class RemoteShutdownError(AbortionError):
    __doc__ = 'Indicates that an RPC has terminated due to remote shutdown of RPCs.'


class NetworkError(AbortionError):
    __doc__ = 'Indicates that some error occurred on the network.'


class LocalError(AbortionError):
    __doc__ = 'Indicates that an RPC has terminated due to a local defect.'


class RemoteError(AbortionError):
    __doc__ = 'Indicates that an RPC has terminated due to a remote defect.'


class RpcContext(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Provides RPC-related information and action.'

    @abc.abstractmethod
    def is_active(self):
        """Describes whether the RPC is active or has terminated."""
        raise NotImplementedError()

    @abc.abstractmethod
    def time_remaining(self):
        """Describes the length of allowed time remaining for the RPC.

    Returns:
      A nonnegative float indicating the length of allowed time in seconds
      remaining for the RPC to complete before it is considered to have timed
      out.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def add_abortion_callback(self, abortion_callback):
        """Registers a callback to be called if the RPC is aborted.

    Args:
      abortion_callback: A callable to be called and passed an Abortion value
        in the event of RPC abortion.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        """Cancels the RPC.

    Idempotent and has no effect if the RPC has already terminated.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def protocol_context(self):
        """Accesses a custom object specified by an implementation provider.

    Returns:
      A value specified by the provider of a Face interface implementation
        affording custom state and behavior.
    """
        raise NotImplementedError()


class Call(six.with_metaclass(abc.ABCMeta, RpcContext)):
    __doc__ = 'Invocation-side utility object for an RPC.'

    @abc.abstractmethod
    def initial_metadata(self):
        """Accesses the initial metadata from the service-side of the RPC.

    This method blocks until the value is available or is known not to have been
    emitted from the service-side of the RPC.

    Returns:
      The initial metadata object emitted by the service-side of the RPC, or
        None if there was no such value.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def terminal_metadata(self):
        """Accesses the terminal metadata from the service-side of the RPC.

    This method blocks until the value is available or is known not to have been
    emitted from the service-side of the RPC.

    Returns:
      The terminal metadata object emitted by the service-side of the RPC, or
        None if there was no such value.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def code(self):
        """Accesses the code emitted by the service-side of the RPC.

    This method blocks until the value is available or is known not to have been
    emitted from the service-side of the RPC.

    Returns:
      The code object emitted by the service-side of the RPC, or None if there
        was no such value.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def details(self):
        """Accesses the details value emitted by the service-side of the RPC.

    This method blocks until the value is available or is known not to have been
    emitted from the service-side of the RPC.

    Returns:
      The details value emitted by the service-side of the RPC, or None if there
        was no such value.
    """
        raise NotImplementedError()


class ServicerContext(six.with_metaclass(abc.ABCMeta, RpcContext)):
    __doc__ = 'A context object passed to method implementations.'

    @abc.abstractmethod
    def invocation_metadata(self):
        """Accesses the metadata from the invocation-side of the RPC.

    This method blocks until the value is available or is known not to have been
    emitted from the invocation-side of the RPC.

    Returns:
      The metadata object emitted by the invocation-side of the RPC, or None if
        there was no such value.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def initial_metadata(self, initial_metadata):
        """Accepts the service-side initial metadata value of the RPC.

    This method need not be called by method implementations if they have no
    service-side initial metadata to transmit.

    Args:
      initial_metadata: The service-side initial metadata value of the RPC to
        be transmitted to the invocation side of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def terminal_metadata(self, terminal_metadata):
        """Accepts the service-side terminal metadata value of the RPC.

    This method need not be called by method implementations if they have no
    service-side terminal metadata to transmit.

    Args:
      terminal_metadata: The service-side terminal metadata value of the RPC to
        be transmitted to the invocation side of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def code(self, code):
        """Accepts the service-side code of the RPC.

    This method need not be called by method implementations if they have no
    code to transmit.

    Args:
      code: The code of the RPC to be transmitted to the invocation side of the
        RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def details(self, details):
        """Accepts the service-side details of the RPC.

    This method need not be called by method implementations if they have no
    service-side details to transmit.

    Args:
      details: The service-side details value of the RPC to be transmitted to
        the invocation side of the RPC.
    """
        raise NotImplementedError()


class ResponseReceiver(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Invocation-side object used to accept the output of an RPC.'

    @abc.abstractmethod
    def initial_metadata(self, initial_metadata):
        """Receives the initial metadata from the service-side of the RPC.

    Args:
      initial_metadata: The initial metadata object emitted from the
        service-side of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def response(self, response):
        """Receives a response from the service-side of the RPC.

    Args:
      response: A response object emitted from the service-side of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def complete(self, terminal_metadata, code, details):
        """Receives the completion values emitted from the service-side of the RPC.

    Args:
      terminal_metadata: The terminal metadata object emitted from the
        service-side of the RPC.
      code: The code object emitted from the service-side of the RPC.
      details: The details object emitted from the service-side of the RPC.
    """
        raise NotImplementedError()


class UnaryUnaryMultiCallable(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords invoking a unary-unary RPC in any call style.'

    @abc.abstractmethod
    def __call__(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
        """Synchronously invokes the underlying RPC.

    Args:
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      with_call: Whether or not to include return a Call for the RPC in addition
        to the response.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      The response value for the RPC, and a Call for the RPC if with_call was
        set to True at invocation.

    Raises:
      AbortionError: Indicating that the RPC was aborted.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def future(self, request, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and a future.Future. In the
        event of RPC completion, the return Future's result value will be the
        response value of the RPC. In the event of RPC abortion, the returned
        Future's exception value will be an AbortionError.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event(self, request, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      request: The request value for the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A Call for the RPC.
    """
        raise NotImplementedError()


class UnaryStreamMultiCallable(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords invoking a unary-stream RPC in any call style.'

    @abc.abstractmethod
    def __call__(self, request, timeout, metadata=None, protocol_options=None):
        """Invokes the underlying RPC.

    Args:
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned iterator may raise
        AbortionError indicating abortion of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event(self, request, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      request: The request value for the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A Call object for the RPC.
    """
        raise NotImplementedError()


class StreamUnaryMultiCallable(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords invoking a stream-unary RPC in any call style.'

    @abc.abstractmethod
    def __call__(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
        """Synchronously invokes the underlying RPC.

    Args:
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      with_call: Whether or not to include return a Call for the RPC in addition
        to the response.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      The response value for the RPC, and a Call for the RPC if with_call was
        set to True at invocation.

    Raises:
      AbortionError: Indicating that the RPC was aborted.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def future(self, request_iterator, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and a future.Future. In the
        event of RPC completion, the return Future's result value will be the
        response value of the RPC. In the event of RPC abortion, the returned
        Future's exception value will be an AbortionError.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event(self, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A single object that is both a Call object for the RPC and a
        stream.Consumer to which the request values of the RPC should be passed.
    """
        raise NotImplementedError()


class StreamStreamMultiCallable(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords invoking a stream-stream RPC in any call style.'

    @abc.abstractmethod
    def __call__(self, request_iterator, timeout, metadata=None, protocol_options=None):
        """Invokes the underlying RPC.

    Args:
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned iterator may raise
        AbortionError indicating abortion of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event(self, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Asynchronously invokes the underlying RPC.

    Args:
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of
        the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A single object that is both a Call object for the RPC and a
        stream.Consumer to which the request values of the RPC should be passed.
    """
        raise NotImplementedError()


class MethodImplementation(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'A sum type that describes a method implementation.\n\n  Attributes:\n    cardinality: A cardinality.Cardinality value.\n    style: A style.Service value.\n    unary_unary_inline: The implementation of the method as a callable value\n      that takes a request value and a ServicerContext object and returns a\n      response value. Only non-None if cardinality is\n      cardinality.Cardinality.UNARY_UNARY and style is style.Service.INLINE.\n    unary_stream_inline: The implementation of the method as a callable value\n      that takes a request value and a ServicerContext object and returns an\n      iterator of response values. Only non-None if cardinality is\n      cardinality.Cardinality.UNARY_STREAM and style is style.Service.INLINE.\n    stream_unary_inline: The implementation of the method as a callable value\n      that takes an iterator of request values and a ServicerContext object and\n      returns a response value. Only non-None if cardinality is\n      cardinality.Cardinality.STREAM_UNARY and style is style.Service.INLINE.\n    stream_stream_inline: The implementation of the method as a callable value\n      that takes an iterator of request values and a ServicerContext object and\n      returns an iterator of response values. Only non-None if cardinality is\n      cardinality.Cardinality.STREAM_STREAM and style is style.Service.INLINE.\n    unary_unary_event: The implementation of the method as a callable value that\n      takes a request value, a response callback to which to pass the response\n      value of the RPC, and a ServicerContext. Only non-None if cardinality is\n      cardinality.Cardinality.UNARY_UNARY and style is style.Service.EVENT.\n    unary_stream_event: The implementation of the method as a callable value\n      that takes a request value, a stream.Consumer to which to pass the\n      response values of the RPC, and a ServicerContext. Only non-None if\n      cardinality is cardinality.Cardinality.UNARY_STREAM and style is\n      style.Service.EVENT.\n    stream_unary_event: The implementation of the method as a callable value\n      that takes a response callback to which to pass the response value of the\n      RPC and a ServicerContext and returns a stream.Consumer to which the\n      request values of the RPC should be passed. Only non-None if cardinality\n      is cardinality.Cardinality.STREAM_UNARY and style is style.Service.EVENT.\n    stream_stream_event: The implementation of the method as a callable value\n      that takes a stream.Consumer to which to pass the response values of the\n      RPC and a ServicerContext and returns a stream.Consumer to which the\n      request values of the RPC should be passed. Only non-None if cardinality\n      is cardinality.Cardinality.STREAM_STREAM and style is\n      style.Service.EVENT.\n  '


class MultiMethodImplementation(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'A general type able to service many methods.'

    @abc.abstractmethod
    def service(self, group, method, response_consumer, context):
        """Services an RPC.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      response_consumer: A stream.Consumer to be called to accept the response
        values of the RPC.
      context: a ServicerContext object.

    Returns:
      A stream.Consumer with which to accept the request values of the RPC. The
        consumer returned from this method may or may not be invoked to
        completion: in the case of RPC abortion, RPC Framework will simply stop
        passing values to this object. Implementations must not assume that this
        object will be called to completion of the request stream or even called
        at all.

    Raises:
      abandonment.Abandoned: May or may not be raised when the RPC has been
        aborted.
      NoSuchMethodError: If this MultiMethod does not recognize the given group
        and name for the RPC and is not able to service the RPC.
    """
        raise NotImplementedError()


class GenericStub(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords RPC invocation via generic methods.'

    @abc.abstractmethod
    def blocking_unary_unary(self, group, method, request, timeout, metadata=None, with_call=False, protocol_options=None):
        """Invokes a unary-request-unary-response method.

    This method blocks until either returning the response value of the RPC
    (in the event of RPC completion) or raising an exception (in the event of
    RPC abortion).

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      with_call: Whether or not to include return a Call for the RPC in addition
        to the response.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      The response value for the RPC, and a Call for the RPC if with_call was
        set to True at invocation.

    Raises:
      AbortionError: Indicating that the RPC was aborted.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def future_unary_unary(self, group, method, request, timeout, metadata=None, protocol_options=None):
        """Invokes a unary-request-unary-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and a future.Future. In the
        event of RPC completion, the return Future's result value will be the
        response value of the RPC. In the event of RPC abortion, the returned
        Future's exception value will be an AbortionError.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def inline_unary_stream(self, group, method, request, timeout, metadata=None, protocol_options=None):
        """Invokes a unary-request-stream-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request: The request value for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned iterator may raise
        AbortionError indicating abortion of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def blocking_stream_unary(self, group, method, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
        """Invokes a stream-request-unary-response method.

    This method blocks until either returning the response value of the RPC
    (in the event of RPC completion) or raising an exception (in the event of
    RPC abortion).

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      with_call: Whether or not to include return a Call for the RPC in addition
        to the response.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      The response value for the RPC, and a Call for the RPC if with_call was
        set to True at invocation.

    Raises:
      AbortionError: Indicating that the RPC was aborted.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def future_stream_unary(self, group, method, request_iterator, timeout, metadata=None, protocol_options=None):
        """Invokes a stream-request-unary-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and a future.Future. In the
        event of RPC completion, the return Future's result value will be the
        response value of the RPC. In the event of RPC abortion, the returned
        Future's exception value will be an AbortionError.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def inline_stream_stream(self, group, method, request_iterator, timeout, metadata=None, protocol_options=None):
        """Invokes a stream-request-stream-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request_iterator: An iterator that yields request values for the RPC.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      An object that is both a Call for the RPC and an iterator of response
        values. Drawing response values from the returned iterator may raise
        AbortionError indicating abortion of the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event_unary_unary(self, group, method, request, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Event-driven invocation of a unary-request-unary-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request: The request value for the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A Call for the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event_unary_stream(self, group, method, request, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Event-driven invocation of a unary-request-stream-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      request: The request value for the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A Call for the RPC.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event_stream_unary(self, group, method, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Event-driven invocation of a unary-request-unary-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A pair of a Call object for the RPC and a stream.Consumer to which the
        request values of the RPC should be passed.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def event_stream_stream(self, group, method, receiver, abortion_callback, timeout, metadata=None, protocol_options=None):
        """Event-driven invocation of a unary-request-stream-response method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.
      receiver: A ResponseReceiver to be passed the response data of the RPC.
      abortion_callback: A callback to be called and passed an Abortion value
        in the event of RPC abortion.
      timeout: A duration of time in seconds to allow for the RPC.
      metadata: A metadata value to be passed to the service-side of the RPC.
      protocol_options: A value specified by the provider of a Face interface
        implementation affording custom state and behavior.

    Returns:
      A pair of a Call object for the RPC and a stream.Consumer to which the
        request values of the RPC should be passed.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def unary_unary(self, group, method):
        """Creates a UnaryUnaryMultiCallable for a unary-unary method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.

    Returns:
      A UnaryUnaryMultiCallable value for the named unary-unary method.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def unary_stream(self, group, method):
        """Creates a UnaryStreamMultiCallable for a unary-stream method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.

    Returns:
      A UnaryStreamMultiCallable value for the name unary-stream method.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def stream_unary(self, group, method):
        """Creates a StreamUnaryMultiCallable for a stream-unary method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.

    Returns:
      A StreamUnaryMultiCallable value for the named stream-unary method.
    """
        raise NotImplementedError()

    @abc.abstractmethod
    def stream_stream(self, group, method):
        """Creates a StreamStreamMultiCallable for a stream-stream method.

    Args:
      group: The group identifier of the RPC.
      method: The method identifier of the RPC.

    Returns:
      A StreamStreamMultiCallable value for the named stream-stream method.
    """
        raise NotImplementedError()


class DynamicStub(six.with_metaclass(abc.ABCMeta)):
    __doc__ = 'Affords RPC invocation via attributes corresponding to afforded methods.\n\n  Instances of this type may be scoped to a single group so that attribute\n  access is unambiguous.\n\n  Instances of this type respond to attribute access as follows: if the\n  requested attribute is the name of a unary-unary method, the value of the\n  attribute will be a UnaryUnaryMultiCallable with which to invoke an RPC; if\n  the requested attribute is the name of a unary-stream method, the value of the\n  attribute will be a UnaryStreamMultiCallable with which to invoke an RPC; if\n  the requested attribute is the name of a stream-unary method, the value of the\n  attribute will be a StreamUnaryMultiCallable with which to invoke an RPC; and\n  if the requested attribute is the name of a stream-stream method, the value of\n  the attribute will be a StreamStreamMultiCallable with which to invoke an RPC.\n  '