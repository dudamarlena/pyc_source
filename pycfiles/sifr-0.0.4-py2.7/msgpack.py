# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/sifr/daemon/msgpack.py
# Compiled at: 2015-06-10 09:00:02
import datetime
from sifr.span import Day, Minute, Hour, Year, Month
from sifr.util import normalize_time

def span_from_resolution(resolution):
    return {'minute': Minute, 
       'hour': Hour, 
       'day': Day, 
       'month': Month, 
       'year': Year}.get(resolution)


class SifrServer(object):

    def __init__(self, storage):
        self.storage = storage

    def incr(self, key, resolutions, amount):
        now = datetime.datetime.now()
        self.storage.incr_multi([ span_from_resolution(res)(now, [key]) for res in resolutions ], amount)

    def incr_unique(self, key, resolutions, identifier):
        now = datetime.datetime.now()
        self.storage.incr_unique_multi([ span_from_resolution(res)(now, [key]) for res in resolutions ], identifier)

    def track(self, key, resolutions, identifier):
        now = datetime.datetime.now()
        self.storage.track_multi([ span_from_resolution(res)(now, [key]) for res in resolutions ], identifier)

    def count(self, key, at, resolution):
        return self.storage.count(span_from_resolution(resolution)(normalize_time(at), [key]))

    def cardinality(self, key, at, resolution):
        return self.storage.cardinality(span_from_resolution(resolution)(normalize_time(at), [key]))

    def uniques(self, key, at, resolution):
        return tuple(self.storage.uniques(span_from_resolution(resolution)(normalize_time(at), [key])))