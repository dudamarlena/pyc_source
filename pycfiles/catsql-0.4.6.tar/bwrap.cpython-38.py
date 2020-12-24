# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythoncode/__SANDBOXES__/bwrap.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 4672 bytes
import os, sys, time, uuid, fcntl, shutil, tempfile, resource, subprocess
default_ro_bind = [
 ('/usr', '/usr'),
 ('/lib', '/lib'),
 ('/lib64', '/lib64'),
 ('/bin', '/bin'),
 ('/sbin', '/sbin')]

def run_code--- This code section failed: ---

 L.  44         0  LOAD_CLOSURE             'context'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object limiter>
                6  LOAD_STR                 'run_code.<locals>.limiter'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'limiter'

 L.  48        12  LOAD_DEREF               'context'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'csq_sandbox_dir'
               18  LOAD_STR                 '/tmp/sandbox'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'tmpdir'

 L.  49        24  LOAD_STR                 '_%s'
               26  LOAD_GLOBAL              uuid
               28  LOAD_METHOD              uuid4
               30  CALL_METHOD_0         0  ''
               32  LOAD_ATTR                hex
               34  BINARY_MODULO    
               36  STORE_FAST               'this_one'

 L.  50        38  LOAD_GLOBAL              os
               40  LOAD_ATTR                path
               42  LOAD_METHOD              join
               44  LOAD_FAST                'tmpdir'
               46  LOAD_FAST                'this_one'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'tmpdir'

 L.  51        52  LOAD_GLOBAL              open

 L.  52        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              join

 L.  53        60  LOAD_DEREF               'context'
               62  LOAD_STR                 'cs_fs_root'
               64  BINARY_SUBSCR    

 L.  54        66  LOAD_STR                 '__QTYPES__'

 L.  55        68  LOAD_STR                 'pythoncode'

 L.  56        70  LOAD_STR                 '__SANDBOXES__'

 L.  57        72  LOAD_STR                 '_template.py'

 L.  52        74  CALL_METHOD_5         5  ''

 L.  51        76  CALL_FUNCTION_1       1  ''
               78  SETUP_WITH           94  'to 94'

 L.  59        80  STORE_FAST               'f'

 L.  60        82  LOAD_FAST                'f'
               84  LOAD_METHOD              read
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'template'
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_WITH       78  '78'
               94  WITH_CLEANUP_START
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

 L.  61       100  LOAD_FAST                'template'

 L.  62       102  LOAD_FAST                'count_opcodes'

 L.  63       104  LOAD_FAST                'result_as_string'

 L.  64       106  LOAD_FAST                'this_one'

 L.  65       108  LOAD_FAST                'opcode_limit'
              110  JUMP_IF_TRUE_OR_POP   118  'to 118'
              112  LOAD_GLOBAL              float
              114  LOAD_STR                 'inf'
              116  CALL_FUNCTION_1       1  ''
            118_0  COME_FROM           110  '110'

 L.  61       118  LOAD_CONST               ('enable_opcode_count', 'result_as_string', 'test_module', 'opcode_limit')
              120  BUILD_CONST_KEY_MAP_4     4 
              122  INPLACE_MODULO   
              124  STORE_FAST               'template'

 L.  67       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              makedirs
              130  LOAD_FAST                'tmpdir'
              132  LOAD_CONST               511
              134  CALL_METHOD_2         2  ''
              136  POP_TOP          

 L.  68       138  LOAD_GLOBAL              open
              140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              join
              146  LOAD_FAST                'tmpdir'
              148  LOAD_STR                 'run_catsoop_test.py'
              150  CALL_METHOD_2         2  ''
              152  LOAD_STR                 'w'
              154  CALL_FUNCTION_2       2  ''
              156  SETUP_WITH          174  'to 174'
              158  STORE_FAST               'f'

 L.  69       160  LOAD_FAST                'f'
              162  LOAD_METHOD              write
              164  LOAD_FAST                'template'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  BEGIN_FINALLY    
            174_0  COME_FROM_WITH      156  '156'
              174  WITH_CLEANUP_START
              176  WITH_CLEANUP_FINISH
              178  END_FINALLY      

 L.  70       180  LOAD_FAST                'options'
              182  LOAD_STR                 'FILES'
              184  BINARY_SUBSCR    
              186  GET_ITER         
            188_0  COME_FROM           254  '254'
              188  FOR_ITER            308  'to 308'
              190  STORE_FAST               'f'

 L.  71       192  LOAD_FAST                'f'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_METHOD              strip
              200  CALL_METHOD_0         0  ''
              202  LOAD_METHOD              lower
              204  CALL_METHOD_0         0  ''
              206  STORE_FAST               'typ'

 L.  72       208  LOAD_FAST                'typ'
              210  LOAD_STR                 'copy'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   248  'to 248'

 L.  73       216  LOAD_GLOBAL              shutil
              218  LOAD_METHOD              copyfile
              220  LOAD_FAST                'f'
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    
              226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              join
              232  LOAD_FAST                'tmpdir'
              234  LOAD_FAST                'f'
              236  LOAD_CONST               2
              238  BINARY_SUBSCR    
              240  CALL_METHOD_2         2  ''
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          
              246  JUMP_BACK           188  'to 188'
            248_0  COME_FROM           214  '214'

 L.  74       248  LOAD_FAST                'typ'
              250  LOAD_STR                 'string'
              252  COMPARE_OP               ==
              254  POP_JUMP_IF_FALSE   188  'to 188'

 L.  75       256  LOAD_GLOBAL              open
              258  LOAD_GLOBAL              os
              260  LOAD_ATTR                path
              262  LOAD_METHOD              join
              264  LOAD_FAST                'tmpdir'
              266  LOAD_FAST                'f'
              268  LOAD_CONST               1
              270  BINARY_SUBSCR    
              272  CALL_METHOD_2         2  ''
              274  LOAD_STR                 'w'
              276  CALL_FUNCTION_2       2  ''
              278  SETUP_WITH          300  'to 300'
              280  STORE_FAST               'fileobj'

 L.  76       282  LOAD_FAST                'fileobj'
              284  LOAD_METHOD              write
              286  LOAD_FAST                'f'
              288  LOAD_CONST               2
              290  BINARY_SUBSCR    
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  POP_BLOCK        
              298  BEGIN_FINALLY    
            300_0  COME_FROM_WITH      278  '278'
              300  WITH_CLEANUP_START
              302  WITH_CLEANUP_FINISH
              304  END_FINALLY      
              306  JUMP_BACK           188  'to 188'

 L.  77       308  LOAD_STR                 '%s.py'
              310  LOAD_FAST                'this_one'
              312  BINARY_MODULO    
              314  DUP_TOP          
              316  STORE_FAST               'ofname'
              318  STORE_FAST               'fname'

 L.  78       320  LOAD_GLOBAL              open
              322  LOAD_GLOBAL              os
              324  LOAD_ATTR                path
              326  LOAD_METHOD              join
              328  LOAD_FAST                'tmpdir'
              330  LOAD_FAST                'fname'
              332  CALL_METHOD_2         2  ''
              334  LOAD_STR                 'w'
              336  CALL_FUNCTION_2       2  ''
              338  SETUP_WITH          364  'to 364'
              340  STORE_FAST               'fileobj'

 L.  79       342  LOAD_FAST                'fileobj'
              344  LOAD_METHOD              write
              346  LOAD_FAST                'code'
              348  LOAD_METHOD              replace
              350  LOAD_STR                 '\r\n'
              352  LOAD_STR                 '\n'
              354  CALL_METHOD_2         2  ''
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          
              360  POP_BLOCK        
              362  BEGIN_FINALLY    
            364_0  COME_FROM_WITH      338  '338'
              364  WITH_CLEANUP_START
              366  WITH_CLEANUP_FINISH
              368  END_FINALLY      

 L.  81       370  LOAD_DEREF               'context'
              372  LOAD_METHOD              get

 L.  82       374  LOAD_STR                 'csq_python_interpreter'

 L.  82       376  LOAD_DEREF               'context'
              378  LOAD_METHOD              get
              380  LOAD_STR                 'cs_python_interpreter'
              382  LOAD_STR                 'python3'
              384  CALL_METHOD_2         2  ''

 L.  81       386  CALL_METHOD_2         2  ''
              388  STORE_FAST               'interp'

 L.  85       390  LOAD_STR                 'bwrap'
              392  LOAD_STR                 '--bind'
              394  LOAD_FAST                'tmpdir'
              396  LOAD_STR                 '/run'
              398  BUILD_LIST_4          4 
              400  STORE_FAST               'args'

 L.  86       402  LOAD_DEREF               'context'
              404  LOAD_METHOD              get
              406  LOAD_STR                 'csq_bwrap_arguments'
              408  LOAD_CONST               None
              410  CALL_METHOD_2         2  ''
              412  STORE_FAST               'supplied_args'

 L.  87       414  LOAD_FAST                'supplied_args'
              416  LOAD_CONST               None
              418  COMPARE_OP               is
          420_422  POP_JUMP_IF_FALSE   510  'to 510'

 L.  88       424  LOAD_FAST                'args'
              426  LOAD_METHOD              extend

 L.  90       428  LOAD_STR                 '--unshare-all'

 L.  91       430  LOAD_STR                 '--chdir'

 L.  92       432  LOAD_STR                 '/run'

 L.  93       434  LOAD_STR                 '--hostname'

 L.  94       436  LOAD_STR                 'sandbox-runner'

 L.  95       438  LOAD_STR                 '--die-with-parent'

 L.  89       440  BUILD_LIST_6          6 

 L.  88       442  CALL_METHOD_1         1  ''
              444  POP_TOP          

 L.  98       446  LOAD_GLOBAL              default_ro_bind
              448  LOAD_DEREF               'context'
              450  LOAD_METHOD              get
              452  LOAD_STR                 'csq_bwrap_extra_ro_binds'
              454  BUILD_LIST_0          0 
              456  CALL_METHOD_2         2  ''
              458  BINARY_ADD       
              460  GET_ITER         
              462  FOR_ITER            490  'to 490'
              464  STORE_FAST               'i'

 L.  99       466  LOAD_FAST                'args'
              468  LOAD_METHOD              append
              470  LOAD_STR                 '--ro-bind'
              472  CALL_METHOD_1         1  ''
              474  POP_TOP          

 L. 100       476  LOAD_FAST                'args'
              478  LOAD_METHOD              extend
              480  LOAD_FAST                'i'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
          486_488  JUMP_BACK           462  'to 462'

 L. 101       490  LOAD_FAST                'args'
              492  LOAD_METHOD              extend
              494  LOAD_DEREF               'context'
              496  LOAD_METHOD              get
              498  LOAD_STR                 'csq_bwrap_extra_arguments'
              500  BUILD_LIST_0          0 
              502  CALL_METHOD_2         2  ''
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
              508  JUMP_FORWARD        520  'to 520'
            510_0  COME_FROM           420  '420'

 L. 103       510  LOAD_FAST                'args'
              512  LOAD_METHOD              extend
              514  LOAD_FAST                'supplied_args'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          
            520_0  COME_FROM           508  '508'

 L. 105       520  LOAD_GLOBAL              subprocess
              522  LOAD_ATTR                Popen

 L. 106       524  LOAD_FAST                'args'
              526  LOAD_FAST                'interp'
              528  LOAD_STR                 '-E'
              530  LOAD_STR                 '-B'
              532  LOAD_STR                 'run_catsoop_test.py'
              534  BUILD_LIST_4          4 
              536  BINARY_ADD       

 L. 107       538  LOAD_FAST                'limiter'

 L. 108       540  LOAD_CONST               0

 L. 109       542  LOAD_GLOBAL              subprocess
              544  LOAD_ATTR                PIPE

 L. 110       546  LOAD_GLOBAL              subprocess
              548  LOAD_ATTR                PIPE

 L. 111       550  LOAD_GLOBAL              subprocess
              552  LOAD_ATTR                PIPE

 L. 105       554  LOAD_CONST               ('preexec_fn', 'bufsize', 'stdin', 'stdout', 'stderr')
              556  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              558  STORE_FAST               'p'

 L. 114       560  LOAD_STR                 ''
              562  STORE_FAST               'out'

 L. 115       564  LOAD_STR                 ''
              566  STORE_FAST               'err'

 L. 116       568  SETUP_FINALLY       606  'to 606'

 L. 117       570  LOAD_FAST                'p'
              572  LOAD_ATTR                communicate
              574  LOAD_FAST                'options'
              576  LOAD_STR                 'STDIN'
              578  BINARY_SUBSCR    
          580_582  JUMP_IF_TRUE_OR_POP   586  'to 586'
              584  LOAD_STR                 ''
            586_0  COME_FROM           580  '580'
              586  LOAD_FAST                'options'
              588  LOAD_STR                 'CLOCKTIME'
              590  BINARY_SUBSCR    
              592  LOAD_CONST               ('timeout',)
              594  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              596  UNPACK_SEQUENCE_2     2 
              598  STORE_FAST               'out'
              600  STORE_FAST               'err'
              602  POP_BLOCK        
              604  JUMP_FORWARD        658  'to 658'
            606_0  COME_FROM_FINALLY   568  '568'

 L. 118       606  DUP_TOP          
              608  LOAD_GLOBAL              subprocess
              610  LOAD_ATTR                TimeoutExpired
              612  COMPARE_OP               exception-match
          614_616  POP_JUMP_IF_FALSE   656  'to 656'
              618  POP_TOP          
              620  POP_TOP          
              622  POP_TOP          

 L. 119       624  LOAD_FAST                'p'
              626  LOAD_METHOD              kill
              628  CALL_METHOD_0         0  ''
              630  POP_TOP          

 L. 120       632  LOAD_FAST                'p'
              634  LOAD_METHOD              wait
              636  CALL_METHOD_0         0  ''
              638  POP_TOP          

 L. 121       640  LOAD_FAST                'p'
              642  LOAD_METHOD              communicate
              644  CALL_METHOD_0         0  ''
              646  UNPACK_SEQUENCE_2     2 
              648  STORE_FAST               'out'
              650  STORE_FAST               'err'
              652  POP_EXCEPT       
              654  JUMP_FORWARD        658  'to 658'
            656_0  COME_FROM           614  '614'
              656  END_FINALLY      
            658_0  COME_FROM           654  '654'
            658_1  COME_FROM           604  '604'

 L. 122       658  LOAD_FAST                'out'
              660  LOAD_METHOD              decode
              662  CALL_METHOD_0         0  ''
              664  STORE_FAST               'out'

 L. 123       666  LOAD_FAST                'err'
              668  LOAD_METHOD              decode
              670  CALL_METHOD_0         0  ''
              672  STORE_FAST               'err'

 L. 125       674  BUILD_LIST_0          0 
              676  STORE_FAST               'files'

 L. 126       678  LOAD_GLOBAL              os
              680  LOAD_METHOD              walk
              682  LOAD_FAST                'tmpdir'
              684  CALL_METHOD_1         1  ''
              686  GET_ITER         
              688  FOR_ITER            784  'to 784'
              690  UNPACK_SEQUENCE_3     3 
              692  STORE_FAST               'root'
              694  STORE_FAST               '_'
              696  STORE_FAST               'fs'

 L. 127       698  LOAD_GLOBAL              len
              700  LOAD_FAST                'root'
              702  CALL_FUNCTION_1       1  ''
              704  STORE_FAST               'lr'

 L. 128       706  LOAD_FAST                'fs'
              708  GET_ITER         
              710  FOR_ITER            780  'to 780'
              712  STORE_FAST               'f'

 L. 129       714  LOAD_GLOBAL              os
              716  LOAD_ATTR                path
              718  LOAD_METHOD              join
              720  LOAD_FAST                'root'
              722  LOAD_FAST                'f'
              724  CALL_METHOD_2         2  ''
              726  STORE_FAST               'fname'

 L. 130       728  LOAD_GLOBAL              open
              730  LOAD_FAST                'fname'
              732  LOAD_STR                 'rb'
              734  CALL_FUNCTION_2       2  ''
              736  SETUP_WITH          770  'to 770'
              738  STORE_FAST               'f'

 L. 131       740  LOAD_FAST                'files'
              742  LOAD_METHOD              append
              744  LOAD_FAST                'fname'
              746  LOAD_FAST                'lr'
              748  LOAD_CONST               None
              750  BUILD_SLICE_2         2 
              752  BINARY_SUBSCR    
              754  LOAD_FAST                'f'
              756  LOAD_METHOD              read
              758  CALL_METHOD_0         0  ''
              760  BUILD_TUPLE_2         2 
              762  CALL_METHOD_1         1  ''
              764  POP_TOP          
              766  POP_BLOCK        
              768  BEGIN_FINALLY    
            770_0  COME_FROM_WITH      736  '736'
              770  WITH_CLEANUP_START
              772  WITH_CLEANUP_FINISH
              774  END_FINALLY      
          776_778  JUMP_BACK           710  'to 710'
          780_782  JUMP_BACK           688  'to 688'

 L. 133       784  LOAD_GLOBAL              shutil
              786  LOAD_METHOD              rmtree
              788  LOAD_FAST                'tmpdir'
              790  LOAD_CONST               True
              792  CALL_METHOD_2         2  ''
              794  POP_TOP          

 L. 135       796  LOAD_FAST                'out'
              798  LOAD_METHOD              rsplit
              800  LOAD_STR                 '---'
              802  LOAD_CONST               1
              804  CALL_METHOD_2         2  ''
              806  STORE_FAST               'n'

 L. 136       808  BUILD_MAP_0           0 
              810  STORE_FAST               'log'

 L. 137       812  LOAD_GLOBAL              len
              814  LOAD_FAST                'n'
              816  CALL_FUNCTION_1       1  ''
              818  LOAD_CONST               2
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   870  'to 870'

 L. 138       826  LOAD_FAST                'n'
              828  UNPACK_SEQUENCE_2     2 
              830  STORE_FAST               'out'
              832  STORE_FAST               'log'

 L. 139       834  SETUP_FINALLY       854  'to 854'

 L. 140       836  LOAD_DEREF               'context'
              838  LOAD_STR                 'csm_util'
              840  BINARY_SUBSCR    
              842  LOAD_METHOD              literal_eval
              844  LOAD_FAST                'log'
              846  CALL_METHOD_1         1  ''
              848  STORE_FAST               'log'
              850  POP_BLOCK        
              852  JUMP_FORWARD        870  'to 870'
            854_0  COME_FROM_FINALLY   834  '834'

 L. 141       854  POP_TOP          
              856  POP_TOP          
              858  POP_TOP          

 L. 142       860  BUILD_MAP_0           0 
              862  STORE_FAST               'log'
              864  POP_EXCEPT       
              866  JUMP_FORWARD        870  'to 870'
              868  END_FINALLY      
            870_0  COME_FROM           866  '866'
            870_1  COME_FROM           852  '852'
            870_2  COME_FROM           822  '822'

 L. 144       870  LOAD_FAST                'log'
              872  BUILD_MAP_0           0 
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_TRUE    894  'to 894'
              880  LOAD_FAST                'log'
              882  LOAD_METHOD              get
              884  LOAD_STR                 'opcode_limit_reached'
              886  LOAD_CONST               False
              888  CALL_METHOD_2         2  ''
          890_892  POP_JUMP_IF_FALSE   912  'to 912'
            894_0  COME_FROM           876  '876'

 L. 145       894  LOAD_FAST                'err'
              896  LOAD_METHOD              strip
              898  CALL_METHOD_0         0  ''
              900  LOAD_STR                 ''
              902  COMPARE_OP               ==
          904_906  POP_JUMP_IF_FALSE   912  'to 912'

 L. 147       908  LOAD_STR                 'Your code did not run to completion, but no error message was returned.\nThis normally means that your code contains an infinite loop or otherwise took too long to run.'

 L. 146       910  STORE_FAST               'err'
            912_0  COME_FROM           904  '904'
            912_1  COME_FROM           890  '890'

 L. 153       912  LOAD_GLOBAL              len
              914  LOAD_FAST                'n'
              916  CALL_FUNCTION_1       1  ''
              918  LOAD_CONST               2
              920  COMPARE_OP               >
          922_924  POP_JUMP_IF_FALSE   938  'to 938'

 L. 154       926  LOAD_STR                 ''
              928  STORE_FAST               'out'

 L. 155       930  BUILD_MAP_0           0 
              932  STORE_FAST               'log'

 L. 156       934  LOAD_STR                 'BAD CODE - this will be logged'
              936  STORE_FAST               'err'
            938_0  COME_FROM           922  '922'

 L. 158       938  LOAD_FAST                'fname'
              940  LOAD_FAST                'out'
              942  LOAD_FAST                'err'
              944  LOAD_FAST                'log'
              946  LOAD_CONST               ('fname', 'out', 'err', 'info')
              948  BUILD_CONST_KEY_MAP_4     4 
              950  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 92