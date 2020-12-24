# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build/bdist.macosx-10.15-x86_64/egg/sphinx_intl/pycompat.py
# Compiled at: 2020-04-19 02:09:17
# Size of source mod 2**32: 2017 bytes
"""
Python compatibility functions.
"""
import sys, os, warnings
from typing import Any, Callable
fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

def relpath--- This code section failed: ---

 L.  16         0  SETUP_FINALLY        18  'to 18'

 L.  17         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              relpath
                8  LOAD_FAST                'path'
               10  LOAD_FAST                'start'
               12  CALL_METHOD_2         2  ''
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L.  18        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    40  'to 40'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  19        32  LOAD_FAST                'path'
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'
               40  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28


def convert_with_2to3(filepath: str) -> str:
    from lib2to3.refactor import RefactoringTool, get_fixers_from_package
    from lib2to3.pgen2.parse import ParseError
    fixers = get_fixers_from_package('lib2to3.fixes')
    refactoring_tool = RefactoringTool(fixers)
    source = refactoring_tool._read_python_source(filepath)[0]
    try:
        tree = refactoring_tool.refactor_stringsource'conf.py'
    except ParseError as err:
        try:
            lineno, offset = err.context[1]
            raise SyntaxError(err.msg, (filepath, lineno, offset, err.value))
        finally:
            err = None
            del err

    else:
        return str(tree)


def execfile_(filepath: str, _globals: Any, open: Callable=open) -> None:
    with open(filepath, 'rb') as (f):
        source = f.read()
    filepath_enc = filepath.encode(fs_encoding)
    try:
        code = compile(source, filepath_enc, 'exec')
    except SyntaxError:
        source = convert_with_2to3(filepath)
        code = compile(source, filepath_enc, 'exec')
        warnings.warn'Support for evaluating Python 2 syntax is deprecated and will be removed in sphinx-intl 4.0. Convert %s to Python 3 syntax.'filepath
    else:
        exec(code, _globals)