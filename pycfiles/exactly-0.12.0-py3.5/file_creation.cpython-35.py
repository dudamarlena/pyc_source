# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/file_creation.py
# Compiled at: 2019-12-27 10:07:53
# Size of source mod 2**32: 4247 bytes
import pathlib
from typing import Optional, Any, Callable
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.test_case_utils.err_msg import path_err_msgs
from exactly_lib.type_system.data.path_ddv import DescribedPath
from exactly_lib.type_system.logic.string_transformer import StringTransformer
from exactly_lib.util.file_utils import ensure_parent_directory_does_exist_and_is_a_directory, ensure_directory_exists

def create_file(file_path: pathlib.Path, operation_on_open_file: Callable[([Any], None)]) -> Optional[str]:
    """
    :return: None iff success. Otherwise an error message.
    """
    try:
        if file_path.exists():
            return 'File does already exist: {}'.format(file_path)
    except NotADirectoryError:
        return 'Part of path exists, but perhaps one in-the-middle-component is not a directory: %s' % str(file_path)

    failure_message = ensure_parent_directory_does_exist_and_is_a_directory(file_path)
    if failure_message is not None:
        return failure_message
    try:
        with file_path.open('x') as (f):
            operation_on_open_file(f)
    except IOError:
        return 'Cannot create file: {}'.format(file_path)


def create_file__dp--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              str
                3  LOAD_GLOBAL              TextRenderer
                6  LOAD_CONST               ('header', 'return')
                9  LOAD_CLOSURE             'path'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object error>
               18  LOAD_STR                 'create_file__dp.<locals>.error'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_FAST               'error'

 L.  45        30  LOAD_DEREF               'path'
               33  LOAD_ATTR                primitive
               36  STORE_FAST               'file_path'

 L.  46        39  SETUP_EXCEPT         68  'to 68'

 L.  47        42  LOAD_FAST                'file_path'
               45  LOAD_ATTR                exists
               48  CALL_FUNCTION_0       0  '0 positional, 0 named'
               51  POP_JUMP_IF_FALSE    64  'to 64'

 L.  48        54  LOAD_FAST                'error'
               57  LOAD_STR                 'File already exists'
               60  CALL_FUNCTION_1       1  '1 positional, 0 named'
               63  RETURN_END_IF    
             64_0  COME_FROM            51  '51'
               64  POP_BLOCK        
               65  JUMP_FORWARD         96  'to 96'
             68_0  COME_FROM_EXCEPT     39  '39'

 L.  49        68  DUP_TOP          
               69  LOAD_GLOBAL              NotADirectoryError
               72  COMPARE_OP               exception-match
               75  POP_JUMP_IF_FALSE    95  'to 95'
               78  POP_TOP          
               79  POP_TOP          
               80  POP_TOP          

 L.  50        81  LOAD_FAST                'error'
               84  LOAD_STR                 'Part of path exists, but perhaps one in-the-middle-component is not a directory'
               87  CALL_FUNCTION_1       1  '1 positional, 0 named'
               90  RETURN_VALUE     
               91  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               95  END_FINALLY      
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            65  '65'

 L.  51        96  LOAD_GLOBAL              ensure_parent_path_does_exist_and_is_a_directory__dp
               99  LOAD_DEREF               'path'
              102  CALL_FUNCTION_1       1  '1 positional, 0 named'
              105  STORE_FAST               'failure_message'

 L.  52       108  LOAD_FAST                'failure_message'
              111  LOAD_CONST               None
              114  COMPARE_OP               is-not
              117  POP_JUMP_IF_FALSE   124  'to 124'

 L.  53       120  LOAD_FAST                'failure_message'
              123  RETURN_VALUE     

 L.  54       124  SETUP_EXCEPT        166  'to 166'

 L.  55       127  LOAD_FAST                'file_path'
              130  LOAD_ATTR                open
              133  LOAD_STR                 'x'
              136  CALL_FUNCTION_1       1  '1 positional, 0 named'
              139  SETUP_WITH          159  'to 159'
              142  STORE_FAST               'f'

 L.  56       145  LOAD_FAST                'operation_on_open_file'
              148  LOAD_FAST                'f'
              151  CALL_FUNCTION_1       1  '1 positional, 0 named'
              154  POP_TOP          
              155  POP_BLOCK        
              156  LOAD_CONST               None
            159_0  COME_FROM_WITH      139  '139'
              159  WITH_CLEANUP_START
              160  WITH_CLEANUP_FINISH
              161  END_FINALLY      
              162  POP_BLOCK        
              163  JUMP_FORWARD        194  'to 194'
            166_0  COME_FROM_EXCEPT    124  '124'

 L.  57       166  DUP_TOP          
              167  LOAD_GLOBAL              IOError
              170  COMPARE_OP               exception-match
              173  POP_JUMP_IF_FALSE   193  'to 193'
              176  POP_TOP          
              177  POP_TOP          
              178  POP_TOP          

 L.  58       179  LOAD_FAST                'error'
              182  LOAD_STR                 'Cannot create file'
              185  CALL_FUNCTION_1       1  '1 positional, 0 named'
              188  RETURN_VALUE     
              189  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
              193  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           163  '163'

