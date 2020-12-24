# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyraminxolver\command_line.py
# Compiled at: 2019-10-26 16:03:57
# Size of source mod 2**32: 1833 bytes
import sys, argparse
from . import PyraminXolver
import pyraminxolver.setup as graph_setup
parser = argparse.ArgumentParser()
parser.add_argument('--input-file', help='Path to file with a bunch of pyraminx scrambles')
parser.add_argument('--output-file', help='Path to output solutions')
parser.add_argument('--scramble', help='Scamble wrapped in "". e.g. "L R U L"')
parser.add_argument('--slack', default=0, type=int, help='Maximum distance to optimal solution for all solutions')
parser.add_argument('--verbose', type=bool, help='Get more details')
args = parser.parse_args()

def main--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              print
                2  LOAD_STR                 'Loading up pyraminx graph'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L.  17         8  LOAD_GLOBAL              PyraminXolver
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'pyra'

 L.  18        14  LOAD_GLOBAL              print
               16  LOAD_STR                 'Graph loaded, ready to solve'
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L.  19        22  LOAD_GLOBAL              args
               24  LOAD_ATTR                slack
               26  STORE_FAST               'slack'

 L.  20        28  BUILD_LIST_0          0 
               30  STORE_FAST               'scrambles'

 L.  21        32  LOAD_GLOBAL              args
               34  LOAD_ATTR                input_file
               36  POP_JUMP_IF_FALSE    92  'to 92'

 L.  22        38  LOAD_GLOBAL              open
               40  LOAD_GLOBAL              args
               42  LOAD_ATTR                input_file
               44  LOAD_STR                 'r'
               46  CALL_FUNCTION_2       2  ''
               48  SETUP_WITH           84  'to 84'
               50  STORE_FAST               'f'

 L.  23        52  LOAD_FAST                'f'
               54  GET_ITER         
               56  FOR_ITER             80  'to 80'
               58  STORE_FAST               'line'

 L.  24        60  LOAD_FAST                'scrambles'
               62  LOAD_METHOD              append
               64  LOAD_FAST                'line'
               66  LOAD_METHOD              replace
               68  LOAD_STR                 '\n'
               70  LOAD_STR                 ''
               72  CALL_METHOD_2         2  ''
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_BACK            56  'to 56'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       48  '48'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      
               90  JUMP_FORWARD        100  'to 100'
             92_0  COME_FROM            36  '36'

 L.  26        92  LOAD_GLOBAL              args
               94  LOAD_ATTR                scramble
               96  BUILD_LIST_1          1 
               98  STORE_FAST               'scrambles'
            100_0  COME_FROM            90  '90'

 L.  28       100  LOAD_FAST                'scrambles'
              102  GET_ITER         
              104  FOR_ITER            334  'to 334'
              106  STORE_FAST               'scramble'

 L.  29       108  LOAD_GLOBAL              args
              110  LOAD_ATTR                output_file
              112  POP_JUMP_IF_FALSE   158  'to 158'

 L.  30       114  LOAD_GLOBAL              open
              116  LOAD_GLOBAL              args
              118  LOAD_ATTR                output_file
              120  LOAD_STR                 'a'
              122  CALL_FUNCTION_2       2  ''
              124  SETUP_WITH          150  'to 150'
              126  STORE_FAST               'f'

 L.  31       128  LOAD_FAST                'f'
              130  LOAD_METHOD              write
              132  LOAD_STR                 'Solving: '
              134  LOAD_FAST                'scramble'
              136  FORMAT_VALUE          0  ''
              138  LOAD_STR                 '\n'
              140  BUILD_STRING_3        3 
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
              146  POP_BLOCK        
              148  BEGIN_FINALLY    
            150_0  COME_FROM_WITH      124  '124'
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      
              156  JUMP_FORWARD        172  'to 172'
            158_0  COME_FROM           112  '112'

 L.  33       158  LOAD_GLOBAL              print
              160  LOAD_STR                 'Solving: '
              162  LOAD_FAST                'scramble'
              164  FORMAT_VALUE          0  ''
              166  BUILD_STRING_2        2 
              168  CALL_FUNCTION_1       1  ''
              170  POP_TOP          
            172_0  COME_FROM           156  '156'

 L.  35       172  LOAD_FAST                'pyra'
              174  LOAD_METHOD              search_scramble
              176  LOAD_FAST                'scramble'
              178  LOAD_FAST                'slack'
              180  CALL_METHOD_2         2  ''
              182  STORE_FAST               'solutions'

 L.  36       184  LOAD_FAST                'solutions'
              186  GET_ITER         
              188  FOR_ITER            280  'to 280'
              190  UNPACK_SEQUENCE_4     4 
              192  STORE_FAST               'solution'
              194  STORE_FAST               'length'
              196  STORE_FAST               'time'
              198  STORE_FAST               'path'

 L.  37       200  LOAD_GLOBAL              args
              202  LOAD_ATTR                output_file
              204  POP_JUMP_IF_FALSE   248  'to 248'

 L.  38       206  LOAD_GLOBAL              open
              208  LOAD_GLOBAL              args
              210  LOAD_ATTR                output_file
              212  LOAD_STR                 'a'
              214  CALL_FUNCTION_2       2  ''
              216  SETUP_WITH          240  'to 240'
              218  STORE_FAST               'f'

 L.  39       220  LOAD_FAST                'f'
              222  LOAD_METHOD              write
              224  LOAD_FAST                'solution'
              226  FORMAT_VALUE          0  ''
              228  LOAD_STR                 '\n'
              230  BUILD_STRING_2        2 
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  POP_BLOCK        
              238  BEGIN_FINALLY    
            240_0  COME_FROM_WITH      216  '216'
              240  WITH_CLEANUP_START
              242  WITH_CLEANUP_FINISH
              244  END_FINALLY      
              246  JUMP_BACK           188  'to 188'
            248_0  COME_FROM           204  '204'

 L.  41       248  LOAD_GLOBAL              print
              250  LOAD_FAST                'solution'
              252  FORMAT_VALUE          0  ''
              254  LOAD_STR                 ' ('
              256  LOAD_FAST                'length'
              258  FORMAT_VALUE          0  ''
              260  LOAD_STR                 ' moves found in '
              262  LOAD_FAST                'time'
              264  LOAD_CONST               1000000
              266  BINARY_FLOOR_DIVIDE
              268  FORMAT_VALUE          0  ''
              270  LOAD_STR                 'ms)'
              272  BUILD_STRING_6        6 
              274  CALL_FUNCTION_1       1  ''
              276  POP_TOP          
              278  JUMP_BACK           188  'to 188'

 L.  43       280  LOAD_GLOBAL              args
              282  LOAD_ATTR                output_file
          284_286  POP_JUMP_IF_FALSE   324  'to 324'

 L.  44       288  LOAD_GLOBAL              open
              290  LOAD_GLOBAL              args
              292  LOAD_ATTR                output_file
              294  LOAD_STR                 'a'
              296  CALL_FUNCTION_2       2  ''
              298  SETUP_WITH          316  'to 316'
              300  STORE_FAST               'f'

 L.  45       302  LOAD_FAST                'f'
              304  LOAD_METHOD              write
              306  LOAD_STR                 '\n'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          
              312  POP_BLOCK        
              314  BEGIN_FINALLY    
            316_0  COME_FROM_WITH      298  '298'
              316  WITH_CLEANUP_START
              318  WITH_CLEANUP_FINISH
              320  END_FINALLY      
              322  JUMP_BACK           104  'to 104'
            324_0  COME_FROM           284  '284'

 L.  47       324  LOAD_GLOBAL              print
              326  LOAD_STR                 ''
              328  CALL_FUNCTION_1       1  ''
              330  POP_TOP          
              332  JUMP_BACK           104  'to 104'

Parse error at or near `BEGIN_FINALLY' instruction at offset 82


def setup():
    print('Setting up the initial pyraminx graph')
    graph_setup
    print('Pyraminx graph generated, PyraminXolver is now ready for use!')