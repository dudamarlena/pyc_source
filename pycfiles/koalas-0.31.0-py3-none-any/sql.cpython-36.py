# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/sql.py
# Compiled at: 2019-09-06 16:01:33
# Size of source mod 2**32: 9752 bytes
import _string
from typing import Dict, Any, Optional
import inspect, pandas as pd
from pyspark.sql import SparkSession, DataFrame as SDataFrame
from databricks import koalas as ks
from databricks.koalas.utils import default_session
from databricks.koalas.frame import DataFrame
from databricks.koalas.series import Series
__all__ = [
 'sql']
from builtins import globals as builtin_globals
from builtins import locals as builtin_locals

def sql(query: str, globals=None, locals=None, **kwargs) -> DataFrame:
    """
    Execute a SQL query and return the result as a Koalas DataFrame.

    This function also supports embedding Python variables (locals, globals, and parameters)
    in the SQL statement by wrapping them in curly braces. See examples section for details.

    In addition to the locals, globals and parameters, the function will also attempt
    to determine if the program currently runs in an IPython (or Jupyter) environment
    and to import the variables from this environment. The variables have the same
    precedence as globals.

    The following variable types are supported:

    - string
    - int
    - float
    - list, tuple, range of above types
    - Koalas DataFrame
    - Koalas Series
    - pandas DataFrame

    Parameters
    ----------
    query : str
        the SQL query
    globals : dict, optional
        the dictionary of global variables, if explicitly set by the user
    locals : dict, optional
        the dictionary of local variables, if explicitly set by the user
    kwargs
        other variables that the user may want to set manually that can be referenced in the query

    Returns
    -------
    Koalas DataFrame

    Examples
    --------

    Calling a built-in SQL function.

    >>> ks.sql("select * from range(10) where id > 7")
       id
    0   8
    1   9

    A query can also reference a local variable or parameter by wrapping them in curly braces:

    >>> bound1 = 7
    >>> ks.sql("select * from range(10) where id > {bound1} and id < {bound2}", bound2=9)
       id
    0   8

    You can also wrap a DataFrame with curly braces to query it directly. Note that when you do
    that, the indexes, if any, automatically become top level columns.

    >>> mydf = ks.range(10)
    >>> x = range(4)
    >>> ks.sql("SELECT * from {mydf} WHERE id IN {x}")
       id
    0   0
    1   1
    2   2
    3   3

    Queries can also be arbitrarily nested in functions:

    >>> def statement():
    ...     mydf2 = ks.DataFrame({"x": range(2)})
    ...     return ks.sql("SELECT * from {mydf2}")
    >>> statement()
       x
    0  0
    1  1

    Mixing Koalas and pandas DataFrames in a join operation. Note that the index is dropped.

    >>> ks.sql('''
    ...   SELECT m1.a, m2.b
    ...   FROM {table1} m1 INNER JOIN {table2} m2
    ...   ON m1.key = m2.key
    ...   ORDER BY m1.a, m2.b''',
    ...   table1=ks.DataFrame({"a": [1,2], "key": ["a", "b"]}),
    ...   table2=pd.DataFrame({"b": [3,4,5], "key": ["a", "b", "b"]}))
       a  b
    0  1  3
    1  2  4
    2  2  5

    Also, it is possible to query using Series.

    >>> myser = ks.Series({'a': [1.0, 2.0, 3.0], 'b': [15.0, 30.0, 45.0]})
    >>> ks.sql("SELECT * from {myser}")
                        0
    0     [1.0, 2.0, 3.0]
    1  [15.0, 30.0, 45.0]
    """
    if globals is None:
        globals = _get_ipython_scope()
    _globals = builtin_globals() if globals is None else dict(globals)
    _locals = builtin_locals() if locals is None else dict(locals)
    _dict = dict(_globals)
    _scope = _get_local_scope()
    _dict.update(_scope)
    _dict.update(_locals)
    _dict.update(kwargs)
    return SQLProcessor(_dict, query, default_session()).execute()


_CAPTURE_SCOPES = 2

