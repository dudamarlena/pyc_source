# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/DataMining.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 1146 bytes
import os, sys
from sklearn import linear_model
import numpy as np, string

def LinearRegression(ModelValues, Variable='DimX*DimY'):
    """
        Return dictionary of string linear mathematical expression for each values type in ModelValues.
        """
    ModelTemplate = string.Template('${Slope}*' + str(Variable) + '+${Intercept}')
    LinearExpressions = {}
    Colors = ('blue', 'red', 'green')
    for RscType, Values in ModelValues.items():
        if len(Values) == 0:
            pass
        else:
            X, Y = [], []
            for x, y in Values:
                X.append(x)
                Y.append(y)

            X = np.array(X)
            Y = np.array(Y)
            Regression = linear_model.LinearRegression()
            Regression.fit(X[:, np.newaxis], Y)
            LinearExpressions[RscType] = ModelTemplate.safe_substitute(Slope='{0:.3f}'.format(float(Regression.coef_)), Intercept='({0:.3f})'.format(float(Regression.intercept_)))

    return LinearExpressions