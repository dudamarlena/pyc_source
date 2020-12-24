# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/configuration_parameters/objects/hds_act_directory.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 2368 bytes
from typing import List
from exactly_lib.definitions import formatting, misc_texts
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.definitions.entity import conf_params
from exactly_lib.definitions.path import REL_HDS_ACT_OPTION
from exactly_lib.definitions.test_case import phase_names, phase_infos
from exactly_lib.definitions.test_case.instructions.instruction_names import HDS_ACT_DIRECTORY_INSTRUCTION_NAME
from exactly_lib.help.entities.configuration_parameters.contents_structure import ConfigurationParameterDocumentation
from exactly_lib.test_case_file_structure.tcds_symbols import SYMBOL_HDS_ACT
from exactly_lib.util.description import Description, DescriptionWithSubSections, from_simple_description
from exactly_lib.util.textformat.textformat_parser import TextParser

class _HdsActDirectoryConfigurationParameter(ConfigurationParameterDocumentation):

    def __init__(self):
        super().__init__(conf_params.HDS_ACT_DIRECTORY_CONF_PARAM_INFO)

    def purpose(self) -> DescriptionWithSubSections:
        parser = TextParser({'phase': phase_names.PHASE_NAME_DICTIONARY, 
         'the_concept': formatting.conf_param_(conf_params.HDS_ACT_DIRECTORY_CONF_PARAM_INFO), 
         'home_dir_env_var': SYMBOL_HDS_ACT, 
         'rel_option': formatting.cli_option(REL_HDS_ACT_OPTION), 
         'executable_file': formatting.misc_name_with_formatting(misc_texts.EXECUTABLE_FILE)})
        return from_simple_description(Description(self.single_line_description(), parser.fnap(_REST_DESCRIPTION)))

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        return [
         phase_infos.CONFIGURATION.instruction_cross_reference_target(HDS_ACT_DIRECTORY_INSTRUCTION_NAME)]


DOCUMENTATION = _HdsActDirectoryConfigurationParameter()
_REST_DESCRIPTION = 'Instructions and phases may use files\nthat are supposed to exist before the test case is executed.\n\n\nE.g., the {phase[act]} phase (by default) references an program that is expected\nto be {executable_file:a}.\n\nIf the path to this file is relative, then it is relative the {the_concept}.\n\n\nThe environment variable {home_dir_env_var} contains the absolute path of this directory.\n\n\nThe option {rel_option} (accepted by many instructions) refers to this directory.\n'