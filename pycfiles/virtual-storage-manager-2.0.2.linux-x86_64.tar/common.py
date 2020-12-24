# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rpc/common.py
# Compiled at: 2016-06-13 14:11:03
import copy, sys, traceback
from oslo.config import cfg
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import importutils
from vsm.openstack.common import jsonutils
from vsm.openstack.common import local
from vsm.openstack.common import log as logging
CONF = cfg.CONF
LOG = logging.getLogger(__name__)
_RPC_ENVELOPE_VERSION = '2.0'
_VERSION_KEY = 'oslo.version'
_MESSAGE_KEY = 'oslo.message'
_SEND_RPC_ENVELOPE = False

class RPCException(Exception):
    message = _('An unknown RPC related exception occurred.')

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                LOG.exception(_('Exception in string format operation'))
                for name, value in kwargs.iteritems():
                    LOG.error('%s: %s' % (name, value))

                message = self.message

        super(RPCException, self).__init__(message)


class RemoteError(RPCException):
    """Signifies that a remote class has raised an exception.

    Contains a string representation of the type of the original exception,
    the value of the original exception, and the traceback.  These are
    sent to the parent as a joined string so printing the exception
    contains all of the relevant info.

    """
    message = _('Remote error: %(exc_type)s %(value)s\n%(traceback)s.')

    def __init__(self, exc_type=None, value=None, traceback=None):
        self.exc_type = exc_type
        self.value = value
        self.traceback = traceback
        super(RemoteError, self).__init__(exc_type=exc_type, value=value, traceback=traceback)


class Timeout(RPCException):
    """Signifies that a timeout has occurred.

    This exception is raised if the rpc_response_timeout is reached while
    waiting for a response from the remote side.
    """
    message = _('Timeout while waiting on RPC response.')


class DuplicateMessageError(RPCException):
    message = _('Found duplicate message(%(msg_id)s). Skipping it.')


class InvalidRPCConnectionReuse(RPCException):
    message = _('Invalid reuse of an RPC connection.')


class UnsupportedRpcVersion(RPCException):
    message = _('Specified RPC version, %(version)s, not supported by this endpoint.')


class UnsupportedRpcEnvelopeVersion(RPCException):
    message = _('Specified RPC envelope version, %(version)s, not supported by this endpoint.')


class Connection(object):
    """A connection, returned by rpc.create_connection().

    This class represents a connection to the message bus used for rpc.
    An instance of this class should never be created by users of the rpc API.
    Use rpc.create_connection() instead.
    """

    def close(self):
        """Close the connection.

        This method must be called when the connection will no longer be used.
        It will ensure that any resources associated with the connection, such
        as a network connection, and cleaned up.
        """
        raise NotImplementedError()

    def create_consumer(self, topic, proxy, fanout=False):
        """Create a consumer on this connection.

        A consumer is associated with a message queue on the backend message
        bus.  The consumer will read messages from the queue, unpack them, and
        dispatch them to the proxy object.  The contents of the message pulled
        off of the queue will determine which method gets called on the proxy
        object.

        :param topic: This is a name associated with what to consume from.
                      Multiple instances of a service may consume from the same
                      topic. For example, all instances of nova-compute consume
                      from a queue called "compute".  In that case, the
                      messages will get distributed amongst the consumers in a
                      round-robin fashion if fanout=False.  If fanout=True,
                      every consumer associated with this topic will get a
                      copy of every message.
        :param proxy: The object that will handle all incoming messages.
        :param fanout: Whether or not this is a fanout topic.  See the
                       documentation for the topic parameter for some
                       additional comments on this.
        """
        raise NotImplementedError()

    def create_worker(self, topic, proxy, pool_name):
        """Create a worker on this connection.

        A worker is like a regular consumer of messages directed to a
        topic, except that it is part of a set of such consumers (the
        "pool") which may run in parallel. Every pool of workers will
        receive a given message, but only one worker in the pool will
        be asked to process it. Load is distributed across the members
        of the pool in round-robin fashion.

        :param topic: This is a name associated with what to consume from.
                      Multiple instances of a service may consume from the same
                      topic.
        :param proxy: The object that will handle all incoming messages.
        :param pool_name: String containing the name of the pool of workers
        """
        raise NotImplementedError()

    def join_consumer_pool(self, callback, pool_name, topic, exchange_name):
        """Register as a member of a group of consumers for a given topic from
        the specified exchange.

        Exactly one member of a given pool will receive each message.

        A message will be delivered to multiple pools, if more than
        one is created.

        :param callback: Callable to be invoked for each message.
        :type callback: callable accepting one argument
        :param pool_name: The name of the consumer pool.
        :type pool_name: str
        :param topic: The routing topic for desired messages.
        :type topic: str
        :param exchange_name: The name of the message exchange where
                              the client should attach. Defaults to
                              the configured exchange.
        :type exchange_name: str
        """
        raise NotImplementedError()

    def consume_in_thread(self):
        """Spawn a thread to handle incoming messages.

        Spawn a thread that will be responsible for handling all incoming
        messages for consumers that were set up on this connection.

        Message dispatching inside of this is expected to be implemented in a
        non-blocking manner.  An example implementation would be having this
        thread pull messages in for all of the consumers, but utilize a thread
        pool for dispatching the messages to the proxy objects.
        """
        raise NotImplementedError()


