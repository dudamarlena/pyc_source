# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\configHelper.py
# Compiled at: 2020-02-14 02:12:36
# Size of source mod 2**32: 2373 bytes
"""
@File    :   configHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Config Tool
"""
import os, configparser

def Count--- This code section failed: ---

 L.  16         0  SETUP_FINALLY       102  'to 102'

 L.  17         2  LOAD_CONST               0
                4  STORE_FAST               'ret'

 L.  18         6  LOAD_GLOBAL              configparser
                8  LOAD_METHOD              ConfigParser
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'cf'

 L.  19        14  LOAD_FAST                'cf'
               16  LOAD_METHOD              read
               18  LOAD_FAST                'fileName'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L.  20        24  LOAD_FAST                'section'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    74  'to 74'

 L.  21        32  LOAD_FAST                'cf'
               34  LOAD_METHOD              sections
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'seclist'

 L.  22        40  LOAD_FAST                'seclist'
               42  GET_ITER         
               44  FOR_ITER             72  'to 72'
               46  STORE_FAST               'sec'

 L.  23        48  LOAD_FAST                'cf'
               50  LOAD_METHOD              options
               52  LOAD_FAST                'sec'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'oplist'

 L.  24        58  LOAD_FAST                'ret'
               60  LOAD_GLOBAL              len
               62  LOAD_FAST                'oplist'
               64  CALL_FUNCTION_1       1  ''
               66  BINARY_ADD       
               68  STORE_FAST               'ret'
               70  JUMP_BACK            44  'to 44'
               72  JUMP_FORWARD         96  'to 96'
             74_0  COME_FROM            30  '30'

 L.  25        74  LOAD_FAST                'cf'
               76  LOAD_METHOD              has_section
               78  LOAD_FAST                'section'
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L.  26        84  LOAD_GLOBAL              len
               86  LOAD_FAST                'cf'
               88  LOAD_FAST                'section'
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'ret'
             96_0  COME_FROM            82  '82'
             96_1  COME_FROM            72  '72'

 L.  27        96  LOAD_FAST                'ret'
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY     0  '0'

 L.  28       102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L.  29       108  POP_EXCEPT       
              110  LOAD_CONST               0
              112  RETURN_VALUE     
              114  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 108


def Sections--- This code section failed: ---

 L.  33         0  SETUP_FINALLY        30  'to 30'

 L.  34         2  LOAD_GLOBAL              configparser
                4  LOAD_METHOD              ConfigParser
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'cf'

 L.  35        10  LOAD_FAST                'cf'
               12  LOAD_METHOD              read
               14  LOAD_FAST                'fileName'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  36        20  LOAD_FAST                'cf'
               22  LOAD_METHOD              sections
               24  CALL_METHOD_0         0  ''
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     0  '0'

 L.  37        30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  38        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
               42  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 36


def GetValue(section, key, default, fileName):
    try:
        cf = configparser.ConfigParser
        cf.readfileName
        if not cf.has_sectionsection:
            return default
        if key in cf[section]:
            default = cf.get(section, key)
        return default
    except:
        return default


def SetValue--- This code section failed: ---

 L.  55         0  SETUP_FINALLY       126  'to 126'

 L.  56         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              access
                6  LOAD_FAST                'fileName'
                8  LOAD_CONST               0
               10  CALL_METHOD_2         2  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  57        18  LOAD_GLOBAL              open
               20  LOAD_FAST                'fileName'
               22  LOAD_STR                 'w'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'fp'

 L.  58        28  LOAD_FAST                'fp'
               30  LOAD_METHOD              close
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          
             36_0  COME_FROM            16  '16'

 L.  60        36  LOAD_GLOBAL              configparser
               38  LOAD_METHOD              ConfigParser
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'cf'

 L.  61        44  LOAD_FAST                'cf'
               46  LOAD_METHOD              read
               48  LOAD_FAST                'fileName'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  62        54  LOAD_FAST                'cf'
               56  LOAD_METHOD              has_section
               58  LOAD_FAST                'section'
               60  CALL_METHOD_1         1  ''
               62  LOAD_CONST               False
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L.  63        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'cf'
               72  LOAD_FAST                'section'
               74  STORE_SUBSCR     
             76_0  COME_FROM            66  '66'

 L.  65        76  LOAD_FAST                'value'
               78  LOAD_FAST                'cf'
               80  LOAD_FAST                'section'
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'key'
               86  STORE_SUBSCR     

 L.  66        88  LOAD_GLOBAL              open
               90  LOAD_FAST                'fileName'
               92  LOAD_STR                 'w'
               94  CALL_FUNCTION_2       2  ''
               96  SETUP_WITH          114  'to 114'
               98  STORE_FAST               'f'

 L.  67       100  LOAD_FAST                'cf'
              102  LOAD_METHOD              write
              104  LOAD_FAST                'f'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM_WITH       96  '96'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

 L.  68       120  POP_BLOCK        
              122  LOAD_CONST               True
              124  RETURN_VALUE     
            126_0  COME_FROM_FINALLY     0  '0'

 L.  69       126  POP_TOP          
              128  POP_TOP          
              130  POP_TOP          

 L.  70       132  POP_EXCEPT       
              134  LOAD_CONST               False
              136  RETURN_VALUE     
              138  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 124


def ParseNoEqual(fileName):
    ret = {}
    try:
        fd = openfileName'r'
        arr = fd.readlines
        group = None
        for item in arr:
            item = item.strip
            if len(item) <= 0:
                pass
            elif item[0] == '#':
                continue
            elif item[0] == '[' and item[(len(item) - 1)] == ']':
                group = item[1:len(item) - 1]
                ret[group] = []
            elif group is None:
                continue
            else:
                ret[group].appenditem

        return ret
    except:
        return ret