# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_transformer/impl/custom.py
# Compiled at: 2020-01-13 16:12:08
# Size of source mod 2**32: 677 bytes
from abc import ABC
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.string_transformer import StringTransformer
from exactly_lib.util.description_tree import renderers

class CustomStringTransformer(StringTransformer, ABC):
    __doc__ = '\n    Base class for built in custom transformers.\n    '

    def __init__(self, name: str):
        self._name = name
        self._structure = renderers.header_only(name)

    @property
    def name(self) -> str:
        return self._name

    def structure(self) -> StructureRenderer:
        return self._structure

    def __str__(self):
        return str(type(self))