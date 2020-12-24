# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyxtcp/http/service.py
# Compiled at: 2015-10-11 04:08:39
import functools, inspect
from .util import service_log
SERVICE_NAME_SUFFIX = 'Service'

class RPCServiceError(Exception):
    pass


class Service(object):

    def __init__(self):
        self._rpc = dict()

    def _is_valid_service_name(self, service_name):
        if len(service_name) <= len(SERVICE_NAME_SUFFIX):
            return False
        return service_name.endswith(SERVICE_NAME_SUFFIX)

    def _get_rpc_class_name_by_frames(self, frames):
        for item in frames:
            if self._is_valid_service_name(item[3]):
                return item[3]

    def with_f_rpc(self, method):
        _last_frame = inspect.currentframe().f_back
        _last_frame_info = inspect.getframeinfo(_last_frame)
        _rpc_class_name = None
        if self._is_valid_service_name(_last_frame_info.function):
            _rpc_class_name = _last_frame_info.function
        else:
            _rpc_class_name = self._get_rpc_class_name_by_frames(inspect.getouterframes(_last_frame))
        if not _rpc_class_name:
            raise RPCServiceError("rpc class name must reg r'^(.{1,})Service$', method must is staticmethod or classmethod")
        service_log.debug(('Key: `{}.{}` to rpc list').format(_rpc_class_name, method.func_name))
        self._rpc[('{}.{}').format(_rpc_class_name, method.func_name)] = method

        @functools.wraps(method)
        def _wrapper(*args, **kwrags):
            return method(*args, **kwrags)

        return _wrapper

    def get_rpc_function(self, func_key):
        if func_key in self._rpc:
            return self._rpc[func_key]

    def get_all_rpc_functions(self):
        return sorted(self._rpc.keys())