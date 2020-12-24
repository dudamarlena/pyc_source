# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/utils/temputils.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 3043 bytes
"""
Module containing utility functions for temperature and wind units conversion
"""
KELVIN_OFFSET = 273.15
FAHRENHEIT_OFFSET = 32.0
FAHRENHEIT_DEGREE_SCALE = 1.8
MILES_PER_HOUR_FOR_ONE_METER_PER_SEC = 2.23694

def kelvin_dict_to(d, target_temperature_unit):
    """
    Converts all the values in a dict from Kelvin temperatures to the
    specified temperature format.

    :param d: the dictionary containing Kelvin temperature values
    :type d: dict
    :param target_temperature_unit: the target temperature unit, may be:
        'celsius' or 'fahrenheit'
    :type target_temperature_unit: str
    :returns: a dict with the same keys as the input dict and converted
        temperature values as values
    :raises: *ValueError* when unknown target temperature units are provided

    """
    if target_temperature_unit == 'kelvin':
        return d
    if target_temperature_unit == 'celsius':
        return {key:kelvin_to_celsius(d[key]) for key in d}
    if target_temperature_unit == 'fahrenheit':
        return {key:kelvin_to_fahrenheit(d[key]) for key in d}
    raise ValueError('Invalid value for target temperature conversion                          unit')


def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Celsius temperature
    :raises: *TypeError* when bad argument types are provided

    """
    if kelvintemp < 0:
        raise ValueError(__name__ + ': negative temperature values not allowed')
    celsiustemp = kelvintemp - KELVIN_OFFSET
    return float('{0:.2f}'.format(celsiustemp))


def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Fahrenheit temperature

    :raises: *TypeError* when bad argument types are provided
    """
    if kelvintemp < 0:
        raise ValueError(__name__ + ': negative temperature values not allowed')
    fahrenheittemp = (kelvintemp - KELVIN_OFFSET) * FAHRENHEIT_DEGREE_SCALE + FAHRENHEIT_OFFSET
    return float('{0:.2f}'.format(fahrenheittemp))


def metric_wind_dict_to_imperial(d):
    """
    Converts all the wind values in a dict from meters/sec (metric measurement 
    system) to miles/hour (imperial measurement system)
    .

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to miles/hour

    """
    result = dict()
    for key, value in d.items():
        if key != 'deg':
            result[key] = value * MILES_PER_HOUR_FOR_ONE_METER_PER_SEC
        else:
            result[key] = value

    return result