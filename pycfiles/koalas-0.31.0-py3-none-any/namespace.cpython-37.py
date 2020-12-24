# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/namespace.py
# Compiled at: 2020-04-01 14:53:32
# Size of source mod 2**32: 80377 bytes
"""
Wrappers around spark that correspond to common pandas functions.
"""
from typing import Optional, Union, List, Tuple, Dict
from collections import OrderedDict
from collections.abc import Iterable
from functools import reduce
import itertools, numpy as np, pandas as pd
from pandas.api.types import is_list_like
from pyspark import sql as spark
import pyspark.sql as F
from pyspark.sql.types import ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType, BooleanType, TimestampType, DecimalType, StringType, DateType, StructType
from databricks import koalas as ks
from databricks.koalas.base import IndexOpsMixin
from databricks.koalas.utils import default_session, name_like_string, scol_for, validate_axis, align_diff_frames
from databricks.koalas.frame import DataFrame, _reduce_spark_multi
from databricks.koalas.internal import _InternalFrame
from databricks.koalas.typedef import pandas_wraps
from databricks.koalas.series import Series, _col
__all__ = [
 'from_pandas',
 'range',
 'read_csv',
 'read_delta',
 'read_table',
 'read_spark_io',
 'read_parquet',
 'read_clipboard',
 'read_excel',
 'read_html',
 'to_datetime',
 'get_dummies',
 'concat',
 'melt',
 'isna',
 'isnull',
 'notna',
 'notnull',
 'read_sql_table',
 'read_sql_query',
 'read_sql',
 'read_json',
 'merge',
 'to_numeric',
 'broadcast']

def from_pandas(pobj: Union[('pd.DataFrame', 'pd.Series')]) -> Union[('Series', 'DataFrame')]:
    """Create a Koalas DataFrame or Series from a pandas DataFrame or Series.

    This is similar to Spark's `SparkSession.createDataFrame()` with pandas DataFrame,
    but this also works with pandas Series and picks the index.

    Parameters
    ----------
    pobj : pandas.DataFrame or pandas.Series
        pandas DataFrame or Series to read.

    Returns
    -------
    Series or DataFrame
        If a pandas Series is passed in, this function returns a Koalas Series.
        If a pandas DataFrame is passed in, this function returns a Koalas DataFrame.
    """
    if isinstance(pobj, pd.Series):
        return Series(pobj)
    if isinstance(pobj, pd.DataFrame):
        return DataFrame(pobj)
    if isinstance(pobj, pd.Index):
        return DataFrame(pd.DataFrame(index=pobj)).index
    raise ValueError('Unknown data type: {}'.format(type(pobj)))


_range = range

def range(start: int, end: Optional[int]=None, step: int=1, num_partitions: Optional[int]=None) -> DataFrame:
    """
    Create a DataFrame with some range of numbers.

    The resulting DataFrame has a single int64 column named `id`, containing elements in a range
    from ``start`` to ``end`` (exclusive) with step value ``step``. If only the first parameter
    (i.e. start) is specified, we treat it as the end value with the start value being 0.

    This is similar to the range function in SparkSession and is used primarily for testing.

    Parameters
    ----------
    start : int
        the start value (inclusive)
    end : int, optional
        the end value (exclusive)
    step : int, optional, default 1
        the incremental step
    num_partitions : int, optional
        the number of partitions of the DataFrame

    Returns
    -------
    DataFrame

    Examples
    --------
    When the first parameter is specified, we generate a range of values up till that number.

    >>> ks.range(5)
       id
    0   0
    1   1
    2   2
    3   3
    4   4

    When start, end, and step are specified:

    >>> ks.range(start = 100, end = 200, step = 20)
        id
    0  100
    1  120
    2  140
    3  160
    4  180
    """
    sdf = default_session().range(start=start, end=end, step=step, numPartitions=num_partitions)
    return DataFrame(sdf)


