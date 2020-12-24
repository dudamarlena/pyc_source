# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\uploader.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 1658 bytes
"""Uploader for google drive"""
import os, logging
logger = logging.getLogger('UPLOADER')
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except Exception:
    logger.error('`pydrive` was not setup properly')
else:

    def upload--- This code section failed: ---

 L.  18         0  SETUP_FINALLY       184  'to 184'

 L.  19         2  LOAD_GLOBAL              GoogleAuth
                4  CALL_FUNCTION_0       0  ''
                6  STORE_FAST               'gauth'

 L.  23         8  LOAD_FAST                'gauth'
               10  LOAD_METHOD              LoadCredentialsFile
               12  LOAD_STR                 'mycreds.txt'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L.  24        18  LOAD_FAST                'gauth'
               20  LOAD_ATTR                credentials
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L.  26        28  LOAD_FAST                'gauth'
               30  LOAD_METHOD              LocalWebserverAuth
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          
               36  JUMP_FORWARD         62  'to 62'
             38_0  COME_FROM            26  '26'

 L.  27        38  LOAD_FAST                'gauth'
               40  LOAD_ATTR                access_token_expired
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L.  29        44  LOAD_FAST                'gauth'
               46  LOAD_METHOD              Refresh
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
               52  JUMP_FORWARD         62  'to 62'
             54_0  COME_FROM            42  '42'

 L.  32        54  LOAD_FAST                'gauth'
               56  LOAD_METHOD              Authorize
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            36  '36'

 L.  36        62  LOAD_FAST                'gauth'
               64  LOAD_METHOD              SaveCredentialsFile
               66  LOAD_STR                 'mycreds.txt'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  38        72  LOAD_GLOBAL              GoogleDrive
               74  LOAD_FAST                'gauth'
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'drive'

 L.  39        80  LOAD_STR                 '118iN1jzavVV-9flrLPZo7DOi0cuxrQ5F'
               82  STORE_FAST               'folder_id'

 L.  40        84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_METHOD              basename
               90  LOAD_FAST                'file_path'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'filename_w_ext'

 L.  41        96  LOAD_GLOBAL              os
               98  LOAD_ATTR                path
              100  LOAD_METHOD              splitext
              102  LOAD_FAST                'filename_w_ext'
              104  CALL_METHOD_1         1  ''
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'filename'
              110  STORE_FAST               'file_extension'

 L.  44       112  LOAD_FAST                'drive'
              114  LOAD_METHOD              CreateFile

 L.  45       116  LOAD_STR                 'parents'
              118  LOAD_STR                 'drive#fileLink'
              120  LOAD_FAST                'folder_id'
              122  LOAD_CONST               ('kind', 'id')
              124  BUILD_CONST_KEY_MAP_2     2 
              126  BUILD_LIST_1          1 
              128  BUILD_MAP_1           1 

 L.  44       130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'f'

 L.  46       134  LOAD_FAST                'filename_w_ext'
              136  LOAD_FAST                'f'
              138  LOAD_STR                 'title'
              140  STORE_SUBSCR     

 L.  49       142  LOAD_FAST                'f'
              144  LOAD_METHOD              SetContentFile
              146  LOAD_FAST                'file_path'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.  50       152  LOAD_FAST                'f'
              154  LOAD_METHOD              Upload
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          

 L.  52       160  LOAD_GLOBAL              logger
              162  LOAD_METHOD              info
              164  LOAD_FAST                'f'
              166  LOAD_STR                 'id'
              168  BINARY_SUBSCR    
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L.  53       174  LOAD_FAST                'f'
              176  LOAD_STR                 'id'
              178  BINARY_SUBSCR    
              180  POP_BLOCK        
              182  RETURN_VALUE     
            184_0  COME_FROM_FINALLY     0  '0'

 L.  54       184  DUP_TOP          
              186  LOAD_GLOBAL              Exception
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   214  'to 214'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L.  55       198  LOAD_GLOBAL              logger
              200  LOAD_METHOD              exception
              202  LOAD_STR                 'Failed to upload %s'
              204  LOAD_FAST                'file_path'
              206  CALL_METHOD_2         2  ''
              208  POP_TOP          
              210  POP_EXCEPT       
              212  JUMP_FORWARD        216  'to 216'
            214_0  COME_FROM           190  '190'
              214  END_FINALLY      
            216_0  COME_FROM           212  '212'

Parse error at or near `POP_TOP' instruction at offset 194