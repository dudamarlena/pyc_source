# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/test_case_doc.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 8157 bytes
from typing import Sequence, TypeVar, Generic, Callable
from exactly_lib.section_document.model import SectionContents, ElementType, SectionContentElement, Instruction, InstructionInfo
from exactly_lib.section_document.source_location import SourceLocationInfo
from exactly_lib.test_case.phases.act import ActPhaseInstruction
from exactly_lib.test_case.phases.assert_ import AssertPhaseInstruction
from exactly_lib.test_case.phases.before_assert import BeforeAssertPhaseInstruction
from exactly_lib.test_case.phases.cleanup import CleanupPhaseInstruction
from exactly_lib.test_case.phases.configuration import ConfigurationPhaseInstruction
from exactly_lib.test_case.phases.setup import SetupPhaseInstruction
T = TypeVar('T')

class ElementWithSourceLocation(Generic[T]):

    def __init__(self, source_location_info: SourceLocationInfo, value: T):
        self._value = value
        self._source_location_info = source_location_info

    @property
    def value(self) -> T:
        return self._value

    @property
    def source_location_info(self) -> SourceLocationInfo:
        return self._source_location_info


class TestCaseOfInstructions(tuple):

    def __new__(cls, configuration_phase: Sequence[ElementWithSourceLocation[ConfigurationPhaseInstruction]], setup_phase: Sequence[ElementWithSourceLocation[SetupPhaseInstruction]], act_phase: Sequence[ElementWithSourceLocation[ActPhaseInstruction]], before_assert_phase: Sequence[ElementWithSourceLocation[BeforeAssertPhaseInstruction]], assert_phase: Sequence[ElementWithSourceLocation[AssertPhaseInstruction]], cleanup_phase: Sequence[ElementWithSourceLocation[CleanupPhaseInstruction]]):
        return tuple.__new__(cls, (configuration_phase,
         setup_phase,
         act_phase,
         before_assert_phase,
         assert_phase,
         cleanup_phase))

    @property
    def configuration_phase(self) -> Sequence[ElementWithSourceLocation[ConfigurationPhaseInstruction]]:
        return self[0]

    @property
    def setup_phase(self) -> Sequence[ElementWithSourceLocation[SetupPhaseInstruction]]:
        return self[1]

    @property
    def act_phase(self) -> Sequence[ElementWithSourceLocation[ActPhaseInstruction]]:
        return self[2]

    @property
    def before_assert_phase(self) -> Sequence[ElementWithSourceLocation[BeforeAssertPhaseInstruction]]:
        return self[3]

    @property
    def assert_phase(self) -> Sequence[ElementWithSourceLocation[AssertPhaseInstruction]]:
        return self[4]

    @property
    def cleanup_phase(self) -> Sequence[ElementWithSourceLocation[CleanupPhaseInstruction]]:
        return self[5]


class TestCase(tuple):

    def __new__(cls, configuration_phase: SectionContents, setup_phase: SectionContents, act_phase: SectionContents, before_assert_phase: SectionContents, assert_phase: SectionContents, cleanup_phase: SectionContents):
        TestCase._TestCase__assert_instruction_class(configuration_phase, ConfigurationPhaseInstruction)
        TestCase._TestCase__assert_instruction_class(setup_phase, SetupPhaseInstruction)
        TestCase._TestCase__assert_instruction_class(act_phase, ActPhaseInstruction)
        TestCase._TestCase__assert_instruction_class(before_assert_phase, BeforeAssertPhaseInstruction)
        TestCase._TestCase__assert_instruction_class(assert_phase, AssertPhaseInstruction)
        TestCase._TestCase__assert_instruction_class(cleanup_phase, CleanupPhaseInstruction)
        return tuple.__new__(cls, (configuration_phase,
         setup_phase,
         act_phase,
         before_assert_phase,
         assert_phase,
         cleanup_phase))

    @property
    def configuration_phase(self) -> SectionContents:
        return self[0]

    @property
    def setup_phase(self) -> SectionContents:
        return self[1]

    @property
    def act_phase(self) -> SectionContents:
        return self[2]

    @property
    def before_assert_phase(self) -> SectionContents:
        return self[3]

    @property
    def assert_phase(self) -> SectionContents:
        return self[4]

    @property
    def cleanup_phase(self) -> SectionContents:
        return self[5]

    def as_test_case_of_instructions(self) -> TestCaseOfInstructions:
        return TestCaseOfInstructions(filter_instructions_with_source_location(_get_configuration_phase_instruction, self.configuration_phase), filter_instructions_with_source_location(_get_setup_phase_instruction, self.setup_phase), filter_instructions_with_source_location(_get_act_phase_instruction, self.act_phase), filter_instructions_with_source_location(_get_before_assert_phase_instruction, self.before_assert_phase), filter_instructions_with_source_location(_get_assert_phase_instruction, self.assert_phase), filter_instructions_with_source_location(_get_cleanup_phase_instruction, self.cleanup_phase))

    @staticmethod
    def __assert_instruction_class(phase_contents: SectionContents, instruction_class):
        for element in phase_contents.elements:
            if element.element_type is ElementType.INSTRUCTION:
                if not isinstance(element.instruction_info.instruction, instruction_class):
                    raise AssertionError


def filter_instructions_with_source_location--- This code section failed: ---

 L. 144         0  LOAD_GLOBAL              SectionContentElement
                3  LOAD_GLOBAL              ElementWithSourceLocation
                6  LOAD_GLOBAL              T
                9  BINARY_SUBSCR    
               10  LOAD_CONST               ('section_element', 'return')
               13  LOAD_CLOSURE             'get_instruction'
               16  BUILD_TUPLE_1         1 
               19  LOAD_CODE                <code_object get_element>
               22  LOAD_STR                 'filter_instructions_with_source_location.<locals>.get_element'
               25  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               31  STORE_FAST               'get_element'

 L. 151        34  LOAD_GLOBAL              filter
               37  LOAD_GLOBAL              _is_instruction_element
               40  LOAD_FAST                'section'
               43  LOAD_ATTR                elements
               46  CALL_FUNCTION_2       2  '2 positional, 0 named'
               49  STORE_FAST               'instruction_elements'

 L. 153        52  LOAD_GLOBAL              list
               55  LOAD_GLOBAL              map
               58  LOAD_FAST                'get_element'
               61  LOAD_FAST                'instruction_elements'
               64  CALL_FUNCTION_2       2  '2 positional, 0 named'
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _is_instruction_element(section_element: SectionContentElement) -> bool:
    return section_element.element_type is ElementType.INSTRUCTION


def _get_instruction(section_element: SectionContentElement) -> Instruction:
    return section_element.instruction_info.instruction


def _get_configuration_phase_instruction(info: InstructionInfo) -> ConfigurationPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, ConfigurationPhaseInstruction)
    return instruction


def _get_setup_phase_instruction(info: InstructionInfo) -> SetupPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, SetupPhaseInstruction)
    return instruction


def _get_act_phase_instruction(info: InstructionInfo) -> ActPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, ActPhaseInstruction)
    return instruction


def _get_before_assert_phase_instruction(info: InstructionInfo) -> BeforeAssertPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, BeforeAssertPhaseInstruction)
    return instruction


def _get_assert_phase_instruction(info: InstructionInfo) -> AssertPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, AssertPhaseInstruction)
    return instruction


def _get_cleanup_phase_instruction(info: InstructionInfo) -> CleanupPhaseInstruction:
    instruction = info.instruction
    assert isinstance(instruction, CleanupPhaseInstruction)
    return instruction