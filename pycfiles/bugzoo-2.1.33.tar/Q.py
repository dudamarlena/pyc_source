# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\util\queries\Q.py
# Compiled at: 2013-12-18 14:05:11
import collections, sys, __builtin__
from ..maths import Math
from ..cnv import CNV
from ..logs import Log
from ..struct import nvl, listwrap
from .. import struct
from ..strings import indent, expand_template
from ..struct import StructList, Struct, Null
from ..multiset import Multiset

def run(query):
    query = struct.wrap(query)
    if isinstance(query['from'], list):
        _from = query['from']
    else:
        _from = run(query['from'])
    if query.edges != None:
        Log.error('not implemented yet')
    if query.filter != None:
        Log.error('not implemented yet')
    for param in listwrap(query.window):
        window(_from, param)

    if query.where != None:
        w = query.where
        _from = filter(_from, w)
    if query.sort != None:
        _from = sort(_from, query.sort)
    if query.select != None:
        _from = select(_from, query.select)
    return _from


def groupby(data, keys=None, size=None, min_size=None, max_size=None):
    if size != None or min_size != None or max_size != None:
        if size != None:
            max_size = size
        return groupby_min_max_size(data, min_size=min_size, max_size=max_size)
    else:
        try:

            def keys2string(x):
                return ('|').join([ unicode(x[k]) for k in keys ])

            def get_keys(d):
                return struct.wrap({k:d[k] for k in keys})

            agg = {}
            for d in data:
                key = keys2string(d)
                if key in agg:
                    pair = agg[key]
                else:
                    pair = (
                     get_keys(d), StructList())
                    agg[key] = pair
                pair[1].append(d)

            return agg.values()
        except Exception as e:
            Log.error('Problem grouping', e)

        return


def index(data, keys=None):
    keys = struct.unwrap(listwrap(keys))
    output = dict()
    for d in data:
        o = output
        for k in keys[:-1]:
            v = d[k]
            o = o.get(v, dict())

        v = d[keys[(-1)]]
        o = o.get(v, list())
        o.append(d)

    return output


def unique_index(data, keys=None):
    """
    RETURN dict THAT USES KEYS TO INDEX DATA
    ONLY ONE VALUE ALLOWED PER UNIQUE KEY
    """
    o = Index(listwrap(keys))
    for d in data:
        try:
            o.add(d)
        except Exception as e:
            Log.error('index {{index}} is not unique {{key}} maps to both {{value1}} and {{value2}}', {'index': keys, 
               'key': select([d], keys)[0], 
               'value1': o[d], 
               'value2': d}, e)

    return o


def map(data, relation):
    """
    EXPECTING A dict THAT MAPS VALUES TO lists
    THE LISTS ARE EXPECTED TO POINT TO MEMBERS OF A SET
    A set() IS RETURNED
    """
    if data == None:
        return Null
    else:
        if isinstance(relation, Struct):
            Log.error('Does not accept a Struct')
        if isinstance(relation, dict):
            try:
                output = set()
                for d in data:
                    for cod in relation.get(d, []):
                        output.add(cod)

                return output
            except Exception as e:
                Log.error('Expecting a dict with lists in codomain', e)

        else:
            try:
                output = set()
                for d in data:
                    cod = relation(d)
                    if cod == None:
                        continue
                    output.add(cod)

                return output
            except Exception as e:
                Log.error('Expecting a dict with lists in codomain', e)

        return Null


def select(data, field_name):
    if isinstance(data, Cube):
        Log.error('Do not know how to deal with cubes yet')
    if isinstance(field_name, basestring):
        return [ d[field_name] for d in data ]
    return [ dict([ (k, v) for k, v in x.items() if k in field_name ]) for x in data ]


def get_columns(data):
    output = {}
    for d in data:
        for k, v in d.items():
            if k not in output:
                c = {'name': k, 'domain': Null}
                output[k] = c

    return [ {'name': n} for n in output ]


def stack(data, name=None, value_column=None, columns=None):
    """
    STACK ALL CUBE DATA TO A SINGLE COLUMN, WITH ONE COLUMN PER DIMENSION
    >>> s
          a   b
     one  1   2
     two  3   4

    >>> stack(s)
     one a    1
     one b    2
     two a    3
     two b    4

    STACK LIST OF HASHES, OR 'MERGE' SEPARATE CUBES
    data - expected to be a list of dicts
    name - give a name to the new column
    value_column - Name given to the new, single value column
    columns - explicitly list the value columns (USE SELECT INSTEAD)
    """
    assert value_column != None
    if isinstance(data, Cube):
        Log.error('Do not know how to deal with cubes yet')
    if columns == None:
        columns = data.get_columns()
    data = data.select(columns)
    name = nvl(name, data.name)
    output = []
    parts = set()
    for r in data:
        for c in columns:
            v = r[c]
            parts.add(c)
            output.append({'name': c, 'value': v})

    edge = struct.wrap({'domain': {'type': 'set', 'partitions': parts}})
    return


