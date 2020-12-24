# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpledependency/__init__.py
# Compiled at: 2011-05-21 15:30:34
from simpledependency.dependency_store import DependencyStore
dependency_store = DependencyStore()
from simpledependency.decorator import dependency_decorator

def override_dependency(original_class=None, replacement_class=None):
    if original_class.__dict__.has_key('___name'):
        dependency_store.stored_dependencies[original_class.___name] = replacement_class
    else:
        raise Exception('You must wrap a class in the dependency_decorator to override it.')