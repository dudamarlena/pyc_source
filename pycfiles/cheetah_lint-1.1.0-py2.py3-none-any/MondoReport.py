# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tools/MondoReport.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = "\n@@TR: This code is pretty much unsupported.\n\nMondoReport.py -- Batching module for Python and Cheetah.\n\nVersion 2001-Nov-18.  Doesn't do much practical yet, but the companion\ntestMondoReport.py passes all its tests.\n-Mike Orr (Iron)\n\nTODO: BatchRecord.prev/next/prev_batches/next_batches/query, prev.query,\nnext.query.\n\nHow about Report: .page(), .all(), .summary()?  Or PageBreaker.\n"
import operator
try:
    from functools import reduce
except ImportError:
    pass

try:
    from Cheetah.NameMapper import valueForKey as lookup_func
except ImportError:

    def lookup_func(obj, name):
        if hasattr(obj, name):
            return getattr(obj, name)
        else:
            return obj[name]


class NegativeError(ValueError):
    pass


def isNumeric(v):
    return isinstance(v, (int, float))


def isNonNegative(v):
    ret = isNumeric(v)
    if ret and v < 0:
        raise NegativeError(v)


def isNotNone(v):
    return v is not None


def Roman(n):
    n = int(n)
    if n < 1:
        raise ValueError('roman numeral for zero or negative undefined: ' + n)
    roman = ''
    while n >= 1000:
        n = n - 1000
        roman = roman + 'M'

    while n >= 500:
        n = n - 500
        roman = roman + 'D'

    while n >= 100:
        n = n - 100
        roman = roman + 'C'

    while n >= 50:
        n = n - 50
        roman = roman + 'L'

    while n >= 10:
        n = n - 10
        roman = roman + 'X'

    while n >= 5:
        n = n - 5
        roman = roman + 'V'

    while n < 5 and n >= 1:
        n = n - 1
        roman = roman + 'I'

    roman = roman.replace('DCCCC', 'CM')
    roman = roman.replace('CCCC', 'CD')
    roman = roman.replace('LXXXX', 'XC')
    roman = roman.replace('XXXX', 'XL')
    roman = roman.replace('VIIII', 'IX')
    roman = roman.replace('IIII', 'IV')
    return roman


def sum(lis):
    return reduce(operator.add, lis, 0)


def mean(lis):
    """Always returns a floating-point number.
    """
    lis_len = len(lis)
    if lis_len == 0:
        return 0.0
    total = float(sum(lis))
    return total / lis_len


def median(lis):
    lis = sorted(lis[:])
    return lis[int(len(lis) / 2)]


def variance(lis):
    raise NotImplementedError()


def variance_n(lis):
    raise NotImplementedError()


def standardDeviation(lis):
    raise NotImplementedError()


def standardDeviation_n(lis):
    raise NotImplementedError()


class IndexFormats:
    """Eight ways to display a subscript index.
       ("Fifty ways to leave your lover....")
    """

    def __init__(self, index, item=None):
        self._index = index
        self._number = index + 1
        self._item = item

    def index(self):
        return self._index

    __call__ = index

    def number(self):
        return self._number

    def even(self):
        return self._number % 2 == 0

    def odd(self):
        return not self.even()

    def even_i(self):
        return self._index % 2 == 0

    def odd_i(self):
        return not self.even_i()

    def letter(self):
        return self.Letter().lower()

    def Letter(self):
        n = ord('A') + self._index
        return chr(n)

    def roman(self):
        return self.Roman().lower()

    def Roman(self):
        return Roman(self._number)

    def item(self):
        return self._item


class ValuesGetterMixin:

    def __init__(self, origList):
        self._origList = origList

    def _getValues(self, field=None, criteria=None):
        if field:
            ret = [ lookup_func(elm, field) for elm in self._origList ]
        else:
            ret = self._origList
        if criteria:
            ret = list(filter(criteria, ret))
        return ret


