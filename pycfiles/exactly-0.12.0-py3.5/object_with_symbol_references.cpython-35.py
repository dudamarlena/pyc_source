# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/object_with_symbol_references.py
# Compiled at: 2018-03-24 06:15:26
# Size of source mod 2**32: 579 bytes
import itertools
from typing import Sequence, List

class ObjectWithSymbolReferences:

    @property
    def references(self) -> Sequence:
        """
        All :class:`SymbolReference` directly referenced by this object.
        """
        return []


def references_from_objects_with_symbol_references(objects: Sequence[ObjectWithSymbolReferences]) -> List:
    """Concatenates the references from a list of :class:`ObjectWithSymbolReferences`"""
    return list(itertools.chain.from_iterable([x.references for x in objects]))