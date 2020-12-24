# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqwrl/__init__.py
# Compiled at: 2020-04-20 19:24:50
# Size of source mod 2**32: 40146 bytes
"""
TODO - basic:
 - tbl.index.name setting
 - tbl adding data - setting columns, appending, etc.
TODO - groupby:
 - groupby options - groupby indexing (esp for expr groupbys)
 - groupby push out VirtualTables
 - groupby aggregate multiple agg types, dict agg
 - groupby transform / apply?
TODO - joins:
 - https://pandas.pydata.org/pandas-docs/stable/merging.html
 - test all hows
 - pd.concat (row-wise: UNION, UNION ALL)
 - pd.merge (https://pandas.pydata.org/pandas-docs/stable/merging.html#database-style-dataframe-joining-merging)
 - todo: move df.join to pd.merge (more general)

"""
import copy, operator
from functools import wraps, partialmethod, reduce
from collections.abc import Iterable
from warnings import warn
import numbers, pandas as pd, numpy as np, sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import mssql, postgresql
import sympy
from toolz import assoc, valfilter
import datashape
__version__ = '0.1.0'
sa_types = {'int64':sa.BigInteger, 
 'int32':sa.Integer, 
 'int':sa.Integer, 
 'int16':sa.SmallInteger, 
 'float32':sa.REAL, 
 'float64':sa.FLOAT, 
 'float':sa.FLOAT, 
 'real':sa.FLOAT, 
 'string':sa.Text, 
 'date':sa.Date, 
 'time':sa.Time, 
 'datetime':sa.DateTime, 
 'bool':sa.Boolean, 
 "timedelta[unit='D']":sa.Interval(second_precision=0, day_precision=9), 
 "timedelta[unit='h']":sa.Interval(second_precision=0, day_precision=0), 
 "timedelta[unit='m']":sa.Interval(second_precision=0, day_precision=0), 
 "timedelta[unit='s']":sa.Interval(second_precision=0, day_precision=0), 
 "timedelta[unit='ms']":sa.Interval(second_precision=3, day_precision=0), 
 "timedelta[unit='us']":sa.Interval(second_precision=6, day_precision=0), 
 "timedelta[unit='ns']":sa.Interval(second_precision=9, day_precision=0)}
sa_revtypes = dict(map(reversed, sa_types.items()))

class MSSQLTimestamp(mssql.TIMESTAMP):
    pass


mssql.base.ischema_names['TIMESTAMP'] = MSSQLTimestamp
sa_revtypes.update({sa.DATETIME: datashape.datetime_, 
 sa.TIMESTAMP: datashape.datetime_, 
 sa.FLOAT: datashape.float64, 
 sa.DATE: datashape.date_, 
 sa.BIGINT: datashape.int64, 
 sa.INTEGER: datashape.int_, 
 sa.BIGINT: datashape.int64, 
 sa.types.NullType: datashape.string, 
 sa.REAL: datashape.float32, 
 sa.Float: datashape.float64, 
 mssql.BIT: datashape.bool_, 
 mssql.DATETIMEOFFSET: datashape.string, 
 mssql.MONEY: datashape.float64, 
 mssql.SMALLMONEY: datashape.float32, 
 mssql.UNIQUEIDENTIFIER: datashape.string, 
 MSSQLTimestamp: datashape.bytes_})
precision_types = {
 sa.Float,
 postgresql.base.DOUBLE_PRECISION}

def precision_to_dtype(precision):
    """
    Maps a float or double precision attribute to the desired dtype.
    The mappings are as follows:
    [1, 24] -> float32
    [25, 53] -> float64
    Values outside of those ranges raise a ``ValueError``.
    Parameter
    ---------
    precision : int
         A double or float precision. e.g. the value returned by
    `postgresql.base.DOUBLE_PRECISION(precision=53).precision`
    Returns
    -------
    dtype : datashape.dtype (float32|float64)
         The dtype to use for columns of the specified precision.
    """
    if isinstance(precision, numbers.Integral):
        if 1 <= precision <= 24:
            return float32
        if 25 <= precision <= 53:
            return float64
    raise ValueError('{} is not a supported precision'.format(precision))


sa_revtypes = valfilter(lambda x: not isinstance(x, sa.Interval), sa_revtypes)

def discover_typeengine(typ):
    if isinstance(typ, sa.Interval):
        if typ.second_precision is None:
            if typ.day_precision is None:
                return datashape.TimeDelta(unit='us')
        if typ.second_precision == 0:
            if typ.day_precision == 0:
                return datashape.TimeDelta(unit='s')
        if typ.second_precision in units_of_power:
            units = typ.day_precision or units_of_power[typ.second_precision]
        else:
            if typ.day_precision > 0:
                units = 'D'
            else:
                raise ValueError('Cannot infer INTERVAL type with parameterssecond_precision=%d, day_precision=%d' % (
                 typ.second_precision, typ.day_precision))
        return datashape.TimeDelta(unit=units)
    if type(typ) in precision_types:
        if typ.precision is not None:
            return precision_to_dtype(typ.precision)
    if typ in sa_revtypes:
        return datashape.dshape(sa_revtypes[typ])[0]
    if type(typ) in sa_revtypes:
        return sa_revtypes[type(typ)]
    if isinstance(typ, sa.Numeric):
        return datashape.Decimal(precision=(typ.precision), scale=(typ.scale))
    if isinstance(typ, (sa.String, sa.Unicode)):
        return datashape.String(typ.length, 'U8')
    for k, v in sa_revtypes.items():
        if isinstance(k, type) and (isinstance(typ, k) or hasattr)(typ, 'impl'):
            if isinstance(typ.impl, k):
                return v
            if k == typ:
                return v
        raise NotImplementedError('No SQL-datashape match for type %s' % typ)


