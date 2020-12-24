# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/performance/list_with_reused_instance.py
# Compiled at: 2020-05-13 07:59:19
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


class Line:

    def __init__(self, start, end):
        self.start = start
        self.end = end


class PointSerializer(Serializer):
    x = fields.IntegerField()
    y = fields.IntegerField()
    z = fields.IntegerField()


class CachedPointSerializer(SerializerCacheMixin, PointSerializer):

    class Meta:
        """Just some empty meta info."""
        pass


class LineSerializer(Serializer):
    start = PointSerializer()
    end = PointSerializer()


class CachedLineSerializer(SerializerCacheMixin, Serializer):
    start = CachedPointSerializer()
    end = CachedPointSerializer()

    class Meta:
        """Just some empty meta info."""
        pass


start_point = Point(0, 0, 0)
end_point = Point(10, 10, 10)
lines = [ Line(start_point, end_point) for _ in range(1000) ]

def simple_serialize():
    return LineSerializer(lines, many=True).data


def cached_serialize():
    return CachedLineSerializer(lines, many=True).data


if __name__ == '__main__':
    import timeit
    assert simple_serialize() == cached_serialize(), 'Result is wrong'
    print ('Simple list serializer without cache: ',
     timeit.timeit('simple_serialize()', setup='from __main__ import simple_serialize', number=100))
    print ('Simple list serializer with cache: ',
     timeit.timeit('cached_serialize()', setup='from __main__ import cached_serialize', number=100))