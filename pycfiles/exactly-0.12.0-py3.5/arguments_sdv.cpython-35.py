# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/logic/program/arguments_sdv.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 1556 bytes
from typing import Sequence
from exactly_lib.symbol.data import list_sdvs
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.object_with_typed_symbol_references import ObjectWithTypedSymbolReferences
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case.validation.sdv_validation import DdvValidatorResolver
from exactly_lib.type_system.logic.program.argument import ArgumentsDdv
from exactly_lib.util.symbol_table import SymbolTable

class ArgumentsSdv(ObjectWithTypedSymbolReferences):

    def __init__(self, arguments: ListSdv, validators: Sequence[DdvValidatorResolver]=()):
        self._arguments = arguments
        self._validators = validators

    def new_accumulated(self, arguments_sdv: 'ArgumentsSdv') -> 'ArgumentsSdv':
        args = list_sdvs.concat([self._arguments, arguments_sdv.arguments_list])
        validators = tuple(self._validators) + tuple(arguments_sdv._validators)
        return ArgumentsSdv(args, validators)

    @property
    def arguments_list(self) -> ListSdv:
        return self._arguments

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._arguments.references

    def resolve(self, symbols: SymbolTable) -> ArgumentsDdv:
        return ArgumentsDdv(self._arguments.resolve(symbols), [vr(symbols) for vr in self._validators])


def new_without_validation(arguments: ListSdv) -> ArgumentsSdv:
    return ArgumentsSdv(arguments, ())