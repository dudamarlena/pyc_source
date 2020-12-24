# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pandasticsearch/operators/grouper.py
# Compiled at: 2018-09-25 01:28:44


class Grouper(object):

    def __init__(self, field, size=20, inner=None, include=None, exclude=None):
        self._field = field
        self._size = size
        self._inner = inner
        self._include = include
        self._exclude = exclude

    @staticmethod
    def from_list(l):
        if len(l) == 1:
            return Grouper(l[0])
        return Grouper(l[0], inner=Grouper.from_list(l[1:]))

    def build(self):
        terms = {'field': self._field, 'size': self._size}
        if self._exclude is not None:
            assert isinstance(self._exclude, list)
            terms['exclude'] = self._exclude
        if self._include is not None:
            assert isinstance(self._include, list)
            terms['include'] = self._include
        agg = {'terms': terms}
        if self._inner is not None:
            agg['aggregations'] = self._inner.build()
        return {self._field: agg}


class RangeGrouper(Grouper):

    def __init__(self, field, range_list):
        assert isinstance(range_list, list)
        super(RangeGrouper, self).__init__(field)
        self._field = field
        self._range_list = range_list

    def build(self):
        ranges = []
        starts = self._range_list[:-1]
        ends = self._range_list[1:]
        for start, end in zip(starts, ends):
            ranges.append({'from': start, 'to': end})

        name = 'range(' + (',').join([ str(x) for x in self._range_list ]) + ')'
        return {name: {'range': {'field': self._field, 'ranges': ranges}}}


class DateGrouper(Grouper):

    def __init__(self, field, interval, format):
        super(DateGrouper, self).__init__(field)
        self._field = field
        self._interval = interval
        self._format = format

    def build(self):
        name = ('date({0},{1})').format(self._field, self._interval)
        return {name: {'date_histogram': {'field': self._field, 
                                     'interval': self._interval, 
                                     'format': self._format}}}