Parse error at or near `None' instruction at offset -1


def create_file_from_transformation_of_existing_file(src_path: pathlib.Path, dst_path: pathlib.Path, transformer: StringTransformer) -> Optional[str]:
    """
    :return: Error message in case of failure
    """

    def write_file(output_file):
        with src_path.open() as (in_file):
            for line in transformer.transform(in_file):
                output_file.write(line)

    return create_file(dst_path, write_file)


def create_file_from_transformation_of_existing_file__dp(src_path: pathlib.Path, dst_path: DescribedPath, transformer: StringTransformer) -> Optional[TextRenderer]:
    """
    :return: Error message in case of failure
    """

    def write_file(output_file):
        with src_path.open() as (in_file):
            for line in transformer.transform(in_file):
                output_file.write(line)

    return create_file__dp(dst_path, write_file)


def ensure_path_exists_as_a_directory__dp--- This code section failed: ---

 L.  99         0  LOAD_GLOBAL              str
                3  LOAD_GLOBAL              TextRenderer
                6  LOAD_CONST               ('header', 'return')
                9  LOAD_CLOSURE             'path'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object error>
               18  LOAD_STR                 'ensure_path_exists_as_a_directory__dp.<locals>.error'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_FAST               'error'

 L. 105        30  SETUP_EXCEPT         50  'to 50'

 L. 106        33  LOAD_GLOBAL              ensure_directory_exists
               36  LOAD_DEREF               'path'
               39  LOAD_ATTR                primitive
               42  CALL_FUNCTION_1       1  '1 positional, 0 named'
               45  RETURN_VALUE     
               46  POP_BLOCK        
               47  JUMP_FORWARD        105  'to 105'
             50_0  COME_FROM_EXCEPT     30  '30'

 L. 107        50  DUP_TOP          
               51  LOAD_GLOBAL              NotADirectoryError
               54  COMPARE_OP               exception-match
               57  POP_JUMP_IF_FALSE    77  'to 77'
               60  POP_TOP          
               61  POP_TOP          
               62  POP_TOP          

 L. 108        63  LOAD_FAST                'error'
               66  LOAD_STR                 'Not a directory'
               69  CALL_FUNCTION_1       1  '1 positional, 0 named'
               72  RETURN_VALUE     
               73  POP_EXCEPT       
               74  JUMP_FORWARD        105  'to 105'

 L. 109        77  DUP_TOP          
               78  LOAD_GLOBAL              FileExistsError
               81  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   104  'to 104'
               87  POP_TOP          
               88  POP_TOP          
               89  POP_TOP          

 L. 110        90  LOAD_FAST                'error'
               93  LOAD_STR                 'Part of path exists, but perhaps one in-the-middle-component is not a directory'
               96  CALL_FUNCTION_1       1  '1 positional, 0 named'
               99  RETURN_VALUE     
              100  POP_EXCEPT       
              101  JUMP_FORWARD        105  'to 105'
              104  END_FINALLY      
            105_0  COME_FROM           101  '101'
            105_1  COME_FROM            74  '74'
            105_2  COME_FROM            47  '47'

Parse error at or near `None' instruction at offset -1


def ensure_parent_path_does_exist_and_is_a_directory__dp(dst_path: DescribedPath) -> Optional[TextRenderer]:
    """
    :return: Failure message if cannot ensure, otherwise None.
    """
    return ensure_path_exists_as_a_directory__dp(dst_path.parent())