def _safe_log(log_func, msg, msg_data):
    """Sanitizes the msg_data field before logging."""
    SANITIZE = {'set_admin_password': [('args', 'new_pass')], 'run_instance': [
                      ('args', 'admin_password')], 
       'route_message': [
                       ('args', 'message', 'args', 'method_info', 'method_kwargs', 'password'),
                       ('args', 'message', 'args', 'method_info', 'method_kwargs', 'admin_password')]}
    has_method = 'method' in msg_data and msg_data['method'] in SANITIZE
    has_context_token = '_context_auth_token' in msg_data
    has_token = 'auth_token' in msg_data
    if not any([has_method, has_context_token, has_token]):
        return log_func(msg, msg_data)
    msg_data = copy.deepcopy(msg_data)
    if has_method:
        for arg in SANITIZE.get(msg_data['method'], []):
            try:
                d = msg_data
                for elem in arg[:-1]:
                    d = d[elem]

                d[arg[(-1)]] = '<SANITIZED>'
            except KeyError as e:
                LOG.info(_('Failed to sanitize %(item)s. Key error %(err)s'), {'item': arg, 'err': e})

    if has_context_token:
        msg_data['_context_auth_token'] = '<SANITIZED>'
    if has_token:
        msg_data['auth_token'] = '<SANITIZED>'
    return log_func(msg, msg_data)


def serialize_remote_exception(failure_info, log_failure=True):
    """Prepares exception data to be sent over rpc.

    Failure_info should be a sys.exc_info() tuple.

    """
    tb = traceback.format_exception(*failure_info)
    failure = failure_info[1]
    if log_failure:
        LOG.error(_('Returning exception %s to caller'), unicode(failure))
        LOG.error(tb)
    kwargs = {}
    if hasattr(failure, 'kwargs'):
        kwargs = failure.kwargs
    data = {'class': str(failure.__class__.__name__), 
       'module': str(failure.__class__.__module__), 
       'message': unicode(failure), 
       'tb': tb, 
       'args': failure.args, 
       'kwargs': kwargs}
    json_data = jsonutils.dumps(data)
    return json_data


