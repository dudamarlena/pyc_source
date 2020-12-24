# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shin4590/src/forks/blueflood-carbon-forwarder/bluefloodserver/util.py
# Compiled at: 2016-01-15 11:21:49
import copy, os, pwd, sys
from os.path import abspath, basename, dirname
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import cPickle as pickle
    USING_CPICKLE = True
except ImportError:
    import pickle
    USING_CPICKLE = False

from time import sleep, time
from twisted.python.util import initgroups
from twisted.scripts.twistd import runApp
if USING_CPICKLE:

    class SafeUnpickler(object):
        PICKLE_SAFE = {'copy_reg': set(['_reconstructor']), 
           '__builtin__': set(['object'])}

        @classmethod
        def find_class(cls, module, name):
            if module not in cls.PICKLE_SAFE:
                raise pickle.UnpicklingError('Attempting to unpickle unsafe module %s' % module)
            __import__(module)
            mod = sys.modules[module]
            if name not in cls.PICKLE_SAFE[module]:
                raise pickle.UnpicklingError('Attempting to unpickle unsafe class %s' % name)
            return getattr(mod, name)

        @classmethod
        def loads(cls, pickle_string):
            pickle_obj = pickle.Unpickler(StringIO(pickle_string))
            pickle_obj.find_global = cls.find_class
            return pickle_obj.load()


else:

    class SafeUnpickler(pickle.Unpickler):
        PICKLE_SAFE = {'copy_reg': set(['_reconstructor']), 
           '__builtin__': set(['object'])}

        def find_class(self, module, name):
            if module not in self.PICKLE_SAFE:
                raise pickle.UnpicklingError('Attempting to unpickle unsafe module %s' % module)
            __import__(module)
            mod = sys.modules[module]
            if name not in self.PICKLE_SAFE[module]:
                raise pickle.UnpicklingError('Attempting to unpickle unsafe class %s' % name)
            return getattr(mod, name)

        @classmethod
        def loads(cls, pickle_string):
            return cls(StringIO(pickle_string)).load()


def get_unpickler(insecure=False):
    if insecure:
        return pickle
    else:
        return SafeUnpickler