def read_csv--- This code section failed: ---

 L. 252         0  LOAD_FAST                'mangle_dupe_cols'
                2  LOAD_CONST               True
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 253         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'mangle_dupe_cols can only be `True`: %s'
               12  LOAD_FAST                'mangle_dupe_cols'
               14  BINARY_MODULO    
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             6  '6'

 L. 254        20  LOAD_FAST                'parse_dates'
               22  LOAD_CONST               False
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 255        28  LOAD_GLOBAL              ValueError
               30  LOAD_STR                 'parse_dates can only be `False`: %s'
               32  LOAD_FAST                'parse_dates'
               34  BINARY_MODULO    
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            26  '26'

 L. 257        40  LOAD_DEREF               'usecols'
               42  LOAD_CONST               None
               44  COMPARE_OP               is-not
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_GLOBAL              callable
               50  LOAD_DEREF               'usecols'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     64  'to 64'

 L. 258        56  LOAD_GLOBAL              list
               58  LOAD_DEREF               'usecols'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  STORE_DEREF              'usecols'
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            46  '46'

 L. 259        64  LOAD_DEREF               'usecols'
               66  LOAD_CONST               None
               68  COMPARE_OP               is
               70  POP_JUMP_IF_TRUE     94  'to 94'
               72  LOAD_GLOBAL              callable
               74  LOAD_DEREF               'usecols'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_JUMP_IF_TRUE     94  'to 94'
               80  LOAD_GLOBAL              len
               82  LOAD_DEREF               'usecols'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  LOAD_CONST               0
               88  COMPARE_OP               >
            90_92  POP_JUMP_IF_FALSE   768  'to 768'
             94_0  COME_FROM            78  '78'
             94_1  COME_FROM            70  '70'

 L. 260        94  LOAD_GLOBAL              default_session
               96  CALL_FUNCTION_0       0  '0 positional arguments'
               98  LOAD_ATTR                read
              100  STORE_FAST               'reader'

 L. 261       102  LOAD_FAST                'reader'
              104  LOAD_METHOD              option
              106  LOAD_STR                 'inferSchema'
              108  LOAD_CONST               True
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  POP_TOP          

 L. 262       114  LOAD_FAST                'reader'
              116  LOAD_METHOD              option
              118  LOAD_STR                 'sep'
              120  LOAD_FAST                'sep'
              122  CALL_METHOD_2         2  '2 positional arguments'
              124  POP_TOP          

 L. 264       126  LOAD_FAST                'header'
              128  LOAD_STR                 'infer'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   150  'to 150'

 L. 265       134  LOAD_FAST                'names'
              136  LOAD_CONST               None
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   146  'to 146'
              142  LOAD_CONST               0
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           140  '140'
              146  LOAD_CONST               None
            148_0  COME_FROM           144  '144'
              148  STORE_FAST               'header'
            150_0  COME_FROM           132  '132'

 L. 266       150  LOAD_FAST                'header'
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 267       158  LOAD_FAST                'reader'
              160  LOAD_METHOD              option
              162  LOAD_STR                 'header'
              164  LOAD_CONST               True
              166  CALL_METHOD_2         2  '2 positional arguments'
              168  POP_TOP          
              170  JUMP_FORWARD        208  'to 208'
            172_0  COME_FROM           156  '156'

 L. 268       172  LOAD_FAST                'header'
              174  LOAD_CONST               None
              176  COMPARE_OP               is
              178  POP_JUMP_IF_FALSE   194  'to 194'

 L. 269       180  LOAD_FAST                'reader'
              182  LOAD_METHOD              option
              184  LOAD_STR                 'header'
              186  LOAD_CONST               False
              188  CALL_METHOD_2         2  '2 positional arguments'
              190  POP_TOP          
              192  JUMP_FORWARD        208  'to 208'
            194_0  COME_FROM           178  '178'

 L. 271       194  LOAD_GLOBAL              ValueError
              196  LOAD_STR                 'Unknown header argument {}'
              198  LOAD_METHOD              format
              200  LOAD_FAST                'header'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  RAISE_VARARGS_1       1  'exception instance'
            208_0  COME_FROM           192  '192'
            208_1  COME_FROM           170  '170'

 L. 273       208  LOAD_FAST                'quotechar'
              210  LOAD_CONST               None
              212  COMPARE_OP               is-not
              214  POP_JUMP_IF_FALSE   228  'to 228'

 L. 274       216  LOAD_FAST                'reader'
              218  LOAD_METHOD              option
              220  LOAD_STR                 'quote'
              222  LOAD_FAST                'quotechar'
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  POP_TOP          
            228_0  COME_FROM           214  '214'

 L. 275       228  LOAD_FAST                'escapechar'
              230  LOAD_CONST               None
              232  COMPARE_OP               is-not
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L. 276       236  LOAD_FAST                'reader'
              238  LOAD_METHOD              option
              240  LOAD_STR                 'escape'
              242  LOAD_FAST                'escapechar'
              244  CALL_METHOD_2         2  '2 positional arguments'
              246  POP_TOP          
            248_0  COME_FROM           234  '234'

 L. 278       248  LOAD_FAST                'comment'
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   304  'to 304'

 L. 279       258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'comment'
              262  LOAD_GLOBAL              str
              264  CALL_FUNCTION_2       2  '2 positional arguments'
          266_268  POP_JUMP_IF_FALSE   284  'to 284'
              270  LOAD_GLOBAL              len
              272  LOAD_FAST                'comment'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  LOAD_CONST               1
              278  COMPARE_OP               !=
          280_282  POP_JUMP_IF_FALSE   292  'to 292'
            284_0  COME_FROM           266  '266'

 L. 280       284  LOAD_GLOBAL              ValueError
              286  LOAD_STR                 'Only length-1 comment characters supported'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  RAISE_VARARGS_1       1  'exception instance'
            292_0  COME_FROM           280  '280'

 L. 281       292  LOAD_FAST                'reader'
              294  LOAD_METHOD              option
              296  LOAD_STR                 'comment'
              298  LOAD_FAST                'comment'
              300  CALL_METHOD_2         2  '2 positional arguments'
              302  POP_TOP          
            304_0  COME_FROM           254  '254'

 L. 283       304  LOAD_FAST                'reader'
              306  LOAD_ATTR                options
              308  BUILD_TUPLE_0         0 
              310  LOAD_FAST                'options'
              312  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              314  POP_TOP          

 L. 285       316  LOAD_GLOBAL              isinstance
              318  LOAD_FAST                'names'
              320  LOAD_GLOBAL              str
              322  CALL_FUNCTION_2       2  '2 positional arguments'
          324_326  POP_JUMP_IF_FALSE   346  'to 346'

 L. 286       328  LOAD_FAST                'reader'
              330  LOAD_METHOD              schema
              332  LOAD_FAST                'names'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  LOAD_METHOD              csv
              338  LOAD_FAST                'path'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  STORE_DEREF              'sdf'
              344  JUMP_FORWARD        392  'to 392'
            346_0  COME_FROM           324  '324'

 L. 288       346  LOAD_FAST                'reader'
              348  LOAD_METHOD              csv
              350  LOAD_FAST                'path'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  STORE_DEREF              'sdf'

 L. 289       356  LOAD_FAST                'header'
              358  LOAD_CONST               None
              360  COMPARE_OP               is
          362_364  POP_JUMP_IF_FALSE   392  'to 392'

 L. 290       366  LOAD_DEREF               'sdf'
              368  LOAD_ATTR                selectExpr

 L. 291       370  LOAD_LISTCOMP            '<code_object <listcomp>>'
              372  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              374  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              376  LOAD_GLOBAL              enumerate
              378  LOAD_DEREF               'sdf'
              380  LOAD_ATTR                schema
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  GET_ITER         
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  CALL_FUNCTION_EX      0  'positional arguments only'
              390  STORE_DEREF              'sdf'
            392_0  COME_FROM           362  '362'
            392_1  COME_FROM           344  '344'

 L. 293       392  LOAD_GLOBAL              isinstance
              394  LOAD_FAST                'names'
              396  LOAD_GLOBAL              list
              398  CALL_FUNCTION_2       2  '2 positional arguments'
          400_402  POP_JUMP_IF_FALSE   516  'to 516'

 L. 294       404  LOAD_GLOBAL              list
              406  LOAD_FAST                'names'
              408  CALL_FUNCTION_1       1  '1 positional argument'
              410  STORE_FAST               'names'

 L. 295       412  LOAD_GLOBAL              len
              414  LOAD_GLOBAL              set
              416  LOAD_FAST                'names'
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  LOAD_GLOBAL              len
              424  LOAD_FAST                'names'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  COMPARE_OP               !=
          430_432  POP_JUMP_IF_FALSE   442  'to 442'

 L. 296       434  LOAD_GLOBAL              ValueError
              436  LOAD_STR                 'Found non-unique column index'
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  RAISE_VARARGS_1       1  'exception instance'
            442_0  COME_FROM           430  '430'

 L. 297       442  LOAD_GLOBAL              len
              444  LOAD_FAST                'names'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  LOAD_GLOBAL              len
              450  LOAD_DEREF               'sdf'
              452  LOAD_ATTR                schema
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  COMPARE_OP               !=
          458_460  POP_JUMP_IF_FALSE   488  'to 488'

 L. 298       462  LOAD_GLOBAL              ValueError

 L. 299       464  LOAD_STR                 'The number of names [%s] does not match the number of columns [%d]. Try names by a Spark SQL DDL-formatted string.'

 L. 301       466  LOAD_GLOBAL              len
              468  LOAD_DEREF               'sdf'
              470  LOAD_ATTR                schema
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  LOAD_GLOBAL              len
              476  LOAD_FAST                'names'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  BUILD_TUPLE_2         2 
              482  BINARY_MODULO    
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  RAISE_VARARGS_1       1  'exception instance'
            488_0  COME_FROM           458  '458'

 L. 303       488  LOAD_DEREF               'sdf'
              490  LOAD_ATTR                selectExpr

 L. 304       492  LOAD_LISTCOMP            '<code_object <listcomp>>'
              494  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              496  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              498  LOAD_GLOBAL              zip
              500  LOAD_DEREF               'sdf'
              502  LOAD_ATTR                schema
              504  LOAD_FAST                'names'
              506  CALL_FUNCTION_2       2  '2 positional arguments'
              508  GET_ITER         
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  CALL_FUNCTION_EX      0  'positional arguments only'
              514  STORE_DEREF              'sdf'
            516_0  COME_FROM           400  '400'

 L. 307       516  LOAD_DEREF               'usecols'
              518  LOAD_CONST               None
              520  COMPARE_OP               is-not
          522_524  POP_JUMP_IF_FALSE   786  'to 786'

 L. 308       526  LOAD_GLOBAL              callable
              528  LOAD_DEREF               'usecols'
              530  CALL_FUNCTION_1       1  '1 positional argument'
          532_534  POP_JUMP_IF_FALSE   562  'to 562'

 L. 309       536  LOAD_CLOSURE             'usecols'
              538  BUILD_TUPLE_1         1 
              540  LOAD_LISTCOMP            '<code_object <listcomp>>'
              542  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              544  MAKE_FUNCTION_8          'closure'
              546  LOAD_DEREF               'sdf'
              548  LOAD_ATTR                schema
              550  GET_ITER         
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  STORE_DEREF              'cols'

 L. 310       556  BUILD_LIST_0          0 
              558  STORE_FAST               'missing'
              560  JUMP_FORWARD        696  'to 696'
            562_0  COME_FROM           532  '532'

 L. 311       562  LOAD_GLOBAL              all
              564  LOAD_GENEXPR             '<code_object <genexpr>>'
              566  LOAD_STR                 'read_csv.<locals>.<genexpr>'
              568  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              570  LOAD_DEREF               'usecols'
              572  GET_ITER         
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  CALL_FUNCTION_1       1  '1 positional argument'
          578_580  POP_JUMP_IF_FALSE   628  'to 628'

 L. 312       582  LOAD_CLOSURE             'usecols'
              584  BUILD_TUPLE_1         1 
              586  LOAD_LISTCOMP            '<code_object <listcomp>>'
              588  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              590  MAKE_FUNCTION_8          'closure'
              592  LOAD_GLOBAL              enumerate
              594  LOAD_DEREF               'sdf'
              596  LOAD_ATTR                schema
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  GET_ITER         
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  STORE_DEREF              'cols'

 L. 314       606  LOAD_CLOSURE             'cols'
              608  LOAD_CLOSURE             'sdf'
              610  BUILD_TUPLE_2         2 
              612  LOAD_LISTCOMP            '<code_object <listcomp>>'
              614  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              616  MAKE_FUNCTION_8          'closure'

 L. 315       618  LOAD_DEREF               'usecols'
              620  GET_ITER         
              622  CALL_FUNCTION_1       1  '1 positional argument'
              624  STORE_FAST               'missing'
              626  JUMP_FORWARD        696  'to 696'
            628_0  COME_FROM           578  '578'

 L. 318       628  LOAD_GLOBAL              all
              630  LOAD_GENEXPR             '<code_object <genexpr>>'
              632  LOAD_STR                 'read_csv.<locals>.<genexpr>'
              634  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              636  LOAD_DEREF               'usecols'
              638  GET_ITER         
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  CALL_FUNCTION_1       1  '1 positional argument'
          644_646  POP_JUMP_IF_FALSE   688  'to 688'

 L. 319       648  LOAD_CLOSURE             'usecols'
              650  BUILD_TUPLE_1         1 
              652  LOAD_LISTCOMP            '<code_object <listcomp>>'
              654  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              656  MAKE_FUNCTION_8          'closure'
              658  LOAD_DEREF               'sdf'
              660  LOAD_ATTR                schema
              662  GET_ITER         
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  STORE_DEREF              'cols'

 L. 320       668  LOAD_CLOSURE             'cols'
              670  BUILD_TUPLE_1         1 
              672  LOAD_LISTCOMP            '<code_object <listcomp>>'
              674  LOAD_STR                 'read_csv.<locals>.<listcomp>'
              676  MAKE_FUNCTION_8          'closure'
              678  LOAD_DEREF               'usecols'
              680  GET_ITER         
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  STORE_FAST               'missing'
              686  JUMP_FORWARD        696  'to 696'
            688_0  COME_FROM           644  '644'

 L. 322       688  LOAD_GLOBAL              ValueError

 L. 323       690  LOAD_STR                 "'usecols' must either be list-like of all strings, all unicode, all integers or a callable."
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  RAISE_VARARGS_1       1  'exception instance'
            696_0  COME_FROM           686  '686'
            696_1  COME_FROM           626  '626'
            696_2  COME_FROM           560  '560'

 L. 326       696  LOAD_GLOBAL              len
              698  LOAD_FAST                'missing'
              700  CALL_FUNCTION_1       1  '1 positional argument'
              702  LOAD_CONST               0
              704  COMPARE_OP               >
          706_708  POP_JUMP_IF_FALSE   722  'to 722'

 L. 327       710  LOAD_GLOBAL              ValueError

 L. 328       712  LOAD_STR                 'Usecols do not match columns, columns expected but not found: %s'
              714  LOAD_FAST                'missing'
              716  BINARY_MODULO    
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  RAISE_VARARGS_1       1  'exception instance'
            722_0  COME_FROM           706  '706'

 L. 331       722  LOAD_GLOBAL              len
              724  LOAD_DEREF               'cols'
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  LOAD_CONST               0
              730  COMPARE_OP               >
          732_734  POP_JUMP_IF_FALSE   748  'to 748'

 L. 332       736  LOAD_DEREF               'sdf'
              738  LOAD_METHOD              select
              740  LOAD_DEREF               'cols'
              742  CALL_METHOD_1         1  '1 positional argument'
              744  STORE_DEREF              'sdf'
              746  JUMP_FORWARD        766  'to 766'
            748_0  COME_FROM           732  '732'

 L. 334       748  LOAD_GLOBAL              default_session
              750  CALL_FUNCTION_0       0  '0 positional arguments'
              752  LOAD_ATTR                createDataFrame
              754  BUILD_LIST_0          0 
              756  LOAD_GLOBAL              StructType
              758  CALL_FUNCTION_0       0  '0 positional arguments'
              760  LOAD_CONST               ('schema',)
              762  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              764  STORE_DEREF              'sdf'
            766_0  COME_FROM           746  '746'
              766  JUMP_FORWARD        786  'to 786'
            768_0  COME_FROM            90  '90'

 L. 336       768  LOAD_GLOBAL              default_session
              770  CALL_FUNCTION_0       0  '0 positional arguments'
              772  LOAD_ATTR                createDataFrame
              774  BUILD_LIST_0          0 
              776  LOAD_GLOBAL              StructType
              778  CALL_FUNCTION_0       0  '0 positional arguments'
              780  LOAD_CONST               ('schema',)
              782  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              784  STORE_DEREF              'sdf'
            786_0  COME_FROM           766  '766'
            786_1  COME_FROM           522  '522'

 L. 338       786  LOAD_GLOBAL              _get_index_map
              788  LOAD_DEREF               'sdf'
              790  LOAD_FAST                'index_col'
              792  CALL_FUNCTION_2       2  '2 positional arguments'
              794  STORE_FAST               'index_map'

 L. 339       796  LOAD_GLOBAL              DataFrame
              798  LOAD_GLOBAL              _InternalFrame
              800  LOAD_DEREF               'sdf'
              802  LOAD_FAST                'index_map'
              804  LOAD_CONST               ('spark_frame', 'index_map')
              806  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  STORE_FAST               'kdf'

 L. 341       812  LOAD_FAST                'dtype'
              814  LOAD_CONST               None
              816  COMPARE_OP               is-not
          818_820  POP_JUMP_IF_FALSE   914  'to 914'

 L. 342       822  LOAD_GLOBAL              isinstance
              824  LOAD_FAST                'dtype'
              826  LOAD_GLOBAL              dict
              828  CALL_FUNCTION_2       2  '2 positional arguments'
          830_832  POP_JUMP_IF_FALSE   878  'to 878'

 L. 343       834  SETUP_LOOP          914  'to 914'
              836  LOAD_FAST                'dtype'
              838  LOAD_METHOD              items
              840  CALL_METHOD_0         0  '0 positional arguments'
              842  GET_ITER         
              844  FOR_ITER            874  'to 874'
              846  UNPACK_SEQUENCE_2     2 
              848  STORE_FAST               'col'
              850  STORE_FAST               'tpe'

 L. 344       852  LOAD_FAST                'kdf'
              854  LOAD_FAST                'col'
              856  BINARY_SUBSCR    
              858  LOAD_METHOD              astype
              860  LOAD_FAST                'tpe'
              862  CALL_METHOD_1         1  '1 positional argument'
              864  LOAD_FAST                'kdf'
              866  LOAD_FAST                'col'
              868  STORE_SUBSCR     
          870_872  JUMP_BACK           844  'to 844'
              874  POP_BLOCK        
              876  JUMP_FORWARD        914  'to 914'
            878_0  COME_FROM           830  '830'

 L. 346       878  SETUP_LOOP          914  'to 914'
              880  LOAD_FAST                'kdf'
              882  LOAD_ATTR                columns
              884  GET_ITER         
              886  FOR_ITER            912  'to 912'
              888  STORE_FAST               'col'

 L. 347       890  LOAD_FAST                'kdf'
              892  LOAD_FAST                'col'
              894  BINARY_SUBSCR    
              896  LOAD_METHOD              astype
              898  LOAD_FAST                'dtype'
              900  CALL_METHOD_1         1  '1 positional argument'
              902  LOAD_FAST                'kdf'
              904  LOAD_FAST                'col'
              906  STORE_SUBSCR     
          908_910  JUMP_BACK           886  'to 886'
              912  POP_BLOCK        
            914_0  COME_FROM_LOOP      878  '878'
            914_1  COME_FROM           876  '876'
            914_2  COME_FROM_LOOP      834  '834'
            914_3  COME_FROM           818  '818'

 L. 349       914  LOAD_FAST                'squeeze'
          916_918  POP_JUMP_IF_FALSE   950  'to 950'
              920  LOAD_GLOBAL              len
              922  LOAD_FAST                'kdf'
              924  LOAD_ATTR                columns
              926  CALL_FUNCTION_1       1  '1 positional argument'
              928  LOAD_CONST               1
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE   950  'to 950'

 L. 350       936  LOAD_FAST                'kdf'
              938  LOAD_FAST                'kdf'
              940  LOAD_ATTR                columns
              942  LOAD_CONST               0
              944  BINARY_SUBSCR    
              946  BINARY_SUBSCR    
              948  RETURN_VALUE     
            950_0  COME_FROM           932  '932'
            950_1  COME_FROM           916  '916'

 L. 351       950  LOAD_FAST                'kdf'
              952  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 952


