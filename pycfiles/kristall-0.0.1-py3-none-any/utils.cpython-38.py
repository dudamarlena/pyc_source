# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jazg/work/kristall/src/kristall/utils.py
# Compiled at: 2020-01-20 09:54:47
# Size of source mod 2**32: 650 bytes
import inspect
from typing import Type, Union

def endpoint(item: Union[(object, Type)]) -> str:
    """Endpoint generation function. Returns fully qualified class name in
    dotted notation.

    :param item: item to generate endpoint for, may be either instance or
                 class
    :type item: Union[object, Type]
    :return: fully qualified class name, suitable for use as endpoint name
    :rtype: str
    """
    if inspect.isclass(item):
        mname = item.__module__
        cqname = item.__qualname__
    else:
        mname = item.__class__.__module__
        cqname = item.__class__.__qualname__
    return f"{mname}.{cqname}"