# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/configuration.py
# Compiled at: 2020-05-13 11:43:26
# Size of source mod 2**32: 1472 bytes
import yaml, os, re, sys, logging
from shutil import copyfile
from pathlib import Path

def get_working_directory():
    userdir = os.path.expanduser('~')
    workingDirectory = os.path.join(userdir, 'PoliCal')
    tasks_db = Path(os.path.join(workingDirectory, 'tasks.db'))
    if not os.path.exists(workingDirectory):
        os.makedirs(workingDirectory)
    if not tasks_db.is_file():
        dir = os.path.dirname(__file__)
        tasks_src = os.path.join(dir, 'tasks.db')
        tasks_dst = os.path.join(workingDirectory, 'tasks.db')
        copyfile(tasks_src, tasks_dst)
    return workingDirectory


def get_file_location(filename):
    workingDirectory = get_working_directory()
    return os.path.join(workingDirectory, filename)


logging.basicConfig(filename=(get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def load_config_file--- This code section failed: ---

 L.  36         0  SETUP_FINALLY        56  'to 56'

 L.  37         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              get_file_location
                6  LOAD_FAST                'config_file_path'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_STR                 'r'
               12  CALL_FUNCTION_2       2  ''
               14  SETUP_WITH           46  'to 46'
               16  STORE_FAST               'config_yaml'

 L.  38        18  LOAD_GLOBAL              yaml
               20  LOAD_METHOD              safe_load
               22  LOAD_FAST                'config_yaml'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'file_config'

 L.  39        28  LOAD_FAST                'file_config'
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  POP_FINALLY           0  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH       14  '14'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      
               52  POP_BLOCK        
               54  JUMP_FORWARD         88  'to 88'
             56_0  COME_FROM_FINALLY     0  '0'

 L.  40        56  DUP_TOP          
               58  LOAD_GLOBAL              IOError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    86  'to 86'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  41        70  LOAD_GLOBAL              logging
               72  LOAD_METHOD              error

 L.  42        74  LOAD_STR                 'Archivo de configuración no encontrado, generando llaves'

 L.  41        76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  43        80  POP_EXCEPT       
               82  LOAD_CONST               None
               84  RETURN_VALUE     
             86_0  COME_FROM            62  '62'
               86  END_FINALLY      
             88_0  COME_FROM            54  '54'

Parse error at or near `POP_BLOCK' instruction at offset 30


def check_for_url(url):
    checker = re.search('^https.*recentupcoming$', url)
    if checker:
        return True
    return False