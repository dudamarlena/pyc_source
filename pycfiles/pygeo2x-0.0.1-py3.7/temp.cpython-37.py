# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pygeo2x\temp.py
# Compiled at: 2019-05-17 07:49:31
# Size of source mod 2**32: 1941 bytes


def convert_temperature(val, old_scale='fahrenheit', new_scale='celsius'):
    """
    Convert from a temperatuure scale to another one among Celsius, Kelvin
    and Fahrenheit.

    Parameters
    ----------
    val: float or int
        Value of the temperature to be converted expressed in the original
        scale.

    old_scale: str
        Original scale from which the temperature value will be converted.
        Supported scales are Celsius ['Celsius', 'celsius', 'c'],
        Kelvin ['Kelvin', 'kelvin', 'k'] or Fahrenheit ['Fahrenheit',
        'fahrenheit', 'f'].

    new_scale: str
        New scale from which the temperature value will be converted.
        Supported scales are Celsius ['Celsius', 'celsius', 'c'],
        Kelvin ['Kelvin', 'kelvin', 'k'] or Fahrenheit ['Fahrenheit',
        'fahrenheit', 'f'].

    Raises
    -------
    NotImplementedError if either of the scales are not one implemented

    Returns
    -------
    res: float
        Value of the converted temperature expressed in the new scale.
    """
    if old_scale.lower() in ('celsius', 'c'):
        temp = val + 273.15
    else:
        if old_scale.lower() in ('kelvin', 'k'):
            temp = val
        else:
            if old_scale.lower() in ('fahrenheit', 'f'):
                temp = 5.0 * (val - 32) / 9.0 + 273.15
            else:
                raise AttributeError(f"{old_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported")
    if new_scale.lower() in ('celsius', 'c'):
        result = temp - 273.15
    else:
        if new_scale.lower() in ('kelvin', 'k'):
            result = temp
        else:
            if new_scale.lower() in ('fahrenheit', 'f'):
                result = (temp - 273.15) * 9.0 / 5.0 + 32
            else:
                raise AttributeError(f"{new_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported")
    return result