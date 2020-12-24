# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/specs.py
# Compiled at: 2018-04-20 03:19:42
import functools, operator
from galaxy import util

def to_str_or_none(value):
    if value is None:
        return
    else:
        return str(value)
        return


def to_bool_or_none(value):
    return util.string_as_bool_or_none(value)


def to_bool(value):
    return util.asbool(value)


def to_float_or_none(value):
    if value is None:
        return
    else:
        return float(value)
        return


def is_in(*args):
    return functools.partial(operator.contains, args)