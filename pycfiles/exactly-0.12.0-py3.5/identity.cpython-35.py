# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_transformer/impl/identity.py
# Compiled at: 2020-01-20 02:27:15
# Size of source mod 2**32: 1941 bytes
from typing import Sequence
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.symbol.logic.string_transformer import StringTransformerSdv
from exactly_lib.test_case_utils.description_tree.tree_structured import WithCachedTreeStructureDescriptionBase
from exactly_lib.test_case_utils.expression import grammar
from exactly_lib.test_case_utils.string_transformer import names, sdvs
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.string_transformer import StringTransformer, StringTransformerModel
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.description_tree import renderers
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.textformat_parser import TextParser

def parse_identity(parser: TokenParser) -> StringTransformerSdv:
    return IDENTITY_TRANSFORMER_SDV


class IdentityStringTransformer(WithCachedTreeStructureDescriptionBase, StringTransformer):

    @property
    def name(self) -> str:
        return names.IDENTITY_TRANSFORMER_NAME

    @property
    def is_identity_transformer(self) -> bool:
        return True

    def _structure(self) -> StructureRenderer:
        return renderers.header_only(names.IDENTITY_TRANSFORMER_NAME)

    def transform(self, lines: StringTransformerModel) -> StringTransformerModel:
        return lines


IDENTITY_TRANSFORMER_SDV = sdvs.StringTransformerSdvConstant(IdentityStringTransformer())

class SyntaxDescription(grammar.SimpleExpressionDescription):

    @property
    def argument_usage_list(self) -> Sequence[a.ArgumentUsage]:
        return ()

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return _TEXT_PARSER.fnap(_DESCRIPTION)


_TEXT_PARSER = TextParser()
_DESCRIPTION = 'Gives output that is identical to the input.\n'