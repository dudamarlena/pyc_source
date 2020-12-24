# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rdisq/serialization.py
# Compiled at: 2020-03-07 02:12:19
# Size of source mod 2**32: 505 bytes
__author__ = 'smackware'
try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

class AbstractSerializer(object):

    def dumps(self, obj):
        raise NotImplementedError('encode is not implemented')

    def loads(self, obj):
        raise NotImplementedError('decode is not implemented')


class PickleSerializer(object):

    @staticmethod
    def dumps(obj):
        return dumps(obj)

    @staticmethod
    def loads(data):
        return loads(data)