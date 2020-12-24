# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/utils/instance_cache.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import troy

class InstanceCache(object):
    """
    Proper reconnect to pilots and CUs is out of scope for Troy at the moment --
    so troy simply caches instances by their native and their troy ID, to be
    able to retrieve them as needed.  That obviously won't survive an
    application restart, 
    """

    def __init__(self):
        self.instance_cache = dict()
        self.nativeid_cache = dict()

    def put(self, instance, instance_id, native_id):
        self.instance_cache[str(instance_id)] = instance
        self.nativeid_cache[str(native_id)] = instance_id

    def get(self, instance_id=None, native_id=None):
        if not instance_id and not native_id:
            return None
        else:
            if not instance_id:
                if str(native_id) not in self.nativeid_cache:
                    return None
                instance_id = self.nativeid_cache[str(native_id)]
            if str(instance_id) not in self.instance_cache:
                return None
            return self.instance_cache[str(instance_id)]

    def _dump(self):
        import pprint
        pprint.pprint(self.instance_cache)