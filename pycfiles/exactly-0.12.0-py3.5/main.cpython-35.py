# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_suite/contents/specification/main.py
# Compiled at: 2018-09-28 05:20:32
# Size of source mod 2**32: 3888 bytes
from exactly_lib import program_info
from exactly_lib.cli.definitions.common_cli_options import SUITE_COMMAND
from exactly_lib.definitions import formatting
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.formatting import SectionName
from exactly_lib.definitions.test_suite import section_names
from exactly_lib.help.program_modes.test_suite.contents.specification import outcome
from exactly_lib.help.program_modes.test_suite.contents_structure.test_suite_help import TestSuiteHelp
from exactly_lib.test_suite import exit_values
from exactly_lib.util.textformat.constructor import sections
from exactly_lib.util.textformat.constructor.sections import SectionContentsConstructor
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h
from exactly_lib.util.textformat.section_target_hierarchy.as_section_contents import SectionContentsConstructorFromHierarchyGenerator
from exactly_lib.util.textformat.section_target_hierarchy.generator import SectionHierarchyGenerator
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.textformat_parser import TextParser
from . import structure

def specification_constructor(suite_help: TestSuiteHelp) -> SectionContentsConstructor:
    return SectionContentsConstructorFromHierarchyGenerator(hierarchy('unused section header', suite_help))


def hierarchy--- This code section failed: ---

 L.  30         0  LOAD_GLOBAL              TextParser

 L.  31         3  LOAD_STR                 'program_name'
                6  LOAD_GLOBAL              formatting
                9  LOAD_ATTR                program_name
               12  LOAD_GLOBAL              program_info
               15  LOAD_ATTR                PROGRAM_NAME
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  32        21  LOAD_STR                 'executable_name'
               24  LOAD_GLOBAL              program_info
               27  LOAD_ATTR                PROGRAM_NAME

 L.  33        30  LOAD_STR                 'suite_program_mode'
               33  LOAD_GLOBAL              SUITE_COMMAND

 L.  34        36  LOAD_STR                 'reporter_concept'
               39  LOAD_GLOBAL              formatting
               42  LOAD_ATTR                concept_
               45  LOAD_GLOBAL              concepts
               48  LOAD_ATTR                SUITE_REPORTER_CONCEPT_INFO
               51  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  35        54  LOAD_STR                 'cases'
               57  LOAD_GLOBAL              section_names
               60  LOAD_ATTR                CASES

 L.  36        63  LOAD_STR                 'suites'
               66  LOAD_GLOBAL              section_names
               69  LOAD_ATTR                SUITES

 L.  37        72  LOAD_STR                 'ALL_PASS'
               75  LOAD_GLOBAL              exit_values
               78  LOAD_ATTR                ALL_PASS
               81  LOAD_ATTR                exit_identifier

 L.  38        84  LOAD_STR                 'generic_section'
               87  LOAD_GLOBAL              SectionName
               90  LOAD_STR                 'NAME'
               93  CALL_FUNCTION_1       1  '1 positional, 0 named'
               96  BUILD_MAP_8           8 
               99  CALL_FUNCTION_1       1  '1 positional, 0 named'
              102  STORE_DEREF              'tp'

 L.  41       105  LOAD_GLOBAL              str
              108  LOAD_GLOBAL              SectionContentsConstructor
              111  LOAD_CONST               ('contents', 'return')
              114  LOAD_CLOSURE             'tp'
              117  BUILD_TUPLE_1         1 
              120  LOAD_CODE                <code_object section_of_parsed>
              123  LOAD_STR                 'hierarchy.<locals>.section_of_parsed'
              126  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
              132  STORE_FAST               'section_of_parsed'

 L.  46       135  LOAD_GLOBAL              h
              138  LOAD_ATTR                hierarchy

 L.  47       141  LOAD_FAST                'header'
              144  LOAD_STR                 'children'

 L.  49       147  LOAD_GLOBAL              h
              150  LOAD_ATTR                child
              153  LOAD_STR                 'introduction'

 L.  50       156  LOAD_GLOBAL              h
              159  LOAD_ATTR                leaf
              162  LOAD_STR                 'Introduction'

 L.  51       165  LOAD_FAST                'section_of_parsed'
              168  LOAD_GLOBAL              _INTRODUCTION
              171  CALL_FUNCTION_1       1  '1 positional, 0 named'
              174  CALL_FUNCTION_2       2  '2 positional, 0 named'
              177  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L.  53       180  LOAD_GLOBAL              h
              183  LOAD_ATTR                child
              186  LOAD_STR                 'structure'

 L.  54       189  LOAD_GLOBAL              structure
              192  LOAD_ATTR                root
              195  LOAD_STR                 'Structure'
              198  LOAD_FAST                'suite_help'
              201  CALL_FUNCTION_2       2  '2 positional, 0 named'
              204  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L.  56       207  LOAD_GLOBAL              h
              210  LOAD_ATTR                child
              213  LOAD_STR                 'file-syntax'

 L.  57       216  LOAD_GLOBAL              h
              219  LOAD_ATTR                leaf
              222  LOAD_STR                 'File syntax'

 L.  58       225  LOAD_FAST                'section_of_parsed'
              228  LOAD_GLOBAL              _FILE_SYNTAX
              231  CALL_FUNCTION_1       1  '1 positional, 0 named'
              234  CALL_FUNCTION_2       2  '2 positional, 0 named'
              237  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L.  60       240  LOAD_GLOBAL              h
              243  LOAD_ATTR                child
              246  LOAD_STR                 'outcome'

 L.  61       249  LOAD_GLOBAL              outcome
              252  LOAD_ATTR                root
              255  LOAD_STR                 'Outcome'
              258  CALL_FUNCTION_1       1  '1 positional, 0 named'
              261  CALL_FUNCTION_2       2  '2 positional, 0 named'
              264  BUILD_LIST_4          4 
              267  CALL_FUNCTION_257   257  '1 positional, 1 named'
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 120


_INTRODUCTION_SUMMARY = '{program_name} has functionality for organizing test cases in test suites.\nA test suite can contain test cases as well as sub suites.\n\n\nThe result of executing a test suite is reported by a {reporter_concept}.\n'
_INTRODUCTION = "A test suite is written as a plain text file:\n\n\n```\n{cases:syntax}\n\na.case\ngroup-dir/*.case\n\n{suites:syntax}\n\nsub-suite.suite\nsub-dir/*.suite\n```\n\n\nIf the file 'example.suite' contains this text, then {program_name} can execute it:\n\n\n```\n> {executable_name} {suite_program_mode} example.suite\n...\n{ALL_PASS}\n```\n\n\nA suite file can have any name - {program_name} does not put any restriction on file names.\n"
_STRUCTURE_INTRO = 'A suite is made up of "sections". The sections are:\n'
_FILE_SYNTAX = 'Syntax is line oriented.\n\n\n"{generic_section:syntax}" on a single line declares the start of section "{generic_section:plain}".\n\n\nThe order of sections is irrelevant.\n\n\nA section may appear any number of times.\nThe contents of all appearances are accumulated.\n\n\nEmpty lines, and lines beginning with "#" are ignored,\nunless part of an instruction.\n'