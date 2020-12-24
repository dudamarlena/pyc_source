# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/SimpleIcsToCSV.py
# Compiled at: 2020-05-12 23:12:11
# Size of source mod 2**32: 7331 bytes
import wget, os, csv, sys
from polical import configuration
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def addEvent--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              configuration
                4  LOAD_METHOD              get_file_location
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  LOAD_STR                 'r'
               12  LOAD_STR                 'utf-8'
               14  LOAD_CONST               ('encoding',)
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  STORE_FAST               'f'

 L.  12        20  LOAD_GLOBAL              open
               22  LOAD_GLOBAL              configuration
               24  LOAD_METHOD              get_file_location
               26  LOAD_STR                 'calendar.csv'
               28  CALL_METHOD_1         1  ''
               30  LOAD_STR                 'w+'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'f2'

 L.  13        36  LOAD_FAST                'f'
               38  LOAD_METHOD              readlines
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'f1'

 L.  15        44  LOAD_FAST                'header'
               46  GET_ITER         
             48_0  COME_FROM            68  '68'
               48  FOR_ITER             82  'to 82'
               50  STORE_FAST               'x'

 L.  16        52  LOAD_FAST                'f2'
               54  LOAD_METHOD              write
               56  LOAD_FAST                'x'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          

 L.  17        62  LOAD_FAST                'x'
               64  LOAD_STR                 'END'
               66  COMPARE_OP               !=
               68  POP_JUMP_IF_FALSE    48  'to 48'

 L.  18        70  LOAD_FAST                'f2'
               72  LOAD_METHOD              write
               74  LOAD_STR                 ';'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            48  'to 48'

 L.  19        82  LOAD_FAST                'f2'
               84  LOAD_METHOD              write
               86  LOAD_STR                 '\n'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  20        92  LOAD_CONST               False
               94  STORE_FAST               'wrBegin'

 L.  23        96  LOAD_CONST               False
               98  STORE_FAST               'wrNormal'

 L.  24       100  LOAD_CONST               False
              102  STORE_FAST               'wrDescription'

 L.  25       104  LOAD_FAST                'f1'
              106  GET_ITER         
            108_0  COME_FROM           486  '486'
            108_1  COME_FROM           482  '482'
          108_110  FOR_ITER            500  'to 500'
              112  STORE_FAST               'x'

 L.  27       114  LOAD_FAST                'x'
              116  LOAD_METHOD              split
              118  LOAD_STR                 ':'
              120  LOAD_CONST               1
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'list'

 L.  29       126  LOAD_LISTCOMP            '<code_object <listcomp>>'
              128  LOAD_STR                 'addEvent.<locals>.<listcomp>'
              130  MAKE_FUNCTION_0          ''
              132  LOAD_FAST                'list'
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  GET_ITER         
              140  CALL_FUNCTION_1       1  ''
              142  STORE_FAST               'chars'

 L.  30       144  LOAD_FAST                'list'
              146  LOAD_CONST               0
              148  BINARY_SUBSCR    
              150  LOAD_STR                 'BEGIN'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   186  'to 186'
              156  LOAD_FAST                'list'
              158  LOAD_CONST               1
              160  BINARY_SUBSCR    
              162  LOAD_STR                 'VEVENT\n'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L.  31       168  LOAD_CONST               True
              170  STORE_FAST               'wrNormal'

 L.  32       172  LOAD_CONST               True
              174  STORE_FAST               'wrBegin'

 L.  33       176  LOAD_STR                 'VEVENT'
              178  LOAD_FAST                'list'
              180  LOAD_CONST               1
              182  STORE_SUBSCR     
              184  JUMP_FORWARD        312  'to 312'
            186_0  COME_FROM           166  '166'
            186_1  COME_FROM           154  '154'

 L.  35       186  LOAD_FAST                'list'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_STR                 'DESCRIPTION'
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   214  'to 214'

 L.  36       198  LOAD_CONST               True
              200  STORE_FAST               'wrDescription'

 L.  39       202  LOAD_FAST                'f2'
              204  LOAD_METHOD              write
              206  LOAD_STR                 '"'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  JUMP_FORWARD        312  'to 312'
            214_0  COME_FROM           196  '196'

 L.  42       214  LOAD_FAST                'chars'
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    
              220  LOAD_STR                 ' '
              222  COMPARE_OP               !=
          224_226  POP_JUMP_IF_FALSE   278  'to 278'
              228  LOAD_FAST                'chars'
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  LOAD_STR                 '\t'
              236  COMPARE_OP               !=
          238_240  POP_JUMP_IF_FALSE   278  'to 278'
              242  LOAD_FAST                'chars'
              244  LOAD_CONST               0
              246  BINARY_SUBSCR    
              248  LOAD_STR                 '\n'
              250  COMPARE_OP               !=
          252_254  POP_JUMP_IF_FALSE   278  'to 278'
              256  LOAD_FAST                'wrDescription'
          258_260  POP_JUMP_IF_FALSE   278  'to 278'

 L.  43       262  LOAD_CONST               False
              264  STORE_FAST               'wrDescription'

 L.  44       266  LOAD_FAST                'f2'
              268  LOAD_METHOD              write
              270  LOAD_STR                 '";'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_FORWARD        312  'to 312'
            278_0  COME_FROM           258  '258'
            278_1  COME_FROM           252  '252'
            278_2  COME_FROM           238  '238'
            278_3  COME_FROM           224  '224'

 L.  45       278  LOAD_FAST                'list'
              280  LOAD_CONST               0
              282  BINARY_SUBSCR    
              284  LOAD_STR                 'END'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   312  'to 312'
              292  LOAD_FAST                'list'
              294  LOAD_CONST               1
              296  BINARY_SUBSCR    
              298  LOAD_STR                 'VEVENT\n'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   312  'to 312'

 L.  46       306  LOAD_CONST               False
              308  STORE_FAST               'wrNormal'
              310  JUMP_FORWARD        312  'to 312'
            312_0  COME_FROM           310  '310'
            312_1  COME_FROM           302  '302'
            312_2  COME_FROM           288  '288'
            312_3  COME_FROM           276  '276'
            312_4  COME_FROM           212  '212'
            312_5  COME_FROM           184  '184'

 L.  50       312  LOAD_FAST                'wrNormal'
          314_316  POP_JUMP_IF_FALSE   414  'to 414'
              318  LOAD_FAST                'wrDescription'
              320  LOAD_CONST               False
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   414  'to 414'

 L.  54       328  SETUP_FINALLY       368  'to 368'

 L.  56       330  LOAD_FAST                'list'
              332  LOAD_CONST               1
              334  BINARY_SUBSCR    
              336  LOAD_METHOD              split
              338  LOAD_STR                 '\n'
              340  LOAD_CONST               1
              342  CALL_METHOD_2         2  ''
              344  STORE_FAST               'removebsn'

 L.  57       346  LOAD_FAST                'f2'
              348  LOAD_METHOD              write
              350  LOAD_FAST                'removebsn'
              352  LOAD_CONST               0
              354  BINARY_SUBSCR    
              356  LOAD_STR                 ';'
              358  BINARY_ADD       
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
              364  POP_BLOCK        
              366  JUMP_FORWARD        412  'to 412'
            368_0  COME_FROM_FINALLY   328  '328'

 L.  58       368  DUP_TOP          
              370  LOAD_GLOBAL              Exception
              372  COMPARE_OP               exception-match
          374_376  POP_JUMP_IF_FALSE   410  'to 410'
              378  POP_TOP          
              380  STORE_FAST               'e'
              382  POP_TOP          
              384  SETUP_FINALLY       398  'to 398'

 L.  59       386  LOAD_GLOBAL              print
              388  LOAD_FAST                'e'
              390  CALL_FUNCTION_1       1  ''
              392  POP_TOP          
              394  POP_BLOCK        
              396  BEGIN_FINALLY    
            398_0  COME_FROM_FINALLY   384  '384'
              398  LOAD_CONST               None
              400  STORE_FAST               'e'
              402  DELETE_FAST              'e'
              404  END_FINALLY      
              406  POP_EXCEPT       
              408  JUMP_FORWARD        412  'to 412'
            410_0  COME_FROM           374  '374'
              410  END_FINALLY      
            412_0  COME_FROM           408  '408'
            412_1  COME_FROM           366  '366'
              412  JUMP_BACK           108  'to 108'
            414_0  COME_FROM           324  '324'
            414_1  COME_FROM           314  '314'

 L.  60       414  LOAD_FAST                'wrNormal'
          416_418  POP_JUMP_IF_FALSE   476  'to 476'
              420  LOAD_FAST                'wrDescription'
          422_424  POP_JUMP_IF_FALSE   476  'to 476'

 L.  63       426  LOAD_FAST                'list'
              428  GET_ITER         
              430  FOR_ITER            452  'to 452'
              432  STORE_FAST               'y'

 L.  65       434  LOAD_SETCOMP             '<code_object <setcomp>>'
              436  LOAD_STR                 'addEvent.<locals>.<setcomp>'
              438  MAKE_FUNCTION_0          ''

 L.  66       440  LOAD_FAST                'list'

 L.  65       442  GET_ITER         
              444  CALL_FUNCTION_1       1  ''
              446  STORE_FAST               'new_list'
          448_450  JUMP_BACK           430  'to 430'

 L.  67       452  LOAD_FAST                'new_list'
              454  GET_ITER         
              456  FOR_ITER            474  'to 474'
              458  STORE_FAST               'x'

 L.  68       460  LOAD_FAST                'f2'
              462  LOAD_METHOD              write
              464  LOAD_FAST                'x'
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
          470_472  JUMP_BACK           456  'to 456'
              474  JUMP_BACK           108  'to 108'
            476_0  COME_FROM           422  '422'
            476_1  COME_FROM           416  '416'

 L.  69       476  LOAD_FAST                'wrNormal'
              478  LOAD_CONST               False
              480  COMPARE_OP               ==
              482  POP_JUMP_IF_FALSE   108  'to 108'
              484  LOAD_FAST                'wrBegin'
              486  POP_JUMP_IF_FALSE   108  'to 108'

 L.  72       488  LOAD_FAST                'f2'
              490  LOAD_METHOD              write
              492  LOAD_STR                 '\n'
              494  CALL_METHOD_1         1  ''
              496  POP_TOP          
              498  JUMP_BACK           108  'to 108'

