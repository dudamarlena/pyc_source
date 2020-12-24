# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\carlo\projects\marlin\marlin\manage.py
# Compiled at: 2020-04-06 18:14:24
# Size of source mod 2**32: 960 bytes
import os
from pathlib import Path

class ManageBookmark:
    marlin_path = Path(Path.home() / '.marlin')

    def __init__(self, bookmark_name, bookmark_path, m_path=marlin_path):
        self.bookmark_name = bookmark_name
        self.bookmark_path = bookmark_path
        self.m_path = m_path

    def add_bookmark(self):
        os.chdir(self.m_path)
        with open((self.bookmark_name), 'w', encoding='utf-8') as (f):
            f.write(self.bookmark_path)

    def remove_bookmark(self):
        os.chdir(self.m_path)
        os.unlink(self.bookmark_name)

    def list_bookmark(self):
        return os.listdir(self.m_path)

    def read_bookmark--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL              os
                2  LOAD_METHOD              chdir
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                m_path
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L.  27        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'bookmark'
               16  LOAD_STR                 'r'
               18  LOAD_STR                 'utf-8'
               20  LOAD_CONST               ('encoding',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  SETUP_WITH           48  'to 48'
               26  STORE_FAST               'f'

 L.  28        28  LOAD_FAST                'f'
               30  LOAD_METHOD              read
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  ROT_TWO          
               38  BEGIN_FINALLY    
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  POP_FINALLY           0  ''
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH       24  '24'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 36

    def create_marlin_folder(self):
        exists = Path(self.m_path).exists()
        if not exists:
            self.m_path.mkdir()