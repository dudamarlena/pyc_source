# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/path_part_sdvs.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 584 bytes
"""
All construction of :class:`PathPartResolver` should be done via this module.

Import qualified!
"""
from exactly_lib.symbol.data.path_sdv import PathPartSdv
from exactly_lib.symbol.data.path_sdv_impls import path_part_sdvs as _impl
from exactly_lib.symbol.data.string_sdv import StringSdv

def empty() -> PathPartSdv:
    return _impl.PathPartSdvAsNothing()


def from_constant_str(file_name: str) -> PathPartSdv:
    return _impl.PathPartSdvAsConstantPath(file_name)


def from_string(string_sdv: StringSdv) -> PathPartSdv:
    return _impl.PathPartSdvAsStringSdv(string_sdv)