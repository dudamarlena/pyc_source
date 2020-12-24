# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\appli\Documents\GitHub\AlphaVantageAPI\alphaVantageAPI\validate_parameters.py
# Compiled at: 2019-09-29 14:24:31
# Size of source mod 2**32: 5319 bytes
import math

def _validate_parameters(api_indicator_matype, option, parameters: dict, **kwargs):
    """Validates kwargs and attaches them to parameters."""
    matype = int(math.fabs(kwargs['matype'])) if 'matype' in kwargs else None
    if option == 'matype':
        if matype is not None:
            if matype in api_indicator_matype:
                parameters['matype'] = matype
    nbdevup = math.fabs(kwargs['nbdevup']) if 'nbdevup' in kwargs else None
    nbdevdn = math.fabs(kwargs['nbdevdn']) if 'nbdevdn' in kwargs else None
    if option == 'nbdevup':
        if nbdevup is not None:
            parameters['nbdevup'] = nbdevup
    if option == 'nbdevdn':
        if nbdevdn is not None:
            parameters['nbdevdn'] = nbdevdn
    timeperiod1 = int(math.fabs(kwargs['timeperiod1'])) if 'timeperiod1' in kwargs else None
    timeperiod2 = int(math.fabs(kwargs['timeperiod2'])) if 'timeperiod2' in kwargs else None
    timeperiod3 = int(math.fabs(kwargs['timeperiod3'])) if 'timeperiod3' in kwargs else None
    if option == 'timeperiod1':
        if timeperiod1 is not None:
            parameters['timeperiod1'] = timeperiod1
    if option == 'timeperiod2':
        if timeperiod2 is not None:
            parameters['timeperiod2'] = timeperiod2
    if option == 'timeperiod3':
        if timeperiod3 is not None:
            parameters['timeperiod3'] = timeperiod3
    acceleration = math.fabs(float(kwargs['acceleration'])) if 'acceleration' in kwargs else None
    maximum = math.fabs(float(kwargs['maximum'])) if 'maximum' in kwargs else None
    if option == 'acceleration':
        if acceleration is not None:
            parameters['acceleration'] = acceleration
    if option == 'maximum':
        if maximum is not None:
            parameters['maximum'] = maximum
    fastlimit = math.fabs(float(kwargs['fastlimit'])) if 'fastlimit' in kwargs else None
    slowlimit = math.fabs(float(kwargs['slowlimit'])) if 'slowlimit' in kwargs else None
    if option == 'fastlimit':
        if fastlimit is not None:
            if fastlimit > 0:
                if fastlimit < 1:
                    parameters['fastlimit'] = fastlimit
    if option == 'slowlimit':
        if slowlimit is not None:
            if slowlimit > 0:
                if slowlimit < 1:
                    parameters['slowlimit'] = slowlimit
    fastperiod = int(math.fabs(kwargs['fastperiod'])) if 'fastperiod' in kwargs else None
    slowperiod = int(math.fabs(kwargs['slowperiod'])) if 'slowperiod' in kwargs else None
    signalperiod = int(math.fabs(kwargs['signalperiod'])) if 'signalperiod' in kwargs else None
    if option == 'fastperiod':
        if fastperiod is not None:
            parameters['fastperiod'] = fastperiod
    if option == 'slowperiod':
        if slowperiod is not None:
            parameters['slowperiod'] = slowperiod
    if option == 'signalperiod':
        if signalperiod is not None:
            parameters['signalperiod'] = signalperiod
    fastmatype = int(math.fabs(kwargs['fastmatype'])) if 'fastmatype' in kwargs else None
    slowmatype = int(math.fabs(kwargs['slowmatype'])) if 'slowmatype' in kwargs else None
    signalmatype = int(math.fabs(kwargs['signalmatype'])) if 'signalmatype' in kwargs else None
    if option == 'fastmatype':
        if fastmatype is not None:
            if fastmatype in api_indicator_matype:
                parameters['fastmatype'] = fastmatype
    if option == 'slowmatype':
        if slowmatype is not None:
            if slowmatype in api_indicator_matype:
                parameters['slowmatype'] = slowmatype
    if option == 'signalmatype':
        if signalmatype is not None:
            if signalmatype in api_indicator_matype:
                parameters['signalmatype'] = signalmatype
    fastkperiod = int(math.fabs(kwargs['fastkperiod'])) if 'fastkperiod' in kwargs else None
    fastdperiod = int(math.fabs(kwargs['fastdperiod'])) if 'fastdperiod' in kwargs else None
    fastdmatype = int(math.fabs(kwargs['fastdmatype'])) if 'fastdmatype' in kwargs else None
    if option == 'fastkperiod':
        if fastkperiod is not None:
            parameters['fastkperiod'] = fastkperiod
    if option == 'fastdperiod':
        if fastdperiod is not None:
            parameters['fastdperiod'] = fastdperiod
    if option == 'fastdmatype':
        if fastdmatype is not None:
            if fastdmatype in api_indicator_matype:
                parameters['fastdmatype'] = fastdmatype
    slowkperiod = int(math.fabs(kwargs['slowkperiod'])) if 'slowkperiod' in kwargs else None
    slowdperiod = int(math.fabs(kwargs['slowdperiod'])) if 'slowdperiod' in kwargs else None
    slowkmatype = int(math.fabs(kwargs['slowkmatype'])) if 'slowkmatype' in kwargs else None
    slowdmatype = int(math.fabs(kwargs['slowdmatype'])) if 'slowdmatype' in kwargs else None
    if option == 'slowkperiod':
        if slowkperiod is not None:
            parameters['slowkperiod'] = slowkperiod
    if option == 'slowdperiod':
        if slowdperiod is not None:
            parameters['slowdperiod'] = slowdperiod
    if option == 'slowkmatype':
        if slowkmatype is not None:
            if slowkmatype in api_indicator_matype:
                parameters['slowkmatype'] = slowkmatype
    if option == 'slowdmatype':
        if slowdmatype is not None:
            if slowdmatype in api_indicator_matype:
                parameters['slowdmatype'] = slowdmatype
    return parameters