def read_json(path: str, index_col: Optional[Union[(str, List[str])]]=None, **options):
    """
    Convert a JSON string to pandas object.

    Parameters
    ----------
    path : string
        File path
    index_col : str or list of str, optional, default: None
        Index column of table in Spark.
    options : dict
        All other options passed directly into Spark's data source.

    Examples
    --------
    >>> df = ks.DataFrame([['a', 'b'], ['c', 'd']],
    ...                   columns=['col 1', 'col 2'])

    >>> df.to_json(path=r'%s/read_json/foo.json' % path, num_files=1)
    >>> ks.read_json(
    ...     path=r'%s/read_json/foo.json' % path
    ... ).sort_values(by="col 1")
      col 1 col 2
    0     a     b
    1     c     d

    >>> df.to_json(path=r'%s/read_json/foo.json' % path, num_files=1, lineSep='___')
    >>> ks.read_json(
    ...     path=r'%s/read_json/foo.json' % path, lineSep='___'
    ... ).sort_values(by="col 1")
      col 1 col 2
    0     a     b
    1     c     d

    You can preserve the index in the roundtrip as below.

    >>> df.to_json(path=r'%s/read_json/bar.json' % path, num_files=1, index_col="index")
    >>> ks.read_json(
    ...     path=r'%s/read_json/bar.json' % path, index_col="index"
    ... ).sort_values(by="col 1")  # doctest: +NORMALIZE_WHITESPACE
          col 1 col 2
    index
    0         a     b
    1         c     d
    """
    return read_spark_io(path, format='json', index_col=index_col, **options)


def read_delta(path: str, version: Optional[str]=None, timestamp: Optional[str]=None, index_col: Optional[Union[(str, List[str])]]=None, **options) -> DataFrame:
    """
    Read a Delta Lake table on some file system and return a DataFrame.

    If the Delta Lake table is already stored in the catalog (aka the metastore), use 'read_table'.

    Parameters
    ----------
    path : string
        Path to the Delta Lake table.
    version : string, optional
        Specifies the table version (based on Delta's internal transaction version) to read from,
        using Delta's time travel feature. This sets Delta's 'versionAsOf' option.
    timestamp : string, optional
        Specifies the table version (based on timestamp) to read from,
        using Delta's time travel feature. This must be a valid date or timestamp string in Spark,
        and sets Delta's 'timestampAsOf' option.
    index_col : str or list of str, optional, default: None
        Index column of table in Spark.
    options
        Additional options that can be passed onto Delta.

    Returns
    -------
    DataFrame

    See Also
    --------
    DataFrame.to_delta
    read_table
    read_spark_io
    read_parquet

    Examples
    --------
    >>> ks.range(1).to_delta('%s/read_delta/foo' % path)
    >>> ks.read_delta('%s/read_delta/foo' % path)
       id
    0   0

    >>> ks.range(10, 15, num_partitions=1).to_delta('%s/read_delta/foo' % path, mode='overwrite')
    >>> ks.read_delta('%s/read_delta/foo' % path)
       id
    0  10
    1  11
    2  12
    3  13
    4  14

    >>> ks.read_delta('%s/read_delta/foo' % path, version=0)
       id
    0   0

    You can preserve the index in the roundtrip as below.

    >>> ks.range(10, 15, num_partitions=1).to_delta(
    ...     '%s/read_delta/bar' % path, index_col="index")
    >>> ks.read_delta('%s/read_delta/bar' % path, index_col="index")
    ... # doctest: +NORMALIZE_WHITESPACE
           id
    index
    0      10
    1      11
    2      12
    3      13
    4      14
    """
    if version is not None:
        options['versionAsOf'] = version
    if timestamp is not None:
        options['timestampAsOf'] = timestamp
    return read_spark_io(path, format='delta', index_col=index_col, **options)


def read_table(name: str, index_col: Optional[Union[(str, List[str])]]=None) -> DataFrame:
    """
    Read a Spark table and return a DataFrame.

    Parameters
    ----------
    name : string
        Table name in Spark.

    index_col : str or list of str, optional, default: None
        Index column of table in Spark.

    Returns
    -------
    DataFrame

    See Also
    --------
    DataFrame.to_table
    read_delta
    read_parquet
    read_spark_io

    Examples
    --------
    >>> ks.range(1).to_table('%s.my_table' % db)
    >>> ks.read_table('%s.my_table' % db)
       id
    0   0

    >>> ks.range(1).to_table('%s.my_table' % db, index_col="index")
    >>> ks.read_table('%s.my_table' % db, index_col="index")  # doctest: +NORMALIZE_WHITESPACE
           id
    index
    0       0
    """
    sdf = default_session().read.table(name)
    index_map = _get_index_map(sdf, index_col)
    return DataFrame(_InternalFrame(spark_frame=sdf, index_map=index_map))


def read_spark_io(path: Optional[str]=None, format: Optional[str]=None, schema: Union[(str, 'StructType')]=None, index_col: Optional[Union[(str, List[str])]]=None, **options) -> DataFrame:
    """Load a DataFrame from a Spark data source.

    Parameters
    ----------
    path : string, optional
        Path to the data source.
    format : string, optional
        Specifies the output data source format. Some common ones are:

        - 'delta'
        - 'parquet'
        - 'orc'
        - 'json'
        - 'csv'
    schema : string or StructType, optional
        Input schema. If none, Spark tries to infer the schema automatically.
        The schema can either be a Spark StructType, or a DDL-formatted string like
        `col0 INT, col1 DOUBLE`.
    index_col : str or list of str, optional, default: None
        Index column of table in Spark.
    options : dict
        All other options passed directly into Spark's data source.

    See Also
    --------
    DataFrame.to_spark_io
    DataFrame.read_table
    DataFrame.read_delta
    DataFrame.read_parquet

    Examples
    --------
    >>> ks.range(1).to_spark_io('%s/read_spark_io/data.parquet' % path)
    >>> ks.read_spark_io(
    ...     '%s/read_spark_io/data.parquet' % path, format='parquet', schema='id long')
       id
    0   0

    >>> ks.range(10, 15, num_partitions=1).to_spark_io('%s/read_spark_io/data.json' % path,
    ...                                                format='json', lineSep='__')
    >>> ks.read_spark_io(
    ...     '%s/read_spark_io/data.json' % path, format='json', schema='id long', lineSep='__')
       id
    0  10
    1  11
    2  12
    3  13
    4  14

    You can preserve the index in the roundtrip as below.

    >>> ks.range(10, 15, num_partitions=1).to_spark_io('%s/read_spark_io/data.orc' % path,
    ...                                                format='orc', index_col="index")
    >>> ks.read_spark_io(
    ...     path=r'%s/read_spark_io/data.orc' % path, format="orc", index_col="index")
    ... # doctest: +NORMALIZE_WHITESPACE
           id
    index
    0      10
    1      11
    2      12
    3      13
    4      14
    """
    sdf = (default_session().read.load)(path=path, format=format, schema=schema, **options)
    index_map = _get_index_map(sdf, index_col)
    return DataFrame(_InternalFrame(spark_frame=sdf, index_map=index_map))


