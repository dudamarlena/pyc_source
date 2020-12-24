# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/string_transformer.py
# Compiled at: 2019-12-27 10:07:50
# Size of source mod 2**32: 1574 bytes
from abc import ABC, abstractmethod
from typing import Iterable
from exactly_lib.test_case.validation.ddv_validation import DdvValidator, constant_success_validator
from exactly_lib.test_case_file_structure.dir_dependent_value import DirDependentValue
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.description.tree_structured import WithNameAndTreeStructureDescription, WithTreeStructureDescription
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironmentDependentValue
StringTransformerModel = Iterable[str]

class StringTransformer(WithNameAndTreeStructureDescription, ABC):
    __doc__ = '\n    Transforms a sequence of lines, where each line is a string.\n    '

    @property
    def is_identity_transformer(self) -> bool:
        """
        Tells if this transformer is the identity transformer
        """
        return False

    def transform(self, lines: StringTransformerModel) -> StringTransformerModel:
        raise NotImplementedError('abstract method')

    def __str__(self):
        return type(self).__name__


StringTransformerAdv = ApplicationEnvironmentDependentValue[StringTransformer]

class StringTransformerDdv(DirDependentValue[ApplicationEnvironmentDependentValue[StringTransformer]], WithTreeStructureDescription, ABC):

    def validator(self) -> DdvValidator:
        return constant_success_validator()

    @abstractmethod
    def value_of_any_dependency(self, tcds: Tcds) -> StringTransformerAdv:
        pass