Parse error at or near `POP_TOP' instruction at offset 496


def convertICStoCSV(url):
    print('Descargando calendario desde Aula Virtual...')
    logging.info('Descargando calendario desde Aula Virtual...')
    filename = configuration.get_file_location('mycalendar.ics')
    if os.path.exists(filename):
        os.remove(filename)
    wget.downloadurlfilename
    addEventfindHeader(filename)filename
    print('\nEspere...')
    logging.info('Descarga de calendario finalizada.')


def findHeader--- This code section failed: ---

 L.  90         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              configuration
                4  LOAD_METHOD              get_file_location
                6  LOAD_FAST                'icsCal'
                8  CALL_METHOD_1         1  ''
               10  LOAD_STR                 'r'
               12  LOAD_STR                 'utf-8'
               14  LOAD_CONST               ('encoding',)
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  STORE_FAST               'f'

 L.  92        20  LOAD_GLOBAL              open
               22  LOAD_GLOBAL              configuration
               24  LOAD_METHOD              get_file_location
               26  LOAD_STR                 'calendar.csv'
               28  CALL_METHOD_1         1  ''
               30  LOAD_STR                 'w+'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'f2'

 L.  93        36  LOAD_FAST                'f'
               38  LOAD_METHOD              readlines
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'f1'

 L.  94        44  LOAD_CONST               False
               46  STORE_FAST               'wrBegin'

 L.  97        48  LOAD_CONST               False
               50  STORE_FAST               'wrNormal'

 L.  98        52  LOAD_CONST               False
               54  STORE_FAST               'wrDescription'

 L.  99        56  LOAD_FAST                'f1'
               58  GET_ITER         
             60_0  COME_FROM           300  '300'
             60_1  COME_FROM           288  '288'
             60_2  COME_FROM           284  '284'
            60_62  FOR_ITER            330  'to 330'
               64  STORE_FAST               'x'

 L. 103        66  LOAD_FAST                'x'
               68  LOAD_METHOD              split
               70  LOAD_STR                 ':'
               72  LOAD_CONST               1
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'list'

 L. 104        78  LOAD_LISTCOMP            '<code_object <listcomp>>'
               80  LOAD_STR                 'findHeader.<locals>.<listcomp>'
               82  MAKE_FUNCTION_0          ''
               84  LOAD_FAST                'list'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'chars'

 L. 106        96  LOAD_FAST                'list'
               98  LOAD_CONST               0
              100  BINARY_SUBSCR    
              102  LOAD_STR                 'BEGIN'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   130  'to 130'
              108  LOAD_FAST                'list'
              110  LOAD_CONST               1
              112  BINARY_SUBSCR    
              114  LOAD_STR                 'VEVENT\n'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 107       120  LOAD_CONST               True
              122  STORE_FAST               'wrNormal'

 L. 108       124  LOAD_CONST               True
              126  STORE_FAST               'wrBegin'
              128  JUMP_FORWARD        192  'to 192'
            130_0  COME_FROM           118  '118'
            130_1  COME_FROM           106  '106'

 L. 111       130  LOAD_FAST                'list'
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  LOAD_STR                 'DESCRIPTION'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   148  'to 148'

 L. 112       142  LOAD_CONST               True
              144  STORE_FAST               'wrDescription'
              146  JUMP_FORWARD        192  'to 192'
            148_0  COME_FROM           140  '140'

 L. 115       148  LOAD_FAST                'chars'
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  LOAD_STR                 ' '
              156  COMPARE_OP               !=
              158  POP_JUMP_IF_FALSE   192  'to 192'
              160  LOAD_FAST                'chars'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_STR                 '\t'
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   192  'to 192'
              172  LOAD_FAST                'chars'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_STR                 '\n'
              180  COMPARE_OP               !=
              182  POP_JUMP_IF_FALSE   192  'to 192'
              184  LOAD_FAST                'wrDescription'
              186  POP_JUMP_IF_FALSE   192  'to 192'

 L. 116       188  LOAD_CONST               False
              190  STORE_FAST               'wrDescription'
            192_0  COME_FROM           186  '186'
            192_1  COME_FROM           182  '182'
            192_2  COME_FROM           170  '170'
            192_3  COME_FROM           158  '158'
            192_4  COME_FROM           146  '146'
            192_5  COME_FROM           128  '128'

 L. 118       192  LOAD_FAST                'list'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_STR                 'END'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   210  'to 210'

 L. 120       204  LOAD_CONST               False
              206  STORE_FAST               'wrNormal'
              208  JUMP_FORWARD        210  'to 210'
            210_0  COME_FROM           208  '208'
            210_1  COME_FROM           202  '202'

 L. 125       210  LOAD_FAST                'wrNormal'
              212  LOAD_CONST               False
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   238  'to 238'
              218  LOAD_FAST                'wrBegin'
              220  LOAD_CONST               True
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   238  'to 238'

 L. 126       226  LOAD_FAST                'f2'
              228  LOAD_METHOD              write
              230  LOAD_STR                 'END\n'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_BACK            60  'to 60'
            238_0  COME_FROM           224  '224'
            238_1  COME_FROM           216  '216'

 L. 127       238  LOAD_FAST                'wrNormal'
          240_242  POP_JUMP_IF_FALSE   282  'to 282'
              244  LOAD_FAST                'wrDescription'
              246  LOAD_CONST               False
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   282  'to 282'

 L. 130       254  LOAD_FAST                'f2'
              256  LOAD_METHOD              write
              258  LOAD_FAST                'list'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              replace
              266  LOAD_STR                 ';'
              268  LOAD_STR                 ''
              270  CALL_METHOD_2         2  ''
              272  LOAD_STR                 ';'
              274  BINARY_ADD       
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
              280  JUMP_BACK            60  'to 60'
            282_0  COME_FROM           250  '250'
            282_1  COME_FROM           240  '240'

 L. 131       282  LOAD_FAST                'wrNormal'
              284  POP_JUMP_IF_FALSE    60  'to 60'
              286  LOAD_FAST                'wrDescription'
              288  POP_JUMP_IF_FALSE    60  'to 60'

 L. 134       290  LOAD_FAST                'list'
              292  LOAD_CONST               0
              294  BINARY_SUBSCR    
              296  LOAD_STR                 'DESCRIPTION'
              298  COMPARE_OP               ==
              300  POP_JUMP_IF_FALSE    60  'to 60'

 L. 135       302  LOAD_FAST                'f2'
              304  LOAD_METHOD              write
              306  LOAD_FAST                'list'
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  LOAD_METHOD              replace
              314  LOAD_STR                 ';'
              316  LOAD_STR                 ''
              318  CALL_METHOD_2         2  ''
              320  LOAD_STR                 ';'
              322  BINARY_ADD       
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
              328  JUMP_BACK            60  'to 60'

 L. 137       330  LOAD_FAST                'f2'
              332  LOAD_METHOD              close
              334  CALL_METHOD_0         0  ''
              336  POP_TOP          

 L. 138       338  BUILD_LIST_0          0 
              340  STORE_FAST               'listHeaders'

 L. 143       342  LOAD_GLOBAL              open
              344  LOAD_GLOBAL              configuration
              346  LOAD_METHOD              get_file_location
              348  LOAD_STR                 'calendar.csv'
              350  CALL_METHOD_1         1  ''
              352  CALL_FUNCTION_1       1  ''
              354  SETUP_WITH          398  'to 398'
              356  STORE_FAST               'csv_file'

 L. 144       358  LOAD_GLOBAL              csv
              360  LOAD_ATTR                reader
              362  LOAD_FAST                'csv_file'
              364  LOAD_STR                 ';'
              366  LOAD_CONST               ('delimiter',)
              368  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              370  STORE_FAST               'csv_reader'

 L. 146       372  LOAD_FAST                'csv_reader'
              374  GET_ITER         
              376  FOR_ITER            394  'to 394'
              378  STORE_FAST               'row'

 L. 147       380  LOAD_FAST                'listHeaders'
              382  LOAD_METHOD              append
              384  LOAD_FAST                'row'
              386  CALL_METHOD_1         1  ''
              388  POP_TOP          
          390_392  JUMP_BACK           376  'to 376'
              394  POP_BLOCK        
              396  BEGIN_FINALLY    
            398_0  COME_FROM_WITH      354  '354'
              398  WITH_CLEANUP_START
              400  WITH_CLEANUP_FINISH
              402  END_FINALLY      

 L. 150       404  LOAD_GLOBAL              configuration
              406  LOAD_METHOD              get_file_location
              408  LOAD_STR                 'calendar.csv'
              410  CALL_METHOD_1         1  ''
              412  STORE_FAST               'filename'

 L. 151       414  LOAD_GLOBAL              os
              416  LOAD_ATTR                path
              418  LOAD_METHOD              exists
              420  LOAD_FAST                'filename'
              422  CALL_METHOD_1         1  ''
          424_426  POP_JUMP_IF_FALSE   438  'to 438'

 L. 152       428  LOAD_GLOBAL              os
              430  LOAD_METHOD              remove
              432  LOAD_FAST                'filename'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          
            438_0  COME_FROM           424  '424'

 L. 154       438  LOAD_GLOBAL              max
              440  LOAD_FAST                'listHeaders'
              442  LOAD_GLOBAL              len
              444  LOAD_CONST               ('key',)
              446  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              448  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 396


def main(argv):
    if len(argv) == 2:
        filename = argv[1]
    else:
        print('python icsReader.py file/location/file.ics')
        logging.info('python icsReader.py file/location/file.ics')
    addEventfindHeader(filename)filename


if __name__ == '__main__':
    main(sys.argv)