# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/lib.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 4006 bytes
import os, re, sys, logging, humanfriendly
logger = logging.getLogger(__name__)
output_types = [
 'list', 'json']
except_directories = ['.Spotlight-V100', '.zfs', 'Android', 'LOST.DIR']
default_output_type = 'json'

def str2bool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    if val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    raise ValueError('invalid truth value %r' % (val,))


def bytes_to_human(b):
    return humanfriendly.format_size(b)


def seconds_to_human(s):
    import datetime
    return str(datetime.timedelta(seconds=s))


def empty_dirs(root_dir, recursive=True):
    dirs_list = []
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if recursive:
            all_subs_empty = True
            for sub in dirs:
                full_sub = os.path.join(root, sub)

            if full_sub not in dirs_list:
                all_subs_empty = False
                break
        else:
            all_subs_empty = not dirs
        if all_subs_empty and is_empty(files):
            dirs_list.append(root)
            (yield root)


def is_empty(files):
    return len(files) == 0


def raise_limits--- This code section failed: ---

 L.  54         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              resource
                6  STORE_FAST               'resource'

 L.  55         8  SETUP_FINALLY        64  'to 64'

 L.  56        10  LOAD_FAST                'resource'
               12  LOAD_METHOD              getrlimit
               14  LOAD_FAST                'resource'
               16  LOAD_ATTR                RLIMIT_NOFILE
               18  CALL_METHOD_1         1  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               '_'
               24  STORE_FAST               'hard'

 L.  57        26  LOAD_GLOBAL              logger
               28  LOAD_METHOD              info
               30  LOAD_STR                 'Current limits, soft and hard : %s %s'
               32  LOAD_FAST                '_'
               34  LOAD_FAST                'hard'
               36  CALL_METHOD_3         3  ''
               38  POP_TOP          

 L.  58        40  LOAD_FAST                'resource'
               42  LOAD_METHOD              setrlimit
               44  LOAD_FAST                'resource'
               46  LOAD_ATTR                RLIMIT_NOFILE
               48  LOAD_FAST                'hard'
               50  LOAD_FAST                'hard'
               52  BUILD_TUPLE_2         2 
               54  CALL_METHOD_2         2  ''
               56  POP_TOP          

 L.  59        58  POP_BLOCK        
               60  LOAD_CONST               True
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY     8  '8'

 L.  60        64  DUP_TOP          
               66  LOAD_GLOBAL              ValueError
               68  LOAD_GLOBAL              OSError
               70  BUILD_TUPLE_2         2 
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   118  'to 118'
               76  POP_TOP          
               78  STORE_FAST               'e'
               80  POP_TOP          
               82  SETUP_FINALLY       106  'to 106'

 L.  61        84  LOAD_GLOBAL              logger
               86  LOAD_METHOD              critical
               88  LOAD_STR                 'You may need to check ulimit parameter: %s'
               90  LOAD_FAST                'e'
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          

 L.  62        96  POP_BLOCK        
               98  POP_EXCEPT       
              100  CALL_FINALLY        106  'to 106'
              102  LOAD_CONST               False
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'
            106_1  COME_FROM_FINALLY    82  '82'
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  END_FINALLY      
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            74  '74'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

Parse error at or near `RETURN_VALUE' instruction at offset 62


def restart():
    python = sys.executable
    print(f"Restarting myself: {python} {sys.argv}")
    os._exit(0)


def find_files(directories, supported_formats):
    directories = [os.path.abspath(d) for d in directories]
    for directory in directories:
        for root, _, files in os.walk(directory):
            if any((e in root for e in except_directories)):
                logger.debug(f"Invalid path {root}")

    else:
        for basename in files:
            filename = os.path.join(root, basename)
            if filename.endswith(tuple(supported_formats)):
                (yield (
                 directory, filename))


def scantree--- This code section failed: ---

 L.  88         0  SETUP_FINALLY        90  'to 90'

 L.  89         2  LOAD_STR                 '/.'
                4  LOAD_FAST                'path'
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L.  90        10  POP_BLOCK        
               12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L.  91        16  LOAD_GLOBAL              os
               18  LOAD_METHOD              scandir
               20  LOAD_FAST                'path'
               22  CALL_METHOD_1         1  ''
               24  GET_ITER         
             26_0  COME_FROM            76  '76'
               26  FOR_ITER             86  'to 86'
               28  STORE_FAST               'entry'

 L.  92        30  LOAD_FAST                'entry'
               32  LOAD_ATTR                is_dir
               34  LOAD_CONST               False
               36  LOAD_CONST               ('follow_symlinks',)
               38  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L.  93        42  LOAD_GLOBAL              scantree
               44  LOAD_FAST                'entry'
               46  LOAD_ATTR                path
               48  LOAD_FAST                'supported_formats'
               50  CALL_FUNCTION_2       2  ''
               52  GET_YIELD_FROM_ITER
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  POP_TOP          
               60  JUMP_BACK            26  'to 26'
             62_0  COME_FROM            40  '40'

 L.  95        62  LOAD_FAST                'entry'
               64  LOAD_ATTR                name
               66  LOAD_METHOD              endswith
               68  LOAD_GLOBAL              tuple
               70  LOAD_FAST                'supported_formats'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_FALSE    26  'to 26'

 L.  96        78  LOAD_FAST                'entry'
               80  YIELD_VALUE      
               82  POP_TOP          
               84  JUMP_BACK            26  'to 26'
               86  POP_BLOCK        
               88  JUMP_FORWARD        134  'to 134'
             90_0  COME_FROM_FINALLY     0  '0'

 L.  97        90  DUP_TOP          
               92  LOAD_GLOBAL              PermissionError
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   132  'to 132'
               98  POP_TOP          
              100  STORE_FAST               'e'
              102  POP_TOP          
              104  SETUP_FINALLY       120  'to 120'

 L.  98       106  LOAD_GLOBAL              logger
              108  LOAD_METHOD              error
              110  LOAD_FAST                'e'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM_FINALLY   104  '104'
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  END_FINALLY      
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM            96  '96'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM            88  '88'

Parse error at or near `LOAD_CONST' instruction at offset 12


def filecount(path, supported_formats):
    return len(list(scantreepathsupported_formats))


def all_files(directory):
    for root, _, files in os.walk(directory):
        if any((e in root for e in except_directories)):
            logger.debug(f"Invalid path {root}")
    else:
        for basename in files:
            (yield os.path.join(root, basename))


def first(iterable, default=None):
    if iterable:
        if isinstanceiterablestr:
            return iterable
        for item in iterable:
            return item

    return default


def num--- This code section failed: ---

 L. 124         0  SETUP_FINALLY        12  'to 12'

 L. 125         2  LOAD_GLOBAL              int
                4  LOAD_FAST                's'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 126        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    38  'to 38'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 127        26  LOAD_GLOBAL              float
               28  LOAD_FAST                's'
               30  CALL_FUNCTION_1       1  ''
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            18  '18'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


def duration_to_seconds(duration):
    if re.match('\\d+s', duration):
        return int(duration[:-1])
    if re.match('\\d+m', duration):
        return int(duration[:-1]) * 60
    if re.match('\\d+h', duration):
        return int(duration[:-1]) * 3600
    raise ValueError(duration)


def seconds_to_str(duration):
    import datetime
    return str(datetime.timedelta(seconds=duration))


default_checks = [
 'keywords', 'strict_title', 'title', 'path',
 'genre', 'album', 'artist', 'rating', 'number']