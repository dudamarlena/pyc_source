# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpledependency/decorator.py
# Compiled at: 2011-05-20 20:00:40
from simpledependency import dependency_store

def dependency_decorator(klass):

    def wrap(*args, **kwargs):
        if dependency_store.stored_dependencies.has_key(klass.__name__):
            return dependency_store.stored_dependencies[klass.__name__](*args, **kwargs)
        return klass(*args, **kwargs)

    wrap.__dict__['___name'] = klass.__name__
    return wrap