def unstack(data, keys=None, column=None, value=None):
    assert keys != None
    assert column != None
    assert value != None
    if isinstance(data, Cube):
        Log.error('Do not know how to deal with cubes yet')
    output = []
    for key, values in groupby(data, keys):
        for v in values:
            key[v[column]] = v[value]

        output.append(key)

    return StructList(output)


def normalize_sort(fieldnames):
    """
    CONVERT SORT PARAMETERS TO A NORMAL FORM SO EASIER TO USE
    """
    if fieldnames == None:
        return StructList()
    else:
        formal = []
        for f in listwrap(fieldnames):
            if isinstance(f, basestring):
                f = {'field': f, 'sort': 1}
            formal.append(f)

        return struct.wrap(formal)


def sort(data, fieldnames=None):
    """
    PASS A FIELD NAME, OR LIST OF FIELD NAMES, OR LIST OF STRUCTS WITH {"field":field_name, "sort":direction}
    """
    try:
        if data == None:
            return Null
        else:
            if fieldnames == None:
                return struct.wrap(sorted(data))
            if not isinstance(fieldnames, list):
                if isinstance(fieldnames, basestring):

                    def comparer(left, right):
                        return cmp(nvl(left, Struct())[fieldnames], nvl(right, Struct())[fieldnames])

                    return struct.wrap(sorted(data, cmp=comparer))
                else:

                    def comparer(left, right):
                        return fieldnames['sort'] * cmp(nvl(left, Struct())[fieldnames['field']], nvl(right, Struct())[fieldnames['field']])

                    return struct.wrap(sorted(data, cmp=comparer))

            formal = normalize_sort(fieldnames)

            def comparer(left, right):
                left = nvl(left, Struct())
                right = nvl(right, Struct())
                for f in formal:
                    try:
                        result = f['sort'] * cmp(left[f['field']], right[f['field']])
                        if result != 0:
                            return result
                    except Exception as e:
                        Log.error('problem with compare', e)

                return 0

            if isinstance(data, list):
                output = struct.wrap(sorted(data, cmp=comparer))
            elif hasattr(data, '__iter__'):
                output = struct.wrap(sorted(list(data), cmp=comparer))
            else:
                Log.error('Do not know how to handle')
            return output

    except Exception as e:
        Log.error('Problem sorting\n{{data}}', {'data': data}, e)

    return


def add(*values):
    total = Null
    for v in values:
        if total == None:
            total = v
        elif v != None:
            total += v

    return total


def filter(data, where):
    """
    where  - a function that accepts (record, rownum, rows) and returns boolean
    """
    if isinstance(where, collections.Callable):
        where = wrap_function(where)
    else:
        if len(data) < 10000:
            return [ d for i, d in enumerate(data) if _filter(struct.wrap(where), d, i, data) ]
        where = CNV.esfilter2where(where)
    return [ d for i, d in enumerate(data) if where(d, i, data) ]


def wrap_function(func):
    """
    RETURN A THREE-PARAMETER WINDOW FUNCTION TO MATCH
    """
    numarg = func.__code__.co_argcount
    if numarg == 0:

        def temp(row, rownum, rows):
            return func()

        return temp
    if numarg == 1:

        def temp(row, rownum, rows):
            return func(row)

        return temp
    if numarg == 2:

        def temp(row, rownum, rows):
            return func(row, rownum)

        return temp
    if numarg == 3:
        return func


def window(data, param):
    """
    MAYBE WE CAN DO THIS WITH NUMPY (no, the edges of windows are not graceful with numpy??
    data - list of records
    """
    name = param.name
    edges = param.edges
    sortColumns = param.sort
    value = wrap_function(param.value)
    aggregate = param.aggregate
    _range = param.range
    if aggregate == None and sortColumns == None and edges == None:
        for rownum, r in enumerate(data):
            r[name] = value(r, rownum, data)

        return
    for rownum, r in enumerate(data):
        r['__temp__'] = value(r, rownum, data)

    for keys, values in groupby(data, edges):
        if not values:
            continue
        sequence = sort(values, sortColumns)
        head = nvl(_range.max, _range.stop)
        tail = nvl(_range.min, _range.start)
        total = aggregate()
        for i in range(head):
            total += sequence[i].__temp__

        for i, r in enumerate(sequence):
            r[name] = total.end()
            total.add(sequence[(i + head)].__temp__)
            total.sub(sequence[(i + tail)].__temp__)

    for r in data:
        r['__temp__'] = None

    return