def read_parquet(path, columns=None, index_col=None, **options) -> DataFrame:
    """Load a parquet object from the file path, returning a DataFrame.

    Parameters
    ----------
    path : string
        File path
    columns : list, default=None
        If not None, only these columns will be read from the file.
    index_col : str or list of str, optional, default: None
        Index column of table in Spark.
    options : dict
        All other options passed directly into Spark's data source.

    Returns
    -------
    DataFrame

    See Also
    --------
    DataFrame.to_parquet
    DataFrame.read_table
    DataFrame.read_delta
    DataFrame.read_spark_io

    Examples
    --------
    >>> ks.range(1).to_parquet('%s/read_spark_io/data.parquet' % path)
    >>> ks.read_parquet('%s/read_spark_io/data.parquet' % path, columns=['id'])
       id
    0   0

    You can preserve the index in the roundtrip as below.

    >>> ks.range(1).to_parquet('%s/read_spark_io/data.parquet' % path, index_col="index")
    >>> ks.read_parquet('%s/read_spark_io/data.parquet' % path, columns=['id'], index_col="index")
    ... # doctest: +NORMALIZE_WHITESPACE
           id
    index
    0       0
    """
    if columns is not None:
        columns = list(columns)
    kdf = read_spark_io(path=path, format='parquet', options=options, index_col=index_col)
    if columns is not None:
        new_columns = [c for c in columns if c in kdf.columns]
        if len(new_columns) > 0:
            kdf = kdf[new_columns]
        else:
            sdf = default_session().createDataFrame([], schema=(StructType()))
            index_map = _get_index_map(sdf, index_col)
            return DataFrame(_InternalFrame(spark_frame=sdf, index_map=index_map))
    return kdf


def read_clipboard(sep='\\s+', **kwargs):
    r"""
    Read text from clipboard and pass to read_csv. See read_csv for the
    full argument list

    Parameters
    ----------
    sep : str, default '\s+'
        A string or regex delimiter. The default of '\s+' denotes
        one or more whitespace characters.

    See Also
    --------
    DataFrame.to_clipboard : Write text out to clipboard.

    Returns
    -------
    parsed : DataFrame
    """
    return from_pandas((pd.read_clipboard)(sep, **kwargs))


def read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None, squeeze=False, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None, nrows=None, na_values=None, keep_default_na=True, verbose=False, parse_dates=False, date_parser=None, thousands=None, comment=None, skipfooter=0, convert_float=True, mangle_dupe_cols=True, **kwds):
    """
    Read an Excel file into a Koalas DataFrame.

    Support both `xls` and `xlsx` file extensions from a local filesystem or URL.
    Support an option to read a single sheet or a list of sheets.

    Parameters
    ----------
    io : str, file descriptor, pathlib.Path, ExcelFile or xlrd.Book
        The string could be a URL. Valid URL schemes include http, ftp, s3,
        gcs, and file. For file URLs, a host is expected. For instance, a local
        file could be /path/to/workbook.xlsx.
    sheet_name : str, int, list, or None, default 0
        Strings are used for sheet names. Integers are used in zero-indexed
        sheet positions. Lists of strings/integers are used to request
        multiple sheets. Specify None to get all sheets.

        Available cases:

        * Defaults to ``0``: 1st sheet as a `DataFrame`
        * ``1``: 2nd sheet as a `DataFrame`
        * ``"Sheet1"``: Load sheet with name "Sheet1"
        * ``[0, 1, "Sheet5"]``: Load first, second and sheet named "Sheet5"
          as a dict of `DataFrame`
        * None: All sheets.

    header : int, list of int, default 0
        Row (0-indexed) to use for the column labels of the parsed
        DataFrame. If a list of integers is passed those row positions will
        be combined into a ``MultiIndex``. Use None if there is no header.
    names : array-like, default None
        List of column names to use. If file contains no header row,
        then you should explicitly pass header=None.
    index_col : int, list of int, default None
        Column (0-indexed) to use as the row labels of the DataFrame.
        Pass None if there is no such column.  If a list is passed,
        those columns will be combined into a ``MultiIndex``.  If a
        subset of data is selected with ``usecols``, index_col
        is based on the subset.
    usecols : int, str, list-like, or callable default None
        Return a subset of the columns.

        * If None, then parse all columns.
        * If str, then indicates comma separated list of Excel column letters
          and column ranges (e.g. "A:E" or "A,C,E:F"). Ranges are inclusive of
          both sides.
        * If list of int, then indicates list of column numbers to be parsed.
        * If list of string, then indicates list of column names to be parsed.
        * If callable, then evaluate each column name against it and parse the
          column if the callable returns ``True``.
    squeeze : bool, default False
        If the parsed data only contains one column then return a Series.
    dtype : Type name or dict of column -> type, default None
        Data type for data or columns. E.g. {'a': np.float64, 'b': np.int32}
        Use `object` to preserve data as stored in Excel and not interpret dtype.
        If converters are specified, they will be applied INSTEAD
        of dtype conversion.
    engine : str, default None
        If io is not a buffer or path, this must be set to identify io.
        Acceptable values are None or xlrd.
    converters : dict, default None
        Dict of functions for converting values in certain columns. Keys can
        either be integers or column labels, values are functions that take one
        input argument, the Excel cell content, and return the transformed
        content.
    true_values : list, default None
        Values to consider as True.
    false_values : list, default None
        Values to consider as False.
    skiprows : list-like
        Rows to skip at the beginning (0-indexed).
    nrows : int, default None
        Number of rows to parse.
    na_values : scalar, str, list-like, or dict, default None
        Additional strings to recognize as NA/NaN. If dict passed, specific
        per-column NA values. By default the following values are interpreted
        as NaN.
    keep_default_na : bool, default True
        If na_values are specified and keep_default_na is False the default NaN
        values are overridden, otherwise they're appended to.
    verbose : bool, default False
        Indicate number of NA values placed in non-numeric columns.
    parse_dates : bool, list-like, or dict, default False
        The behavior is as follows:

        * bool. If True -> try parsing the index.
        * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
          each as a separate date column.
        * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
          a single date column.
        * dict, e.g. {{'foo' : [1, 3]}} -> parse columns 1, 3 as date and call
          result 'foo'

        If a column or index contains an unparseable date, the entire column or
        index will be returned unaltered as an object data type. For non-standard
        datetime parsing, use ``pd.to_datetime`` after ``pd.read_csv``

        Note: A fast-path exists for iso8601-formatted dates.
    date_parser : function, optional
        Function to use for converting a sequence of string columns to an array of
        datetime instances. The default uses ``dateutil.parser.parser`` to do the
        conversion. Koalas will try to call `date_parser` in three different ways,
        advancing to the next if an exception occurs: 1) Pass one or more arrays
        (as defined by `parse_dates`) as arguments; 2) concatenate (row-wise) the
        string values from the columns defined by `parse_dates` into a single array
        and pass that; and 3) call `date_parser` once for each row using one or
        more strings (corresponding to the columns defined by `parse_dates`) as
        arguments.
    thousands : str, default None
        Thousands separator for parsing string columns to numeric.  Note that
        this parameter is only necessary for columns stored as TEXT in Excel,
        any numeric columns will automatically be parsed, regardless of display
        format.
    comment : str, default None
        Comments out remainder of line. Pass a character or characters to this
        argument to indicate comments in the input file. Any data between the
        comment string and the end of the current line is ignored.
    skipfooter : int, default 0
        Rows at the end to skip (0-indexed).
    convert_float : bool, default True
        Convert integral floats to int (i.e., 1.0 --> 1). If False, all numeric
        data will be read in as floats: Excel stores all numbers as floats
        internally.
    mangle_dupe_cols : bool, default True
        Duplicate columns will be specified as 'X', 'X.1', ...'X.N', rather than
        'X'...'X'. Passing in False will cause data to be overwritten if there
        are duplicate names in the columns.
    **kwds : optional
        Optional keyword arguments can be passed to ``TextFileReader``.

    Returns
    -------
    DataFrame or dict of DataFrames
        DataFrame from the passed in Excel file. See notes in sheet_name
        argument for more information on when a dict of DataFrames is returned.

    See Also
    --------
    DataFrame.to_excel : Write DataFrame to an Excel file.
    DataFrame.to_csv : Write DataFrame to a comma-separated values (csv) file.
    read_csv : Read a comma-separated values (csv) file into DataFrame.

    Examples
    --------
    The file can be read using the file name as string or an open file object:

    >>> ks.read_excel('tmp.xlsx', index_col=0)  # doctest: +SKIP
           Name  Value
    0   string1      1
    1   string2      2
    2  #Comment      3

    >>> ks.read_excel(open('tmp.xlsx', 'rb'),
    ...               sheet_name='Sheet3')  # doctest: +SKIP
       Unnamed: 0      Name  Value
    0           0   string1      1
    1           1   string2      2
    2           2  #Comment      3

    Index and header can be specified via the `index_col` and `header` arguments

    >>> ks.read_excel('tmp.xlsx', index_col=None, header=None)  # doctest: +SKIP
         0         1      2
    0  NaN      Name  Value
    1  0.0   string1      1
    2  1.0   string2      2
    3  2.0  #Comment      3

    Column types are inferred but can be explicitly specified

    >>> ks.read_excel('tmp.xlsx', index_col=0,
    ...               dtype={'Name': str, 'Value': float})  # doctest: +SKIP
           Name  Value
    0   string1    1.0
    1   string2    2.0
    2  #Comment    3.0

    True, False, and NA values, and thousands separators have defaults,
    but can be explicitly specified, too. Supply the values you would like
    as strings or lists of strings!

    >>> ks.read_excel('tmp.xlsx', index_col=0,
    ...               na_values=['string1', 'string2'])  # doctest: +SKIP
           Name  Value
    0      None      1
    1      None      2
    2  #Comment      3

    Comment lines in the excel input file can be skipped using the `comment` kwarg

    >>> ks.read_excel('tmp.xlsx', index_col=0, comment='#')  # doctest: +SKIP
          Name  Value
    0  string1    1.0
    1  string2    2.0
    2     None    NaN
    """
    pdfs = (pd.read_excel)(io=io, 
     sheet_name=sheet_name, 
     header=header, 
     names=names, 
     index_col=index_col, 
     usecols=usecols, 
     squeeze=squeeze, 
     dtype=dtype, 
     engine=engine, 
     converters=converters, 
     true_values=true_values, 
     false_values=false_values, 
     skiprows=skiprows, 
     nrows=nrows, 
     na_values=na_values, 
     keep_default_na=keep_default_na, 
     verbose=verbose, 
     parse_dates=parse_dates, 
     date_parser=date_parser, 
     thousands=thousands, 
     comment=comment, 
     skipfooter=skipfooter, 
     convert_float=convert_float, 
     mangle_dupe_cols=mangle_dupe_cols, **kwds)
    if isinstance(pdfs, dict):
        return OrderedDict([(key, from_pandas(value)) for key, value in pdfs.items])
    return from_pandas(pdfs)