def deserialize_remote_exception(conf, data):
    failure = jsonutils.loads(str(data))
    trace = failure.get('tb', [])
    message = failure.get('message', '') + '\n' + ('\n').join(trace)
    name = failure.get('class')
    module = failure.get('module')
    if module not in conf.allowed_rpc_exception_modules:
        return RemoteError(name, failure.get('message'), trace)
    try:
        mod = importutils.import_module(module)
        klass = getattr(mod, name)
        if not issubclass(klass, Exception):
            raise TypeError('Can only deserialize Exceptions')
        failure = klass(**failure.get('kwargs', {}))
    except (AttributeError, TypeError, ImportError):
        return RemoteError(name, failure.get('message'), trace)

    ex_type = type(failure)
    str_override = lambda self: message
    new_ex_type = type(ex_type.__name__ + '_Remote', (ex_type,), {'__str__': str_override, '__unicode__': str_override})
    try:
        failure.__class__ = new_ex_type
    except TypeError:
        failure.args = (message,) + failure.args[1:]

    return failure


class CommonRpcContext(object):

    def __init__(self, **kwargs):
        self.values = kwargs

    def set_status_values(self, values):
        self.values['status_values'] = values

    def __getattr__(self, key):
        try:
            return self.values[key]
        except KeyError:
            raise AttributeError(key)

    def to_dict(self):
        return copy.deepcopy(self.values)

    @classmethod
    def from_dict(cls, values):
        return cls(**values)

    def deepcopy(self):
        return self.from_dict(self.to_dict())

    def update_store(self):
        local.store.context = self

    def elevated(self, read_deleted=None, overwrite=False):
        """Return a version of this context with admin flag set."""
        context = self.deepcopy()
        context.values['is_admin'] = True
        context.values.setdefault('roles', [])
        if 'admin' not in context.values['roles']:
            context.values['roles'].append('admin')
        if read_deleted is not None:
            context.values['read_deleted'] = read_deleted
        return context


class ClientException(Exception):
    """This encapsulates some actual exception that is expected to be
    hit by an RPC proxy object. Merely instantiating it records the
    current exception information, which will be passed back to the
    RPC client without exceptional logging."""

    def __init__(self):
        self._exc_info = sys.exc_info()


def catch_client_exception(exceptions, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if type(e) in exceptions:
            raise ClientException()
        else:
            raise


def client_exceptions(*exceptions):
    """Decorator for manager methods that raise expected exceptions.
    Marking a Manager method with this decorator allows the declaration
    of expected exceptions that the RPC layer should not consider fatal,
    and not log as if they were generated in a real error scenario. Note
    that this will cause listed exceptions to be wrapped in a
    ClientException, which is used internally by the RPC layer."""

    def outer(func):

        def inner(*args, **kwargs):
            return catch_client_exception(exceptions, func, *args, **kwargs)

        return inner

    return outer


def version_is_compatible(imp_version, version):
    """Determine whether versions are compatible.

    :param imp_version: The version implemented
    :param version: The version requested by an incoming message.
    """
    version_parts = version.split('.')
    imp_version_parts = imp_version.split('.')
    if int(version_parts[0]) != int(imp_version_parts[0]):
        return False
    if int(version_parts[1]) > int(imp_version_parts[1]):
        return False
    return True


def serialize_msg(raw_msg, force_envelope=False):
    if not _SEND_RPC_ENVELOPE and not force_envelope:
        return raw_msg
    msg = {_VERSION_KEY: _RPC_ENVELOPE_VERSION, _MESSAGE_KEY: jsonutils.dumps(raw_msg)}
    return msg


def deserialize_msg(msg):
    if not isinstance(msg, dict):
        return msg
    base_envelope_keys = (_VERSION_KEY, _MESSAGE_KEY)
    if not all(map(lambda key: key in msg, base_envelope_keys)):
        return msg
    if not version_is_compatible(_RPC_ENVELOPE_VERSION, msg[_VERSION_KEY]):
        raise UnsupportedRpcEnvelopeVersion(version=msg[_VERSION_KEY])
    raw_msg = jsonutils.loads(msg[_MESSAGE_KEY])
    return raw_msg