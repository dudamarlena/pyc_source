# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/performance/list_simple.py
# Compiled at: 2020-05-13 07:44:32
import os, django, sys
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()
from rest_framework.serializers import Serializer
from rest_framework import fields
from drf_serializer_cache import SerializerCacheMixin

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


points = [ Point(x, y, z) for x in range(10) for y in range(10) for z in range(10)
         ]

class PointSerializer(Serializer):
    x = fields.IntegerField()
    y = fields.IntegerField()
    z = fields.IntegerField()


class CachedPointSerializer(SerializerCacheMixin, PointSerializer):
    pass


def simple_serialize():
    return PointSerializer(points, many=True).data


def cached_serialize():
    return CachedPointSerializer(points, many=True).data


if __name__ == '__main__':
    import timeit
    assert simple_serialize() == cached_serialize(), 'Result is wrong'
    print ('Simple list serializer without cache: ',
     timeit.timeit('simple_serialize()', setup='from __main__ import simple_serialize', number=100))
    print ('Simple list serializer with cache(100% cache miss): ',
     timeit.timeit('cached_serialize()', setup='from __main__ import cached_serialize', number=100))