def is_striter(val):
    return isinstance(val, Iterable) and all((isinstance(el, str) for el in val))


def is_iter_notstr(val):
    return isinstance(val, Iterable) and not isinstance(val, str)


def and_(*args):
    return reduce(operator.and_, args)


def _dtype(type_name):
    if type_name == 'string':
        type_name = 'object'
    return np.dtype(type_name)


class DB:

    def __init__(self, engine, verbose=False, check='auto', autoindex=True):
        if isinstance(engine, str):
            engine = sa.create_engine(engine, echo=verbose)
        else:
            engine.echo = verbose
        self.engine = engine
        if check == 'auto':
            try:
                from IPython import get_ipython
                check = get_ipython() is not None
            except ImportError:
                check = False

        self.check = check
        self.autoindex = autoindex

    @property
    def metadata(self):
        return sa.MetaData().reflect(bind=(self.engine))

    @property
    def tables(self):
        return self.engine.table_names()

    def __iter__(self):
        return iter(self.tables)

    def __contains__(self, k):
        return k in self.tables

    def __len__(self):
        return len(self.tables)

    def __getitem__(self, k):
        if self.check:
            assert k in self
        return Table((self.engine), k, check=(self.check), index=(self.autoindex))

    def __setitem__(self, k, v):
        if k not in self:
            metadata, _ = Table.from_df(v, k)
            metadata.create_all(self.engine)
            self[k].append(v)
        else:
            raise NotImplementedError()


_colobjtypes = {str: sa.String}

def to_sqlalchemy_type(s):
    if s.dtype.name in sa_types:
        return sa_types[s.dtype.name]
    el = s.iloc[0]
    if type(el).__name__ in sa_types:
        return sa_types[s.dtype.name]
    for k, v in _colobjtypes.items():
        if isinstance(el, k):
            return v
        raise TypeError('unknown type: %s / %s' % (s.dtype.name, type(el)))


_numeric_types = [typ for typ in sa_types if any((typ.startswith(numtyp) for numtyp in ('bool',
                                                                                        'float',
                                                                                        'int',
                                                                                        'timedelta')))]

