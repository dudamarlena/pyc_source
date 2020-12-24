# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/location.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 7953 bytes
import inspect, pyficache
from trepan.lib import stack as Mstack
import os.path as osp
from trepan.processor.parse.semantics import Location
INVALID_LOCATION = None

def resolve_location--- This code section failed: ---

 L.  29         0  LOAD_FAST                'proc'
                3  LOAD_ATTR                curframe
                6  STORE_FAST               'curframe'

 L.  30         9  LOAD_FAST                'location'
               12  LOAD_STR                 '.'
               15  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE   105  'to 105'

 L.  31        21  LOAD_FAST                'curframe'
               24  POP_JUMP_IF_TRUE     44  'to 44'

 L.  32        27  LOAD_FAST                'proc'
               30  LOAD_ATTR                errmsg
               33  LOAD_STR                 "Don't have a stack to get location from"
               36  CALL_FUNCTION_1       1  '1 positional, 0 named'
               39  POP_TOP          

 L.  33        40  LOAD_GLOBAL              INVALID_LOCATION
               43  RETURN_END_IF    

 L.  34        44  LOAD_GLOBAL              Mstack
               47  LOAD_ATTR                frame2file
               50  LOAD_FAST                'proc'
               53  LOAD_ATTR                core
               56  LOAD_FAST                'curframe'
               59  LOAD_STR                 'canonic'
               62  LOAD_CONST               False
               65  CALL_FUNCTION_258   258  '2 positional, 1 named'
               68  STORE_FAST               'filename'

 L.  35        71  LOAD_GLOBAL              inspect
               74  LOAD_ATTR                getlineno
               77  LOAD_FAST                'curframe'
               80  CALL_FUNCTION_1       1  '1 positional, 0 named'
               83  STORE_FAST               'lineno'

 L.  36        86  LOAD_GLOBAL              Location
               89  LOAD_FAST                'filename'
               92  LOAD_FAST                'lineno'
               95  LOAD_CONST               False
               98  LOAD_CONST               None
              101  CALL_FUNCTION_4       4  '4 positional, 0 named'
              104  RETURN_END_IF    

 L.  38       105  LOAD_GLOBAL              isinstance
              108  LOAD_FAST                'location'
              111  LOAD_GLOBAL              Location
              114  CALL_FUNCTION_2       2  '2 positional, 0 named'
              117  POP_JUMP_IF_TRUE    126  'to 126'
              120  LOAD_ASSERT              AssertionError
              123  RAISE_VARARGS_1       1  'exception'
            126_0  COME_FROM           117  '117'

 L.  39       126  LOAD_CONST               False
              129  STORE_FAST               'is_address'

 L.  40       132  LOAD_FAST                'proc'
              135  LOAD_ATTR                curframe
              138  POP_JUMP_IF_FALSE   162  'to 162'

 L.  41       141  LOAD_FAST                'curframe'
              144  LOAD_ATTR                f_globals
              147  STORE_FAST               'g'

 L.  42       150  LOAD_FAST                'curframe'
              153  LOAD_ATTR                f_locals
              156  STORE_FAST               'l'
              159  JUMP_FORWARD        180  'to 180'
              162  ELSE                     '180'

 L.  44       162  LOAD_GLOBAL              globals
              165  CALL_FUNCTION_0       0  '0 positional, 0 named'
              168  STORE_FAST               'g'

 L.  45       171  LOAD_GLOBAL              locals
              174  CALL_FUNCTION_0       0  '0 positional, 0 named'
              177  STORE_FAST               'l'
            180_0  COME_FROM           159  '159'

 L.  47       180  LOAD_FAST                'location'
              183  LOAD_ATTR                method
              186  POP_JUMP_IF_FALSE   386  'to 386'

 L.  49       189  LOAD_CONST               None
              192  DUP_TOP          
              193  STORE_FAST               'filename'
              196  STORE_FAST               'lineno'

 L.  50       199  LOAD_STR                 'Object %s is not known yet as a function, '
              202  LOAD_FAST                'location'
              205  LOAD_ATTR                method
              208  BINARY_MODULO    
              209  STORE_FAST               'msg'

 L.  51       212  SETUP_EXCEPT        240  'to 240'

 L.  52       215  LOAD_GLOBAL              eval
              218  LOAD_FAST                'location'
              221  LOAD_ATTR                method
              224  LOAD_FAST                'g'
              227  LOAD_FAST                'l'
              230  CALL_FUNCTION_3       3  '3 positional, 0 named'
              233  STORE_FAST               'modfunc'
              236  POP_BLOCK        
              237  JUMP_FORWARD        265  'to 265'
            240_0  COME_FROM_EXCEPT    212  '212'

 L.  53       240  POP_TOP          
              241  POP_TOP          
              242  POP_TOP          

 L.  54       243  LOAD_FAST                'proc'
              246  LOAD_ATTR                errmsg
              249  LOAD_FAST                'msg'
              252  CALL_FUNCTION_1       1  '1 positional, 0 named'
              255  POP_TOP          

 L.  55       256  LOAD_GLOBAL              INVALID_LOCATION
              259  RETURN_VALUE     
              260  POP_EXCEPT       
              261  JUMP_FORWARD        265  'to 265'
              264  END_FINALLY      
            265_0  COME_FROM           261  '261'
            265_1  COME_FROM           237  '237'

 L.  57       265  SETUP_EXCEPT        322  'to 322'

 L.  59       268  LOAD_GLOBAL              inspect
              271  LOAD_ATTR                isfunction
              274  LOAD_FAST                'modfunc'
              277  CALL_FUNCTION_1       1  '1 positional, 0 named'
              280  POP_JUMP_IF_TRUE    318  'to 318'
              283  LOAD_GLOBAL              hasattr
              286  LOAD_FAST                'modfunc'
              289  LOAD_STR                 'im_func'
              292  CALL_FUNCTION_2       2  '2 positional, 0 named'
            295_0  COME_FROM           280  '280'
              295  POP_JUMP_IF_FALSE   301  'to 301'

 L.  60       298  JUMP_FORWARD        318  'to 318'
              301  ELSE                     '318'

 L.  62       301  LOAD_FAST                'proc'
              304  LOAD_ATTR                errmsg
              307  LOAD_FAST                'msg'
              310  CALL_FUNCTION_1       1  '1 positional, 0 named'
              313  POP_TOP          

 L.  63       314  LOAD_GLOBAL              INVALID_LOCATION
              317  RETURN_VALUE     
            318_0  COME_FROM           298  '298'
              318  POP_BLOCK        
              319  JUMP_FORWARD        347  'to 347'
            322_0  COME_FROM_EXCEPT    265  '265'

 L.  64       322  POP_TOP          
              323  POP_TOP          
              324  POP_TOP          

 L.  65       325  LOAD_FAST                'proc'
              328  LOAD_ATTR                errmsg
              331  LOAD_FAST                'msg'
              334  CALL_FUNCTION_1       1  '1 positional, 0 named'
              337  POP_TOP          

 L.  66       338  LOAD_GLOBAL              INVALID_LOCATION
              341  RETURN_VALUE     
              342  POP_EXCEPT       
              343  JUMP_FORWARD        347  'to 347'
              346  END_FINALLY      
            347_0  COME_FROM           343  '343'
            347_1  COME_FROM           319  '319'

 L.  67       347  LOAD_FAST                'proc'
              350  LOAD_ATTR                core
              353  LOAD_ATTR                canonic
              356  LOAD_FAST                'modfunc'
              359  LOAD_ATTR                __code__
              362  LOAD_ATTR                co_filename
              365  CALL_FUNCTION_1       1  '1 positional, 0 named'
              368  STORE_FAST               'filename'

 L.  70       371  LOAD_FAST                'modfunc'
              374  LOAD_ATTR                __code__
              377  LOAD_ATTR                co_firstlineno
              380  STORE_FAST               'lineno'
              383  JUMP_FORWARD        802  'to 802'
              386  ELSE                     '802'

 L.  71       386  LOAD_FAST                'location'
              389  LOAD_ATTR                path
              392  POP_JUMP_IF_FALSE   739  'to 739'

 L.  72       395  LOAD_FAST                'proc'
              398  LOAD_ATTR                core
              401  LOAD_ATTR                canonic
              404  LOAD_FAST                'location'
              407  LOAD_ATTR                path
              410  CALL_FUNCTION_1       1  '1 positional, 0 named'
              413  STORE_FAST               'filename'

 L.  73       416  LOAD_FAST                'location'
              419  LOAD_ATTR                line_number
              422  STORE_FAST               'lineno'

 L.  74       425  LOAD_CONST               None
              428  STORE_FAST               'modfunc'

 L.  75       431  LOAD_STR                 '%s is not known as a file'
              434  LOAD_FAST                'location'
              437  LOAD_ATTR                path
              440  BINARY_MODULO    
              441  STORE_FAST               'msg'

 L.  76       444  LOAD_GLOBAL              osp
              447  LOAD_ATTR                isfile
              450  LOAD_FAST                'filename'
              453  CALL_FUNCTION_1       1  '1 positional, 0 named'
              456  POP_JUMP_IF_TRUE    673  'to 673'

 L.  78       459  SETUP_EXCEPT        487  'to 487'

 L.  79       462  LOAD_GLOBAL              eval
              465  LOAD_FAST                'location'
              468  LOAD_ATTR                path
              471  LOAD_FAST                'g'
              474  LOAD_FAST                'l'
              477  CALL_FUNCTION_3       3  '3 positional, 0 named'
              480  STORE_FAST               'modfunc'
              483  POP_BLOCK        
              484  JUMP_FORWARD        525  'to 525'
            487_0  COME_FROM_EXCEPT    459  '459'

 L.  80       487  POP_TOP          
              488  POP_TOP          
              489  POP_TOP          

 L.  81       490  LOAD_STR                 "Don't see '%s' as a existing file or as an module"

 L.  82       493  LOAD_FAST                'location'
              496  LOAD_ATTR                path
              499  BINARY_MODULO    
              500  STORE_FAST               'msg'

 L.  83       503  LOAD_FAST                'proc'
              506  LOAD_ATTR                errmsg
              509  LOAD_FAST                'msg'
              512  CALL_FUNCTION_1       1  '1 positional, 0 named'
              515  POP_TOP          

 L.  84       516  LOAD_GLOBAL              INVALID_LOCATION
              519  RETURN_VALUE     
              520  POP_EXCEPT       
              521  JUMP_FORWARD        525  'to 525'
              524  END_FINALLY      
            525_0  COME_FROM           521  '521'
            525_1  COME_FROM           484  '484'

 L.  86       525  LOAD_FAST                'location'
              528  LOAD_ATTR                is_address
              531  STORE_FAST               'is_address'

 L.  87       534  LOAD_GLOBAL              inspect
              537  LOAD_ATTR                ismodule
              540  LOAD_FAST                'modfunc'
              543  CALL_FUNCTION_1       1  '1 positional, 0 named'
              546  POP_JUMP_IF_FALSE   656  'to 656'

 L.  88       549  LOAD_GLOBAL              hasattr
              552  LOAD_FAST                'modfunc'
              555  LOAD_STR                 '__file__'
              558  CALL_FUNCTION_2       2  '2 positional, 0 named'
              561  POP_JUMP_IF_FALSE   640  'to 640'

 L.  89       564  LOAD_GLOBAL              pyficache
              567  LOAD_ATTR                pyc2py
              570  LOAD_FAST                'modfunc'
              573  LOAD_ATTR                __file__
              576  CALL_FUNCTION_1       1  '1 positional, 0 named'
              579  STORE_FAST               'filename'

 L.  90       582  LOAD_FAST                'proc'
              585  LOAD_ATTR                core
              588  LOAD_ATTR                canonic
              591  LOAD_FAST                'filename'
              594  CALL_FUNCTION_1       1  '1 positional, 0 named'
              597  STORE_FAST               'filename'

 L.  91       600  LOAD_FAST                'lineno'
              603  POP_JUMP_IF_TRUE    621  'to 621'

 L.  93       606  LOAD_CONST               1
              609  STORE_FAST               'lineno'

 L.  94       612  LOAD_CONST               False
              615  STORE_FAST               'is_address'
              618  JUMP_FORWARD        621  'to 621'
            621_0  COME_FROM           618  '618'

 L.  95       621  LOAD_GLOBAL              Location
              624  LOAD_FAST                'filename'
              627  LOAD_FAST                'lineno'
              630  LOAD_FAST                'is_address'
              633  LOAD_FAST                'modfunc'
              636  CALL_FUNCTION_4       4  '4 positional, 0 named'
              639  RETURN_END_IF    

 L.  97       640  LOAD_STR                 "module '%s' doesn't have a file associated with it"

 L.  98       643  LOAD_FAST                'location'
              646  LOAD_ATTR                path
              649  BINARY_MODULO    
              650  STORE_FAST               'msg'
              653  JUMP_FORWARD        656  'to 656'
            656_0  COME_FROM           653  '653'

 L. 100       656  LOAD_FAST                'proc'
              659  LOAD_ATTR                errmsg
              662  LOAD_FAST                'msg'
              665  CALL_FUNCTION_1       1  '1 positional, 0 named'
              668  POP_TOP          

 L. 101       669  LOAD_GLOBAL              INVALID_LOCATION
              672  RETURN_END_IF    

 L. 102       673  LOAD_GLOBAL              pyficache
              676  LOAD_ATTR                maxline
              679  LOAD_FAST                'filename'
              682  CALL_FUNCTION_1       1  '1 positional, 0 named'
              685  STORE_FAST               'maxline'

 L. 103       688  LOAD_FAST                'maxline'
              691  POP_JUMP_IF_FALSE   802  'to 802'
              694  LOAD_FAST                'lineno'
              697  LOAD_FAST                'maxline'
              700  COMPARE_OP               >
            703_0  COME_FROM           691  '691'
              703  POP_JUMP_IF_FALSE   802  'to 802'

 L. 105       706  LOAD_FAST                'proc'
              709  LOAD_ATTR                errmsg
              712  LOAD_STR                 'Line number %d out of range; %s has %d lines.'

 L. 106       715  LOAD_FAST                'lineno'
              718  LOAD_FAST                'filename'
              721  LOAD_FAST                'maxline'
              724  BUILD_TUPLE_3         3 
              727  BINARY_MODULO    
              728  CALL_FUNCTION_1       1  '1 positional, 0 named'
              731  POP_TOP          

 L. 107       732  LOAD_GLOBAL              INVALID_LOCATION
              735  RETURN_END_IF    
              736  JUMP_FORWARD        802  'to 802'
              739  ELSE                     '802'

 L. 108       739  LOAD_FAST                'location'
              742  LOAD_ATTR                line_number
              745  POP_JUMP_IF_FALSE   802  'to 802'

 L. 109       748  LOAD_GLOBAL              Mstack
              751  LOAD_ATTR                frame2file
              754  LOAD_FAST                'proc'
              757  LOAD_ATTR                core
              760  LOAD_FAST                'curframe'
              763  LOAD_STR                 'canonic'
              766  LOAD_CONST               False
              769  CALL_FUNCTION_258   258  '2 positional, 1 named'
              772  STORE_FAST               'filename'

 L. 110       775  LOAD_FAST                'location'
              778  LOAD_ATTR                line_number
              781  STORE_FAST               'lineno'

 L. 111       784  LOAD_FAST                'location'
              787  LOAD_ATTR                is_address
              790  STORE_FAST               'is_address'

 L. 112       793  LOAD_CONST               None
              796  STORE_FAST               'modfunc'
              799  JUMP_FORWARD        802  'to 802'
            802_0  COME_FROM           799  '799'
            802_1  COME_FROM           736  '736'
            802_2  COME_FROM           383  '383'

 L. 113       802  LOAD_GLOBAL              Location
              805  LOAD_FAST                'filename'
              808  LOAD_FAST                'lineno'
              811  LOAD_FAST                'is_address'
              814  LOAD_FAST                'modfunc'
              817  CALL_FUNCTION_4       4  '4 positional, 0 named'
              820  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 295


