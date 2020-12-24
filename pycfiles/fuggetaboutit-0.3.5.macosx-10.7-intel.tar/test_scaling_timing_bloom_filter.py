# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/fuggetaboutit/tests/test_scaling_timing_bloom_filter.py
# Compiled at: 2013-11-19 18:52:28
from fuggetaboutit.scaling_timing_bloom_filter import ScalingTimingBloomFilter
import tornado.ioloop, tornado.testing, time
from fuggetaboutit.utils import TimingBlock, TestFile

class TestScalingTimingBloomFilter(tornado.testing.AsyncTestCase):

    def test_decay(self):
        stbf = ScalingTimingBloomFilter(500, decay_time=4, ioloop=self.io_loop).start()
        stbf += 'hello'
        assert stbf.contains('hello') == True
        try:
            self.wait(timeout=4)
        except:
            pass

        assert stbf.contains('hello') == False

    def test_save(self):
        stbf = ScalingTimingBloomFilter(5, decay_time=30, ioloop=self.io_loop).start()
        stbf += 'hello'
        assert 'hello' in stbf
        prev_num_nonzero = stbf.blooms[0]['bloom'].num_non_zero
        stbf.tofile(open('test.stbf', 'w+'))
        with TestFile('test.stbf') as (fd):
            stbf2 = ScalingTimingBloomFilter.fromfile(fd)
        stbf.add('hello2')
        assert 'hello' in stbf
        assert 'hello2' in stbf
        assert prev_num_nonzero == stbf2.blooms[0]['bloom'].num_non_zero

    def test_size_stability--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL           0  'ScalingTimingBloomFilter'
                3  LOAD_CONST               10
                6  LOAD_CONST               'decay_time'
                9  LOAD_CONST               5
               12  LOAD_CONST               'min_fill_factor'
               15  LOAD_CONST               0.2
               18  LOAD_CONST               'growth_factor'
               21  LOAD_CONST               2
               24  LOAD_CONST               'ioloop'
               27  LOAD_FAST             0  'self'
               30  LOAD_ATTR             1  'io_loop'
               33  CALL_FUNCTION_1025  1025  None
               36  LOAD_ATTR             2  'start'
               39  CALL_FUNCTION_0       0  None
               42  STORE_FAST            1  'stbf'

 L.  40        45  SETUP_LOOP           37  'to 85'
               48  LOAD_GLOBAL           3  'xrange'
               51  LOAD_CONST               100
               54  CALL_FUNCTION_1       1  None
               57  GET_ITER         
               58  FOR_ITER             23  'to 84'
               61  STORE_FAST            2  'i'

 L.  41        64  LOAD_FAST             1  'stbf'
               67  LOAD_ATTR             4  'add'
               70  LOAD_CONST               'FOO%d'
               73  LOAD_FAST             2  'i'
               76  BINARY_MODULO    
               77  CALL_FUNCTION_1       1  None
               80  POP_TOP          
               81  JUMP_BACK            58  'to 58'
               84  POP_BLOCK        
             85_0  COME_FROM            45  '45'

 L.  43        85  LOAD_GLOBAL           5  'len'
               88  LOAD_FAST             1  'stbf'
               91  LOAD_ATTR             6  'blooms'
               94  CALL_FUNCTION_1       1  None
               97  LOAD_CONST               0
              100  COMPARE_OP            4  >
              103  POP_JUMP_IF_TRUE    115  'to 115'
              106  LOAD_ASSERT              AssertionError
              109  LOAD_CONST               'Did not scale up'
              112  RAISE_VARARGS_2       2  None

 L.  45       115  SETUP_LOOP          118  'to 236'
              118  LOAD_GLOBAL           3  'xrange'
              121  LOAD_CONST               100
              124  LOAD_CONST               130
              127  CALL_FUNCTION_2       2  None
              130  GET_ITER         
              131  FOR_ITER            101  'to 235'
              134  STORE_FAST            2  'i'

 L.  46       137  LOAD_FAST             1  'stbf'
              140  LOAD_ATTR             4  'add'
              143  LOAD_CONST               'FOO%d'
              146  LOAD_FAST             2  'i'
              149  BINARY_MODULO    
              150  CALL_FUNCTION_1       1  None
              153  POP_TOP          

 L.  47       154  SETUP_EXCEPT         20  'to 177'

 L.  48       157  LOAD_FAST             0  'self'
              160  LOAD_ATTR             8  'wait'
              163  LOAD_CONST               'timeout'
              166  LOAD_CONST               0.5
              169  CALL_FUNCTION_256   256  None
              172  POP_TOP          
              173  POP_BLOCK        
              174  JUMP_FORWARD          7  'to 184'
            177_0  COME_FROM           154  '154'

 L.  49       177  POP_TOP          
              178  POP_TOP          
              179  POP_TOP          

 L.  50       180  JUMP_FORWARD          1  'to 184'
              183  END_FINALLY      
            184_0  COME_FROM           183  '183'
            184_1  COME_FROM           174  '174'

 L.  51       184  LOAD_GLOBAL           5  'len'
              187  LOAD_FAST             1  'stbf'
              190  LOAD_ATTR             6  'blooms'
              193  CALL_FUNCTION_1       1  None
              196  LOAD_CONST               1
              199  COMPARE_OP            2  ==
              202  POP_JUMP_IF_FALSE   131  'to 131'
              205  LOAD_FAST             1  'stbf'
              208  LOAD_ATTR             6  'blooms'
              211  LOAD_CONST               0
              214  BINARY_SUBSCR    
              215  LOAD_CONST               'id'
              218  BINARY_SUBSCR    
              219  LOAD_CONST               1
              222  COMPARE_OP            2  ==
            225_0  COME_FROM           202  '202'
              225  POP_JUMP_IF_FALSE   131  'to 131'

 L.  52       228  LOAD_CONST               None
              231  RETURN_END_IF    
            232_0  COME_FROM           225  '225'
              232  JUMP_BACK           131  'to 131'
              235  POP_BLOCK        
            236_0  COME_FROM           115  '115'

 L.  53       236  LOAD_CONST               'Did not scale down'
              239  POP_JUMP_IF_TRUE    248  'to 248'
              242  LOAD_ASSERT              AssertionError
              245  RAISE_VARARGS_1       1  None