def _get_local_scope():
    try:
        return inspect.stack()[_CAPTURE_SCOPES][0].f_locals
    except Exception as e:
        return {}


def _get_ipython_scope():
    """
    Tries to extract the dictionary of variables if the program is running
    in an IPython notebook environment.
    """
    try:
        from IPython import get_ipython
        shell = get_ipython()
        return shell.user_ns
    except Exception as e:
        return


_escape_table = [chr(x) for x in range(128)]
_escape_table[0] = '\\0'
_escape_table[ord('\\')] = '\\\\'
_escape_table[ord('\n')] = '\\n'
_escape_table[ord('\r')] = '\\r'
_escape_table[ord('\x1a')] = '\\Z'
_escape_table[ord('"')] = '\\"'
_escape_table[ord("'")] = "\\'"

def escape_sql_string(value: str) -> str:
    r"""Escapes value without adding quotes.

    >>> escape_sql_string("foo\nbar")
    'foo\\nbar'

    >>> escape_sql_string("'abc'de")
    "\\'abc\\'de"

    >>> escape_sql_string('"abc"de')
    '\\"abc\\"de'
    """
    return value.translate(_escape_table)


class SQLProcessor(object):

    def __init__(self, scope: Dict[(str, Any)], statement: str, session: SparkSession):
        self._scope = scope
        self._statement = statement
        self._temp_views = {}
        self._cached_vars = {}
        self._normalized_statement = None
        self._session = session

    def execute(self) -> DataFrame:
        """
        Returns a DataFrame for which the SQL statement has been executed by
        the underlying SQL engine.

        >>> str0 = 'abc'
        >>> ks.sql("select {str0}")
           abc
        0  abc

        >>> str1 = 'abc"abc'
        >>> str2 = "abc'abc"
        >>> ks.sql("select {str0}, {str1}, {str2}")
           abc  abc"abc  abc'abc
        0  abc  abc"abc  abc'abc

        >>> strs = ['a', 'b']
        >>> ks.sql("select 'a' in {strs} as cond1, 'c' in {strs} as cond2")
           cond1  cond2
        0   True  False
        """
        blocks = _string.formatter_parser(self._statement)
        res = ''
        try:
            for pre, inner, _, _ in blocks:
                var_next = '' if inner is None else self._convert(inner)
                res = res + pre + var_next

            self._normalized_statement = res
            sdf = self._session.sql(self._normalized_statement)
        finally:
            for v in self._temp_views:
                self._session.catalog.dropTempView(v)

        return DataFrame(sdf)

    def _convert(self, key) -> Any:
        """
        Given a {} key, returns an equivalent SQL representation.
        This conversion performs all the necessary escaping so that the string
        returned can be directly injected into the SQL statement.
        """
        if key in self._cached_vars:
            return self._cached_vars[key]
        else:
            if key not in self._scope:
                raise ValueError('The key {} in the SQL statement was not found in global, local or parameters variables'.format(key))
            var = self._scope[key]
            fillin = self._convert_var(var)
            self._cached_vars[key] = fillin
            return fillin

    def _convert_var(self, var) -> Any:
        """
        Converts a python object into a string that is legal SQL.
        """
        if isinstance(var, (int, float)):
            return str(var)
        else:
            if isinstance(var, Series):
                return self._convert_var(var.to_dataframe())
            else:
                if isinstance(var, pd.DataFrame):
                    return self._convert_var(ks.DataFrame(var))
                else:
                    if isinstance(var, DataFrame):
                        df_id = 'koalas_' + str(id(var))
                        if df_id not in self._temp_views:
                            sdf = var.to_spark()
                            sdf.createOrReplaceTempView(df_id)
                            self._temp_views[df_id] = sdf
                        return df_id
                    if isinstance(var, str):
                        return '"' + escape_sql_string(var) + '"'
                if isinstance(var, list):
                    return '(' + ', '.join([self._convert_var(v) for v in var]) + ')'
            if isinstance(var, (tuple, range)):
                return self._convert_var(list(var))
        raise ValueError('Unsupported variable type {}: {}'.format(type(var), str(var)))