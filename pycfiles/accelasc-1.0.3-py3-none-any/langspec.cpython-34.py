# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lucas/Programmation/Python/AlwaysCorrectCorrectnessCompiler/accc/langspec/langspec.py
# Compiled at: 2015-03-06 11:03:28
# Size of source mod 2**32: 5700 bytes
__doc__ = '\nThis module describes languages specifications for ACCC.\n'
from accc.lexems import *
INDENTATION = 'indent'
BEG_BLOCK = 'begin_block'
END_BLOCK = 'end_block'
BEG_LINE = 'begin line'
END_LINE = 'end line'
BEG_ACTION = 'begin action'
END_ACTION = 'end action'
BEG_CONDITION = 'begin condition'
END_CONDITION = 'end condition'
LOGICAL_AND = 'logical and'
LOGICAL_OR = 'logical or'

def constructSpec(indentation, begin_block, end_block, begin_line, end_line, begin_action, end_action, begin_condition, end_condition, logical_and, logical_or):
    """Return a language specification based on parameters."""
    return {INDENTATION: indentation, 
     BEG_BLOCK: begin_block, 
     END_BLOCK: end_block, 
     BEG_LINE: begin_line, 
     END_LINE: end_line, 
     BEG_ACTION: begin_action, 
     END_ACTION: end_action, 
     BEG_CONDITION: begin_condition, 
     END_CONDITION: end_condition, 
     LOGICAL_AND: logical_and, 
     LOGICAL_OR: logical_or}


def translated(structure, values, lang_spec):
    """Return code associated to given structure and values, 
    translate with given language specification."""
    indentation = '\t'
    endline = '\n'
    object_code = ''
    stack = []
    push = lambda x: stack.append(x)
    pop = lambda : stack.pop()
    last = --- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              len
                3  LOAD_DEREF               'stack'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  LOAD_CONST               0
               12  COMPARE_OP               >
               15  POP_JUMP_IF_FALSE    26  'to 26'
               18  LOAD_DEREF               'stack'
               21  LOAD_CONST               -1
               24  BINARY_SUBSCR    
               25  RETURN_END_IF_LAMBDA
             26_0  COME_FROM            15  '15'
               26  LOAD_STR                 ' '
               29  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1

    def indented_code(s, level, end=''):
        return lang_spec[INDENTATION] * level + s + end

    level = 0
    CONDITIONS = [LEXEM_TYPE_PREDICAT, LEXEM_TYPE_CONDITION]
    ACTION = LEXEM_TYPE_ACTION
    DOWNLEVEL = LEXEM_TYPE_DOWNLEVEL
    for lexem_type in structure:
        if lexem_type is ACTION:
            if last() in CONDITIONS:
                value, values = values[0:len(stack)], values[len(stack):]
                object_code += indented_code(lang_spec[BEG_CONDITION] + lang_spec[LOGICAL_AND].join(value) + lang_spec[END_CONDITION], level, lang_spec[END_LINE])
                if len(lang_spec[BEG_BLOCK]) > 0:
                    object_code += indented_code(lang_spec[BEG_BLOCK], level, lang_spec[END_LINE])
                stack = []
                level += 1
            object_code += indented_code(lang_spec[BEG_ACTION] + values[0], level, lang_spec[END_ACTION] + lang_spec[END_LINE])
            values = values[1:]
        elif lexem_type in CONDITIONS:
            push(lexem_type)
        elif lexem_type is DOWNLEVEL:
            level -= 1
            if level >= 0:
                object_code += indented_code(lang_spec[END_BLOCK], level)
            else:
                level = 0
                continue

    while level > 0:
        level -= 1
        if level >= 0:
            object_code += indented_code(lang_spec[END_BLOCK], level)
        else:
            level = 0

    return object_code


def cpp_spec():
    """C++ specification, provided for example, and java compatible."""
    return {INDENTATION: '\t', 
     BEG_BLOCK: '{', 
     END_BLOCK: '}\n', 
     BEG_LINE: '', 
     END_LINE: '\n', 
     BEG_ACTION: '', 
     END_ACTION: ';', 
     BEG_CONDITION: 'if(', 
     END_CONDITION: ')', 
     LOGICAL_AND: ' && ', 
     LOGICAL_OR: ' || '}


def ada_spec():
    """Ada specification, provided for example"""
    return {INDENTATION: '\t', 
     BEG_BLOCK: 'begin', 
     END_BLOCK: 'end\n', 
     BEG_LINE: '', 
     END_LINE: '\n', 
     BEG_ACTION: '', 
     END_ACTION: ';', 
     BEG_CONDITION: 'if(', 
     END_CONDITION: ') then', 
     LOGICAL_AND: ' and ', 
     LOGICAL_OR: ' or '}


def python_spec():
    """Python specification, provided for use"""
    return {INDENTATION: '\t', 
     BEG_BLOCK: '', 
     END_BLOCK: '', 
     BEG_LINE: '', 
     END_LINE: '\n', 
     BEG_ACTION: '', 
     END_ACTION: '', 
     BEG_CONDITION: 'if ', 
     END_CONDITION: ':', 
     LOGICAL_AND: ' and ', 
     LOGICAL_OR: ' or '}