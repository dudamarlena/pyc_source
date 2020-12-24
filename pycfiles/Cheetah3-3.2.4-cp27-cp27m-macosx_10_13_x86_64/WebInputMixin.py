# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/WebInputMixin.py
# Compiled at: 2019-09-22 10:12:27
"""Provides helpers for Template.webInput(), a method for importing web
transaction variables in bulk.  See the docstring of webInput for full details.
"""
from Cheetah.Utils.Misc import useOrRaise

class NonNumericInputError(ValueError):
    pass


class _Converter:
    """A container object for info about type converters.
    .name, string, name of this converter (for error messages).
    .func, function, factory function.
    .default, value to use or raise if the real value is missing.
    .error, value to use or raise if .func() raises an exception.
    """

    def __init__(self, name, func, default, error):
        self.name = name
        self.func = func
        self.default = default
        self.error = error


def _lookup(name, func, multi, converters):
    """Look up a Webware field/cookie/value/session value.  Return
    '(realName, value)' where 'realName' is like 'name' but with any
    conversion suffix strips off.  Applies numeric conversion and
    single vs multi values according to the comments in the source.
    """
    colon = name.find(':')
    if colon != -1:
        longName = name
        shortName, ext = name[:colon], name[colon + 1:]
    else:
        longName = shortName = name
        ext = ''
    if longName != shortName:
        values = func(longName, None) or func(shortName, None)
    else:
        values = func(shortName, None)
    if values is None:
        values = []
    else:
        if isinstance(values, str):
            values = [
             values]
        try:
            converter = converters[ext]
        except KeyError:
            fmt = "'%s' is not a valid converter name in '%s'"
            tup = (ext, longName)
            raise TypeError(fmt % tup)

    if converter.func is not None:
        tmp = values[:]
        values = []
        for elm in tmp:
            try:
                elm = converter.func(elm)
            except (TypeError, ValueError):
                tup = (
                 converter.name, elm)
                errmsg = "%s '%s' contains invalid characters" % tup
                elm = useOrRaise(converter.error, errmsg)

            values.append(elm)

    if multi:
        return (shortName, values)
    else:
        if len(values) == 0:
            return (shortName, useOrRaise(converter.default))
        return (
         shortName, values[0])