def read_html(io, match='.+', flavor=None, header=None, index_col=None, skiprows=None, attrs=None, parse_dates=False, thousands=',', encoding=None, decimal='.', converters=None, na_values=None, keep_default_na=True, displayed_only=True):
    """Read HTML tables into a ``list`` of ``DataFrame`` objects.

    Parameters
    ----------
    io : str or file-like
        A URL, a file-like object, or a raw string containing HTML. Note that
        lxml only accepts the http, ftp and file url protocols. If you have a
        URL that starts with ``'https'`` you might try removing the ``'s'``.

    match : str or compiled regular expression, optional
        The set of tables containing text matching this regex or string will be
        returned. Unless the HTML is extremely simple you will probably need to
        pass a non-empty string here. Defaults to '.+' (match any non-empty
        string). The default value will return all tables contained on a page.
        This value is converted to a regular expression so that there is
        consistent behavior between Beautiful Soup and lxml.

    flavor : str or None, container of strings
        The parsing engine to use. 'bs4' and 'html5lib' are synonymous with
        each other, they are both there for backwards compatibility. The
        default of ``None`` tries to use ``lxml`` to parse and if that fails it
        falls back on ``bs4`` + ``html5lib``.

    header : int or list-like or None, optional
        The row (or list of rows for a :class:`~ks.MultiIndex`) to use to
        make the columns headers.

    index_col : int or list-like or None, optional
        The column (or list of columns) to use to create the index.

    skiprows : int or list-like or slice or None, optional
        0-based. Number of rows to skip after parsing the column integer. If a
        sequence of integers or a slice is given, will skip the rows indexed by
        that sequence.  Note that a single element sequence means 'skip the nth
        row' whereas an integer means 'skip n rows'.

    attrs : dict or None, optional
        This is a dictionary of attributes that you can pass to use to identify
        the table in the HTML. These are not checked for validity before being
        passed to lxml or Beautiful Soup. However, these attributes must be
        valid HTML table attributes to work correctly. For example, ::

            attrs = {'id': 'table'}

        is a valid attribute dictionary because the 'id' HTML tag attribute is
        a valid HTML attribute for *any* HTML tag as per `this document
        <http://www.w3.org/TR/html-markup/global-attributes.html>`__. ::

            attrs = {'asdf': 'table'}

        is *not* a valid attribute dictionary because 'asdf' is not a valid
        HTML attribute even if it is a valid XML attribute.  Valid HTML 4.01
        table attributes can be found `here
        <http://www.w3.org/TR/REC-html40/struct/tables.html#h-11.2>`__. A
        working draft of the HTML 5 spec can be found `here
        <http://www.w3.org/TR/html-markup/table.html>`__. It contains the
        latest information on table attributes for the modern web.

    parse_dates : bool, optional
        See :func:`~ks.read_csv` for more details.

    thousands : str, optional
        Separator to use to parse thousands. Defaults to ``','``.

    encoding : str or None, optional
        The encoding used to decode the web page. Defaults to ``None``.``None``
        preserves the previous encoding behavior, which depends on the
        underlying parser library (e.g., the parser library will try to use
        the encoding provided by the document).

    decimal : str, default '.'
        Character to recognize as decimal point (e.g. use ',' for European
        data).

    converters : dict, default None
        Dict of functions for converting values in certain columns. Keys can
        either be integers or column labels, values are functions that take one
        input argument, the cell (not column) content, and return the
        transformed content.

    na_values : iterable, default None
        Custom NA values

    keep_default_na : bool, default True
        If na_values are specified and keep_default_na is False the default NaN
        values are overridden, otherwise they're appended to

    displayed_only : bool, default True
        Whether elements with "display: none" should be parsed

    Returns
    -------
    dfs : list of DataFrames

    See Also
    --------
    read_csv
    DataFrame.to_html
    """
    pdfs = pd.read_html(io=io,
      match=match,
      flavor=flavor,
      header=header,
      index_col=index_col,
      skiprows=skiprows,
      attrs=attrs,
      parse_dates=parse_dates,
      thousands=thousands,
      encoding=encoding,
      decimal=decimal,
      converters=converters,
      na_values=na_values,
      keep_default_na=keep_default_na,
      displayed_only=displayed_only)
    return [from_pandas(pdf) for pdf in pdfs]


def read_sql_table(table_name, con, schema=None, index_col=None, columns=None, **options):
    """
    Read SQL database table into a DataFrame.

    Given a table name and a JDBC URI, returns a DataFrame.

    Parameters
    ----------
    table_name : str
        Name of SQL table in database.
    con : str
        A JDBC URI could be provided as as str.

        .. note:: The URI must be JDBC URI instead of Python's database URI.

    schema : str, default None
        Name of SQL schema in database to query (if database flavor
        supports this). Uses default schema if None (default).
    index_col : str or list of str, optional, default: None
        Column(s) to set as index(MultiIndex).
    columns : list, default None
        List of column names to select from SQL table.
    options : dict
        All other options passed directly into Spark's JDBC data source.

    Returns
    -------
    DataFrame
        A SQL table is returned as two-dimensional data structure with labeled
        axes.

    See Also
    --------
    read_sql_query : Read SQL query into a DataFrame.
    read_sql : Read SQL query or database table into a DataFrame.

    Examples
    --------
    >>> ks.read_sql_table('table_name', 'jdbc:postgresql:db_name')  # doctest: +SKIP
    """
    reader = default_session().read
    reader.option'dbtable'table_name
    reader.option'url'con
    if schema is not None:
        reader.schema(schema)
    (reader.options)(**options)
    sdf = reader.format('jdbc').load
    index_map = _get_index_map(sdf, index_col)
    kdf = DataFrame(_InternalFrame(spark_frame=sdf, index_map=index_map))
    if columns is not None:
        if isinstance(columns, str):
            columns = [
             columns]
        kdf = kdf[columns]
    return kdf


def read_sql_query(sql, con, index_col=None, **options):
    """Read SQL query into a DataFrame.

    Returns a DataFrame corresponding to the result set of the query
    string. Optionally provide an `index_col` parameter to use one of the
    columns as the index, otherwise default index will be used.

    .. note:: Some database might hit the issue of Spark: SPARK-27596

    Parameters
    ----------
    sql : string SQL query
        SQL query to be executed.
    con : str
        A JDBC URI could be provided as as str.

        .. note:: The URI must be JDBC URI instead of Python's database URI.

    index_col : string or list of strings, optional, default: None
        Column(s) to set as index(MultiIndex).
    options : dict
        All other options passed directly into Spark's JDBC data source.

    Returns
    -------
    DataFrame

    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql

    Examples
    --------
    >>> ks.read_sql_query('SELECT * FROM table_name', 'jdbc:postgresql:db_name')  # doctest: +SKIP
    """
    reader = default_session().read
    reader.option'query'sql
    reader.option'url'con
    (reader.options)(**options)
    sdf = reader.format('jdbc').load
    index_map = _get_index_map(sdf, index_col)
    return DataFrame(_InternalFrame(spark_frame=sdf, index_map=index_map))


def read_sql(sql, con, index_col=None, columns=None, **options):
    """
    Read SQL query or database table into a DataFrame.

    This function is a convenience wrapper around ``read_sql_table`` and
    ``read_sql_query`` (for backward compatibility). It will delegate
    to the specific function depending on the provided input. A SQL query
    will be routed to ``read_sql_query``, while a database table name will
    be routed to ``read_sql_table``. Note that the delegated function might
    have more specific notes about their functionality not listed here.

    .. note:: Some database might hit the issue of Spark: SPARK-27596

    Parameters
    ----------
    sql : string
        SQL query to be executed or a table name.
    con : str
        A JDBC URI could be provided as as str.

        .. note:: The URI must be JDBC URI instead of Python's database URI.

    index_col : string or list of strings, optional, default: None
        Column(s) to set as index(MultiIndex).
    columns : list, default: None
        List of column names to select from SQL table (only used when reading
        a table).
    options : dict
        All other options passed directly into Spark's JDBC data source.

    Returns
    -------
    DataFrame

    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql_query : Read SQL query into a DataFrame.

    Examples
    --------
    >>> ks.read_sql('table_name', 'jdbc:postgresql:db_name')  # doctest: +SKIP
    >>> ks.read_sql('SELECT * FROM table_name', 'jdbc:postgresql:db_name')  # doctest: +SKIP
    """
    striped = sql.strip
    if ' ' not in striped:
        return read_sql_table(sql, con, index_col=index_col, columns=columns, **options)
    return read_sql_query(sql, con, index_col=index_col, **options)


