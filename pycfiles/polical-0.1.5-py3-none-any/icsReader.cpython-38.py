# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/icsReader.py
# Compiled at: 2020-05-12 23:12:19
# Size of source mod 2**32: 2088 bytes
import wget, os
from polical import configuration
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def convertICStoCSV--- This code section failed: ---

 L.   9         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Empezando:'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L.  10        10  LOAD_GLOBAL              logging
               12  LOAD_METHOD              infoc
               14  LOAD_STR                 'Eliminando si existe'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  11        20  LOAD_GLOBAL              print
               22  LOAD_STR                 'Empezando:'
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          

 L.  12        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'Eliminando si existe'
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L.  13        36  LOAD_STR                 'mycalendar.ics'
               38  STORE_FAST               'filename'

 L.  14        40  LOAD_GLOBAL              os
               42  LOAD_ATTR                path
               44  LOAD_METHOD              exists
               46  LOAD_FAST                'filename'
               48  CALL_METHOD_1         1  ''
               50  POP_JUMP_IF_FALSE    62  'to 62'

 L.  15        52  LOAD_GLOBAL              os
               54  LOAD_METHOD              remove
               56  LOAD_FAST                'filename'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
             62_0  COME_FROM            50  '50'

 L.  16        62  LOAD_STR                 'https://educacionvirtual.epn.edu.ec/calendar/export_execute.php?userid=7587&authtoken=a43c2f67460752ab1e1b0d5a784dd330cb5b93e7&preset_what=all&preset_time=recentupcoming'
               64  STORE_FAST               'url'

 L.  17        66  LOAD_GLOBAL              wget
               68  LOAD_METHOD              download
               70  LOAD_FAST                'url'
               72  LOAD_STR                 'mycalendar.ics'
               74  CALL_METHOD_2         2  ''
               76  POP_TOP          

 L.  18        78  LOAD_GLOBAL              open
               80  LOAD_STR                 'mycalendar.ics'
               82  LOAD_STR                 'r'
               84  CALL_FUNCTION_2       2  ''
               86  STORE_FAST               'f'

 L.  19        88  LOAD_GLOBAL              open
               90  LOAD_STR                 'calendar.csv'
               92  LOAD_STR                 'w+'
               94  CALL_FUNCTION_2       2  ''
               96  STORE_FAST               'f2'

 L.  20        98  LOAD_FAST                'f'
              100  LOAD_METHOD              readlines
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'f1'

 L.  21       106  LOAD_STR                 'BEGIN'
              108  LOAD_STR                 'UID'
              110  LOAD_STR                 'SUMMARY'
              112  LOAD_STR                 'DESCRIPTION'
              114  LOAD_STR                 'CLASS'
              116  LOAD_STR                 'LAST-MODIFIED'
              118  LOAD_STR                 'DTSTAMP'
              120  LOAD_STR                 'DTSTART'
              122  LOAD_STR                 'DTEND'
              124  LOAD_STR                 'CATEGORIES'
              126  BUILD_LIST_10        10 
              128  STORE_FAST               'headers'

 L.  22       130  LOAD_FAST                'headers'
              132  GET_ITER         
              134  FOR_ITER            154  'to 154'
              136  STORE_FAST               'x'

 L.  23       138  LOAD_FAST                'f2'
              140  LOAD_METHOD              write
              142  LOAD_FAST                'x'
              144  LOAD_STR                 ';'
              146  BINARY_ADD       
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  JUMP_BACK           134  'to 134'

 L.  24       154  LOAD_FAST                'f2'
              156  LOAD_METHOD              write
              158  LOAD_STR                 '\n'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L.  25       164  LOAD_CONST               False
              166  STORE_FAST               'wrBegin'

 L.  26       168  LOAD_CONST               False
              170  STORE_FAST               'wrNormal'

 L.  27       172  LOAD_CONST               False
              174  STORE_FAST               'wrDescription'

 L.  28       176  LOAD_FAST                'f1'
              178  GET_ITER         
            180_0  COME_FROM           458  '458'
            180_1  COME_FROM           454  '454'
          180_182  FOR_ITER            472  'to 472'
              184  STORE_FAST               'x'

 L.  31       186  LOAD_FAST                'x'
              188  LOAD_METHOD              split
              190  LOAD_STR                 ':'
              192  LOAD_CONST               1
              194  CALL_METHOD_2         2  ''
              196  STORE_FAST               'list'

 L.  32       198  LOAD_FAST                'list'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  LOAD_STR                 'BEGIN'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   240  'to 240'
              210  LOAD_FAST                'list'
              212  LOAD_CONST               1
              214  BINARY_SUBSCR    
              216  LOAD_STR                 'VEVENT\n'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   240  'to 240'

 L.  33       222  LOAD_CONST               True
              224  STORE_FAST               'wrNormal'

 L.  34       226  LOAD_CONST               True
              228  STORE_FAST               'wrBegin'

 L.  35       230  LOAD_STR                 'VEVENT'
              232  LOAD_FAST                'list'
              234  LOAD_CONST               1
              236  STORE_SUBSCR     
              238  JUMP_FORWARD        334  'to 334'
            240_0  COME_FROM           220  '220'
            240_1  COME_FROM           208  '208'

 L.  37       240  LOAD_FAST                'list'
              242  LOAD_CONST               0
              244  BINARY_SUBSCR    
              246  LOAD_STR                 'DESCRIPTION'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   270  'to 270'

 L.  38       254  LOAD_CONST               True
              256  STORE_FAST               'wrDescription'

 L.  39       258  LOAD_FAST                'f2'
              260  LOAD_METHOD              write
              262  LOAD_STR                 '"'
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
              268  JUMP_FORWARD        334  'to 334'
            270_0  COME_FROM           250  '250'

 L.  41       270  LOAD_FAST                'list'
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  LOAD_STR                 'CLASS'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   300  'to 300'

 L.  42       284  LOAD_CONST               False
              286  STORE_FAST               'wrDescription'

 L.  43       288  LOAD_FAST                'f2'
              290  LOAD_METHOD              write
              292  LOAD_STR                 '";'
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          
              298  JUMP_FORWARD        334  'to 334'
            300_0  COME_FROM           280  '280'

 L.  45       300  LOAD_FAST                'list'
              302  LOAD_CONST               0
              304  BINARY_SUBSCR    
              306  LOAD_STR                 'END'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   334  'to 334'
              314  LOAD_FAST                'list'
              316  LOAD_CONST               1
              318  BINARY_SUBSCR    
              320  LOAD_STR                 'VEVENT\n'
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   334  'to 334'

 L.  46       328  LOAD_CONST               False
              330  STORE_FAST               'wrNormal'
              332  JUMP_FORWARD        334  'to 334'
            334_0  COME_FROM           332  '332'
            334_1  COME_FROM           324  '324'
            334_2  COME_FROM           310  '310'
            334_3  COME_FROM           298  '298'
            334_4  COME_FROM           268  '268'
            334_5  COME_FROM           238  '238'

 L.  50       334  LOAD_FAST                'wrNormal'
          336_338  POP_JUMP_IF_FALSE   386  'to 386'
              340  LOAD_FAST                'wrDescription'
              342  LOAD_CONST               False
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   386  'to 386'

 L.  51       350  LOAD_FAST                'list'
              352  LOAD_CONST               1
              354  BINARY_SUBSCR    
              356  LOAD_METHOD              split
              358  LOAD_STR                 '\n'
              360  LOAD_CONST               1
              362  CALL_METHOD_2         2  ''
              364  STORE_FAST               'removebsn'

 L.  52       366  LOAD_FAST                'f2'
              368  LOAD_METHOD              write
              370  LOAD_FAST                'removebsn'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  LOAD_STR                 ';'
              378  BINARY_ADD       
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
              384  JUMP_BACK           180  'to 180'
            386_0  COME_FROM           346  '346'
            386_1  COME_FROM           336  '336'

 L.  53       386  LOAD_FAST                'wrNormal'
          388_390  POP_JUMP_IF_FALSE   448  'to 448'
              392  LOAD_FAST                'wrDescription'
          394_396  POP_JUMP_IF_FALSE   448  'to 448'

 L.  54       398  LOAD_FAST                'list'
              400  GET_ITER         
              402  FOR_ITER            446  'to 446'
              404  STORE_FAST               'y'

 L.  55       406  LOAD_SETCOMP             '<code_object <setcomp>>'
              408  LOAD_STR                 'convertICStoCSV.<locals>.<setcomp>'
              410  MAKE_FUNCTION_0          ''
              412  LOAD_FAST                'list'
              414  GET_ITER         
              416  CALL_FUNCTION_1       1  ''
              418  STORE_FAST               'new_list'

 L.  56       420  LOAD_FAST                'new_list'
              422  GET_ITER         
              424  FOR_ITER            442  'to 442'
              426  STORE_FAST               'x'

 L.  57       428  LOAD_FAST                'f2'
              430  LOAD_METHOD              write
              432  LOAD_FAST                'x'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          
          438_440  JUMP_BACK           424  'to 424'
          442_444  JUMP_BACK           402  'to 402'
              446  JUMP_BACK           180  'to 180'
            448_0  COME_FROM           394  '394'
            448_1  COME_FROM           388  '388'

 L.  58       448  LOAD_FAST                'wrNormal'
              450  LOAD_CONST               False
              452  COMPARE_OP               ==
              454  POP_JUMP_IF_FALSE   180  'to 180'
              456  LOAD_FAST                'wrBegin'
              458  POP_JUMP_IF_FALSE   180  'to 180'

 L.  59       460  LOAD_FAST                'f2'
              462  LOAD_METHOD              write
              464  LOAD_STR                 '\n'
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
              470  JUMP_BACK           180  'to 180'

Parse error at or near `POP_TOP' instruction at offset 468