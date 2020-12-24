# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythonic/pythonic.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 5083 bytes
import ast, logging, traceback, collections.abc
LOGGER = logging.getLogger(__name__)
tutor.qtype_inherit('smallbox')
base1, _ = tutor.question('pythoncode')
defaults.update({'csq_soln':'', 
 'csq_check_function':lambda sub, soln: type(sub) == type(soln) and sub == soln, 
 'csq_input_check':lambda sub: None, 
 'csq_npoints':1, 
 'csq_msg_function':lambda sub, soln: '', 
 'csq_show_check':False, 
 'csq_code_pre':'', 
 'csq_mode':'raw', 
 'csq_size':50})

def gensym(code=''):
    pre = n = '___'
    count = 0
    while n in code:
        n = '%s%s' % (pre, count)
        count += 1

    return n


INVALID_SUBMISSION_MSG = '<font color="red">Your submission could not be evaluated.  Please check that you have entered a valid Python expression.</font>  '

def handle_submission--- This code section failed: ---

 L.  61         0  LOAD_FAST                'submissions'
                2  LOAD_FAST                'info'
                4  LOAD_STR                 'csq_name'
                6  BINARY_SUBSCR    
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              strip
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'sub'

 L.  62        16  LOAD_GLOBAL              LOGGER
               18  LOAD_METHOD              error
               20  LOAD_STR                 '[qtypes.pythonic] submission: %r'
               22  LOAD_FAST                'sub'
               24  BINARY_MODULO    
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L.  64        30  LOAD_FAST                'info'
               32  LOAD_STR                 'csq_input_check'
               34  BINARY_SUBSCR    
               36  LOAD_FAST                'sub'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'inp'

 L.  65        42  LOAD_FAST                'inp'
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_FALSE    64  'to 64'

 L.  66        50  LOAD_CONST               0.0
               52  LOAD_STR                 '<font color="red">%s</font>'
               54  LOAD_FAST                'inp'
               56  BINARY_MODULO    
               58  LOAD_CONST               ('score', 'msg')
               60  BUILD_CONST_KEY_MAP_2     2 
               62  RETURN_VALUE     
             64_0  COME_FROM            48  '48'

 L.  68        64  LOAD_GLOBAL              base1
               66  LOAD_STR                 'get_sandbox'
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'info'
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          

 L.  69        76  LOAD_FAST                'info'
               78  LOAD_STR                 'csq_mode'
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'raw'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    98  'to 98'

 L.  70        88  LOAD_FAST                'info'
               90  LOAD_STR                 'csq_soln'
               92  BINARY_SUBSCR    
               94  STORE_FAST               'soln'
               96  JUMP_FORWARD        176  'to 176'
             98_0  COME_FROM            86  '86'

 L.  72        98  LOAD_FAST                'info'
              100  LOAD_STR                 'csq_code_pre'
              102  BINARY_SUBSCR    
              104  STORE_FAST               'code'

 L.  73       106  LOAD_FAST                'info'
              108  LOAD_STR                 'csq_soln'
              110  BINARY_SUBSCR    
              112  STORE_FAST               's'

 L.  74       114  LOAD_FAST                'code'
              116  LOAD_STR                 '\n_catsoop_answer = %s'
              118  LOAD_FAST                's'
              120  BINARY_MODULO    
              122  INPLACE_ADD      
              124  STORE_FAST               'code'

 L.  75       126  LOAD_FAST                'info'
              128  LOAD_METHOD              get
              130  LOAD_STR                 'csq_options'
              132  BUILD_MAP_0           0 
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'opts'

 L.  76       138  LOAD_FAST                'info'
              140  LOAD_STR                 'sandbox_run_code'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'info'
              146  LOAD_FAST                'code'
              148  LOAD_FAST                'opts'
              150  LOAD_CONST               True
              152  LOAD_CONST               ('result_as_string',)
              154  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L.  77       156  LOAD_STR                 'info'

 L.  76       158  BINARY_SUBSCR    

 L.  78       160  LOAD_STR                 'result'

 L.  76       162  BINARY_SUBSCR    
              164  STORE_FAST               'soln'

 L.  79       166  LOAD_GLOBAL              eval
              168  LOAD_FAST                'soln'
              170  LOAD_FAST                'info'
              172  CALL_FUNCTION_2       2  ''
              174  STORE_FAST               'soln'
            176_0  COME_FROM            96  '96'

 L.  80       176  SETUP_FINALLY       332  'to 332'

 L.  81       178  LOAD_FAST                'sub'
              180  LOAD_STR                 ''
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   208  'to 208'

 L.  82       186  LOAD_GLOBAL              LOGGER
              188  LOAD_METHOD              debug
              190  LOAD_STR                 '[qtypes.pythonic] invalid submission, empty submission'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L.  83       196  LOAD_CONST               0.0
              198  LOAD_GLOBAL              INVALID_SUBMISSION_MSG
              200  LOAD_CONST               ('score', 'msg')
              202  BUILD_CONST_KEY_MAP_2     2 
              204  POP_BLOCK        
              206  RETURN_VALUE     
            208_0  COME_FROM           184  '184'

 L.  84       208  LOAD_GLOBAL              ast
              210  LOAD_ATTR                parse
              212  LOAD_FAST                'sub'
              214  LOAD_STR                 'eval'
              216  LOAD_CONST               ('mode',)
              218  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              220  POP_TOP          

 L.  85       222  LOAD_FAST                'info'
              224  LOAD_STR                 'csq_code_pre'
              226  BINARY_SUBSCR    
              228  STORE_FAST               'code'

 L.  86       230  LOAD_FAST                'code'
              232  LOAD_STR                 '\n_catsoop_answer = %s'
              234  LOAD_FAST                'sub'
              236  BINARY_MODULO    
              238  INPLACE_ADD      
              240  STORE_FAST               'code'

 L.  87       242  LOAD_FAST                'info'
              244  LOAD_METHOD              get
              246  LOAD_STR                 'csq_options'
              248  BUILD_MAP_0           0 
              250  CALL_METHOD_2         2  ''
              252  STORE_FAST               'opts'

 L.  88       254  LOAD_GLOBAL              LOGGER
              256  LOAD_METHOD              debug
              258  LOAD_STR                 '[qtypes.pythonic] code to run:\n%s'
              260  LOAD_FAST                'code'
              262  BINARY_MODULO    
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          

 L.  89       268  LOAD_FAST                'info'
              270  LOAD_STR                 'sandbox_run_code'
              272  BINARY_SUBSCR    

 L.  90       274  LOAD_FAST                'info'

 L.  90       276  LOAD_FAST                'code'

 L.  90       278  LOAD_FAST                'opts'

 L.  90       280  LOAD_FAST                'info'
              282  LOAD_STR                 'csq_mode'
              284  BINARY_SUBSCR    
              286  LOAD_STR                 'raw'
              288  COMPARE_OP               !=

 L.  89       290  LOAD_CONST               ('result_as_string',)
              292  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L.  91       294  LOAD_STR                 'info'

 L.  89       296  BINARY_SUBSCR    

 L.  91       298  LOAD_STR                 'result'

 L.  89       300  BINARY_SUBSCR    
              302  STORE_FAST               'sub'

 L.  92       304  LOAD_FAST                'info'
              306  LOAD_STR                 'csq_mode'
              308  BINARY_SUBSCR    
              310  LOAD_STR                 'raw'
              312  COMPARE_OP               !=
          314_316  POP_JUMP_IF_FALSE   328  'to 328'

 L.  93       318  LOAD_GLOBAL              eval
              320  LOAD_FAST                'sub'
              322  LOAD_FAST                'info'
              324  CALL_FUNCTION_2       2  ''
              326  STORE_FAST               'sub'
            328_0  COME_FROM           314  '314'
              328  POP_BLOCK        
              330  JUMP_FORWARD        546  'to 546'
            332_0  COME_FROM_FINALLY   176  '176'

 L.  94       332  DUP_TOP          
              334  LOAD_GLOBAL              Exception
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   544  'to 544'
              342  POP_TOP          
              344  STORE_FAST               'err'
              346  POP_TOP          
              348  SETUP_FINALLY       532  'to 532'

 L.  95       350  LOAD_GLOBAL              LOGGER
              352  LOAD_METHOD              error
              354  LOAD_STR                 '[qtypes.pythonic] invalid submission: %r'
              356  LOAD_FAST                'sub'
              358  BINARY_MODULO    
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          

 L.  96       364  LOAD_GLOBAL              LOGGER
              366  LOAD_METHOD              error
              368  LOAD_STR                 '[qtypes.pythonic] invalid submission exception=%s'
              370  LOAD_GLOBAL              str
              372  LOAD_FAST                'err'
              374  CALL_FUNCTION_1       1  ''
              376  BINARY_MODULO    
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          

 L.  97       382  LOAD_GLOBAL              LOGGER
              384  LOAD_METHOD              error
              386  LOAD_STR                 '[qtypes.pythonic] traceback: %s'
              388  LOAD_GLOBAL              traceback
              390  LOAD_METHOD              format_exc
              392  CALL_METHOD_0         0  ''
              394  BINARY_MODULO    
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          

 L.  98       400  LOAD_STR                 ''
              402  STORE_FAST               'msg'

 L.  99       404  LOAD_FAST                'info'
              406  LOAD_STR                 'csq_msg_function'
              408  BINARY_SUBSCR    
              410  STORE_FAST               'mfunc'

 L. 100       412  SETUP_FINALLY       432  'to 432'

 L. 101       414  LOAD_FAST                'msg'
              416  LOAD_FAST                'mfunc'
              418  LOAD_FAST                'sub'
              420  LOAD_FAST                'soln'
              422  CALL_FUNCTION_2       2  ''
              424  INPLACE_ADD      
              426  STORE_FAST               'msg'
              428  POP_BLOCK        
              430  JUMP_FORWARD        474  'to 474'
            432_0  COME_FROM_FINALLY   412  '412'

 L. 102       432  POP_TOP          
              434  POP_TOP          
              436  POP_TOP          

 L. 103       438  SETUP_FINALLY       456  'to 456'

 L. 104       440  LOAD_FAST                'msg'
              442  LOAD_FAST                'mfunc'
              444  LOAD_FAST                'sub'
              446  CALL_FUNCTION_1       1  ''
              448  INPLACE_ADD      
              450  STORE_FAST               'msg'
              452  POP_BLOCK        
              454  JUMP_FORWARD        468  'to 468'
            456_0  COME_FROM_FINALLY   438  '438'

 L. 105       456  POP_TOP          
              458  POP_TOP          
              460  POP_TOP          

 L. 106       462  POP_EXCEPT       
              464  JUMP_FORWARD        468  'to 468'
              466  END_FINALLY      
            468_0  COME_FROM           464  '464'
            468_1  COME_FROM           454  '454'
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           430  '430'

 L. 107       474  LOAD_FAST                'msg'
              476  LOAD_STR                 ''
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   488  'to 488'

 L. 108       484  LOAD_GLOBAL              INVALID_SUBMISSION_MSG
              486  STORE_FAST               'msg'
            488_0  COME_FROM           480  '480'

 L. 109       488  LOAD_FAST                'info'
              490  LOAD_STR                 'csq_show_check'
              492  BINARY_SUBSCR    
          494_496  POP_JUMP_IF_FALSE   514  'to 514'

 L. 110       498  LOAD_FAST                'msg'
              500  LOAD_STR                 '<img src="%s" /><br/>'
              502  LOAD_FAST                'info'
              504  LOAD_STR                 'cs_cross_image'
              506  BINARY_SUBSCR    
              508  BINARY_MODULO    
              510  INPLACE_ADD      
              512  STORE_FAST               'msg'
            514_0  COME_FROM           494  '494'

 L. 111       514  LOAD_CONST               0.0
              516  LOAD_FAST                'msg'
              518  LOAD_CONST               ('score', 'msg')
              520  BUILD_CONST_KEY_MAP_2     2 
              522  ROT_FOUR         
              524  POP_BLOCK        
              526  POP_EXCEPT       
              528  CALL_FINALLY        532  'to 532'
              530  RETURN_VALUE     
            532_0  COME_FROM           528  '528'
            532_1  COME_FROM_FINALLY   348  '348'
              532  LOAD_CONST               None
              534  STORE_FAST               'err'
              536  DELETE_FAST              'err'
              538  END_FINALLY      
              540  POP_EXCEPT       
              542  JUMP_FORWARD        546  'to 546'
            544_0  COME_FROM           338  '338'
              544  END_FINALLY      
            546_0  COME_FROM           542  '542'
            546_1  COME_FROM           330  '330'

 L. 113       546  LOAD_FAST                'info'
              548  LOAD_STR                 'csq_check_function'
              550  BINARY_SUBSCR    
              552  STORE_FAST               'check'

 L. 114       554  SETUP_FINALLY       570  'to 570'

 L. 115       556  LOAD_FAST                'check'
              558  LOAD_FAST                'sub'
              560  LOAD_FAST                'soln'
              562  CALL_FUNCTION_2       2  ''
              564  STORE_FAST               'check_result'
              566  POP_BLOCK        
              568  JUMP_FORWARD        624  'to 624'
            570_0  COME_FROM_FINALLY   554  '554'

 L. 116       570  POP_TOP          
              572  POP_TOP          
              574  POP_TOP          

 L. 117       576  LOAD_FAST                'info'
              578  LOAD_STR                 'csm_errors'
              580  BINARY_SUBSCR    
              582  STORE_FAST               'err'

 L. 118       584  LOAD_FAST                'err'
              586  LOAD_METHOD              html_format
              588  LOAD_FAST                'err'
              590  LOAD_METHOD              clear_info
              592  LOAD_FAST                'info'
              594  LOAD_GLOBAL              traceback
              596  LOAD_METHOD              format_exc
              598  CALL_METHOD_0         0  ''
              600  CALL_METHOD_2         2  ''
              602  CALL_METHOD_1         1  ''
              604  STORE_FAST               'e'

 L. 120       606  LOAD_CONST               0.0

 L. 121       608  LOAD_STR                 '<font color="red">An error occurred in the checker: <pre>%s</pre></font>'

 L. 122       610  LOAD_FAST                'e'

 L. 121       612  BINARY_MODULO    

 L. 119       614  BUILD_TUPLE_2         2 
              616  STORE_FAST               'check_result'
              618  POP_EXCEPT       
              620  JUMP_FORWARD        624  'to 624'
              622  END_FINALLY      
            624_0  COME_FROM           620  '620'
            624_1  COME_FROM           568  '568'

 L. 125       624  LOAD_GLOBAL              isinstance
              626  LOAD_FAST                'check_result'
              628  LOAD_GLOBAL              collections
              630  LOAD_ATTR                abc
              632  LOAD_ATTR                Mapping
              634  CALL_FUNCTION_2       2  ''
          636_638  POP_JUMP_IF_FALSE   658  'to 658'

 L. 126       640  LOAD_FAST                'check_result'
              642  LOAD_STR                 'score'
              644  BINARY_SUBSCR    
              646  STORE_FAST               'score'

 L. 127       648  LOAD_FAST                'check_result'
              650  LOAD_STR                 'msg'
              652  BINARY_SUBSCR    
              654  STORE_FAST               'msg'
              656  JUMP_FORWARD        754  'to 754'
            658_0  COME_FROM           636  '636'

 L. 128       658  LOAD_GLOBAL              isinstance
              660  LOAD_FAST                'check_result'
              662  LOAD_GLOBAL              collections
              664  LOAD_ATTR                abc
              666  LOAD_ATTR                Sequence
              668  CALL_FUNCTION_2       2  ''
          670_672  POP_JUMP_IF_FALSE   684  'to 684'

 L. 129       674  LOAD_FAST                'check_result'
              676  UNPACK_SEQUENCE_2     2 
              678  STORE_FAST               'score'
              680  STORE_FAST               'msg'
              682  JUMP_FORWARD        754  'to 754'
            684_0  COME_FROM           670  '670'

 L. 131       684  LOAD_FAST                'check_result'
              686  STORE_FAST               'score'

 L. 132       688  LOAD_FAST                'info'
              690  LOAD_STR                 'csq_msg_function'
              692  BINARY_SUBSCR    
              694  STORE_FAST               'mfunc'

 L. 133       696  SETUP_FINALLY       712  'to 712'

 L. 134       698  LOAD_FAST                'mfunc'
              700  LOAD_FAST                'sub'
              702  LOAD_FAST                'soln'
              704  CALL_FUNCTION_2       2  ''
              706  STORE_FAST               'msg'
              708  POP_BLOCK        
              710  JUMP_FORWARD        754  'to 754'
            712_0  COME_FROM_FINALLY   696  '696'

 L. 135       712  POP_TOP          
              714  POP_TOP          
              716  POP_TOP          

 L. 136       718  SETUP_FINALLY       732  'to 732'

 L. 137       720  LOAD_FAST                'mfunc'
              722  LOAD_FAST                'sub'
              724  CALL_FUNCTION_1       1  ''
              726  STORE_FAST               'msg'
              728  POP_BLOCK        
              730  JUMP_FORWARD        748  'to 748'
            732_0  COME_FROM_FINALLY   718  '718'

 L. 138       732  POP_TOP          
              734  POP_TOP          
              736  POP_TOP          

 L. 139       738  LOAD_STR                 ''
              740  STORE_FAST               'msg'
              742  POP_EXCEPT       
              744  JUMP_FORWARD        748  'to 748'
              746  END_FINALLY      
            748_0  COME_FROM           744  '744'
            748_1  COME_FROM           730  '730'
              748  POP_EXCEPT       
              750  JUMP_FORWARD        754  'to 754'
              752  END_FINALLY      
            754_0  COME_FROM           750  '750'
            754_1  COME_FROM           710  '710'
            754_2  COME_FROM           682  '682'
            754_3  COME_FROM           656  '656'

 L. 141       754  LOAD_GLOBAL              float
              756  LOAD_FAST                'score'
              758  CALL_FUNCTION_1       1  ''
              760  STORE_FAST               'percent'

 L. 142       762  LOAD_STR                 ''
              764  STORE_FAST               'response'

 L. 143       766  LOAD_FAST                'info'
              768  LOAD_STR                 'csq_show_check'
              770  BINARY_SUBSCR    
          772_774  POP_JUMP_IF_FALSE   822  'to 822'

 L. 144       776  LOAD_FAST                'percent'
              778  LOAD_CONST               1.0
              780  COMPARE_OP               ==
          782_784  POP_JUMP_IF_FALSE   800  'to 800'

 L. 145       786  LOAD_STR                 '<img src="%s" /><br/>'
              788  LOAD_FAST                'info'
              790  LOAD_STR                 'cs_check_image'
              792  BINARY_SUBSCR    
              794  BINARY_MODULO    
              796  STORE_FAST               'response'
              798  JUMP_FORWARD        822  'to 822'
            800_0  COME_FROM           782  '782'

 L. 146       800  LOAD_FAST                'percent'
              802  LOAD_CONST               0.0
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   822  'to 822'

 L. 147       810  LOAD_STR                 '<img src="%s" /><br/>'
              812  LOAD_FAST                'info'
              814  LOAD_STR                 'cs_cross_image'
              816  BINARY_SUBSCR    
              818  BINARY_MODULO    
              820  STORE_FAST               'response'
            822_0  COME_FROM           806  '806'
            822_1  COME_FROM           798  '798'
            822_2  COME_FROM           772  '772'

 L. 149       822  LOAD_FAST                'response'
              824  LOAD_FAST                'msg'
              826  INPLACE_ADD      
              828  STORE_FAST               'response'

 L. 151       830  LOAD_FAST                'percent'
              832  LOAD_FAST                'response'
              834  LOAD_CONST               ('score', 'msg')
              836  BUILD_CONST_KEY_MAP_2     2 
              838  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 524


def answer_display(**info):
    if info['csq_mode'] == 'raw':
        out = '<p>Solution: <tt>%r</tt><p>' % (info['csq_soln'],)
    else:
        out = '<p>Solution: <tt>%s</tt><p>' % (info['csq_soln'],)
    return out