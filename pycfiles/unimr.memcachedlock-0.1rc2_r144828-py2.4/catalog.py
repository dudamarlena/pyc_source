# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/memcachedlock/catalog.py
# Compiled at: 2009-04-24 10:31:30
import memcachedlock
from wrapper import wrap_method, call

def get_key(fun, *args, **kargs):
    (fun, instance) = args[0:2]
    return ('/').join(instance.getPhysicalPath())


@memcachedlock.zlock(get_key)
def catalog_object(self, *args, **kw):
    """ ZCatalog's catalog_object """
    call(self, 'catalog_object', *args, **kw)


def patch(scope, original, replacement):
    wrap_method(scope, original, replacement)