# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/priv.py
# Compiled at: 2020-04-11 17:06:53
# Size of source mod 2**32: 2384 bytes
__doc__ = '\naehostd.priv - privileged helper service module\n'
import os, logging, time
from .__about__ import __version__
from .cfg import CFG
from .service import init_service
LOG_NAME = 'aehostd.priv'
DESCRIPTION = 'Privileged helper service for AE-DIR'
REFRESH_INTERVAL = 2.0

def process_sudoers--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        18  'to 18'

 L.  27         2  LOAD_GLOBAL              os
                4  LOAD_METHOD              stat
                6  LOAD_GLOBAL              CFG
                8  LOAD_ATTR                sudoers_file
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'sudoers_stat'
               14  POP_BLOCK        
               16  JUMP_FORWARD         42  'to 42'
             18_0  COME_FROM_FINALLY     0  '0'

 L.  28        18  DUP_TOP          
               20  LOAD_GLOBAL              OSError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    40  'to 40'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  30        32  LOAD_FAST                'last_sudoers_stat'
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'
               40  END_FINALLY      
             42_0  COME_FROM            16  '16'

 L.  31        42  LOAD_FAST                'last_sudoers_stat'
               44  STORE_FAST               'next_sudoers_stat'

 L.  32        46  LOAD_FAST                'last_sudoers_stat'
               48  LOAD_FAST                'sudoers_stat'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE   206  'to 206'

 L.  33        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              join

 L.  34        60  LOAD_GLOBAL              CFG
               62  LOAD_ATTR                sudoers_includedir

 L.  35        64  LOAD_GLOBAL              os
               66  LOAD_ATTR                path
               68  LOAD_METHOD              basename
               70  LOAD_GLOBAL              CFG
               72  LOAD_ATTR                sudoers_file
               74  CALL_METHOD_1         1  ''

 L.  33        76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'target_filename'

 L.  37        80  LOAD_GLOBAL              logging
               82  LOAD_METHOD              debug

 L.  38        84  LOAD_STR                 'New sudoers file at %s to be moved to %s'

 L.  39        86  LOAD_GLOBAL              CFG
               88  LOAD_ATTR                sudoers_file

 L.  40        90  LOAD_FAST                'target_filename'

 L.  37        92  CALL_METHOD_3         3  ''
               94  POP_TOP          

 L.  42        96  SETUP_FINALLY       146  'to 146'

 L.  43        98  LOAD_GLOBAL              os
              100  LOAD_METHOD              chmod
              102  LOAD_GLOBAL              CFG
              104  LOAD_ATTR                sudoers_file
              106  LOAD_CONST               288
              108  CALL_METHOD_2         2  ''
              110  POP_TOP          

 L.  44       112  LOAD_GLOBAL              os
              114  LOAD_METHOD              chown
              116  LOAD_GLOBAL              CFG
              118  LOAD_ATTR                sudoers_file
              120  LOAD_CONST               0
              122  LOAD_CONST               0
              124  CALL_METHOD_3         3  ''
              126  POP_TOP          

 L.  45       128  LOAD_GLOBAL              os
              130  LOAD_METHOD              rename
              132  LOAD_GLOBAL              CFG
              134  LOAD_ATTR                sudoers_file
              136  LOAD_FAST                'target_filename'
              138  CALL_METHOD_2         2  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  JUMP_FORWARD        186  'to 186'
            146_0  COME_FROM_FINALLY    96  '96'

 L.  46       146  DUP_TOP          
              148  LOAD_GLOBAL              Exception
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   184  'to 184'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L.  47       160  LOAD_GLOBAL              logging
              162  LOAD_ATTR                error

 L.  48       164  LOAD_STR                 'Moving sudoers file at %s to %s failed!'

 L.  49       166  LOAD_GLOBAL              CFG
              168  LOAD_ATTR                sudoers_file

 L.  50       170  LOAD_FAST                'target_filename'

 L.  51       172  LOAD_CONST               True

 L.  47       174  LOAD_CONST               ('exc_info',)
              176  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              178  POP_TOP          
              180  POP_EXCEPT       
              182  JUMP_FORWARD        206  'to 206'
            184_0  COME_FROM           152  '152'
              184  END_FINALLY      
            186_0  COME_FROM           144  '144'

 L.  54       186  LOAD_GLOBAL              logging
              188  LOAD_METHOD              info

 L.  55       190  LOAD_STR                 'Successfully moved sudoers file at %s to %s'

 L.  56       192  LOAD_GLOBAL              CFG
              194  LOAD_ATTR                sudoers_file

 L.  57       196  LOAD_FAST                'target_filename'

 L.  54       198  CALL_METHOD_3         3  ''
              200  POP_TOP          

 L.  59       202  LOAD_FAST                'sudoers_stat'
              204  STORE_FAST               'next_sudoers_stat'
            206_0  COME_FROM           182  '182'
            206_1  COME_FROM            52  '52'

 L.  60       206  LOAD_FAST                'next_sudoers_stat'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_FOUR' instruction at offset 34


def main():
    """
    entry point for privileged helper service running as root
    """
    script_name, ctx = init_service(LOG_NAME, DESCRIPTION, service_uid=0, service_gid=0)
    last_sudoers_stat = None
    with ctx:
        try:
            logging.debug'Started privileged helper service'
            while True:
                if CFG.sudoers_file:
                    last_sudoers_stat = process_sudoers(last_sudoers_stat)
                time.sleepREFRESH_INTERVAL

        except (KeyboardInterrupt, SystemExit) as exit_exc:
            try:
                logging.debug'Exit exception received: %r'exit_exc
            finally:
                exit_exc = None
                del exit_exc

        else:
            logging.info'Stopped %s %s'script_name__version__


if __name__ == '__main__':
    main()