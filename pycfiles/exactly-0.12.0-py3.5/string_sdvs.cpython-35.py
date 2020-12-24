# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/string_sdvs.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1629 bytes
"""
Import qualified!
"""
from typing import Iterable
from exactly_lib.symbol import symbol_usage as su
from exactly_lib.symbol.data.impl import string_sdv_impls as _impl
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.data.string_sdv import StringFragmentSdv, StringSdv
from exactly_lib.type_system.data.concrete_strings import StrValueTransformer

def str_fragment(constant: str) -> StringFragmentSdv:
    return _impl.ConstantStringFragmentSdv(constant)


def symbol_fragment(symbol_reference: su.SymbolReference) -> StringFragmentSdv:
    return _impl.SymbolStringFragmentSdv(symbol_reference)


def path_fragment(path: PathSdv) -> StringFragmentSdv:
    return _impl.PathAsStringFragmentSdv(path)


def list_fragment(list_sdv: ListSdv) -> StringFragmentSdv:
    return _impl.ListAsStringFragmentSdv(list_sdv)


def transformed_fragment(fragment: StringFragmentSdv, transformer: StrValueTransformer) -> StringFragmentSdv:
    return _impl.TransformedStringFragmentSdv(fragment, transformer)


def str_constant(string: str) -> StringSdv:
    return StringSdv((str_fragment(string),))


def symbol_reference(symbol_ref: su.SymbolReference) -> StringSdv:
    return StringSdv((symbol_fragment(symbol_ref),))


def from_path_sdv(path: PathSdv) -> StringSdv:
    return StringSdv((path_fragment(path),))


def from_list_sdv(list_sdv: ListSdv) -> StringSdv:
    return StringSdv((list_fragment(list_sdv),))


def from_fragments(fragments: Iterable[StringFragmentSdv]) -> StringSdv:
    return StringSdv(tuple(fragments))