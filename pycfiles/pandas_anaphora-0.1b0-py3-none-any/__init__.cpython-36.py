# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\GMWERB\software\pandas-anaphora\anaphora\__init__.py
# Compiled at: 2018-11-10 02:24:02
# Size of source mod 2**32: 11426 bytes
""" Anaphora for Pandas DataFrame columns (because writing `lambda x:` sucks)

Inspired by the Spark/PySpark dataframe API, with a wistful eye towards Dplyr in R...

Tested with:
- Python 3.6 (should work with 3.5 and probably 3.4)
- Pandas 0.23 (will probably not work in older versions, maybe >= 0.20 is fine)

Example:
    import pandas as pd
    from pandas_anaphora import register_anaphora, Col
    register_anaphora_methods()

    data = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]}, index=['this', 'that', 'other'])

    # the old way
    data1 = data.copy()
    b_above_4 = data1['b'] > 4
    data1.loc[b_above_4, 'x'] = data1.loc[b_above_4, 'a']
    a_is_3 = data1['a']
    data1.loc[a_is_3, 'a'] = 300
    data1.at['this', 'b'] = -data1.at['this', 'b']

    # the new way
    data2 = data1        .with_column('x', Col('b') > 4)        .with_column('a', 300, loc=Col() == 3)        .with_column('b', -Col('b').loc['this'])

    pd.testing.assert_frame_equal(data1, data2)
"""
import operator as op
try:
    import cytoolz as tz
except ImportError:
    import toolz as tz

import pandas as pd
__all__ = ('anaphora_register_methods', 'Col', 'with_column', 'mutate', 'mutate_sequential')

def anaphora_register_methods(include=(), exclude=()):
    """ Register functions as Pandas object methods

    Registered methods:
    - anaphora.with_column -> pandas.DataFrame.with_column
    - anaphora.mutate -> pandas.DataFrame.mutate
    """
    methods = {'with_column':with_column, 
     'mutate':mutate}
    if not include:
        include = set(methods.keys())
    exclude = set(exclude)
    whitelist = include - exclude
    for name, method in methods.items():
        if name in whitelist:
            setattr(pd.DataFrame, name, method)


def _error_unknown_option(key):
    return KeyError('Unknown option: {}'.format(key))


def _error_mutually_exclusive_kwargs(keys):
    pretty_key_list = ', '.join(map("'{]'".format, subset_types.keys()))
    return ValueError('Arguments are mutually exclusive: {}'.format(pretty_key_list))


class ColType(type):
    __doc__ = ' Metaclass for Col objects\n\n    Used to explicitly whitelist dunder methods, which are blacklisted by the custom ``Col.__getattr__``. Also,\n    Python "magic method" lookup skips both ``__getattr__`` and ``__getattributes__``, and instead looks directly\n    on the class. So dunders need to be explicitly present on the class to be recognized by Python. E.g. in\n    ``Col(\'y\') + 1``, Python skips both ``Col.__getattributes__(\'add\')`` and ``Col.__getattr__(\'add\')``; it just\n    looks for ``Col.__add__``. See https://docs.python.org/3.7/reference/datamodel.html#special-lookup\n    '

    class GetterPusher:

        def __init__(self, name=None):
            self.name = name

        def __set_name__(self, cls, name):
            self.name = name

        def __get__(self, col_obj, cls):
            self.col = col_obj
            return self

    class SeriesAttr(GetterPusher):

        def __call__(self, *args, **kwargs):
            self.col.push((op.attrgetter)(self.name, *args, **kwargs))
            return self.col

    class SeriesMethod(GetterPusher):

        def __call__(self, *args, **kwargs):
            self.col.push((op.methodcaller)(self.name, *args, **kwargs))
            return self.col

    dunder_whitelist = {'__add__':op.add, 
     '__xor__':op.xor, 
     '__lt__':op.lt, 
     '__le__':op.le, 
     '__eq__':op.eq, 
     '__ne__':op.ne, 
     '__gt__':op.gt, 
     '__ge__':op.ge, 
     '__add__':op.add, 
     '__sub__':op.sub, 
     '__mul__':op.mul, 
     '__matmul__':op.matmul, 
     '__truediv__':op.truediv, 
     '__floordiv__':op.floordiv, 
     '__mod__':op.mod, 
     '__divmod__':None, 
     '__pow__':op.pow, 
     '__lshift__':op.lshift, 
     '__rshift__':None, 
     '__and__':op.and_, 
     '__xor__':op.xor, 
     '__or__':op.or_, 
     '__radd__':None, 
     '__rsub__':None, 
     '__rmul__':None, 
     '__rmatmul__':None, 
     '__rtruediv__':None, 
     '__rfloordiv__':None, 
     '__rmod__':None, 
     '__rdivmod__':None, 
     '__rpow__':None, 
     '__rlshift__':None, 
     '__rrshift__':None, 
     '__rand__':None, 
     '__rxor__':None, 
     '__ror__':None, 
     '__iadd__':op.iadd, 
     '__isub__':op.isub, 
     '__imul__':op.imul, 
     '__imatmul__':op.imatmul, 
     '__itruediv__':op.itruediv, 
     '__ifloordiv__':op.ifloordiv, 
     '__imod__':op.imod, 
     '__idivmod__':None, 
     '__ipow__':op.ipow, 
     '__ilshift__':op.ilshift, 
     '__irshift__':op.irshift, 
     '__iand__':op.iand, 
     '__ixor__':op.ixor, 
     '__ior__':op.ior, 
     '__neg__':op.neg, 
     '__pos__':op.pos, 
     '__abs__':abs, 
     '__invert__':op.invert, 
     '__round__':round}

    def __new__(meta, name, bases, attrs):
        cls = super().__new__(meta, name, bases, attrs)
        for name, fn in meta.dunder_whitelist.items():
            setattr(cls, name, meta.SeriesMethod(name))

        return cls