def to_datetime(arg, errors='raise', format=None, unit=None, infer_datetime_format=False, origin='unix'):
    """
    Convert argument to datetime.

    Parameters
    ----------
    arg : integer, float, string, datetime, list, tuple, 1-d array, Series
           or DataFrame/dict-like

    errors : {'ignore', 'raise', 'coerce'}, default 'raise'

        - If 'raise', then invalid parsing will raise an exception
        - If 'coerce', then invalid parsing will be set as NaT
        - If 'ignore', then invalid parsing will return the input
    format : string, default None
        strftime to parse time, eg "%d/%m/%Y", note that "%f" will parse
        all the way up to nanoseconds.
    unit : string, default None
        unit of the arg (D,s,ms,us,ns) denote the unit, which is an
        integer or float number. This will be based off the origin.
        Example, with unit='ms' and origin='unix' (the default), this
        would calculate the number of milliseconds to the unix epoch start.
    infer_datetime_format : boolean, default False
        If True and no `format` is given, attempt to infer the format of the
        datetime strings, and if it can be inferred, switch to a faster
        method of parsing them. In some cases this can increase the parsing
        speed by ~5-10x.
    origin : scalar, default 'unix'
        Define the reference date. The numeric values would be parsed as number
        of units (defined by `unit`) since this reference date.

        - If 'unix' (or POSIX) time; origin is set to 1970-01-01.
        - If 'julian', unit must be 'D', and origin is set to beginning of
          Julian Calendar. Julian day number 0 is assigned to the day starting
          at noon on January 1, 4713 BC.
        - If Timestamp convertible, origin is set to Timestamp identified by
          origin.

    Returns
    -------
    ret : datetime if parsing succeeded.
        Return type depends on input:

        - list-like: DatetimeIndex
        - Series: Series of datetime64 dtype
        - scalar: Timestamp

        In case when it is not possible to return designated types (e.g. when
        any element of input is before Timestamp.min or after Timestamp.max)
        return will have datetime.datetime type (or corresponding
        array/Series).

    Examples
    --------
    Assembling a datetime from multiple columns of a DataFrame. The keys can be
    common abbreviations like ['year', 'month', 'day', 'minute', 'second',
    'ms', 'us', 'ns']) or plurals of the same

    >>> df = ks.DataFrame({'year': [2015, 2016],
    ...                    'month': [2, 3],
    ...                    'day': [4, 5]})
    >>> ks.to_datetime(df)
    0   2015-02-04
    1   2016-03-05
    Name: _to_datetime2(arg_day=day, arg_month=month, arg_year=year), dtype: datetime64[ns]

    If a date does not meet the `timestamp limitations
    <http://pandas.pydata.org/pandas-docs/stable/timeseries.html
    #timeseries-timestamp-limits>`_, passing errors='ignore'
    will return the original input instead of raising any exception.

    Passing errors='coerce' will force an out-of-bounds date to NaT,
    in addition to forcing non-dates (or non-parseable dates) to NaT.

    >>> ks.to_datetime('13000101', format='%Y%m%d', errors='ignore')
    datetime.datetime(1300, 1, 1, 0, 0)
    >>> ks.to_datetime('13000101', format='%Y%m%d', errors='coerce')
    NaT

    Passing infer_datetime_format=True can often-times speedup a parsing
    if its not an ISO8601 format exactly, but in a regular format.

    >>> s = ks.Series(['3/11/2000', '3/12/2000', '3/13/2000'] * 1000)
    >>> s.head()
    0    3/11/2000
    1    3/12/2000
    2    3/13/2000
    3    3/11/2000
    4    3/12/2000
    Name: 0, dtype: object

    >>> import timeit
    >>> timeit.timeit(
    ...    lambda: repr(ks.to_datetime(s, infer_datetime_format=True)),
    ...    number = 1)  # doctest: +SKIP
    0.35832712500000063

    >>> timeit.timeit(
    ...    lambda: repr(ks.to_datetime(s, infer_datetime_format=False)),
    ...    number = 1)  # doctest: +SKIP
    0.8895321660000004

    Using a unix epoch time

    >>> ks.to_datetime(1490195805, unit='s')
    Timestamp('2017-03-22 15:16:45')
    >>> ks.to_datetime(1490195805433502912, unit='ns')
    Timestamp('2017-03-22 15:16:45.433502912')

    Using a non-unix epoch origin

    >>> ks.to_datetime([1, 2, 3], unit='D', origin=pd.Timestamp('1960-01-01'))
    DatetimeIndex(['1960-01-02', '1960-01-03', '1960-01-04'], dtype='datetime64[ns]', freq=None)
    """
    if isinstance(arg, Series):
        return _to_datetime1(arg,
          errors=errors,
          format=format,
          unit=unit,
          infer_datetime_format=infer_datetime_format,
          origin=origin)
    if isinstance(arg, DataFrame):
        return _to_datetime2(arg_year=(arg['year']),
          arg_month=(arg['month']),
          arg_day=(arg['day']),
          errors=errors,
          format=format,
          unit=unit,
          infer_datetime_format=infer_datetime_format,
          origin=origin)
    if isinstance(arg, dict):
        return _to_datetime2(arg_year=(arg['year']),
          arg_month=(arg['month']),
          arg_day=(arg['day']),
          errors=errors,
          format=format,
          unit=unit,
          infer_datetime_format=infer_datetime_format,
          origin=origin)
    return pd.to_datetime(arg,
      errors=errors,
      format=format,
      unit=unit,
      infer_datetime_format=infer_datetime_format,
      origin=origin)


def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None):
    """
    Convert categorical variable into dummy/indicator variables, also
    known as one hot encoding.

    Parameters
    ----------
    data : array-like, Series, or DataFrame
    prefix : string, list of strings, or dict of strings, default None
        String to append DataFrame column names.
        Pass a list with length equal to the number of columns
        when calling get_dummies on a DataFrame. Alternatively, `prefix`
        can be a dictionary mapping column names to prefixes.
    prefix_sep : string, default '_'
        If appending prefix, separator/delimiter to use. Or pass a
        list or dictionary as with `prefix.`
    dummy_na : bool, default False
        Add a column to indicate NaNs, if False NaNs are ignored.
    columns : list-like, default None
        Column names in the DataFrame to be encoded.
        If `columns` is None then all the columns with
        `object` or `category` dtype will be converted.
    sparse : bool, default False
        Whether the dummy-encoded columns should be be backed by
        a :class:`SparseArray` (True) or a regular NumPy array (False).
        In Koalas, this value must be "False".
    drop_first : bool, default False
        Whether to get k-1 dummies out of k categorical levels by removing the
        first level.
    dtype : dtype, default np.uint8
        Data type for new columns. Only a single dtype is allowed.

    Returns
    -------
    dummies : DataFrame

    See Also
    --------
    Series.str.get_dummies

    Examples
    --------
    >>> s = ks.Series(list('abca'))

    >>> ks.get_dummies(s)
       a  b  c
    0  1  0  0
    1  0  1  0
    2  0  0  1
    3  1  0  0

    >>> df = ks.DataFrame({'A': ['a', 'b', 'a'], 'B': ['b', 'a', 'c'],
    ...                    'C': [1, 2, 3]},
    ...                   columns=['A', 'B', 'C'])

    >>> ks.get_dummies(df, prefix=['col1', 'col2'])
       C  col1_a  col1_b  col2_a  col2_b  col2_c
    0  1       1       0       0       1       0
    1  2       0       1       1       0       0
    2  3       1       0       0       0       1

    >>> ks.get_dummies(ks.Series(list('abcaa')))
       a  b  c
    0  1  0  0
    1  0  1  0
    2  0  0  1
    3  1  0  0
    4  1  0  0

    >>> ks.get_dummies(ks.Series(list('abcaa')), drop_first=True)
       b  c
    0  0  0
    1  1  0
    2  0  1
    3  0  0
    4  0  0

    >>> ks.get_dummies(ks.Series(list('abc')), dtype=float)
         a    b    c
    0  1.0  0.0  0.0
    1  0.0  1.0  0.0
    2  0.0  0.0  1.0
    """
    if sparse is not False:
        raise NotImplementedError('get_dummies currently does not support sparse')
    else:
        if columns is not None:
            if not is_list_like(columns):
                raise TypeError('Input must be a list-like for parameter `columns`')
        if dtype is None:
            dtype = 'byte'
        if isinstance(data, Series):
            if prefix is not None:
                prefix = [
                 str(prefix)]
            column_labels = [
             (
              data.name,)]
            kdf = data.to_dataframe
            remaining_columns = []
        else:
            if isinstance(prefix, str):
                raise NotImplementedError('get_dummies currently does not support prefix as string types')
            else:
                kdf = data.copy
                if columns is None:
                    column_labels = [label for label in kdf._internal.column_labels if isinstance(kdf._internal.spark_type_for(label), _get_dummies_default_accept_types)]
                else:
                    if isinstance(columns, (str, tuple)):
                        if isinstance(columns, str):
                            key = (
                             columns,)
                        else:
                            key = columns
                        column_labels = [label for label in kdf._internal.column_labels if label[:len(key)] == key]
                        if len(column_labels) == 0:
                            raise KeyError(column_labels)
                        if prefix is None:
                            prefix = [str(label[len(key):]) if len(label) > len(key) + 1 else label[len(key)] if len(label) == len(key) + 1 else '' for label in column_labels]
                    elif any((isinstance(col, str) for col in columns)) and any((isinstance(col, tuple) for col in columns)):
                        raise ValueError('Expected tuple, got str')
                    else:
                        column_labels = [label for key in columns if not label == key if label[0] == key for label in kdf._internal if label[0] == key]
            if len(column_labels) == 0:
                if columns is None:
                    return kdf
                raise KeyError('{} not in index'.format(columns))
            if prefix is None:
                prefix = [str(label) if len(label) > 1 else label[0] for label in column_labels]
            column_labels_set = set(column_labels)
            remaining_columns = [kdf[label].rename(name_like_string(label)) for label in kdf._internal.column_labels if label not in column_labels_set]
        if any((not isinstance(kdf._internal.spark_type_for(label), _get_dummies_acceptable_types) for label in column_labels)):
            raise NotImplementedError('get_dummies currently only accept {} values'.format(', '.join([t.typeName for t in _get_dummies_acceptable_types])))
        if prefix is not None and len(column_labels) != len(prefix):
            raise ValueError("Length of 'prefix' ({}) did not match the length of the columns being encoded ({}).".formatlen(prefix)len(column_labels))
    all_values = _reduce_spark_multi(kdf._sdf, [F.collect_set(kdf._internal.spark_column_for(label)) for label in column_labels])
    for i, label in enumerate(column_labels):
        values = sorted(all_values[i])
        if drop_first:
            values = values[1:]

        def column_name(value):
            if prefix is None or prefix[i] == '':
                return str(value)
            return '{}{}{}'.format(prefix[i], prefix_sep, value)

        for value in values:
            remaining_columns.append((kdf[label].notnull & (kdf[label] == value)).astype(dtype).rename(column_name(value)))

        if dummy_na:
            remaining_columns.append(kdf[label].isnull.astype(dtype).rename(column_name('nan')))

    return kdf[remaining_columns]


