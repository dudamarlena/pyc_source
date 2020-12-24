# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/fuggetaboutit/tests/test_timing_bloom_filter.py
# Compiled at: 2013-11-19 17:15:53
from fuggetaboutit.timing_bloom_filter import TimingBloomFilter, _ENTRIES_PER_8BYTE
import tornado.ioloop, tornado.testing, time
from fuggetaboutit.utils import TimingBlock, TestFile

class TestTimingBloomFilter(tornado.testing.AsyncTestCase):

    def test_decay(self):
        tbf = TimingBloomFilter(500, decay_time=4, ioloop=self.io_loop).start()
        tbf += 'hello'
        assert tbf.contains('hello') == True
        try:
            self.wait(timeout=4)
        except:
            pass

        assert tbf.contains('hello') == False

    def test_optimization_size(self):
        tbf = TimingBloomFilter(500, decay_time=4, ioloop=self.io_loop)
        assert _ENTRIES_PER_8BYTE == 2
        assert len(tbf.data) < tbf.num_bytes

    def test_save(self):
        tbf = TimingBloomFilter(5, decay_time=30, ioloop=self.io_loop).start()
        tbf += 'hello'
        assert 'hello' in tbf
        prev_num_nonzero = tbf.num_non_zero
        tbf.tofile(open('test.tbf', 'w+'))
        with TestFile('test.tbf') as (fd):
            tbf2 = TimingBloomFilter.fromfile(fd)
        assert 'hello' in tbf
        assert prev_num_nonzero == tbf2.num_non_zero

    def test_holistic--- This code section failed: ---

 L.  42         0  LOAD_GLOBAL           0  'int'
                3  LOAD_CONST               20000.0
                6  CALL_FUNCTION_1       1  None
                9  STORE_FAST            1  'n'

 L.  43        12  LOAD_GLOBAL           0  'int'
               15  LOAD_CONST               10000.0
               18  CALL_FUNCTION_1       1  None
               21  STORE_FAST            2  'N'

 L.  44        24  LOAD_CONST               3
               27  STORE_FAST            3  'T'

 L.  45        30  LOAD_CONST               'TimingBloom with capacity %e and expiration time %ds'
               33  LOAD_FAST             1  'n'
               36  LOAD_FAST             3  'T'
               39  BUILD_TUPLE_2         2 
               42  BINARY_MODULO    
               43  PRINT_ITEM       
               44  PRINT_NEWLINE_CONT

 L.  47        45  LOAD_GLOBAL           1  'TimingBlock'
               48  LOAD_CONST               'Initialization'
               51  CALL_FUNCTION_1       1  None
               54  SETUP_WITH           32  'to 89'
               57  POP_TOP          

 L.  48        58  LOAD_GLOBAL           2  'TimingBloomFilter'
               61  LOAD_FAST             1  'n'
               64  LOAD_CONST               'decay_time'
               67  LOAD_FAST             3  'T'
               70  LOAD_CONST               'ioloop'
               73  LOAD_FAST             0  'self'
               76  LOAD_ATTR             3  'io_loop'
               79  CALL_FUNCTION_513   513  None
               82  STORE_FAST            4  'tbf'
               85  POP_BLOCK        
               86  LOAD_CONST               None
             89_0  COME_FROM_WITH       54  '54'
               89  WITH_CLEANUP     
               90  END_FINALLY      

 L.  50        91  LOAD_FAST             4  'tbf'
               94  LOAD_ATTR             4  'decay'
               97  STORE_DEREF           0  'orig_decay'

 L.  51       100  LOAD_CLOSURE          0  'orig_decay'
              106  LOAD_CODE                <code_object new_decay>
              109  MAKE_CLOSURE_0        0  None
              112  STORE_FAST            5  'new_decay'

 L.  55       115  LOAD_GLOBAL           5  'setattr'
              118  LOAD_FAST             4  'tbf'
              121  LOAD_CONST               'decay'
              124  LOAD_FAST             5  'new_decay'
              127  CALL_FUNCTION_3       3  None
              130  POP_TOP          

 L.  56       131  LOAD_FAST             4  'tbf'
              134  LOAD_ATTR             6  '_setup_decay'
              137  CALL_FUNCTION_0       0  None
              140  POP_TOP          

 L.  57       141  LOAD_FAST             4  'tbf'
              144  LOAD_ATTR             7  'start'
              147  CALL_FUNCTION_0       0  None
              150  POP_TOP          

 L.  59       151  LOAD_CONST               'num_hashes = %d, num_bytes = %d'
              154  LOAD_FAST             4  'tbf'
              157  LOAD_ATTR             8  'num_hashes'
              160  LOAD_FAST             4  'tbf'
              163  LOAD_ATTR             9  'num_bytes'
              166  BUILD_TUPLE_2         2 
              169  BINARY_MODULO    
              170  PRINT_ITEM       
              171  PRINT_NEWLINE_CONT

 L.  60       172  LOAD_CONST               'sizeof(TimingBloom) = %d bytes'
              175  LOAD_FAST             4  'tbf'
              178  LOAD_ATTR             9  'num_bytes'
              181  BINARY_MODULO    
              182  PRINT_ITEM       
              183  PRINT_NEWLINE_CONT

 L.  62       184  LOAD_GLOBAL           1  'TimingBlock'
              187  LOAD_CONST               'Adding %d values'
              190  LOAD_FAST             2  'N'
              193  BINARY_MODULO    
              194  LOAD_FAST             2  'N'
              197  CALL_FUNCTION_2       2  None
              200  SETUP_WITH           47  'to 250'
              203  POP_TOP          

 L.  63       204  SETUP_LOOP           39  'to 246'
              207  LOAD_GLOBAL          10  'xrange'
              210  LOAD_FAST             2  'N'
              213  CALL_FUNCTION_1       1  None
              216  GET_ITER         
              217  FOR_ITER             25  'to 245'
              220  STORE_FAST            6  'i'

 L.  64       223  LOAD_FAST             4  'tbf'
              226  LOAD_ATTR            11  'add'
              229  LOAD_GLOBAL          12  'str'
              232  LOAD_FAST             6  'i'
              235  CALL_FUNCTION_1       1  None
              238  CALL_FUNCTION_1       1  None
              241  POP_TOP          
              242  JUMP_BACK           217  'to 217'
              245  POP_BLOCK        
            246_0  COME_FROM           204  '204'
              246  POP_BLOCK        
              247  LOAD_CONST               None
            250_0  COME_FROM_WITH      200  '200'
              250  WITH_CLEANUP     
              251  END_FINALLY      

 L.  65       252  LOAD_GLOBAL          13  'time'
              255  LOAD_ATTR            13  'time'
              258  CALL_FUNCTION_0       0  None
              261  STORE_FAST            7  'last_insert'

 L.  67       264  LOAD_GLOBAL           1  'TimingBlock'
              267  LOAD_CONST               'Testing %d positive values'
              270  LOAD_FAST             2  'N'
              273  BINARY_MODULO    
              274  LOAD_FAST             2  'N'
              277  CALL_FUNCTION_2       2  None
              280  SETUP_WITH           52  'to 335'
              283  POP_TOP          

 L.  68       284  SETUP_LOOP           44  'to 331'
              287  LOAD_GLOBAL          10  'xrange'
              290  LOAD_FAST             2  'N'
              293  CALL_FUNCTION_1       1  None
              296  GET_ITER         
              297  FOR_ITER             30  'to 330'
              300  STORE_FAST            6  'i'

 L.  69       303  LOAD_GLOBAL          12  'str'
              306  LOAD_FAST             6  'i'
              309  CALL_FUNCTION_1       1  None
              312  LOAD_FAST             4  'tbf'
              315  COMPARE_OP            6  in
              318  POP_JUMP_IF_TRUE    297  'to 297'
              321  LOAD_ASSERT              AssertionError
              324  RAISE_VARARGS_1       1  None
              327  JUMP_BACK           297  'to 297'
              330  POP_BLOCK        
            331_0  COME_FROM           284  '284'
              331  POP_BLOCK        
              332  LOAD_CONST               None
            335_0  COME_FROM_WITH      280  '280'
              335  WITH_CLEANUP     
              336  END_FINALLY      

 L.  71       337  LOAD_GLOBAL           1  'TimingBlock'
              340  LOAD_CONST               'Testing %d negative values'
              343  LOAD_FAST             2  'N'
              346  BINARY_MODULO    
              347  LOAD_FAST             2  'N'
              350  CALL_FUNCTION_2       2  None
              353  SETUP_WITH          125  'to 481'
              356  POP_TOP          

 L.  72       357  LOAD_CONST               0
              360  STORE_FAST            8  'err'

 L.  73       363  SETUP_LOOP           58  'to 424'
              366  LOAD_GLOBAL          10  'xrange'
              369  LOAD_FAST             2  'N'
              372  LOAD_CONST               2
              375  LOAD_FAST             2  'N'
              378  BINARY_MULTIPLY  
              379  CALL_FUNCTION_2       2  None
              382  GET_ITER         
              383  FOR_ITER             37  'to 423'
              386  STORE_FAST            6  'i'

 L.  74       389  LOAD_GLOBAL          12  'str'
              392  LOAD_FAST             6  'i'
              395  CALL_FUNCTION_1       1  None
              398  LOAD_FAST             4  'tbf'
              401  COMPARE_OP            6  in
              404  POP_JUMP_IF_FALSE   383  'to 383'

 L.  75       407  LOAD_FAST             8  'err'
              410  LOAD_CONST               1
              413  INPLACE_ADD      
              414  STORE_FAST            8  'err'
              417  JUMP_BACK           383  'to 383'
              420  JUMP_BACK           383  'to 383'
              423  POP_BLOCK        
            424_0  COME_FROM           363  '363'

 L.  76       424  LOAD_FAST             8  'err'
              427  LOAD_GLOBAL          15  'float'
              430  LOAD_FAST             2  'N'
              433  CALL_FUNCTION_1       1  None
              436  BINARY_DIVIDE    
              437  STORE_FAST            9  'tot_err'

 L.  77       440  LOAD_FAST             9  'tot_err'
              443  LOAD_FAST             4  'tbf'
              446  LOAD_ATTR            16  'error'
              449  COMPARE_OP            1  <=
              452  POP_JUMP_IF_TRUE    477  'to 477'
              455  LOAD_ASSERT              AssertionError
              458  LOAD_CONST               'Error is too high: %f > %f'
              461  LOAD_FAST             9  'tot_err'
              464  LOAD_FAST             4  'tbf'
              467  LOAD_ATTR            16  'error'
              470  BUILD_TUPLE_2         2 
              473  BINARY_MODULO    
              474  RAISE_VARARGS_2       2  None
              477  POP_BLOCK        
              478  LOAD_CONST               None
            481_0  COME_FROM_WITH      353  '353'
              481  WITH_CLEANUP     
              482  END_FINALLY      

 L.  79       483  SETUP_EXCEPT         59  'to 545'

 L.  80       486  LOAD_FAST             3  'T'
              489  LOAD_GLOBAL          13  'time'
              492  LOAD_ATTR            13  'time'
              495  CALL_FUNCTION_0       0  None
              498  LOAD_FAST             7  'last_insert'
              501  BINARY_SUBTRACT  
              502  BINARY_SUBTRACT  
              503  LOAD_CONST               1
              506  BINARY_ADD       
              507  STORE_FAST           10  't'

 L.  81       510  LOAD_FAST            10  't'
              513  LOAD_CONST               0
              516  COMPARE_OP            4  >
              519  POP_JUMP_IF_FALSE   541  'to 541'

 L.  82       522  LOAD_FAST             0  'self'
              525  LOAD_ATTR            17  'wait'
              528  LOAD_CONST               'timeout'
              531  LOAD_FAST            10  't'
              534  CALL_FUNCTION_256   256  None
              537  POP_TOP          
              538  JUMP_FORWARD          0  'to 541'
            541_0  COME_FROM           538  '538'
              541  POP_BLOCK        
              542  JUMP_FORWARD          7  'to 552'
            545_0  COME_FROM           483  '483'

 L.  83       545  POP_TOP          
              546  POP_TOP          
              547  POP_TOP          

 L.  84       548  JUMP_FORWARD          1  'to 552'
              551  END_FINALLY      
            552_0  COME_FROM           551  '551'
            552_1  COME_FROM           542  '542'

 L.  86       552  LOAD_GLOBAL           1  'TimingBlock'
              555  LOAD_CONST               'Testing %d expired values'
              558  LOAD_FAST             2  'N'
              561  BINARY_MODULO    
              562  LOAD_FAST             2  'N'
              565  CALL_FUNCTION_2       2  None
              568  SETUP_WITH          118  'to 689'
              571  POP_TOP          

 L.  87       572  LOAD_CONST               0
              575  STORE_FAST            8  'err'

 L.  88       578  SETUP_LOOP           51  'to 632'
              581  LOAD_GLOBAL          10  'xrange'
              584  LOAD_FAST             2  'N'
              587  CALL_FUNCTION_1       1  None
              590  GET_ITER         
              591  FOR_ITER             37  'to 631'
              594  STORE_FAST            6  'i'

 L.  89       597  LOAD_GLOBAL          12  'str'
              600  LOAD_FAST             6  'i'
              603  CALL_FUNCTION_1       1  None
              606  LOAD_FAST             4  'tbf'
              609  COMPARE_OP            6  in
              612  POP_JUMP_IF_FALSE   591  'to 591'

 L.  90       615  LOAD_FAST             8  'err'
              618  LOAD_CONST               1
              621  INPLACE_ADD      
              622  STORE_FAST            8  'err'
              625  JUMP_BACK           591  'to 591'
              628  JUMP_BACK           591  'to 591'
              631  POP_BLOCK        
            632_0  COME_FROM           578  '578'

 L.  91       632  LOAD_FAST             8  'err'
              635  LOAD_GLOBAL          15  'float'
              638  LOAD_FAST             2  'N'
              641  CALL_FUNCTION_1       1  None
              644  BINARY_DIVIDE    
              645  STORE_FAST            9  'tot_err'

 L.  92       648  LOAD_FAST             9  'tot_err'
              651  LOAD_FAST             4  'tbf'
              654  LOAD_ATTR            16  'error'
              657  COMPARE_OP            1  <=
              660  POP_JUMP_IF_TRUE    685  'to 685'
              663  LOAD_ASSERT              AssertionError
              666  LOAD_CONST               'Error is too high: %f > %f'
              669  LOAD_FAST             9  'tot_err'
              672  LOAD_FAST             4  'tbf'
              675  LOAD_ATTR            16  'error'
              678  BUILD_TUPLE_2         2 
              681  BINARY_MODULO    
              682  RAISE_VARARGS_2       2  None
              685  POP_BLOCK        
              686  LOAD_CONST               None
            689_0  COME_FROM_WITH      568  '568'
              689  WITH_CLEANUP     
              690  END_FINALLY      

 L.  94       691  LOAD_FAST             4  'tbf'
              694  LOAD_ATTR            18  'num_non_zero'
              697  LOAD_CONST               0
              700  COMPARE_OP            2  ==
              703  POP_JUMP_IF_TRUE    722  'to 722'
              706  LOAD_ASSERT              AssertionError
              709  LOAD_CONST               'All entries in the bloom should be zero: %d non-zero entries'
              712  LOAD_FAST             4  'tbf'
              715  LOAD_ATTR            18  'num_non_zero'
              718  BINARY_MODULO    
              719  RAISE_VARARGS_2       2  None

Parse error at or near `POP_BLOCK' instruction at offset 477