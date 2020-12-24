# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/negar/negar.py
# Compiled at: 2020-02-08 05:39:49
# Size of source mod 2**32: 18073 bytes
from re import search
from traceback import format_exc
from tzlocal import get_localzone
from datetime import datetime
from platform import system, release, machine
from getpass import getuser
from os.path import isfile
from inspect import getframeinfo, stack
from negar.countriesWithTheirCapital import countries

def get_country(_city):
    data = countries
    if _city in data:
        return data[_city]
    return 'unknown'


def err_temp_func(file_, line, problem):
    error_template = 'negar module - error | python file : {} | line : {} | problem : {}'
    return error_template.format(file_, line, problem)


def justify_text(text_, length):
    return '{}{}{}'.format(int((length - len(str(text_))) / 2) * ' ', text_, length * ' ')[:length]


def header_row(header_specs):
    sep = '—' * (len(header_specs) - 4)
    out = '\n  .{1}.\n {0}\n  |{1}|\n'.format(header_specs, sep)
    return out


def log_row(row_num, log_date, log_time, row_text, row_log_size, row_file_name, row_type, row_line_num):
    row_num = justify_text(row_num, 7)
    row_type = justify_text(row_type, 8)
    out = '  |{num}| {date} | {time} | {text}{pad}|{file}|{type}|{line}|\n'.format(num=row_num,
      date=log_date,
      time=log_time,
      text=row_text,
      file=row_file_name,
      type=row_type,
      line=row_line_num,
      pad=(' ' * (row_log_size - (len(row_text) + 1))))
    out += '  |{}|\n'.format('—' * (len(out) - 5))
    return out


