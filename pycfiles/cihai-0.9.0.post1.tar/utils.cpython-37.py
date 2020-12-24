# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/t/work/cihai/cihai/cihai/utils.py
# Compiled at: 2019-08-17 10:48:09
# Size of source mod 2**32: 3864 bytes
"""
Utility and helper methods for cihai.
"""
from __future__ import absolute_import, print_function, unicode_literals
import sys
from . import exc
from ._compat import collections_abc, reraise

def merge_dict(base, additional):
    """
    Combine two dictionary-like objects.

    Notes
    -----
    Code from https://github.com/pypa/warehouse
    Copyright 2013 Donald Stufft

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    """
    if base is None:
        return additional
    else:
        if additional is None:
            return base
        return isinstance(base, collections_abc.Mapping) and isinstance(additional, collections_abc.Mapping) or additional
    merged = base
    for key, value in additional.items():
        if isinstance(value, collections_abc.Mapping):
            merged[key] = merge_dict(merged.get(key), value)
        else:
            merged[key] = value

    return merged


def supports_wide():
    """Return affirmative if python interpreter supports wide characters.

    Returns
    -------
    bool :
        True if python supports wide character sets
    """
    return sys.maxunicode > 65535


def import_string(import_name, silent=False):
    """
    Imports an object based on a string.

    This is useful if you want to use import paths as endpoints or
    something similar.  An import path can  be specified either in dotted
    notation (``xml.sax.saxutils.escape``) or with a colon as object
    delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    Parameters
    ----------
    import_name : string
        the dotted name for the object to import.
    silent : bool
        if set to `True` import errors are ignored and `None` is returned instead.

    Returns
    -------
    imported object

    Raises
    ------
    cihai.exc.ImportStringError (ImportError, cihai.exc.CihaiException)

    Notes
    -----
    This is from werkzeug.utils c769200 on May 23, LICENSE BSD.
    https://github.com/pallets/werkzeug

    Changes:
    - Exception raised is cihai.exc.ImportStringError
    - Add NOQA C901 to avoid complexity lint
    - Format with black
    """
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]
            module_name, obj_name = import_name.rsplit('.', 1)
            try:
                module = __import__(module_name, None, None, [obj_name])
            except ImportError:
                module = import_string(module_name)

            try:
                return getattr(module, obj_name)
            except AttributeError as e:
                try:
                    raise ImportError(e)
                finally:
                    e = None
                    del e

    except ImportError as e:
        try:
            if not silent:
                reraise(exc.ImportStringError, exc.ImportStringError(import_name, e), sys.exc_info()[2])
        finally:
            e = None
            del e