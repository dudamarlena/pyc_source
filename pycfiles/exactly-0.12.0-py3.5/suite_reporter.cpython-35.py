# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/concepts/objects/suite_reporter.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1849 bytes
from typing import List
from exactly_lib.cli.definitions.program_modes.test_suite.command_line_options import OPTION_FOR_REPORTER
from exactly_lib.definitions import formatting
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.definitions.entity import suite_reporters as reporters, concepts
from exactly_lib.definitions.entity.concepts import SUITE_REPORTER_CONCEPT_INFO
from exactly_lib.definitions.entity.suite_reporters import all_suite_reporters_cross_refs
from exactly_lib.help.entities.concepts.contents_structure import ConceptDocumentation
from exactly_lib.util.description import Description, DescriptionWithSubSections, from_simple_description
from exactly_lib.util.textformat.textformat_parser import TextParser

class _SuiteReporterConcept(ConceptDocumentation):

    def __init__(self):
        super().__init__(SUITE_REPORTER_CONCEPT_INFO)

    def purpose(self) -> DescriptionWithSubSections:
        tp = TextParser({'reporter_option': formatting.cli_option(OPTION_FOR_REPORTER), 
         'default_reporter': formatting.entity(reporters.DEFAULT_REPORTER.singular_name), 
         'suite_reporter': formatting.concept_(concepts.SUITE_REPORTER_CONCEPT_INFO)})
        return from_simple_description(Description(self.single_line_description(), tp.fnap(_DESCRIPTION_REST)))

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        return all_suite_reporters_cross_refs()


SUITE_REPORTER_CONCEPT = _SuiteReporterConcept()
_DESCRIPTION_REST = 'Note that some scenarios are not reported by the {suite_reporter},\nsuch as invalid command line arguments.\n\nSee the test suite specification for details.\n\n\nThe reporter is specified via the command line using the {reporter_option} option.\n\n\nDefault: {default_reporter}.\n'