# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_slice/video.py
# Compiled at: 2019-06-11 23:51:07
# Size of source mod 2**32: 374 bytes
from moviepy import editor

def remove_sections--- This code section failed: ---

 L.   7         0  LOAD_GLOBAL              editor
                2  LOAD_METHOD              concatenate_videoclips

 L.   8         4  LOAD_CLOSURE             'video_clip'
                6  BUILD_TUPLE_1         1 
                8  LOAD_LISTCOMP            '<code_object <listcomp>>'
               10  LOAD_STR                 'remove_sections.<locals>.<listcomp>'
               12  MAKE_FUNCTION_8          'closure'
               14  LOAD_FAST                'sections'
               16  GET_ITER         
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  RETURN_VALUE     

 L.  11        24  FOR_ITER             52  'to 52'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'start'
               30  STORE_FAST               'end'

 L.  12        32  LOAD_FAST                'clips'
               34  LOAD_METHOD              append
               36  LOAD_DEREF               'video_clip'
               38  LOAD_METHOD              subclip
               40  LOAD_FAST                'start'
               42  LOAD_FAST                'end'
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  POP_TOP          
               50  JUMP_BACK            24  'to 24'
               52  POP_BLOCK        

 L.  13        54  LOAD_GLOBAL              editor
               56  LOAD_METHOD              concatenate_videoclips
               58  LOAD_FAST                'clips'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `FOR_ITER' instruction at offset 24