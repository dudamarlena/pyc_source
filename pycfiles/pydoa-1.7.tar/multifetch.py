# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydo/multifetch.py
# Compiled at: 2007-02-15 13:23:36
from pydo.base import PyDO
from pydo.log import debug
from pydo.utils import iflatten, _strip_tablename
from inspect import isclass
import string
from itertools import izip

class TableAlias(object):
    __module__ = __name__

    def __init__(self, obj, alias):
        self.obj = obj
        self.alias = alias
        self.connectionAlias = self.obj.connectionAlias

    def getAlias(self):
        return self.alias

    def getTable(self):
        return '%s %s' % (self.obj.getTable(), self.alias)

    def getColumns(self, alias=True):
        return self.obj.getColumns(self.alias)

    def getUniquenessConstraints(self):
        return self.obj.getUniquenessConstraints()

    def getDBI(self):
        return self.obj.getDBI()

    def __call__(self, **kwargs):
        return self.obj(**kwargs)


def _processResultSpec(resultSpec):
    for i in resultSpec:
        if isinstance(i, (list, tuple)):
            if len(i) == 2 and isclass(i[0]) and isinstance(i[1], basestring):
                yield TableAlias(*i)
            else:
                raise ValueError, 'nested sequence!'
        else:
            if isclass(i):
                if not issubclass(i, PyDO):
                    raise ValueError, 'unknown class'
            elif not isinstance(i, (TableAlias, basestring)):
                raise ValueError, 'table alias or string expression: %s' % i
            yield i


def iterfetch(resultSpec, sqlTemplate, *values, **kwargs):
    """
    a method that executes sql and returns rows of tuples of PyDO
    objects and scalar values, ordered according to a result set
    specification.

    resultSpec is a list that may contain:

      * PyDO classes;
      
      * 2-tuples of (PyDO class, alias string), which indicate that
        the table represented by the PyDO class is to be referenced by
        the given alias;

      * strings, which represent arbitrary SQL expressions that may
        occur in a SQL column-list specification.

    sqlTemplate is a string that may contain interpolation variables
    in the style of string.Template.  In particular, two variables are
    supplied to this template automatically:

      $COLUMNS -- a list of columns computed from the supplied resultSpec;

      $TABLES -- a list of tables similarly computed.

    Additional interpolation variables may be passed in as keyword
    arguments.  Bind variables to the SQL may also be passed in,
    through positional arguments; if there is only one positional
    argument, and it is a dictionary, it will be used instead of a
    list of values, under the assumption that either the 'named' or
    'pyformat' paramstyle is being used.

    For each element E in the resultSpec, the result row contains one
    element F.  If E is a PyDO class, F will either be an instance of
    E, or, if all its corresponding columns were null for that row and
    E has a uniqueness constraint (which in PyDO is implicitly a not
    null constraint), None.  If E is a string, F will be whatever the
    cursor returned for that column.
    """
    resultSpec = list(_processResultSpec(resultSpec))
    objs = [ x for x in resultSpec if not isinstance(x, basestring) ]
    caliases = tuple(frozenset((o.connectionAlias for o in objs)))
    if len(caliases) > 1:
        raise ValueError, 'objects passed to fetch must have same connection alias'
    elif len(caliases) == 0:
        raise ValueError, 'must supply some object in result spec'
    dbi = objs[0].getDBI()
    tables = (', ').join((x.getTable() for x in objs))
    noneable = [ o for o in objs if o.getUniquenessConstraints() ]
    allcols = []
    for item in resultSpec:
        if hasattr(item, 'getColumns'):
            allcols.append(sorted(item.getColumns(True)))
        else:
            allcols.append(item)

    columns = (', ').join(iflatten(allcols))
    sql = string.Template(sqlTemplate).substitute(kwargs, TABLES=tables, COLUMNS=columns)
    c = dbi.cursor()
    if len(values) == 1 and isinstance(values[0], dict):
        values = values[0]
    if dbi.verbose:
        debug('SQL: %s', sql)
        debug('bind variables: %s', values)
    c.execute(sql, values)
    result = c.fetchall()
    c.close()
    if not result:
        raise StopIteration
    retrow = []
    for row in result:
        del retrow[:]
        p = 0
        for (o, cols) in izip(resultSpec, allcols):
            if isinstance(o, basestring):
                retrow.append(row[p])
                p += 1
            else:
                assert isinstance(o, TableAlias) or isclass(o) and issubclass(o, PyDO)
                d = {}
                for col in cols:
                    d[_strip_tablename(col)] = row[p]
                    p += 1

                if o in noneable:
                    for v in d.itervalues():
                        if v is not None:
                            notnull = True
                            break
                        else:
                            notnull = False

                else:
                    notnull = True
                if notnull:
                    retrow.append(o(**d))
                else:
                    retrow.append(None)

        yield tuple(retrow)

    return


def fetch(resultSpec, sqlTemplate, *values, **kwargs):
    return list(iterfetch(resultSpec, sqlTemplate, *values, **kwargs))


fetch.__doc__ = iterfetch.__doc__
__all__ = [
 'fetch']