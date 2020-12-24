# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysolrwrapper/filter.py
# Compiled at: 2019-01-19 06:16:44
# Size of source mod 2**32: 699 bytes


class Filter:
    pass


class FilterText(Filter):

    def __init__(self, value: [
 str]):
        self._value = value

    def __repr__(self):
        return f"({' '.join(self._value)})"


class FilterColumnEnum(Filter):

    def __init__(self, column: str, value: [str]):
        self._column = column
        self._value = value

    def __repr__(self):
        return f"{self._column}:({' OR '.join(self._value)})"


def AND(*filters: Filter):
    tmp = ' AND '.join([str(x) for x in filters])
    return tmp


def OR(*filters: Filter):
    tmp = ' OR '.join([str(x) for x in filters])
    return f"({tmp})"


def NOT(*filters: Filter):
    tmp = 'NOT (' + AND(*filters) + ')'
    return tmp