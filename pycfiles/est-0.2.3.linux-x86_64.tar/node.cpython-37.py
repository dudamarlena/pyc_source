# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflow/scheme/node.py
# Compiled at: 2019-12-02 10:03:40
# Size of source mod 2**32: 4380 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '29/05/2017'
import functools, logging, traceback
from collections import namedtuple
import inspect
_logger = logging.getLogger(__file__)
next_node_free_id = 0

def get_next_node_free_id():
    global next_node_free_id
    _id = next_node_free_id
    next_node_free_id += 1
    return _id


_callback_info = namedtuple('_callback_info', [
 'callback', 'handler', 'need_instanciation'])

def trace_unhandled_exceptions(func):

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            outData = func(*args, **kwargs)
        except Exception as e:
            try:
                _logger.exception(e)
                errorMessage = '{0}'.format(e)
                traceBack = traceback.format_exc()
                return WorkflowException(msg=errorMessage,
                  traceBack=traceBack,
                  data=(args[1]))
            finally:
                e = None
                del e

        return outData

    return wrapped_func


class Node(object):
    __doc__ = "\n    Node in the `.Scheme`. Will be associated to a tomwer process.\n\n    :param callback: pointer to a class or a function or str defining the\n                     callback. If the callback is a class then the handler\n                     should be defined or the class should have a default\n                     'process' function that will be called by default.\n    :param int id: unique id of the node.\n    :param dict properties: properties of the node\n    :param str luigi_task: luigi task associate to this node\n    "
    need_stop_join = False

    def __init__(self, callback, id=None, properties=None, error_handler=None):
        self.id = id or get_next_node_free_id()
        self.properties = properties or {}
        self.upstream_nodes = set()
        self.downstream_nodes = set()
        self._Node__process_instance = None
        self.callback = callback
        self._error_handler = error_handler
        self.outData = None

    @property
    def callback(self):
        return self._Node__callback

    @callback.setter
    def callback(self, callback):
        need_instanciation = type(callback) is str or inspect.isclass(callback)
        self._Node__callback = _callback_info(callback=callback, handler=None, need_instanciation=need_instanciation)

    def isfinal(self):
        return len(self.downstream_nodes) is 0

    def isstart(self):
        return len(self.upstream_nodes) is 0


class WorkflowException(Exception):

    def __init__(self, traceBack='', data=None, msg=None):
        if data is None:
            data = {}
        super(WorkflowException, self).__init__(msg)
        self.errorMessage = msg
        self.data = data
        self.traceBack = traceBack