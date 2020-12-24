# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmcS2.py
# Compiled at: 2011-05-11 15:13:54
"""Markov-Chain Monte-Carlo algorithms.

Here, we do MCMC when -log(p) is a sum of squares."""
import mcmcSQ, die, mcmc, g_implements, findleak
_s = None

def go_step--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL           0  'findleak'
                3  LOAD_ATTR             1  'vm'
                6  LOAD_CONST               'go_step start'
                9  CALL_FUNCTION_1       1  None
               12  POP_TOP          

 L.  19        13  LOAD_GLOBAL           2  'g_implements'
               16  LOAD_ATTR             3  'impl'
               19  LOAD_FAST             0  'x'
               22  LOAD_ATTR             4  'current'
               25  CALL_FUNCTION_0       0  None
               28  LOAD_GLOBAL           5  'mcmc'
               31  LOAD_ATTR             6  'position_base'
               34  CALL_FUNCTION_2       2  None
               37  POP_JUMP_IF_TRUE     74  'to 74'
               40  LOAD_ASSERT              AssertionError
               43  LOAD_CONST               'Bad pseudoposition: %s'
               46  LOAD_GLOBAL           2  'g_implements'
               49  LOAD_ATTR             8  'why'
               52  LOAD_FAST             0  'x'
               55  LOAD_ATTR             4  'current'
               58  CALL_FUNCTION_0       0  None
               61  LOAD_GLOBAL           5  'mcmc'
               64  LOAD_ATTR             6  'position_base'
               67  CALL_FUNCTION_2       2  None
               70  BINARY_MODULO    
               71  RAISE_VARARGS_2       2  None

 L.  20        74  LOAD_GLOBAL           9  '_s'
               77  LOAD_CONST               None
               80  COMPARE_OP            8  is
               83  POP_JUMP_IF_FALSE   146  'to 146'

 L.  21        86  LOAD_CONST               'INITIALIZING mcmc'
               89  PRINT_ITEM       
               90  PRINT_NEWLINE_CONT

 L.  22        91  LOAD_GLOBAL           5  'mcmc'
               94  LOAD_ATTR            11  'bootstepper'
               97  LOAD_CONST               None
              100  LOAD_FAST             0  'x'
              103  LOAD_ATTR             4  'current'
              106  CALL_FUNCTION_0       0  None
              109  LOAD_FAST             0  'x'
              112  LOAD_ATTR            12  'archive'
              115  LOAD_ATTR            13  'mvn'
              118  LOAD_ATTR            14  'cov'
              121  LOAD_CONST               None
              124  CALL_FUNCTION_4       4  None
              127  STORE_GLOBAL          9  '_s'

 L.  23       130  LOAD_GLOBAL           0  'findleak'
              133  LOAD_ATTR             1  'vm'
              136  LOAD_CONST               'go_step initialize end'
              139  CALL_FUNCTION_1       1  None
              142  POP_TOP          
              143  JUMP_FORWARD          0  'to 146'
            146_0  COME_FROM           143  '143'

 L.  24       146  LOAD_CONST               'SQ STEP'
              149  PRINT_ITEM       
              150  PRINT_NEWLINE_CONT

 L.  25       151  LOAD_FAST             0  'x'
              154  LOAD_ATTR            15  'step'
              157  LOAD_CONST               'showvec'
              160  LOAD_FAST             1  'showvec'
              163  LOAD_CONST               'atmisc'
              166  BUILD_MAP_1           1  None
              169  LOAD_CONST               'SQ'
              172  LOAD_CONST               'stepper'
              175  STORE_MAP        
              176  CALL_FUNCTION_512   512  None
              179  STORE_FAST            2  'accepted'

 L.  26       182  LOAD_GLOBAL           0  'findleak'
              185  LOAD_ATTR             1  'vm'
              188  LOAD_CONST               'go_step accepted start'
              191  CALL_FUNCTION_1       1  None
              194  POP_TOP          

 L.  27       195  LOAD_FAST             2  'accepted'
              198  POP_JUMP_IF_FALSE   257  'to 257'

 L.  28       201  LOAD_FAST             0  'x'
              204  LOAD_ATTR             4  'current'
              207  CALL_FUNCTION_0       0  None
              210  STORE_FAST            3  'cur'

 L.  29       213  LOAD_CONST               'Cur from SQ:'
              216  PRINT_ITEM       
              217  LOAD_FAST             3  'cur'
              220  LOAD_ATTR            16  'prms'
              223  CALL_FUNCTION_0       0  None
              226  PRINT_ITEM_CONT  
              227  PRINT_NEWLINE_CONT

 L.  30       228  LOAD_GLOBAL           9  '_s'
              231  LOAD_ATTR            17  '_set_current'
              234  LOAD_FAST             3  'cur'
              237  CALL_FUNCTION_1       1  None
              240  POP_TOP          

 L.  31       241  LOAD_GLOBAL           0  'findleak'
              244  LOAD_ATTR             1  'vm'
              247  LOAD_CONST               'go_step accepted end'
              250  CALL_FUNCTION_1       1  None
              253  POP_TOP          
              254  JUMP_FORWARD          0  'to 257'
            257_0  COME_FROM           254  '254'

 L.  32       257  LOAD_GLOBAL           0  'findleak'
              260  LOAD_ATTR             1  'vm'
              263  LOAD_CONST               'go_step Bootstep start'
              266  CALL_FUNCTION_1       1  None
              269  POP_TOP          

 L.  33       270  LOAD_GLOBAL          18  'len'
              273  LOAD_GLOBAL           9  '_s'
              276  LOAD_ATTR            12  'archive'
              279  CALL_FUNCTION_1       1  None
              282  LOAD_GLOBAL           9  '_s'
              285  LOAD_ATTR            19  'np'
              288  LOAD_GLOBAL           9  '_s'
              291  LOAD_ATTR            20  'F'
              294  BINARY_DIVIDE    
              295  COMPARE_OP            4  >
              298  POP_JUMP_IF_FALSE   513  'to 513'

 L.  34       301  LOAD_CONST               'BOOT STEP'
              304  PRINT_ITEM       
              305  PRINT_NEWLINE_CONT

 L.  35       306  LOAD_GLOBAL           9  '_s'
              309  LOAD_ATTR            15  'step'
              312  CALL_FUNCTION_0       0  None
              315  STORE_FAST            2  'accepted'

 L.  36       318  LOAD_CONST               'Accepted:'
              321  PRINT_ITEM       
              322  LOAD_FAST             2  'accepted'
              325  PRINT_ITEM_CONT  
              326  PRINT_NEWLINE_CONT

 L.  37       327  LOAD_FAST             0  'x'
              330  LOAD_ATTR             4  'current'
              333  CALL_FUNCTION_0       0  None
              336  STORE_FAST            3  'cur'

 L.  38       339  LOAD_CONST               'Cur from BOOT:'
              342  PRINT_ITEM       
              343  LOAD_FAST             3  'cur'
              346  LOAD_ATTR            16  'prms'
              349  CALL_FUNCTION_0       0  None
              352  PRINT_ITEM_CONT  
              353  PRINT_NEWLINE_CONT

 L.  39       354  LOAD_GLOBAL           9  '_s'
              357  LOAD_ATTR             4  'current'
              360  CALL_FUNCTION_0       0  None
              363  STORE_FAST            4  'SQpos'

 L.  40       366  LOAD_GLOBAL          21  'isinstance'
              369  LOAD_FAST             4  'SQpos'
              372  LOAD_GLOBAL          22  'mcmcSQ'
              375  LOAD_ATTR            23  'position'
              378  CALL_FUNCTION_2       2  None
              381  POP_JUMP_IF_TRUE    390  'to 390'
              384  LOAD_ASSERT              AssertionError
              387  RAISE_VARARGS_1       1  None

 L.  41       390  LOAD_FAST             0  'x'
              393  LOAD_ATTR            12  'archive'
              396  LOAD_ATTR            24  'add'
              399  LOAD_FAST             4  'SQpos'
              402  CALL_FUNCTION_1       1  None
              405  POP_TOP          

 L.  42       406  LOAD_FAST             2  'accepted'
              409  POP_JUMP_IF_FALSE   454  'to 454'

 L.  43       412  LOAD_GLOBAL           0  'findleak'
              415  LOAD_ATTR             1  'vm'
              418  LOAD_CONST               'go_step BOOTstep-set_current start'
              421  CALL_FUNCTION_1       1  None
              424  POP_TOP          

 L.  44       425  LOAD_FAST             0  'x'
              428  LOAD_ATTR            17  '_set_current'
              431  LOAD_FAST             4  'SQpos'
              434  CALL_FUNCTION_1       1  None
              437  POP_TOP          

 L.  45       438  LOAD_GLOBAL           0  'findleak'
              441  LOAD_ATTR             1  'vm'
              444  LOAD_CONST               'go_step BOOTstep-set_current end'
              447  CALL_FUNCTION_1       1  None
              450  POP_TOP          
              451  JUMP_FORWARD          0  'to 454'
            454_0  COME_FROM           451  '451'

 L.  46       454  LOAD_FAST             0  'x'
              457  LOAD_ATTR            25  'print_at'
              460  LOAD_CONST               'misc'
              463  BUILD_MAP_2           2  None
              466  LOAD_CONST               'Boot'
              469  LOAD_CONST               'stepper'
              472  STORE_MAP        
              473  LOAD_GLOBAL           9  '_s'
              476  LOAD_ATTR            26  'a'
              479  LOAD_CONST               0
              482  BINARY_SUBSCR    
              483  LOAD_ATTR            27  'vs'
              486  CALL_FUNCTION_0       0  None
              489  LOAD_CONST               'BootScale'
              492  STORE_MAP        
              493  CALL_FUNCTION_256   256  None
              496  POP_TOP          

 L.  47       497  LOAD_GLOBAL           0  'findleak'
              500  LOAD_ATTR             1  'vm'
              503  LOAD_CONST               'go_step BOOTstep end'
              506  CALL_FUNCTION_1       1  None
              509  POP_TOP          
              510  JUMP_FORWARD          0  'to 513'
            513_0  COME_FROM           510  '510'

 L.  49       513  LOAD_GLOBAL           0  'findleak'
              516  LOAD_ATTR             1  'vm'
              519  LOAD_CONST               'go_step end'
              522  CALL_FUNCTION_1       1  None
              525  POP_TOP          
              526  LOAD_CONST               None
              529  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 526


mcmcSQ.go_step = go_step
if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        print __doc__
        die.exit(0)
    mcmcSQ.go(sys.argv)
# global _s ## Warning: Unused global