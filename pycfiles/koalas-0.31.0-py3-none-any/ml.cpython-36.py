# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/ml.py
# Compiled at: 2019-09-06 16:01:33
# Size of source mod 2**32: 3005 bytes
from typing import List, Tuple, TYPE_CHECKING
import numpy as np, pandas as pd, pyspark
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
if TYPE_CHECKING:
    import databricks.koalas as ks
CORRELATION_OUTPUT_COLUMN = '_correlation_output'

def corr(kdf: 'ks.DataFrame', method: str='pearson') -> pd.DataFrame:
    """
    The correlation matrix of all the numerical columns of this dataframe.

    Only accepts scalar numerical values for now.

    :param kdf: the koalas dataframe.
    :param method: {'pearson', 'spearman'}
                   * pearson : standard correlation coefficient
                   * spearman : Spearman rank correlation
    :return: :class:`pandas.DataFrame`

    >>> ks.DataFrame({'A': [0, 1], 'B': [1, 0], 'C': ['x', 'y']}).corr()
         A    B
    A  1.0 -1.0
    B -1.0  1.0
    """
    assert method in ('pearson', 'spearman')
    ndf, fields = to_numeric_df(kdf)
    corr = Correlation.corr(ndf, CORRELATION_OUTPUT_COLUMN, method)
    pcorr = corr.toPandas()
    arr = pcorr.iloc[(0, 0)].toArray()
    arr = pd.DataFrame(arr)
    arr.columns = fields
    arr = arr.set_index(pd.Index(fields))
    return arr


def to_numeric_df(kdf: 'ks.DataFrame') -> Tuple[(pyspark.sql.DataFrame, List[str])]:
    """
    Takes a dataframe and turns it into a dataframe containing a single numerical
    vector of doubles. This dataframe has a single field called '_1'.

    TODO: index is not preserved currently
    :param kdf: the koalas dataframe.
    :return: a pair of dataframe, list of strings (the name of the columns
             that were converted to numerical types)

    >>> to_numeric_df(ks.DataFrame({'A': [0, 1], 'B': [1, 0], 'C': ['x', 'y']}))
    (DataFrame[_correlation_output: vector], ['A', 'B'])
    """
    accepted_types = {np.dtype(dt) for dt in [np.int8, np.int16, np.int32, np.int64,
     np.float32, np.float64, np.bool_]}
    numeric_fields = [fname for fname in kdf._internal.data_columns if kdf[fname].dtype in accepted_types]
    numeric_df = (kdf._sdf.select)(*[kdf._internal.scol_for(fname) for fname in numeric_fields])
    va = VectorAssembler(inputCols=numeric_fields, outputCol=CORRELATION_OUTPUT_COLUMN)
    v = va.transform(numeric_df).select(CORRELATION_OUTPUT_COLUMN)
    return (v, numeric_fields)