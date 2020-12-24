# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mygrate/callbacks.py
# Compiled at: 2014-07-18 08:16:56
import os, os.path, sys, optparse, cPickle, MySQLdb, MySQLdb.cursors

class MygrateCallbacks(object):
    """Manages registration of callbacks for actions against tables.

    """

    def __init__(self):
        self.callbacks = {}
        self.error_handler = self._default_error_handler

    def _default_error_handler(self, table, action, args, kwargs):
        raise

    def get_registered_tables(self):
        return self.callbacks.keys()

    def register_error_handler(self, handler):
        """Registers an error handler for all registered callbacks. When
        execution of a callback results in an exception, ``handler`` is called
        with four arguments: the table, the action, a tuple of positional
        arguments, and a dict of keyword arguments.

        The error handler will be called within scope of the original
        exception, so ``raise`` may be used to propagate the exception and
        :func:`sys.exc_info` will return information about it.

        :param handler: The function to handle callback exceptions.

        """
        self.error_handler = handler

    def register(self, table, action, callback):
        """Registers a callback for a single action on a given table.

        :param table: The table the callback should apply to.
        :param action: The action the callback should apply to.
        :param callback: The function to call when the action happens on the
                         table.

        """
        self.callbacks.setdefault(table, {})
        self.callbacks[table][action] = callback

    def execute(self, table, action, *args, **kwargs):
        if table not in self.callbacks:
            return
        if action not in self.callbacks[table]:
            return
        callback = self.callbacks[table][action]
        try:
            callback(table, *args, **kwargs)
        except Exception:
            self.error_handler(table, action, args, kwargs)