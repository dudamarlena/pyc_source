# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/django/registry.py
# Compiled at: 2009-09-20 21:52:30
_CLASS_REGISTRY = []

def classes():
    return _CLASS_REGISTRY


def register_router(klass, ns, name=None):
    if not name:
        name = klass.__name__
        tpl = (klass, name, ns)
        if tpl not in _CLASS_REGISTRY:
            _CLASS_REGISTRY.append(tpl)