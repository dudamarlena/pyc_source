# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/string_transformer_ddvs.py
# Compiled at: 2019-12-27 10:07:50
# Size of source mod 2**32: 772 bytes
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.impls import advs
from exactly_lib.type_system.logic.string_transformer import StringTransformerDdv, StringTransformer, StringTransformerAdv

class StringTransformerConstantDdv(StringTransformerDdv):
    __doc__ = '\n    A :class:`StringTransformerResolver` that is a constant :class:`StringTransformer`\n    '

    def __init__(self, value: StringTransformer):
        self._value = value

    def structure(self) -> StructureRenderer:
        return self._value.structure()

    def value_of_any_dependency(self, tcds: Tcds) -> StringTransformerAdv:
        return advs.ConstantAdv(self._value)