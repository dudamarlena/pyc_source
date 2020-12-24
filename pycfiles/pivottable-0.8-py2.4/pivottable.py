# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pivottable/pivottable.py
# Compiled at: 2011-02-03 13:33:02
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

try:
    from itertools import product
except ImportError:

    def product(*args, **kwds):
        pools = map(tuple, args) * kwds.get('repeat', 1)
        result = [[]]
        for pool in pools:
            result = [ x + [y] for x in result for y in pool ]

        for prod in result:
            yield tuple(prod)


def resolve_attr(obj, attr):
    for name in attr.split('.'):
        obj = getattr(obj, name)

    return obj


def o_attrgetter(*items):
    if len(items) == 1:
        attr = items[0]

        def g(obj):
            return resolve_attr(obj, attr)

    else:

        def g(obj):
            return tuple((resolve_attr(obj, attr) for attr in items))

    return g


def o_itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return obj[item]

    else:

        def g(obj):
            return tuple((obj[item] for item in items))

    return g


from sys import version_info
if version_info < (2, 5):

    def all(iterable):
        for element in iterable:
            if not element:
                return False

        return True


    attrgetter = o_attrgetter
    itemgetter = o_itemgetter
else:
    from operator import itemgetter, attrgetter
from itertools import ifilter
__all__ = [
 'PivotTable', 'Agregation', 'GroupBy', 'Sum']

class PivotTableError(Exception):
    __module__ = __name__


class Aggregation(object):
    __module__ = __name__
    values = []

    def append(self, value):
        self.values.append(value)

    def __call__(self):
        raise NotImplementedError


class GroupBy(Aggregation):
    __module__ = __name__


class Sum(Aggregation):
    __module__ = __name__

    def __call__(self):
        return sum(self.values)


