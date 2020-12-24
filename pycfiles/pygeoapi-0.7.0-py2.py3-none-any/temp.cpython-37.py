# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    elif old_scale.lower() in ('kelvin', 'k'):
        temp = val
    elif old_scale.lower() in ('fahrenheit', 'f'):
        temp = 5.0 * (val - 32) / 9.0 + 273.15
    else:
        raise AttributeError(f"{old_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported")
    if new_scale.lower() in ('celsius', 'c'):
        result = temp - 273.15
    elif new_scale.lower() in ('kelvin', 'k'):
        result = temp
    elif new_scale.lower() in ('fahrenheit', 'f'):
        result = (temp - 273.15) * 9.0 / 5.0 + 32
    else:
        raise AttributeError(f"{new_scale} is unsupported. Celsius, Kelvin and Fahrenheit are supported")
    return result