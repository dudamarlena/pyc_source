# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/description/tree_structured.py
# Compiled at: 2020-01-13 16:12:08
# Size of source mod 2**32: 815 bytes
from abc import ABC, abstractmethod
from exactly_lib.util.description_tree import renderers
from exactly_lib.util.description_tree.renderer import NodeRenderer
StructureRenderer = NodeRenderer[None]

class WithTreeStructureDescription(ABC):

    @abstractmethod
    def structure(self) -> StructureRenderer:
        """
        The structure of the object, that can be used in traced.

        The returned tree is constant.
        """
        pass


class WithNameAndTreeStructureDescription(WithTreeStructureDescription, ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def structure(self) -> StructureRenderer:
        """
        The structure of the object, that can be used in traced.

        The returned tree is constant.
        """
        pass