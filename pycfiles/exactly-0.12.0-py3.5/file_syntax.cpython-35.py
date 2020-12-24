# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_case/contents/specification/file_syntax.py
# Compiled at: 2019-12-27 10:07:51
# Size of source mod 2**32: 6976 bytes
from exactly_lib.definitions import formatting, misc_texts
from exactly_lib.definitions.entity import directives, concepts
from exactly_lib.definitions.entity.concepts import ACTOR_CONCEPT_INFO
from exactly_lib.definitions.formatting import AnyInstructionNameDictionary
from exactly_lib.help.program_modes.test_case.contents.specification.utils import Setup
from exactly_lib.help.render import see_also
from exactly_lib.section_document.syntax import section_header, LINE_COMMENT_MARKER
from exactly_lib.test_case.phase_identifier import DEFAULT_PHASE
from exactly_lib.test_case_utils.string_matcher import matcher_options as contents_opts
from exactly_lib.util.textformat.constructor import paragraphs, sections
from exactly_lib.util.textformat.section_target_hierarchy import hierarchies as h, generator
from exactly_lib.util.textformat.textformat_parser import TextParser

def root--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              _text_parser
                3  LOAD_FAST                'setup'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  STORE_DEREF              'tp'

 L.  18        12  LOAD_GLOBAL              str
               15  LOAD_GLOBAL              paragraphs
               18  LOAD_ATTR                ParagraphItemsConstructor
               21  LOAD_CONST               ('template', 'return')
               24  LOAD_CLOSURE             'tp'
               27  BUILD_TUPLE_1         1 
               30  LOAD_CODE                <code_object paragraphs_of>
               33  LOAD_STR                 'root.<locals>.paragraphs_of'
               36  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               42  STORE_DEREF              'paragraphs_of'

 L.  21        45  LOAD_GLOBAL              str
               48  LOAD_GLOBAL              sections
               51  LOAD_ATTR                SectionContentsConstructor
               54  LOAD_CONST               ('template', 'return')
               57  LOAD_CLOSURE             'paragraphs_of'
               60  BUILD_TUPLE_1         1 
               63  LOAD_CODE                <code_object initial_paragraphs_of>
               66  LOAD_STR                 'root.<locals>.initial_paragraphs_of'
               69  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               75  STORE_FAST               'initial_paragraphs_of'

 L.  24        78  LOAD_GLOBAL              sections
               81  LOAD_ATTR                contents

 L.  25        84  LOAD_DEREF               'paragraphs_of'
               87  LOAD_GLOBAL              FILE_INCLUSION_DOC
               90  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  26        93  LOAD_GLOBAL              see_also
               96  LOAD_ATTR                SeeAlsoSectionConstructor

 L.  27        99  LOAD_GLOBAL              see_also
              102  LOAD_ATTR                items_of_targets
              105  LOAD_GLOBAL              _FILE_INCLUSION_SEE_ALSO_TARGETS
              108  CALL_FUNCTION_1       1  '1 positional, 0 named'
              111  CALL_FUNCTION_1       1  '1 positional, 0 named'
              114  BUILD_LIST_1          1 
              117  CALL_FUNCTION_2       2  '2 positional, 0 named'
              120  STORE_FAST               'file_inclusion_doc'

 L.  30       123  LOAD_GLOBAL              h
              126  LOAD_ATTR                hierarchy

 L.  31       129  LOAD_FAST                'header'
              132  LOAD_STR                 'initial_paragraphs'

 L.  32       135  LOAD_DEREF               'paragraphs_of'
              138  LOAD_GLOBAL              _INTRO
              141  CALL_FUNCTION_1       1  '1 positional, 0 named'
              144  LOAD_STR                 'children'

 L.  34       147  LOAD_GLOBAL              h
              150  LOAD_ATTR                child_leaf
              153  LOAD_STR                 'phases'

 L.  35       156  LOAD_STR                 'Phases'

 L.  36       159  LOAD_FAST                'initial_paragraphs_of'
              162  LOAD_GLOBAL              PHASES_DOC
              165  CALL_FUNCTION_1       1  '1 positional, 0 named'
              168  CALL_FUNCTION_3       3  '3 positional, 0 named'

 L.  38       171  LOAD_GLOBAL              h
              174  LOAD_ATTR                child_leaf
              177  LOAD_STR                 'phase-contents'

 L.  39       180  LOAD_STR                 'Phase contents'

 L.  40       183  LOAD_FAST                'initial_paragraphs_of'
              186  LOAD_GLOBAL              PHASES_CONTENTS_DOC
              189  CALL_FUNCTION_1       1  '1 positional, 0 named'
              192  CALL_FUNCTION_3       3  '3 positional, 0 named'

 L.  42       195  LOAD_GLOBAL              h
              198  LOAD_ATTR                child_hierarchy
              201  LOAD_STR                 'instructions'

 L.  43       204  LOAD_STR                 'Instructions'

 L.  44       207  LOAD_DEREF               'paragraphs_of'
              210  LOAD_GLOBAL              INSTRUCTIONS_DOC
              213  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  45       216  LOAD_GLOBAL              h
              219  LOAD_ATTR                child_leaf
              222  LOAD_STR                 'description'

 L.  46       225  LOAD_STR                 'Instruction descriptions'

 L.  47       228  LOAD_FAST                'initial_paragraphs_of'
              231  LOAD_GLOBAL              INSTRUCTIONS_DESCRIPTION_DOC
              234  CALL_FUNCTION_1       1  '1 positional, 0 named'
              237  CALL_FUNCTION_3       3  '3 positional, 0 named'
              240  BUILD_LIST_1          1 
              243  CALL_FUNCTION_4       4  '4 positional, 0 named'

 L.  50       246  LOAD_GLOBAL              h
              249  LOAD_ATTR                child_leaf
              252  LOAD_STR                 'file-inclusion'

 L.  51       255  LOAD_STR                 'File inclusion'

 L.  52       258  LOAD_FAST                'file_inclusion_doc'
              261  CALL_FUNCTION_3       3  '3 positional, 0 named'

 L.  54       264  LOAD_GLOBAL              h
              267  LOAD_ATTR                child_leaf
              270  LOAD_STR                 'com-empty'

 L.  55       273  LOAD_STR                 'Comments and empty lines'

 L.  56       276  LOAD_FAST                'initial_paragraphs_of'
              279  LOAD_GLOBAL              OTHER_DOC
              282  CALL_FUNCTION_1       1  '1 positional, 0 named'
              285  CALL_FUNCTION_3       3  '3 positional, 0 named'
              288  BUILD_LIST_5          5 
              291  CALL_FUNCTION_513   513  '1 positional, 2 named'
              294  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 30


