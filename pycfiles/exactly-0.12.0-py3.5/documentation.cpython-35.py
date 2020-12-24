# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/files_matcher/documentation.py
# Compiled at: 2020-01-31 19:34:09
# Size of source mod 2**32: 2998 bytes
from typing import Sequence
from exactly_lib.definitions import matcher_model, misc_texts
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.test_case_utils import file_properties
from exactly_lib.test_case_utils.expression import grammar
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.textformat_parser import TextParser

class EmptyDoc(grammar.SimpleExpressionDescription):

    @property
    def argument_usage_list(self) -> Sequence[a.ArgumentUsage]:
        return ()

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return _TP.fnap(_CHECKS_THAT_PATH_IS_AN_EMPTY_DIRECTORY)


class NumFilesDoc(grammar.SimpleExpressionDescription):

    @property
    def argument_usage_list(self) -> Sequence[a.ArgumentUsage]:
        return (syntax_elements.INTEGER_MATCHER_SYNTAX_ELEMENT.single_mandatory,)

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return _TP.fnap(_CHECKS_THAT_DIRECTORY_CONTAINS_SPECIFIED_NUMBER_OF_FILES)


class SelectionDoc(grammar.SimpleExpressionDescription):

    @property
    def argument_usage_list(self) -> Sequence[a.ArgumentUsage]:
        return (
         syntax_elements.FILE_MATCHER_SYNTAX_ELEMENT.single_mandatory,
         syntax_elements.FILES_MATCHER_SYNTAX_ELEMENT.single_mandatory)

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return _TP.fnap(_SELECTION_DESCRIPTION)


class PruneDoc(grammar.SimpleExpressionDescription):

    @property
    def argument_usage_list(self) -> Sequence[a.ArgumentUsage]:
        return (
         syntax_elements.FILE_MATCHER_SYNTAX_ELEMENT.single_mandatory,
         syntax_elements.FILES_MATCHER_SYNTAX_ELEMENT.single_mandatory)

    @property
    def description_rest(self) -> Sequence[ParagraphItem]:
        return _TP.fnap(_PRUNE_DESCRIPTION)


_TP = TextParser({'FILE_MATCHER': syntax_elements.FILE_MATCHER_SYNTAX_ELEMENT.singular_name, 
 'FILES_MATCHER': syntax_elements.FILES_MATCHER_SYNTAX_ELEMENT.singular_name, 
 'model': matcher_model.FILES_MATCHER_MODEL, 
 'element': matcher_model.FILE_MATCHER_MODEL, 
 'NOTE': misc_texts.NOTE_LINE_HEADER, 
 'SYMBOLIC_LINKS_ARE_FOLLOWED': misc_texts.SYMBOLIC_LINKS_ARE_FOLLOWED, 
 'symbolic_link': file_properties.TYPE_INFO[file_properties.FileType.SYMLINK].name})
_SELECTION_DESCRIPTION = 'Applies {FILES_MATCHER} to the sub set of {element:s} matched by {FILE_MATCHER}.\n'
_PRUNE_DESCRIPTION = 'Excludes contents of directories matched by {FILE_MATCHER}.\n\n\n{SYMBOLIC_LINKS_ARE_FOLLOWED}.\n\n\n{NOTE} {FILE_MATCHER} is only applied to directories (and {symbolic_link:s} to directories).\n'
_CHECKS_THAT_PATH_IS_AN_EMPTY_DIRECTORY = 'Tests that the {model} is empty.\n'
_CHECKS_THAT_DIRECTORY_CONTAINS_SPECIFIED_NUMBER_OF_FILES = 'Tests the number of {element:s}.\n'