class VirtualTable:

    def __init__(self, engine, salc, check=True, whereclause=None, from_i=None, to_i=None, sort_by=[], index=True, columns=None):
        self.engine = engine
        self.sa = salc
        self._whereclause = whereclause
        self._from_i = from_i
        self._to_i = to_i
        self._sort_by = sort_by
        if isinstance(index, (str, Expression)):
            index = [
             index]
        if index == True:
            self._ix = [c.name for c in self.sa_columns if c.primary_key]
            self._ixdata = [c for c in self.sa_columns if c.primary_key]
        else:
            if is_striter(index):
                self._ix = list(index)
                self._ixdata = [self.sa_colmap[col] for col in self._ix]
            else:
                if index == False or index is None:
                    self._ix = []
                    self._ixdata = []
                else:
                    if all((isinstance(ix, Expression) for ix in index)):
                        self._ix = [c.name for c in index]
                        self._ixdata = list(index)
                    elif columns is None:
                        self._columns = [c.name for c in self.sa_columns if c.name not in self._ix]
                        self._coldata = [c for c in self.sa_columns if c.name not in self._ix]
                    else:
                        if is_striter(columns):
                            self._columns = list(columns)
                            self._coldata = [self.sa_colmap[col] for col in self._columns]
                        else:
                            if all((isinstance(col, Expression) for col in columns)):
                                self._columns = [c.name for c in columns]
                                self._coldata = list(columns)

    def copy(self, **new_attrs):
        new = copy.copy(self)
        for k, v in new_attrs.items():
            setattr(new, k, v)
        else:
            return new

    @property
    def sa_columns(self):
        cols = self.sa.columns
        self.__dict__['sa_columns'] = cols
        return cols

    @property
    def sa_colmap(self):
        colmap = {c:c.name for c in self.sa_columns}
        self.__dict__['sa_colmap'] = colmap
        return colmap

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, column_names):
        assert len(column_names) == len(self._coldata)
        self._columns = column_names

    def _colmatches(self, col, singleton=False, required=False):
        matches = [datum for name, datum in zip(self._columns, self._coldata) if col == name]
        if required:
            if not matches:
                raise KeyError('key %r not found among %r' % (col, self._columns))
        if singleton:
            if len(matches) > 1:
                raise KeyError('ambiguous key %r among %r' % (col, self._columns))
            matches = matches[0] if matches else None
        return matches

    def rename(self, columns=None):
        if columns is not None:
            if isinstance(columns, Mapping):
                new_cols = [columns.get(col, col) for col in self._columns]
            else:
                if isinstance(columns, Callable):
                    new_cols = [columns(col) for col in self._columns]
                else:
                    raise TypeError('unknown mapper type: %s' % type(columns))
            return self.copy(_columns=new_cols)
        return self

    @property
    def coltypes(self):
        cols = [c for c in self.sa_columns if c.name not in self._ix]
        return pd.Series([str(discover_typeengine(c.type)) for c in cols], index=[c.name for c in cols])

    @property
    def dtypes(self):
        return self.coltypes.map(_dtype)

    def iteritems(self):
        (yield from zip(self._columns, self._coldata))
        if False:
            yield None

    items = iteritems

    def keys(self):
        (yield from self._columns)
        if False:
            yield None

    __iter__ = keys

    def __getitem__(self, k):
        if isinstance(k, str):
            colmatches = self._colmatches(k, required=True)
            if len(colmatches) == 1:
                return Expression(self, colmatches[0], k)
            return self.copy(_columns=([k] * len(colmatches)), _coldata=colmatches)
        else:
            if is_striter(k):
                new_columns = []
                new_coldata = []
                for el in k:
                    colmatches = self._colmatches(el, required=True)
                    new_columns += [el] * len(colmatches)
                    new_coldata += colmatches
                else:
                    return self.copy(_columns=new_columns, _coldata=new_coldata)

            if isinstance(k, slice):
                return self.islice(k)
            if isinstance(k, Expression):
                return self.where(k)
        return self._loc(k)

    @property
    def index(self):
        if len(self._ix) == 0:
            return
        if len(self._ix) == 1:
            return Expression(self, self._ixdata[0], self._ix[0])
        return self.copy(_columns=(list(_ix)), _coldata=(list(_ixdata)))

    def reset_index(self, drop=False):
        if drop:
            return self.copy(_ix=[], _ixdata=[])
        return self.copy(_ix=[], _ixdata=[], _columns=(self._columns + self._ix), _coldata=(self._coldata + self._ixdata))

    def set_index(self, keys, drop=True, append=False):
        if isinstance(keys, (str, Expression)):
            keys = [
             keys]
        new_ix = list(self._ix) if append else []
        new_ixdata = list(self._ixdata) if append else []
        new_columns = list(self._columns)
        new_coldata = list(self._coldata)
        for k in keys:
            if isinstance(k, str):
                new_ixdata.append(self._colmatches(k, singleton=True, required=True))
                new_ix.append(k)
                if drop:
                    ix = new_columns.index(k)
                    new_columns.pop(ix)
                    new_coldata.pop(ix)
            elif isinstance(k, Expression):
                new_ixdata.append(k)
                new_ix.append(k.name)
            else:
                return self.copy(_ix=new_ix, _ixdata=new_ixdata, _columns=new_columns,
                  _coldata=new_coldata)

    def _lookup(self, k):
        result = self.where(self.index == k).df
        if len(result) == 1:
            return result.iloc[0]
        if len(result) == 0:
            raise KeyError('%r not found in %s' % (k, self.index))
        return result

    def _loc(self, k):
        if isinstance(k, tuple):
            if len(k) == 2:
                condition, cols = k
                if not isinstance(cols, str):
                    if is_striter(cols):
                        return self._loc(condition)[cols]
        if isinstance(k, slice):
            if k.step is not None:
                return self._loc(slice(k.start, k.stop))[::k.step]
                if k.start is None:
                    if k.stop is not None:
                        return self.where(self.index <= k.stop)
            else:
                if k.start is not None:
                    if k.stop is None:
                        return self.where(self.index >= k.start)
                if k.start is not None and k.stop is not None:
                    return self.where(self.index >= k.start & self.index <= k.stop)
            return self
        if isinstance(k, Expression):
            return self.where(k)
        if is_iter_notstr(k):
            results = [self._lookup(el) for el in k]
            result = pd.concat([pd.DataFrame([r]) if isinstance(r, pd.Series) else r for r in results])
            result.index.name = self.index.name
            dtypes = dict(zip(self.columns, self.dtypes))
            for col in result.columns:
                result[col] = result[col].astype(dtypes[col])
            else:
                return result

        return self._lookup(k)

    def islice(self, from_i=None, to_i=None, step=None):
        if isinstance(from_i, slice):
            if to_i is None:
                if step is None:
                    return self.islice(from_i.start, from_i.stop, from_i.step)
        elif step is not None:
            if not (step == -1 and self._sort_by):
                raise AssertionError
            sort_by = [(
             by, not asc) for by, asc in self._sort_by]
        else:
            sort_by = self._sort_by
        if not (from_i is not None and from_i < 0):
            if to_i is not None:
                if to_i < 0:
                    l = len(self)
                    if from_i is not None:
                        if from_i < 0:
                            from_i += l
                    if to_i is not None:
                        if to_i < 0:
                            to_i += l
            base_from = 0 if self._from_i is None else self._from_i
            base_to = float('inf') if self._to_i is None else self._to_i
            new_from = base_from + (from_i or 0)
            new_to = base_to if to_i is None else min(base_to, base_from + to_i)
            if new_to == float('inf'):
                new_to = None
        return self.copy(_from_i=(new_from or None), _to_i=new_to, _sort_by=sort_by)

    @property
    def iloc(self):
        return Indexer(self.islice)

    @property
    def loc(self):
        return Indexer(self._loc)

    def where(self, where):
        if self._from_i or self._to_i:
            warn('wheres on slices not accurately implemented, use at your own risk')
        if self._whereclause is not None:
            where = self._whereclause & where
        return self.copy(_whereclause=where)

    def head(self, n=5):
        return self.islice(0, n)

    def tail(self, n=5):
        return self.islice(-n)

    def sort_values(self, by, ascending=True):
        if self._from_i or self._to_i:
            warn('sorts on slices not accurately implemented, use at your own risk')
        elif isinstance(by, (str, Expression)):
            by = [
             by]
            ascending = [ascending]
        else:
            if ascending in {False, True}:
                ascending = [
                 ascending] * len(by)
        sort_by = list(self._sort_by)
        for k, asc in zip(reversed(by), reversed(ascending)):
            if isinstance(k, str):
                colmatch = self._colmatches(k, singleton=True, required=True)
                sort_by.insert(0, (Expression(self, colmatch, k), asc))
            elif isinstance(k, Expression):
                sort_by.insert(0, (k, asc))
            else:
                raise TypeError('unknown type for sort: %s' % type(k))
        else:
            return self.copy(_sort_by=sort_by)

    def sort_index(self, ascending=True):
        if self._from_i or self._to_i:
            warn('sorts on slices not accurately implemented, use at your own risk')
        return self.sort_values([Expression(self, datum, ix) for ix, datum in zip(self._ix, self._ixdata)],
          ascending=ascending)

    def _query_sorted_by(self, q, by, ascending=True):
        if isinstance(by, (str, Expression)):
            by = [
             by]
            ascending = [ascending]
        else:
            if ascending in {False, True}:
                ascending = [
                 ascending] * len(by)
        order_by = []
        for k, asc in zip(by, ascending):
            if isinstance(k, str):
                k = self._colmatches(k, singleton=True, required=True)
            else:
                if isinstance(k, Expression):
                    k = k.sa
                else:
                    raise TypeError('unknown by type: %s' % type(k))
            order_by.append(k if asc else k.desc())
        else:
            return (q.order_by)(*order_by)

    def connect(self):
        return self.engine.connect()

    def _select_query(self, what, where=None, from_i=None, to_i=None, groupby=None, sort_by=None, sort_ascending=True):
        if sort_by is not None:
            return self.sort_values(by=sort_by, ascending=sort_ascending)._select_query(what,
              where=where, from_i=from_i, to_i=to_i, groupby=groupby)
        else:
            if where is not None:
                return self.where(where)._select_query(what, from_i=from_i, to_i=to_i, groupby=groupby)
            if from_i is not None or to_i is not None:
                return self.islice(from_i, to_i)._select_query(what, groupby=groupby)
            q = sa.select(what).select_from(self.sa)
            if self._whereclause is not None:
                q = q.where(self._whereclause.sa)
            if self._to_i is not None:
                q = q.limit(self._to_i - (self._from_i or 0))
            if self._from_i is not None and self._from_i > 0:
                q = q.offset(self._from_i)
        if self._sort_by is not None:
            q = (q.order_by)(*[by.sa if asc else by.sa.desc() for by, asc in self._sort_by])
        if groupby is not None:
            q = (q.group_by)(*groupby)
        return q

    def select_row(self, what, **kwargs):
        singleton = not isinstance(what, list)
        if singleton:
            what = [
             what]
        with self.connect() as (conn):
            q = (self._select_query)(what, **kwargs)
            resp = conn.execute(q).fetchone()
        if singleton:
            return resp[0]
        return resp

    def iterselect(self, what, **kwargs):
        what_dedup = [el for i, el in enumerate(what) if el not in what[:i]]
        ixs = [what_dedup.index(el) for el in what]
        with self.connect() as (conn):
            q = (self._select_query)(what_dedup, **kwargs)
            for row in conn.execute(q):
                (yield tuple((row[i] for i in ixs)))

    def itertuples(self, index=True, name='Pandas'):
        names = self._ix + self._columns if index else self._columns
        data = self._ixdata + self._coldata if index else self._coldata
        typ = namedtuple(name, names)
        for row in self.iterselect(data):
            (yield typ(*row))

    def iterrows(self):
        n_ix = len(self.ix)
        for row in self.iterselect(self._ixdata + self._coldata):
            (yield (row[:n_ix], pd.Series((row[n_ix:]), index=(self._columns))))

    def to_dataframe(self):
        names = self._ix + self._columns
        data = self._ixdata + self._coldata
        df = pd.DataFrame.from_records((list(self.iterselect(data))), columns=(list(range(len(names)))))
        if len(self._ix) == 1:
            df.set_index(0, inplace=True)
            df.index.name = self._ix[0]
        else:
            if self._ix:
                df.set_index((list(range(len(self._ix)))), inplace=True)
                df.index.names = self._ix
            else:
                df.columns = self._columns
                if self._from_i is not None:
                    self._ix or df.index += self._from_i
            return df

    @property
    def data(self):
        return self.to_dataframe()

    @property
    def df(self):
        return self.to_dataframe()

    def __len__(self):
        return self.select_row(sa.func.count())

    def insert(self, rows):
        ins = self.sa.insert()
        with self.connect() as (conn):
            conn.execute(ins, rows)

    def append(self, df):
        if df.index.name is None:
            rows = [row.to_dict() for _, row in df.iterrows()]
        else:
            rows = [assoc(row.to_dict(), df.index.name, ix) for ix, row in df.iterrows()]
        self.insert(rows)

    def _agg_pairwise(self, how):
        how = {}.get(how, how)
        cols = self.columns
        fn = getattr(func, how)
        resp = self.select_row([fn(self[col1].sa, self[col2].sa) for col1 in cols for col2 in cols])
        result = pd.DataFrame.from_records([resp[i * len(cols):(i + 1) * len(cols)] for i in range(len(cols))],
          index=cols,
          columns=cols)
        return result

    def aggregate(self, how, axis=None, skipna=None):
        how = {'mean':'avg', 
         'std':'stddev',  'var':'variance'}.get(how, how)
        fn = getattr(func, how)
        if axis in {0, None}:
            cols = self.columns
            vals = self.select_row([fn(self[col].sa) for col in cols])
            return pd.Series(vals, index=cols)
        if axis == 1:
            agg_sa = fn(*[self[col].sa for col in self.columns])
            return Expression(self, agg_sa, how)
        raise ValueError('axis not in {None, 0, 1}: %s' % axis)

    def nunique(self, dropna=True):
        cols = self.columns
        vals = self.select_row([func.count(self[col].sa.distinct()) for col in cols])
        return pd.Series(vals, index=cols)

    def groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, **kwargs):
        return GroupBy(self, by, sort=sort, as_index=as_index)

    def _repr_html_(self):
        df = self.head().df
        if len(self) > len(df):
            df = df.append(pd.Series('...', index=(df.columns), name='...'))
        return df._repr_html_()

    def alias(self, name=None):
        new_sa = self.sa.alias(name=name)
        new_cols = new_sa.columns
        new_ixdata = [getattr(new_cols, c.name) for c in self._ixdata]
        new_coldata = [getattr(new_cols, c.name) for c in self._coldata]
        return self.copy(sa=new_sa, _ixdata=new_ixdata, _coldata=new_coldata)

    def join(self, other, on=None, how='left', lsuffix='', rsuffix='', sort=False):
        if not how in {'right', 'inner', 'left', 'outer'}:
            raise AssertionError
        elif how == 'right':
            return other.join(self, on=on, how='left', lsuffix=rsuffix, rsuffix=lsuffix, sort=sort)
            alias_self = self.alias()
            alias_other = other.alias()
            if on is None:
                assert set(alias_self._ix) == set(alias_other._ix), 'mismatched indexes'
                on_clause = and_(*[ixdata == alias_other._ixdata[alias_other._ix.index(ix)] for ix, ixdata in zip(alias_self._ix, alias_self._ixdata)])
            else:
                if isinstance(on, str):
                    on = [
                     on]
                on_clause = and_(*[alias_self[col].sa == alias_other[col].sa for col in on])
            col_overlap = set(alias_self.columns) & set(alias_other.columns)
            if col_overlap:
                if not lsuffix:
                    assert rsuffix, 'columns overlap but no suffix specified'
                self_columns = [str(col) + lsuffix if col in col_overlap else col for col in alias_self.columns]
                other_columns = [str(col) + rsuffix if col in col_overlap else col for col in alias_other.columns]
                new_cols = self_columns + other_columns
        else:
            new_cols = alias_self.columns + alias_other.columns
        new_sa = alias_self.sa.join((alias_other.sa), on_clause, isouter=(how != 'inner'), full=(how == 'outer'))
        new_table = VirtualTable((self.engine), new_sa, index=False)
        for col in new_table._coldata:
            pass

        if sort:
            new_table = new_table.sort_index()
        return new_table


