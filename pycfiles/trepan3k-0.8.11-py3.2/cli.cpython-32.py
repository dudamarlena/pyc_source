# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/cli.py
# Compiled at: 2018-08-19 14:41:23
"""The command-line interface to the debugger.
"""
import os, pyficache, sys, tempfile, os.path as osp
package = 'trepan'
from trepan import client as Mclient
from trepan import clifns as Mclifns
from trepan import debugger as Mdebugger
from trepan import exception as Mexcept
from trepan import options as Moptions
from trepan.interfaces import server as Mserver
from trepan.lib import file as Mfile
from trepan import misc as Mmisc
__title__ = package
from trepan.version import VERSION

def main--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              list
                3  LOAD_FAST                'sys_argv'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  STORE_FAST               'orig_sys_argv'

 L.  47        12  LOAD_GLOBAL              Moptions
               15  LOAD_ATTR                process_options
               18  LOAD_GLOBAL              __title__

 L.  48        21  LOAD_GLOBAL              VERSION

 L.  49        24  LOAD_FAST                'sys_argv'
               27  CALL_FUNCTION_3       3  '3 positional, 0 named'
               30  UNPACK_SEQUENCE_3     3 
               33  STORE_FAST               'opts'
               36  STORE_FAST               'dbg_opts'
               39  STORE_FAST               'sys_argv'

 L.  51        42  LOAD_FAST                'opts'
               45  LOAD_ATTR                server
               48  LOAD_CONST               None
               51  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE   218  'to 218'

 L.  52        57  LOAD_FAST                'opts'
               60  LOAD_ATTR                server
               63  LOAD_STR                 'tcp'
               66  COMPARE_OP               ==
               69  POP_JUMP_IF_FALSE    98  'to 98'

 L.  53        72  BUILD_MAP_2           2  ''
               75  LOAD_STR                 'TCP'
               78  LOAD_STR                 'IO'
               81  STORE_MAP        
               82  LOAD_FAST                'opts'
               85  LOAD_ATTR                port
               88  LOAD_STR                 'PORT'
               91  STORE_MAP        
               92  STORE_FAST               'connection_opts'
               95  JUMP_FORWARD        111  'to 111'
               98  ELSE                     '111'

 L.  55        98  BUILD_MAP_1           1  ''
              101  LOAD_STR                 'FIFO'
              104  LOAD_STR                 'IO'
              107  STORE_MAP        
              108  STORE_FAST               'connection_opts'
            111_0  COME_FROM            95  '95'

 L.  56       111  LOAD_GLOBAL              Mserver
              114  LOAD_ATTR                ServerInterface
              117  LOAD_STR                 'connection_opts'
              120  LOAD_FAST                'connection_opts'
              123  CALL_FUNCTION_256   256  '0 positional, 1 named'
              126  STORE_FAST               'intf'

 L.  57       129  LOAD_FAST                'intf'
              132  LOAD_FAST                'dbg_opts'
              135  LOAD_STR                 'interface'
              138  STORE_SUBSCR     

 L.  58       139  LOAD_STR                 'FIFO'
              142  LOAD_FAST                'intf'
              145  LOAD_ATTR                server_type
              148  COMPARE_OP               ==
              151  POP_JUMP_IF_FALSE   177  'to 177'

 L.  59       154  LOAD_GLOBAL              print
              157  LOAD_STR                 'Starting FIFO server for process %s.'
              160  LOAD_GLOBAL              os
              163  LOAD_ATTR                getpid
              166  CALL_FUNCTION_0       0  '0 positional, 0 named'
              169  BINARY_MODULO    
              170  CALL_FUNCTION_1       1  '1 positional, 0 named'
              173  POP_TOP          
              174  JUMP_ABSOLUTE       247  'to 247'
              177  ELSE                     '215'

 L.  60       177  LOAD_STR                 'TCP'
              180  LOAD_FAST                'intf'
              183  LOAD_ATTR                server_type
              186  COMPARE_OP               ==
              189  POP_JUMP_IF_FALSE   247  'to 247'

 L.  61       192  LOAD_GLOBAL              print
              195  LOAD_STR                 'Starting TCP server listening on port %s.'

 L.  62       198  LOAD_FAST                'intf'
              201  LOAD_ATTR                inout
              204  LOAD_ATTR                PORT
              207  BINARY_MODULO    
              208  CALL_FUNCTION_1       1  '1 positional, 0 named'
              211  POP_TOP          

 L.  63       212  JUMP_ABSOLUTE       247  'to 247'
              215  JUMP_FORWARD        247  'to 247'
              218  ELSE                     '247'

 L.  64       218  LOAD_FAST                'opts'
              221  LOAD_ATTR                client
              224  POP_JUMP_IF_FALSE   247  'to 247'

 L.  65       227  LOAD_GLOBAL              Mclient
              230  LOAD_ATTR                run
              233  LOAD_FAST                'opts'
              236  LOAD_FAST                'sys_argv'
              239  CALL_FUNCTION_2       2  '2 positional, 0 named'
              242  POP_TOP          

 L.  66       243  LOAD_CONST               None
              246  RETURN_END_IF    
            247_0  COME_FROM           215  '215'

 L.  68       247  LOAD_FAST                'orig_sys_argv'
              250  LOAD_FAST                'dbg_opts'
              253  LOAD_STR                 'orig_sys_argv'
              256  STORE_SUBSCR     

 L.  70       257  LOAD_FAST                'dbg'
              260  LOAD_CONST               None
              263  COMPARE_OP               is
              266  POP_JUMP_IF_FALSE   303  'to 303'

 L.  71       269  LOAD_GLOBAL              Mdebugger
              272  LOAD_ATTR                Trepan
              275  LOAD_FAST                'dbg_opts'
              278  CALL_FUNCTION_1       1  '1 positional, 0 named'
              281  STORE_FAST               'dbg'

 L.  72       284  LOAD_FAST                'dbg'
              287  LOAD_ATTR                core
              290  LOAD_ATTR                add_ignore
              293  LOAD_GLOBAL              main
              296  CALL_FUNCTION_1       1  '1 positional, 0 named'
              299  POP_TOP          

 L.  73       300  JUMP_FORWARD        303  'to 303'
            303_0  COME_FROM           300  '300'

 L.  74       303  LOAD_GLOBAL              Moptions
              306  LOAD_ATTR                _postprocess_options
              309  LOAD_FAST                'dbg'
              312  LOAD_FAST                'opts'
              315  CALL_FUNCTION_2       2  '2 positional, 0 named'
              318  POP_TOP          

 L.  80       319  LOAD_GLOBAL              len
              322  LOAD_FAST                'sys_argv'
              325  CALL_FUNCTION_1       1  '1 positional, 0 named'
              328  LOAD_CONST               0
              331  COMPARE_OP               ==
              334  POP_JUMP_IF_FALSE   346  'to 346'

 L.  83       337  LOAD_CONST               None
              340  STORE_FAST               'mainpyfile'
              343  JUMP_FORWARD       1261  'to 1261'
              346  ELSE                     '1261'

 L.  85       346  LOAD_FAST                'sys_argv'
              349  LOAD_CONST               0
              352  BINARY_SUBSCR    
              353  STORE_FAST               'mainpyfile'

 L.  86       356  LOAD_GLOBAL              osp
              359  LOAD_ATTR                isfile
              362  LOAD_FAST                'mainpyfile'
              365  CALL_FUNCTION_1       1  '1 positional, 0 named'
              368  POP_JUMP_IF_TRUE    495  'to 495'

 L.  87       371  LOAD_GLOBAL              Mclifns
              374  LOAD_ATTR                whence_file
              377  LOAD_FAST                'mainpyfile'
              380  CALL_FUNCTION_1       1  '1 positional, 0 named'
              383  STORE_FAST               'mainpyfile'

 L.  88       386  LOAD_GLOBAL              Mfile
              389  LOAD_ATTR                readable
              392  LOAD_FAST                'mainpyfile'
              395  CALL_FUNCTION_1       1  '1 positional, 0 named'
              398  STORE_FAST               'is_readable'

 L.  89       401  LOAD_FAST                'is_readable'
              404  LOAD_CONST               None
              407  COMPARE_OP               is
              410  POP_JUMP_IF_FALSE   449  'to 449'

 L.  90       413  LOAD_GLOBAL              print
              416  LOAD_STR                 "%s: Python script file '%s' does not exist"

 L.  91       419  LOAD_GLOBAL              __title__
              422  LOAD_FAST                'mainpyfile'
              425  BUILD_TUPLE_2         2 
              428  BINARY_MODULO    
              429  CALL_FUNCTION_1       1  '1 positional, 0 named'
              432  POP_TOP          

 L.  92       433  LOAD_GLOBAL              sys
              436  LOAD_ATTR                exit
              439  LOAD_CONST               1
              442  CALL_FUNCTION_1       1  '1 positional, 0 named'
              445  POP_TOP          
              446  JUMP_ABSOLUTE       495  'to 495'
              449  ELSE                     '492'

 L.  93       449  LOAD_FAST                'is_readable'
              452  POP_JUMP_IF_TRUE    495  'to 495'

 L.  94       455  LOAD_GLOBAL              print
              458  LOAD_STR                 "%s: Can't read Python script file '%s'"

 L.  95       461  LOAD_GLOBAL              __title__
              464  LOAD_FAST                'mainpyfile'
              467  BUILD_TUPLE_2         2 
              470  BINARY_MODULO    
              471  CALL_FUNCTION_1       1  '1 positional, 0 named'
              474  POP_TOP          

 L.  96       475  LOAD_GLOBAL              sys
              478  LOAD_ATTR                exit
              481  LOAD_CONST               1
              484  CALL_FUNCTION_1       1  '1 positional, 0 named'
              487  POP_TOP          

 L.  97       488  LOAD_CONST               None
              491  RETURN_END_IF    
              492  JUMP_FORWARD        495  'to 495'
            495_0  COME_FROM           492  '492'

 L.  99       495  LOAD_GLOBAL              Mfile
              498  LOAD_ATTR                is_compiled_py
              501  LOAD_FAST                'mainpyfile'
              504  CALL_FUNCTION_1       1  '1 positional, 0 named'
              507  POP_JUMP_IF_FALSE  1147  'to 1147'

 L. 100       510  SETUP_EXCEPT        811  'to 811'

 L. 101       513  LOAD_CONST               0
              516  LOAD_CONST               ('load_module', 'PYTHON_VERSION', 'IS_PYPY')
              519  IMPORT_NAME              xdis
              522  IMPORT_FROM              load_module
              525  STORE_FAST               'load_module'
              528  IMPORT_FROM              PYTHON_VERSION
              531  STORE_FAST               'PYTHON_VERSION'
              534  IMPORT_FROM              IS_PYPY
              537  STORE_FAST               'IS_PYPY'
              540  POP_TOP          

 L. 103       541  LOAD_FAST                'load_module'
              544  LOAD_FAST                'mainpyfile'
              547  LOAD_STR                 'code_objects'
              550  LOAD_CONST               None
              553  LOAD_STR                 'fast_load'

 L. 104       556  LOAD_CONST               True
              559  CALL_FUNCTION_513   513  '1 positional, 2 named'
              562  UNPACK_SEQUENCE_6     6 
              565  STORE_FAST               'python_version'
              568  STORE_FAST               'timestamp'
              571  STORE_FAST               'magic_int'
              574  STORE_FAST               'co'
              577  STORE_FAST               'is_pypy'
              580  STORE_FAST               'source_size'

 L. 105       583  LOAD_FAST                'is_pypy'
              586  LOAD_FAST                'IS_PYPY'
              589  COMPARE_OP               ==
              592  POP_JUMP_IF_TRUE    601  'to 601'
              595  LOAD_ASSERT              AssertionError
              598  RAISE_VARARGS_1       1  'exception'
            601_0  COME_FROM           592  '592'

 L. 106       601  LOAD_FAST                'python_version'
              604  LOAD_FAST                'PYTHON_VERSION'
              607  COMPARE_OP               ==
              610  POP_JUMP_IF_TRUE    635  'to 635'
              613  LOAD_ASSERT              AssertionError

 L. 107       616  LOAD_STR                 'bytecode is for version %s but we are version %s'

 L. 108       619  LOAD_FAST                'python_version'
              622  LOAD_FAST                'PYTHON_VERSION'
              625  BUILD_TUPLE_2         2 
              628  BINARY_MODULO    
              629  CALL_FUNCTION_1       1  '1 positional, 0 named'
              632  RAISE_VARARGS_1       1  'exception'
            635_0  COME_FROM           610  '610'

 L. 111       635  LOAD_FAST                'co'
              638  LOAD_ATTR                co_filename
              641  STORE_FAST               'py_file'

 L. 112       644  LOAD_GLOBAL              osp
              647  LOAD_ATTR                isabs
              650  LOAD_FAST                'py_file'
              653  CALL_FUNCTION_1       1  '1 positional, 0 named'
              656  POP_JUMP_IF_FALSE   668  'to 668'

 L. 113       659  LOAD_FAST                'py_file'
              662  STORE_FAST               'try_file'
              665  JUMP_FORWARD        767  'to 767'
              668  ELSE                     '767'

 L. 115       668  LOAD_GLOBAL              osp
              671  LOAD_ATTR                dirname
              674  LOAD_FAST                'mainpyfile'
              677  CALL_FUNCTION_1       1  '1 positional, 0 named'
              680  STORE_FAST               'mainpydir'

 L. 116       683  LOAD_GLOBAL              sys
              686  LOAD_ATTR                implementation
              689  LOAD_ATTR                cache_tag
              692  STORE_FAST               'tag'

 L. 118       695  LOAD_GLOBAL              osp
              698  LOAD_ATTR                join
              701  LOAD_FAST                'mainpydir'
              704  LOAD_FAST                'tag'
              707  CALL_FUNCTION_2       2  '2 positional, 0 named'
              710  LOAD_FAST                'mainpydir'
              713  BUILD_LIST_2          2 
              716  LOAD_GLOBAL              os
              719  LOAD_ATTR                environ
              722  LOAD_STR                 'PATH'
              725  BINARY_SUBSCR    
              726  LOAD_ATTR                split
              729  LOAD_GLOBAL              osp
              732  LOAD_ATTR                pathsep
              735  CALL_FUNCTION_1       1  '1 positional, 0 named'
              738  BINARY_ADD       
              739  LOAD_STR                 '.'
              742  BUILD_LIST_1          1 
              745  BINARY_ADD       
              746  STORE_FAST               'dirnames'

 L. 119       749  LOAD_GLOBAL              Mclifns
              752  LOAD_ATTR                whence_file
              755  LOAD_FAST                'py_file'
              758  LOAD_FAST                'dirnames'
              761  CALL_FUNCTION_2       2  '2 positional, 0 named'
              764  STORE_FAST               'try_file'
            767_0  COME_FROM           665  '665'

 L. 121       767  LOAD_GLOBAL              osp
              770  LOAD_ATTR                isfile
              773  LOAD_FAST                'try_file'
              776  CALL_FUNCTION_1       1  '1 positional, 0 named'
              779  POP_JUMP_IF_FALSE   791  'to 791'

 L. 122       782  LOAD_FAST                'try_file'
              785  STORE_FAST               'mainpyfile'

 L. 123       788  JUMP_FORWARD        807  'to 807'
              791  ELSE                     '807'

 L. 126       791  LOAD_GLOBAL              IOError
              794  LOAD_STR                 'Python file name embedded in code %s not found'
              797  LOAD_FAST                'try_file'
              800  BINARY_MODULO    
              801  CALL_FUNCTION_1       1  '1 positional, 0 named'
              804  RAISE_VARARGS_1       1  'exception'
            807_0  COME_FROM           788  '788'
              807  POP_BLOCK        
              808  JUMP_ABSOLUTE      1147  'to 1147'
            811_0  COME_FROM_EXCEPT    510  '510'

 L. 127       811  DUP_TOP          
              812  LOAD_GLOBAL              IOError
              815  COMPARE_OP               exception-match
              818  POP_JUMP_IF_FALSE  1143  'to 1143'
              821  POP_TOP          
              822  POP_TOP          
              823  POP_TOP          

 L. 128       824  SETUP_EXCEPT        847  'to 847'

 L. 129       827  LOAD_CONST               0
              830  LOAD_CONST               ('decompile_file',)
              833  IMPORT_NAME              uncompyle6
              836  IMPORT_FROM              decompile_file
              839  STORE_FAST               'decompile_file'
              842  POP_TOP          
              843  POP_BLOCK        
              844  JUMP_FORWARD        911  'to 911'
            847_0  COME_FROM_EXCEPT    824  '824'

 L. 130       847  DUP_TOP          
              848  LOAD_GLOBAL              ImportError
              851  COMPARE_OP               exception-match
              854  POP_JUMP_IF_FALSE   910  'to 910'
              857  POP_TOP          
              858  POP_TOP          
              859  POP_TOP          

 L. 131       860  LOAD_GLOBAL              print
              863  LOAD_STR                 "%s: Compiled python file '%s', but uncompyle6 not found"

 L. 132       866  LOAD_GLOBAL              __title__
              869  LOAD_FAST                'mainpyfile'
              872  BUILD_TUPLE_2         2 
              875  BINARY_MODULO    
              876  LOAD_STR                 'file'
              879  LOAD_GLOBAL              sys
              882  LOAD_ATTR                stderr
              885  CALL_FUNCTION_257   257  '1 positional, 1 named'
              888  POP_TOP          

 L. 133       889  LOAD_GLOBAL              sys
              892  LOAD_ATTR                exit
              895  LOAD_CONST               1
              898  CALL_FUNCTION_1       1  '1 positional, 0 named'
              901  POP_TOP          

 L. 134       902  LOAD_CONST               None
              905  RETURN_VALUE     
              906  POP_EXCEPT       
              907  JUMP_FORWARD        911  'to 911'
              910  END_FINALLY      
            911_0  COME_FROM           907  '907'
            911_1  COME_FROM           844  '844'

 L. 136       911  LOAD_GLOBAL              osp
              914  LOAD_ATTR                basename
              917  LOAD_FAST                'mainpyfile'
              920  CALL_FUNCTION_1       1  '1 positional, 0 named'
              923  LOAD_ATTR                strip
              926  LOAD_STR                 '.pyc'
              929  CALL_FUNCTION_1       1  '1 positional, 0 named'
              932  STORE_FAST               'short_name'

 L. 137       935  LOAD_GLOBAL              tempfile
              938  LOAD_ATTR                NamedTemporaryFile
              941  LOAD_STR                 'suffix'
              944  LOAD_STR                 '.py'
              947  LOAD_STR                 'prefix'

 L. 138       950  LOAD_FAST                'short_name'
              953  LOAD_STR                 '_'
              956  BINARY_ADD       
              957  LOAD_STR                 'delete'

 L. 139       960  LOAD_CONST               False
              963  CALL_FUNCTION_768   768  '0 positional, 3 named'
              966  STORE_FAST               'fd'

 L. 140       969  LOAD_FAST                'fd'
              972  LOAD_ATTR                file
              975  LOAD_ATTR                write
              978  STORE_DEREF              'old_write'

 L. 142       981  LOAD_CLOSURE             'old_write'
              984  BUILD_TUPLE_1         1 
              987  LOAD_CODE                <code_object write_wrapper>
              990  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
              993  STORE_FAST               'write_wrapper'

 L. 149       996  LOAD_FAST                'write_wrapper'
              999  LOAD_FAST                'fd'
             1002  LOAD_ATTR                file
             1005  STORE_ATTR               write

 L. 153      1008  SETUP_EXCEPT       1037  'to 1037'

 L. 154      1011  LOAD_FAST                'decompile_file'
             1014  LOAD_FAST                'mainpyfile'
             1017  LOAD_FAST                'fd'
             1020  LOAD_ATTR                file
             1023  LOAD_STR                 'mapstream'
             1026  LOAD_FAST                'fd'
             1029  CALL_FUNCTION_258   258  '2 positional, 1 named'
             1032  POP_TOP          
             1033  POP_BLOCK        
             1034  JUMP_FORWARD       1091  'to 1091'
           1037_0  COME_FROM_EXCEPT   1008  '1008'

 L. 155      1037  POP_TOP          
             1038  POP_TOP          
             1039  POP_TOP          

 L. 156      1040  LOAD_GLOBAL              print
             1043  LOAD_STR                 "%s: error decompiling '%s'"

 L. 157      1046  LOAD_GLOBAL              __title__
             1049  LOAD_FAST                'mainpyfile'
             1052  BUILD_TUPLE_2         2 
             1055  BINARY_MODULO    
             1056  LOAD_STR                 'file'
             1059  LOAD_GLOBAL              sys
             1062  LOAD_ATTR                stderr
             1065  CALL_FUNCTION_257   257  '1 positional, 1 named'
             1068  POP_TOP          

 L. 158      1069  LOAD_GLOBAL              sys
             1072  LOAD_ATTR                exit
             1075  LOAD_CONST               1
             1078  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1081  POP_TOP          

 L. 159      1082  LOAD_CONST               None
             1085  RETURN_VALUE     
             1086  POP_EXCEPT       
             1087  JUMP_FORWARD       1091  'to 1091'
             1090  END_FINALLY      
           1091_0  COME_FROM          1087  '1087'
           1091_1  COME_FROM          1034  '1034'

 L. 166      1091  LOAD_FAST                'fd'
             1094  LOAD_ATTR                name
             1097  STORE_FAST               'mainpyfile'

 L. 167      1100  LOAD_FAST                'fd'
             1103  LOAD_ATTR                close
             1106  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1109  POP_TOP          

 L. 175      1110  LOAD_GLOBAL              print
             1113  LOAD_STR                 "%s: couldn't find Python source so we recreated it at '%s'"

 L. 176      1116  LOAD_GLOBAL              __title__
             1119  LOAD_FAST                'mainpyfile'
             1122  BUILD_TUPLE_2         2 
             1125  BINARY_MODULO    
             1126  LOAD_STR                 'file'
             1129  LOAD_GLOBAL              sys
             1132  LOAD_ATTR                stderr
             1135  CALL_FUNCTION_257   257  '1 positional, 1 named'
             1138  POP_TOP          

 L. 178      1139  POP_EXCEPT       
             1140  JUMP_ABSOLUTE      1147  'to 1147'
             1143  END_FINALLY      
             1144  JUMP_FORWARD       1147  'to 1147'
           1147_0  COME_FROM          1144  '1144'

 L. 182      1147  LOAD_GLOBAL              pyficache
             1150  LOAD_ATTR                pyc2py
             1153  LOAD_FAST                'mainpyfile'
             1156  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1159  STORE_FAST               'mainpyfile_noopt'

 L. 183      1162  LOAD_FAST                'mainpyfile'
             1165  LOAD_FAST                'mainpyfile_noopt'
             1168  COMPARE_OP               !=
             1171  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 184      1174  LOAD_GLOBAL              Mfile
             1177  LOAD_ATTR                readable
             1180  LOAD_FAST                'mainpyfile_noopt'
             1183  CALL_FUNCTION_1       1  '1 positional, 0 named'
           1186_0  COME_FROM          1171  '1171'
             1186  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 185      1189  LOAD_GLOBAL              print
             1192  LOAD_STR                 "%s: Compiled Python script given and we can't use that."

 L. 186      1195  LOAD_GLOBAL              __title__
             1198  BINARY_MODULO    
             1199  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1202  POP_TOP          

 L. 187      1203  LOAD_GLOBAL              print
             1206  LOAD_STR                 '%s: Substituting non-compiled name: %s'

 L. 188      1209  LOAD_GLOBAL              __title__
             1212  LOAD_FAST                'mainpyfile_noopt'
             1215  BUILD_TUPLE_2         2 
             1218  BINARY_MODULO    
             1219  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1222  POP_TOP          

 L. 189      1223  LOAD_FAST                'mainpyfile_noopt'
             1226  STORE_FAST               'mainpyfile'

 L. 190      1229  JUMP_FORWARD       1232  'to 1232'
           1232_0  COME_FROM          1229  '1229'

 L. 194      1232  LOAD_GLOBAL              osp
             1235  LOAD_ATTR                dirname
             1238  LOAD_FAST                'mainpyfile'
             1241  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1244  DUP_TOP          
             1245  LOAD_GLOBAL              sys
             1248  LOAD_ATTR                path
             1251  LOAD_CONST               0
             1254  STORE_SUBSCR     
             1255  LOAD_FAST                'dbg'
             1258  STORE_ATTR               main_dirname
           1261_0  COME_FROM           343  '343'

 L. 198      1261  LOAD_CONST               False
             1264  LOAD_FAST                'dbg'
             1267  STORE_ATTR               sig_received

 L. 205      1270  SETUP_LOOP         1597  'to 1597'

 L. 210      1273  SETUP_EXCEPT       1399  'to 1399'

 L. 211      1276  LOAD_FAST                'dbg'
             1279  LOAD_ATTR                program_sys_argv
             1282  POP_JUMP_IF_FALSE  1319  'to 1319'
             1285  LOAD_FAST                'mainpyfile'
           1288_0  COME_FROM          1282  '1282'
             1288  POP_JUMP_IF_FALSE  1319  'to 1319'

 L. 212      1291  LOAD_FAST                'dbg'
             1294  LOAD_ATTR                run_script
             1297  LOAD_FAST                'mainpyfile'
             1300  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1303  STORE_FAST               'normal_termination'

 L. 213      1306  LOAD_FAST                'normal_termination'
             1309  POP_JUMP_IF_TRUE   1347  'to 1347'

 L. 213      1312  BREAK_LOOP       
             1313  JUMP_ABSOLUTE      1347  'to 1347'
             1316  JUMP_FORWARD       1347  'to 1347'
             1319  ELSE                     '1347'

 L. 215      1319  LOAD_STR                 'No program'
             1322  LOAD_FAST                'dbg'
             1325  LOAD_ATTR                core
             1328  STORE_ATTR               execution_status

 L. 216      1331  LOAD_FAST                'dbg'
             1334  LOAD_ATTR                core
             1337  LOAD_ATTR                processor
             1340  LOAD_ATTR                process_commands
             1343  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1346  POP_TOP          
           1347_0  COME_FROM          1316  '1316'

 L. 219      1347  LOAD_STR                 'Terminated'
             1350  LOAD_FAST                'dbg'
             1353  LOAD_ATTR                core
             1356  STORE_ATTR               execution_status

 L. 220      1359  LOAD_FAST                'dbg'
             1362  LOAD_ATTR                intf
             1365  LOAD_CONST               -1
             1368  BINARY_SUBSCR    
             1369  LOAD_ATTR                msg
             1372  LOAD_STR                 'The program finished - quit or restart'
             1375  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1378  POP_TOP          

 L. 221      1379  LOAD_FAST                'dbg'
             1382  LOAD_ATTR                core
             1385  LOAD_ATTR                processor
             1388  LOAD_ATTR                process_commands
             1391  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1394  POP_TOP          
             1395  POP_BLOCK        
             1396  JUMP_BACK          1273  'to 1273'
           1399_0  COME_FROM_EXCEPT   1273  '1273'

 L. 222      1399  DUP_TOP          
             1400  LOAD_GLOBAL              Mexcept
             1403  LOAD_ATTR                DebuggerQuit
             1406  COMPARE_OP               exception-match
             1409  POP_JUMP_IF_FALSE  1420  'to 1420'
             1412  POP_TOP          
             1413  POP_TOP          
             1414  POP_TOP          

 L. 223      1415  BREAK_LOOP       
             1416  POP_EXCEPT       
             1417  JUMP_BACK          1273  'to 1273'

 L. 224      1420  DUP_TOP          
             1421  LOAD_GLOBAL              Mexcept
             1424  LOAD_ATTR                DebuggerRestart
             1427  COMPARE_OP               exception-match
             1430  POP_JUMP_IF_FALSE  1575  'to 1575'
             1433  POP_TOP          
             1434  POP_TOP          
             1435  POP_TOP          

 L. 225      1436  LOAD_STR                 'Restart requested'
             1439  LOAD_FAST                'dbg'
             1442  LOAD_ATTR                core
             1445  STORE_ATTR               execution_status

 L. 226      1448  LOAD_FAST                'dbg'
             1451  LOAD_ATTR                program_sys_argv
             1454  POP_JUMP_IF_FALSE  1570  'to 1570'

 L. 227      1457  LOAD_GLOBAL              list
             1460  LOAD_FAST                'dbg'
             1463  LOAD_ATTR                program_sys_argv
             1466  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1469  LOAD_GLOBAL              sys
             1472  STORE_ATTR               argv

 L. 228      1475  LOAD_STR                 'Restarting %s with arguments:'

 L. 229      1478  LOAD_FAST                'dbg'
             1481  LOAD_ATTR                core
             1484  LOAD_ATTR                filename
             1487  LOAD_FAST                'mainpyfile'
             1490  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1493  BINARY_MODULO    
             1494  STORE_FAST               'part1'

 L. 230      1497  LOAD_STR                 ' '
             1500  LOAD_ATTR                join
             1503  LOAD_FAST                'dbg'
             1506  LOAD_ATTR                program_sys_argv
             1509  LOAD_CONST               1
             1512  LOAD_CONST               None
             1515  BUILD_SLICE_2         2 
             1518  BINARY_SUBSCR    
             1519  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1522  STORE_FAST               'args'

 L. 231      1525  LOAD_FAST                'dbg'
             1528  LOAD_ATTR                intf
             1531  LOAD_CONST               -1
             1534  BINARY_SUBSCR    
             1535  LOAD_ATTR                msg

 L. 232      1538  LOAD_GLOBAL              Mmisc
             1541  LOAD_ATTR                wrapped_lines
             1544  LOAD_FAST                'part1'
             1547  LOAD_FAST                'args'

 L. 233      1550  LOAD_FAST                'dbg'
             1553  LOAD_ATTR                settings
             1556  LOAD_STR                 'width'
             1559  BINARY_SUBSCR    
             1560  CALL_FUNCTION_3       3  '3 positional, 0 named'
             1563  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1566  POP_TOP          
             1567  JUMP_FORWARD       1571  'to 1571'
             1570  ELSE                     '1571'

 L. 234      1570  BREAK_LOOP       
           1571_0  COME_FROM          1567  '1567'
             1571  POP_EXCEPT       
             1572  JUMP_BACK          1273  'to 1273'

 L. 235      1575  DUP_TOP          
             1576  LOAD_GLOBAL              SystemExit
             1579  COMPARE_OP               exception-match
             1582  POP_JUMP_IF_FALSE  1593  'to 1593'
             1585  POP_TOP          
             1586  POP_TOP          
             1587  POP_TOP          

 L. 237      1588  BREAK_LOOP       
             1589  POP_EXCEPT       
             1590  JUMP_BACK          1273  'to 1273'
             1593  END_FINALLY      

 L. 238      1594  CONTINUE           1273  'to 1273'
           1597_0  COME_FROM_LOOP     1270  '1270'

 L. 241      1597  LOAD_FAST                'orig_sys_argv'
             1600  LOAD_GLOBAL              sys
             1603  STORE_ATTR               argv

 L. 242      1606  LOAD_CONST               None
             1609  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 1597


if __name__ == '__main__':
    main()
# global __title__ ## Warning: Unused global