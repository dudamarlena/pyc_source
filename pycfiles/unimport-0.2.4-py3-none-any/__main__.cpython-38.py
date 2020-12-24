# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/hakan/Desktop/project/unimport/unimport/__main__.py
# Compiled at: 2020-04-17 04:33:23
# Size of source mod 2**32: 3031 bytes
import argparse, pathlib, sys
from unimport import __version__, __description__
from unimport.session import Session
parser = argparse.ArgumentParser(description=__description__)
exclusive_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('sources',
  default='.',
  nargs='*',
  help='files and folders to find the unused imports.',
  type=(pathlib.Path))
parser.add_argument('-c',
  '--config',
  default='.',
  help='read configuration from PATH.',
  metavar='PATH',
  type=(pathlib.Path))
parser.add_argument('-d',
  '--diff',
  action='store_true',
  help='Prints a diff of all the changes unimport would make to a file.')
exclusive_group.add_argument('-r',
  '--remove',
  action='store_true',
  help='remove unused imports automatically.')
exclusive_group.add_argument('-p',
  '--permission',
  action='store_true',
  help='Refactor permission after see diff.')
parser.add_argument('--check',
  action='store_true',
  help='Prints which file the unused imports are in.')
parser.add_argument('-v',
  '--version',
  action='version',
  version=f"Unimport {__version__}",
  help='Prints version of unimport')

def print_if_exists(sequence):
    if sequence:
        print(*sequence, **{'sep': '\n'})
        return True


