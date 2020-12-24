# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/serialization/_serializer.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 243 bytes


class Serializer(object):

    def serialize(self, data, **kwargs):
        raise NotImplementedError

    def deserialize(self, data, **kwargs):
        raise NotImplementedError

    def combine(self, a, b):
        raise NotImplementedError