class Table(VirtualTable):

    @staticmethod
    def from_df(df, name, metadata=None):
        metadata = sa.MetaData() if metadata is None else metadata
        cols = [sa.Column(col, to_sqlalchemy_type(df[col])) for col in df.columns]
        if df.index.name is not None:
            ix = df.index.to_series()
            cols = [sa.Column((ix.name), (to_sqlalchemy_type(ix)), primary_key=(ix.is_unique))] + cols
        return (
         metadata, (sa.Table)(name, metadata, *cols))

    def __init__(self, engine, table, **kwargs):
        salc = sa.Table(table, (sa.MetaData()), autoload=True, autoload_with=engine)
        (super().__init__)(engine, salc, **kwargs)


class Expression:

    def __init__(self, table, salc, name):
        self.table = table
        self.sa = salc
        self.name = name

    def copy(self, **new_attrs):
        new = copy.copy(self)
        for k, v in new_attrs.items():
            setattr(new, k, v)
        else:
            return new

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, repr(self.sa))

    def __len__--- This code section failed: ---

 L. 740         0  LOAD_FAST                'self'
                2  LOAD_ATTR                table
                4  LOAD_METHOD              connect
                6  CALL_METHOD_0         0  ''
                8  SETUP_WITH           66  'to 66'
               10  STORE_FAST               'conn'

 L. 741        12  LOAD_FAST                'self'
               14  LOAD_ATTR                table
               16  LOAD_METHOD              _select_query
               18  LOAD_GLOBAL              sa
               20  LOAD_ATTR                func
               22  LOAD_METHOD              count
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                sa
               28  CALL_METHOD_1         1  ''
               30  BUILD_LIST_1          1 
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'q'

 L. 742        36  LOAD_FAST                'conn'
               38  LOAD_METHOD              execute
               40  LOAD_FAST                'q'
               42  CALL_METHOD_1         1  ''
               44  LOAD_METHOD              fetchone
               46  CALL_METHOD_0         0  ''
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  POP_BLOCK        
               54  ROT_TWO          
               56  BEGIN_FINALLY    
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  POP_FINALLY           0  ''
               64  RETURN_VALUE     
             66_0  COME_FROM_WITH        8  '8'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 54

    def __iter__--- This code section failed: ---

 L. 744         0  LOAD_FAST                'self'
                2  LOAD_ATTR                table
                4  LOAD_METHOD              connect
                6  CALL_METHOD_0         0  ''
                8  SETUP_WITH           64  'to 64'
               10  STORE_FAST               'conn'

 L. 745        12  LOAD_FAST                'self'
               14  LOAD_ATTR                table
               16  LOAD_METHOD              _select_query
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                sa
               22  BUILD_LIST_1          1 
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'q'

 L. 746        28  LOAD_GLOBAL              iter
               30  LOAD_GENEXPR             '<code_object <genexpr>>'
               32  LOAD_STR                 'Expression.__iter__.<locals>.<genexpr>'
               34  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               36  LOAD_FAST                'conn'
               38  LOAD_METHOD              execute
               40  LOAD_FAST                'q'
               42  CALL_METHOD_1         1  ''
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_1       1  ''
               50  POP_BLOCK        
               52  ROT_TWO          
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM_WITH        8  '8'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 52

    def iteritems--- This code section failed: ---

 L. 748         0  LOAD_FAST                'self'
                2  LOAD_ATTR                table
                4  LOAD_METHOD              connect
                6  CALL_METHOD_0         0  ''
                8  SETUP_WITH          196  'to 196'
               10  STORE_FAST               'conn'

 L. 749        12  LOAD_FAST                'self'
               14  LOAD_ATTR                table
               16  LOAD_ATTR                _ix
               18  POP_JUMP_IF_FALSE   122  'to 122'

 L. 750        20  LOAD_FAST                'self'
               22  LOAD_ATTR                table
               24  LOAD_ATTR                _ixdata
               26  STORE_FAST               'ixs'

 L. 751        28  LOAD_FAST                'self'
               30  LOAD_ATTR                table
               32  LOAD_METHOD              _select_query
               34  LOAD_FAST                'ixs'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                sa
               40  BUILD_LIST_1          1 
               42  BINARY_ADD       
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'q'

 L. 752        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'ixs'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               1
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    86  'to 86'

 L. 753        60  LOAD_GLOBAL              iter
               62  LOAD_FAST                'conn'
               64  LOAD_METHOD              execute
               66  LOAD_FAST                'q'
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  POP_BLOCK        
               74  ROT_TWO          
               76  BEGIN_FINALLY    
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  POP_FINALLY           0  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            58  '58'

 L. 754        86  LOAD_GLOBAL              iter
               88  LOAD_GENEXPR             '<code_object <genexpr>>'
               90  LOAD_STR                 'Expression.iteritems.<locals>.<genexpr>'
               92  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               94  LOAD_FAST                'conn'
               96  LOAD_METHOD              execute
               98  LOAD_FAST                'q'
              100  CALL_METHOD_1         1  ''
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  CALL_FUNCTION_1       1  ''
              108  POP_BLOCK        
              110  ROT_TWO          
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  RETURN_VALUE     
            122_0  COME_FROM            18  '18'

 L. 756       122  LOAD_FAST                'self'
              124  LOAD_ATTR                table
              126  LOAD_ATTR                _from_i
              128  JUMP_IF_TRUE_OR_POP   132  'to 132'
              130  LOAD_CONST               0
            132_0  COME_FROM           128  '128'
              132  STORE_FAST               'from_i'

 L. 757       134  LOAD_FAST                'self'
              136  LOAD_ATTR                table
              138  LOAD_METHOD              _select_query
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                sa
              144  BUILD_LIST_1          1 
              146  CALL_METHOD_1         1  ''
              148  STORE_FAST               'q'

 L. 758       150  LOAD_GLOBAL              iter
              152  LOAD_GENEXPR             '<code_object <genexpr>>'
              154  LOAD_STR                 'Expression.iteritems.<locals>.<genexpr>'
              156  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 759       158  LOAD_GLOBAL              enumerate
              160  LOAD_FAST                'conn'
              162  LOAD_METHOD              execute
              164  LOAD_FAST                'q'
              166  CALL_METHOD_1         1  ''
              168  LOAD_FAST                'from_i'
              170  CALL_FUNCTION_2       2  ''

 L. 758       172  GET_ITER         
              174  CALL_FUNCTION_1       1  ''
              176  CALL_FUNCTION_1       1  ''
              178  POP_BLOCK        
              180  ROT_TWO          
              182  BEGIN_FINALLY    
              184  WITH_CLEANUP_START
              186  WITH_CLEANUP_FINISH
              188  POP_FINALLY           0  ''
              190  RETURN_VALUE     
              192  POP_BLOCK        
              194  BEGIN_FINALLY    
            196_0  COME_FROM_WITH        8  '8'
              196  WITH_CLEANUP_START
              198  WITH_CLEANUP_FINISH
              200  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 74

    def __getitem__(self, k):
        if isinstance(k, slice) or isinstance(k, Expression):
            return self.copy(table=(self.table[k]))
        raise TypeError('unrecognized key type: %s' % type(k))

    def to_series(self):
        tbl = self.table
        vals = []
        ixs = []
        for ix, val in self.iteritems():
            vals.append(val)
            ixs.append(ix)
        else:
            if len(tbl._ix) < 2:
                name = tbl._ix[0] if tbl._ix else None
                ix = pd.Index(ixs, name=name)
            else:
                ix = pd.MultiIndex.from_tuples(ixs, names=(tbl._ix))
            return pd.Series(vals, index=ix, name=(self.name))

    @property
    def data(self):
        return self.to_series()

    @property
    def s(self):
        return self.data

    @property
    def dtype(self):
        return np.dtype(str(discover_typeengine(self.sa.type)))

    @property
    def iloc(self):
        return Indexer(self.islice)

    def _lookup(self, k):
        tbl = self.table
        select = self.copy(table=(tbl.where(tbl.index == k)))
        result = select.s
        if len(result) == 0:
            raise KeyError('%r not found in %s' % (k, tbl.index))
        return result

    def _loc(self, k):
        if isinstance(k, (slice, Expression)):
            return self.copy(table=(self.table._loc(k)))
        if is_iter_notstr(k):
            return pd.concat([self._lookup(el) for el in k])
        result = self._lookup(k)
        if len(result) == 1:
            return result.iloc[0]
        return result

    @property
    def loc(self):
        return Indexer(self._loc)

    def aggregate(self, how, axis=None, skipna=None):
        how = {'mean':'avg',  'std':'stddev',  'var':'variance'}.get(how, how)
        assert axis in {0, None}
        fn = getattr(func, how)
        return self.table.select_row(fn(self.sa))

    def nunique(self, dropna=True):
        return len(self.unique())

    def isnull(self):
        return self == None

    isna = isnull

    def notnull(self):
        return self != None

    notna = notnull

    def sort_values(self, ascending=True):
        assert ascending in {False, True}
        return self.copy(table=self.table.sort_values(self, ascending=ascending))

    def nlargest(self, n=5):
        return self.sort_values(ascending=False).head(n)

    def nsmallest(self, n=5):
        return self.sort_values(ascending=True).head(n)

    def groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, **kwargs):
        return GroupBy(self, by, sort=sort, as_index=as_index)


