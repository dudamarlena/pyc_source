# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/ssm/local_level.py
# Compiled at: 2018-02-01 11:59:15
from .. import families as fam
from .. import tsm
from .llm import *
from .nllm import *

class LocalLevel(tsm.TSM):
    """ Wrapper for local level models

    **** LOCAL LEVEL MODEL ****

    Parameters
    ----------
    data : pd.DataFrame or np.array
        Field to specify the time series data that will be used.

    integ : int (default : 0)
        Specifies how many times to difference the time series.

    target : str (pd.DataFrame) or int (np.array)
        Specifies which column name or array index to use. By default, first
        column/array will be selected as the dependent variable.

    family : 
        e.g. pf.Normal(0,1)
    """

    def __new__(cls, data, family, integ=0, target=None):
        if isinstance(family, fam.Normal):
            return LLEV(data=data, integ=integ, target=target)
        else:
            return NLLEV(data=data, family=family, integ=integ, target=target)

    def __init__(self, data, family, integ=0, target=None):
        pass