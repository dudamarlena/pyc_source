# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/slacy/src/pvn2/env/lib/python2.6/site-packages/methodpickle/defer.py
# Compiled at: 2011-02-11 15:41:49
import sys
from copy import deepcopy

class MethodStore(object):
    """Store the module & method name of any method, even if it's not
    loaded.  Provides a simple helper to load & run the method.  This is
    useful for running method invocations that have come in externally from
    other modules.  module_name must me on the import path for this to work
    right."""

    def __init__(self, method=None, module_name=None, class_name=None, method_name=None, attr_name=None):
        if method:
            if hasattr(method, 'im_self'):
                self._module_name = method.im_class.__module__
                self._class_name = method.im_class.__name__
                self._method_name = method.__name__
                self._method_self = deepcopy(method.im_self)
            else:
                self._module_name = method.__module__
                self._class_name = None
                self._method_name = method.__name__
                self._method_self = None
            self._attr_name = attr_name
        else:
            self._module_name = module_name
            self._class_name = None
            self._method_name = method_name
            self._method_self = None
            self._attr_name = attr_name
        self._method = None
        return

    def __getstate__(self):
        """This is what's pickled."""
        return {'module_name': self._module_name, 
           'method_name': self._method_name, 
           'attr_name': self._attr_name, 
           'class_name': self._class_name, 
           'method_self': self._method_self}

    def __setstate__(self, data):
        """Take what was pickled, and restore the state."""
        self.__init__(module_name=data['module_name'], class_name=data['class_name'], method_name=data['method_name'], attr_name=data['attr_name'])
        self._method_self = data['method_self']

    def run(self, *args, **kwargs):
        """Load and run the method, passing the given args, and returning
        the result."""
        method_class = None
        if not self._method:
            if self._class_name:
                __import__(self._module_name, globals(), locals(), [
                 self._class_name])
            else:
                __import__(self._module_name, globals(), locals(), [
                 self._method_name])
            method_module = sys.modules[self._module_name]
            if not method_module:
                raise Exception("Can't find module %s" % self._module_name)
            if self._class_name:
                method_class = getattr(method_module, self._class_name)
                self._method = getattr(method_class, self._method_name)
            else:
                self._method = getattr(method_module, self._method_name)
            if self._attr_name:
                self._method = getattr(self._method, self._attr_name)
            if not self._method:
                raise Exception("Can't find find method via %s %s %s %s" % (
                 self._method_name, self._class_name,
                 self._module_name, self._attr_name))
        if method_class:
            return self._method(self._method_self, *args, **kwargs)
        else:
            return self._method(*args, **kwargs)
            return

    def __str__(self):
        return 'MethodStore(%s)' % (', ').join((self._module_name,
         self._class_name,
         self._method_name,
         self._attr_name))


class DeferredExecution(object):
    """Storage for a deferred (cross-process, cross-machine, persistently
    storable) method call.  We store the method details, as well as a deep
    copy of all the arguments."""

    def __init__(self, stored_method, *args, **kwargs):
        self._stored_method = stored_method
        self._args = deepcopy(args)
        self._kwargs = deepcopy(kwargs)
        self._result = None
        self._run = False
        return

    def __getstate__(self):
        return {'stored_method': self._stored_method, 
           'args': self._args, 
           'kwargs': self._kwargs}

    def __setstate__(self, data):
        self.__init__(data['stored_method'], *data['args'], **data['kwargs'])

    def run(self):
        """Load and run the stored method, returning the result."""
        self._result = self._stored_method.run(*self._args, **self._kwargs)
        self._run = True
        return self._result

    @property
    def result(self):
        """Return the result from the last run."""
        if not self._run:
            raise Exception('You must call run() before getting the result')
        return self._result


class deferred(object):
    """Decorator that returns a deferred execution object."""

    def __init__(self, method):
        self._method = method

    def __call__(self, *args, **kwargs):
        return DeferredExecution(MethodStore(method=self._method, attr_name='_method'), *args, **kwargs)


def defer(method, *args, **kwargs):
    """Helper factory method for the DeferredExecution class.  This is
    easier to use on classes that aren't wrapped in the Defer decorator
    above."""
    return DeferredExecution(MethodStore(method=method), *args, **kwargs)