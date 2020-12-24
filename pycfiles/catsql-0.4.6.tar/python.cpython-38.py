# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/python.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4956 bytes
import os, ast, sys, time, uuid, fcntl, shutil, hashlib, logging, tempfile, resource, subprocess
LOGGER = logging.getLogger('cs')
_resource_mapper = {'CPUTIME':(
  resource.RLIMIT_CPU, lambda x: (x, x + 1)), 
 'MEMORY':(
  resource.RLIMIT_AS, lambda x: (x, x)), 
 'FILESIZE':(
  resource.RLIMIT_FSIZE, lambda x: (x, x))}

def run_code--- This code section failed: ---

 L.  47         0  LOAD_FAST                'options'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'do_rlimits'
                6  LOAD_CONST               True
                8  CALL_METHOD_2         2  ''
               10  POP_JUMP_IF_FALSE    96  'to 96'

 L.  48        12  LOAD_GLOBAL              resource
               14  LOAD_ATTR                RLIMIT_NPROC
               16  LOAD_CONST               (0, 0)
               18  BUILD_TUPLE_2         2 
               20  BUILD_LIST_1          1 
               22  STORE_DEREF              'rlimits'

 L.  49        24  LOAD_GLOBAL              _resource_mapper
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''
               30  GET_ITER         
               32  FOR_ITER             94  'to 94'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'key'
               38  STORE_FAST               'val'

 L.  50        40  LOAD_FAST                'key'
               42  LOAD_STR                 'MEMORY'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    62  'to 62'
               48  LOAD_FAST                'options'
               50  LOAD_FAST                'key'
               52  BINARY_SUBSCR    
               54  LOAD_CONST               0
               56  COMPARE_OP               <=
               58  POP_JUMP_IF_FALSE    62  'to 62'

 L.  51        60  JUMP_BACK            32  'to 32'
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            46  '46'

 L.  52        62  LOAD_DEREF               'rlimits'
               64  LOAD_METHOD              append
               66  LOAD_FAST                'val'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'val'
               74  LOAD_CONST               1
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'options'
               80  LOAD_FAST                'key'
               82  BINARY_SUBSCR    
               84  CALL_FUNCTION_1       1  ''
               86  BUILD_TUPLE_2         2 
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_BACK            32  'to 32'
               94  JUMP_FORWARD        100  'to 100'
             96_0  COME_FROM            10  '10'

 L.  54        96  BUILD_LIST_0          0 
               98  STORE_DEREF              'rlimits'
            100_0  COME_FROM            94  '94'

 L.  56       100  LOAD_CLOSURE             'context'
              102  LOAD_CLOSURE             'rlimits'
              104  BUILD_TUPLE_2         2 
              106  LOAD_CODE                <code_object limiter>
              108  LOAD_STR                 'run_code.<locals>.limiter'
              110  MAKE_FUNCTION_8          'closure'
              112  STORE_FAST               'limiter'

 L.  62       114  LOAD_DEREF               'context'
              116  LOAD_METHOD              get
              118  LOAD_STR                 'csq_sandbox_dir'
              120  LOAD_STR                 '/tmp/sandbox'
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'tmpdir'

 L.  63       126  LOAD_STR                 '_%s'
              128  LOAD_GLOBAL              uuid
              130  LOAD_METHOD              uuid4
              132  CALL_METHOD_0         0  ''
              134  LOAD_ATTR                hex
              136  BINARY_MODULO    
              138  STORE_FAST               'this_one'

 L.  64       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              join
              146  LOAD_FAST                'tmpdir'
              148  LOAD_FAST                'this_one'
              150  CALL_METHOD_2         2  ''
              152  STORE_FAST               'tmpdir'

 L.  65       154  LOAD_GLOBAL              open

 L.  66       156  LOAD_GLOBAL              os
              158  LOAD_ATTR                path
              160  LOAD_METHOD              join

 L.  67       162  LOAD_DEREF               'context'
              164  LOAD_STR                 'cs_fs_root'
              166  BINARY_SUBSCR    

 L.  68       168  LOAD_STR                 '__QTYPES__'

 L.  69       170  LOAD_STR                 'pythoncode'

 L.  70       172  LOAD_STR                 '__SANDBOXES__'

 L.  71       174  LOAD_STR                 '_template.py'

 L.  66       176  CALL_METHOD_5         5  ''

 L.  65       178  CALL_FUNCTION_1       1  ''
              180  SETUP_WITH          196  'to 196'

 L.  73       182  STORE_FAST               'f'

 L.  74       184  LOAD_FAST                'f'
              186  LOAD_METHOD              read
              188  CALL_METHOD_0         0  ''
              190  STORE_FAST               'template'
              192  POP_BLOCK        
              194  BEGIN_FINALLY    
            196_0  COME_FROM_WITH      180  '180'
              196  WITH_CLEANUP_START
              198  WITH_CLEANUP_FINISH
              200  END_FINALLY      

 L.  75       202  LOAD_FAST                'template'

 L.  76       204  LOAD_FAST                'count_opcodes'

 L.  77       206  LOAD_FAST                'result_as_string'

 L.  78       208  LOAD_FAST                'this_one'

 L.  79       210  LOAD_FAST                'opcode_limit'
              212  JUMP_IF_TRUE_OR_POP   220  'to 220'
              214  LOAD_GLOBAL              float
              216  LOAD_STR                 'inf'
              218  CALL_FUNCTION_1       1  ''
            220_0  COME_FROM           212  '212'

 L.  75       220  LOAD_CONST               ('enable_opcode_count', 'result_as_string', 'test_module', 'opcode_limit')
              222  BUILD_CONST_KEY_MAP_4     4 
              224  INPLACE_MODULO   
              226  STORE_FAST               'template'

 L.  81       228  LOAD_GLOBAL              os
              230  LOAD_METHOD              makedirs
              232  LOAD_FAST                'tmpdir'
              234  LOAD_CONST               511
              236  CALL_METHOD_2         2  ''
              238  POP_TOP          

 L.  82       240  LOAD_GLOBAL              open
              242  LOAD_GLOBAL              os
              244  LOAD_ATTR                path
              246  LOAD_METHOD              join
              248  LOAD_FAST                'tmpdir'
              250  LOAD_STR                 'run_catsoop_test.py'
              252  CALL_METHOD_2         2  ''
              254  LOAD_STR                 'w'
              256  CALL_FUNCTION_2       2  ''
              258  SETUP_WITH          276  'to 276'
              260  STORE_FAST               'f'

 L.  83       262  LOAD_FAST                'f'
              264  LOAD_METHOD              write
              266  LOAD_FAST                'template'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
              272  POP_BLOCK        
              274  BEGIN_FINALLY    
            276_0  COME_FROM_WITH      258  '258'
              276  WITH_CLEANUP_START
              278  WITH_CLEANUP_FINISH
              280  END_FINALLY      

 L.  84       282  LOAD_FAST                'options'
              284  LOAD_STR                 'FILES'
              286  BINARY_SUBSCR    
              288  GET_ITER         
            290_0  COME_FROM           358  '358'
              290  FOR_ITER            416  'to 416'
              292  STORE_FAST               'f'

 L.  85       294  LOAD_FAST                'f'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  LOAD_METHOD              strip
              302  CALL_METHOD_0         0  ''
              304  LOAD_METHOD              lower
              306  CALL_METHOD_0         0  ''
              308  STORE_FAST               'typ'

 L.  86       310  LOAD_FAST                'typ'
              312  LOAD_STR                 'copy'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   352  'to 352'

 L.  87       320  LOAD_GLOBAL              shutil
              322  LOAD_METHOD              copyfile
              324  LOAD_FAST                'f'
              326  LOAD_CONST               1
              328  BINARY_SUBSCR    
              330  LOAD_GLOBAL              os
              332  LOAD_ATTR                path
              334  LOAD_METHOD              join
              336  LOAD_FAST                'tmpdir'
              338  LOAD_FAST                'f'
              340  LOAD_CONST               2
              342  BINARY_SUBSCR    
              344  CALL_METHOD_2         2  ''
              346  CALL_METHOD_2         2  ''
              348  POP_TOP          
              350  JUMP_BACK           290  'to 290'
            352_0  COME_FROM           316  '316'

 L.  88       352  LOAD_FAST                'typ'
              354  LOAD_STR                 'string'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   290  'to 290'

 L.  89       362  LOAD_GLOBAL              open
              364  LOAD_GLOBAL              os
              366  LOAD_ATTR                path
              368  LOAD_METHOD              join
              370  LOAD_FAST                'tmpdir'
              372  LOAD_FAST                'f'
              374  LOAD_CONST               1
              376  BINARY_SUBSCR    
              378  CALL_METHOD_2         2  ''
              380  LOAD_STR                 'w'
              382  CALL_FUNCTION_2       2  ''
              384  SETUP_WITH          406  'to 406'
              386  STORE_FAST               'fileobj'

 L.  90       388  LOAD_FAST                'fileobj'
              390  LOAD_METHOD              write
              392  LOAD_FAST                'f'
              394  LOAD_CONST               2
              396  BINARY_SUBSCR    
              398  CALL_METHOD_1         1  ''
              400  POP_TOP          
              402  POP_BLOCK        
              404  BEGIN_FINALLY    
            406_0  COME_FROM_WITH      384  '384'
              406  WITH_CLEANUP_START
              408  WITH_CLEANUP_FINISH
              410  END_FINALLY      
          412_414  JUMP_BACK           290  'to 290'

 L.  91       416  LOAD_STR                 '%s.py'
              418  LOAD_FAST                'this_one'
              420  BINARY_MODULO    
              422  STORE_FAST               'fname'

 L.  92       424  LOAD_GLOBAL              open
              426  LOAD_GLOBAL              os
              428  LOAD_ATTR                path
              430  LOAD_METHOD              join
              432  LOAD_FAST                'tmpdir'
              434  LOAD_FAST                'fname'
              436  CALL_METHOD_2         2  ''
              438  LOAD_STR                 'w'
              440  CALL_FUNCTION_2       2  ''
              442  SETUP_WITH          468  'to 468'
              444  STORE_FAST               'fileobj'

 L.  93       446  LOAD_FAST                'fileobj'
              448  LOAD_METHOD              write
              450  LOAD_FAST                'code'
              452  LOAD_METHOD              replace
              454  LOAD_STR                 '\r\n'
              456  LOAD_STR                 '\n'
              458  CALL_METHOD_2         2  ''
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
              464  POP_BLOCK        
              466  BEGIN_FINALLY    
            468_0  COME_FROM_WITH      442  '442'
              468  WITH_CLEANUP_START
              470  WITH_CLEANUP_FINISH
              472  END_FINALLY      

 L.  95       474  LOAD_GLOBAL              LOGGER
              476  LOAD_METHOD              debug

 L.  96       478  LOAD_STR                 '[pythoncode.sandbox.python] context cs_version=%s, cs_python_interpreter=%s'

 L.  97       480  LOAD_DEREF               'context'
              482  LOAD_METHOD              get
              484  LOAD_STR                 'cs_version'
              486  CALL_METHOD_1         1  ''
              488  LOAD_DEREF               'context'
              490  LOAD_METHOD              get
              492  LOAD_STR                 'cs_python_interpreter'
              494  CALL_METHOD_1         1  ''
              496  BUILD_TUPLE_2         2 

 L.  96       498  BINARY_MODULO    

 L.  95       500  CALL_METHOD_1         1  ''
              502  POP_TOP          

 L. 100       504  LOAD_DEREF               'context'
              506  LOAD_METHOD              get

 L. 101       508  LOAD_STR                 'csq_python_interpreter'

 L. 101       510  LOAD_DEREF               'context'
              512  LOAD_METHOD              get
              514  LOAD_STR                 'cs_python_interpreter'
              516  LOAD_STR                 'python3'
              518  CALL_METHOD_2         2  ''

 L. 100       520  CALL_METHOD_2         2  ''
              522  STORE_FAST               'interp'

 L. 104       524  SETUP_FINALLY       568  'to 568'

 L. 105       526  LOAD_GLOBAL              subprocess
              528  LOAD_ATTR                Popen

 L. 106       530  LOAD_FAST                'interp'
              532  LOAD_STR                 '-E'
              534  LOAD_STR                 '-B'
              536  LOAD_STR                 'run_catsoop_test.py'
              538  BUILD_LIST_4          4 

 L. 107       540  LOAD_FAST                'tmpdir'

 L. 108       542  LOAD_FAST                'limiter'

 L. 109       544  LOAD_CONST               0

 L. 110       546  LOAD_GLOBAL              subprocess
              548  LOAD_ATTR                PIPE

 L. 111       550  LOAD_GLOBAL              subprocess
              552  LOAD_ATTR                PIPE

 L. 112       554  LOAD_GLOBAL              subprocess
              556  LOAD_ATTR                PIPE

 L. 105       558  LOAD_CONST               ('cwd', 'preexec_fn', 'bufsize', 'stdin', 'stdout', 'stderr')
              560  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              562  STORE_FAST               'p'
              564  POP_BLOCK        
              566  JUMP_FORWARD        642  'to 642'
            568_0  COME_FROM_FINALLY   524  '524'

 L. 114       568  DUP_TOP          
              570  LOAD_GLOBAL              Exception
              572  COMPARE_OP               exception-match
          574_576  POP_JUMP_IF_FALSE   640  'to 640'
              578  POP_TOP          
              580  STORE_FAST               'err'
              582  POP_TOP          
              584  SETUP_FINALLY       628  'to 628'

 L. 115       586  LOAD_GLOBAL              LOGGER
              588  LOAD_METHOD              error

 L. 116       590  LOAD_STR                 '[pythoncode.sandbox.python] error executing subprocess, interp=%s, fname=%s, tmpdir=%s, preexec_fn=%s'

 L. 117       592  LOAD_FAST                'interp'
              594  LOAD_FAST                'fname'
              596  LOAD_FAST                'tmpdir'
              598  LOAD_FAST                'limiter'
              600  BUILD_TUPLE_4         4 

 L. 116       602  BINARY_MODULO    

 L. 115       604  CALL_METHOD_1         1  ''
              606  POP_TOP          

 L. 119       608  LOAD_GLOBAL              Exception

 L. 120       610  LOAD_STR                 '[cs.qtypes.pythoncode.python] Failed to execute subprocess interp=%s (need to set csq_python_interpreter?), err=%s'

 L. 121       612  LOAD_FAST                'interp'
              614  LOAD_FAST                'err'
              616  BUILD_TUPLE_2         2 

 L. 120       618  BINARY_MODULO    

 L. 119       620  CALL_FUNCTION_1       1  ''
              622  RAISE_VARARGS_1       1  ''
              624  POP_BLOCK        
              626  BEGIN_FINALLY    
            628_0  COME_FROM_FINALLY   584  '584'
              628  LOAD_CONST               None
              630  STORE_FAST               'err'
              632  DELETE_FAST              'err'
              634  END_FINALLY      
              636  POP_EXCEPT       
              638  JUMP_FORWARD        642  'to 642'
            640_0  COME_FROM           574  '574'
              640  END_FINALLY      
            642_0  COME_FROM           638  '638'
            642_1  COME_FROM           566  '566'

 L. 124       642  LOAD_STR                 ''
              644  STORE_FAST               'out'

 L. 125       646  LOAD_STR                 ''
              648  STORE_FAST               'err'

 L. 126       650  SETUP_FINALLY       688  'to 688'

 L. 127       652  LOAD_FAST                'p'
              654  LOAD_ATTR                communicate
              656  LOAD_FAST                'options'
              658  LOAD_STR                 'STDIN'
              660  BINARY_SUBSCR    
          662_664  JUMP_IF_TRUE_OR_POP   668  'to 668'
              666  LOAD_STR                 ''
            668_0  COME_FROM           662  '662'
              668  LOAD_FAST                'options'
              670  LOAD_STR                 'CLOCKTIME'
              672  BINARY_SUBSCR    
              674  LOAD_CONST               ('timeout',)
              676  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              678  UNPACK_SEQUENCE_2     2 
              680  STORE_FAST               'out'
              682  STORE_FAST               'err'
              684  POP_BLOCK        
              686  JUMP_FORWARD        740  'to 740'
            688_0  COME_FROM_FINALLY   650  '650'

 L. 128       688  DUP_TOP          
              690  LOAD_GLOBAL              subprocess
              692  LOAD_ATTR                TimeoutExpired
              694  COMPARE_OP               exception-match
          696_698  POP_JUMP_IF_FALSE   738  'to 738'
              700  POP_TOP          
              702  POP_TOP          
              704  POP_TOP          

 L. 129       706  LOAD_FAST                'p'
              708  LOAD_METHOD              kill
              710  CALL_METHOD_0         0  ''
              712  POP_TOP          

 L. 130       714  LOAD_FAST                'p'
              716  LOAD_METHOD              wait
              718  CALL_METHOD_0         0  ''
              720  POP_TOP          

 L. 131       722  LOAD_FAST                'p'
              724  LOAD_METHOD              communicate
              726  CALL_METHOD_0         0  ''
              728  UNPACK_SEQUENCE_2     2 
              730  STORE_FAST               'out'
              732  STORE_FAST               'err'
              734  POP_EXCEPT       
              736  JUMP_FORWARD        740  'to 740'
            738_0  COME_FROM           696  '696'
              738  END_FINALLY      
            740_0  COME_FROM           736  '736'
            740_1  COME_FROM           686  '686'

 L. 132       740  LOAD_FAST                'out'
              742  LOAD_METHOD              decode
              744  CALL_METHOD_0         0  ''
              746  STORE_FAST               'out'

 L. 133       748  LOAD_FAST                'err'
              750  LOAD_METHOD              decode
              752  CALL_METHOD_0         0  ''
              754  STORE_FAST               'err'

 L. 135       756  LOAD_GLOBAL              shutil
              758  LOAD_METHOD              rmtree
              760  LOAD_FAST                'tmpdir'
              762  LOAD_CONST               True
              764  CALL_METHOD_2         2  ''
              766  POP_TOP          

 L. 137       768  LOAD_FAST                'out'
              770  LOAD_METHOD              rsplit
              772  LOAD_STR                 '---'
              774  LOAD_CONST               1
              776  CALL_METHOD_2         2  ''
              778  STORE_FAST               'n'

 L. 138       780  BUILD_MAP_0           0 
              782  STORE_FAST               'log'

 L. 139       784  LOAD_GLOBAL              len
              786  LOAD_FAST                'n'
              788  CALL_FUNCTION_1       1  ''
              790  LOAD_CONST               2
              792  COMPARE_OP               ==
          794_796  POP_JUMP_IF_FALSE   842  'to 842'

 L. 140       798  LOAD_FAST                'n'
              800  UNPACK_SEQUENCE_2     2 
              802  STORE_FAST               'out'
              804  STORE_FAST               'log'

 L. 141       806  SETUP_FINALLY       826  'to 826'

 L. 142       808  LOAD_DEREF               'context'
              810  LOAD_STR                 'csm_util'
              812  BINARY_SUBSCR    
              814  LOAD_METHOD              literal_eval
              816  LOAD_FAST                'log'
              818  CALL_METHOD_1         1  ''
              820  STORE_FAST               'log'
              822  POP_BLOCK        
              824  JUMP_FORWARD        842  'to 842'
            826_0  COME_FROM_FINALLY   806  '806'

 L. 143       826  POP_TOP          
              828  POP_TOP          
              830  POP_TOP          

 L. 144       832  BUILD_MAP_0           0 
              834  STORE_FAST               'log'
              836  POP_EXCEPT       
              838  JUMP_FORWARD        842  'to 842'
              840  END_FINALLY      
            842_0  COME_FROM           838  '838'
            842_1  COME_FROM           824  '824'
            842_2  COME_FROM           794  '794'

 L. 146       842  LOAD_FAST                'log'
              844  BUILD_MAP_0           0 
              846  COMPARE_OP               ==
          848_850  POP_JUMP_IF_TRUE    866  'to 866'
              852  LOAD_FAST                'log'
              854  LOAD_METHOD              get
              856  LOAD_STR                 'opcode_limit_reached'
              858  LOAD_CONST               False
              860  CALL_METHOD_2         2  ''
          862_864  POP_JUMP_IF_FALSE   884  'to 884'
            866_0  COME_FROM           848  '848'

 L. 147       866  LOAD_FAST                'err'
              868  LOAD_METHOD              strip
              870  CALL_METHOD_0         0  ''
              872  LOAD_STR                 ''
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_FALSE   884  'to 884'

 L. 149       880  LOAD_STR                 'Your code did not run to completion, but no error message was returned.\nThis normally means that your code contains an infinite loop or otherwise took too long to run.'

 L. 148       882  STORE_FAST               'err'
            884_0  COME_FROM           876  '876'
            884_1  COME_FROM           862  '862'

 L. 155       884  LOAD_GLOBAL              len
              886  LOAD_FAST                'n'
              888  CALL_FUNCTION_1       1  ''
              890  LOAD_CONST               2
              892  COMPARE_OP               >
          894_896  POP_JUMP_IF_FALSE   910  'to 910'

 L. 156       898  LOAD_STR                 ''
              900  STORE_FAST               'out'

 L. 157       902  BUILD_MAP_0           0 
              904  STORE_FAST               'log'

 L. 158       906  LOAD_STR                 'BAD CODE - this will be logged'
              908  STORE_FAST               'err'
            910_0  COME_FROM           894  '894'

 L. 160       910  LOAD_FAST                'fname'
              912  LOAD_FAST                'out'
              914  LOAD_FAST                'err'
              916  LOAD_FAST                'log'
              918  LOAD_CONST               ('fname', 'out', 'err', 'info')
              920  BUILD_CONST_KEY_MAP_4     4 
              922  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 194