# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/cli.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 9688 bytes
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
              230  LOAD_ATTR                main
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
              343  JUMP_FORWARD       1264  'to 1264'
              346  ELSE                     '1264'

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
              507  POP_JUMP_IF_FALSE  1150  'to 1150'

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
              808  JUMP_ABSOLUTE      1150  'to 1150'
            811_0  COME_FROM_EXCEPT    510  '510'

 L. 127       811  DUP_TOP          
              812  LOAD_GLOBAL              IOError
              815  COMPARE_OP               exception-match
              818  POP_JUMP_IF_FALSE  1146  'to 1146'
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
              990  LOAD_STR                 'main.<locals>.write_wrapper'
              993  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
              996  STORE_FAST               'write_wrapper'

 L. 149       999  LOAD_FAST                'write_wrapper'
             1002  LOAD_FAST                'fd'
             1005  LOAD_ATTR                file
             1008  STORE_ATTR               write

 L. 153      1011  SETUP_EXCEPT       1040  'to 1040'

 L. 154      1014  LOAD_FAST                'decompile_file'
             1017  LOAD_FAST                'mainpyfile'
             1020  LOAD_FAST                'fd'
             1023  LOAD_ATTR                file
             1026  LOAD_STR                 'mapstream'
             1029  LOAD_FAST                'fd'
             1032  CALL_FUNCTION_258   258  '2 positional, 1 named'
             1035  POP_TOP          
             1036  POP_BLOCK        
             1037  JUMP_FORWARD       1094  'to 1094'
           1040_0  COME_FROM_EXCEPT   1011  '1011'

 L. 155      1040  POP_TOP          
             1041  POP_TOP          
             1042  POP_TOP          

 L. 156      1043  LOAD_GLOBAL              print
             1046  LOAD_STR                 "%s: error decompiling '%s'"

 L. 157      1049  LOAD_GLOBAL              __title__
             1052  LOAD_FAST                'mainpyfile'
             1055  BUILD_TUPLE_2         2 
             1058  BINARY_MODULO    
             1059  LOAD_STR                 'file'
             1062  LOAD_GLOBAL              sys
             1065  LOAD_ATTR                stderr
             1068  CALL_FUNCTION_257   257  '1 positional, 1 named'
             1071  POP_TOP          

 L. 158      1072  LOAD_GLOBAL              sys
             1075  LOAD_ATTR                exit
             1078  LOAD_CONST               1
             1081  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1084  POP_TOP          

 L. 159      1085  LOAD_CONST               None
             1088  RETURN_VALUE     
             1089  POP_EXCEPT       
             1090  JUMP_FORWARD       1094  'to 1094'
             1093  END_FINALLY      
           1094_0  COME_FROM          1090  '1090'
           1094_1  COME_FROM          1037  '1037'

 L. 166      1094  LOAD_FAST                'fd'
             1097  LOAD_ATTR                name
             1100  STORE_FAST               'mainpyfile'

 L. 167      1103  LOAD_FAST                'fd'
             1106  LOAD_ATTR                close
             1109  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1112  POP_TOP          

 L. 175      1113  LOAD_GLOBAL              print
             1116  LOAD_STR                 "%s: couldn't find Python source so we recreated it at '%s'"

 L. 176      1119  LOAD_GLOBAL              __title__
             1122  LOAD_FAST                'mainpyfile'
             1125  BUILD_TUPLE_2         2 
             1128  BINARY_MODULO    
             1129  LOAD_STR                 'file'
             1132  LOAD_GLOBAL              sys
             1135  LOAD_ATTR                stderr
             1138  CALL_FUNCTION_257   257  '1 positional, 1 named'
             1141  POP_TOP          

 L. 178      1142  POP_EXCEPT       
             1143  JUMP_ABSOLUTE      1150  'to 1150'
             1146  END_FINALLY      
             1147  JUMP_FORWARD       1150  'to 1150'
           1150_0  COME_FROM          1147  '1147'

 L. 182      1150  LOAD_GLOBAL              pyficache
             1153  LOAD_ATTR                pyc2py
             1156  LOAD_FAST                'mainpyfile'
             1159  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1162  STORE_FAST               'mainpyfile_noopt'

 L. 183      1165  LOAD_FAST                'mainpyfile'
             1168  LOAD_FAST                'mainpyfile_noopt'
             1171  COMPARE_OP               !=
             1174  POP_JUMP_IF_FALSE  1235  'to 1235'

 L. 184      1177  LOAD_GLOBAL              Mfile
             1180  LOAD_ATTR                readable
             1183  LOAD_FAST                'mainpyfile_noopt'
             1186  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1189  POP_JUMP_IF_FALSE  1235  'to 1235'

 L. 185      1192  LOAD_GLOBAL              print
             1195  LOAD_STR                 "%s: Compiled Python script given and we can't use that."

 L. 186      1198  LOAD_GLOBAL              __title__
             1201  BINARY_MODULO    
             1202  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1205  POP_TOP          

 L. 187      1206  LOAD_GLOBAL              print
             1209  LOAD_STR                 '%s: Substituting non-compiled name: %s'

 L. 188      1212  LOAD_GLOBAL              __title__
             1215  LOAD_FAST                'mainpyfile_noopt'
             1218  BUILD_TUPLE_2         2 
             1221  BINARY_MODULO    
             1222  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1225  POP_TOP          

 L. 189      1226  LOAD_FAST                'mainpyfile_noopt'
             1229  STORE_FAST               'mainpyfile'
           1232_0  COME_FROM          1189  '1189'

 L. 190      1232  JUMP_FORWARD       1235  'to 1235'
           1235_0  COME_FROM          1232  '1232'

 L. 194      1235  LOAD_GLOBAL              osp
             1238  LOAD_ATTR                dirname
             1241  LOAD_FAST                'mainpyfile'
             1244  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1247  DUP_TOP          
             1248  LOAD_GLOBAL              sys
             1251  LOAD_ATTR                path
             1254  LOAD_CONST               0
             1257  STORE_SUBSCR     
             1258  LOAD_FAST                'dbg'
             1261  STORE_ATTR               main_dirname
           1264_0  COME_FROM           343  '343'

 L. 198      1264  LOAD_CONST               False
             1267  LOAD_FAST                'dbg'
             1270  STORE_ATTR               sig_received

 L. 205      1273  SETUP_LOOP         1600  'to 1600'

 L. 210      1276  SETUP_EXCEPT       1402  'to 1402'

 L. 211      1279  LOAD_FAST                'dbg'
             1282  LOAD_ATTR                program_sys_argv
             1285  POP_JUMP_IF_FALSE  1322  'to 1322'
             1288  LOAD_FAST                'mainpyfile'
           1291_0  COME_FROM          1285  '1285'
             1291  POP_JUMP_IF_FALSE  1322  'to 1322'

 L. 212      1294  LOAD_FAST                'dbg'
             1297  LOAD_ATTR                run_script
             1300  LOAD_FAST                'mainpyfile'
             1303  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1306  STORE_FAST               'normal_termination'

 L. 213      1309  LOAD_FAST                'normal_termination'
             1312  POP_JUMP_IF_TRUE   1350  'to 1350'

 L. 213      1315  BREAK_LOOP       
             1316  JUMP_ABSOLUTE      1350  'to 1350'
             1319  JUMP_FORWARD       1350  'to 1350'
             1322  ELSE                     '1350'

 L. 215      1322  LOAD_STR                 'No program'
             1325  LOAD_FAST                'dbg'
             1328  LOAD_ATTR                core
             1331  STORE_ATTR               execution_status

 L. 216      1334  LOAD_FAST                'dbg'
             1337  LOAD_ATTR                core
             1340  LOAD_ATTR                processor
             1343  LOAD_ATTR                process_commands
             1346  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1349  POP_TOP          
           1350_0  COME_FROM          1319  '1319'

 L. 219      1350  LOAD_STR                 'Terminated'
             1353  LOAD_FAST                'dbg'
             1356  LOAD_ATTR                core
             1359  STORE_ATTR               execution_status

 L. 220      1362  LOAD_FAST                'dbg'
             1365  LOAD_ATTR                intf
             1368  LOAD_CONST               -1
             1371  BINARY_SUBSCR    
             1372  LOAD_ATTR                msg
             1375  LOAD_STR                 'The program finished - quit or restart'
             1378  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1381  POP_TOP          

 L. 221      1382  LOAD_FAST                'dbg'
             1385  LOAD_ATTR                core
             1388  LOAD_ATTR                processor
             1391  LOAD_ATTR                process_commands
             1394  CALL_FUNCTION_0       0  '0 positional, 0 named'
             1397  POP_TOP          
             1398  POP_BLOCK        
             1399  JUMP_BACK          1276  'to 1276'
           1402_0  COME_FROM_EXCEPT   1276  '1276'

 L. 222      1402  DUP_TOP          
             1403  LOAD_GLOBAL              Mexcept
             1406  LOAD_ATTR                DebuggerQuit
             1409  COMPARE_OP               exception-match
             1412  POP_JUMP_IF_FALSE  1423  'to 1423'
             1415  POP_TOP          
             1416  POP_TOP          
             1417  POP_TOP          

 L. 223      1418  BREAK_LOOP       
             1419  POP_EXCEPT       
             1420  JUMP_BACK          1276  'to 1276'

 L. 224      1423  DUP_TOP          
             1424  LOAD_GLOBAL              Mexcept
             1427  LOAD_ATTR                DebuggerRestart
             1430  COMPARE_OP               exception-match
             1433  POP_JUMP_IF_FALSE  1578  'to 1578'
             1436  POP_TOP          
             1437  POP_TOP          
             1438  POP_TOP          

 L. 225      1439  LOAD_STR                 'Restart requested'
             1442  LOAD_FAST                'dbg'
             1445  LOAD_ATTR                core
             1448  STORE_ATTR               execution_status

 L. 226      1451  LOAD_FAST                'dbg'
             1454  LOAD_ATTR                program_sys_argv
             1457  POP_JUMP_IF_FALSE  1573  'to 1573'

 L. 227      1460  LOAD_GLOBAL              list
             1463  LOAD_FAST                'dbg'
             1466  LOAD_ATTR                program_sys_argv
             1469  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1472  LOAD_GLOBAL              sys
             1475  STORE_ATTR               argv

 L. 228      1478  LOAD_STR                 'Restarting %s with arguments:'

 L. 229      1481  LOAD_FAST                'dbg'
             1484  LOAD_ATTR                core
             1487  LOAD_ATTR                filename
             1490  LOAD_FAST                'mainpyfile'
             1493  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1496  BINARY_MODULO    
             1497  STORE_FAST               'part1'

 L. 230      1500  LOAD_STR                 ' '
             1503  LOAD_ATTR                join
             1506  LOAD_FAST                'dbg'
             1509  LOAD_ATTR                program_sys_argv
             1512  LOAD_CONST               1
             1515  LOAD_CONST               None
             1518  BUILD_SLICE_2         2 
             1521  BINARY_SUBSCR    
             1522  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1525  STORE_FAST               'args'

 L. 231      1528  LOAD_FAST                'dbg'
             1531  LOAD_ATTR                intf
             1534  LOAD_CONST               -1
             1537  BINARY_SUBSCR    
             1538  LOAD_ATTR                msg

 L. 232      1541  LOAD_GLOBAL              Mmisc
             1544  LOAD_ATTR                wrapped_lines
             1547  LOAD_FAST                'part1'
             1550  LOAD_FAST                'args'

 L. 233      1553  LOAD_FAST                'dbg'
             1556  LOAD_ATTR                settings
             1559  LOAD_STR                 'width'
             1562  BINARY_SUBSCR    
             1563  CALL_FUNCTION_3       3  '3 positional, 0 named'
             1566  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1569  POP_TOP          
             1570  JUMP_FORWARD       1574  'to 1574'
             1573  ELSE                     '1574'

 L. 234      1573  BREAK_LOOP       
           1574_0  COME_FROM          1570  '1570'
             1574  POP_EXCEPT       
             1575  JUMP_BACK          1276  'to 1276'

 L. 235      1578  DUP_TOP          
             1579  LOAD_GLOBAL              SystemExit
             1582  COMPARE_OP               exception-match
             1585  POP_JUMP_IF_FALSE  1596  'to 1596'
             1588  POP_TOP          
             1589  POP_TOP          
             1590  POP_TOP          

 L. 237      1591  BREAK_LOOP       
             1592  POP_EXCEPT       
             1593  JUMP_BACK          1276  'to 1276'
             1596  END_FINALLY      

 L. 238      1597  CONTINUE           1276  'to 1276'
           1600_0  COME_FROM_LOOP     1273  '1273'

 L. 241      1600  LOAD_FAST                'orig_sys_argv'
             1603  LOAD_GLOBAL              sys
             1606  STORE_ATTR               argv

 L. 242      1609  LOAD_CONST               None
             1612  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 1600


if __name__ == '__main__':
    main()
# global __title__ ## Warning: Unused global