# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\bots\console\output_style.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3745 bytes
import os, shutil
from PyInquirer import prompt
from ...binders import available_formats
from core.arguments import get_args

def get_output_path(self):
    """Returns a valid output path where the files are stored"""
    args = get_args()
    output_path = args.output_path
    if args.suppress:
        if not output_path:
            output_path = self.app.output_path
        if not output_path:
            output_path = os.path.join('Lightnovels', 'Unknown Novel')
    if not output_path:
        answer = prompt([
         {'type':'input', 
          'name':'output', 
          'message':'Enter output direcotry:', 
          'default':os.path.abspath(self.app.output_path)}])
        output_path = answer['output']
    output_path = os.path.abspath(output_path)
    if os.path.exists(output_path):
        if self.force_replace_old():
            shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path, exist_ok=True)
    return output_path


def force_replace_old(self):
    args = get_args()
    if args.force:
        return True
    if args.ignore:
        return False
    if args.suppress:
        return False
    answer = prompt([
     {'type':'list', 
      'name':'replace', 
      'message':'What to do with existing folder?', 
      'choices':[
       'Remove old folder and start fresh',
       'Download remaining chapters only']}])
    return answer['replace'].startswith('Remove')


def get_output_formats--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              get_args
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'args'

 L.  91         6  LOAD_FAST                'args'
                8  LOAD_ATTR                output_formats
               10  STORE_DEREF              'formats'

 L.  92        12  LOAD_DEREF               'formats'
               14  POP_JUMP_IF_TRUE     60  'to 60'
               16  LOAD_FAST                'args'
               18  LOAD_ATTR                suppress
               20  POP_JUMP_IF_TRUE     60  'to 60'

 L.  93        22  LOAD_GLOBAL              prompt

 L.  95        24  LOAD_STR                 'checkbox'

 L.  96        26  LOAD_STR                 'formats'

 L.  97        28  LOAD_STR                 'Which output formats to create?'

 L.  98        30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'get_output_formats.<locals>.<listcomp>'
               34  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               36  LOAD_GLOBAL              available_formats
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''

 L.  94        42  LOAD_CONST               ('type', 'name', 'message', 'choices')
               44  BUILD_CONST_KEY_MAP_4     4 

 L.  93        46  BUILD_LIST_1          1 
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'answer'

 L. 101        52  LOAD_FAST                'answer'
               54  LOAD_STR                 'formats'
               56  BINARY_SUBSCR    
               58  STORE_DEREF              'formats'
             60_0  COME_FROM            20  '20'
             60_1  COME_FROM            14  '14'

 L. 104        60  LOAD_DEREF               'formats'
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  LOAD_GLOBAL              len
               66  LOAD_DEREF               'formats'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               0
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    82  'to 82'
             76_0  COME_FROM            62  '62'

 L. 105        76  LOAD_STR                 'epub'
               78  BUILD_LIST_1          1 
               80  STORE_DEREF              'formats'
             82_0  COME_FROM            74  '74'

 L. 108        82  LOAD_CLOSURE             'formats'
               84  BUILD_TUPLE_1         1 
               86  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               88  LOAD_STR                 'get_output_formats.<locals>.<dictcomp>'
               90  MAKE_FUNCTION_8          'closure'
               92  LOAD_GLOBAL              available_formats
               94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 86


def should_pack_by_volume(self):
    """Returns whether to generate single or multiple files by volumes"""
    args = get_args()
    if args.single:
        return False
    if args.multi:
        return True
    if args.suppress:
        return False
    answer = prompt([
     {'type':'list', 
      'name':'split', 
      'message':'How many files to generate?', 
      'choices':[
       'Pack everything into a single file',
       'Split by volume into multiple files']}])
    return answer['split'].startswith('Split')