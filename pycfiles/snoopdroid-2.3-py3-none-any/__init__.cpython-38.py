# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/snoopdroid/snoopdroid/__init__.py
# Compiled at: 2020-04-03 08:08:14
# Size of source mod 2**32: 2832 bytes
import os, sys, argparse, datetime
from .ui import info, logo
from .acquisition import Acquisition
from .virustotal import virustotal_lookup
from .koodous import koodous_lookup

def main--- This code section failed: ---

 L.  32         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_STR                 'Extract information from Android device'
                6  LOAD_CONST               ('description',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L.  33        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '--storage'
               18  LOAD_GLOBAL              os
               20  LOAD_METHOD              getcwd
               22  CALL_METHOD_0         0  ''
               24  LOAD_STR                 'Specify a different base folder to store the acquisition'
               26  LOAD_CONST               ('default', 'help')
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  POP_TOP          

 L.  34        32  LOAD_FAST                'parser'
               34  LOAD_ATTR                add_argument
               36  LOAD_STR                 '--limit'
               38  LOAD_CONST               None
               40  LOAD_STR                 'Set a limit to the number of packages to extract (mainly for debug purposes)'
               42  LOAD_CONST               ('default', 'help')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  POP_TOP          

 L.  35        48  LOAD_FAST                'parser'
               50  LOAD_ATTR                add_argument
               52  LOAD_STR                 '--all-apks'
               54  LOAD_STR                 'store_true'
               56  LOAD_STR                 'Extract all packages installed on the phone, even those marked as safe'
               58  LOAD_CONST               ('action', 'help')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  POP_TOP          

 L.  36        64  LOAD_FAST                'parser'
               66  LOAD_ATTR                add_argument
               68  LOAD_STR                 '--virustotal'
               70  LOAD_STR                 'store_true'
               72  LOAD_STR                 'Check packages on VirusTotal'
               74  LOAD_CONST               ('action', 'help')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  POP_TOP          

 L.  37        80  LOAD_FAST                'parser'
               82  LOAD_ATTR                add_argument
               84  LOAD_STR                 '--koodous'
               86  LOAD_STR                 'store_true'
               88  LOAD_STR                 'Check packages on Koodous'
               90  LOAD_CONST               ('action', 'help')
               92  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               94  POP_TOP          

 L.  38        96  LOAD_FAST                'parser'
               98  LOAD_ATTR                add_argument
              100  LOAD_STR                 '--all-checks'
              102  LOAD_STR                 'store_true'
              104  LOAD_STR                 'Run all available checks'
              106  LOAD_CONST               ('action', 'help')
              108  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              110  POP_TOP          

 L.  39       112  LOAD_FAST                'parser'
              114  LOAD_ATTR                add_argument
              116  LOAD_STR                 '--from-file'
              118  LOAD_CONST               None
              120  LOAD_STR                 'Instead of acquiring from phone, load an existing packages.json file for lookups (mainly for debug purposes)'
              122  LOAD_CONST               ('default', 'help')
              124  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              126  POP_TOP          

 L.  40       128  LOAD_FAST                'parser'
              130  LOAD_METHOD              parse_args
              132  CALL_METHOD_0         0  ''
              134  STORE_FAST               'args'

 L.  42       136  LOAD_GLOBAL              logo
              138  CALL_FUNCTION_0       0  ''
              140  POP_TOP          

 L.  44       142  SETUP_FINALLY       324  'to 324'

 L.  45       144  LOAD_FAST                'args'
              146  LOAD_ATTR                from_file
              148  POP_JUMP_IF_FALSE   164  'to 164'

 L.  46       150  LOAD_GLOBAL              Acquisition
              152  LOAD_METHOD              fromJSON
              154  LOAD_FAST                'args'
              156  LOAD_ATTR                from_file
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               'acq'
              162  JUMP_FORWARD        238  'to 238'
            164_0  COME_FROM           148  '148'

 L.  49       164  LOAD_GLOBAL              datetime
              166  LOAD_ATTR                datetime
              168  LOAD_METHOD              now
              170  CALL_METHOD_0         0  ''
              172  LOAD_METHOD              isoformat
              174  CALL_METHOD_0         0  ''
              176  LOAD_METHOD              split
              178  LOAD_STR                 '.'
              180  CALL_METHOD_1         1  ''
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_METHOD              replace
              188  LOAD_STR                 ':'
              190  LOAD_STR                 ''
              192  CALL_METHOD_2         2  ''
              194  STORE_FAST               'acq_folder'

 L.  50       196  LOAD_GLOBAL              os
              198  LOAD_ATTR                path
              200  LOAD_METHOD              join
              202  LOAD_FAST                'args'
              204  LOAD_ATTR                storage
              206  LOAD_FAST                'acq_folder'
              208  CALL_METHOD_2         2  ''
              210  STORE_FAST               'storage_folder'

 L.  52       212  LOAD_GLOBAL              Acquisition
              214  LOAD_FAST                'storage_folder'

 L.  53       216  LOAD_FAST                'args'
              218  LOAD_ATTR                all_apks

 L.  53       220  LOAD_FAST                'args'
              222  LOAD_ATTR                limit

 L.  52       224  LOAD_CONST               ('storage_folder', 'all_apks', 'limit')
              226  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              228  STORE_FAST               'acq'

 L.  54       230  LOAD_FAST                'acq'
              232  LOAD_METHOD              run
              234  CALL_METHOD_0         0  ''
              236  POP_TOP          
            238_0  COME_FROM           162  '162'

 L.  56       238  LOAD_FAST                'acq'
              240  LOAD_ATTR                packages
              242  STORE_FAST               'packages'

 L.  58       244  LOAD_GLOBAL              len
              246  LOAD_FAST                'packages'
              248  CALL_FUNCTION_1       1  ''
              250  LOAD_CONST               0
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   264  'to 264'

 L.  59       258  POP_BLOCK        
              260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           254  '254'

 L.  61       264  LOAD_FAST                'args'
              266  LOAD_ATTR                virustotal
          268_270  POP_JUMP_IF_TRUE    280  'to 280'
              272  LOAD_FAST                'args'
              274  LOAD_ATTR                all_checks
          276_278  POP_JUMP_IF_FALSE   288  'to 288'
            280_0  COME_FROM           268  '268'

 L.  62       280  LOAD_GLOBAL              virustotal_lookup
              282  LOAD_FAST                'packages'
              284  CALL_FUNCTION_1       1  ''
              286  POP_TOP          
            288_0  COME_FROM           276  '276'

 L.  64       288  LOAD_GLOBAL              print
              290  LOAD_STR                 ''
              292  CALL_FUNCTION_1       1  ''
              294  POP_TOP          

 L.  66       296  LOAD_FAST                'args'
              298  LOAD_ATTR                koodous
          300_302  POP_JUMP_IF_TRUE    312  'to 312'
              304  LOAD_FAST                'args'
              306  LOAD_ATTR                all_checks
          308_310  POP_JUMP_IF_FALSE   320  'to 320'
            312_0  COME_FROM           300  '300'

 L.  67       312  LOAD_GLOBAL              koodous_lookup
              314  LOAD_FAST                'packages'
              316  CALL_FUNCTION_1       1  ''
              318  POP_TOP          
            320_0  COME_FROM           308  '308'
              320  POP_BLOCK        
              322  JUMP_FORWARD        364  'to 364'
            324_0  COME_FROM_FINALLY   142  '142'

 L.  68       324  DUP_TOP          
              326  LOAD_GLOBAL              KeyboardInterrupt
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   362  'to 362'
              334  POP_TOP          
              336  POP_TOP          
              338  POP_TOP          

 L.  69       340  LOAD_GLOBAL              print
              342  LOAD_STR                 ''
              344  CALL_FUNCTION_1       1  ''
              346  POP_TOP          

 L.  70       348  LOAD_GLOBAL              sys
              350  LOAD_METHOD              exit
              352  LOAD_CONST               -1
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
              358  POP_EXCEPT       
              360  JUMP_FORWARD        364  'to 364'
            362_0  COME_FROM           330  '330'
              362  END_FINALLY      
            364_0  COME_FROM           360  '360'
            364_1  COME_FROM           322  '322'

Parse error at or near `LOAD_CONST' instruction at offset 260


if __name__ == '__main__':
    main()