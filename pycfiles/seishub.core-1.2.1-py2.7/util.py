# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\registry\util.py
# Compiled at: 2010-12-23 17:42:44


class RegistryListProxy(object):
    """
    Load a dynamically updated list into a list style registry
    """

    def __init__(self, registry):
        self.registry = registry

    def __get__(self, obj, objtype):
        registry = obj.__getattribute__(self.registry)
        list.__init__(registry, registry.get())
        return registry