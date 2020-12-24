# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/DemandFunction.py
# Compiled at: 2007-04-18 06:57:54


def getLinearDemandFunction(constant, slope):

    def df(price):
        return max(0.0, constant + slope * price)

    return df