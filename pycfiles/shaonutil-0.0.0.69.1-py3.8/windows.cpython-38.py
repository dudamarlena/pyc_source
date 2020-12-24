# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\windows.py
# Compiled at: 2020-04-04 20:39:11
# Size of source mod 2**32: 2034 bytes
"""Windows"""
from psutil import AccessDenied as AccessDeniedError
import ctypes, sys, os, inspect, os

def is_winapp_admin--- This code section failed: ---

 L.  11         0  SETUP_FINALLY        16  'to 16'

 L.  12         2  LOAD_GLOBAL              ctypes
                4  LOAD_ATTR                windll
                6  LOAD_ATTR                shell32
                8  LOAD_METHOD              IsUserAnAdmin
               10  CALL_METHOD_0         0  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  13        16  POP_TOP          
               18  POP_TOP          
               20  POP_TOP          

 L.  14        22  POP_EXCEPT       
               24  LOAD_CONST               False
               26  RETURN_VALUE     
               28  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 22


def get_UAC_permission():
    """Get Windows User Account Control Permission for the executing file. If already executing file has admin access, do not ask for permission."""
    if is_winapp_admin():
        print('The executing file already has admin access.')
    else:
        executing_script = sys.argv[0]
        pathname = os.path.dirname(executing_script)
        executing_script_full_path = os.path.join(os.path.abspath(pathname), executing_script)
        rest_params = sys.argv[1:]
        final_arg_list_unfiltered = [executing_script_full_path] + rest_params
        final_arg_list = ['"' + path_elem + '"' if ' ' in path_elem else path_elem for path_elem in final_arg_list_unfiltered]
        final_arg_str = ' '.join(final_arg_list)
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, final_arg_str, None, 1)