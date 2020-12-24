# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/help/with_see_also_set.py
# Compiled at: 2019-12-27 10:07:51
# Size of source mod 2**32: 3370 bytes
import itertools
from typing import Sequence, List
from exactly_lib.common.help.see_also import SeeAlsoSet
from exactly_lib.common.help.syntax_contents_structure import InvokationVariant, SyntaxElementDescription, invokation_variant_from_args
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure.core import ParagraphItem

class SyntaxDescriptionHelperBase:
    __doc__ = '\n    A self contained documentation item - can give used and referred elements.\n    '

    @property
    def see_also(self) -> SeeAlsoSet:
        return SeeAlsoSet(())

    @property
    def sub_sed_list(self) -> List[SyntaxElementDescription]:
        return []

    @property
    def syntax_element_definitions(self) -> List[SyntaxElementDescription]:
        raise NotImplementedError('abstract method')


class SyntaxElementDescriptionTree(SyntaxDescriptionHelperBase):

    @property
    def element(self) -> a.Named:
        raise NotImplementedError('abstract method')

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return []

    @property
    def invokation_variants(self) -> Sequence[InvokationVariant]:
        return []

    @property
    def as_sed(self) -> SyntaxElementDescription:
        return SyntaxElementDescription(self.element.name, self.description_rest, self.invokation_variants)

    @property
    def sub_syntax_element_definition_trees(self) -> List['SyntaxElementDescriptionTree']:
        return []

    @property
    def syntax_element_definitions(self) -> List[SyntaxElementDescription]:
        all_trees = [self] + flatten(self.sub_syntax_element_definition_trees)
        return [tree.as_sed for tree in all_trees]


class InvokationVariantHelper(SyntaxDescriptionHelperBase):

    @property
    def syntax(self) -> Sequence[a.ArgumentUsage]:
        return []

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return []

    @property
    def as_invokation_variant(self) -> InvokationVariant:
        return invokation_variant_from_args(self.syntax, self.description_rest)

    @property
    def sub_syntax_element_definition_trees(self) -> List[SyntaxElementDescriptionTree]:
        return []

    @property
    def syntax_element_definitions(self) -> List[SyntaxElementDescription]:
        return [tree.as_sed for tree in flatten(self.sub_syntax_element_definition_trees)]


class SyntaxElementDescriptionTreeFromSed(SyntaxElementDescriptionTree):

    def __init__(self, element: a.Named, sed: SyntaxElementDescription):
        self._element = element
        self._sed = sed

    @property
    def element(self) -> a.Named:
        return self._element

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return self._sed.description_rest

    @property
    def invokation_variants(self) -> Sequence[InvokationVariant]:
        return self._sed.invokation_variants


def flatten(trees: Sequence[SyntaxElementDescriptionTree]) -> List[SyntaxElementDescriptionTree]:
    return list(trees) + list(itertools.chain.from_iterable(tree.sub_syntax_element_definition_trees for tree in trees))