def text--- This code section failed: ---

 L.  57         0  LOAD_GLOBAL              stack
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_CONST               1
                6  BINARY_SUBSCR    
                8  STORE_FAST               'x'

 L.  58        10  LOAD_FAST                'x'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'x'

 L.  59        18  LOAD_GLOBAL              getframeinfo
               20  LOAD_FAST                'x'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'get_log_file_python_file_name_or_line'

 L.  72        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'get_log_file_python_file_name_or_line'
               30  LOAD_ATTR                lineno
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'line_python_file'

 L.  75        36  LOAD_GLOBAL              str
               38  LOAD_FAST                'get_log_file_python_file_name_or_line'
               40  LOAD_ATTR                filename
               42  LOAD_METHOD              split
               44  LOAD_STR                 '/'
               46  CALL_METHOD_1         1  ''
               48  LOAD_CONST               -1
               50  BINARY_SUBSCR    
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'python_file_name'

 L.  77        56  LOAD_FAST                'python_file_name'
               58  LOAD_CONST               ('<stdin>', '<input>')
               60  COMPARE_OP               in
               62  POP_JUMP_IF_FALSE    70  'to 70'

 L.  78        64  LOAD_STR                 'interpreter'
               66  STORE_FAST               'python_file'
               68  JUMP_FORWARD        108  'to 108'
             70_0  COME_FROM            62  '62'

 L.  79        70  LOAD_GLOBAL              len
               72  LOAD_FAST                'python_file_name'
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_CONST               18
               78  COMPARE_OP               <
               80  POP_JUMP_IF_FALSE    88  'to 88'

 L.  80        82  LOAD_FAST                'python_file_name'
               84  STORE_FAST               'python_file'
               86  JUMP_FORWARD        108  'to 108'
             88_0  COME_FROM            80  '80'

 L.  82        88  LOAD_GLOBAL              print
               90  LOAD_GLOBAL              err_temp_func
               92  LOAD_FAST                'python_file_name'
               94  LOAD_FAST                'line_python_file'
               96  LOAD_STR                 'maximum size of python file name is 15 character ...'
               98  CALL_FUNCTION_3       3  ''
              100  CALL_FUNCTION_1       1  ''
              102  POP_TOP          

 L.  83       104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            86  '86'
            108_1  COME_FROM            68  '68'

 L.  86       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'save'
              112  LOAD_GLOBAL              str
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   124  'to 124'

 L.  87       118  LOAD_FAST                'save'
              120  STORE_FAST               'log_file'
              122  JUMP_FORWARD        158  'to 158'
            124_0  COME_FROM           116  '116'

 L.  88       124  LOAD_FAST                'save'
              126  LOAD_CONST               None
              128  COMPARE_OP               is
              130  POP_JUMP_IF_FALSE   138  'to 138'

 L.  89       132  LOAD_STR                 'log.txt'
              134  STORE_FAST               'log_file'
              136  JUMP_FORWARD        158  'to 158'
            138_0  COME_FROM           130  '130'

 L.  91       138  LOAD_GLOBAL              print
              140  LOAD_GLOBAL              err_temp_func
              142  LOAD_FAST                'python_file_name'
              144  LOAD_FAST                'line_python_file'
              146  LOAD_STR                 '"save" type is not str ...'
              148  CALL_FUNCTION_3       3  ''
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L.  92       154  LOAD_CONST               None
              156  RETURN_VALUE     
            158_0  COME_FROM           136  '136'
            158_1  COME_FROM           122  '122'

 L.  95       158  LOAD_FAST                'text_log'
              160  LOAD_CONST               None
              162  COMPARE_OP               is
              164  POP_JUMP_IF_FALSE   186  'to 186'

 L.  96       166  LOAD_GLOBAL              print
              168  LOAD_GLOBAL              err_temp_func
              170  LOAD_FAST                'python_file_name'
              172  LOAD_FAST                'line_python_file'
              174  LOAD_STR                 '"text" value is empty ...'
              176  CALL_FUNCTION_3       3  ''
              178  CALL_FUNCTION_1       1  ''
              180  POP_TOP          

 L.  97       182  LOAD_CONST               None
              184  RETURN_VALUE     
            186_0  COME_FROM           164  '164'

 L.  98       186  LOAD_GLOBAL              isinstance
              188  LOAD_FAST                'text_log'
              190  LOAD_GLOBAL              str
              192  CALL_FUNCTION_2       2  ''
              194  POP_JUMP_IF_TRUE    216  'to 216'

 L.  99       196  LOAD_GLOBAL              print
              198  LOAD_GLOBAL              err_temp_func
              200  LOAD_FAST                'python_file_name'
              202  LOAD_FAST                'line_python_file'
              204  LOAD_STR                 '"text" type is not str ...'
              206  CALL_FUNCTION_3       3  ''
              208  CALL_FUNCTION_1       1  ''
              210  POP_TOP          

 L. 100       212  LOAD_CONST               None
              214  RETURN_VALUE     
            216_0  COME_FROM           194  '194'

 L. 101       216  LOAD_FAST                'text_log'
              218  LOAD_STR                 ''
              220  COMPARE_OP               ==
              222  POP_JUMP_IF_FALSE   244  'to 244'

 L. 102       224  LOAD_GLOBAL              print
              226  LOAD_GLOBAL              err_temp_func
              228  LOAD_FAST                'python_file_name'
              230  LOAD_FAST                'line_python_file'
              232  LOAD_STR                 '"text" value is empty ...'
              234  CALL_FUNCTION_3       3  ''
              236  CALL_FUNCTION_1       1  ''
              238  POP_TOP          

 L. 103       240  LOAD_CONST               None
              242  RETURN_VALUE     
            244_0  COME_FROM           222  '222'

 L. 105       244  LOAD_FAST                'text_log'
              246  STORE_FAST               'log_text'

 L. 108       248  LOAD_FAST                'size'
              250  LOAD_CONST               None
              252  COMPARE_OP               is
          254_256  POP_JUMP_IF_FALSE   264  'to 264'

 L. 109       258  LOAD_CONST               3
              260  STORE_FAST               'log_size'
              262  JUMP_FORWARD        360  'to 360'
            264_0  COME_FROM           254  '254'

 L. 110       264  LOAD_GLOBAL              isinstance
              266  LOAD_FAST                'size'
              268  LOAD_GLOBAL              int
              270  CALL_FUNCTION_2       2  ''
          272_274  POP_JUMP_IF_TRUE    296  'to 296'

 L. 111       276  LOAD_GLOBAL              print
              278  LOAD_GLOBAL              err_temp_func
              280  LOAD_FAST                'python_file_name'
              282  LOAD_FAST                'line_python_file'
              284  LOAD_STR                 '"size" type is not str ...'
              286  CALL_FUNCTION_3       3  ''
              288  CALL_FUNCTION_1       1  ''
              290  POP_TOP          

 L. 112       292  LOAD_CONST               None
              294  RETURN_VALUE     
            296_0  COME_FROM           272  '272'

 L. 113       296  LOAD_FAST                'size'
              298  LOAD_CONST               5
              300  COMPARE_OP               >
          302_304  POP_JUMP_IF_FALSE   326  'to 326'

 L. 114       306  LOAD_GLOBAL              print
              308  LOAD_GLOBAL              err_temp_func
              310  LOAD_FAST                'python_file_name'
              312  LOAD_FAST                'line_python_file'
              314  LOAD_STR                 '"size" value range is not (1 ... 5) ...'
              316  CALL_FUNCTION_3       3  ''
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          

 L. 115       322  LOAD_CONST               None
              324  RETURN_VALUE     
            326_0  COME_FROM           302  '302'

 L. 116       326  LOAD_FAST                'size'
              328  LOAD_CONST               0
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   356  'to 356'

 L. 117       336  LOAD_GLOBAL              print
              338  LOAD_GLOBAL              err_temp_func
              340  LOAD_FAST                'python_file_name'
              342  LOAD_FAST                'line_python_file'
              344  LOAD_STR                 '"size" value is not in range (1 ... 5) ...'
              346  CALL_FUNCTION_3       3  ''
              348  CALL_FUNCTION_1       1  ''
              350  POP_TOP          

 L. 118       352  LOAD_CONST               None
              354  RETURN_VALUE     
            356_0  COME_FROM           332  '332'

 L. 120       356  LOAD_FAST                'size'
              358  STORE_FAST               'log_size'
            360_0  COME_FROM           262  '262'

 L. 133       360  LOAD_FAST                'log_size'
              362  LOAD_CONST               1
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   404  'to 404'
              370  LOAD_GLOBAL              len
              372  LOAD_FAST                'log_text'
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_CONST               69
              378  COMPARE_OP               >
          380_382  POP_JUMP_IF_FALSE   404  'to 404'

 L. 134       384  LOAD_GLOBAL              print
              386  LOAD_GLOBAL              err_temp_func
              388  LOAD_FAST                'python_file_name'
              390  LOAD_FAST                'line_python_file'
              392  LOAD_STR                 '"size = 1" maximum 69 character support ...'
              394  CALL_FUNCTION_3       3  ''
              396  CALL_FUNCTION_1       1  ''
              398  POP_TOP          

 L. 135       400  LOAD_CONST               None
              402  RETURN_VALUE     
            404_0  COME_FROM           380  '380'
            404_1  COME_FROM           366  '366'

 L. 136       404  LOAD_FAST                'log_size'
              406  LOAD_CONST               2
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   448  'to 448'
              414  LOAD_GLOBAL              len
              416  LOAD_FAST                'log_text'
              418  CALL_FUNCTION_1       1  ''
              420  LOAD_CONST               93
              422  COMPARE_OP               >
          424_426  POP_JUMP_IF_FALSE   448  'to 448'

 L. 137       428  LOAD_GLOBAL              print
              430  LOAD_GLOBAL              err_temp_func
              432  LOAD_FAST                'python_file_name'
              434  LOAD_FAST                'line_python_file'
              436  LOAD_STR                 '"size = 2" maximum 93 character support ...'
              438  CALL_FUNCTION_3       3  ''
              440  CALL_FUNCTION_1       1  ''
              442  POP_TOP          

 L. 138       444  LOAD_CONST               None
              446  RETURN_VALUE     
            448_0  COME_FROM           424  '424'
            448_1  COME_FROM           410  '410'

 L. 139       448  LOAD_FAST                'log_size'
              450  LOAD_CONST               3
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   492  'to 492'
              458  LOAD_GLOBAL              len
              460  LOAD_FAST                'log_text'
              462  CALL_FUNCTION_1       1  ''
              464  LOAD_CONST               131
              466  COMPARE_OP               >
          468_470  POP_JUMP_IF_FALSE   492  'to 492'

 L. 140       472  LOAD_GLOBAL              print
              474  LOAD_GLOBAL              err_temp_func
              476  LOAD_FAST                'python_file_name'
              478  LOAD_FAST                'line_python_file'
              480  LOAD_STR                 '"size = 3" maximum 131 character support ...'
              482  CALL_FUNCTION_3       3  ''
              484  CALL_FUNCTION_1       1  ''
              486  POP_TOP          

 L. 141       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           468  '468'
            492_1  COME_FROM           454  '454'

 L. 142       492  LOAD_FAST                'log_size'
              494  LOAD_CONST               4
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   536  'to 536'
              502  LOAD_GLOBAL              len
              504  LOAD_FAST                'log_text'
              506  CALL_FUNCTION_1       1  ''
              508  LOAD_CONST               199
              510  COMPARE_OP               >
          512_514  POP_JUMP_IF_FALSE   536  'to 536'

 L. 143       516  LOAD_GLOBAL              print
              518  LOAD_GLOBAL              err_temp_func
              520  LOAD_FAST                'python_file_name'
              522  LOAD_FAST                'line_python_file'
              524  LOAD_STR                 '"size = 4" maximum 199 character support ...'
              526  CALL_FUNCTION_3       3  ''
              528  CALL_FUNCTION_1       1  ''
              530  POP_TOP          

 L. 144       532  LOAD_CONST               None
              534  RETURN_VALUE     
            536_0  COME_FROM           512  '512'
            536_1  COME_FROM           498  '498'

 L. 145       536  LOAD_FAST                'log_size'
              538  LOAD_CONST               5
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   580  'to 580'
              546  LOAD_GLOBAL              len
              548  LOAD_FAST                'log_text'
              550  CALL_FUNCTION_1       1  ''
              552  LOAD_CONST               397
              554  COMPARE_OP               >
          556_558  POP_JUMP_IF_FALSE   580  'to 580'

 L. 146       560  LOAD_GLOBAL              print
              562  LOAD_GLOBAL              err_temp_func
              564  LOAD_FAST                'python_file_name'
              566  LOAD_FAST                'line_python_file'
              568  LOAD_STR                 '"size = 5" maximum 397 character support ...'
              570  CALL_FUNCTION_3       3  ''
              572  CALL_FUNCTION_1       1  ''
              574  POP_TOP          

 L. 147       576  LOAD_CONST               None
              578  RETURN_VALUE     
            580_0  COME_FROM           556  '556'
            580_1  COME_FROM           542  '542'

 L. 150       580  LOAD_GLOBAL              justify_text
              582  LOAD_FAST                'python_file'
              584  LOAD_CONST               18
              586  CALL_FUNCTION_2       2  ''
              588  STORE_FAST               'justified_python_file'

 L. 153       590  LOAD_GLOBAL              len
              592  LOAD_FAST                'line_python_file'
              594  CALL_FUNCTION_1       1  ''
              596  LOAD_CONST               6
              598  COMPARE_OP               <=
          600_602  POP_JUMP_IF_FALSE   616  'to 616'

 L. 154       604  LOAD_GLOBAL              justify_text
              606  LOAD_FAST                'line_python_file'
              608  LOAD_CONST               6
              610  CALL_FUNCTION_2       2  ''
              612  STORE_FAST               'justified_line_python_file'
              614  JUMP_FORWARD        636  'to 636'
            616_0  COME_FROM           600  '600'

 L. 156       616  LOAD_GLOBAL              print
              618  LOAD_GLOBAL              err_temp_func
              620  LOAD_FAST                'python_file_name'
              622  LOAD_FAST                'line_python_file'
              624  LOAD_STR                 'maximum python line number support is 999999 ...'
              626  CALL_FUNCTION_3       3  ''
              628  CALL_FUNCTION_1       1  ''
              630  POP_TOP          

 L. 157       632  LOAD_CONST               None
              634  RETURN_VALUE     
            636_0  COME_FROM           614  '614'

 L. 160       636  LOAD_FAST                'log_file'
              638  STORE_FAST               'log_file_name'

 L. 163       640  LOAD_GLOBAL              round
              642  LOAD_CONST               0.057
              644  LOAD_CONST               5
              646  LOAD_CONST               0.1
              648  LOAD_CONST               2.9
              650  LOAD_CONST               3.9
              652  LOAD_CONST               4.4
              654  LOAD_CONST               4.7
              656  BUILD_LIST_5          5 
              658  LOAD_FAST                'log_size'
              660  LOAD_CONST               1
              662  BINARY_SUBTRACT  
              664  BINARY_SUBSCR    
              666  BINARY_SUBTRACT  
              668  LOAD_CONST               20
              670  BINARY_MULTIPLY  
              672  BINARY_MULTIPLY  
              674  LOAD_CONST               1
              676  CALL_FUNCTION_2       2  ''
              678  STORE_FAST               'log_file_size'

 L. 167       680  LOAD_GLOBAL              str
              682  LOAD_GLOBAL              get_localzone
              684  CALL_FUNCTION_0       0  ''
              686  CALL_FUNCTION_1       1  ''
              688  LOAD_METHOD              lower
              690  CALL_METHOD_0         0  ''
              692  LOAD_METHOD              split
              694  LOAD_STR                 '/'
              696  CALL_METHOD_1         1  ''
              698  LOAD_CONST               0
              700  BINARY_SUBSCR    
              702  STORE_FAST               'continent'

 L. 170       704  LOAD_GLOBAL              str
              706  LOAD_GLOBAL              get_localzone
              708  CALL_FUNCTION_0       0  ''
              710  CALL_FUNCTION_1       1  ''
              712  LOAD_METHOD              lower
              714  CALL_METHOD_0         0  ''
              716  LOAD_METHOD              split
              718  LOAD_STR                 '/'
              720  CALL_METHOD_1         1  ''
              722  LOAD_CONST               1
              724  BINARY_SUBSCR    
              726  STORE_FAST               'city'

 L. 173       728  LOAD_GLOBAL              str
              730  LOAD_GLOBAL              get_country
              732  LOAD_FAST                'city'
              734  CALL_FUNCTION_1       1  ''
              736  CALL_FUNCTION_1       1  ''
              738  STORE_FAST               'country'

 L. 176       740  LOAD_GLOBAL              str
              742  LOAD_GLOBAL              getuser
              744  CALL_FUNCTION_0       0  ''
              746  CALL_FUNCTION_1       1  ''
              748  STORE_FAST               'username'

 L. 179       750  LOAD_GLOBAL              str
              752  LOAD_GLOBAL              system
              754  CALL_FUNCTION_0       0  ''
              756  LOAD_METHOD              lower
              758  CALL_METHOD_0         0  ''
              760  CALL_FUNCTION_1       1  ''
              762  STORE_FAST               'os'

 L. 182       764  LOAD_GLOBAL              str
              766  LOAD_GLOBAL              release
              768  CALL_FUNCTION_0       0  ''
              770  LOAD_METHOD              lower
              772  CALL_METHOD_0         0  ''
              774  CALL_FUNCTION_1       1  ''
              776  STORE_FAST               'version'

 L. 185       778  LOAD_GLOBAL              str
              780  LOAD_GLOBAL              machine
              782  CALL_FUNCTION_0       0  ''
              784  LOAD_METHOD              lower
              786  CALL_METHOD_0         0  ''
              788  CALL_FUNCTION_1       1  ''
              790  STORE_FAST               'architecture'

 L. 188       792  LOAD_GLOBAL              str
              794  LOAD_GLOBAL              datetime
              796  LOAD_METHOD              now
              798  CALL_METHOD_0         0  ''
              800  CALL_FUNCTION_1       1  ''
              802  LOAD_METHOD              split
              804  LOAD_STR                 ' '
              806  CALL_METHOD_1         1  ''
              808  LOAD_CONST               0
              810  BINARY_SUBSCR    
              812  STORE_FAST               'date'

 L. 191       814  LOAD_GLOBAL              str
              816  LOAD_GLOBAL              datetime
              818  LOAD_METHOD              now
              820  CALL_METHOD_0         0  ''
              822  CALL_FUNCTION_1       1  ''
              824  LOAD_METHOD              split
              826  LOAD_STR                 ' '
              828  CALL_METHOD_1         1  ''
              830  LOAD_CONST               1
              832  BINARY_SUBSCR    
              834  LOAD_METHOD              split
              836  LOAD_STR                 '.'
              838  CALL_METHOD_1         1  ''
              840  LOAD_CONST               0
              842  BINARY_SUBSCR    
              844  STORE_FAST               'time'

 L. 194       846  LOAD_STR                 'text'
              848  STORE_FAST               'log_type'

 L. 199       850  LOAD_STR                 '%s < %s < %s | %s | %s > %s > %s'

 L. 200       852  LOAD_FAST                'city'

 L. 200       854  LOAD_FAST                'country'

 L. 200       856  LOAD_FAST                'continent'

 L. 200       858  LOAD_FAST                'username'

 L. 200       860  LOAD_FAST                'os'

 L. 200       862  LOAD_FAST                'version'

 L. 200       864  LOAD_FAST                'architecture'

 L. 199       866  BUILD_TUPLE_7         7 
              868  BINARY_MODULO    
              870  STORE_FAST               'spec_center'

 L. 201       872  LOAD_GLOBAL              justify_text
              874  LOAD_FAST                'spec_center'
              876  LOAD_CONST               2
              878  LOAD_GLOBAL              int
              880  LOAD_GLOBAL              len
              882  LOAD_FAST                'spec_center'
              884  CALL_FUNCTION_1       1  ''
              886  LOAD_FAST                'log_file_size'
              888  BINARY_TRUE_DIVIDE
              890  CALL_FUNCTION_1       1  ''
              892  BINARY_MULTIPLY  
              894  LOAD_GLOBAL              len
              896  LOAD_FAST                'spec_center'
              898  CALL_FUNCTION_1       1  ''
              900  BINARY_ADD       
              902  CALL_FUNCTION_2       2  ''
              904  STORE_FAST               'spec_center'

 L. 202       906  LOAD_STR                 ' |  num  |    date    |   time   |'
              908  LOAD_FAST                'spec_center'
              910  BINARY_ADD       
              912  LOAD_STR                 '|       file       |  type  | line | '
              914  BINARY_ADD       
              916  STORE_FAST               'specifications'

 L. 205       918  LOAD_GLOBAL              isfile
              920  LOAD_FAST                'log_file_name'
              922  CALL_FUNCTION_1       1  ''
          924_926  POP_JUMP_IF_TRUE   1000  'to 1000'

 L. 207       928  LOAD_GLOBAL              open
              930  LOAD_FAST                'log_file_name'
              932  LOAD_STR                 'w'
              934  CALL_FUNCTION_2       2  ''
              936  SETUP_WITH          990  'to 990'
              938  STORE_FAST               'log_file'

 L. 209       940  LOAD_FAST                'log_file'
              942  LOAD_METHOD              write
              944  LOAD_GLOBAL              header_row
              946  LOAD_FAST                'specifications'
              948  CALL_FUNCTION_1       1  ''
              950  CALL_METHOD_1         1  ''
              952  POP_TOP          

 L. 212       954  LOAD_FAST                'log_file'
              956  LOAD_METHOD              write

 L. 213       958  LOAD_GLOBAL              log_row
              960  LOAD_CONST               1
              962  LOAD_FAST                'date'
              964  LOAD_FAST                'time'
              966  LOAD_FAST                'text_log'
              968  LOAD_GLOBAL              len
              970  LOAD_FAST                'spec_center'
              972  CALL_FUNCTION_1       1  ''
              974  LOAD_FAST                'justified_python_file'
              976  LOAD_FAST                'log_type'

 L. 214       978  LOAD_FAST                'justified_line_python_file'

 L. 213       980  CALL_FUNCTION_8       8  ''

 L. 212       982  CALL_METHOD_1         1  ''
              984  POP_TOP          
              986  POP_BLOCK        
              988  BEGIN_FINALLY    
            990_0  COME_FROM_WITH      936  '936'
              990  WITH_CLEANUP_START
              992  WITH_CLEANUP_FINISH
              994  END_FINALLY      
          996_998  JUMP_FORWARD       1350  'to 1350'
           1000_0  COME_FROM           924  '924'

 L. 217      1000  LOAD_GLOBAL              isfile
             1002  LOAD_FAST                'log_file_name'
             1004  CALL_FUNCTION_1       1  ''
         1006_1008  POP_JUMP_IF_FALSE  1350  'to 1350'

 L. 218      1010  LOAD_GLOBAL              open
             1012  LOAD_FAST                'log_file_name'
             1014  LOAD_STR                 'r'
             1016  CALL_FUNCTION_2       2  ''
             1018  SETUP_WITH         1098  'to 1098'
             1020  STORE_FAST               'f'

 L. 219      1022  LOAD_FAST                'f'
             1024  LOAD_METHOD              read
             1026  CALL_METHOD_0         0  ''
             1028  LOAD_METHOD              splitlines
             1030  CALL_METHOD_0         0  ''
             1032  LOAD_CONST               -1
             1034  BINARY_SUBSCR    
             1036  LOAD_STR                 '  |'
             1038  LOAD_STR                 '—'
             1040  LOAD_GLOBAL              len
             1042  LOAD_FAST                'specifications'
             1044  CALL_FUNCTION_1       1  ''
             1046  LOAD_CONST               4
             1048  BINARY_SUBTRACT  
             1050  BINARY_MULTIPLY  
             1052  BINARY_ADD       
             1054  LOAD_STR                 '|'
             1056  BINARY_ADD       
             1058  COMPARE_OP               !=
         1060_1062  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 220      1064  LOAD_GLOBAL              print
             1066  LOAD_GLOBAL              err_temp_func
             1068  LOAD_FAST                'python_file_name'
             1070  LOAD_FAST                'line_python_file'

 L. 221      1072  LOAD_STR                 "previously defined log file size , can't be resized ..."

 L. 220      1074  CALL_FUNCTION_3       3  ''
             1076  CALL_FUNCTION_1       1  ''
             1078  POP_TOP          

 L. 222      1080  POP_BLOCK        
             1082  BEGIN_FINALLY    
             1084  WITH_CLEANUP_START
             1086  WITH_CLEANUP_FINISH
             1088  POP_FINALLY           0  ''
             1090  LOAD_CONST               None
             1092  RETURN_VALUE     
           1094_0  COME_FROM          1060  '1060'
             1094  POP_BLOCK        
             1096  BEGIN_FINALLY    
           1098_0  COME_FROM_WITH     1018  '1018'
             1098  WITH_CLEANUP_START
             1100  WITH_CLEANUP_FINISH
             1102  END_FINALLY      

 L. 225      1104  LOAD_GLOBAL              open
             1106  LOAD_FAST                'log_file_name'
             1108  LOAD_STR                 'r'
             1110  CALL_FUNCTION_2       2  ''
             1112  SETUP_WITH         1202  'to 1202'
             1114  STORE_FAST               'f'

 L. 226      1116  LOAD_FAST                'f'
             1118  LOAD_METHOD              read
             1120  CALL_METHOD_0         0  ''
             1122  LOAD_METHOD              splitlines
             1124  CALL_METHOD_0         0  ''
             1126  LOAD_CONST               -2
             1128  BINARY_SUBSCR    
             1130  LOAD_METHOD              split
             1132  LOAD_STR                 '| '
             1134  LOAD_GLOBAL              str
             1136  LOAD_GLOBAL              datetime
             1138  LOAD_METHOD              now
             1140  CALL_METHOD_0         0  ''
             1142  LOAD_ATTR                year
             1144  CALL_FUNCTION_1       1  ''
             1146  BINARY_ADD       
             1148  LOAD_STR                 '-'
             1150  BINARY_ADD       
             1152  LOAD_CONST               1
             1154  CALL_METHOD_2         2  ''
             1156  LOAD_CONST               0
             1158  BINARY_SUBSCR    
             1160  STORE_FAST               'line_number'

 L. 227      1162  LOAD_FAST                'line_number'
             1164  LOAD_METHOD              replace
             1166  LOAD_STR                 '|'
             1168  LOAD_STR                 ''
             1170  CALL_METHOD_2         2  ''
             1172  STORE_FAST               'line_number'

 L. 228      1174  LOAD_FAST                'line_number'
             1176  LOAD_METHOD              replace
             1178  LOAD_STR                 ' '
             1180  LOAD_STR                 ''
             1182  CALL_METHOD_2         2  ''
             1184  STORE_FAST               'line_number'

 L. 229      1186  LOAD_GLOBAL              int
             1188  LOAD_FAST                'line_number'
             1190  CALL_FUNCTION_1       1  ''
             1192  LOAD_CONST               1
             1194  BINARY_ADD       
             1196  STORE_FAST               'line_number'
             1198  POP_BLOCK        
             1200  BEGIN_FINALLY    
           1202_0  COME_FROM_WITH     1112  '1112'
             1202  WITH_CLEANUP_START
             1204  WITH_CLEANUP_FINISH
             1206  END_FINALLY      

 L. 232      1208  LOAD_GLOBAL              len
             1210  LOAD_GLOBAL              str
             1212  LOAD_FAST                'line_number'
             1214  CALL_FUNCTION_1       1  ''
             1216  CALL_FUNCTION_1       1  ''
             1218  LOAD_CONST               7
             1220  COMPARE_OP               >
         1222_1224  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 233      1226  LOAD_GLOBAL              print
             1228  LOAD_GLOBAL              err_temp_func
             1230  LOAD_FAST                'python_file_name'
             1232  LOAD_FAST                'line_python_file'

 L. 234      1234  LOAD_STR                 "'size = 5' maximum line number support is 9999999 ..."

 L. 233      1236  CALL_FUNCTION_3       3  ''
             1238  CALL_FUNCTION_1       1  ''
             1240  POP_TOP          

 L. 235      1242  LOAD_CONST               None
             1244  RETURN_VALUE     
           1246_0  COME_FROM          1222  '1222'

 L. 238      1246  LOAD_GLOBAL              len
             1248  LOAD_GLOBAL              str
             1250  LOAD_FAST                'line_number'
             1252  CALL_FUNCTION_1       1  ''
             1254  CALL_FUNCTION_1       1  ''
             1256  LOAD_CONST               7
             1258  COMPARE_OP               <=
         1260_1262  POP_JUMP_IF_FALSE  1276  'to 1276'

 L. 239      1264  LOAD_GLOBAL              justify_text
             1266  LOAD_FAST                'line_number'
             1268  LOAD_CONST               7
             1270  CALL_FUNCTION_2       2  ''
             1272  STORE_FAST               'log_file_number'
             1274  JUMP_FORWARD       1296  'to 1296'
           1276_0  COME_FROM          1260  '1260'

 L. 241      1276  LOAD_GLOBAL              print
             1278  LOAD_GLOBAL              err_temp_func
             1280  LOAD_FAST                'python_file_name'
             1282  LOAD_FAST                'line_python_file'

 L. 242      1284  LOAD_STR                 'maximum number to numbering lines support is 9999999 ...'

 L. 241      1286  CALL_FUNCTION_3       3  ''
             1288  CALL_FUNCTION_1       1  ''
             1290  POP_TOP          

 L. 243      1292  LOAD_CONST               None
             1294  RETURN_VALUE     
           1296_0  COME_FROM          1274  '1274'

 L. 246      1296  LOAD_GLOBAL              open
             1298  LOAD_FAST                'log_file_name'
             1300  LOAD_STR                 'a'
             1302  CALL_FUNCTION_2       2  ''
             1304  SETUP_WITH         1344  'to 1344'
             1306  STORE_FAST               'log_file'

 L. 249      1308  LOAD_FAST                'log_file'
             1310  LOAD_METHOD              write
             1312  LOAD_GLOBAL              log_row
             1314  LOAD_FAST                'log_file_number'
             1316  LOAD_FAST                'date'
             1318  LOAD_FAST                'time'
             1320  LOAD_FAST                'text_log'
             1322  LOAD_GLOBAL              len
             1324  LOAD_FAST                'spec_center'
             1326  CALL_FUNCTION_1       1  ''
             1328  LOAD_FAST                'justified_python_file'

 L. 250      1330  LOAD_FAST                'log_type'

 L. 250      1332  LOAD_FAST                'justified_line_python_file'

 L. 249      1334  CALL_FUNCTION_8       8  ''
             1336  CALL_METHOD_1         1  ''
             1338  POP_TOP          
             1340  POP_BLOCK        
             1342  BEGIN_FINALLY    
           1344_0  COME_FROM_WITH     1304  '1304'
             1344  WITH_CLEANUP_START
             1346  WITH_CLEANUP_FINISH
             1348  END_FINALLY      
           1350_0  COME_FROM          1006  '1006'
           1350_1  COME_FROM           996  '996'

