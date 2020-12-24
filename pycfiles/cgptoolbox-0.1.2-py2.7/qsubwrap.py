# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\qsubwrap.py
# Compiled at: 2012-02-10 06:21:49
"""
qsub a bash wrapper around another script.

Usage: qsubwrap [options] JOBSCRIPT

Example:

== JOBSCRIPT ==
#!/usr/bin/env python
#PBS -l walltime=00:01:00
#PBS -j oe
print "Hello"

generates something like this:

== JOBSCRIPT.sh ==
#!/bin/bash
#PBS -l walltime=00:01:00
#PBS -j oe
./JOBSCRIPT

submits it with qsub, and deletes it when qsub has returned.
"""
import os, sys, argparse
from cgp.utils.commands import getstatusoutput

def main--- This code section failed: ---

 L.  33         0  LOAD_CONST               '#!/bin/bash\n%s\n%s\n'
                3  STORE_FAST            0  'wrapper'

 L.  34         6  LOAD_GLOBAL           0  'len'
                9  LOAD_GLOBAL           1  'sys'
               12  LOAD_ATTR             2  'argv'
               15  CALL_FUNCTION_1       1  None
               18  LOAD_CONST               1
               21  COMPARE_OP            4  >
               24  POP_JUMP_IF_FALSE    43  'to 43'

 L.  35        27  LOAD_GLOBAL           1  'sys'
               30  LOAD_ATTR             2  'argv'
               33  LOAD_CONST               -1
               36  BINARY_SUBSCR    
               37  STORE_FAST            1  'jobscript'
               40  JUMP_FORWARD         17  'to 60'

 L.  37        43  LOAD_GLOBAL           3  '__doc__'
               46  PRINT_ITEM       
               47  PRINT_NEWLINE_CONT

 L.  38        48  LOAD_GLOBAL           4  'RuntimeError'
               51  LOAD_CONST               'No jobscript specified'
               54  CALL_FUNCTION_1       1  None
               57  RAISE_VARARGS_1       1  None
             60_0  COME_FROM            40  '40'

 L.  39        60  LOAD_FAST             1  'jobscript'
               63  LOAD_CONST               '.sh'
               66  BINARY_ADD       
               67  STORE_FAST            2  'wrapscript'

 L.  42        70  LOAD_GLOBAL           5  'open'
               73  LOAD_FAST             1  'jobscript'
               76  CALL_FUNCTION_1       1  None
               79  SETUP_WITH           32  'to 114'
               82  STORE_FAST            3  'f'

 L.  43        85  LOAD_CONST               '\n'
               88  LOAD_ATTR             6  'join'
               91  LOAD_GENEXPR             '<code_object <genexpr>>'
               94  MAKE_FUNCTION_0       0  None

 L.  44        97  LOAD_FAST             3  'f'
              100  GET_ITER         
              101  CALL_FUNCTION_1       1  None
              104  CALL_FUNCTION_1       1  None
              107  STORE_FAST            4  'directives'
              110  POP_BLOCK        
              111  LOAD_CONST               None
            114_0  COME_FROM_WITH       79  '79'
              114  WITH_CLEANUP     
              115  END_FINALLY      

 L.  47       116  LOAD_GLOBAL           7  'os'
              119  LOAD_ATTR             8  'path'
              122  LOAD_ATTR             9  'exists'
              125  LOAD_FAST             2  'wrapscript'
              128  CALL_FUNCTION_1       1  None
              131  UNARY_NOT        
              132  POP_JUMP_IF_TRUE    141  'to 141'
              135  LOAD_ASSERT              AssertionError
              138  RAISE_VARARGS_1       1  None

 L.  48       141  LOAD_GLOBAL           5  'open'
              144  LOAD_FAST             2  'wrapscript'
              147  LOAD_CONST               'w'
              150  CALL_FUNCTION_2       2  None
              153  SETUP_WITH           42  'to 198'
              156  STORE_FAST            3  'f'

 L.  49       159  LOAD_FAST             3  'f'
              162  LOAD_ATTR            11  'write'
              165  LOAD_FAST             0  'wrapper'
              168  LOAD_FAST             4  'directives'
              171  LOAD_GLOBAL           7  'os'
              174  LOAD_ATTR             8  'path'
              177  LOAD_ATTR            12  'realpath'
              180  LOAD_FAST             1  'jobscript'
              183  CALL_FUNCTION_1       1  None
              186  BUILD_TUPLE_2         2 
              189  BINARY_MODULO    
              190  CALL_FUNCTION_1       1  None
              193  POP_TOP          
              194  POP_BLOCK        
              195  LOAD_CONST               None
            198_0  COME_FROM_WITH      153  '153'
              198  WITH_CLEANUP     
              199  END_FINALLY      

 L.  52       200  LOAD_GLOBAL          13  'getstatusoutput'
              203  LOAD_CONST               'chmod u+x %s'
              206  LOAD_FAST             1  'jobscript'
              209  BINARY_MODULO    
              210  CALL_FUNCTION_1       1  None
              213  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST            5  'status'
              219  STORE_FAST            6  'output'

 L.  53       222  LOAD_FAST             5  'status'
              225  LOAD_CONST               0
              228  COMPARE_OP            2  ==
              231  POP_JUMP_IF_TRUE    243  'to 243'
              234  LOAD_ASSERT              AssertionError
              237  LOAD_FAST             6  'output'
              240  RAISE_VARARGS_2       2  None

 L.  56       243  LOAD_CONST               'qsub %s %s'
              246  LOAD_CONST               ' '
              249  LOAD_ATTR             6  'join'
              252  LOAD_GLOBAL           1  'sys'
              255  LOAD_ATTR             2  'argv'
              258  LOAD_CONST               1
              261  LOAD_CONST               -1
              264  SLICE+3          
              265  CALL_FUNCTION_1       1  None
              268  LOAD_FAST             2  'wrapscript'
              271  BUILD_TUPLE_2         2 
              274  BINARY_MODULO    
              275  STORE_FAST            7  'cmd'

 L.  57       278  LOAD_GLOBAL          13  'getstatusoutput'
              281  LOAD_FAST             7  'cmd'
              284  CALL_FUNCTION_1       1  None
              287  UNPACK_SEQUENCE_2     2 
              290  STORE_FAST            5  'status'
              293  STORE_FAST            6  'output'

 L.  58       296  LOAD_CONST               'qsub returned %s\nCommand: %s\n\nOutput: %s'
              299  STORE_FAST            8  'msg'

 L.  59       302  LOAD_FAST             5  'status'
              305  LOAD_CONST               0
              308  COMPARE_OP            2  ==
              311  POP_JUMP_IF_TRUE    336  'to 336'
              314  LOAD_ASSERT              AssertionError
              317  LOAD_FAST             8  'msg'
              320  LOAD_FAST             5  'status'
              323  LOAD_FAST             7  'cmd'
              326  LOAD_FAST             6  'output'
              329  BUILD_TUPLE_3         3 
              332  BINARY_MODULO    
              333  RAISE_VARARGS_2       2  None

 L.  61       336  LOAD_GLOBAL           7  'os'
              339  LOAD_ATTR            14  'remove'
              342  LOAD_FAST             2  'wrapscript'
              345  CALL_FUNCTION_1       1  None
              348  POP_TOP          

 L.  62       349  LOAD_FAST             6  'output'
              352  PRINT_ITEM       
              353  PRINT_NEWLINE_CONT

Parse error at or near `PRINT_ITEM' instruction at offset 352


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_known_args()
    main()