class RecordStats(IndexFormats, ValuesGetterMixin):
    """The statistics that depend on the current record.
    """

    def __init__(self, origList, index):
        record = origList[index]
        IndexFormats.__init__(self, index, record)
        ValuesGetterMixin.__init__(self, origList)

    def length(self):
        return len(self._origList)

    def first(self):
        return self._index == 0

    def last(self):
        return self._index >= len(self._origList) - 1

    def _firstOrLastValue(self, field, currentIndex, otherIndex):
        currentValue = self._origList[currentIndex]
        try:
            otherValue = self._origList[otherIndex]
        except IndexError:
            return True

        if field:
            currentValue = lookup_func(currentValue, field)
            otherValue = lookup_func(otherValue, field)
        return currentValue != otherValue

    def firstValue(self, field=None):
        return self._firstOrLastValue(field, self._index, self._index - 1)

    def lastValue(self, field=None):
        return self._firstOrLastValue(field, self._index, self._index + 1)

    def percentOfTotal(self, field=None, suffix='%', default='N/A', decimals=2):
        rec = self._origList[self._index]
        if field:
            val = lookup_func(rec, field)
        else:
            val = rec
        try:
            lis = self._getValues(field, isNumeric)
        except NegativeError:
            return default

        total = sum(lis)
        if total == 0.0:
            return default
        else:
            val = float(val)
            try:
                percent = val / total * 100
            except ZeroDivisionError:
                return default

            if decimals == 0:
                percent = int(percent)
            else:
                percent = round(percent, decimals)
            if suffix:
                return str(percent) + suffix
            return percent

    def __call__(self):
        """This instance is not callable, so we override the super method.
        """
        raise NotImplementedError()

    def prev(self):
        if self._index == 0:
            return
        else:
            length = self.length()
            start = self._index - length
            return PrevNextPage(self._origList, length, start)
            return

    def next(self):
        if self._index + self.length() == self.length():
            return
        else:
            length = self.length()
            start = self._index + length
            return PrevNextPage(self._origList, length, start)
            return

    def prevPages(self):
        raise NotImplementedError()

    def nextPages(self):
        raise NotImplementedError()

    prev_batches = prevPages
    next_batches = nextPages

    def summary(self):
        raise NotImplementedError()

    def _prevNextHelper(self, start, end, size, orphan, sequence):
        """Copied from Zope's DT_InSV.py's "opt" function.
        """
        if size < 1:
            if start > 0 and end > 0 and end >= start:
                size = end + 1 - start
            else:
                size = 7
        if start > 0:
            try:
                sequence[(start - 1)]
            except Exception:
                start = len(sequence)

            if end > 0:
                if end < start:
                    end = start
            else:
                end = start + size - 1
                try:
                    sequence[(end + orphan - 1)]
                except Exception:
                    end = len(sequence)

        elif end > 0:
            try:
                sequence[(end - 1)]
            except Exception:
                end = len(sequence)

            start = end + 1 - size
            if start - 1 < orphan:
                start = 1
        else:
            start = 1
            end = start + size - 1
            try:
                sequence[(end + orphan - 1)]
            except Exception:
                end = len(sequence)

        return (start, end, size)


class Summary(ValuesGetterMixin):
    """The summary statistics, that don't depend on the current record.
    """

    def __init__(self, origList):
        ValuesGetterMixin.__init__(self, origList)

    def sum(self, field=None):
        lis = self._getValues(field, isNumeric)
        return sum(lis)

    total = sum

    def count(self, field=None):
        lis = self._getValues(field, isNotNone)
        return len(lis)

    def min(self, field=None):
        lis = self._getValues(field, isNotNone)
        return min(lis)

    def max(self, field=None):
        lis = self._getValues(field, isNotNone)
        return max(lis)

    def mean(self, field=None):
        """Always returns a floating point number.
        """
        lis = self._getValues(field, isNumeric)
        return mean(lis)

    average = mean

    def median(self, field=None):
        lis = self._getValues(field, isNumeric)
        return median(lis)

    def variance(self, field=None):
        raise NotImplementedError()

    def variance_n(self, field=None):
        raise NotImplementedError()

    def standardDeviation(self, field=None):
        raise NotImplementedError()

    def standardDeviation_n(self, field=None):
        raise NotImplementedError()


class PrevNextPage:

    def __init__(self, origList, size, start):
        end = start + size
        self.start = IndexFormats(start, origList[start])
        self.end = IndexFormats(end, origList[end])
        self.length = size


class MondoReport:
    _RecordStatsClass = RecordStats
    _SummaryClass = Summary

    def __init__(self, origlist):
        self._origList = origlist

    def page(self, size, start, overlap=0, orphan=0):
        """Returns list of ($r, $a, $b)
        """
        if overlap != 0:
            raise NotImplementedError('non-zero overlap')
        if orphan != 0:
            raise NotImplementedError('non-zero orphan')
        origList = self._origList
        start = max(0, start)
        end = min(start + size, len(self._origList))
        mySlice = origList[start:end]
        ret = []
        for rel in range(size):
            abs_ = start + rel
            r = mySlice[rel]
            a = self._RecordStatsClass(origList, abs_)
            b = self._RecordStatsClass(mySlice, rel)
            tup = (r, a, b)
            ret.append(tup)

        return ret

    batch = page

    def all(self):
        origList_len = len(self._origList)
        return self.page(origList_len, 0, 0, 0)

    def summary(self):
        return self._SummaryClass(self._origList)