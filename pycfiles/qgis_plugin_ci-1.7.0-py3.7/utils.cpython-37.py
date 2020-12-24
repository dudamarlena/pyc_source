# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qgispluginci/utils.py
# Compiled at: 2020-05-01 10:08:01
# Size of source mod 2**32: 961 bytes
import re, os

def replace_in_file(file_path: str, pattern, new: str, encoding: str='utf8'):
    with open(file_path, 'r', encoding=encoding) as (f):
        content = f.read()
    content = re.sub(pattern, new, content, flags=(re.M))
    with open(file_path, 'w', encoding=encoding) as (f):
        f.write(content)


def configure_file(source_file: str, dest_file: str, replace: dict):
    with open(source_file, 'r', encoding='utf-8') as (f):
        content = f.read()
    for pattern, new in replace.items():
        content = re.sub(pattern, new, content, flags=(re.M))

    with open(dest_file, 'w', encoding='utf-8') as (f):
        f.write(content)


def touch_file--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              dirname
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'basedir'

 L.  24        12  LOAD_FAST                'create_dir'
               14  POP_JUMP_IF_FALSE    38  'to 38'
               16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              exists
               22  LOAD_FAST                'basedir'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  POP_JUMP_IF_TRUE     38  'to 38'

 L.  25        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              makedirs
               32  LOAD_FAST                'basedir'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  POP_TOP          
             38_0  COME_FROM            26  '26'
             38_1  COME_FROM            14  '14'

 L.  26        38  LOAD_GLOBAL              open
               40  LOAD_FAST                'path'
               42  LOAD_STR                 'a'
               44  CALL_FUNCTION_2       2  '2 positional arguments'
               46  SETUP_WITH           72  'to 72'
               48  POP_TOP          

 L.  27        50  LOAD_FAST                'update_time'
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L.  28        54  LOAD_GLOBAL              os
               56  LOAD_METHOD              utime
               58  LOAD_FAST                'path'
               60  LOAD_CONST               None
               62  CALL_METHOD_2         2  '2 positional arguments'
               64  POP_TOP          
               66  JUMP_FORWARD         68  'to 68'
             68_0  COME_FROM            66  '66'
             68_1  COME_FROM            52  '52'

 L.  30        68  POP_BLOCK        
               70  LOAD_CONST               None
             72_0  COME_FROM_WITH       46  '46'
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 68