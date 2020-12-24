# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\tools\linq.py
# Compiled at: 2018-11-19 03:00:10
# Size of source mod 2**32: 4129 bytes
from collections import Iterable

class linq(object):

    def __init__(self, iterable):
        if not isinstance(iterable, Iterable):
            raise TypeError('参数类型错误')
        self._linq__end = False
        self._linq__iterable = iterable

    def __get_iterable(self):
        if self._linq__end:
            raise StopIteration('迭代器不可重复使用')
        self._linq__end = True
        return self._linq__iterable

    def all(self, predicate):
        return all(map(predicate, self._linq__get_iterable()))

    def any(self, predicate=None):
        return any(map(predicate, self._linq__get_iterable()))

    def where(self, predicate):
        return linq(filter(predicate, self._linq__get_iterable()))

    def max(self):
        return max(self._linq__get_iterable())

    def min(self):
        return min(self._linq__get_iterable())

    def average(self):
        count = 0
        total = 0.0
        for number in self._linq__get_iterable():
            total += number
            count += 1

        return total / count

    def union(self, iterable):
        return linq(self._linq__union(iterable))

    def __union(self, iterable):
        for x in self._linq__get_iterable():
            yield x

        for x in iterable:
            yield x

    def count(self):
        count = 0
        for number in self._linq__get_iterable():
            count += 1

        return count

    def first(self, defaultValue=None):
        return next(self._linq__get_iterable(), defaultValue)

    def last(self, defaultValue=None):
        it = self._linq__get_iterable()
        x = None
        b = False
        while True:
            try:
                x = next(it)
                b = True
            except StopIteration:
                if b:
                    return x
                else:
                    return defaultValue

    def sum(self):
        return sum(self._linq__get_iterable())

    def tolist(self):
        return list(self._linq__get_iterable())

    def select(self, selector):
        return linq(map(selector, self._linq__get_iterable()))


if __name__ == '__main__':
    test_result = {'select-list': {'expected': linq([1, 2, 3, 4, 5, 6]).where(lambda x: x % 2 == 0).select(lambda x: x * 2).tolist(), 
                     'actual': [4, 8, 12]}, 
     
     'sum': {'expected': linq([1, 2, 3, 4, 5, 6]).where(lambda x: x % 2 == 0).sum(), 
             'actual': 12}, 
     
     'max': {'expected': linq([1, 2, 3, 4, 5, 6]).max(), 
             'actual': 6}, 
     
     'min': {'expected': linq([1, 2, 3, 4, 5, 6]).min(), 
             'actual': 1}, 
     
     'all': {'expected': [linq([1, 2, 3, 4, 5, 6]).all(lambda x: x < 3),
                          linq([1, 2, 3, 4, 5, 6]).all(lambda x: x > 0)], 
             
             'actual': [False, True]}, 
     
     'any': {'expected': [linq([1, 2, 3, 4, 5, 6]).any(lambda x: x > 3),
                          linq([1, 2, 3, 4, 5, 6]).any(lambda x: x < 0)], 
             
             'actual': [True, False]}, 
     
     'average': {'expected': linq([1, 2, 3, 4, 5, 6]).average(), 
                 'actual': 3.5}, 
     
     'union': {'expected': linq([1, 2, 3, 4, 5, 6]).union([8, 9, 10]).tolist(), 
               'actual': [1, 2, 3, 4, 5, 6, 8, 9, 10]}, 
     
     'count': {'expected': linq([1, 2, 3, 4, 5, 6]).where(lambda x: x > 1).count(), 
               'actual': 5}, 
     
     'first': {'expected': linq([1, 2, 3, 4, 5, 6]).where(lambda x: x > 1).first(), 
               'actual': 2}, 
     
     'last': {'expected': linq([1, 2, 3, 4, 5, 6]).where(lambda x: x < 4).last(), 
              'actual': 3}}
    for name, result in test_result.items():
        expected = result['expected']
        actual = result['actual']
        if expected == actual:
            print('%s 测试成功!' % name)
        else:
            print('%s 测试失败!\n    应为: %s\n    实为: %s' % (name, actual, expected))