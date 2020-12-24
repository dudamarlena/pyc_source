# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hatak/unpackrequest.py
# Compiled at: 2015-03-18 15:58:33
# Size of source mod 2**32: 532 bytes


class UnpackRequest(object):

    def __init__(self):
        self.unpackers = {}

    def add(self, name, method):
        self.unpackers[name] = method

    def generate_property(self, unpacker):
        return property(lambda self: unpacker(self.request))

    def __call__(self, obj):
        for key, unpacker in self.unpackers.items():
            prop = self.generate_property(unpacker)
            setattr(obj.__class__, key, prop)


def unpack(obj, request):
    obj.request = request
    request.registry['unpacker'](obj)