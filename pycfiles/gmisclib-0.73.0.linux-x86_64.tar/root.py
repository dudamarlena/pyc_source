# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/root.py
# Compiled at: 2009-10-31 07:08:16
"""Solve a 1-dimensional equation to find the roots.
This does alternating secant and bisection steps.
It will work for any function, discontinuous or not.
For a nasty function, it might be a factor of 2 slower
than bisection, but for a nearly-linear function,
it can be much faster than bisection.
"""

def _root1--- This code section failed: ---

 L.  13         0  LOAD_FAST             6  'epsx'
                3  LOAD_CONST               0.0
                6  COMPARE_OP            4  >
                9  POP_JUMP_IF_TRUE     18  'to 18'
               12  LOAD_ASSERT              AssertionError
               15  RAISE_VARARGS_1       1  None

 L.  14        18  LOAD_FAST             7  'epsf'
               21  LOAD_CONST               0.0
               24  COMPARE_OP            5  >=
               27  POP_JUMP_IF_TRUE     36  'to 36'
               30  LOAD_ASSERT              AssertionError
               33  RAISE_VARARGS_1       1  None

 L.  15        36  LOAD_FAST             2  'xh'
               39  LOAD_FAST             1  'xl'
               42  COMPARE_OP            4  >
               45  POP_JUMP_IF_TRUE     54  'to 54'
               48  LOAD_ASSERT              AssertionError
               51  RAISE_VARARGS_1       1  None

 L.  16        54  LOAD_FAST             5  'fh'
               57  LOAD_CONST               0
               60  COMPARE_OP            4  >
               63  LOAD_FAST             4  'fl'
               66  LOAD_CONST               0
               69  COMPARE_OP            4  >
               72  COMPARE_OP            3  !=
               75  POP_JUMP_IF_TRUE     84  'to 84'
               78  LOAD_ASSERT              AssertionError
               81  RAISE_VARARGS_1       1  None

 L.  17        84  LOAD_FAST             2  'xh'
               87  LOAD_FAST             1  'xl'
               90  BINARY_SUBTRACT  
               91  LOAD_FAST             6  'epsx'
               94  COMPARE_OP            1  <=
               97  POP_JUMP_IF_FALSE   247  'to 247'

 L.  18       100  LOAD_FAST             1  'xl'
              103  LOAD_FAST             2  'xh'
              106  COMPARE_OP            1  <=
              109  POP_JUMP_IF_TRUE    131  'to 131'
              112  LOAD_ASSERT              AssertionError
              115  LOAD_CONST               'Not xl=%.15g <= xh=%.15g'
              118  LOAD_FAST             1  'xl'
              121  LOAD_FAST             2  'xh'
              124  BUILD_TUPLE_2         2 
              127  BINARY_MODULO    
              128  RAISE_VARARGS_2       2  None

 L.  19       131  LOAD_FAST             4  'fl'
              134  LOAD_FAST             5  'fh'
              137  BINARY_SUBTRACT  
              138  LOAD_CONST               0.0
              141  COMPARE_OP            2  ==
              144  POP_JUMP_IF_FALSE   168  'to 168'

 L.  20       147  LOAD_FAST             1  'xl'
              150  LOAD_CONST               0.5
              153  LOAD_FAST             2  'xh'
              156  LOAD_FAST             1  'xl'
              159  BINARY_SUBTRACT  
              160  BINARY_MULTIPLY  
              161  BINARY_ADD       
              162  STORE_FAST            8  'tmp'
              165  JUMP_FORWARD         26  'to 194'

 L.  22       168  LOAD_FAST             1  'xl'
              171  LOAD_FAST             1  'xl'
              174  LOAD_FAST             2  'xh'
              177  BINARY_SUBTRACT  
              178  LOAD_FAST             4  'fl'
              181  BINARY_MULTIPLY  
              182  LOAD_FAST             5  'fh'
              185  LOAD_FAST             4  'fl'
              188  BINARY_SUBTRACT  
              189  BINARY_DIVIDE    
              190  BINARY_ADD       
              191  STORE_FAST            8  'tmp'
            194_0  COME_FROM           165  '165'

 L.  23       194  LOAD_FAST             1  'xl'
              197  LOAD_FAST             8  'tmp'
              200  DUP_TOP          
              201  ROT_THREE        
              202  COMPARE_OP            0  <
              205  JUMP_IF_FALSE_OR_POP   217  'to 217'
              208  LOAD_FAST             2  'xh'
              211  COMPARE_OP            0  <
              214  JUMP_FORWARD          2  'to 219'
            217_0  COME_FROM           205  '205'
              217  ROT_TWO          
              218  POP_TOP          
            219_0  COME_FROM           214  '214'
              219  POP_JUMP_IF_TRUE    243  'to 243'

 L.  24       222  LOAD_FAST             1  'xl'
              225  LOAD_CONST               0.5
              228  LOAD_FAST             2  'xh'
              231  LOAD_FAST             1  'xl'
              234  BINARY_SUBTRACT  
              235  BINARY_MULTIPLY  
              236  BINARY_ADD       
              237  STORE_FAST            8  'tmp'
              240  JUMP_FORWARD          0  'to 243'
            243_0  COME_FROM           240  '240'

 L.  25       243  LOAD_FAST             8  'tmp'
              246  RETURN_VALUE     
            247_0  COME_FROM            97  '97'

 L.  26       247  LOAD_GLOBAL           1  'abs'
              250  LOAD_FAST             4  'fl'
              253  CALL_FUNCTION_1       1  None
              256  LOAD_FAST             7  'epsf'
              259  COMPARE_OP            1  <=
              262  POP_JUMP_IF_FALSE   269  'to 269'

 L.  27       265  LOAD_FAST             1  'xl'
              268  RETURN_END_IF    
            269_0  COME_FROM           262  '262'

 L.  28       269  LOAD_GLOBAL           1  'abs'
              272  LOAD_FAST             5  'fh'
              275  CALL_FUNCTION_1       1  None
              278  LOAD_FAST             7  'epsf'
              281  COMPARE_OP            1  <=
              284  POP_JUMP_IF_FALSE   291  'to 291'

 L.  29       287  LOAD_FAST             2  'xh'
              290  RETURN_END_IF    
            291_0  COME_FROM           284  '284'

 L.  31       291  LOAD_FAST             1  'xl'
              294  LOAD_FAST             2  'xh'
              297  COMPARE_OP            0  <
              300  POP_JUMP_IF_TRUE    309  'to 309'
              303  LOAD_ASSERT              AssertionError
              306  RAISE_VARARGS_1       1  None

 L.  32       309  LOAD_FAST             1  'xl'
              312  LOAD_FAST             4  'fl'
              315  BUILD_TUPLE_2         2 
              318  LOAD_FAST             2  'xh'
              321  LOAD_FAST             5  'fh'
              324  BUILD_TUPLE_2         2 
              327  BUILD_LIST_2          2 
              330  STORE_FAST            9  'q'

 L.  35       333  LOAD_FAST             5  'fh'
              336  LOAD_CONST               0
              339  COMPARE_OP            4  >
              342  LOAD_FAST             4  'fl'
              345  LOAD_CONST               0
              348  COMPARE_OP            4  >
              351  COMPARE_OP            3  !=
              354  POP_JUMP_IF_FALSE   369  'to 369'
              357  LOAD_FAST             5  'fh'
              360  LOAD_FAST             4  'fl'
              363  COMPARE_OP            3  !=
            366_0  COME_FROM           354  '354'
              366  POP_JUMP_IF_TRUE    375  'to 375'
              369  LOAD_ASSERT              AssertionError
              372  RAISE_VARARGS_1       1  None

 L.  36       375  LOAD_FAST             1  'xl'
              378  LOAD_FAST             5  'fh'
              381  BINARY_MULTIPLY  
              382  LOAD_FAST             2  'xh'
              385  LOAD_FAST             4  'fl'
              388  BINARY_MULTIPLY  
              389  BINARY_SUBTRACT  
              390  LOAD_FAST             5  'fh'
              393  LOAD_FAST             4  'fl'
              396  BINARY_SUBTRACT  
              397  BINARY_DIVIDE    
              398  STORE_FAST           10  'xsec'

 L.  37       401  LOAD_FAST             1  'xl'
              404  LOAD_FAST            10  'xsec'
              407  DUP_TOP          
              408  ROT_THREE        
              409  COMPARE_OP            0  <
              412  JUMP_IF_FALSE_OR_POP   424  'to 424'
              415  LOAD_FAST             2  'xh'
              418  COMPARE_OP            0  <
              421  JUMP_FORWARD          2  'to 426'
            424_0  COME_FROM           412  '412'
              424  ROT_TWO          
              425  POP_TOP          
            426_0  COME_FROM           421  '421'
              426  POP_JUMP_IF_FALSE   575  'to 575'

 L.  38       429  LOAD_FAST             0  'f'
              432  LOAD_FAST            10  'xsec'
              435  LOAD_FAST             3  'p'
              438  CALL_FUNCTION_2       2  None
              441  STORE_FAST           11  'fsec'

 L.  39       444  LOAD_FAST            11  'fsec'
              447  LOAD_CONST               0
              450  COMPARE_OP            2  ==
              453  POP_JUMP_IF_FALSE   460  'to 460'

 L.  40       456  LOAD_FAST            10  'xsec'
              459  RETURN_END_IF    
            460_0  COME_FROM           453  '453'

 L.  41       460  LOAD_FAST            11  'fsec'
              463  LOAD_CONST               0
              466  COMPARE_OP            4  >
              469  POP_JUMP_IF_TRUE    490  'to 490'
              472  LOAD_FAST            11  'fsec'
              475  LOAD_CONST               0
              478  COMPARE_OP            0  <
              481  POP_JUMP_IF_TRUE    490  'to 490'
              484  LOAD_ASSERT              AssertionError
              487  RAISE_VARARGS_1       1  None

 L.  42       490  LOAD_FAST             9  'q'
              493  LOAD_ATTR             2  'append'
              496  LOAD_FAST            10  'xsec'
              499  LOAD_FAST            11  'fsec'
              502  BUILD_TUPLE_2         2 
              505  CALL_FUNCTION_1       1  None
              508  POP_TOP          

 L.  44       509  LOAD_FAST            11  'fsec'
              512  LOAD_CONST               0
              515  COMPARE_OP            4  >
              518  LOAD_FAST             4  'fl'
              521  LOAD_CONST               0
              524  COMPARE_OP            4  >
              527  COMPARE_OP            2  ==
              530  POP_JUMP_IF_FALSE   554  'to 554'

 L.  45       533  LOAD_FAST            10  'xsec'
              536  LOAD_FAST             2  'xh'
              539  LOAD_FAST            10  'xsec'
              542  BINARY_SUBTRACT  
              543  LOAD_CONST               0.5
              546  BINARY_MULTIPLY  
              547  BINARY_ADD       
              548  STORE_FAST           12  'xbi'
              551  JUMP_ABSOLUTE       593  'to 593'

 L.  47       554  LOAD_FAST            10  'xsec'
              557  LOAD_FAST             1  'xl'
              560  LOAD_FAST            10  'xsec'
              563  BINARY_SUBTRACT  
              564  LOAD_CONST               0.5
              567  BINARY_MULTIPLY  
              568  BINARY_ADD       
              569  STORE_FAST           12  'xbi'
              572  JUMP_FORWARD         18  'to 593'

 L.  49       575  LOAD_FAST             1  'xl'
              578  LOAD_CONST               0.5
              581  LOAD_FAST             2  'xh'
              584  LOAD_FAST             1  'xl'
              587  BINARY_SUBTRACT  
              588  BINARY_MULTIPLY  
              589  BINARY_ADD       
              590  STORE_FAST           12  'xbi'
            593_0  COME_FROM           572  '572'

 L.  53       593  LOAD_FAST             1  'xl'
              596  LOAD_FAST            12  'xbi'
              599  DUP_TOP          
              600  ROT_THREE        
              601  COMPARE_OP            1  <=
              604  JUMP_IF_FALSE_OR_POP   616  'to 616'
              607  LOAD_FAST             2  'xh'
              610  COMPARE_OP            1  <=
              613  JUMP_FORWARD          2  'to 618'
            616_0  COME_FROM           604  '604'
              616  ROT_TWO          
              617  POP_TOP          
            618_0  COME_FROM           613  '613'
              618  POP_JUMP_IF_TRUE    643  'to 643'
              621  LOAD_ASSERT              AssertionError
              624  LOAD_CONST               'Not xl=%.15g <= xbi=%.15g <= xh=%.15g'
              627  LOAD_FAST             1  'xl'
              630  LOAD_FAST            12  'xbi'
              633  LOAD_FAST             2  'xh'
              636  BUILD_TUPLE_3         3 
              639  BINARY_MODULO    
              640  RAISE_VARARGS_2       2  None

 L.  54       643  LOAD_FAST             1  'xl'
              646  LOAD_FAST            12  'xbi'
              649  DUP_TOP          
              650  ROT_THREE        
              651  COMPARE_OP            0  <
              654  JUMP_IF_FALSE_OR_POP   666  'to 666'
              657  LOAD_FAST             2  'xh'
              660  COMPARE_OP            0  <
              663  JUMP_FORWARD          2  'to 668'
            666_0  COME_FROM           654  '654'
              666  ROT_TWO          
              667  POP_TOP          
            668_0  COME_FROM           663  '663'
              668  POP_JUMP_IF_FALSE   766  'to 766'
              671  LOAD_FAST            12  'xbi'
              674  LOAD_FAST            10  'xsec'
              677  COMPARE_OP            3  !=
            680_0  COME_FROM           668  '668'
              680  POP_JUMP_IF_FALSE   766  'to 766'

 L.  55       683  LOAD_FAST             0  'f'
              686  LOAD_FAST            12  'xbi'
              689  LOAD_FAST             3  'p'
              692  CALL_FUNCTION_2       2  None
              695  STORE_FAST           13  'fbi'

 L.  56       698  LOAD_FAST            13  'fbi'
              701  LOAD_CONST               0
              704  COMPARE_OP            2  ==
              707  POP_JUMP_IF_FALSE   714  'to 714'

 L.  57       710  LOAD_FAST            12  'xbi'
              713  RETURN_END_IF    
            714_0  COME_FROM           707  '707'

 L.  58       714  LOAD_FAST            13  'fbi'
              717  LOAD_CONST               0
              720  COMPARE_OP            4  >
              723  POP_JUMP_IF_TRUE    744  'to 744'
              726  LOAD_FAST            13  'fbi'
              729  LOAD_CONST               0
              732  COMPARE_OP            0  <
              735  POP_JUMP_IF_TRUE    744  'to 744'
              738  LOAD_ASSERT              AssertionError
              741  RAISE_VARARGS_1       1  None

 L.  59       744  LOAD_FAST             9  'q'
              747  LOAD_ATTR             2  'append'
              750  LOAD_FAST            12  'xbi'
              753  LOAD_FAST            13  'fbi'
              756  BUILD_TUPLE_2         2 
              759  CALL_FUNCTION_1       1  None
              762  POP_TOP          
              763  JUMP_FORWARD          0  'to 766'
            766_0  COME_FROM           763  '763'

 L.  61       766  LOAD_GLOBAL           3  'len'
              769  LOAD_FAST             9  'q'
              772  CALL_FUNCTION_1       1  None
              775  LOAD_CONST               2
              778  COMPARE_OP            1  <=
              781  POP_JUMP_IF_FALSE   796  'to 796'

 L.  64       784  LOAD_CONST               0.5
              787  LOAD_FAST             1  'xl'
              790  LOAD_FAST             2  'xh'
              793  BINARY_ADD       
              794  BINARY_MULTIPLY  
              795  RETURN_END_IF    
            796_0  COME_FROM           781  '781'

 L.  66       796  LOAD_FAST             9  'q'
              799  LOAD_ATTR             4  'sort'
              802  CALL_FUNCTION_0       0  None
              805  POP_TOP          

 L.  68       806  LOAD_CONST               0
              809  STORE_FAST           14  'X'

 L.  69       812  LOAD_CONST               1
              815  STORE_FAST           15  'F'

 L.  71       818  SETUP_LOOP          182  'to 1003'
              821  LOAD_GLOBAL           5  'range'
              824  LOAD_CONST               1
              827  LOAD_GLOBAL           3  'len'
              830  LOAD_FAST             9  'q'
              833  CALL_FUNCTION_1       1  None
              836  CALL_FUNCTION_2       2  None
              839  GET_ITER         
              840  FOR_ITER            159  'to 1002'
              843  STORE_FAST           16  'i'

 L.  72       846  LOAD_FAST             9  'q'
              849  LOAD_FAST            16  'i'
              852  BINARY_SUBSCR    
              853  LOAD_FAST            14  'X'
              856  BINARY_SUBSCR    
              857  LOAD_FAST             9  'q'
              860  LOAD_FAST            16  'i'
              863  LOAD_CONST               1
              866  BINARY_SUBTRACT  
              867  BINARY_SUBSCR    
              868  LOAD_FAST            14  'X'
              871  BINARY_SUBSCR    
              872  COMPARE_OP            3  !=
              875  POP_JUMP_IF_TRUE    884  'to 884'
              878  LOAD_ASSERT              AssertionError
              881  RAISE_VARARGS_1       1  None

 L.  73       884  LOAD_FAST             9  'q'
              887  LOAD_FAST            16  'i'
              890  BINARY_SUBSCR    
              891  LOAD_FAST            15  'F'
              894  BINARY_SUBSCR    
              895  LOAD_CONST               0
              898  COMPARE_OP            4  >
              901  LOAD_FAST             9  'q'
              904  LOAD_FAST            16  'i'
              907  LOAD_CONST               1
              910  BINARY_SUBTRACT  
              911  BINARY_SUBSCR    
              912  LOAD_FAST            15  'F'
              915  BINARY_SUBSCR    
              916  LOAD_CONST               0
              919  COMPARE_OP            4  >
              922  COMPARE_OP            3  !=
              925  POP_JUMP_IF_FALSE   840  'to 840'

 L.  74       928  LOAD_GLOBAL           6  '_root1'
              931  LOAD_FAST             0  'f'
              934  LOAD_FAST             9  'q'
              937  LOAD_FAST            16  'i'
              940  LOAD_CONST               1
              943  BINARY_SUBTRACT  
              944  BINARY_SUBSCR    
              945  LOAD_FAST            14  'X'
              948  BINARY_SUBSCR    
              949  LOAD_FAST             9  'q'
              952  LOAD_FAST            16  'i'
              955  BINARY_SUBSCR    
              956  LOAD_FAST            14  'X'
              959  BINARY_SUBSCR    
              960  LOAD_FAST             3  'p'
              963  LOAD_FAST             9  'q'
              966  LOAD_FAST            16  'i'
              969  LOAD_CONST               1
              972  BINARY_SUBTRACT  
              973  BINARY_SUBSCR    
              974  LOAD_FAST            15  'F'
              977  BINARY_SUBSCR    
              978  LOAD_FAST             9  'q'
              981  LOAD_FAST            16  'i'
              984  BINARY_SUBSCR    
              985  LOAD_FAST            15  'F'
              988  BINARY_SUBSCR    
              989  LOAD_FAST             6  'epsx'
              992  LOAD_FAST             7  'epsf'
              995  CALL_FUNCTION_8       8  None
              998  RETURN_END_IF    
            999_0  COME_FROM           925  '925'
              999  JUMP_BACK           840  'to 840'
             1002  POP_BLOCK        
           1003_0  COME_FROM           818  '818'

 L.  75      1003  LOAD_GLOBAL           7  'RuntimeError'
             1006  LOAD_CONST               'Lost a root: %s'
             1009  LOAD_GLOBAL           8  'repr'
             1012  LOAD_FAST             9  'q'
             1015  CALL_FUNCTION_1       1  None
             1018  BINARY_MODULO    
             1019  RAISE_VARARGS_2       2  None