def main--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              parser
                2  LOAD_METHOD              parse_args
                4  LOAD_FAST                'argv'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'namespace'

 L.  67        10  LOAD_GLOBAL              any
               12  LOAD_LISTCOMP            '<code_object <listcomp>>'
               14  LOAD_STR                 'main.<locals>.<listcomp>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_GLOBAL              vars
               20  LOAD_FAST                'namespace'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_METHOD              items
               26  CALL_METHOD_0         0  ''
               28  GET_ITER         
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               2
               34  LOAD_CONST               None
               36  BUILD_SLICE_2         2 
               38  BINARY_SUBSCR    
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'any_namespace'

 L.  68        44  LOAD_FAST                'namespace'
               46  LOAD_ATTR                permission
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  LOAD_FAST                'namespace'
               52  LOAD_ATTR                diff
               54  POP_JUMP_IF_TRUE     62  'to 62'

 L.  69        56  LOAD_CONST               True
               58  LOAD_FAST                'namespace'
               60  STORE_ATTR               diff
             62_0  COME_FROM            54  '54'
             62_1  COME_FROM            48  '48'

 L.  70        62  LOAD_GLOBAL              Session
               64  LOAD_FAST                'namespace'
               66  LOAD_ATTR                config
               68  LOAD_CONST               ('config_file',)
               70  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               72  STORE_FAST               'session'

 L.  71        74  LOAD_FAST                'namespace'
               76  LOAD_ATTR                sources
               78  GET_ITER         
            80_82  FOR_ITER            348  'to 348'
               84  STORE_FAST               'source_path'

 L.  72        86  LOAD_FAST                'session'
               88  LOAD_METHOD              _list_paths
               90  LOAD_FAST                'source_path'
               92  LOAD_STR                 '**/*.py'
               94  CALL_METHOD_2         2  ''
               96  GET_ITER         
             98_0  COME_FROM           328  '328'
               98  FOR_ITER            346  'to 346'
              100  STORE_FAST               'py_path'

 L.  73       102  LOAD_FAST                'any_namespace'
              104  POP_JUMP_IF_FALSE   112  'to 112'
              106  LOAD_FAST                'namespace'
              108  LOAD_ATTR                check
              110  POP_JUMP_IF_FALSE   236  'to 236'
            112_0  COME_FROM           104  '104'

 L.  74       112  LOAD_FAST                'session'
              114  LOAD_ATTR                scanner
              116  LOAD_ATTR                run_visit
              118  LOAD_FAST                'session'
              120  LOAD_METHOD              _read
              122  LOAD_FAST                'py_path'
              124  CALL_METHOD_1         1  ''
              126  LOAD_CONST               0
              128  BINARY_SUBSCR    
              130  LOAD_CONST               ('source',)
              132  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              134  POP_TOP          

 L.  75       136  LOAD_FAST                'session'
              138  LOAD_ATTR                scanner
              140  LOAD_METHOD              get_unused_imports
              142  CALL_METHOD_0         0  ''
              144  GET_ITER         
              146  FOR_ITER            226  'to 226'
              148  STORE_FAST               'imp'

 L.  76       150  LOAD_FAST                'imp'
              152  LOAD_STR                 'star'
              154  BINARY_SUBSCR    
              156  POP_JUMP_IF_FALSE   176  'to 176'

 L.  77       158  LOAD_STR                 'Used object; '
              160  LOAD_FAST                'imp'
              162  LOAD_STR                 'modules'
              164  BINARY_SUBSCR    
              166  FORMAT_VALUE          0  ''
              168  LOAD_STR                 ', '
              170  BUILD_STRING_3        3 
              172  STORE_FAST               'modules'
              174  JUMP_FORWARD        180  'to 180'
            176_0  COME_FROM           156  '156'

 L.  79       176  LOAD_STR                 ''
              178  STORE_FAST               'modules'
            180_0  COME_FROM           174  '174'

 L.  80       180  LOAD_GLOBAL              print

 L.  81       182  LOAD_STR                 '\x1b[93m'
              184  LOAD_FAST                'imp'
              186  LOAD_STR                 'name'
              188  BINARY_SUBSCR    
              190  FORMAT_VALUE          0  ''
              192  LOAD_STR                 '\x1b[00m at \x1b[92m'
              194  LOAD_GLOBAL              str
              196  LOAD_FAST                'py_path'
              198  CALL_FUNCTION_1       1  ''
              200  FORMAT_VALUE          0  ''
              202  LOAD_STR                 ':'
              204  LOAD_FAST                'imp'
              206  LOAD_STR                 'lineno'
              208  BINARY_SUBSCR    
              210  FORMAT_VALUE          0  ''
              212  LOAD_STR                 '\x1b[00m '
              214  LOAD_FAST                'modules'
              216  FORMAT_VALUE          0  ''
              218  BUILD_STRING_8        8 

 L.  80       220  CALL_FUNCTION_1       1  ''
              222  POP_TOP          
              224  JUMP_BACK           146  'to 146'

 L.  86       226  LOAD_FAST                'session'
              228  LOAD_ATTR                scanner
              230  LOAD_METHOD              clear
              232  CALL_METHOD_0         0  ''
              234  POP_TOP          
            236_0  COME_FROM           110  '110'

 L.  87       236  LOAD_FAST                'namespace'
              238  LOAD_ATTR                diff
          240_242  POP_JUMP_IF_FALSE   324  'to 324'

 L.  88       244  LOAD_GLOBAL              print_if_exists

 L.  89       246  LOAD_GLOBAL              tuple
              248  LOAD_FAST                'session'
              250  LOAD_METHOD              diff_file
              252  LOAD_FAST                'py_path'
              254  CALL_METHOD_1         1  ''
              256  CALL_FUNCTION_1       1  ''

 L.  88       258  CALL_FUNCTION_1       1  ''
              260  STORE_FAST               'exists_diff'

 L.  91       262  LOAD_FAST                'namespace'
              264  LOAD_ATTR                permission
          266_268  POP_JUMP_IF_FALSE   324  'to 324'
              270  LOAD_FAST                'exists_diff'
          272_274  POP_JUMP_IF_FALSE   324  'to 324'

 L.  92       276  LOAD_GLOBAL              input

 L.  93       278  LOAD_STR                 "Apply suggested changes to \x1b[92m'"
              280  LOAD_FAST                'py_path'
              282  FORMAT_VALUE          0  ''
              284  LOAD_STR                 "'\x1b[00m [y/n/q] ? >"
              286  BUILD_STRING_3        3 

 L.  92       288  CALL_FUNCTION_1       1  ''
              290  STORE_FAST               'action'

 L.  95       292  LOAD_FAST                'action'
              294  LOAD_STR                 'q'
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   308  'to 308'

 L.  96       302  POP_TOP          
              304  JUMP_BACK            80  'to 80'
              306  JUMP_FORWARD        324  'to 324'
            308_0  COME_FROM           298  '298'

 L.  97       308  LOAD_FAST                'action'
              310  LOAD_STR                 'y'
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   324  'to 324'

 L.  98       318  LOAD_CONST               True
              320  LOAD_FAST                'namespace'
              322  STORE_ATTR               remove
            324_0  COME_FROM           314  '314'
            324_1  COME_FROM           306  '306'
            324_2  COME_FROM           272  '272'
            324_3  COME_FROM           266  '266'
            324_4  COME_FROM           240  '240'

 L.  99       324  LOAD_FAST                'namespace'
              326  LOAD_ATTR                remove
              328  POP_JUMP_IF_FALSE    98  'to 98'

 L. 100       330  LOAD_FAST                'session'
              332  LOAD_ATTR                refactor_file
              334  LOAD_FAST                'py_path'
              336  LOAD_CONST               True
              338  LOAD_CONST               ('apply',)
              340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              342  POP_TOP          
              344  JUMP_BACK            98  'to 98'
              346  JUMP_BACK            80  'to 80'

Parse error at or near `JUMP_FORWARD' instruction at offset 306


if __name__ == '__main__':
    main(sys.argv[1:])