def concat(objs, axis=0, join='outer', ignore_index=False):
    """
    Concatenate pandas objects along a particular axis with optional set logic
    along the other axes.

    Parameters
    ----------
    objs : a sequence of Series or DataFrame
        Any None objects will be dropped silently unless
        they are all None in which case a ValueError will be raised
    axis : {0/'index', 1/'columns'}, default 0
        The axis to concatenate along.
    join : {'inner', 'outer'}, default 'outer'
        How to handle indexes on other axis (or axes).
    ignore_index : bool, default False
        If True, do not use the index values along the concatenation axis. The
        resulting axis will be labeled 0, ..., n - 1. This is useful if you are
        concatenating objects where the concatenation axis does not have
        meaningful indexing information. Note the index values on the other
        axes are still respected in the join.

    Returns
    -------
    object, type of objs
        When concatenating all ``Series`` along the index (axis=0), a
        ``Series`` is returned. When ``objs`` contains at least one
        ``DataFrame``, a ``DataFrame`` is returned. When concatenating along
        the columns (axis=1), a ``DataFrame`` is returned.

    See Also
    --------
    Series.append : Concatenate Series.
    DataFrame.join : Join DataFrames using indexes.
    DataFrame.merge : Merge DataFrames by indexes or columns.

    Examples
    --------
    Combine two ``Series``.

    >>> s1 = ks.Series(['a', 'b'])
    >>> s2 = ks.Series(['c', 'd'])
    >>> ks.concat([s1, s2])
    0    a
    1    b
    0    c
    1    d
    Name: 0, dtype: object

    Clear the existing index and reset it in the result
    by setting the ``ignore_index`` option to ``True``.

    >>> ks.concat([s1, s2], ignore_index=True)
    0    a
    1    b
    2    c
    3    d
    Name: 0, dtype: object

    Combine two ``DataFrame`` objects with identical columns.

    >>> df1 = ks.DataFrame([['a', 1], ['b', 2]],
    ...                    columns=['letter', 'number'])
    >>> df1
      letter  number
    0      a       1
    1      b       2
    >>> df2 = ks.DataFrame([['c', 3], ['d', 4]],
    ...                    columns=['letter', 'number'])
    >>> df2
      letter  number
    0      c       3
    1      d       4

    >>> ks.concat([df1, df2])
      letter  number
    0      a       1
    1      b       2
    0      c       3
    1      d       4

    Combine ``DataFrame`` and ``Series`` objects with different columns.

    >>> ks.concat([df2, s1, s2])
          0 letter  number
    0  None      c     3.0
    1  None      d     4.0
    0     a   None     NaN
    1     b   None     NaN
    0     c   None     NaN
    1     d   None     NaN

    Combine ``DataFrame`` objects with overlapping columns
    and return everything. Columns outside the intersection will
    be filled with ``None`` values.

    >>> df3 = ks.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']],
    ...                    columns=['letter', 'number', 'animal'])
    >>> df3
      letter  number animal
    0      c       3    cat
    1      d       4    dog

    >>> ks.concat([df1, df3])
      animal letter  number
    0   None      a       1
    1   None      b       2
    0    cat      c       3
    1    dog      d       4

    Combine ``DataFrame`` objects with overlapping columns
    and return only those that are shared by passing ``inner`` to
    the ``join`` keyword argument.

    >>> ks.concat([df1, df3], join="inner")
      letter  number
    0      a       1
    1      b       2
    0      c       3
    1      d       4

    >>> df4 = ks.DataFrame([['bird', 'polly'], ['monkey', 'george']],
    ...                    columns=['animal', 'name'])

    Combine with column axis.

    >>> ks.concat([df1, df4], axis=1)
      letter  number  animal    name
    0      a       1    bird   polly
    1      b       2  monkey  george

    """
    if not isinstance(objs, (DataFrame, IndexOpsMixin)):
        if not isinstance(objs, Iterable):
            raise TypeError('first argument must be an iterable of koalas objects, you passed an object of type "{name}"'.format(name=(type(objs).__name__)))
        if len(objs) == 0:
            raise ValueError('No objects to concatenate')
        objs = list(filter(lambda obj: obj is not None, objs))
        if len(objs) == 0:
            raise ValueError('All objects passed were None')
        for obj in objs:
            if not isinstance(obj, (Series, DataFrame)):
                raise TypeError("cannot concatenate object of type '{name}; only ks.Series and ks.DataFrame are valid".format(name=(type(objs).__name__)))

        axis = validate_axis(axis)
        if axis == 1:
            if isinstance(objs[0], ks.Series):
                concat_kdf = objs[0].to_frame
            else:
                concat_kdf = objs[0]
            with ks.option_context'compute.ops_on_diff_frames'True:

                def resolve_func(kdf, this_column_labels, that_column_labels):
                    duplicated_names = set((this_column_label[1:] for this_column_label in this_column_labels)).intersection(set((that_column_label[1:] for that_column_label in that_column_labels)))
                    assert len(duplicated_names) > 0, 'inner or full join type does not include non-common columns'
                    pretty_names = [name_like_string(column_label) for column_label in duplicated_names]
                    raise ValueError('Labels have to be unique; however, got duplicated labels %s.' % pretty_names)

                for kser_or_kdf in objs[1:]:
                    if isinstance(kser_or_kdf, Series):
                        that_kdf = kser_or_kdf.to_frame
                    else:
                        that_kdf = kser_or_kdf
                    this_index_level = concat_kdf._internal.column_labels_level
                    that_index_level = that_kdf._internal.column_labels_level
                    if this_index_level > that_index_level:
                        concat_kdf = that_kdf._index_normalized_frame(concat_kdf)
                    if this_index_level < that_index_level:
                        that_kdf = concat_kdf._index_normalized_frame(that_kdf)
                    if join == 'inner':
                        concat_kdf = align_diff_frames(resolve_func,
                          concat_kdf, that_kdf, fillna=False, how='inner')
                    elif join == 'outer':
                        concat_kdf = align_diff_frames(resolve_func,
                          concat_kdf, that_kdf, fillna=False, how='full')
                    else:
                        raise ValueError('Only can inner (intersect) or outer (union) join the other axis.')

            if ignore_index:
                concat_kdf.columns = list(map(str, _range(len(concat_kdf.columns))))
            return concat_kdf
        should_return_series = all(map(lambda obj: isinstance(obj, Series), objs))
        new_objs = []
        for obj in objs:
            if isinstance(obj, Series):
                obj = obj.rename('0').to_dataframe
            new_objs.append(obj)

        objs = new_objs
        column_labels_levels = set((obj._internal.column_labels_level for obj in objs))
        if len(column_labels_levels) != 1:
            raise ValueError('MultiIndex columns should have the same levels')
        if not ignore_index:
            indices_of_kdfs = [kdf.index for kdf in objs]
            index_of_first_kdf = indices_of_kdfs[0]
            for index_of_kdf in indices_of_kdfs:
                if index_of_first_kdf.names != index_of_kdf.names:
                    raise ValueError('Index type and names should be same in the objects to concatenate. You passed different indices {index_of_first_kdf} and {index_of_kdf}'.format(index_of_first_kdf=(index_of_first_kdf.names),
                      index_of_kdf=(index_of_kdf.names)))

    else:
        column_labelses_of_kdfs = [kdf._internal.column_labels for kdf in objs]
        if ignore_index:
            index_names_of_kdfs = [[] for _ in objs]
        else:
            index_names_of_kdfs = [kdf._internal.index_names for kdf in objs]
        if all((name == index_names_of_kdfs[0] for name in index_names_of_kdfs)):
            if all((idx == column_labelses_of_kdfs[0] for idx in column_labelses_of_kdfs)):
                kdfs = objs
                merged_columns = column_labelses_of_kdfs[0]
            else:
                if join == 'inner':
                    interested_columns = (set.intersection)(*map(set, column_labelses_of_kdfs))
                    merged_columns = sorted(list(map(lambda c: column_labelses_of_kdfs[0][column_labelses_of_kdfs[0].index(c)], interested_columns)))
                    kdfs = [kdf[merged_columns] for kdf in objs]
                else:
                    if join == 'outer':
                        merged_columns = sorted(list(set(itertools.chain.from_iterable(column_labelses_of_kdfs))))
                        kdfs = []
                        for kdf in objs:
                            columns_to_add = list(set(merged_columns) - set(kdf._internal.column_labels))
                            sdf = kdf._sdf
                            for label in columns_to_add:
                                sdf = sdf.withColumnname_like_string(label)F.lit(None)

                            data_columns = kdf._internal.data_spark_column_names + [name_like_string(label) for label in columns_to_add]
                            kdf = DataFrame(kdf._internal.copy(spark_frame=sdf,
                              column_labels=(kdf._internal.column_labels + columns_to_add),
                              data_spark_columns=[scol_for(sdf, col) for col in data_columns]))
                            kdfs.append(kdf[merged_columns])

                    else:
                        raise ValueError('Only can inner (intersect) or outer (union) join the other axis.')
            if ignore_index:
                sdfs = [kdf._sdf.select(kdf._internal.data_spark_columns) for kdf in kdfs]
        else:
            sdfs = [kdf._sdf.select(kdf._internal.index_spark_columns + kdf._internal.data_spark_columns) for kdf in kdfs]
    concatenated = reduce(lambda x, y: x.union(y), sdfs)
    index_map = None if ignore_index else kdfs[0]._internal.index_map
    result_kdf = DataFrame(kdfs[0]._internal.copy(spark_frame=concatenated,
      index_map=index_map,
      data_spark_columns=[scol_for(concatenated, col) for col in kdfs[0]._internal.data_spark_column_names]))
    if should_return_series:
        return _col(result_kdf)
    return result_kdf


def melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value'):
    return DataFrame.melt(frame, id_vars, value_vars, var_name, value_name)


melt.__doc__ = DataFrame.melt.__doc__

def isna(obj):
    """
    Detect missing values for an array-like object.

    This function takes a scalar or array-like object and indicates
    whether values are missing (``NaN`` in numeric arrays, ``None`` or ``NaN``
    in object arrays).

    Parameters
    ----------
    obj : scalar or array-like
        Object to check for null or missing values.

    Returns
    -------
    bool or array-like of bool
        For scalar input, returns a scalar boolean.
        For array input, returns an array of boolean indicating whether each
        corresponding element is missing.

    See Also
    --------
    notnull : Boolean inverse of pandas.isnull.
    Series.isna : Detect missing values in a Series.
    Series.isnull : Detect missing values in a Series.
    DataFrame.isna : Detect missing values in a DataFrame.
    DataFrame.isnull : Detect missing values in a DataFrame.
    Index.isna : Detect missing values in an Index.
    Index.isnull : Detect missing values in an Index.

    Examples
    --------
    Scalar arguments (including strings) result in a scalar boolean.

    >>> ks.isna('dog')
    False

    >>> ks.isna(np.nan)
    True

    ndarrays result in an ndarray of booleans.

    >>> array = np.array([[1, np.nan, 3], [4, 5, np.nan]])
    >>> array
    array([[ 1., nan,  3.],
           [ 4.,  5., nan]])
    >>> ks.isna(array)
    array([[False,  True, False],
           [False, False,  True]])

    For Series and DataFrame, the same type is returned, containing booleans.

    >>> df = ks.DataFrame({'a': ['ant', 'bee', 'cat'], 'b': ['dog', None, 'fly']})
    >>> df
         a     b
    0  ant   dog
    1  bee  None
    2  cat   fly

    >>> ks.isna(df)
           a      b
    0  False  False
    1  False   True
    2  False  False

    >>> ks.isnull(df.b)
    0    False
    1     True
    2    False
    Name: b, dtype: bool
    """
    if isinstance(obj, (DataFrame, Series)):
        return obj.isnull
    return pd.isnull(obj)


isnull = isna

