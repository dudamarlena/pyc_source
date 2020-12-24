# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\energy\castep.py
# Compiled at: 2020-01-13 14:07:55
# Size of source mod 2**32: 3300 bytes
import re, os, shutil, platform, numpy as np
import elastic3rd.energy.glue as glue

def get_base_vec--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              zeros
                4  LOAD_CONST               (3, 3)
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'BaseVec'

 L.  12        10  LOAD_FAST                'BaseName'
               12  LOAD_STR                 '.cell'
               14  BINARY_ADD       
               16  STORE_FAST               'FileName'

 L.  13        18  LOAD_GLOBAL              open
               20  LOAD_FAST                'FileName'
               22  LOAD_STR                 'r'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'fopen'

 L.  14        28  LOAD_CONST               0
               30  STORE_FAST               'flag'

 L.  15        32  LOAD_CONST               0
               34  STORE_FAST               'count'

 L.  16        36  LOAD_FAST                'fopen'
               38  GET_ITER         
             40_0  COME_FROM            92  '92'
               40  FOR_ITER            146  'to 146'
               42  STORE_FAST               'eachline'

 L.  17        44  LOAD_FAST                'eachline'
               46  LOAD_METHOD              strip
               48  LOAD_STR                 '\n'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'eachline'

 L.  18        54  LOAD_FAST                'eachline'
               56  LOAD_METHOD              strip
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'eachline'

 L.  19        62  LOAD_FAST                'eachline'
               64  LOAD_STR                 '%BLOCK LATTICE_CART'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L.  20        70  LOAD_CONST               1
               72  STORE_FAST               'flag'

 L.  21        74  JUMP_BACK            40  'to 40'
               76  JUMP_FORWARD         90  'to 90'
             78_0  COME_FROM            68  '68'

 L.  22        78  LOAD_FAST                'eachline'
               80  LOAD_STR                 '%ENDBLOCK LATTICE_CART'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L.  23        86  POP_TOP          
               88  BREAK_LOOP          146  'to 146'
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            76  '76'

 L.  24        90  LOAD_FAST                'flag'
               92  POP_JUMP_IF_FALSE    40  'to 40'

 L.  25        94  LOAD_GLOBAL              re
               96  LOAD_METHOD              split
               98  LOAD_STR                 '\\s+'
              100  LOAD_FAST                'eachline'
              102  CALL_METHOD_2         2  ''
              104  STORE_FAST               'linei'

 L.  26       106  LOAD_GLOBAL              np
              108  LOAD_METHOD              asarray
              110  LOAD_FAST                'linei'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'Basei'

 L.  27       116  LOAD_FAST                'Basei'
              118  LOAD_METHOD              astype
              120  LOAD_GLOBAL              np
              122  LOAD_ATTR                float64
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'Basei'

 L.  28       128  LOAD_FAST                'Basei'
              130  LOAD_FAST                'BaseVec'
              132  LOAD_FAST                'count'
              134  STORE_SUBSCR     

 L.  29       136  LOAD_FAST                'count'
              138  LOAD_CONST               1
              140  BINARY_ADD       
              142  STORE_FAST               'count'
              144  JUMP_BACK            40  'to 40'

 L.  30       146  LOAD_FAST                'fopen'
              148  LOAD_METHOD              close
              150  CALL_METHOD_0         0  ''
              152  POP_TOP          

 L.  31       154  LOAD_FAST                'BaseVec'
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 76