class Col(metaclass=ColType):
    __doc__ = " A proxy for a Series in a DataFrame\n\n    Example:\n        import pandas as pd\n        from pandas_anaphora import Col\n\n        data = pd.DataFrame(\n        add_one_to_y = Col('y') + 1\n        pd.testing.assert_series_equal(\n            data['y'] + 1,\n            add_one_to_y(data)\n        )\n    "

    class SeriesIndexer(ColType.GetterPusher):

        def __getitem__(self, *args):

            def get_index(x):
                return getattr(x, self.name)[args]

            self.col.push(get_index)
            return self.col

    loc = SeriesIndexer()
    iloc = SeriesIndexer()

    class _MethodArgCollector:

        def __init__(self, col, name):
            self.col = col
            self.name = name

        def __call__(self, *args, **kwargs):
            self.col.push((op.methodcaller)(self.name, *args, **kwargs))
            return self.col

    def __getattr__(self, name):
        method_or_attr = getattr(pd.Series, name)
        if name.startswith('_'):
            raise AttributeError('Attribute/method access not implemented for pd.Series.{}'.format(name))
        if callable(method_or_attr):
            return Col._MethodArgCollector(self, name)
        else:
            self.push(op.attrgetter(name))
            return self

    def __init__(self, spec=None):
        self.spec = spec
        self.fns = []

    def __repr__(self):
        return 'Col({})'.format(repr(self.spec))

    def push(self, fn):
        self.fns.append(fn)

    def compute(self, df):
        if isinstance(df, pd.Series):
            col = df.loc[self.spec]
        else:
            col = df.loc[:, self.spec]
        if not self.fns:
            return col
        else:
            return (tz.compose)(*reversed(self.fns))(col)

    def __call__(self, df):
        return self.compute(df)


def _apply_col(df, colname, val):
    if callable(val):
        if isinstance(val, Col):
            if val.spec is None:
                val.spec = colname
        return val(df)
    else:
        return val


def with_column(df, colname, fn, loc=None, iloc=None, copy=True):
    """ Assign a column to a DataFrame """
    if copy:
        df = df.copy()
    else:
        subset_types = {'loc':loc, 
         'iloc':iloc}
        subset_types_given = [key for key, value in subset_types.items() if value is not None]
        n_subset_types_given = len(subset_types_given)
        if n_subset_types_given > 1:
            raise _error_mutally_exclusive_kwargs(subset_types_given)
        else:
            if n_subset_types_given == 0:
                subset_types_given.append('loc')
                subset_types['loc'] = slice(None)
        subset_type = subset_types_given[0]
        subset_value = subset_types[subset_type]
        subset_value = _apply_col(df, colname, subset_value)
        if subset_type == 'loc':
            df.loc[(subset_value, colname)] = _apply_col(df.loc[subset_value], colname, fn)
        else:
            df.loc[(df.index[subset_value], colname)] = _apply_col(df.iloc[subset_value], colname, fn)
    return df


def _mutate_impl(df, mutations, sequential=False):
    df = df.copy()
    if sequential:
        newdf = df
    else:
        newdf = df.copy()
    for name, val in mutations.items():
        newdf[name] = _apply_col(df, name, val)

    return newdf


def mutate(df, **mutations):
    """ Like dplyr::mutate in R

    DOES NOT allow access to LHS from the RHS

    Example:
        df = pd.DataFrame({'y': [1,2,3]})
        mutate(df, x=Col('y')*10)
    """
    return _mutate_impl(df, mutations, sequential=False)


def mutate_sequential(df, **mutations):
    """ Like dplyr::mutate in R with evil powers

    DOES allow access to LHS from the RHS

    Example:
        df = pd.DataFrame({'y': [1,2,3]})
        mutate(df, x=Col('y')*10, y=Col('x')+1)
    """
    return _mutate_impl(df, mutations, sequential=True)