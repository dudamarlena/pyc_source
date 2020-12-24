# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/list_sdvs.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1506 bytes
"""
All construction of :class:`ListResolver` should be done via this module.

Import qualified!
"""
import itertools
from typing import Iterable
from exactly_lib.symbol.data import list_sdv as _impl
from exactly_lib.symbol.data import string_sdvs as _string_sdvs
from exactly_lib.symbol.data.list_sdv import ListSdv, ElementSdv
from exactly_lib.symbol.data.string_sdv import StringSdv
from exactly_lib.symbol.symbol_usage import SymbolReference

def empty() -> ListSdv:
    return from_strings(())


def from_elements(elements: Iterable[ElementSdv]) -> ListSdv:
    return ListSdv(elements)


def from_strings(elements: Iterable[StringSdv]) -> ListSdv:
    return ListSdv([string_element(element) for element in elements])


def from_string(element: StringSdv) -> ListSdv:
    return from_strings([element])


def from_str_constants(str_list: Iterable[str]) -> ListSdv:
    return ListSdv([str_element(e) for e in str_list])


def from_str_constant(constant: str) -> ListSdv:
    return from_str_constants([constant])


def concat(lists: Iterable[ListSdv]) -> ListSdv:
    return ListSdv(itertools.chain.from_iterable([x.elements for x in lists]))


def string_element(string_sdv: StringSdv) -> ElementSdv:
    return _impl.StringElementSdv(string_sdv)


def symbol_element(symbol_reference: SymbolReference) -> ElementSdv:
    return _impl.SymbolReferenceElementSdv(symbol_reference)


def str_element(s: str) -> ElementSdv:
    return string_element(_string_sdvs.str_constant(s))