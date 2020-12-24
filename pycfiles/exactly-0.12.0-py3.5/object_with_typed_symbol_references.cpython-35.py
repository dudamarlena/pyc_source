# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/object_with_typed_symbol_references.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 690 bytes
from typing import Sequence
from exactly_lib.symbol.object_with_symbol_references import ObjectWithSymbolReferences
from exactly_lib.symbol.symbol_usage import SymbolReference

class ObjectWithTypedSymbolReferences(ObjectWithSymbolReferences):
    __doc__ = '\n    A variant of :class:`ObjectWithSymbolReferences` with\n    more specific type hints.\n\n    Would like to have these type hints in :class:`ObjectWithSymbolReferences`,\n    but that is not possible for the moment due to circular dependencies.\n    '

    @property
    def references(self) -> Sequence[SymbolReference]:
        """
        All :class:`SymbolReference` directly referenced by this object.
        """
        return []