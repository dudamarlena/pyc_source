# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/ssm/dynamic_glm.py
# Compiled at: 2018-02-01 11:59:15
from .. import families as fam
from .. import tsm
from .dynlin import *
from .ndynlin import *

class DynamicGLM(tsm.TSM):
    """ Wrapper for dynamic GLM models

    Parameters
    ----------
    formula : str
        Patsy string specifying the regression

    data : pd.DataFrame or np.array
        Field to specify the time series data that will be used.

    family : 
        e.g. pf.Normal(0,1)
    """

    def __new__(cls, formula, data, family):
        if isinstance(family, fam.Normal):
            return DynReg(formula=formula, data=data)
        else:
            return NDynReg(formula=formula, data=data, family=family)

    def __init__(self, formula, data, family):
        pass