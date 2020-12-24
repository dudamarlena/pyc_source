# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/config.py
# Compiled at: 2009-07-20 09:44:04
"""Paste Configuration Middleware and Objects"""
from paste.registry import RegistryManager, StackedObjectProxy
__all__ = [
 'DispatchingConfig', 'CONFIG', 'ConfigMiddleware']

class DispatchingConfig(StackedObjectProxy):
    """
    This is a configuration object that can be used globally,
    imported, have references held onto.  The configuration may differ
    by thread (or may not).

    Specific configurations are registered (and deregistered) either
    for the process or for threads.
    """

    def __init__(self, name='DispatchingConfig'):
        super(DispatchingConfig, self).__init__(name=name)
        self.__dict__['_process_configs'] = []

    def push_thread_config(self, conf):
        """
        Make ``conf`` the active configuration for this thread.
        Thread-local configuration always overrides process-wide
        configuration.

        This should be used like::

            conf = make_conf()
            dispatching_config.push_thread_config(conf)
            try:
                ... do stuff ...
            finally:
                dispatching_config.pop_thread_config(conf)
        """
        self._push_object(conf)

    def pop_thread_config(self, conf=None):
        """
        Remove a thread-local configuration.  If ``conf`` is given,
        it is checked against the popped configuration and an error
        is emitted if they don't match.
        """
        self._pop_object(conf)

    def push_process_config(self, conf):
        """
        Like push_thread_config, but applies the configuration to
        the entire process.
        """
        self._process_configs.append(conf)

    def pop_process_config(self, conf=None):
        self._pop_from(self._process_configs, conf)

    def _pop_from(self, lst, conf):
        popped = lst.pop()
        if conf is not None and popped is not conf:
            raise AssertionError('The config popped (%s) is not the same as the config expected (%s)' % (
             popped, conf))
        return

    def _current_obj(self):
        try:
            return super(DispatchingConfig, self)._current_obj()
        except TypeError:
            if self._process_configs:
                return self._process_configs[(-1)]
            raise AttributeError('No configuration has been registered for this process or thread')

    current = current_conf = _current_obj


CONFIG = DispatchingConfig()
no_config = object()

class ConfigMiddleware(RegistryManager):
    """
    A WSGI middleware that adds a ``paste.config`` key (by default)
    to the request environment, as well as registering the
    configuration temporarily (for the length of the request) with
    ``paste.config.CONFIG`` (or any other ``DispatchingConfig``
    object).
    """

    def __init__(self, application, config, dispatching_config=CONFIG, environ_key='paste.config'):
        """
        This delegates all requests to `application`, adding a *copy*
        of the configuration `config`.
        """

        def register_config(environ, start_response):
            popped_config = environ.get(environ_key, no_config)
            current_config = environ[environ_key] = config.copy()
            environ['paste.registry'].register(dispatching_config, current_config)
            try:
                app_iter = application(environ, start_response)
            finally:
                if popped_config is no_config:
                    environ.pop(environ_key, None)
                else:
                    environ[environ_key] = popped_config

            return app_iter

        super(self.__class__, self).__init__(register_config)


def make_config_filter(app, global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return ConfigMiddleware(app, conf)


make_config_middleware = ConfigMiddleware.__doc__