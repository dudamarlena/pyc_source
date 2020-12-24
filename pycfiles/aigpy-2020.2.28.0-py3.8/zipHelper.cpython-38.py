# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\zipHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 2314 bytes
import os, tarfile, zipfile

def _getParaType--- This code section failed: ---

 L.  11         0  SETUP_FINALLY        24  'to 24'

 L.  12         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              isfile
                8  LOAD_FAST                'para'
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L.  13        14  POP_BLOCK        
               16  LOAD_CONST               0
               18  RETURN_VALUE     
             20_0  COME_FROM            12  '12'
               20  POP_BLOCK        
               22  JUMP_FORWARD         36  'to 36'
             24_0  COME_FROM_FINALLY     0  '0'

 L.  14        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  15        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'
             36_1  COME_FROM            22  '22'

 L.  16        36  SETUP_FINALLY        60  'to 60'

 L.  17        38  LOAD_GLOBAL              os
               40  LOAD_ATTR                path
               42  LOAD_METHOD              isdir
               44  LOAD_FAST                'para'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    56  'to 56'

 L.  18        50  POP_BLOCK        
               52  LOAD_CONST               1
               54  RETURN_VALUE     
             56_0  COME_FROM            48  '48'
               56  POP_BLOCK        
               58  JUMP_FORWARD         72  'to 72'
             60_0  COME_FROM_FINALLY    36  '36'

 L.  19        60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  20        66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            58  '58'

 L.  21        72  LOAD_CONST               2
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 16


def _getZipType--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        48  'to 48'

 L.  27         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              basename
                8  LOAD_FAST                'zipName'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'name'

 L.  28        14  LOAD_FAST                'name'
               16  LOAD_METHOD              lower
               18  CALL_METHOD_0         0  ''
               20  LOAD_METHOD              find
               22  LOAD_STR                 '.tar'
               24  CALL_METHOD_1         1  ''
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L.  29        32  POP_BLOCK        
               34  LOAD_STR                 'tar'
               36  RETURN_VALUE     
             38_0  COME_FROM            30  '30'

 L.  31        38  POP_BLOCK        
               40  LOAD_STR                 'zip'
               42  RETURN_VALUE     
               44  POP_BLOCK        
               46  JUMP_FORWARD         60  'to 60'
             48_0  COME_FROM_FINALLY     0  '0'

 L.  32        48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  33        54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            46  '46'

