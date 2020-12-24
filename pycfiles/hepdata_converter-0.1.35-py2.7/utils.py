# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/writers/utils.py
# Compiled at: 2020-03-05 14:33:22


def error_value_processor(value, error):
    """
    If an error is a percentage, we convert to a float, then
    calculate the percentage of the supplied value.

    :param value: base value, e.g. 10
    :param error: e.g. 20.0%
    :return: the absolute error, e.g. 12 for the above case.
    """
    if isinstance(error, (str, unicode)):
        try:
            if '%' in error:
                error_float = float(error.replace('%', ''))
                error_abs = value / 100 * error_float
                return error_abs
            if error == '':
                error = 0.0
            else:
                error = float(error)
        except:
            pass

    return error