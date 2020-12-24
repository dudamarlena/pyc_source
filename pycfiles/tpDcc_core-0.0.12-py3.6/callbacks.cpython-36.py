# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/managers/callbacks.py
# Compiled at: 2020-05-13 19:27:59
# Size of source mod 2**32: 4343 bytes
"""
Module that contains base callbackManager class
"""
from __future__ import print_function, division, absolute_import
import sys, tpDcc
from tpDcc import register
from tpDcc.abstract import callback

class CallbacksManager(object):
    __doc__ = '\n    Static class used to manage all callbacks instances\n    '
    _initialized = False

    @classmethod
    def initialize(cls):
        """
        Initializes all module callbacks
        """
        if cls._initialized:
            return
        default_callbacks = {'Tick': callback.PythonTickCallback}
        try:
            shutdown_type = getattr(tpDcc.Callbacks, 'ShutdownCallback')
        except AttributeError:
            shutdown_type = None

        for callback_name in tpDcc.callbacks():
            n_type = getattr(tpDcc.DccCallbacks, callback_name)[1]['type']
            if n_type == 'simple':
                callback_type = callback.SimpleCallback
            else:
                if n_type == 'filter':
                    callback_type = callback.FilterCallback
                else:
                    tpDcc.logger.warning('Callback Type "{}" is not valid! Using Simplecallback instead ...'.format(n_type))
                    callback_type = callback.SimpleCallback
            if not hasattr(tpDcc, 'Callbacks'):
                tpDcc.logger.warning('DCC {} has no callbacks registered!'.format(tpDcc.Dcc.get_name()))
                return
            callback_class = getattr(tpDcc.Callbacks, '{}Callback'.format(callback_name), None)
            if not callback_class:
                callback_class = default_callbacks.get(callback_name, callback.ICallback)
                tpDcc.logger.warning('Dcc {} does not provides an ICallback for {}Callback. Using {} instead'.format(tpDcc.Dcc.get_name(), callback_name, callback_class.__name__))
            new_callback = getattr(tpDcc, callback_name, None)
            if new_callback:
                new_callback.cleanup()
            register.register_class(callback_name, callback_type(callback_class, shutdown_type))
            tpDcc.logger.debug('Creating Callback "{}" of type "{}" ...'.format(callback_name, callback_class))

        cls._initialized = True

    @classmethod
    def register(cls, callback_type, fn, owner=None):
        """
        Registers, is callback exists, a new callback
        :param callback_type: str, type of callback
        :param fn: Python function to be called when callback is emitted
        :param owner, class
        """
        if type(callback_type) in [list, tuple]:
            callback_type = callback_type[0]
        if callback_type in sys.modules[tpDcc.__name__].__dict__.keys():
            sys.modules[tpDcc.__name__].__dict__[callback_type].register(fn, owner)

    @classmethod
    def unregister(cls, callback_type, fn):
        """
        Unregisters, is callback exists, a new callback
        :param callback_type: str, type of callback
        :param fn: Python function we want to unregister
        """
        if type(callback_type) in [list, tuple]:
            callback_type = callback_type[0]
        if callback_type in sys.modules[tpDcc.__name__].__dict__.keys():
            sys.modules[tpDcc.__name__].__dict__[callback_type].unregister(fn)

    @classmethod
    def unregister_owner_callbacks(cls, owner):
        """
        Unregister all the callbacks from all registered callbacks that belongs to a specific owner
        :param owner: class
        """
        if not cls._initialized:
            return
        for k, v in sys.modules[tpDcc.__name__].__dict__.items():
            if isinstance(v, callback.AbstractCallback):
                v.unregister_owner_callbacks(owner=owner)

    @classmethod
    def cleanup(cls):
        """
        Cleanup all module callbacks
        :param owner: class, If given, only
        :return:
        """
        if not cls._initialized:
            return
        for k, v in sys.modules[tpDcc.__name__].__dict__.items():
            if isinstance(v, callback.AbstractCallback):
                v.cleanup()

        cls._initialized = False