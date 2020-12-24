# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/test_suite/section_infos.py
# Compiled at: 2018-09-19 20:57:36
# Size of source mod 2**32: 1710 bytes
"""New structures for information about sections.
Should replace other structures and values, if found useful.
"""
from exactly_lib.definitions.cross_ref.concrete_cross_refs import TestSuiteSectionCrossReference, TestSuiteSectionInstructionCrossReference
from exactly_lib.definitions.section_info import SectionInfo
from exactly_lib.definitions.test_suite import section_names

class TestSuiteSectionInfo(SectionInfo):

    @property
    def cross_reference_target(self) -> TestSuiteSectionCrossReference:
        return TestSuiteSectionCrossReference(self.name.plain)

    def instruction_cross_reference_target(self, instruction_name: str) -> TestSuiteSectionInstructionCrossReference:
        return TestSuiteSectionInstructionCrossReference(self.name.plain, instruction_name)


class TestSuiteSectionWithoutInstructionsInfo(TestSuiteSectionInfo):

    def instruction_cross_reference_target(self, instruction_name: str) -> TestSuiteSectionInstructionCrossReference:
        raise ValueError('The {} section do not have instructions'.format(self.name.plain))


CONFIGURATION = TestSuiteSectionInfo(section_names.CONFIGURATION.plain)
CASES = TestSuiteSectionWithoutInstructionsInfo(section_names.CASES.plain)
SUITES = TestSuiteSectionWithoutInstructionsInfo(section_names.SUITES.plain)
CASE__SETUP = TestSuiteSectionInfo(section_names.CASE__SETUP.plain)
CASE__ACT = TestSuiteSectionInfo(section_names.CASE__ACT.plain)
CASE__BEFORE_ASSERT = TestSuiteSectionInfo(section_names.CASE__BEFORE_ASSERT.plain)
CASE__ASSERT = TestSuiteSectionInfo(section_names.CASE__ASSERT.plain)
CASE__CLEANUP = TestSuiteSectionInfo(section_names.CASE__CLEANUP.plain)