def write_base_vec--- This code section failed: ---

 L.  34         0  LOAD_FAST                'BaseName'
                2  LOAD_STR                 '.cell'
                4  BINARY_ADD       
                6  STORE_FAST               'FileName'

 L.  35         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'FileName'
               12  LOAD_STR                 'r'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'fopen'

 L.  36        18  LOAD_GLOBAL              open
               20  LOAD_STR                 'tmpfile'
               22  LOAD_STR                 'a'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'tmpopen'

 L.  37        28  LOAD_CONST               0
               30  STORE_FAST               'flag'

 L.  38        32  LOAD_CONST               0
               34  STORE_FAST               'count'

 L.  39        36  BUILD_LIST_0          0 
               38  STORE_FAST               'lines'

 L.  40        40  LOAD_FAST                'fopen'
               42  GET_ITER         
               44  FOR_ITER            188  'to 188'
               46  STORE_FAST               'eachline'

 L.  41        48  LOAD_FAST                'eachline'
               50  LOAD_METHOD              strip
               52  LOAD_STR                 '\n'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'linei'

 L.  42        58  LOAD_FAST                'linei'
               60  LOAD_METHOD              strip
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'linei'

 L.  44        66  LOAD_FAST                'linei'
               68  LOAD_STR                 '%BLOCK LATTICE_CART'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    92  'to 92'

 L.  45        74  LOAD_FAST                'tmpopen'
               76  LOAD_METHOD              write
               78  LOAD_STR                 '%BLOCK LATTICE_CART\n'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L.  46        84  LOAD_CONST               1
               86  STORE_FAST               'flag'

 L.  47        88  JUMP_BACK            44  'to 44'
               90  JUMP_FORWARD        104  'to 104'
             92_0  COME_FROM            72  '72'

 L.  48        92  LOAD_FAST                'linei'
               94  LOAD_STR                 '%ENDBLOCK LATTICE_CART'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   104  'to 104'

 L.  49       100  LOAD_CONST               0
              102  STORE_FAST               'flag'
            104_0  COME_FROM            98  '98'
            104_1  COME_FROM            90  '90'

 L.  50       104  LOAD_FAST                'flag'
              106  POP_JUMP_IF_FALSE   176  'to 176'

 L.  51       108  LOAD_GLOBAL              range
              110  LOAD_CONST               0
              112  LOAD_CONST               3
              114  CALL_FUNCTION_2       2  ''
              116  GET_ITER         
              118  FOR_ITER            156  'to 156'
              120  STORE_FAST               'j'

 L.  52       122  LOAD_FAST                'tmpopen'
              124  LOAD_METHOD              write
              126  LOAD_STR                 '      '
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L.  53       132  LOAD_FAST                'tmpopen'
              134  LOAD_METHOD              write
              136  LOAD_STR                 '%.15f'
              138  LOAD_FAST                'BaseVec'
              140  LOAD_FAST                'count'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'j'
              146  BINARY_SUBSCR    
              148  BINARY_MODULO    
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_BACK           118  'to 118'

 L.  54       156  LOAD_FAST                'tmpopen'
              158  LOAD_METHOD              write
              160  LOAD_STR                 '\n'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L.  55       166  LOAD_FAST                'count'
              168  LOAD_CONST               1
              170  BINARY_ADD       
              172  STORE_FAST               'count'
              174  JUMP_BACK            44  'to 44'
            176_0  COME_FROM           106  '106'

 L.  57       176  LOAD_FAST                'tmpopen'
              178  LOAD_METHOD              write
              180  LOAD_FAST                'eachline'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
              186  JUMP_BACK            44  'to 44'

 L.  58       188  LOAD_FAST                'fopen'
              190  LOAD_METHOD              close
              192  CALL_METHOD_0         0  ''
              194  POP_TOP          

 L.  59       196  LOAD_FAST                'tmpopen'
              198  LOAD_METHOD              close
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

 L.  60       204  LOAD_GLOBAL              os
              206  LOAD_METHOD              remove
              208  LOAD_FAST                'FileName'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L.  61       214  LOAD_GLOBAL              os
              216  LOAD_METHOD              rename
              218  LOAD_STR                 'tmpfile'
              220  LOAD_FAST                'FileName'
              222  CALL_METHOD_2         2  ''
              224  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 90


def run(NP, BaseName):
    plat = platform.platform.split'-'[0].lower
    if plat == 'windows':
        RunStr = 'RunCASTEP -np ' + str(int(NP)) + ' ' + BaseName
    else:
        if plat == 'linux':
            RunStr = './RunCASTEP.sh -np ' + str(int(NP)) + ' ' + BaseName
    return RunStr


def get_energy(BaseName):
    FileName = BaseName + '.castep'
    fopen = openFileName'r'
    for eachline in fopen:
        linei = eachline.split'='
        flag = linei[0].strip
        flag0 = flag.split','[0]
        if flag0 == 'Final energy':
            energy = linei[1].strip.split' '[0]
        fopen.close
        energy = float(energy)
        Energy = glue.multi_energyenergy
        return Energy


def copy_files(BaseName, Path):
    plat = platform.platform.split'-'[0].lower
    shutil.copyfile(BaseName + '.cell')(Path + '/' + BaseName + '.cell')
    shutil.copyfile(BaseName + '.param')(Path + '/' + BaseName + '.param')
    if plat == 'windows':
        shutil.copyfile'RunCASTEP.bat'(Path + '/RunCASTEP.bat')
    else:
        if plat == 'linux':
            shutil.copyfile'RunCASTEP.sh'(Path + '/RunCASTEP.sh')
            os.system('chmod 777 ' + Path + '/RunCASTEP.sh')