def resolve_address_location--- This code section failed: ---

 L. 121         0  LOAD_FAST                'proc'
                3  LOAD_ATTR                curframe
                6  STORE_FAST               'curframe'

 L. 122         9  LOAD_FAST                'location'
               12  LOAD_STR                 '.'
               15  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    82  'to 82'

 L. 123        21  LOAD_GLOBAL              Mstack
               24  LOAD_ATTR                frame2file
               27  LOAD_FAST                'proc'
               30  LOAD_ATTR                core
               33  LOAD_FAST                'curframe'
               36  LOAD_STR                 'canonic'
               39  LOAD_CONST               False
               42  CALL_FUNCTION_258   258  '2 positional, 1 named'
               45  STORE_FAST               'filename'

 L. 124        48  LOAD_FAST                'curframe'
               51  LOAD_ATTR                f_lasti
               54  STORE_FAST               'offset'

 L. 125        57  LOAD_CONST               True
               60  STORE_FAST               'is_address'

 L. 126        63  LOAD_GLOBAL              Location
               66  LOAD_FAST                'filename'
               69  LOAD_FAST                'offset'
               72  LOAD_CONST               False
               75  LOAD_CONST               None
               78  CALL_FUNCTION_4       4  '4 positional, 0 named'
               81  RETURN_END_IF    

 L. 128        82  LOAD_GLOBAL              isinstance
               85  LOAD_FAST                'location'
               88  LOAD_GLOBAL              Location
               91  CALL_FUNCTION_2       2  '2 positional, 0 named'
               94  POP_JUMP_IF_TRUE    103  'to 103'
               97  LOAD_ASSERT              AssertionError
              100  RAISE_VARARGS_1       1  'exception'
            103_0  COME_FROM            94  '94'

 L. 129       103  LOAD_CONST               True
              106  STORE_FAST               'is_address'

 L. 130       109  LOAD_FAST                'proc'
              112  LOAD_ATTR                curframe
              115  POP_JUMP_IF_FALSE   139  'to 139'

 L. 131       118  LOAD_FAST                'curframe'
              121  LOAD_ATTR                f_globals
              124  STORE_FAST               'g'

 L. 132       127  LOAD_FAST                'curframe'
              130  LOAD_ATTR                f_locals
              133  STORE_FAST               'l'
              136  JUMP_FORWARD        157  'to 157'
              139  ELSE                     '157'

 L. 134       139  LOAD_GLOBAL              globals
              142  CALL_FUNCTION_0       0  '0 positional, 0 named'
              145  STORE_FAST               'g'

 L. 135       148  LOAD_GLOBAL              locals
              151  CALL_FUNCTION_0       0  '0 positional, 0 named'
              154  STORE_FAST               'l'
            157_0  COME_FROM           136  '136'

 L. 137       157  LOAD_FAST                'location'
              160  LOAD_ATTR                method
              163  POP_JUMP_IF_FALSE   357  'to 357'

 L. 139       166  LOAD_CONST               None
              169  DUP_TOP          
              170  STORE_FAST               'filename'
              173  STORE_FAST               'offset'

 L. 140       176  LOAD_STR                 'Object %s is not known yet as a function, '
              179  LOAD_FAST                'location'
              182  LOAD_ATTR                method
              185  BINARY_MODULO    
              186  STORE_FAST               'msg'

 L. 141       189  SETUP_EXCEPT        217  'to 217'

 L. 142       192  LOAD_GLOBAL              eval
              195  LOAD_FAST                'location'
              198  LOAD_ATTR                method
              201  LOAD_FAST                'g'
              204  LOAD_FAST                'l'
              207  CALL_FUNCTION_3       3  '3 positional, 0 named'
              210  STORE_FAST               'modfunc'
              213  POP_BLOCK        
              214  JUMP_FORWARD        242  'to 242'
            217_0  COME_FROM_EXCEPT    189  '189'

 L. 143       217  POP_TOP          
              218  POP_TOP          
              219  POP_TOP          

 L. 144       220  LOAD_FAST                'proc'
              223  LOAD_ATTR                errmsg
              226  LOAD_FAST                'msg'
              229  CALL_FUNCTION_1       1  '1 positional, 0 named'
              232  POP_TOP          

 L. 145       233  LOAD_GLOBAL              INVALID_LOCATION
              236  RETURN_VALUE     
              237  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
              241  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           214  '214'

 L. 147       242  SETUP_EXCEPT        299  'to 299'

 L. 149       245  LOAD_GLOBAL              inspect
              248  LOAD_ATTR                isfunction
              251  LOAD_FAST                'modfunc'
              254  CALL_FUNCTION_1       1  '1 positional, 0 named'
              257  POP_JUMP_IF_TRUE    295  'to 295'
              260  LOAD_GLOBAL              hasattr
              263  LOAD_FAST                'modfunc'
              266  LOAD_STR                 'im_func'
              269  CALL_FUNCTION_2       2  '2 positional, 0 named'
            272_0  COME_FROM           257  '257'
              272  POP_JUMP_IF_FALSE   278  'to 278'

 L. 150       275  JUMP_FORWARD        295  'to 295'
              278  ELSE                     '295'

 L. 152       278  LOAD_FAST                'proc'
              281  LOAD_ATTR                errmsg
              284  LOAD_FAST                'msg'
              287  CALL_FUNCTION_1       1  '1 positional, 0 named'
              290  POP_TOP          

 L. 153       291  LOAD_GLOBAL              INVALID_LOCATION
              294  RETURN_VALUE     
            295_0  COME_FROM           275  '275'
              295  POP_BLOCK        
              296  JUMP_FORWARD        324  'to 324'
            299_0  COME_FROM_EXCEPT    242  '242'

 L. 154       299  POP_TOP          
              300  POP_TOP          
              301  POP_TOP          

 L. 155       302  LOAD_FAST                'proc'
              305  LOAD_ATTR                errmsg
              308  LOAD_FAST                'msg'
              311  CALL_FUNCTION_1       1  '1 positional, 0 named'
              314  POP_TOP          

 L. 156       315  LOAD_GLOBAL              INVALID_LOCATION
              318  RETURN_VALUE     
              319  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
              323  END_FINALLY      
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           296  '296'

 L. 157       324  LOAD_FAST                'proc'
              327  LOAD_ATTR                core
              330  LOAD_ATTR                canonic
              333  LOAD_FAST                'modfunc'
              336  LOAD_ATTR                func_code
              339  LOAD_ATTR                co_filename
              342  CALL_FUNCTION_1       1  '1 positional, 0 named'
              345  STORE_FAST               'filename'

 L. 160       348  LOAD_CONST               0
              351  STORE_FAST               'offset'
              354  JUMP_FORWARD        791  'to 791'
              357  ELSE                     '791'

 L. 161       357  LOAD_FAST                'location'
              360  LOAD_ATTR                path
              363  POP_JUMP_IF_FALSE   719  'to 719'

 L. 162       366  LOAD_FAST                'proc'
              369  LOAD_ATTR                core
              372  LOAD_ATTR                canonic
              375  LOAD_FAST                'location'
              378  LOAD_ATTR                path
              381  CALL_FUNCTION_1       1  '1 positional, 0 named'
              384  STORE_FAST               'filename'

 L. 163       387  LOAD_FAST                'location'
              390  LOAD_ATTR                line_number
              393  STORE_FAST               'offset'

 L. 164       396  LOAD_FAST                'location'
              399  LOAD_ATTR                is_address
              402  STORE_FAST               'is_address'

 L. 165       405  LOAD_CONST               None
              408  STORE_FAST               'modfunc'

 L. 166       411  LOAD_STR                 '%s is not known as a file'
              414  LOAD_FAST                'location'
              417  LOAD_ATTR                path
              420  BINARY_MODULO    
              421  STORE_FAST               'msg'

 L. 167       424  LOAD_GLOBAL              osp
              427  LOAD_ATTR                isfile
              430  LOAD_FAST                'filename'
              433  CALL_FUNCTION_1       1  '1 positional, 0 named'
              436  POP_JUMP_IF_TRUE    653  'to 653'

 L. 169       439  SETUP_EXCEPT        467  'to 467'

 L. 170       442  LOAD_GLOBAL              eval
              445  LOAD_FAST                'location'
              448  LOAD_ATTR                path
              451  LOAD_FAST                'g'
              454  LOAD_FAST                'l'
              457  CALL_FUNCTION_3       3  '3 positional, 0 named'
              460  STORE_FAST               'modfunc'
              463  POP_BLOCK        
              464  JUMP_FORWARD        505  'to 505'
            467_0  COME_FROM_EXCEPT    439  '439'

 L. 171       467  POP_TOP          
              468  POP_TOP          
              469  POP_TOP          

 L. 172       470  LOAD_STR                 "Don't see '%s' as a existing file or as an module"

 L. 173       473  LOAD_FAST                'location'
              476  LOAD_ATTR                path
              479  BINARY_MODULO    
              480  STORE_FAST               'msg'

 L. 174       483  LOAD_FAST                'proc'
              486  LOAD_ATTR                errmsg
              489  LOAD_FAST                'msg'
              492  CALL_FUNCTION_1       1  '1 positional, 0 named'
              495  POP_TOP          

 L. 175       496  LOAD_GLOBAL              INVALID_LOCATION
              499  RETURN_VALUE     
              500  POP_EXCEPT       
              501  JUMP_FORWARD        505  'to 505'
              504  END_FINALLY      
            505_0  COME_FROM           501  '501'
            505_1  COME_FROM           464  '464'

 L. 177       505  LOAD_FAST                'location'
              508  LOAD_ATTR                is_address
              511  STORE_FAST               'is_address'

 L. 178       514  LOAD_GLOBAL              inspect
              517  LOAD_ATTR                ismodule
              520  LOAD_FAST                'modfunc'
              523  CALL_FUNCTION_1       1  '1 positional, 0 named'
              526  POP_JUMP_IF_FALSE   636  'to 636'

 L. 179       529  LOAD_GLOBAL              hasattr
              532  LOAD_FAST                'modfunc'
              535  LOAD_STR                 '__file__'
              538  CALL_FUNCTION_2       2  '2 positional, 0 named'
              541  POP_JUMP_IF_FALSE   620  'to 620'

 L. 180       544  LOAD_GLOBAL              pyficache
              547  LOAD_ATTR                pyc2py
              550  LOAD_FAST                'modfunc'
              553  LOAD_ATTR                __file__
              556  CALL_FUNCTION_1       1  '1 positional, 0 named'
              559  STORE_FAST               'filename'

 L. 181       562  LOAD_FAST                'proc'
              565  LOAD_ATTR                core
              568  LOAD_ATTR                canonic
              571  LOAD_FAST                'filename'
              574  CALL_FUNCTION_1       1  '1 positional, 0 named'
              577  STORE_FAST               'filename'

 L. 182       580  LOAD_FAST                'offset'
              583  POP_JUMP_IF_TRUE    601  'to 601'

 L. 184       586  LOAD_CONST               0
              589  STORE_FAST               'offset'

 L. 185       592  LOAD_CONST               True
              595  STORE_FAST               'is_address'
              598  JUMP_FORWARD        601  'to 601'
            601_0  COME_FROM           598  '598'

 L. 186       601  LOAD_GLOBAL              Location
              604  LOAD_FAST                'filename'
              607  LOAD_FAST                'offset'
              610  LOAD_FAST                'is_address'
              613  LOAD_FAST                'modfunc'
              616  CALL_FUNCTION_4       4  '4 positional, 0 named'
              619  RETURN_END_IF    

 L. 188       620  LOAD_STR                 "module '%s' doesn't have a file associated with it"

 L. 189       623  LOAD_FAST                'location'
              626  LOAD_ATTR                path
              629  BINARY_MODULO    
              630  STORE_FAST               'msg'
              633  JUMP_FORWARD        636  'to 636'
            636_0  COME_FROM           633  '633'

 L. 191       636  LOAD_FAST                'proc'
              639  LOAD_ATTR                errmsg
              642  LOAD_FAST                'msg'
              645  CALL_FUNCTION_1       1  '1 positional, 0 named'
              648  POP_TOP          

 L. 192       649  LOAD_GLOBAL              INVALID_LOCATION
              652  RETURN_END_IF    

 L. 193       653  LOAD_GLOBAL              pyficache
              656  LOAD_ATTR                maxline
              659  LOAD_FAST                'filename'
              662  CALL_FUNCTION_1       1  '1 positional, 0 named'
              665  STORE_FAST               'maxline'

 L. 194       668  LOAD_FAST                'maxline'
              671  POP_JUMP_IF_FALSE   791  'to 791'
              674  LOAD_FAST                'offset'
              677  LOAD_FAST                'maxline'
              680  COMPARE_OP               >
            683_0  COME_FROM           671  '671'
              683  POP_JUMP_IF_FALSE   791  'to 791'

 L. 196       686  LOAD_FAST                'proc'
              689  LOAD_ATTR                errmsg
              692  LOAD_STR                 'Line number %d out of range; %s has %d lines.'

 L. 197       695  LOAD_FAST                'offset'
              698  LOAD_FAST                'filename'
              701  LOAD_FAST                'maxline'
              704  BUILD_TUPLE_3         3 
              707  BINARY_MODULO    
              708  CALL_FUNCTION_1       1  '1 positional, 0 named'
              711  POP_TOP          

 L. 198       712  LOAD_GLOBAL              INVALID_LOCATION
              715  RETURN_END_IF    
              716  JUMP_FORWARD        791  'to 791'
              719  ELSE                     '791'

 L. 199       719  LOAD_FAST                'location'
              722  LOAD_ATTR                line_number
              725  LOAD_CONST               None
              728  COMPARE_OP               is-not
              731  POP_JUMP_IF_FALSE   791  'to 791'

 L. 200       734  LOAD_GLOBAL              Mstack
              737  LOAD_ATTR                frame2file
              740  LOAD_FAST                'proc'
              743  LOAD_ATTR                core
              746  LOAD_FAST                'curframe'
              749  LOAD_STR                 'canonic'
              752  LOAD_CONST               False
              755  CALL_FUNCTION_258   258  '2 positional, 1 named'
              758  STORE_FAST               'filename'

 L. 201       761  LOAD_FAST                'location'
              764  LOAD_ATTR                line_number
              767  STORE_FAST               'offset'

 L. 202       770  LOAD_FAST                'location'
              773  LOAD_ATTR                is_address
              776  STORE_FAST               'is_address'

 L. 203       779  LOAD_FAST                'proc'
              782  LOAD_ATTR                list_object
              785  STORE_FAST               'modfunc'
              788  JUMP_FORWARD        791  'to 791'
            791_0  COME_FROM           788  '788'
            791_1  COME_FROM           716  '716'
            791_2  COME_FROM           354  '354'

 L. 204       791  LOAD_GLOBAL              Location
              794  LOAD_FAST                'filename'
              797  LOAD_FAST                'offset'
              800  LOAD_FAST                'is_address'
              803  LOAD_FAST                'modfunc'
              806  CALL_FUNCTION_4       4  '4 positional, 0 named'
              809  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 272