def _text_parser(setup: Setup) -> TextParser:
    return TextParser{'phase_declaration_for_NAME': section_header'NAME', 
     'instruction': AnyInstructionNameDictionary(), 
     'default_phase': setup.phase_names[DEFAULT_PHASE.identifier].syntax, 
     'phase': setup.phase_names, 
     'actor': formatting.concept_ACTOR_CONCEPT_INFO, 
     'CONTENTS_EQUALS_ARGUMENT': contents_opts.EQUALS_ARGUMENT, 
     'CONTENTS_EMPTY_ARGUMENT': contents_opts.EMPTY_ARGUMENT, 
     'line_comment_char': LINE_COMMENT_MARKER, 
     'file_inclusion_directive_in_text': formatting.keyworddirectives.INCLUDING_DIRECTIVE_INFO.singular_name, 
     'file_inclusion_directive': directives.INCLUDING_DIRECTIVE_INFO.singular_name, 
     'shell_command': formatting.misc_name_with_formattingmisc_texts.SHELL_COMMAND}


_FILE_INCLUSION_SEE_ALSO_TARGETS = [
 concepts.DIRECTIVE_CONCEPT_INFO.cross_reference_target,
 directives.INCLUDING_DIRECTIVE_INFO.cross_reference_target]
_INTRO = 'Syntax is line oriented.\n\n\nTop level elements start at the beginning of a line,\nand line ends mark the end of elements, although some may span several lines.\n'
PHASES_DOC = '"{phase_declaration_for_NAME}" on a single line declares the start of phase NAME.\n\nThis line marks the start the {phase[assert]} phase, for example:\n\n\n```\n[assert]\n```\n\n\nThe following lines will belong to this phase.\n\n\nFile contents before the first phase declaration belong to the default phase,\nwhich is {default_phase}.\n\n\nThe order of the different phases in the test case file is irrelevant.\nThe phases are always executed in the same order,\nregardless of the order they appear in the test case file.\n\n\nA phase can be declared more than once.\n\nContents of multiple declarations are merged, and executed in the order it appears in the file.\n\nHere, {instruction[exit_code]} is executed before {instruction[stderr]}:\n\n\n```\n[assert]\n\nexit-code == 0\n\n[act]\n\nhelloworld\n\n[assert]\n\nstderr {CONTENTS_EMPTY_ARGUMENT}\n```\n'
PHASES_CONTENTS_DOC = 'All phases except the {phase[act]} phase consist of a sequence of "instructions" (see below).\n\n\nThe contents of the {phase[act]} phase depends on which {actor} is used.\n\nBy default, it is expected to contain a single command line.\n'
INSTRUCTIONS_DOC = 'Instructions start at the beginning of the line with a space separated identifier that\nis the name of the instruction.\n\n\nThe name may optionally be followed by arguments. Most instructions use a syntax for\noptions, arguments and quoting that resembles the unix shell.\n\nThe exact syntax depends on the particular instruction.\n\n\nAn instruction may span several lines, as this form of {instruction[stdout]} does:\n\n\n```\nstdout {CONTENTS_EQUALS_ARGUMENT} <<EOF\nHello, World!\nEOF\n```\n'
INSTRUCTIONS_DESCRIPTION_DOC = 'An instruction may optionally be preceded by a "description" -\na free text within quotes that is\ndisplayed together with the instruction source line in error messages.\n\nThe purpose of a description is to describe the meaning of the instruction using\ntext that is easier to understand than the source line.\n\nA description is a quoted string using shell syntax.\n\n\nFor example, a free text may be easier to understand than {shell_command:a}:\n\n\n```\n{phase[assert]:syntax}\n\n\'PATH should contain /usr/local/bin\'\n\n$ tr \':\' \'\\n\' < ../result/stdout | grep \'^/usr/local/bin$\'\n```\n\n\nA description may span several lines.\n'
OTHER_DOC = 'Lines beginning with "{line_comment_char}" are comments.\n\nComments may only appear on lines between instructions and phase headers.\n\n\nEmpty lines that are not part of an instruction are ignored.\n\n\nEmpty lines, and lines with comment line syntax, may be part of instruction and\nthe {phase[act]} phase, though,\nas in the {instruction[stdout]} instruction here:\n\n\n```\nstdout {CONTENTS_EQUALS_ARGUMENT} <<EOF\nthis assertion expects 4 lines of output\n{line_comment_char} this is the second line of the expected output\n\nthe above empty line is part of the expected output\nEOF\n```\n'
FILE_INCLUSION_DOC = 'Parts of a test case can be put in an external file,\nusing the {file_inclusion_directive_in_text} directive:\n\n\n```\n{file_inclusion_directive} external-part-of-test-case.xly\n```\n'