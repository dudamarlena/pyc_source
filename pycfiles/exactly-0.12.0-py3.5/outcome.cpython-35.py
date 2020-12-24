# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_suite/contents/specification/outcome.py
# Compiled at: 2019-04-17 17:16:00
# Size of source mod 2**32: 5109 bytes
from exactly_lib.cli.definitions import exit_codes
from exactly_lib.definitions import formatting
from exactly_lib.definitions import misc_texts
from exactly_lib.definitions.entity import concepts
from exactly_lib.help.render import see_also
from exactly_lib.test_suite import exit_values
from exactly_lib.util.textformat.constructor import sections, paragraphs
from exactly_lib.util.textformat.constructor.environment import ConstructionEnvironment
from exactly_lib.util.textformat.constructor.sections import SectionContentsConstructor
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h, generator
from exactly_lib.util.textformat.structure import document as doc
from exactly_lib.util.textformat.structure.structures import *
from exactly_lib.util.textformat.textformat_parser import TextParser

def root(header: str) -> generator.SectionHierarchyGenerator:
    preamble_paragraphs = TEXT_PARSER.fnap(PREAMBLE)

    def const_contents(header_: str, paragraphs_: List[ParagraphItem]) -> generator.SectionHierarchyGenerator:
        return h.leaf(header_, sections.constant_contents(section_contents(paragraphs_)))

    return h.hierarchy(header, paragraphs.constant(preamble_paragraphs), [
     h.child('reporting', h.leaf('Reporting', _ReportingContentsConstructor())),
     h.child('scenarios', const_contents('Scenarios', _scenarios_list()))])


PREAMBLE = ''
TEXT_PARSER = TextParser({'suite_reporter': formatting.concept_(concepts.SUITE_REPORTER_CONCEPT_INFO), 
 'an_exit_code': misc_texts.EXIT_CODE.singular_determined, 
 'exit_code': misc_texts.EXIT_CODE.singular, 
 'an_exit_identifier': misc_texts.EXIT_IDENTIFIER.singular_determined})
REPORTING = 'Outcome is reported via {an_exit_code} and stdout.\n\nstderr may contain helpful information.\n\n\nOutput on stdout is handled by the selected {suite_reporter}.\n\nThe {suite_reporter} also handles the {exit_code}, in some scenarios.\n'

def _scenarios_list() -> List[ParagraphItem]:
    items = [
     list_item('Invalid command line arguments', scenario_description([], TEXT_PARSER.fnap(_INVALID_CLI_ARGUMENT), str(exit_codes.EXIT_INVALID_USAGE), _EMPTY_STDOUT)),
     list_item('Invalid suite', scenario_description([], TEXT_PARSER.fnap(_INVALID_SUITE), str(exit_values.INVALID_SUITE.exit_code), _DEPENDS_ON_SUITE_REPORTER)),
     list_item('Complete execution', scenario_description([], TEXT_PARSER.fnap(_COMPLETE_EXECUTION), _DEPENDS_ON_SUITE_REPORTER, _DEPENDS_ON_SUITE_REPORTER))]
    the_list = lists.HeaderContentList(items, lists.Format(lists.ListType.ITEMIZED_LIST, custom_separations=SEPARATION_OF_HEADER_AND_CONTENTS))
    return [the_list]


def scenario_description(purpose_paragraphs: List[ParagraphItem], failure_condition: List[ParagraphItem], exit_code: str, stdout: str) -> List[ParagraphItem]:
    outcome_on_error = singe_exit_value_display(exit_code, stdout)
    return purpose_paragraphs + failure_condition + [outcome_on_error]


def singe_exit_value_display(exit_code: str, stdout: str) -> ParagraphItem:
    return first_column_is_header_table([
     [
      cell([para(misc_texts.EXIT_CODE_TITLE)]),
      cell([para(exit_code)])],
     [
      cell([para('stdout')]),
      cell([para(stdout)])]])


class _ReportingContentsConstructor(SectionContentsConstructor):

    def apply(self, environment: ConstructionEnvironment) -> doc.SectionContents:
        initial_paragraphs = TEXT_PARSER.fnap(REPORTING)
        sub_sections = see_also.see_also_sections(_SEE_ALSO_TARGETS, environment)
        return doc.SectionContents(initial_paragraphs, sub_sections)


_SEE_ALSO_TARGETS = [
 concepts.SUITE_REPORTER_CONCEPT_INFO.cross_reference_target]
_EMPTY_STDOUT = 'empty'
_DEPENDS_ON_SUITE_REPORTER = 'Depends on the selected ' + formatting.concept_(concepts.SUITE_REPORTER_CONCEPT_INFO)
_INVALID_CLI_ARGUMENT = 'Invalid argument or an argument that denotes a non-existing file.\n'
_INVALID_SUITE = 'Syntax error in a suite file, or a reference to a non-existing case or sub-suite file.\n'
_COMPLETE_EXECUTION = 'The suite has been executed.\n\nIndividual test cases may have failed, or may not be executable (due to syntax error, e.g.).\n'