Parse error at or near `BEGIN_FINALLY' instruction at offset 1082


def error--- This code section failed: ---

 L. 257         0  LOAD_GLOBAL              format_exc
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'error_log'

 L. 258         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'error_log'
               10  LOAD_METHOD              splitlines
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               2
               18  COMPARE_OP               <
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 259        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 262        26  LOAD_GLOBAL              str
               28  LOAD_FAST                'error_log'
               30  LOAD_METHOD              splitlines
               32  CALL_METHOD_0         0  ''
               34  LOAD_CONST               -1
               36  BINARY_SUBSCR    
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'error_text'

 L. 263        42  LOAD_GLOBAL              filter
               44  LOAD_LAMBDA              '<code_object <lambda>>'
               46  LOAD_STR                 'error.<locals>.<lambda>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_FAST                'error_log'
               52  LOAD_METHOD              splitlines
               54  CALL_METHOD_0         0  ''
               56  CALL_FUNCTION_2       2  ''
               58  BUILD_LIST_UNPACK_1     1 
               60  STORE_FAST               'a'

 L. 266        62  LOAD_GLOBAL              search
               64  LOAD_STR                 'File "(.*)", line (.*), in (.*)'
               66  LOAD_FAST                'a'
               68  LOAD_CONST               -1
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_2       2  ''
               74  LOAD_METHOD              groups
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'python_file_name'

 L. 267        80  LOAD_FAST                'a'
               82  LOAD_CONST               None
               84  LOAD_CONST               -1
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  LOAD_CONST               None
               92  LOAD_CONST               None
               94  LOAD_CONST               -1
               96  BUILD_SLICE_3         3 
               98  BINARY_SUBSCR    
              100  GET_ITER         
              102  FOR_ITER            152  'to 152'
              104  STORE_FAST               'i'

 L. 268       106  LOAD_GLOBAL              search
              108  LOAD_STR                 'File "(.*)", line (.*), in (.*)'
              110  LOAD_FAST                'i'
              112  CALL_FUNCTION_2       2  ''
              114  LOAD_METHOD              groups
              116  CALL_METHOD_0         0  ''
              118  STORE_FAST               'x'

 L. 269       120  LOAD_FAST                'x'
              122  POP_JUMP_IF_FALSE   146  'to 146'
              124  LOAD_FAST                'python_file_name'
              126  LOAD_CONST               2
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'x'
              132  LOAD_CONST               2
              134  BINARY_SUBSCR    
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   146  'to 146'

 L. 270       140  LOAD_FAST                'x'
              142  STORE_FAST               'python_file_name'
              144  JUMP_BACK           102  'to 102'
            146_0  COME_FROM           138  '138'
            146_1  COME_FROM           122  '122'

 L. 272       146  POP_TOP          
              148  BREAK_LOOP          152  'to 152'
              150  JUMP_BACK           102  'to 102'

 L. 275       152  LOAD_GLOBAL              str
              154  LOAD_FAST                'python_file_name'
              156  LOAD_CONST               1
              158  BINARY_SUBSCR    
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'line_python_file'

 L. 278       164  LOAD_GLOBAL              str
              166  LOAD_FAST                'python_file_name'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_METHOD              split
              176  LOAD_STR                 '/'
              178  CALL_METHOD_1         1  ''
              180  LOAD_CONST               -1
              182  BINARY_SUBSCR    
              184  STORE_FAST               'python_file_name'

 L. 290       186  LOAD_FAST                'python_file_name'
              188  LOAD_CONST               ('<stdin>', '<input>')
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   200  'to 200'

 L. 291       194  LOAD_STR                 'interpreter'
              196  STORE_FAST               'python_file'
              198  JUMP_FORWARD        238  'to 238'
            200_0  COME_FROM           192  '192'

 L. 292       200  LOAD_GLOBAL              len
              202  LOAD_FAST                'python_file_name'
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_CONST               18
              208  COMPARE_OP               <
              210  POP_JUMP_IF_FALSE   218  'to 218'

 L. 293       212  LOAD_FAST                'python_file_name'
              214  STORE_FAST               'python_file'
              216  JUMP_FORWARD        238  'to 238'
            218_0  COME_FROM           210  '210'

 L. 295       218  LOAD_GLOBAL              print
              220  LOAD_GLOBAL              err_temp_func
              222  LOAD_FAST                'python_file_name'
              224  LOAD_FAST                'line_python_file'
              226  LOAD_STR                 'maximum size of python file name is 15 character ...'
              228  CALL_FUNCTION_3       3  ''
              230  CALL_FUNCTION_1       1  ''
              232  POP_TOP          

 L. 296       234  LOAD_CONST               None
              236  RETURN_VALUE     
            238_0  COME_FROM           216  '216'
            238_1  COME_FROM           198  '198'

 L. 299       238  LOAD_GLOBAL              isinstance
              240  LOAD_FAST                'save'
              242  LOAD_GLOBAL              str
              244  CALL_FUNCTION_2       2  ''
              246  POP_JUMP_IF_FALSE   254  'to 254'

 L. 300       248  LOAD_FAST                'save'
              250  STORE_FAST               'log_file'
              252  JUMP_FORWARD        290  'to 290'
            254_0  COME_FROM           246  '246'

 L. 301       254  LOAD_FAST                'save'
              256  LOAD_CONST               None
              258  COMPARE_OP               is
          260_262  POP_JUMP_IF_FALSE   270  'to 270'

 L. 302       264  LOAD_STR                 'log.txt'
              266  STORE_FAST               'log_file'
              268  JUMP_FORWARD        290  'to 290'
            270_0  COME_FROM           260  '260'

 L. 304       270  LOAD_GLOBAL              print
              272  LOAD_GLOBAL              err_temp_func
              274  LOAD_FAST                'python_file_name'
              276  LOAD_FAST                'line_python_file'
              278  LOAD_STR                 '"save" type is not str ...'
              280  CALL_FUNCTION_3       3  ''
              282  CALL_FUNCTION_1       1  ''
              284  POP_TOP          

 L. 305       286  LOAD_CONST               None
              288  RETURN_VALUE     
            290_0  COME_FROM           268  '268'
            290_1  COME_FROM           252  '252'

 L. 308       290  LOAD_FAST                'size'
              292  LOAD_CONST               None
              294  COMPARE_OP               is
          296_298  POP_JUMP_IF_FALSE   306  'to 306'

 L. 309       300  LOAD_CONST               3
              302  STORE_FAST               'log_size'
              304  JUMP_FORWARD        402  'to 402'
            306_0  COME_FROM           296  '296'

 L. 310       306  LOAD_GLOBAL              isinstance
              308  LOAD_FAST                'size'
              310  LOAD_GLOBAL              int
              312  CALL_FUNCTION_2       2  ''
          314_316  POP_JUMP_IF_TRUE    338  'to 338'

 L. 311       318  LOAD_GLOBAL              print
              320  LOAD_GLOBAL              err_temp_func
              322  LOAD_FAST                'python_file_name'
              324  LOAD_FAST                'line_python_file'
              326  LOAD_STR                 '"size" type is not str ...'
              328  CALL_FUNCTION_3       3  ''
              330  CALL_FUNCTION_1       1  ''
              332  POP_TOP          

 L. 312       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           314  '314'

 L. 313       338  LOAD_FAST                'size'
              340  LOAD_CONST               5
              342  COMPARE_OP               >
          344_346  POP_JUMP_IF_FALSE   368  'to 368'

 L. 314       348  LOAD_GLOBAL              print
              350  LOAD_GLOBAL              err_temp_func
              352  LOAD_FAST                'python_file_name'
              354  LOAD_FAST                'line_python_file'
              356  LOAD_STR                 '"size" value range is not (1 ... 5) ...'
              358  CALL_FUNCTION_3       3  ''
              360  CALL_FUNCTION_1       1  ''
              362  POP_TOP          

 L. 315       364  LOAD_CONST               None
              366  RETURN_VALUE     
            368_0  COME_FROM           344  '344'

 L. 316       368  LOAD_FAST                'size'
              370  LOAD_CONST               0
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   398  'to 398'

 L. 317       378  LOAD_GLOBAL              print
              380  LOAD_GLOBAL              err_temp_func
              382  LOAD_FAST                'python_file_name'
              384  LOAD_FAST                'line_python_file'
              386  LOAD_STR                 '"size" value is not in range (1 ... 5) ...'
              388  CALL_FUNCTION_3       3  ''
              390  CALL_FUNCTION_1       1  ''
              392  POP_TOP          

 L. 318       394  LOAD_CONST               None
              396  RETURN_VALUE     
            398_0  COME_FROM           374  '374'

 L. 320       398  LOAD_FAST                'size'
              400  STORE_FAST               'log_size'
            402_0  COME_FROM           304  '304'

 L. 333       402  LOAD_FAST                'log_size'
              404  LOAD_CONST               1
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   446  'to 446'
              412  LOAD_GLOBAL              len
              414  LOAD_FAST                'error_text'
              416  CALL_FUNCTION_1       1  ''
              418  LOAD_CONST               69
              420  COMPARE_OP               >
          422_424  POP_JUMP_IF_FALSE   446  'to 446'

 L. 334       426  LOAD_GLOBAL              print
              428  LOAD_GLOBAL              err_temp_func
              430  LOAD_FAST                'python_file_name'
              432  LOAD_FAST                'line_python_file'
              434  LOAD_STR                 '"size = 1" maximum 69 character support ...'
              436  CALL_FUNCTION_3       3  ''
              438  CALL_FUNCTION_1       1  ''
              440  POP_TOP          

 L. 335       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           422  '422'
            446_1  COME_FROM           408  '408'

 L. 336       446  LOAD_FAST                'log_size'
              448  LOAD_CONST               2
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   490  'to 490'
              456  LOAD_GLOBAL              len
              458  LOAD_FAST                'error_text'
              460  CALL_FUNCTION_1       1  ''
              462  LOAD_CONST               93
              464  COMPARE_OP               >
          466_468  POP_JUMP_IF_FALSE   490  'to 490'

 L. 337       470  LOAD_GLOBAL              print
              472  LOAD_GLOBAL              err_temp_func
              474  LOAD_FAST                'python_file_name'
              476  LOAD_FAST                'line_python_file'
              478  LOAD_STR                 '"size = 2" maximum 93 character support ...'
              480  CALL_FUNCTION_3       3  ''
              482  CALL_FUNCTION_1       1  ''
              484  POP_TOP          

 L. 338       486  LOAD_CONST               None
              488  RETURN_VALUE     
            490_0  COME_FROM           466  '466'
            490_1  COME_FROM           452  '452'

 L. 339       490  LOAD_FAST                'log_size'
              492  LOAD_CONST               3
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_FALSE   534  'to 534'
              500  LOAD_GLOBAL              len
              502  LOAD_FAST                'error_text'
              504  CALL_FUNCTION_1       1  ''
              506  LOAD_CONST               131
              508  COMPARE_OP               >
          510_512  POP_JUMP_IF_FALSE   534  'to 534'

 L. 340       514  LOAD_GLOBAL              print
              516  LOAD_GLOBAL              err_temp_func
              518  LOAD_FAST                'python_file_name'
              520  LOAD_FAST                'line_python_file'
              522  LOAD_STR                 '"size = 3" maximum 131 character support ...'
              524  CALL_FUNCTION_3       3  ''
              526  CALL_FUNCTION_1       1  ''
              528  POP_TOP          

 L. 341       530  LOAD_CONST               None
              532  RETURN_VALUE     
            534_0  COME_FROM           510  '510'
            534_1  COME_FROM           496  '496'

 L. 342       534  LOAD_FAST                'log_size'
              536  LOAD_CONST               4
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   578  'to 578'
              544  LOAD_GLOBAL              len
              546  LOAD_FAST                'error_text'
              548  CALL_FUNCTION_1       1  ''
              550  LOAD_CONST               199
              552  COMPARE_OP               >
          554_556  POP_JUMP_IF_FALSE   578  'to 578'

 L. 343       558  LOAD_GLOBAL              print
              560  LOAD_GLOBAL              err_temp_func
              562  LOAD_FAST                'python_file_name'
              564  LOAD_FAST                'line_python_file'
              566  LOAD_STR                 '"size = 4" maximum 199 character support ...'
              568  CALL_FUNCTION_3       3  ''
              570  CALL_FUNCTION_1       1  ''
              572  POP_TOP          

 L. 344       574  LOAD_CONST               None
              576  RETURN_VALUE     
            578_0  COME_FROM           554  '554'
            578_1  COME_FROM           540  '540'

 L. 345       578  LOAD_FAST                'log_size'
              580  LOAD_CONST               5
              582  COMPARE_OP               ==
          584_586  POP_JUMP_IF_FALSE   622  'to 622'
              588  LOAD_GLOBAL              len
              590  LOAD_FAST                'error_text'
              592  CALL_FUNCTION_1       1  ''
              594  LOAD_CONST               397
              596  COMPARE_OP               >
          598_600  POP_JUMP_IF_FALSE   622  'to 622'

 L. 346       602  LOAD_GLOBAL              print
              604  LOAD_GLOBAL              err_temp_func
              606  LOAD_FAST                'python_file_name'
              608  LOAD_FAST                'line_python_file'
              610  LOAD_STR                 '"size = 5" maximum 397 character support ...'
              612  CALL_FUNCTION_3       3  ''
              614  CALL_FUNCTION_1       1  ''
              616  POP_TOP          

 L. 347       618  LOAD_CONST               None
              620  RETURN_VALUE     
            622_0  COME_FROM           598  '598'
            622_1  COME_FROM           584  '584'

 L. 350       622  LOAD_GLOBAL              justify_text
              624  LOAD_FAST                'python_file'
              626  LOAD_CONST               18
              628  CALL_FUNCTION_2       2  ''
              630  STORE_FAST               'justified_python_file'

 L. 353       632  LOAD_GLOBAL              len
              634  LOAD_FAST                'line_python_file'
              636  CALL_FUNCTION_1       1  ''
              638  LOAD_CONST               6
              640  COMPARE_OP               <=
          642_644  POP_JUMP_IF_FALSE   658  'to 658'

 L. 354       646  LOAD_GLOBAL              justify_text
              648  LOAD_FAST                'line_python_file'
              650  LOAD_CONST               6
              652  CALL_FUNCTION_2       2  ''
              654  STORE_FAST               'justified_line_python_file'
              656  JUMP_FORWARD        678  'to 678'
            658_0  COME_FROM           642  '642'

 L. 356       658  LOAD_GLOBAL              print
              660  LOAD_GLOBAL              err_temp_func
              662  LOAD_FAST                'python_file_name'
              664  LOAD_FAST                'line_python_file'
              666  LOAD_STR                 'maximum python line number support is 999999 ...'
              668  CALL_FUNCTION_3       3  ''
              670  CALL_FUNCTION_1       1  ''
              672  POP_TOP          

 L. 357       674  LOAD_CONST               None
              676  RETURN_VALUE     
            678_0  COME_FROM           656  '656'

 L. 360       678  LOAD_FAST                'log_file'
              680  STORE_FAST               'log_file_name'

 L. 363       682  LOAD_GLOBAL              round
              684  LOAD_CONST               0.057
              686  LOAD_CONST               5
              688  LOAD_CONST               0.1
              690  LOAD_CONST               2.9
              692  LOAD_CONST               3.9
              694  LOAD_CONST               4.4
              696  LOAD_CONST               4.7
              698  BUILD_LIST_5          5 
              700  LOAD_FAST                'log_size'
              702  LOAD_CONST               1
              704  BINARY_SUBTRACT  
              706  BINARY_SUBSCR    
              708  BINARY_SUBTRACT  
              710  LOAD_CONST               20
              712  BINARY_MULTIPLY  
              714  BINARY_MULTIPLY  
              716  LOAD_CONST               1
              718  CALL_FUNCTION_2       2  ''
              720  STORE_FAST               'log_file_size'

 L. 366       722  LOAD_GLOBAL              str
              724  LOAD_GLOBAL              get_localzone
              726  CALL_FUNCTION_0       0  ''
              728  CALL_FUNCTION_1       1  ''
              730  LOAD_METHOD              lower
              732  CALL_METHOD_0         0  ''
              734  LOAD_METHOD              split
              736  LOAD_STR                 '/'
              738  CALL_METHOD_1         1  ''
              740  LOAD_CONST               0
              742  BINARY_SUBSCR    
              744  STORE_FAST               'continent'

 L. 369       746  LOAD_GLOBAL              str
              748  LOAD_GLOBAL              get_localzone
              750  CALL_FUNCTION_0       0  ''
              752  CALL_FUNCTION_1       1  ''
              754  LOAD_METHOD              lower
              756  CALL_METHOD_0         0  ''
              758  LOAD_METHOD              split
              760  LOAD_STR                 '/'
              762  CALL_METHOD_1         1  ''
              764  LOAD_CONST               1
              766  BINARY_SUBSCR    
              768  STORE_FAST               'city'

 L. 372       770  LOAD_GLOBAL              str
              772  LOAD_GLOBAL              get_country
              774  LOAD_FAST                'city'
              776  CALL_FUNCTION_1       1  ''
              778  CALL_FUNCTION_1       1  ''
              780  STORE_FAST               'country'

 L. 375       782  LOAD_GLOBAL              str
              784  LOAD_GLOBAL              getuser
              786  CALL_FUNCTION_0       0  ''
              788  CALL_FUNCTION_1       1  ''
              790  STORE_FAST               'username'

 L. 378       792  LOAD_GLOBAL              str
              794  LOAD_GLOBAL              system
              796  CALL_FUNCTION_0       0  ''
              798  LOAD_METHOD              lower
              800  CALL_METHOD_0         0  ''
              802  CALL_FUNCTION_1       1  ''
              804  STORE_FAST               'os'

 L. 381       806  LOAD_GLOBAL              str
              808  LOAD_GLOBAL              release
              810  CALL_FUNCTION_0       0  ''
              812  LOAD_METHOD              lower
              814  CALL_METHOD_0         0  ''
              816  CALL_FUNCTION_1       1  ''
              818  STORE_FAST               'version'

 L. 384       820  LOAD_GLOBAL              str
              822  LOAD_GLOBAL              machine
              824  CALL_FUNCTION_0       0  ''
              826  LOAD_METHOD              lower
              828  CALL_METHOD_0         0  ''
              830  CALL_FUNCTION_1       1  ''
              832  STORE_FAST               'architecture'

 L. 387       834  LOAD_GLOBAL              str
              836  LOAD_GLOBAL              datetime
              838  LOAD_METHOD              now
              840  CALL_METHOD_0         0  ''
              842  CALL_FUNCTION_1       1  ''
              844  LOAD_METHOD              split
              846  LOAD_STR                 ' '
              848  CALL_METHOD_1         1  ''
              850  LOAD_CONST               0
              852  BINARY_SUBSCR    
              854  STORE_FAST               'date'

 L. 390       856  LOAD_GLOBAL              str
              858  LOAD_GLOBAL              datetime
              860  LOAD_METHOD              now
              862  CALL_METHOD_0         0  ''
              864  CALL_FUNCTION_1       1  ''
              866  LOAD_METHOD              split
              868  LOAD_STR                 ' '
              870  CALL_METHOD_1         1  ''
              872  LOAD_CONST               1
              874  BINARY_SUBSCR    
              876  LOAD_METHOD              split
              878  LOAD_STR                 '.'
              880  CALL_METHOD_1         1  ''
              882  LOAD_CONST               0
              884  BINARY_SUBSCR    
              886  STORE_FAST               'time'

 L. 393       888  LOAD_STR                 ' error'
              890  STORE_FAST               'log_type'

 L. 398       892  LOAD_STR                 '%s < %s < %s | %s | %s > %s > %s'

 L. 399       894  LOAD_FAST                'city'

 L. 399       896  LOAD_FAST                'country'

 L. 399       898  LOAD_FAST                'continent'

 L. 399       900  LOAD_FAST                'username'

 L. 399       902  LOAD_FAST                'os'

 L. 399       904  LOAD_FAST                'version'

 L. 399       906  LOAD_FAST                'architecture'

 L. 398       908  BUILD_TUPLE_7         7 
              910  BINARY_MODULO    
              912  STORE_FAST               'spec_center'

 L. 400       914  LOAD_GLOBAL              justify_text
              916  LOAD_FAST                'spec_center'
              918  LOAD_CONST               2
              920  LOAD_GLOBAL              int
              922  LOAD_GLOBAL              len
              924  LOAD_FAST                'spec_center'
              926  CALL_FUNCTION_1       1  ''
              928  LOAD_FAST                'log_file_size'
              930  BINARY_TRUE_DIVIDE
              932  CALL_FUNCTION_1       1  ''
              934  BINARY_MULTIPLY  
              936  LOAD_GLOBAL              len
              938  LOAD_FAST                'spec_center'
              940  CALL_FUNCTION_1       1  ''
              942  BINARY_ADD       
              944  CALL_FUNCTION_2       2  ''
              946  STORE_FAST               'spec_center'

 L. 401       948  LOAD_STR                 ' |  num  |    date    |   time   |'
              950  LOAD_FAST                'spec_center'
              952  BINARY_ADD       
              954  LOAD_STR                 '|       file       |  type  | line | '
              956  BINARY_ADD       
              958  STORE_FAST               'specifications'

 L. 404       960  LOAD_GLOBAL              isfile
              962  LOAD_FAST                'log_file_name'
              964  CALL_FUNCTION_1       1  ''
          966_968  POP_JUMP_IF_TRUE   1042  'to 1042'

 L. 407       970  LOAD_GLOBAL              open
              972  LOAD_FAST                'log_file_name'
              974  LOAD_STR                 'w'
              976  CALL_FUNCTION_2       2  ''
              978  SETUP_WITH         1032  'to 1032'
              980  STORE_FAST               'log_file'

 L. 410       982  LOAD_FAST                'log_file'
              984  LOAD_METHOD              write
              986  LOAD_GLOBAL              header_row
              988  LOAD_FAST                'specifications'
              990  CALL_FUNCTION_1       1  ''
              992  CALL_METHOD_1         1  ''
              994  POP_TOP          

 L. 413       996  LOAD_FAST                'log_file'
              998  LOAD_METHOD              write

 L. 414      1000  LOAD_GLOBAL              log_row
             1002  LOAD_CONST               1
             1004  LOAD_FAST                'date'
             1006  LOAD_FAST                'time'
             1008  LOAD_FAST                'error_text'
             1010  LOAD_GLOBAL              len
             1012  LOAD_FAST                'spec_center'
             1014  CALL_FUNCTION_1       1  ''
             1016  LOAD_FAST                'justified_python_file'
             1018  LOAD_FAST                'log_type'

 L. 415      1020  LOAD_FAST                'justified_line_python_file'

 L. 414      1022  CALL_FUNCTION_8       8  ''

 L. 413      1024  CALL_METHOD_1         1  ''
             1026  POP_TOP          
             1028  POP_BLOCK        
             1030  BEGIN_FINALLY    
           1032_0  COME_FROM_WITH      978  '978'
             1032  WITH_CLEANUP_START
             1034  WITH_CLEANUP_FINISH
             1036  END_FINALLY      
         1038_1040  JUMP_FORWARD       1392  'to 1392'
           1042_0  COME_FROM           966  '966'

 L. 418      1042  LOAD_GLOBAL              isfile
             1044  LOAD_FAST                'log_file_name'
             1046  CALL_FUNCTION_1       1  ''
         1048_1050  POP_JUMP_IF_FALSE  1392  'to 1392'

 L. 419      1052  LOAD_GLOBAL              open
             1054  LOAD_FAST                'log_file_name'
             1056  LOAD_STR                 'r'
             1058  CALL_FUNCTION_2       2  ''
             1060  SETUP_WITH         1140  'to 1140'
             1062  STORE_FAST               'f'

 L. 420      1064  LOAD_FAST                'f'
             1066  LOAD_METHOD              read
             1068  CALL_METHOD_0         0  ''
             1070  LOAD_METHOD              splitlines
             1072  CALL_METHOD_0         0  ''
             1074  LOAD_CONST               -1
             1076  BINARY_SUBSCR    
             1078  LOAD_STR                 '  |'
             1080  LOAD_STR                 '—'
             1082  LOAD_GLOBAL              len
             1084  LOAD_FAST                'specifications'
             1086  CALL_FUNCTION_1       1  ''
             1088  LOAD_CONST               4
             1090  BINARY_SUBTRACT  
             1092  BINARY_MULTIPLY  
             1094  BINARY_ADD       
             1096  LOAD_STR                 '|'
             1098  BINARY_ADD       
             1100  COMPARE_OP               !=
         1102_1104  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 421      1106  LOAD_GLOBAL              print
             1108  LOAD_GLOBAL              err_temp_func
             1110  LOAD_FAST                'python_file_name'
             1112  LOAD_FAST                'line_python_file'

 L. 422      1114  LOAD_STR                 "previously defined log file size , can't be resized ..."

 L. 421      1116  CALL_FUNCTION_3       3  ''
             1118  CALL_FUNCTION_1       1  ''
             1120  POP_TOP          

 L. 423      1122  POP_BLOCK        
             1124  BEGIN_FINALLY    
             1126  WITH_CLEANUP_START
             1128  WITH_CLEANUP_FINISH
             1130  POP_FINALLY           0  ''
             1132  LOAD_CONST               None
             1134  RETURN_VALUE     
           1136_0  COME_FROM          1102  '1102'
             1136  POP_BLOCK        
             1138  BEGIN_FINALLY    
           1140_0  COME_FROM_WITH     1060  '1060'
             1140  WITH_CLEANUP_START
             1142  WITH_CLEANUP_FINISH
             1144  END_FINALLY      

 L. 426      1146  LOAD_GLOBAL              open
             1148  LOAD_FAST                'log_file_name'
             1150  LOAD_STR                 'r'
             1152  CALL_FUNCTION_2       2  ''
             1154  SETUP_WITH         1244  'to 1244'
             1156  STORE_FAST               'f'

 L. 427      1158  LOAD_FAST                'f'
             1160  LOAD_METHOD              read
             1162  CALL_METHOD_0         0  ''
             1164  LOAD_METHOD              splitlines
             1166  CALL_METHOD_0         0  ''
             1168  LOAD_CONST               -2
             1170  BINARY_SUBSCR    
             1172  LOAD_METHOD              split
             1174  LOAD_STR                 '| '
             1176  LOAD_GLOBAL              str
             1178  LOAD_GLOBAL              datetime
             1180  LOAD_METHOD              now
             1182  CALL_METHOD_0         0  ''
             1184  LOAD_ATTR                year
             1186  CALL_FUNCTION_1       1  ''
             1188  BINARY_ADD       
             1190  LOAD_STR                 '-'
             1192  BINARY_ADD       
             1194  LOAD_CONST               1
             1196  CALL_METHOD_2         2  ''
             1198  LOAD_CONST               0
             1200  BINARY_SUBSCR    
             1202  STORE_FAST               'line_number'

 L. 428      1204  LOAD_FAST                'line_number'
             1206  LOAD_METHOD              replace
             1208  LOAD_STR                 '|'
             1210  LOAD_STR                 ''
             1212  CALL_METHOD_2         2  ''
             1214  STORE_FAST               'line_number'

 L. 429      1216  LOAD_FAST                'line_number'
             1218  LOAD_METHOD              replace
             1220  LOAD_STR                 ' '
             1222  LOAD_STR                 ''
             1224  CALL_METHOD_2         2  ''
             1226  STORE_FAST               'line_number'

 L. 430      1228  LOAD_GLOBAL              int
             1230  LOAD_FAST                'line_number'
             1232  CALL_FUNCTION_1       1  ''
             1234  LOAD_CONST               1
             1236  BINARY_ADD       
             1238  STORE_FAST               'line_number'
             1240  POP_BLOCK        
             1242  BEGIN_FINALLY    
           1244_0  COME_FROM_WITH     1154  '1154'
             1244  WITH_CLEANUP_START
             1246  WITH_CLEANUP_FINISH
             1248  END_FINALLY      

 L. 433      1250  LOAD_GLOBAL              len
             1252  LOAD_GLOBAL              str
             1254  LOAD_FAST                'line_number'
             1256  CALL_FUNCTION_1       1  ''
             1258  CALL_FUNCTION_1       1  ''
             1260  LOAD_CONST               7
             1262  COMPARE_OP               >
         1264_1266  POP_JUMP_IF_FALSE  1288  'to 1288'

 L. 434      1268  LOAD_GLOBAL              print
             1270  LOAD_GLOBAL              err_temp_func
             1272  LOAD_FAST                'python_file_name'
             1274  LOAD_FAST                'line_python_file'

 L. 435      1276  LOAD_STR                 "'size = 5' maximum line number support is 9999999 ..."

 L. 434      1278  CALL_FUNCTION_3       3  ''
             1280  CALL_FUNCTION_1       1  ''
             1282  POP_TOP          

 L. 436      1284  LOAD_CONST               None
             1286  RETURN_VALUE     
           1288_0  COME_FROM          1264  '1264'

 L. 439      1288  LOAD_GLOBAL              len
             1290  LOAD_GLOBAL              str
             1292  LOAD_FAST                'line_number'
             1294  CALL_FUNCTION_1       1  ''
             1296  CALL_FUNCTION_1       1  ''
             1298  LOAD_CONST               7
             1300  COMPARE_OP               <=
         1302_1304  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 440      1306  LOAD_GLOBAL              justify_text
             1308  LOAD_FAST                'line_number'
             1310  LOAD_CONST               7
             1312  CALL_FUNCTION_2       2  ''
             1314  STORE_FAST               'log_file_number'
             1316  JUMP_FORWARD       1338  'to 1338'
           1318_0  COME_FROM          1302  '1302'

 L. 442      1318  LOAD_GLOBAL              print
             1320  LOAD_GLOBAL              err_temp_func
             1322  LOAD_FAST                'python_file_name'
             1324  LOAD_FAST                'line_python_file'

 L. 443      1326  LOAD_STR                 'maximum number to numbering lines support is 9999999 ...'

 L. 442      1328  CALL_FUNCTION_3       3  ''
             1330  CALL_FUNCTION_1       1  ''
             1332  POP_TOP          

 L. 444      1334  LOAD_CONST               None
             1336  RETURN_VALUE     
           1338_0  COME_FROM          1316  '1316'

 L. 447      1338  LOAD_GLOBAL              open
             1340  LOAD_FAST                'log_file_name'
             1342  LOAD_STR                 'a'
             1344  CALL_FUNCTION_2       2  ''
             1346  SETUP_WITH         1386  'to 1386'
             1348  STORE_FAST               'log_file'

 L. 449      1350  LOAD_FAST                'log_file'
             1352  LOAD_METHOD              write
             1354  LOAD_GLOBAL              log_row
             1356  LOAD_FAST                'log_file_number'
             1358  LOAD_FAST                'date'
             1360  LOAD_FAST                'time'
             1362  LOAD_FAST                'error_text'
             1364  LOAD_GLOBAL              len
             1366  LOAD_FAST                'spec_center'
             1368  CALL_FUNCTION_1       1  ''
             1370  LOAD_FAST                'justified_python_file'

 L. 450      1372  LOAD_FAST                'log_type'

 L. 450      1374  LOAD_FAST                'justified_line_python_file'

 L. 449      1376  CALL_FUNCTION_8       8  ''
             1378  CALL_METHOD_1         1  ''
             1380  POP_TOP          
             1382  POP_BLOCK        
             1384  BEGIN_FINALLY    
           1386_0  COME_FROM_WITH     1346  '1346'
             1386  WITH_CLEANUP_START
             1388  WITH_CLEANUP_FINISH
             1390  END_FINALLY      
           1392_0  COME_FROM          1048  '1048'
           1392_1  COME_FROM          1038  '1038'

Parse error at or near `BEGIN_FINALLY' instruction at offset 1124