# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/util/fonts/_vispy_fonts.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 752 bytes
from ..fetching import load_data_file
_vispy_fonts = ('OpenSans', 'Cabin')

def _get_vispy_font_filename--- This code section failed: ---

 L.  15         0  LOAD_FAST                'face'
                2  LOAD_STR                 '-'
                4  BINARY_ADD       
                6  STORE_FAST               'name'

 L.  16         8  LOAD_FAST                'name'
               10  LOAD_FAST                'bold'
               12  POP_JUMP_IF_TRUE     22  'to 22'
               14  LOAD_FAST                'italic'
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  LOAD_STR                 'Regular'
               20  JUMP_FORWARD         24  'to 24'
             22_0  COME_FROM            16  '16'
             22_1  COME_FROM            12  '12'
               22  LOAD_STR                 ''
             24_0  COME_FROM            20  '20'
               24  INPLACE_ADD      
               26  STORE_FAST               'name'

 L.  17        28  LOAD_FAST                'name'
               30  LOAD_FAST                'bold'
               32  POP_JUMP_IF_FALSE    38  'to 38'
               34  LOAD_STR                 'Bold'
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            32  '32'
               38  LOAD_STR                 ''
             40_0  COME_FROM            36  '36'
               40  INPLACE_ADD      
               42  STORE_FAST               'name'

 L.  18        44  LOAD_FAST                'name'
               46  LOAD_FAST                'italic'
               48  POP_JUMP_IF_FALSE    54  'to 54'
               50  LOAD_STR                 'Italic'
               52  JUMP_FORWARD         56  'to 56'
             54_0  COME_FROM            48  '48'
               54  LOAD_STR                 ''
             56_0  COME_FROM            52  '52'
               56  INPLACE_ADD      
               58  STORE_FAST               'name'

 L.  19        60  LOAD_FAST                'name'
               62  LOAD_STR                 '.ttf'
               64  INPLACE_ADD      
               66  STORE_FAST               'name'

 L.  20        68  LOAD_GLOBAL              load_data_file
               70  LOAD_STR                 'fonts/%s'
               72  LOAD_FAST                'name'
               74  BINARY_MODULO    
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 22_1