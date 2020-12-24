# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/player.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 3927 bytes
import logging, vlc
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal, get_app
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit import HTML, print_formatted_text
from .lib import seconds_to_human
from .playlist import print_playlist
logger = logging.getLogger(__name__)
logging.getLogger('vlc').setLevel(logging.NOTSET)

def play--- This code section failed: ---

 L.  18         0  LOAD_DEREF               'tracks'
                2  POP_JUMP_IF_TRUE     18  'to 18'

 L.  19         4  LOAD_GLOBAL              logger
                6  LOAD_METHOD              warning
                8  LOAD_STR                 'Empty playlist'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L.  20        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM             2  '2'

 L.  22     18_20  SETUP_FINALLY       394  'to 394'

 L.  23        22  LOAD_GLOBAL              vlc
               24  LOAD_METHOD              Instance
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'instance'

 L.  24        30  LOAD_FAST                'instance'
               32  POP_JUMP_IF_TRUE     50  'to 50'

 L.  25        34  LOAD_GLOBAL              logger
               36  LOAD_METHOD              critical
               38  LOAD_STR                 'Unable to start VLC instance'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  26        44  POP_BLOCK        
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            32  '32'

 L.  28        50  LOAD_FAST                'instance'
               52  LOAD_METHOD              media_list_player_new
               54  CALL_METHOD_0         0  ''
               56  STORE_DEREF              'player'

 L.  29        58  LOAD_DEREF               'player'
               60  POP_JUMP_IF_TRUE     78  'to 78'

 L.  30        62  LOAD_GLOBAL              logger
               64  LOAD_METHOD              critical
               66  LOAD_STR                 'Unable to create VLC player'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  31        72  POP_BLOCK        
               74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            60  '60'

 L.  33        78  LOAD_LISTCOMP            '<code_object <listcomp>>'
               80  LOAD_STR                 'play.<locals>.<listcomp>'
               82  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               84  LOAD_DEREF               'tracks'
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'tracks_path'

 L.  34        92  LOAD_FAST                'instance'
               94  LOAD_METHOD              media_list_new
               96  LOAD_FAST                'tracks_path'
               98  CALL_METHOD_1         1  ''
              100  STORE_FAST               'media_list'

 L.  35       102  LOAD_FAST                'media_list'
              104  POP_JUMP_IF_TRUE    122  'to 122'

 L.  36       106  LOAD_GLOBAL              logger
              108  LOAD_METHOD              critical
              110  LOAD_STR                 'Unable to create VLC media list'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L.  37       116  POP_BLOCK        
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM           104  '104'

 L.  39       122  LOAD_DEREF               'player'
              124  LOAD_METHOD              set_media_list
              126  LOAD_FAST                'media_list'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L.  40       132  LOAD_GLOBAL              KeyBindings
              134  CALL_FUNCTION_0       0  ''
              136  STORE_FAST               'bindings'

 L.  42       138  LOAD_CODE                <code_object print_help>
              140  LOAD_STR                 'play.<locals>.print_help'
              142  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              144  STORE_DEREF              'print_help'

 L.  45       146  LOAD_FAST                'bindings'
              148  LOAD_METHOD              add
              150  LOAD_STR                 'p'
              152  CALL_METHOD_1         1  ''

 L.  46       154  LOAD_CLOSURE             'player'
              156  BUILD_TUPLE_1         1 
              158  LOAD_CODE                <code_object _play_binding>
              160  LOAD_STR                 'play.<locals>._play_binding'
              162  MAKE_FUNCTION_8          'closure'
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               '_play_binding'

 L.  52       168  LOAD_FAST                'bindings'
              170  LOAD_METHOD              add
              172  LOAD_STR                 'q'
              174  CALL_METHOD_1         1  ''

 L.  53       176  LOAD_CLOSURE             'player'
              178  BUILD_TUPLE_1         1 
              180  LOAD_CODE                <code_object _quit_binding>
              182  LOAD_STR                 'play.<locals>._quit_binding'
              184  MAKE_FUNCTION_8          'closure'
              186  CALL_FUNCTION_1       1  ''
              188  STORE_FAST               '_quit_binding'

 L.  57       190  LOAD_FAST                'bindings'
              192  LOAD_METHOD              add
              194  LOAD_STR                 's'
              196  CALL_METHOD_1         1  ''

 L.  58       198  LOAD_CLOSURE             'player'
              200  BUILD_TUPLE_1         1 
              202  LOAD_CODE                <code_object _pause_binding>
              204  LOAD_STR                 'play.<locals>._pause_binding'
              206  MAKE_FUNCTION_8          'closure'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               '_pause_binding'

 L.  61       212  LOAD_FAST                'bindings'
              214  LOAD_METHOD              add
              216  LOAD_STR                 'l'
              218  CALL_METHOD_1         1  ''

 L.  62       220  LOAD_CLOSURE             'player'
              222  LOAD_CLOSURE             'tracks'
              224  BUILD_TUPLE_2         2 
              226  LOAD_CODE                <code_object _playlist_binding>
              228  LOAD_STR                 'play.<locals>._playlist_binding'
              230  MAKE_FUNCTION_8          'closure'
              232  CALL_FUNCTION_1       1  ''
              234  STORE_FAST               '_playlist_binding'

 L.  74       236  LOAD_FAST                'bindings'
              238  LOAD_METHOD              add
              240  LOAD_STR                 'right'
              242  CALL_METHOD_1         1  ''

 L.  75       244  LOAD_CLOSURE             'player'
              246  BUILD_TUPLE_1         1 
              248  LOAD_CODE                <code_object _next_binding>
              250  LOAD_STR                 'play.<locals>._next_binding'
              252  MAKE_FUNCTION_8          'closure'
              254  CALL_FUNCTION_1       1  ''
              256  STORE_FAST               '_next_binding'

 L.  78       258  LOAD_FAST                'bindings'
              260  LOAD_METHOD              add
              262  LOAD_STR                 'left'
              264  CALL_METHOD_1         1  ''

 L.  79       266  LOAD_CLOSURE             'player'
              268  BUILD_TUPLE_1         1 
              270  LOAD_CODE                <code_object _previous_binding>
              272  LOAD_STR                 'play.<locals>._previous_binding'
              274  MAKE_FUNCTION_8          'closure'
              276  CALL_FUNCTION_1       1  ''
              278  STORE_FAST               '_previous_binding'

 L.  82       280  LOAD_FAST                'bindings'
              282  LOAD_METHOD              add
              284  LOAD_STR                 'h'
              286  CALL_METHOD_1         1  ''

 L.  83       288  LOAD_CLOSURE             'print_help'
              290  BUILD_TUPLE_1         1 
              292  LOAD_CODE                <code_object _help>
              294  LOAD_STR                 'play.<locals>._help'
              296  MAKE_FUNCTION_8          'closure'
              298  CALL_FUNCTION_1       1  ''
              300  STORE_FAST               '_help'

 L.  89       302  LOAD_CLOSURE             'player'
              304  BUILD_TUPLE_1         1 
              306  LOAD_CODE                <code_object bottom_toolbar>
              308  LOAD_STR                 'play.<locals>.bottom_toolbar'
              310  MAKE_FUNCTION_8          'closure'
              312  STORE_DEREF              'bottom_toolbar'

 L. 102       314  LOAD_DEREF               'print_help'
              316  CALL_FUNCTION_0       0  ''
              318  POP_TOP          

 L. 103       320  LOAD_DEREF               'player'
              322  LOAD_METHOD              play
              324  CALL_METHOD_0         0  ''
              326  POP_TOP          

 L. 105       328  LOAD_GLOBAL              HSplit

 L. 106       330  LOAD_GLOBAL              Window
              332  LOAD_GLOBAL              FormattedTextControl
              334  LOAD_CLOSURE             'bottom_toolbar'
              336  BUILD_TUPLE_1         1 
              338  LOAD_LAMBDA              '<code_object <lambda>>'
              340  LOAD_STR                 'play.<locals>.<lambda>'
              342  MAKE_FUNCTION_8          'closure'
              344  LOAD_STR                 'class:bottom-toolbar.text'
              346  LOAD_CONST               ('style',)
              348  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              350  LOAD_STR                 'class:bottom-toolbar'
              352  LOAD_CONST               ('style',)
              354  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              356  BUILD_LIST_1          1 

 L. 105       358  CALL_FUNCTION_1       1  ''
              360  STORE_FAST               'root_container'

 L. 108       362  LOAD_GLOBAL              Layout
              364  LOAD_FAST                'root_container'
              366  CALL_FUNCTION_1       1  ''
              368  STORE_FAST               'layout'

 L. 109       370  LOAD_GLOBAL              Application
              372  LOAD_FAST                'layout'
              374  LOAD_FAST                'bindings'
              376  LOAD_CONST               ('layout', 'key_bindings')
              378  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              380  STORE_FAST               'app'

 L. 110       382  LOAD_FAST                'app'
              384  LOAD_METHOD              run
              386  CALL_METHOD_0         0  ''
              388  POP_TOP          
              390  POP_BLOCK        
              392  JUMP_FORWARD        432  'to 432'
            394_0  COME_FROM_FINALLY    18  '18'

 L. 111       394  DUP_TOP          
              396  LOAD_GLOBAL              NameError
              398  COMPARE_OP               exception-match
          400_402  POP_JUMP_IF_FALSE   430  'to 430'
              404  POP_TOP          
              406  POP_TOP          
              408  POP_TOP          

 L. 112       410  LOAD_GLOBAL              logger
              412  LOAD_METHOD              critical
              414  LOAD_STR                 'Your VLC version may be outdated: %s'
              416  LOAD_GLOBAL              vlc
              418  LOAD_METHOD              libvlc_get_version
              420  CALL_METHOD_0         0  ''
              422  CALL_METHOD_2         2  ''
              424  POP_TOP          
              426  POP_EXCEPT       
              428  JUMP_FORWARD        432  'to 432'
            430_0  COME_FROM           400  '400'
              430  END_FINALLY      
            432_0  COME_FROM           428  '428'
            432_1  COME_FROM           392  '392'

Parse error at or near `RETURN_VALUE' instruction at offset 48