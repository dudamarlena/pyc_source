# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\qsubwrapmpi.py
# Compiled at: 2012-02-10 06:21:49
__doc__ = '\nqsub a bash/mpirun wrapper around another script.\n\nUsage: qsubwrapmpi [options] JOBSCRIPT\n\nExample:\n\n== JOBSCRIPT ==\n#!/usr/bin/env python\n#PBS -l walltime=00:01:00\n#PBS -j oe\nprint "Hello"\n\ngenerates something like this:\n\n== JOBSCRIPT.sh ==\n#!/bin/bash\n#PBS -l walltime=00:01:00\n#PBS -j oe\n#PBS -l nodes=1:ppn=8\nmodule load openmpi/1.4\nmpirun ./JOBSCRIPT\n\nsubmits it with qsub, and deletes it when qsub has returned.\n'
import os, sys, argparse
from cgp.utils.commands import getstatusoutput

def main--- This code section failed: ---

 L.  44         0  LOAD_CONST               '\n    #!/bin/bash\n    %s\n    #PBS -lnodes=1:ppn=8\n    # add :ib to require Infiniband\n    #PBS -lpmem=2000MB\n    module load openmpi/1.4\n    mpirun %s\n    '
                3  LOAD_ATTR             0  'strip'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            0  'wrapper'

 L.  45        12  LOAD_GLOBAL           1  'len'
               15  LOAD_GLOBAL           2  'sys'
               18  LOAD_ATTR             3  'argv'
               21  CALL_FUNCTION_1       1  None
               24  LOAD_CONST               1
               27  COMPARE_OP            4  >
               30  POP_JUMP_IF_FALSE    49  'to 49'

 L.  46        33  LOAD_GLOBAL           2  'sys'
               36  LOAD_ATTR             3  'argv'
               39  LOAD_CONST               -1
               42  BINARY_SUBSCR    
               43  STORE_FAST            1  'jobscript'
               46  JUMP_FORWARD         17  'to 66'

 L.  48        49  LOAD_GLOBAL           4  '__doc__'
               52  PRINT_ITEM       
               53  PRINT_NEWLINE_CONT

 L.  49        54  LOAD_GLOBAL           5  'RuntimeError'
               57  LOAD_CONST               'No jobscript specified'
               60  CALL_FUNCTION_1       1  None
               63  RAISE_VARARGS_1       1  None
             66_0  COME_FROM            46  '46'

 L.  50        66  LOAD_FAST             1  'jobscript'
               69  LOAD_CONST               '.mpi.sh'
               72  BINARY_ADD       
               73  STORE_FAST            2  'wrapscript'

 L.  53        76  LOAD_GLOBAL           6  'open'
               79  LOAD_FAST             1  'jobscript'
               82  CALL_FUNCTION_1       1  None
               85  SETUP_WITH           32  'to 120'
               88  STORE_FAST            3  'f'

 L.  54        91  LOAD_CONST               '\n'
               94  LOAD_ATTR             7  'join'
               97  LOAD_GENEXPR             '<code_object <genexpr>>'
              100  MAKE_FUNCTION_0       0  None

 L.  55       103  LOAD_FAST             3  'f'
              106  GET_ITER         
              107  CALL_FUNCTION_1       1  None
              110  CALL_FUNCTION_1       1  None
              113  STORE_FAST            4  'directives'
              116  POP_BLOCK        
              117  LOAD_CONST               None
            120_0  COME_FROM_WITH       85  '85'
              120  WITH_CLEANUP     
              121  END_FINALLY      

 L.  58       122  LOAD_GLOBAL           8  'os'
              125  LOAD_ATTR             9  'path'
              128  LOAD_ATTR            10  'exists'
              131  LOAD_FAST             2  'wrapscript'
              134  CALL_FUNCTION_1       1  None
              137  UNARY_NOT        
              138  POP_JUMP_IF_TRUE    147  'to 147'
              141  LOAD_ASSERT              AssertionError
              144  RAISE_VARARGS_1       1  None

 L.  59       147  LOAD_GLOBAL           6  'open'
              150  LOAD_FAST             2  'wrapscript'
              153  LOAD_CONST               'w'
              156  CALL_FUNCTION_2       2  None
              159  SETUP_WITH           42  'to 204'
              162  STORE_FAST            3  'f'

 L.  60       165  LOAD_FAST             3  'f'
              168  LOAD_ATTR            12  'write'
              171  LOAD_FAST             0  'wrapper'
              174  LOAD_FAST             4  'directives'
              177  LOAD_GLOBAL           8  'os'
              180  LOAD_ATTR             9  'path'
              183  LOAD_ATTR            13  'realpath'
              186  LOAD_FAST             1  'jobscript'
              189  CALL_FUNCTION_1       1  None
              192  BUILD_TUPLE_2         2 
              195  BINARY_MODULO    
              196  CALL_FUNCTION_1       1  None
              199  POP_TOP          
              200  POP_BLOCK        
              201  LOAD_CONST               None
            204_0  COME_FROM_WITH      159  '159'
              204  WITH_CLEANUP     
              205  END_FINALLY      

 L.  63       206  LOAD_GLOBAL          14  'getstatusoutput'
              209  LOAD_CONST               'chmod u+x %s'
              212  LOAD_FAST             1  'jobscript'
              215  BINARY_MODULO    
              216  CALL_FUNCTION_1       1  None
              219  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST            5  'status'
              225  STORE_FAST            6  'output'

 L.  64       228  LOAD_FAST             5  'status'
              231  LOAD_CONST               0
              234  COMPARE_OP            2  ==
              237  POP_JUMP_IF_TRUE    249  'to 249'
              240  LOAD_ASSERT              AssertionError
              243  LOAD_FAST             6  'output'
              246  RAISE_VARARGS_2       2  None

 L.  67       249  LOAD_CONST               'qsub %s %s'
              252  LOAD_CONST               ' '
              255  LOAD_ATTR             7  'join'
              258  LOAD_GLOBAL           2  'sys'
              261  LOAD_ATTR             3  'argv'
              264  LOAD_CONST               1
              267  LOAD_CONST               -1
              270  SLICE+3          
              271  CALL_FUNCTION_1       1  None
              274  LOAD_FAST             2  'wrapscript'
              277  BUILD_TUPLE_2         2 
              280  BINARY_MODULO    
              281  STORE_FAST            7  'cmd'

 L.  68       284  LOAD_GLOBAL          14  'getstatusoutput'
              287  LOAD_FAST             7  'cmd'
              290  CALL_FUNCTION_1       1  None
              293  UNPACK_SEQUENCE_2     2 
              296  STORE_FAST            5  'status'
              299  STORE_FAST            6  'output'

 L.  69       302  LOAD_CONST               'qsub returned %s\nCommand: %s\n\nOutput: %s'
              305  STORE_FAST            8  'msg'

 L.  70       308  LOAD_FAST             5  'status'
              311  LOAD_CONST               0
              314  COMPARE_OP            2  ==
              317  POP_JUMP_IF_TRUE    342  'to 342'
              320  LOAD_ASSERT              AssertionError
              323  LOAD_FAST             8  'msg'
              326  LOAD_FAST             5  'status'
              329  LOAD_FAST             7  'cmd'
              332  LOAD_FAST             6  'output'
              335  BUILD_TUPLE_3         3 
              338  BINARY_MODULO    
              339  RAISE_VARARGS_2       2  None

 L.  72       342  LOAD_GLOBAL           8  'os'
              345  LOAD_ATTR            15  'remove'
              348  LOAD_FAST             2  'wrapscript'
              351  CALL_FUNCTION_1       1  None
              354  POP_TOP          

 L.  73       355  LOAD_FAST             6  'output'
              358  PRINT_ITEM       
              359  PRINT_NEWLINE_CONT

Parse error at or near `PRINT_ITEM' instruction at offset 358


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_known_args()
    main()