class PivotTable(object):
    __module__ = __name__
    yaxis_order = []
    xaxis_sort = True
    rows = []
    calculate_subtotals = False
    calculate_totals = False
    subtotal_label = None
    total_label = None
    _sheaders = set()
    _xaxis = None
    _iod = OrderedDict()
    _gk = []

    def __xaxis_get(self):
        """The name of the object attribute that will be use to pivot values.
        This attr must exist in the list of objects assigned to rows. E.g. if
        you want a table that, as columns, has all months for a given year and
        your object provide such date in a 'period' attribute, you should
        assign 'period' as the xaxis
        """
        return self._xaxis

    def __xaxis_set(self, value):
        old_val = self._xaxis
        if not all((hasattr(i, value) for i in self.rows)):
            self._xaxis = old_val
            raise PivotTableError('Selected X-axis is not defined in the submitted objects')
        else:
            self._xaxis = value

    xaxis = property(__xaxis_get, __xaxis_set, doc=__xaxis_get.__doc__)

    def __yaxis_get(self):
        """A list of dictionaries that provides the information required to
        proper understand your object and what kind of pivot table you need.
        Provide a dictionary for each attribute in your object you want in the
        table minus the xaxis attr (that you have already defined in xaxis).
        Each attribute you define will be a row in the new table except the
        ones you define as GroupBy attributes (these are going to be use as the
        pivot keys).
        The supported keys in each dictionary are:
            Mandatory:
                * 'attr': the name of the attr in your object that will provide
                          a value to use in the table
                * 'label': the name you want to show in the table that
                           represents the attr. Useful for translation
                           purposes
                * 'aggr': the kind of operation that will be acted upon the
                          submitted attr. See pivottable.Aggregation for more
                          on this. 
            Optional:
                * 'format': a callable that will be use in 'attr' before
                            presenting the information. Useful for localizing
                            number formats (e.g. an attr value is 0.234 but you
                            want to display '23.4%' to american audiences and
                            '23,4%' to german ones)
        """
        return self._yaxis

    def __yaxis_set(self, value):
        for i in value:
            if 'attr' not in i or 'label' not in i or 'aggr' not in i:
                raise PivotTableError('Your missing some mandatory key in Y-axis definition')

        self._yaxis = value

    yaxis = property(__yaxis_get, __yaxis_set, doc=__yaxis_get.__doc__)

    def __xaxis_format_get(self):
        """Callable that will be applied to the pivotted headers. Useful for
        localization: if your columns will be datetime objects, intead of
        returning the datetime repr, return a string: e.g: "jan-10", "ene-10",
        etc"""
        return self._xaxis_format

    def __xaxis_format_set(self, value):
        if not callable(value):
            raise PivotTableError('Value for X-axis format must be a callable')
        self._xaxis_format = value

    xaxis_format = property(__xaxis_format_get, __xaxis_format_set, doc=__xaxis_format_get.__doc__)

    def _groupby_getter(self):
        """Return all yaxis attributes that were defined as 'group by'"""
        return [ n.get('attr') for n in self.yaxis if n['aggr'] == GroupBy ]

    def _notgroupby_getter(self):
        """Return all yaxis attributes that were defined as not 'group by'"""
        return [ n.get('attr') for n in self.yaxis if n['aggr'] != GroupBy ]

    @property
    def headers(self):
        self._populate_sheaders()
        not_ = False
        self._headers = []
        try:
            self._gk = [
             None] * len(self.yaxis_order)
        except TypeError, e:
            not_ = 0

        try:
            for i in self._groupby_getter():
                if i not in self.yaxis_order:
                    self._headers.append(i)
                else:
                    try:
                        self._gk[self.yaxis_order.index(i)] = i
                    except IndexError:
                        if not isinstance(not_, bool):
                            self._gk[not_] = i
                            not_ += 1

        except AttributeError:
            raise PivotTableError('You need to define Y-axis')

        try:
            while 1:
                self._gk.remove(None)

        except ValueError:
            pass

        if 'metric' not in self._gk:
            self._gk.append('metric')
        self._headers = self._gk + self._headers
        if self.xaxis_sort:
            self._headers += sorted(self._sheaders)
        else:
            self._headers += list(self._sheaders)
        self._iod = OrderedDict([ (i, None) for i in self._headers ])
        return self._headers

    @property
    def result(self):
        self._r = []
        h_ = OrderedDict()
        for h in enumerate(self.headers):
            try:
                h_['c%d' % h[0]] = self.xaxis_format(h[1])
            except AttributeError:
                h_['c%d' % h[0]] = self._dummy_formatter(h[1])

        self._r.append(h_)
        del h_
        ngk = [ i for i in self._notgroupby_getter() ]
        try:
            kd = attrgetter(*self.yaxis_order)
        except TypeError:
            kd = o_attrgetter(*self.yaxis_order)

        k_ = map(kd, self.rows)
        try:
            k_ = sorted(set(k_), key=itemgetter(*range(0, len(k_[0]))))
        except TypeError:
            k_ = sorted(set(k_), key=o_itemgetter(*range(0, len(k_[0]))))
        except IndexError, e:
            k_ = sorted(set(k_))

        for i in k_:
            for j in enumerate(ifilter(lambda x: kd(x) == i, self.rows)):
                for k in enumerate(ngk):
                    if j[0] == 0:
                        cn = -1
                        self._r.append(self._iod.copy())
                    elif k[0] == 0:
                        cn = len(ngk) * -1
                    else:
                        cn += 1
                    m_label = [ m.get('label', k[1]) for m in self.yaxis if m['attr'] == k[1] ]
                    self._r[cn]['metric'] = m_label[0]
                    for l in self.yaxis_order:
                        self._r[cn][l] = getattr(j[1], l)

                    m_format = [ m.get('format', self._dummy_formatter) for m in self.yaxis if m['attr'] == k[1] ]
                    self._r[cn][getattr(j[1], self.xaxis)] = m_format[0](getattr(j[1], k[1]))

        return (n.values() for n in self._r)

    def _populate_sheaders(self):
        """For every submitted row, find the attr mapped to xaxis and return a
        list of them"""
        self._sheaders = set()
        if self.xaxis is None:
            raise PivotTableError('You need to define X-axis')
        for i in self.rows:
            self._sheaders.add(getattr(i, self.xaxis))

        return

    @staticmethod
    def _dummy_formatter(value):
        """Return the same value as submitted in unicode"""
        if value is None:
            return
        return unicode(value)