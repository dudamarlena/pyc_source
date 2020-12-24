# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/lib/data_structures/proxy_container.py
# Compiled at: 2017-12-22 14:35:18
import functools, sys
if sys.version_info[0] <= 2:
    import new

class ProxyContainerMethodsMetaClass(type):

    def __init__(cls, name, bases, dct):
        func_names_to_proxy = dct.get('_proxyfunc_func_set_') or set(['__setitem__', '__getitem__', '__delitem__',
         '__contains__', '__iter__', '__len__'])
        for attr in func_names_to_proxy:
            if not hasattr(cls, attr):
                if sys.version_info[0] > 2:
                    func = functools.partialmethod(dct['_proxyfunc_'], attr)
                    setattr(cls, attr, func)
                else:
                    func = (lambda attr: lambda self, *args, **kwargs: dct['_proxyfunc_'](self, attr, *args, **kwargs))(attr)
                    setattr(cls, attr, new.instancemethod(func, None, cls))

        return super(ProxyContainerMethodsMetaClass, cls).__init__(name, bases, dct)