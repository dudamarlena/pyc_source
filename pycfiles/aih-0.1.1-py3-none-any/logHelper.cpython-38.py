# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\logHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 638 bytes
__doc__ = '\n@File    :   logHelper.py\n@Time    :   2019/02/28\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   LOG FILE TOOL\n'
import os, time

def write--- This code section failed: ---

 L.  15         0  SETUP_FINALLY        40  'to 40'

 L.  16         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'path'
                6  LOAD_STR                 'a+'
                8  CALL_FUNCTION_2       2  ''
               10  STORE_FAST               'fd'

 L.  17        12  LOAD_FAST                'fd'
               14  LOAD_METHOD              write
               16  LOAD_FAST                'string'
               18  LOAD_STR                 '\n'
               20  BINARY_ADD       
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L.  18        26  LOAD_FAST                'fd'
               28  LOAD_METHOD              close
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L.  19        34  POP_BLOCK        
               36  LOAD_CONST               True
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L.  20        40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  21        46  POP_EXCEPT       
               48  LOAD_CONST               False
               50  RETURN_VALUE     
               52  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 38


def writeByTime(path, string):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtimetime.time)
    return writepath('[' + date + ']  ' + string)


def clear(path):
    try:
        os.removepath
    except:
        pass