for opname in ('lt', 'le', 'gt', 'eq', 'ge', 'ne', 'mul', 'add', 'sub', 'truediv',
               'pow', 'and_', 'or_'):
    op = getattr(operator, opname)

    def fn(self, other, op=op):
        if hasattr(other, 'sa'):
            new_sa = op(self.sa, other.sa)
            new_name = self.name if other.name == self.name else None
        else:
            new_sa = op(self.sa, other)
            new_name = self.name
        return Expression(self.table, new_sa, new_name)


    setattr(Expression, '__%s__' % opname.strip('_'), fn)
else:
    for method in ('head', 'tail', 'islice', 'sort_index', 'where'):
        tbl_fn = getattr(Table, method)

        @wraps(tbl_fn)
        def fn(self, *args, tbl_fn=tbl_fn, **kwargs):
            return self.copy(table=tbl_fn(self.table, *args, **kwargs))


        setattr(Expression, method, fn)
    else:
        for sql_func in ('rank', ):
            op = getattr(func, sql_func)

            def fn(self, op=op):
                return Expression(self.table, op(self.sa), self.name)


            setattr(Expression, sql_func, fn)
        else:
            for sql_method in ('startswith', 'endswith', 'in_'):
                method = getattr(sa.sql.operators.ColumnOperators, sql_method)

                @wraps(method)
                def fn(self, *args, _method=method, **kwargs):
                    return Expression(self.table, _method(self.sa, *args, **kwargs), self.name)


                setattr(Expression, sql_method, fn)
            else:
                for sql_method in ('distinct', ):
                    method = getattr(sa.sql.operators.ColumnOperators, sql_method)

                    @wraps(method)
                    def fn(self, *args, _method=method, **kwargs):
                        return Expression(self.table.reset_index(), _method(self.sa, *args, **kwargs), self.name)


                    setattr(Expression, sql_method, fn)
                else:
                    Expression.isin = Expression.in_
                    Expression.unique = Expression.distinct

                    class Indexer:

                        def __init__(self, getter, setter=None):
                            self.getter = getter
                            self.setter = setter

                        def __getitem__(self, k):
                            return self.getter(k)


                    class GroupBy:

                        def __init__(self, base, by, sort=True, as_index=True):
                            assert isinstance(base, (Table, Expression))
                            self.base = base
                            if isinstance(by, (str, Expression)):
                                by = [
                                 by]
                            self.by = [base[k] if isinstance(k, str) else k for k in by]
                            self.sort = sort
                            self.as_index = as_index

                        def __getitem__(self, k):
                            if isinstance(self.base, Table):
                                if isinstance(k, str) or is_striter(k):
                                    return GroupBy(self.base[k], self.by)
                            raise TypeError('unrecognized key type %s for groupby base type %s' % (
                             type(k), type(self.base)))

                        @property
                        def table(self):
                            if isinstance(self.base, Table):
                                return self.base
                            return self.base.table

                        def get_group(self, group):
                            singleton = len(self.by) == 1
                            if singleton:
                                group = isinstance(group, str) or isinstance(group, Iterable) or [
                                 group]
                            condition = and_(*[by_el == group_el for by_el, group_el in zip(self.by, group)])
                            return self.base.where(condition)

                        @property
                        def groups--- This code section failed: ---

 L. 912         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'GroupBy.groups.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                by
               10  GET_ITER         
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'by'

 L. 913        16  LOAD_GLOBAL              len
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                by
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               1
               26  COMPARE_OP               ==
               28  STORE_DEREF              'singleton'

 L. 914        30  LOAD_GLOBAL              list
               32  LOAD_DEREF               'self'
               34  LOAD_ATTR                table
               36  LOAD_ATTR                iterselect
               38  LOAD_FAST                'by'
               40  LOAD_FAST                'by'
               42  LOAD_CONST               ('groupby',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'groups'

 L. 915        50  LOAD_CLOSURE             'self'
               52  LOAD_CLOSURE             'singleton'
               54  BUILD_TUPLE_2         2 
               56  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               58  LOAD_STR                 'GroupBy.groups.<locals>.<dictcomp>'
               60  MAKE_FUNCTION_8          'closure'

 L. 917        62  LOAD_FAST                'groups'

 L. 915        64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 56

                        def __len__--- This code section failed: ---

 L. 920         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'GroupBy.__len__.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                by
               10  GET_ITER         
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'by'

 L. 921        16  LOAD_FAST                'self'
               18  LOAD_ATTR                table
               20  LOAD_ATTR                _select_query
               22  LOAD_FAST                'by'
               24  LOAD_FAST                'by'
               26  LOAD_CONST               ('groupby',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  LOAD_METHOD              count
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'q'

 L. 922        36  LOAD_FAST                'self'
               38  LOAD_ATTR                table
               40  LOAD_METHOD              connect
               42  CALL_METHOD_0         0  ''
               44  SETUP_WITH           78  'to 78'
               46  STORE_FAST               'conn'

 L. 923        48  LOAD_FAST                'conn'
               50  LOAD_METHOD              execute
               52  LOAD_FAST                'q'
               54  CALL_METHOD_1         1  ''
               56  LOAD_METHOD              fetchone
               58  CALL_METHOD_0         0  ''
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  POP_BLOCK        
               66  ROT_TWO          
               68  BEGIN_FINALLY    
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  POP_FINALLY           0  ''
               76  RETURN_VALUE     
             78_0  COME_FROM_WITH       44  '44'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 66

                        def __iter__(self):
                            by = [by.sa for by in self.by]
                            singleton = len(self.by) == 1
                            sort_by = self.by if self.sort else None
                            for group in self.table.iterselect(by, groupby=by, sort_by=sort_by):
                                condition = and_(*[by_el == group_el for by_el, group_el in zip(self.by, group)])
                                (yield (group[0] if singleton else group, self.base.where(condition)))

                        def apply(self, func, *args, **kwargs):
                            return pd.concat([func(data.data, *args, **kwargs) for _, data in self])

                        def transform(self, func, *args, **kwargs):
                            return pd.concat([func(data.data, *args, **kwargs) for _, data in self])

                        def size(self):
                            bynames = [by.name for by in self.by]
                            by = [by.sa for by in self.by]
                            vals = []
                            ixs = []
                            for row in self.table.iterselect((by + [sa.func.count()]), groupby=by):
                                vals.append(row[(-1)])
                                ixs.append(row[:-1])
                            else:
                                if len(bynames) < 2:
                                    ix = pd.Index(ixs, name=(bynames[0]))
                                else:
                                    ix = pd.MultiIndex.from_tuples(ixs, names=bynames)
                                return pd.Series(vals, index=ix)

                        def aggregate(self, how, as_df=True):
                            how = {'mean':'avg', 
                             'std':'stddev',  'var':'variance'}.get(how, how)
                            valid_types = _numeric_types if how in {'stddev', 'sum', 'variance', 'avg'} else sa_types
                            fn = getattr(func, how)
                            by = [by.sa for by in self.by]
                            bynames = [by.name for by in self.by]
                            if isinstance(self.base, Table):
                                colnames = [col for col, dtype in zip(self.base.columns, self.base.coltypes) if dtype in valid_types if col not in bynames]
                                salc = [by.sa for by in self.by] + [fn(self.base[col].sa) for col in colnames]
                            else:
                                colnames = [
                                 self.base.name]
                                salc = [by.sa for by in self.by] + [fn(self.base.sa)]
                            ix = self.by if self.as_index else None
                            sort_by = self.by if self.sort else None
                            new_q = as_df or self.table._select_query(salc, groupby=by, sort_by=sort_by)
                            new_sa = new_q
                            vt = VirtualTable(self.table.engine, new_sa)
                            vt._ixdata, vt._coldata = vt._coldata[:len(bynames)], vt._coldata[len(bynames):]
                            vt._ix, vt._columns = bynames, colnames
                            if not self.as_index:
                                vt = vt.reset_index()[(bynames + colnames)]
                            else:
                                return vt
                                df = pd.DataFrame.from_records((list(self.table.iterselect(salc, groupby=by, sort_by=sort_by))), columns=(list(range(len(salc)))))
                                if self.as_index:
                                    df.set_index((list(range(len(self.by)))), inplace=True)
                                    df.index.names = bynames
                                    df.columns = colnames
                                else:
                                    df.columns = bynames + colnames
                            if not isinstance(self.base, Table):
                                if self.as_index:
                                    return df[colnames[0]]
                            return df

                        agg = aggregate


                    for agg_fn in ('min', 'max', 'mean', 'sum', 'std', 'var', 'count'):

                        def wrapped(self, axis=None, skipna=None, how=agg_fn):
                            return self.aggregate(how, axis=axis, skipna=skipna)


                        wrapped.__name__ = agg_fn
                        setattr(Table, agg_fn, wrapped)
                        setattr(Expression, agg_fn, wrapped)
                        setattr(GroupBy, agg_fn, partialmethod((GroupBy.aggregate), how=agg_fn))
                    else:
                        for pair_agg_fn in ('corr', 'cov'):

                            def wrapped(self, how=pair_agg_fn):
                                return self._agg_pairwise(how)


                            wrapped.__name__ = pair_agg_fn
                            setattr(Table, pair_agg_fn, wrapped)