Parse error at or near `BINARY_MODULO' instruction at offset 1018


def root--- This code section failed: ---

 L.  90         0  LOAD_FAST             2  'xh'
                3  LOAD_FAST             1  'xl'
                6  COMPARE_OP            0  <
                9  POP_JUMP_IF_FALSE    16  'to 16'

 L.  91        12  LOAD_CONST               None
               15  RETURN_END_IF    
             16_0  COME_FROM             9  '9'

 L.  92        16  LOAD_FAST             0  'f'
               19  LOAD_FAST             1  'xl'
               22  LOAD_FAST             3  'p'
               25  CALL_FUNCTION_2       2  None
               28  STORE_FAST            6  'fl'

 L.  93        31  LOAD_FAST             6  'fl'
               34  LOAD_CONST               0
               37  COMPARE_OP            2  ==
               40  POP_JUMP_IF_FALSE    47  'to 47'

 L.  94        43  LOAD_FAST             1  'xl'
               46  RETURN_END_IF    
             47_0  COME_FROM            40  '40'

 L.  95        47  LOAD_FAST             0  'f'
               50  LOAD_FAST             2  'xh'
               53  LOAD_FAST             3  'p'
               56  CALL_FUNCTION_2       2  None
               59  STORE_FAST            7  'fh'

 L.  96        62  LOAD_FAST             7  'fh'
               65  LOAD_CONST               0
               68  COMPARE_OP            2  ==
               71  POP_JUMP_IF_FALSE    78  'to 78'

 L.  97        74  LOAD_FAST             2  'xh'
               77  RETURN_END_IF    
             78_0  COME_FROM            71  '71'

 L.  98        78  LOAD_FAST             2  'xh'
               81  LOAD_FAST             1  'xl'
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_FALSE    94  'to 94'

 L.  99        90  LOAD_CONST               None
               93  RETURN_END_IF    
             94_0  COME_FROM            87  '87'

 L. 102        94  LOAD_FAST             6  'fl'
               97  LOAD_CONST               0
              100  COMPARE_OP            4  >
              103  LOAD_FAST             7  'fh'
              106  LOAD_CONST               0
              109  COMPARE_OP            4  >
              112  COMPARE_OP            3  !=
              115  POP_JUMP_IF_TRUE    127  'to 127'
              118  LOAD_ASSERT              AssertionError
              121  LOAD_CONST               '0 or an even number of roots in initial x-range.'
              124  RAISE_VARARGS_2       2  None

 L. 103       127  LOAD_GLOBAL           2  '_root1'
              130  LOAD_FAST             0  'f'
              133  LOAD_FAST             1  'xl'
              136  LOAD_FAST             2  'xh'
              139  LOAD_FAST             3  'p'
              142  LOAD_FAST             6  'fl'
              145  LOAD_FAST             7  'fh'
              148  LOAD_FAST             4  'epsx'
              151  LOAD_FAST             5  'epsf'
              154  CALL_FUNCTION_8       8  None
              157  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_8' instruction at offset 154


def _test1f(x, p):
    return 100 / int(round(x)) - 10


def test():
    q = root(_test1f, 1, 1000, None, 1e-06, 0.01)
    assert _test1f(q, None) == 0
    q = root(_test1f, 1, 16, None, 1e-06, 0.01)
    assert _test1f(q, None) == 0
    return


def iroot(y, xl, xh, epsy=0.0):
    """Find a zero in an array y.
        This function assumes there is known to be a root in [xl,xh].
        It returns a real-number index into the array which
        linearly interpolates to zero.
        """
    import math
    assert 0 <= xl < y.shape[0]
    assert 0 <= xh < y.shape[0]

    def interp(x, y):
        xi = math.floor(x)
        frac = x - xi
        i = int(xi)
        if frac > 0:
            return y[i] + (y[(i + 1)] - y[i]) * frac
        return y[i]

    return root(interp, xl, xh, y, 0.001, epsy)


def testi():
    import Num
    y = 0.64234 * (Num.arange(100) - 32.234)
    assert abs(iroot(y, 10, 50) - 32.234) < 0.002


if __name__ == '__main__':
    test()
    testi()