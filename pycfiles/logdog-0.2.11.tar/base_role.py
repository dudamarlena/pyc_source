# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/core/base_role.py
# Compiled at: 2015-04-04 17:44:17
from __future__ import absolute_import, unicode_literals
import logging
from tornado import gen
from tornado.concurrent import Future
from .config import Config
from .msg import Msg
from .utils import mark_as_proxy_method, is_proxy, simple_oid
logger = logging.getLogger(__name__)

class BaseRole(object):
    defaults = Config(unique=False, start_delay=0)
    _singleton_cache = {}

    @classmethod
    def factory(cls, *args, **kwargs):
        unique = kwargs.get(b'unique', False) or cls.defaults.unique
        if unique:
            key = cls.__singleton_key__(args, kwargs)
            if key in cls._singleton_cache:
                return cls._singleton_cache[key]
            new_obj = cls(*args, **kwargs)
            cls._singleton_cache[key] = new_obj
            return new_obj
        return cls(*args, **kwargs)

    @classmethod
    def __singleton_key__(cls, passed_args, passed_kwargs):
        return (b'{}.{}:{}').format(cls.__module__, cls.__name__, passed_kwargs.get(b'config_name', b'unknown'))

    @property
    def is_unique(self):
        return self.config.unique

    @property
    def is_active(self):
        return self.started or self.config.namespace_default in self.namespaces or self.config.namespace_default in self.app.active_namespaces or bool(set(self.namespaces).intersection(self.app.active_namespaces))

    def __init__(self, *items, **config):
        self._oid = simple_oid()
        self.app = config.pop(b'app')
        self.parent = config.pop(b'parent')
        self.namespaces = config.pop(b'namespaces', None) or self.app.namespaces
        self.config = self.defaults.copy_and_update(config)
        self.items = items
        self._started = self._unique_start_lock = False
        self._started_futures = []
        self._stopped_futures = []
        self.input = self.output = None
        self.send = getattr(self, b'send', None)
        self._forward = getattr(self, b'_forward', None)
        return

    def __str__(self):
        return (b'{}:{}').format(self.__class__.__name__, self.parent)

    @property
    def active_items(self):
        return [ i for i in self.items if i.is_active ]

    def construct_subrole(self, name, conf):
        if isinstance(conf, (list, tuple)):
            conf = {b'*': conf}
        elif conf is None:
            conf = {}
        conf[b'app'] = self.app
        conf[b'parent'] = self
        return self.app.config.find_and_construct_class(name=name, kwargs=conf)

    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, value):
        self._started = bool(value)
        futures = self._started_futures if self.started else self._stopped_futures
        for future in futures:
            future.set_result(self._started)

        if self._started:
            logger.debug(b'[%s] Started.', self)

    def wait_for_start(self):
        f = Future()
        if not self.started:
            self._started_futures.append(f)
        else:
            f.set_result(True)
        return f

    def wait_for_stop(self):
        f = Future()
        if not self.started:
            self._stopped_futures.append(f)
        else:
            f.set_result(False)
        return f

    def link_methods(self):
        if getattr(self, b'send', None) is None:
            self.send = self.get_send_method()
        if getattr(self, b'_forward', None) is None:
            self._forward = self.get_forward_method()
        return

    @mark_as_proxy_method
    def _input_forwarder(self, data):
        return self.output.send(data)

    def get_send_method(self):
        return getattr(self, b'on_recv', self._input_forwarder)

    def get_forward_method(self):
        method = self._input_forwarder
        obj = self.output
        while is_proxy(method):
            if obj:
                method = obj.send
                obj = obj.output
            else:
                break

        return method

    def set_input(self, obj):
        self.input = obj

    def set_output(self, obj):
        self.output = obj

    def _prepare_message_meta(self, **extra):
        meta = self.config.get(b'meta')
        if meta:
            extra.update(meta)
        extra.setdefault(b'host', None)
        return extra

    def _prepare_message(self, data):
        return Msg(message=data, source=None, meta=self._prepare_message_meta())

    def _pre_start(self):
        pass

    def _post_stop(self):
        pass

    @gen.coroutine
    def start(self):
        need_to_skip_start = self.started or not self.is_active
        if not need_to_skip_start and self.is_unique and self._unique_start_lock:
            need_to_skip_start = True
        if not need_to_skip_start:
            if self.is_unique:
                self._unique_start_lock = True
            if self.config.start_delay:
                yield gen.sleep(self.config.start_delay)
            logger.debug(b'[%s] Starting...', self)
            if hasattr(self.output, b'wait_for_start'):
                yield gen.maybe_future(self.output.wait_for_start())
            yield gen.maybe_future(self._pre_start())
            self.started = True
            if self.is_unique:
                logger.debug(b'[%s] Started in a shared mode.', self)

    @gen.coroutine
    def stop(self):
        if self.started:
            logger.debug(b'[%s] Stopping...', self)
            if hasattr(self.input, b'wait_for_stop'):
                yield self.input.wait_for_stop()
            self.started = False
            yield gen.maybe_future(self._post_stop())