# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/help/syntax_contents_structure.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 2464 bytes
from typing import Sequence
from exactly_lib.definitions.argument_rendering import cl_syntax
from exactly_lib.definitions.argument_rendering.cl_syntax import arg_syntax
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure.core import ParagraphItem

class InvokationVariant(tuple):

    def __new__(cls, syntax: str, description_rest: Sequence[ParagraphItem]=None):
        return tuple.__new__(cls, (syntax, [] if description_rest is None else description_rest))

    @property
    def syntax(self) -> str:
        return self[0]

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return self[1]


def invokation_variant_from_string(syntax: str, description_rest: Sequence[ParagraphItem]=None) -> InvokationVariant:
    return InvokationVariant(syntax, description_rest)


def invokation_variant_from_args(argument_usages: Sequence[a.ArgumentUsage], description_rest: Sequence[ParagraphItem]=None) -> InvokationVariant:
    return InvokationVariant(cl_syntax.cl_syntax_for_args(argument_usages), description_rest)


class SyntaxElementDescription(tuple):

    def __new__(cls, element_name: str, description_rest: Sequence[ParagraphItem], invokation_variants: Sequence[InvokationVariant]=None):
        return tuple.__new__(cls, (element_name,
         description_rest,
         [] if invokation_variants is None else invokation_variants))

    @property
    def element_name(self) -> str:
        return self[0]

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return self[1]

    @property
    def invokation_variants(self) -> Sequence[InvokationVariant]:
        return self[2]


def cli_argument_syntax_element_description(argument: a.Argument, description_rest: Sequence[ParagraphItem], invokation_variants: Sequence[InvokationVariant]=None) -> SyntaxElementDescription:
    return SyntaxElementDescription(arg_syntax(argument), description_rest, invokation_variants)