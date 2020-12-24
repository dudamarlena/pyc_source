# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/_plugin_wrapping.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 3425 bytes
import collections, logging, threading, grpc
from grpc import _common
from grpc._cython import cygrpc
_LOGGER = logging.getLogger(__name__)

class _AuthMetadataContext(collections.namedtuple('AuthMetadataContext', ('service_url', 'method_name')), grpc.AuthMetadataContext):
    pass


class _CallbackState(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.called = False
        self.exception = None


class _AuthMetadataPluginCallback(grpc.AuthMetadataPluginCallback):

    def __init__(self, state, callback):
        self._state = state
        self._callback = callback

    def __call__(self, metadata, error):
        with self._state.lock:
            if self._state.exception is None:
                if self._state.called:
                    raise RuntimeError('AuthMetadataPluginCallback invoked more than once!')
                else:
                    self._state.called = True
            else:
                raise RuntimeError('AuthMetadataPluginCallback raised exception "{}"!'.format(self._state.exception))
        if error is None:
            self._callback(metadata, cygrpc.StatusCode.ok, None)
        else:
            self._callback(None, cygrpc.StatusCode.internal, _common.encode(str(error)))


class _Plugin(object):

    def __init__(self, metadata_plugin):
        self._metadata_plugin = metadata_plugin

    def __call__(self, service_url, method_name, callback):
        context = _AuthMetadataContext(_common.decode(service_url), _common.decode(method_name))
        callback_state = _CallbackState()
        try:
            self._metadata_plugin(context, _AuthMetadataPluginCallback(callback_state, callback))
        except Exception as exception:
            _LOGGER.exception('AuthMetadataPluginCallback "%s" raised exception!', self._metadata_plugin)
            with callback_state.lock:
                callback_state.exception = exception
                if callback_state.called:
                    return
            callback(None, cygrpc.StatusCode.internal, _common.encode(str(exception)))


def metadata_plugin_call_credentials(metadata_plugin, name):
    if name is None:
        try:
            effective_name = metadata_plugin.__name__
        except AttributeError:
            effective_name = metadata_plugin.__class__.__name__

    else:
        effective_name = name
    return grpc.CallCredentials(cygrpc.MetadataPluginCallCredentials(_Plugin(metadata_plugin), _common.encode(effective_name)))