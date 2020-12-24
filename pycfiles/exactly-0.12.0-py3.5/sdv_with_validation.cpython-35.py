# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/sdv_with_validation.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 411 bytes
from exactly_lib.symbol.object_with_typed_symbol_references import ObjectWithTypedSymbolReferences
from exactly_lib.test_case.validation.sdv_validation import SdvValidator

class WithValidation:

    @property
    def validator(self) -> SdvValidator:
        raise NotImplementedError('abstract method')


class ObjectWithSymbolReferencesAndValidation(ObjectWithTypedSymbolReferences, WithValidation):
    pass