Parse error at or near `LOAD_ASSERT' instruction at offset 242

    def test_holistic--- This code section failed: ---

 L.  57         0  LOAD_GLOBAL           0  'int'
                3  LOAD_CONST               10000.0
                6  CALL_FUNCTION_1       1  None
                9  STORE_FAST            1  'n'

 L.  58        12  LOAD_GLOBAL           0  'int'
               15  LOAD_CONST               20000.0
               18  CALL_FUNCTION_1       1  None
               21  STORE_FAST            2  'N'

 L.  59        24  LOAD_CONST               3
               27  STORE_FAST            3  'T'

 L.  60        30  LOAD_CONST               'ScalingTimingBloom with capacity %e and expiration time %ds'
               33  LOAD_FAST             1  'n'
               36  LOAD_FAST             3  'T'
               39  BUILD_TUPLE_2         2 
               42  BINARY_MODULO    
               43  PRINT_ITEM       
               44  PRINT_NEWLINE_CONT

 L.  62        45  LOAD_GLOBAL           1  'TimingBlock'
               48  LOAD_CONST               'Initialization'
               51  CALL_FUNCTION_1       1  None
               54  SETUP_WITH           32  'to 89'
               57  POP_TOP          

 L.  63        58  LOAD_GLOBAL           2  'ScalingTimingBloomFilter'
               61  LOAD_FAST             1  'n'
               64  LOAD_CONST               'decay_time'
               67  LOAD_FAST             3  'T'
               70  LOAD_CONST               'ioloop'
               73  LOAD_FAST             0  'self'
               76  LOAD_ATTR             3  'io_loop'
               79  CALL_FUNCTION_513   513  None
               82  STORE_FAST            4  'stbf'
               85  POP_BLOCK        
               86  LOAD_CONST               None
             89_0  COME_FROM_WITH       54  '54'
               89  WITH_CLEANUP     
               90  END_FINALLY      

 L.  65        91  LOAD_FAST             4  'stbf'
               94  LOAD_ATTR             4  'decay'
               97  STORE_DEREF           0  'orig_decay'

 L.  66       100  LOAD_CLOSURE          0  'orig_decay'
              106  LOAD_CODE                <code_object new_decay>
              109  MAKE_CLOSURE_0        0  None
              112  STORE_FAST            5  'new_decay'

 L.  70       115  LOAD_GLOBAL           5  'setattr'
              118  LOAD_FAST             4  'stbf'
              121  LOAD_CONST               'decay'
              124  LOAD_FAST             5  'new_decay'
              127  CALL_FUNCTION_3       3  None
              130  POP_TOP          

 L.  71       131  LOAD_FAST             4  'stbf'
              134  LOAD_ATTR             6  '_setup_decay'
              137  CALL_FUNCTION_0       0  None
              140  POP_TOP          

 L.  72       141  LOAD_FAST             4  'stbf'
              144  LOAD_ATTR             7  'start'
              147  CALL_FUNCTION_0       0  None
              150  POP_TOP          

 L.  74       151  LOAD_CONST               'State of blooms: %d blooms with expected error %.2f%%'
              154  LOAD_GLOBAL           8  'len'
              157  LOAD_FAST             4  'stbf'
              160  LOAD_ATTR             9  'blooms'
              163  CALL_FUNCTION_1       1  None
              166  LOAD_FAST             4  'stbf'
              169  LOAD_ATTR            10  'expected_error'
              172  CALL_FUNCTION_0       0  None
              175  LOAD_CONST               100.0
              178  BINARY_MULTIPLY  
              179  BUILD_TUPLE_2         2 
              182  BINARY_MODULO    
              183  PRINT_ITEM       
              184  PRINT_NEWLINE_CONT

 L.  76       185  LOAD_GLOBAL           1  'TimingBlock'
              188  LOAD_CONST               'Adding %d values'
              191  LOAD_FAST             2  'N'
              194  BINARY_MODULO    
              195  LOAD_FAST             2  'N'
              198  CALL_FUNCTION_2       2  None
              201  SETUP_WITH           47  'to 251'
              204  POP_TOP          

 L.  77       205  SETUP_LOOP           39  'to 247'
              208  LOAD_GLOBAL          11  'xrange'
              211  LOAD_FAST             2  'N'
              214  CALL_FUNCTION_1       1  None
              217  GET_ITER         
              218  FOR_ITER             25  'to 246'
              221  STORE_FAST            6  'i'

 L.  78       224  LOAD_FAST             4  'stbf'
              227  LOAD_ATTR            12  'add'
              230  LOAD_GLOBAL          13  'str'
              233  LOAD_FAST             6  'i'
              236  CALL_FUNCTION_1       1  None
              239  CALL_FUNCTION_1       1  None
              242  POP_TOP          
              243  JUMP_BACK           218  'to 218'
              246  POP_BLOCK        
            247_0  COME_FROM           205  '205'
              247  POP_BLOCK        
              248  LOAD_CONST               None
            251_0  COME_FROM_WITH      201  '201'
              251  WITH_CLEANUP     
              252  END_FINALLY      

 L.  79       253  LOAD_GLOBAL          14  'time'
              256  LOAD_ATTR            14  'time'
              259  CALL_FUNCTION_0       0  None
              262  STORE_FAST            7  'last_insert'

 L.  81       265  LOAD_CONST               'State of blooms: %d blooms with expected error %.2f%%'
              268  LOAD_GLOBAL           8  'len'
              271  LOAD_FAST             4  'stbf'
              274  LOAD_ATTR             9  'blooms'
              277  CALL_FUNCTION_1       1  None
              280  LOAD_FAST             4  'stbf'
              283  LOAD_ATTR            10  'expected_error'
              286  CALL_FUNCTION_0       0  None
              289  LOAD_CONST               100.0
              292  BINARY_MULTIPLY  
              293  BUILD_TUPLE_2         2 
              296  BINARY_MODULO    
              297  PRINT_ITEM       
              298  PRINT_NEWLINE_CONT

 L.  83       299  LOAD_GLOBAL           1  'TimingBlock'
              302  LOAD_CONST               'Testing %d positive values'
              305  LOAD_FAST             2  'N'
              308  BINARY_MODULO    
              309  LOAD_FAST             2  'N'
              312  CALL_FUNCTION_2       2  None
              315  SETUP_WITH           52  'to 370'
              318  POP_TOP          

 L.  84       319  SETUP_LOOP           44  'to 366'
              322  LOAD_GLOBAL          11  'xrange'
              325  LOAD_FAST             2  'N'
              328  CALL_FUNCTION_1       1  None
              331  GET_ITER         
              332  FOR_ITER             30  'to 365'
              335  STORE_FAST            6  'i'

 L.  85       338  LOAD_GLOBAL          13  'str'
              341  LOAD_FAST             6  'i'
              344  CALL_FUNCTION_1       1  None
              347  LOAD_FAST             4  'stbf'
              350  COMPARE_OP            6  in
              353  POP_JUMP_IF_TRUE    332  'to 332'
              356  LOAD_ASSERT              AssertionError
              359  RAISE_VARARGS_1       1  None
              362  JUMP_BACK           332  'to 332'
              365  POP_BLOCK        
            366_0  COME_FROM           319  '319'
              366  POP_BLOCK        
              367  LOAD_CONST               None
            370_0  COME_FROM_WITH      315  '315'
              370  WITH_CLEANUP     
              371  END_FINALLY      

 L.  87       372  LOAD_GLOBAL           1  'TimingBlock'
              375  LOAD_CONST               'Testing %d negative values'
              378  LOAD_FAST             2  'N'
              381  BINARY_MODULO    
              382  LOAD_FAST             2  'N'
              385  CALL_FUNCTION_2       2  None
              388  SETUP_WITH          125  'to 516'
              391  POP_TOP          

 L.  88       392  LOAD_CONST               0
              395  STORE_FAST            8  'err'

 L.  89       398  SETUP_LOOP           58  'to 459'
              401  LOAD_GLOBAL          11  'xrange'
              404  LOAD_FAST             2  'N'
              407  LOAD_CONST               2
              410  LOAD_FAST             2  'N'
              413  BINARY_MULTIPLY  
              414  CALL_FUNCTION_2       2  None
              417  GET_ITER         
              418  FOR_ITER             37  'to 458'
              421  STORE_FAST            6  'i'

 L.  90       424  LOAD_GLOBAL          13  'str'
              427  LOAD_FAST             6  'i'
              430  CALL_FUNCTION_1       1  None
              433  LOAD_FAST             4  'stbf'
              436  COMPARE_OP            6  in
              439  POP_JUMP_IF_FALSE   418  'to 418'

 L.  91       442  LOAD_FAST             8  'err'
              445  LOAD_CONST               1
              448  INPLACE_ADD      
              449  STORE_FAST            8  'err'
              452  JUMP_BACK           418  'to 418'
              455  JUMP_BACK           418  'to 418'
              458  POP_BLOCK        
            459_0  COME_FROM           398  '398'

 L.  92       459  LOAD_FAST             8  'err'
              462  LOAD_GLOBAL          16  'float'
              465  LOAD_FAST             2  'N'
              468  CALL_FUNCTION_1       1  None
              471  BINARY_DIVIDE    
              472  STORE_FAST            9  'tot_err'

 L.  93       475  LOAD_FAST             9  'tot_err'
              478  LOAD_FAST             4  'stbf'
              481  LOAD_ATTR            17  'error'
              484  COMPARE_OP            1  <=
              487  POP_JUMP_IF_TRUE    512  'to 512'
              490  LOAD_ASSERT              AssertionError
              493  LOAD_CONST               'Error is too high: %f > %f'
              496  LOAD_FAST             9  'tot_err'
              499  LOAD_FAST             4  'stbf'
              502  LOAD_ATTR            17  'error'
              505  BUILD_TUPLE_2         2 
              508  BINARY_MODULO    
              509  RAISE_VARARGS_2       2  None
              512  POP_BLOCK        
              513  LOAD_CONST               None
            516_0  COME_FROM_WITH      388  '388'
              516  WITH_CLEANUP     
              517  END_FINALLY      

 L.  95       518  SETUP_EXCEPT         59  'to 580'

 L.  96       521  LOAD_FAST             3  'T'
              524  LOAD_GLOBAL          14  'time'
              527  LOAD_ATTR            14  'time'
              530  CALL_FUNCTION_0       0  None
              533  LOAD_FAST             7  'last_insert'
              536  BINARY_SUBTRACT  
              537  BINARY_SUBTRACT  
              538  LOAD_CONST               1
              541  BINARY_ADD       
              542  STORE_FAST           10  't'

 L.  97       545  LOAD_FAST            10  't'
              548  LOAD_CONST               0
              551  COMPARE_OP            4  >
              554  POP_JUMP_IF_FALSE   576  'to 576'

 L.  98       557  LOAD_FAST             0  'self'
              560  LOAD_ATTR            18  'wait'
              563  LOAD_CONST               'timeout'
              566  LOAD_FAST            10  't'
              569  CALL_FUNCTION_256   256  None
              572  POP_TOP          
              573  JUMP_FORWARD          0  'to 576'
            576_0  COME_FROM           573  '573'
              576  POP_BLOCK        
              577  JUMP_FORWARD          7  'to 587'
            580_0  COME_FROM           518  '518'

 L.  99       580  POP_TOP          
              581  POP_TOP          
              582  POP_TOP          

 L. 100       583  JUMP_FORWARD          1  'to 587'
              586  END_FINALLY      
            587_0  COME_FROM           586  '586'
            587_1  COME_FROM           577  '577'

 L. 102       587  LOAD_CONST               'State of blooms: %d blooms with expected error %.2f%%'
              590  LOAD_GLOBAL           8  'len'
              593  LOAD_FAST             4  'stbf'
              596  LOAD_ATTR             9  'blooms'
              599  CALL_FUNCTION_1       1  None
              602  LOAD_FAST             4  'stbf'
              605  LOAD_ATTR            10  'expected_error'
              608  CALL_FUNCTION_0       0  None
              611  LOAD_CONST               100.0
              614  BINARY_MULTIPLY  
              615  BUILD_TUPLE_2         2 
              618  BINARY_MODULO    
              619  PRINT_ITEM       
              620  PRINT_NEWLINE_CONT

 L. 104       621  LOAD_GLOBAL           1  'TimingBlock'
              624  LOAD_CONST               'Testing %d expired values'
              627  LOAD_FAST             2  'N'
              630  BINARY_MODULO    
              631  LOAD_FAST             2  'N'
              634  CALL_FUNCTION_2       2  None
              637  SETUP_WITH          118  'to 758'
              640  POP_TOP          

 L. 105       641  LOAD_CONST               0
              644  STORE_FAST            8  'err'

 L. 106       647  SETUP_LOOP           51  'to 701'
              650  LOAD_GLOBAL          11  'xrange'
              653  LOAD_FAST             2  'N'
              656  CALL_FUNCTION_1       1  None
              659  GET_ITER         
              660  FOR_ITER             37  'to 700'
              663  STORE_FAST            6  'i'

 L. 107       666  LOAD_GLOBAL          13  'str'
              669  LOAD_FAST             6  'i'
              672  CALL_FUNCTION_1       1  None
              675  LOAD_FAST             4  'stbf'
              678  COMPARE_OP            6  in
              681  POP_JUMP_IF_FALSE   660  'to 660'

 L. 108       684  LOAD_FAST             8  'err'
              687  LOAD_CONST               1
              690  INPLACE_ADD      
              691  STORE_FAST            8  'err'
              694  JUMP_BACK           660  'to 660'
              697  JUMP_BACK           660  'to 660'
              700  POP_BLOCK        
            701_0  COME_FROM           647  '647'

 L. 109       701  LOAD_FAST             8  'err'
              704  LOAD_GLOBAL          16  'float'
              707  LOAD_FAST             2  'N'
              710  CALL_FUNCTION_1       1  None
              713  BINARY_DIVIDE    
              714  STORE_FAST            9  'tot_err'

 L. 110       717  LOAD_FAST             9  'tot_err'
              720  LOAD_FAST             4  'stbf'
              723  LOAD_ATTR            17  'error'
              726  COMPARE_OP            1  <=
              729  POP_JUMP_IF_TRUE    754  'to 754'
              732  LOAD_ASSERT              AssertionError
              735  LOAD_CONST               'Error is too high: %f > %f'
              738  LOAD_FAST             9  'tot_err'
              741  LOAD_FAST             4  'stbf'
              744  LOAD_ATTR            17  'error'
              747  BUILD_TUPLE_2         2 
              750  BINARY_MODULO    
              751  RAISE_VARARGS_2       2  None
              754  POP_BLOCK        
              755  LOAD_CONST               None
            758_0  COME_FROM_WITH      637  '637'
              758  WITH_CLEANUP     
              759  END_FINALLY      

 L. 112       760  LOAD_FAST             4  'stbf'
              763  LOAD_ATTR             4  'decay'
              766  CALL_FUNCTION_0       0  None
              769  POP_TOP          

 L. 113       770  LOAD_GLOBAL           8  'len'
              773  LOAD_FAST             4  'stbf'
              776  LOAD_ATTR             9  'blooms'
              779  CALL_FUNCTION_1       1  None
              782  LOAD_CONST               0
              785  COMPARE_OP            2  ==
              788  POP_JUMP_IF_TRUE    813  'to 813'
              791  LOAD_ASSERT              AssertionError
              794  LOAD_CONST               'Decay should have pruned all but one bloom filters: %d blooms left'
              797  LOAD_GLOBAL           8  'len'
              800  LOAD_FAST             4  'stbf'
              803  LOAD_ATTR             9  'blooms'
              806  CALL_FUNCTION_1       1  None
              809  BINARY_MODULO    
              810  RAISE_VARARGS_2       2  None

 L. 115       813  LOAD_FAST             4  'stbf'
              816  LOAD_ATTR            12  'add'
              819  LOAD_CONST               'test'
              822  CALL_FUNCTION_1       1  None
              825  POP_TOP          

 L. 116       826  LOAD_CONST               'test'
              829  LOAD_FAST             4  'stbf'
              832  COMPARE_OP            6  in
              835  POP_JUMP_IF_TRUE    844  'to 844'
              838  LOAD_ASSERT              AssertionError
              841  RAISE_VARARGS_1       1  None

Parse error at or near `POP_BLOCK' instruction at offset 512