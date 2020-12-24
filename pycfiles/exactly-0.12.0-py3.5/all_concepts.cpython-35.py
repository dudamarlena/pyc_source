# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/concepts/all_concepts.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 1101 bytes
from typing import List
from exactly_lib.help.entities.concepts.contents_structure import ConceptDocumentation
from exactly_lib.help.entities.concepts.objects import instruction, action_to_check, actor, environment_variable, preprocessor, sds, shell_syntax, hds, tcds, suite_reporter, symbol, type_, configuration_parameter, current_working_directory, directive

def all_concepts() -> List[ConceptDocumentation]:
    return [
     instruction.INSTRUCTION_CONCEPT,
     actor.ACTOR_CONCEPT,
     action_to_check.ACTOR_CONCEPT,
     shell_syntax.SHELL_SYNTAX_CONCEPT,
     tcds.TEST_CASE_DIRECTORY_STRUCTURE_CONCEPT,
     hds.HDS_CONCEPT,
     sds.SANDBOX_CONCEPT,
     symbol.SYMBOL_CONCEPT,
     current_working_directory.CURRENT_WORKING_DIRECTORY_CONCEPT,
     configuration_parameter.CONFIGURATION_PARAMETER_CONCEPT,
     environment_variable.ENVIRONMENT_VARIABLE_CONCEPT,
     preprocessor.PREPROCESSOR_CONCEPT,
     suite_reporter.SUITE_REPORTER_CONCEPT,
     type_.TYPE_CONCEPT,
     directive.DIRECTIVE_CONCEPT]