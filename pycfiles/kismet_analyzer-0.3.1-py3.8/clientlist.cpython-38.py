# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kismetanalyzer/clientlist.py
# Compiled at: 2019-02-08 05:19:56
# Size of source mod 2**32: 2097 bytes
from __future__ import print_function
import argparse, json, sqlite3, sys
from kismetanalyzer.model import AccessPoint
from kismetanalyzer.util import does_ssid_matches

def gen_clientlist--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              argparse
                2  LOAD_ATTR                ArgumentParser
                4  LOAD_STR                 'Print a list of connected clients for the given SSID.'
                6  LOAD_CONST               ('description',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'parser'

 L.  20        12  LOAD_FAST                'parser'
               14  LOAD_ATTR                add_argument
               16  LOAD_STR                 '--in'
               18  LOAD_STR                 'store'
               20  LOAD_STR                 'infile'
               22  LOAD_CONST               True
               24  LOAD_STR                 'Input file (.kismet)'
               26  LOAD_CONST               ('action', 'dest', 'required', 'help')
               28  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               30  POP_TOP          

 L.  21        32  LOAD_FAST                'parser'
               34  LOAD_ATTR                add_argument
               36  LOAD_STR                 '--ssid'
               38  LOAD_STR                 'store'
               40  LOAD_STR                 'ssid'
               42  LOAD_CONST               True

 L.  22        44  LOAD_STR                 'SSID (or SSID regex)'

 L.  21        46  LOAD_CONST               ('action', 'dest', 'required', 'help')
               48  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               50  POP_TOP          

 L.  23        52  LOAD_FAST                'parser'
               54  LOAD_METHOD              parse_args
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'parameters'

 L.  26        60  SETUP_FINALLY        78  'to 78'

 L.  27        62  LOAD_GLOBAL              sqlite3
               64  LOAD_METHOD              connect
               66  LOAD_FAST                'parameters'
               68  LOAD_ATTR                infile
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'db'
               74  POP_BLOCK        
               76  JUMP_FORWARD        136  'to 136'
             78_0  COME_FROM_FINALLY    60  '60'

 L.  28        78  DUP_TOP          
               80  LOAD_GLOBAL              Exception
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   134  'to 134'
               86  POP_TOP          
               88  STORE_FAST               'e'
               90  POP_TOP          
               92  SETUP_FINALLY       122  'to 122'

 L.  29        94  LOAD_GLOBAL              print
               96  LOAD_STR                 'Failed to open kismet logfile: {0}'
               98  LOAD_METHOD              format
              100  LOAD_FAST                'e'
              102  CALL_METHOD_1         1  ''
              104  CALL_FUNCTION_1       1  ''
              106  POP_TOP          

 L.  30       108  LOAD_GLOBAL              sys
              110  LOAD_METHOD              exit
              112  LOAD_CONST               1
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_FINALLY    92  '92'
              122  LOAD_CONST               None
              124  STORE_FAST               'e'
              126  DELETE_FAST              'e'
              128  END_FINALLY      
              130  POP_EXCEPT       
              132  JUMP_FORWARD        136  'to 136'
            134_0  COME_FROM            84  '84'
              134  END_FINALLY      
            136_0  COME_FROM           132  '132'
            136_1  COME_FROM            76  '76'

 L.  32       136  SETUP_FINALLY       164  'to 164'

 L.  33       138  LOAD_STR                 "SELECT * FROM devices where type='Wi-Fi AP'; "
              140  STORE_FAST               'sql'

 L.  34       142  LOAD_FAST                'db'
              144  LOAD_METHOD              cursor
              146  CALL_METHOD_0         0  ''
              148  STORE_FAST               'c'

 L.  35       150  LOAD_FAST                'c'
              152  LOAD_METHOD              execute
              154  LOAD_FAST                'sql'
              156  CALL_METHOD_1         1  ''
              158  STORE_FAST               'sql_result'
              160  POP_BLOCK        
              162  JUMP_FORWARD        192  'to 192'
            164_0  COME_FROM_FINALLY   136  '136'

 L.  36       164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L.  37       170  LOAD_GLOBAL              print
              172  LOAD_STR                 'Failed to extract data from database'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          

 L.  38       178  LOAD_GLOBAL              sys
              180  LOAD_METHOD              exit
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           162  '162'

 L.  41       192  LOAD_GLOBAL              set
              194  CALL_FUNCTION_0       0  ''
              196  STORE_FAST               'devs'

 L.  43       198  LOAD_FAST                'sql_result'
              200  GET_ITER         
              202  FOR_ITER            340  'to 340'
              204  STORE_FAST               'row'

 L.  44       206  SETUP_FINALLY       294  'to 294'

 L.  47       208  LOAD_GLOBAL              json
              210  LOAD_METHOD              loads
              212  LOAD_FAST                'row'
              214  LOAD_CONST               14
              216  BINARY_SUBSCR    
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'dev'

 L.  51       222  LOAD_GLOBAL              AccessPoint
              224  LOAD_METHOD              from_json
              226  LOAD_FAST                'dev'
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'ap'

 L.  56       232  LOAD_FAST                'parameters'
              234  LOAD_ATTR                ssid
              236  LOAD_CONST               None
              238  COMPARE_OP               is-not
          240_242  POP_JUMP_IF_FALSE   262  'to 262'

 L.  57       244  LOAD_GLOBAL              does_ssid_matches
              246  LOAD_FAST                'dev'
              248  LOAD_FAST                'parameters'
              250  LOAD_ATTR                ssid
              252  CALL_FUNCTION_2       2  ''
          254_256  POP_JUMP_IF_TRUE    262  'to 262'

 L.  59       258  POP_BLOCK        
              260  JUMP_BACK           202  'to 202'
            262_0  COME_FROM           254  '254'
            262_1  COME_FROM           240  '240'

 L.  61       262  LOAD_FAST                'ap'
              264  LOAD_ATTR                client_map
              266  STORE_FAST               'client_map'

 L.  62       268  LOAD_FAST                'client_map'
              270  GET_ITER         
              272  FOR_ITER            290  'to 290'
              274  STORE_FAST               'c'

 L.  63       276  LOAD_FAST                'devs'
              278  LOAD_METHOD              add
              280  LOAD_FAST                'c'
              282  CALL_METHOD_1         1  ''
              284  POP_TOP          
          286_288  JUMP_BACK           272  'to 272'
              290  POP_BLOCK        
              292  JUMP_BACK           202  'to 202'
            294_0  COME_FROM_FINALLY   206  '206'

 L.  65       294  DUP_TOP          
              296  LOAD_GLOBAL              Exception
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   336  'to 336'
              304  POP_TOP          
              306  STORE_FAST               'e'
              308  POP_TOP          
              310  SETUP_FINALLY       324  'to 324'

 L.  66       312  POP_BLOCK        
              314  POP_EXCEPT       
              316  CALL_FINALLY        324  'to 324'
              318  JUMP_BACK           202  'to 202'
              320  POP_BLOCK        
              322  BEGIN_FINALLY    
            324_0  COME_FROM           316  '316'
            324_1  COME_FROM_FINALLY   310  '310'
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  END_FINALLY      
              332  POP_EXCEPT       
              334  JUMP_BACK           202  'to 202'
            336_0  COME_FROM           300  '300'
              336  END_FINALLY      
              338  JUMP_BACK           202  'to 202'

 L.  68       340  LOAD_GLOBAL              print
              342  LOAD_STR                 '\n'
              344  LOAD_METHOD              join
              346  LOAD_FAST                'devs'
              348  CALL_METHOD_1         1  ''
              350  CALL_FUNCTION_1       1  ''
              352  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 260