def notna(obj):
    """
    Detect existing (non-missing) values.

    Return a boolean same-sized object indicating if the values are not NA.
    Non-missing values get mapped to True. NA values, such as None or
    :attr:`numpy.NaN`, get mapped to False values.

    Returns
    -------
    bool or array-like of bool
        Mask of bool values for each element that
        indicates whether an element is not an NA value.

    See Also
    --------
    isna : Detect missing values for an array-like object.
    Series.notna : Boolean inverse of Series.isna.
    Series.notnull :Boolean inverse of Series.isnull.
    DataFrame.notna :Boolean inverse of DataFrame.isna.
    DataFrame.notnull : Boolean inverse of DataFrame.isnull.
    Index.notna : Boolean inverse of Index.isna.
    Index.notnull : Boolean inverse of Index.isnull.

    Examples
    --------
    Show which entries in a DataFrame are not NA.

    >>> df = ks.DataFrame({'age': [5, 6, np.NaN],
    ...                    'born': [pd.NaT, pd.Timestamp('1939-05-27'),
    ...                             pd.Timestamp('1940-04-25')],
    ...                    'name': ['Alfred', 'Batman', ''],
    ...                    'toy': [None, 'Batmobile', 'Joker']})
    >>> df
       age       born    name        toy
    0  5.0        NaT  Alfred       None
    1  6.0 1939-05-27  Batman  Batmobile
    2  NaN 1940-04-25              Joker

    >>> df.notnull()
         age   born  name    toy
    0   True  False  True  False
    1   True   True  True   True
    2  False   True  True   True

    Show which entries in a Series are not NA.

    >>> ser = ks.Series([5, 6, np.NaN])
    >>> ser
    0    5.0
    1    6.0
    2    NaN
    Name: 0, dtype: float64

    >>> ks.notna(ser)
    0     True
    1     True
    2    False
    Name: 0, dtype: bool

    >>> ks.notna(ser.index)
    True
    """
    if isinstance(obj, (DataFrame, Series)):
        return obj.notna
    return pd.notna(obj)


notnull = notna

def merge(obj, right: 'DataFrame', how: str='inner', on: Union[(str, List[str], Tuple[(str, ...)], List[Tuple[(str, ...)]])]=None, left_on: Union[(str, List[str], Tuple[(str, ...)], List[Tuple[(str, ...)]])]=None, right_on: Union[(str, List[str], Tuple[(str, ...)], List[Tuple[(str, ...)]])]=None, left_index: bool=False, right_index: bool=False, suffixes: Tuple[(str, str)]=('_x', '_y')) -> 'DataFrame':
    """
    Merge DataFrame objects with a database-style join.

    The index of the resulting DataFrame will be one of the following:
        - 0...n if no index is used for merging
        - Index of the left DataFrame if merged only on the index of the right DataFrame
        - Index of the right DataFrame if merged only on the index of the left DataFrame
        - All involved indices if merged using the indices of both DataFrames
            e.g. if `left` with indices (a, x) and `right` with indices (b, x), the result will
            be an index (x, a, b)

    Parameters
    ----------
    right: Object to merge with.
    how: Type of merge to be performed.
        {'left', 'right', 'outer', 'inner'}, default 'inner'

        left: use only keys from left frame, similar to a SQL left outer join; preserve key
            order.
        right: use only keys from right frame, similar to a SQL right outer join; preserve key
            order.
        outer: use union of keys from both frames, similar to a SQL full outer join; sort keys
            lexicographically.
        inner: use intersection of keys from both frames, similar to a SQL inner join;
            preserve the order of the left keys.
    on: Column or index level names to join on. These must be found in both DataFrames. If on
        is None and not merging on indexes then this defaults to the intersection of the
        columns in both DataFrames.
    left_on: Column or index level names to join on in the left DataFrame. Can also
        be an array or list of arrays of the length of the left DataFrame.
        These arrays are treated as if they are columns.
    right_on: Column or index level names to join on in the right DataFrame. Can also
        be an array or list of arrays of the length of the right DataFrame.
        These arrays are treated as if they are columns.
    left_index: Use the index from the left DataFrame as the join key(s). If it is a
        MultiIndex, the number of keys in the other DataFrame (either the index or a number of
        columns) must match the number of levels.
    right_index: Use the index from the right DataFrame as the join key. Same caveats as
        left_index.
    suffixes: Suffix to apply to overlapping column names in the left and right side,
        respectively.

    Returns
    -------
    DataFrame
        A DataFrame of the two merged objects.

    Examples
    --------

    >>> df1 = ks.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
    ...                     'value': [1, 2, 3, 5]},
    ...                    columns=['lkey', 'value'])
    >>> df2 = ks.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
    ...                     'value': [5, 6, 7, 8]},
    ...                    columns=['rkey', 'value'])
    >>> df1
      lkey  value
    0  foo      1
    1  bar      2
    2  baz      3
    3  foo      5
    >>> df2
      rkey  value
    0  foo      5
    1  bar      6
    2  baz      7
    3  foo      8

    Merge df1 and df2 on the lkey and rkey columns. The value columns have
    the default suffixes, _x and _y, appended.

    >>> merged = ks.merge(df1, df2, left_on='lkey', right_on='rkey')
    >>> merged.sort_values(by=['lkey', 'value_x', 'rkey', 'value_y'])  # doctest: +ELLIPSIS
      lkey  value_x rkey  value_y
    ...bar        2  bar        6
    ...baz        3  baz        7
    ...foo        1  foo        5
    ...foo        1  foo        8
    ...foo        5  foo        5
    ...foo        5  foo        8

    >>> left_kdf = ks.DataFrame({'A': [1, 2]})
    >>> right_kdf = ks.DataFrame({'B': ['x', 'y']}, index=[1, 2])

    >>> ks.merge(left_kdf, right_kdf, left_index=True, right_index=True).sort_index()
       A  B
    1  2  x

    >>> ks.merge(left_kdf, right_kdf, left_index=True, right_index=True, how='left').sort_index()
       A     B
    0  1  None
    1  2     x

    >>> ks.merge(left_kdf, right_kdf, left_index=True, right_index=True, how='right').sort_index()
         A  B
    1  2.0  x
    2  NaN  y

    >>> ks.merge(left_kdf, right_kdf, left_index=True, right_index=True, how='outer').sort_index()
         A     B
    0  1.0  None
    1  2.0     x
    2  NaN     y

    Notes
    -----
    As described in #263, joining string columns currently returns None for missing values
        instead of NaN.
    """
    return obj.merge(right,
      how=how,
      on=on,
      left_on=left_on,
      right_on=right_on,
      left_index=left_index,
      right_index=right_index,
      suffixes=suffixes)


def to_numeric(arg):
    """
    Convert argument to a numeric type.

    Parameters
    ----------
    arg : scalar, list, tuple, 1-d array, or Series

    Returns
    -------
    ret : numeric if parsing succeeded.

    See Also
    --------
    DataFrame.astype : Cast argument to a specified dtype.
    to_datetime : Convert argument to datetime.
    to_timedelta : Convert argument to timedelta.
    numpy.ndarray.astype : Cast a numpy array to a specified type.

    Examples
    --------

    >>> kser = ks.Series(['1.0', '2', '-3'])
    >>> kser
    0    1.0
    1      2
    2     -3
    Name: 0, dtype: object

    >>> ks.to_numeric(kser)
    0    1.0
    1    2.0
    2   -3.0
    Name: 0, dtype: float32

    If given Series contains invalid value to cast float, just cast it to `np.nan`

    >>> kser = ks.Series(['apple', '1.0', '2', '-3'])
    >>> kser
    0    apple
    1      1.0
    2        2
    3       -3
    Name: 0, dtype: object

    >>> ks.to_numeric(kser)
    0    NaN
    1    1.0
    2    2.0
    3   -3.0
    Name: 0, dtype: float32

    Also support for list, tuple, np.array, or a scalar

    >>> ks.to_numeric(['1.0', '2', '-3'])
    array([ 1.,  2., -3.])

    >>> ks.to_numeric(('1.0', '2', '-3'))
    array([ 1.,  2., -3.])

    >>> ks.to_numeric(np.array(['1.0', '2', '-3']))
    array([ 1.,  2., -3.])

    >>> ks.to_numeric('1.0')
    1.0
    """
    if isinstance(arg, Series):
        return arg._with_new_scol(arg._internal.spark_column.cast('float'))
    return pd.to_numeric(arg)


def broadcast(obj):
    """
    Marks a DataFrame as small enough for use in broadcast joins.

    Parameters
    ----------
    obj : DataFrame

    Returns
    -------
    ret : DataFrame with broadcast hint.

    See Also
    --------
    DataFrame.merge : Merge DataFrame objects with a database-style join.
    DataFrame.join : Join columns of another DataFrame.
    DataFrame.update : Modify in place using non-NA values from another DataFrame.

    Examples
    --------
        >>> df1 = ks.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
        ...                     'value': [1, 2, 3, 5]},
        ...                    columns=['lkey', 'value'])
        >>> df2 = ks.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
        ...                     'value': [5, 6, 7, 8]},
        ...                    columns=['rkey', 'value'])
        >>> merged = df1.merge(ks.broadcast(df2), left_on='lkey', right_on='rkey')
        >>> merged.explain()  # doctest: +ELLIPSIS
        == Physical Plan ==
        ...
        ...BroadcastHashJoin...
        ...
    """
    if not isinstance(obj, DataFrame):
        raise ValueError('Invalid type : expected DataFrame got {}'.format(type(obj)))
    return DataFrame(obj._internal.with_new_sdf(F.broadcast(obj._sdf)))


@pandas_wraps
def _to_datetime1(arg, errors, format, unit, infer_datetime_format, origin) -> Series[np.datetime64]:
    return pd.to_datetime(arg,
      errors=errors,
      format=format,
      unit=unit,
      infer_datetime_format=infer_datetime_format,
      origin=origin)


@pandas_wraps
def _to_datetime2(arg_year, arg_month, arg_day, errors, format, unit, infer_datetime_format, origin) -> Series[np.datetime64]:
    arg = dict(year=arg_year, month=arg_month, day=arg_day)
    for key in arg:
        if arg[key] is None:
            del arg[key]

    return pd.to_datetime(arg,
      errors=errors,
      format=format,
      unit=unit,
      infer_datetime_format=infer_datetime_format,
      origin=origin)


def _get_index_map(sdf: spark.DataFrame, index_col: Optional[Union[(str, List[str])]]=None):
    if index_col is not None:
        if isinstance(index_col, str):
            index_col = [
             index_col]
        sdf_columns = set(sdf.columns)
        for col in index_col:
            if col not in sdf_columns:
                raise KeyError(col)

        index_map = OrderedDict(((col, (col,)) for col in index_col))
    else:
        index_map = None
    return index_map


_get_dummies_default_accept_types = (
 DecimalType, StringType, DateType)
_get_dummies_acceptable_types = _get_dummies_default_accept_types + (
 ByteType,
 ShortType,
 IntegerType,
 LongType,
 FloatType,
 DoubleType,
 BooleanType,
 TimestampType)