Parse error at or near `LOAD_STR' instruction at offset 34


def _open--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        46  'to 46'

 L.  39         2  LOAD_FAST                'ptype'
                4  LOAD_STR                 'tar'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  40        10  LOAD_GLOBAL              tarfile
               12  LOAD_METHOD              open
               14  LOAD_FAST                'zipName'
               16  LOAD_FAST                'mode'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'pZip'
               22  JUMP_FORWARD         40  'to 40'
             24_0  COME_FROM             8  '8'

 L.  42        24  LOAD_GLOBAL              zipfile
               26  LOAD_METHOD              ZipFile
               28  LOAD_FAST                'zipName'
               30  LOAD_FAST                'mode'
               32  LOAD_GLOBAL              zipfile
               34  LOAD_ATTR                ZIP_DEFLATED
               36  CALL_METHOD_3         3  ''
               38  STORE_FAST               'pZip'
             40_0  COME_FROM            22  '22'

 L.  43        40  LOAD_FAST                'pZip'
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY     0  '0'

 L.  44        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  45        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
               58  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 52


def _write--- This code section failed: ---

 L.  49         0  SETUP_FINALLY        46  'to 46'

 L.  50         2  LOAD_FAST                'ptype'
                4  LOAD_STR                 'tar'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  51        10  LOAD_FAST                'pZip'
               12  LOAD_ATTR                add
               14  LOAD_FAST                'pfilename'
               16  LOAD_FAST                'parcname'
               18  LOAD_CONST               ('arcname',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  POP_TOP          
               24  JUMP_FORWARD         40  'to 40'
             26_0  COME_FROM             8  '8'

 L.  53        26  LOAD_FAST                'pZip'
               28  LOAD_ATTR                write
               30  LOAD_FAST                'pfilename'
               32  LOAD_FAST                'parcname'
               34  LOAD_CONST               ('arcname',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          
             40_0  COME_FROM            24  '24'

 L.  54        40  POP_BLOCK        
               42  LOAD_CONST               True
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY     0  '0'

 L.  55        46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  56        52  POP_EXCEPT       
               54  LOAD_CONST               False
               56  RETURN_VALUE     
               58  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 44


def myzip--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              _getParaType
                2  LOAD_FAST                'inPath'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'check'

 L.  67         8  LOAD_GLOBAL              _getZipType
               10  LOAD_FAST                'outPath'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'ptype'

 L.  68        16  SETUP_FINALLY       228  'to 228'

 L.  69        18  LOAD_GLOBAL              _open
               20  LOAD_FAST                'outPath'
               22  LOAD_FAST                'ptype'
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'pZip'

 L.  70        28  LOAD_FAST                'check'
               30  LOAD_CONST               2
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    70  'to 70'

 L.  71        36  LOAD_FAST                'inPath'
               38  GET_ITER         
               40  FOR_ITER             70  'to 70'
               42  STORE_FAST               'file'

 L.  72        44  LOAD_FAST                'pZip'
               46  LOAD_METHOD              _write
               48  LOAD_FAST                'pZip'
               50  LOAD_FAST                'ptype'
               52  LOAD_FAST                'file'
               54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              basename
               60  LOAD_FAST                'file'
               62  CALL_METHOD_1         1  ''
               64  CALL_METHOD_4         4  ''
               66  POP_TOP          
               68  JUMP_BACK            40  'to 40'
             70_0  COME_FROM            34  '34'

 L.  73        70  LOAD_FAST                'check'
               72  LOAD_CONST               0
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE   102  'to 102'

 L.  74        78  LOAD_FAST                'pZip'
               80  LOAD_METHOD              _write
               82  LOAD_FAST                'pZip'
               84  LOAD_FAST                'ptype'
               86  LOAD_FAST                'inPath'
               88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_METHOD              basename
               94  LOAD_FAST                'inPath'
               96  CALL_METHOD_1         1  ''
               98  CALL_METHOD_4         4  ''
              100  POP_TOP          
            102_0  COME_FROM            76  '76'

 L.  75       102  LOAD_FAST                'check'
              104  LOAD_CONST               1
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   214  'to 214'

 L.  76       110  LOAD_GLOBAL              os
              112  LOAD_ATTR                path
              114  LOAD_METHOD              dirname
              116  LOAD_FAST                'inPath'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'name'

 L.  77       122  LOAD_GLOBAL              os
              124  LOAD_METHOD              walk
              126  LOAD_FAST                'inPath'
              128  CALL_METHOD_1         1  ''
              130  GET_ITER         
              132  FOR_ITER            214  'to 214'
              134  UNPACK_SEQUENCE_3     3 
              136  STORE_FAST               'dirpath'
              138  STORE_FAST               'dirnames'
              140  STORE_FAST               'filenames'

 L.  78       142  LOAD_FAST                'dirpath'
              144  LOAD_METHOD              replace
              146  LOAD_FAST                'name'
              148  LOAD_STR                 ''
              150  CALL_METHOD_2         2  ''
              152  STORE_FAST               'fpath'

 L.  79       154  LOAD_FAST                'fpath'
              156  POP_JUMP_IF_FALSE   168  'to 168'
              158  LOAD_FAST                'fpath'
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                sep
              164  BINARY_ADD       
              166  JUMP_IF_TRUE_OR_POP   170  'to 170'
            168_0  COME_FROM           156  '156'
              168  LOAD_STR                 ''
            170_0  COME_FROM           166  '166'
              170  STORE_FAST               'fpath'

 L.  80       172  LOAD_FAST                'filenames'
              174  GET_ITER         
              176  FOR_ITER            212  'to 212'
              178  STORE_FAST               'filename'

 L.  81       180  LOAD_FAST                'pZip'
              182  LOAD_METHOD              _write
              184  LOAD_FAST                'pZip'
              186  LOAD_FAST                'ptype'
              188  LOAD_GLOBAL              os
              190  LOAD_ATTR                path
              192  LOAD_METHOD              join
              194  LOAD_FAST                'dirpath'
              196  LOAD_FAST                'filename'
              198  CALL_METHOD_2         2  ''
              200  LOAD_FAST                'fpath'
              202  LOAD_FAST                'filename'
              204  BINARY_ADD       
              206  CALL_METHOD_4         4  ''
              208  POP_TOP          
              210  JUMP_BACK           176  'to 176'
              212  JUMP_BACK           132  'to 132'
            214_0  COME_FROM           108  '108'

 L.  82       214  LOAD_FAST                'pZip'
              216  LOAD_METHOD              close
              218  CALL_METHOD_0         0  ''
              220  POP_TOP          

 L.  83       222  POP_BLOCK        
              224  LOAD_CONST               True
              226  RETURN_VALUE     
            228_0  COME_FROM_FINALLY    16  '16'

 L.  84       228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L.  85       234  POP_EXCEPT       
              236  LOAD_CONST               False
              238  RETURN_VALUE     
              240  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 234


def myunzip--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              _getZipType
                2  LOAD_FAST                'zipName'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'ptype'

 L.  90         8  SETUP_FINALLY        48  'to 48'

 L.  91        10  LOAD_GLOBAL              _open
               12  LOAD_FAST                'zipName'
               14  LOAD_FAST                'ptype'
               16  LOAD_STR                 'r'
               18  CALL_FUNCTION_3       3  ''
               20  STORE_FAST               'pZip'

 L.  92        22  LOAD_FAST                'pZip'
               24  LOAD_ATTR                extractall
               26  LOAD_FAST                'outPath'
               28  LOAD_CONST               ('path',)
               30  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               32  POP_TOP          

 L.  93        34  LOAD_FAST                'pZip'
               36  LOAD_METHOD              close
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L.  94        42  POP_BLOCK        
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY     8  '8'

 L.  95        48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  96        54  POP_EXCEPT       
               56  LOAD_CONST               False
               58  RETURN_VALUE     
               60  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 46