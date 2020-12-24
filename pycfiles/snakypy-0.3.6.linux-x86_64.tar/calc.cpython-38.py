# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/calc.py
# Compiled at: 2020-03-21 13:30:36
# Size of source mod 2**32: 2979 bytes
from snakypy.utils.calc import BMI

def bmi(sex, weight, height):
    """
    This function is responsible for calling the class of body mass index (BMI).

    >>> from snakypy.calc import bmi
    >>> bmi('m', 60, 1.73)

    **output:**

    .. code-block:: shell

        'Under weight.'

    Arguments:
        **sex {str}** -- You must receive a string with a single character.                      The string must be either "**m**" for "male" or "**f**" for "female"

        **weight {float}** -- You should receive a float, this is where you put the                           weight. **E.g:** 60.4

        **height {float}** -- You should receive a float, this is where you put the                           height. **E.g:** 1.73

    Returns:
        **[object]** -- The return will be a string informing the result or a false Boolean,                     if the arguments are wrong.
    """
    return BMI(sex, weight, height).main()


def percentage(per, whole, *, operation=None, log=False):
    """
    This function will calculate a whole with a certain percentage value.

    >>> from snakypy.calc import percentage
    >>> percentage(25, 500)
    >>> percentage(25, 500, log=True)
    >>> percentage(25, 500, operation='+')
    >>> percentage(25, 500, operation='-')
    >>> percentage(25, 500, operation='+', log=True)
    >>> percentage(25, 500, operation='-', log=True)

    **output:**

    .. code-block:: shell

        125
        '>> 25% of 500 = 125.00'
        625.00
        375.00
        '>> 500 + 25% = 625.00'
        '>> 500 - 25% = 375.00'

    Arguments:

        **per {float}** -- Input argument that should receive a float representing                        a certain percentage value.

        **whole {float}** -- Input argument that should receive a float representing                          total value.

    Keyword Arguments:

        **operation {str}** -- This named parameter must receive two types of string                            values. One is the plus sign ('+') that will add the total                            to the imposed percentage. The other is the minus sign ('-'),                            which subtracts the total value from the imposed percentage                            value. (default: {None})

        **log {bool}** -- If this parameter is of the value True, then the return will be                      a custom string with the percent signs and the operation.                      (default: {False})
    """
    option = {'+':lambda : whole + whole * (per / 100), 
     '-':lambda : whole - whole * (per / 100)}.get(operation, lambda : whole * (per / 100))()
    if log:
        if operation == '+':
            return f">> {whole} + {per}% = {option:.2f}"
        if operation == '-':
            return f">> {whole} - {per}% = {option:.2f}"
        return f">> {per}% of {whole} = {option:.2f}"
    return option


__all__ = [
 'bmi', 'percentage']