def groupby_size(data, size):
    if hasattr(data, 'next'):
        iterator = data
    else:
        if hasattr(data, '__iter__'):
            iterator = data.__iter__()
        else:
            Log.error('do not know how to handle this type')
        done = []

        def more():
            output = []
            for i in range(size):
                try:
                    output.append(iterator.next())
                except StopIteration:
                    done.append(True)
                    break

            return output

        i = 0
        while True:
            output = more()
            yield (i, output)
            if len(done) > 0:
                break
            i += 1


def groupby_Multiset(data, min_size, max_size):
    if min_size == None:
        min_size = 0
    total = 0
    i = 0
    g = list()
    for k, c in data.items():
        if total < min_size or total + c < max_size:
            total += c
            g.append(k)
        elif total < max_size:
            yield (
             i, g)
            i += 1
            total = c
            g = [k]
        if total >= max_size:
            Log.error('({{min}}, {{max}}) range is too strict given step of {{increment}}', {'min': min_size, 
               'max': max_size, 'increment': c})

    if g:
        yield (
         i, g)
    return


def groupby_min_max_size(data, min_size=0, max_size=None):
    if max_size == None:
        max_size = sys.maxint
    if hasattr(data, '__iter__'):

        def _iter():
            g = 0
            out = []
            for i, d in enumerate(data):
                out.append(d)
                if (i + 1) % max_size == 0:
                    yield (
                     g, out)
                    g += 1
                    out = []

            if out:
                yield (
                 g, out)

        return _iter()
    else:
        if not isinstance(data, Multiset):
            return groupby_size(data, max_size)
        else:
            return groupby_Multiset(data, min_size, max_size)

        return


class Cube:

    def __init__(self, data=None, edges=None, name=None):
        if isinstance(data, Cube):
            Log.error('do not know how to handle cubes yet')
        columns = get_columns(data)
        if edges == None:
            self.edges = [{'name': 'index', 'domain': {'type': 'numeric', 'min': 0, 'max': len(data), 'interval': 1}}]
            self.data = data
            self.select = columns
            return
        else:
            self.name = name
            self.edges = edges
            self.select = Null
            return

    def get_columns(self):
        return self.columns


class Domain:

    def __init__(self):
        pass

    def part2key(self, part):
        pass

    def part2label(self, part):
        pass

    def part2value(self, part):
        pass


class Index(object):

    def __init__(self, keys):
        self._data = {}
        self._keys = struct.unwrap(keys)
        self.count = 0
        code = 'def lookup(d0):\n'
        for i, k in enumerate(self._keys):
            code = code + indent(expand_template('for k{{next}}, d{{next}} in d{{curr}}.items():\n', {'next': i + 1, 
               'curr': i}), prefix='    ', indent=i + 1)

        i = len(self._keys)
        code = code + indent(expand_template('yield d{{curr}}', {'curr': i}), prefix='    ', indent=i + 1)
        exec code
        self.lookup = lookup

    def __getitem__(self, key):
        try:
            if isinstance(key, dict):
                key = struct.unwrap(key)
                key = [ key.get(k, None) for k in self._keys ]
            else:
                if not isinstance(key, list):
                    key = [
                     key]
                d = self._data
                for i, v in enumerate(key):
                    if v == None:
                        Log.error('can not handle when {{key}} == None', {'key': self._keys[i]})
                    if v not in d:
                        return Null
                    d = d[v]

            return d
        except Exception as e:
            Log.error('something went wrong', e)

        return

    def __setitem__(self, key, value):
        Log.error('Not implemented')

    def add(self, val):
        if not isinstance(val, dict):
            val = {
             (
              self._keys[0], val)}
        d = self._data
        for k in self._keys[0:-1]:
            v = val[k]
            if v == None:
                Log.error('can not handle when {{key}} == None', {'key': k})
            if v not in d:
                e = {}
                d[v] = e
            d = d[v]

        v = val[self._keys[(-1)]]
        if v in d:
            Log.error('key already filled')
        d[v] = val
        self.count += 1
        return

    def __contains__(self, key):
        return self[key] != None

    def __iter__(self):
        return self.lookup(self._data)

    def __sub__(self, other):
        output = Index(self._keys)
        for v in self:
            if v not in other:
                output.add(v)

        return output

    def __and__(self, other):
        output = Index(self._keys)
        for v in self:
            if v in other:
                output.add(v)

        return output

    def __or__(self, other):
        output = Index(self._keys)
        for v in self:
            output.add(v)

        for v in other:
            output.add(v)

        return output

    def __len__(self):
        return self.count

    def subtract(self, other):
        return self.__sub__(other)

    def intersect(self, other):
        return self.__and__(other)


def range(_min, _max=None, size=1):
    """
    RETURN (min, max) PAIRS OF GIVEN SIZE, WHICH COVER THE _min, _max RANGE
    THE LAST PAIR BE SMALLER
    """
    if _max == None:
        _max = _min
        _min = 0
    _max = int(Math.ceiling(_max))
    output = ((x, min(x + size, _max)) for x in __builtin__.range(_min, _max, size))
    return output