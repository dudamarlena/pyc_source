# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/util/formatter.py
# Compiled at: 2019-08-19 15:09:29
__all__ = [
 'tangoFormatter']
from taurus.core.units import Quantity

def tangoFormatter(dtype=None, **kwargs):
    """
    The tango formatter callable. Returns a format string based on
    the `format` Tango Attribute configuration (Display.Format in Tango DB)

    :param dtype: (type) type of the value object
    :param kwargs: other keyword arguments (ignored)

    :return: the string formatting
    """
    if dtype is Quantity:
        fmt = '{:~{bc.modelObj.format_spec}}'
    else:
        fmt = '{:{bc.modelObj.format_spec}}'
    return fmt