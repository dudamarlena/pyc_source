# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_sv.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 28890 bytes
from datetime import datetime
import dateutil.relativedelta as relativedelta
from .parse_common import is_numeric, look_for_fractions

def extractnumber_sv(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number
    """
    text = text.lower()
    aWords = text.split()
    and_pass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            val = float(word)
        else:
            if word == 'första':
                val = 1
            else:
                if word == 'andra':
                    val = 2
                else:
                    if word == 'tredje':
                        val = 3
                    else:
                        if word == 'fjärde':
                            val = 4
                        else:
                            if word == 'femte':
                                val = 5
                            else:
                                if word == 'sjätte':
                                    val = 6
                                else:
                                    if is_fractional_sv(word):
                                        val = is_fractional_sv(word)
                                    else:
                                        if word == 'en':
                                            val = 1
        if word == 'ett':
            val = 1
        else:
            if word == 'två':
                val = 2
            else:
                if word == 'tre':
                    val = 3
                else:
                    if word == 'fyra':
                        val = 4
                    else:
                        if word == 'fem':
                            val = 5
                        else:
                            if word == 'sex':
                                val = 6
                            else:
                                if word == 'sju':
                                    val = 7
                                else:
                                    if word == 'åtta':
                                        val = 8
                                    else:
                                        if word == 'nio':
                                            val = 9
                                        else:
                                            if word == 'tio':
                                                val = 10
                                            else:
                                                if val:
                                                    if count < len(aWords) - 1:
                                                        wordNext = aWords[(count + 1)]
                                                    else:
                                                        wordNext = ''
                                                    valNext = is_fractional_sv(wordNext)
                                                    if valNext:
                                                        val = val * valNext
                                                        aWords[count + 1] = ''
                                                if not val:
                                                    aPieces = word.split('/')
                                                    if look_for_fractions(aPieces):
                                                        val = float(aPieces[0]) / float(aPieces[1])
                                                    else:
                                                        if and_pass:
                                                            val = valPreAnd
                                                            break
                                                        else:
                                                            count += 1
                                                            continue
                                            aWords[count] = ''
        if and_pass:
            aWords[count - 1] = ''
            val += valPreAnd
        else:
            if count + 1 < len(aWords) and aWords[(count + 1)] == 'och':
                and_pass = True
                valPreAnd = val
                val = False
                count += 2
                continue
            else:
                if count + 2 < len(aWords):
                    if aWords[(count + 2)] == 'och':
                        and_pass = True
                        valPreAnd = val
                        val = False
                        count += 3
                        continue
                break

    return val or False


def extract_datetime_sv--- This code section failed: ---

 L. 129         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_sv.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 149         8  LOAD_CLOSURE             'datestr'
               10  LOAD_CLOSURE             'dayOffset'
               12  LOAD_CLOSURE             'found'
               14  LOAD_CLOSURE             'hrAbs'
               16  LOAD_CLOSURE             'hrOffset'
               18  LOAD_CLOSURE             'minAbs'
               20  LOAD_CLOSURE             'minOffset'
               22  LOAD_CLOSURE             'monthOffset'
               24  LOAD_CLOSURE             'secOffset'
               26  LOAD_CLOSURE             'timeStr'
               28  LOAD_CLOSURE             'yearOffset'
               30  BUILD_TUPLE_11       11 
               32  LOAD_CODE                <code_object date_found>
               34  LOAD_STR                 'extract_datetime_sv.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 159        40  LOAD_FAST                'string'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'currentDate'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 160        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 162        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 163        60  LOAD_CONST               False
               62  STORE_FAST               'daySpecified'

 L. 164        64  LOAD_CONST               False
               66  STORE_DEREF              'dayOffset'

 L. 165        68  LOAD_CONST               0
               70  STORE_DEREF              'monthOffset'

 L. 166        72  LOAD_CONST               0
               74  STORE_DEREF              'yearOffset'

 L. 167        76  LOAD_FAST                'currentDate'
               78  STORE_FAST               'dateNow'

 L. 168        80  LOAD_FAST                'dateNow'
               82  LOAD_METHOD              strftime
               84  LOAD_STR                 '%w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'today'

 L. 169        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%Y'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'currentYear'

 L. 170       100  LOAD_CONST               False
              102  STORE_FAST               'fromFlag'

 L. 171       104  LOAD_STR                 ''
              106  STORE_DEREF              'datestr'

 L. 172       108  LOAD_CONST               False
              110  STORE_FAST               'hasYear'

 L. 173       112  LOAD_STR                 ''
              114  STORE_FAST               'timeQualifier'

 L. 175       116  LOAD_STR                 'morgon'
              118  LOAD_STR                 'förmiddag'
              120  LOAD_STR                 'eftermiddag'
              122  LOAD_STR                 'kväll'
              124  BUILD_LIST_4          4 
              126  STORE_FAST               'timeQualifiersList'

 L. 176       128  LOAD_STR                 'på'
              130  LOAD_STR                 'i'
              132  LOAD_STR                 'den här'
              134  LOAD_STR                 'kring'
              136  LOAD_STR                 'efter'
              138  BUILD_LIST_5          5 
              140  STORE_FAST               'markers'

 L. 177       142  LOAD_STR                 'måndag'
              144  LOAD_STR                 'tisdag'
              146  LOAD_STR                 'onsdag'
              148  LOAD_STR                 'torsdag'

 L. 178       150  LOAD_STR                 'fredag'
              152  LOAD_STR                 'lördag'
              154  LOAD_STR                 'söndag'
              156  BUILD_LIST_7          7 
              158  STORE_FAST               'days'

 L. 179       160  LOAD_STR                 'januari'
              162  LOAD_STR                 'februari'
              164  LOAD_STR                 'mars'
              166  LOAD_STR                 'april'
              168  LOAD_STR                 'maj'
              170  LOAD_STR                 'juni'

 L. 180       172  LOAD_STR                 'juli'
              174  LOAD_STR                 'augusti'
              176  LOAD_STR                 'september'
              178  LOAD_STR                 'oktober'
              180  LOAD_STR                 'november'

 L. 181       182  LOAD_STR                 'december'
              184  BUILD_LIST_12        12 
              186  STORE_FAST               'months'

 L. 182       188  LOAD_STR                 'jan'
              190  LOAD_STR                 'feb'
              192  LOAD_STR                 'mar'
              194  LOAD_STR                 'apr'
              196  LOAD_STR                 'may'
              198  LOAD_STR                 'june'
              200  LOAD_STR                 'july'
              202  LOAD_STR                 'aug'

 L. 183       204  LOAD_STR                 'sept'
              206  LOAD_STR                 'oct'
              208  LOAD_STR                 'nov'
              210  LOAD_STR                 'dec'
              212  BUILD_LIST_12        12 
              214  STORE_FAST               'monthsShort'

 L. 185       216  LOAD_FAST                'clean_string'
              218  LOAD_FAST                'string'
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  STORE_FAST               'words'

 L. 187   224_226  SETUP_LOOP         1924  'to 1924'
              228  LOAD_GLOBAL              enumerate
              230  LOAD_FAST                'words'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  GET_ITER         
            236_0  COME_FROM          1784  '1784'
          236_238  FOR_ITER           1922  'to 1922'
              240  UNPACK_SEQUENCE_2     2 
              242  STORE_FAST               'idx'
              244  STORE_FAST               'word'

 L. 188       246  LOAD_FAST                'word'
              248  LOAD_STR                 ''
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   258  'to 258'

 L. 189       256  CONTINUE            236  'to 236'
            258_0  COME_FROM           252  '252'

 L. 190       258  LOAD_FAST                'idx'
              260  LOAD_CONST               1
              262  COMPARE_OP               >
          264_266  POP_JUMP_IF_FALSE   280  'to 280'
              268  LOAD_FAST                'words'
              270  LOAD_FAST                'idx'
              272  LOAD_CONST               2
              274  BINARY_SUBTRACT  
              276  BINARY_SUBSCR    
              278  JUMP_FORWARD        282  'to 282'
            280_0  COME_FROM           264  '264'
              280  LOAD_STR                 ''
            282_0  COME_FROM           278  '278'
              282  STORE_FAST               'wordPrevPrev'

 L. 191       284  LOAD_FAST                'idx'
              286  LOAD_CONST               0
              288  COMPARE_OP               >
          290_292  POP_JUMP_IF_FALSE   306  'to 306'
              294  LOAD_FAST                'words'
              296  LOAD_FAST                'idx'
              298  LOAD_CONST               1
              300  BINARY_SUBTRACT  
              302  BINARY_SUBSCR    
              304  JUMP_FORWARD        308  'to 308'
            306_0  COME_FROM           290  '290'
              306  LOAD_STR                 ''
            308_0  COME_FROM           304  '304'
              308  STORE_FAST               'wordPrev'

 L. 192       310  LOAD_FAST                'idx'
              312  LOAD_CONST               1
              314  BINARY_ADD       
              316  LOAD_GLOBAL              len
              318  LOAD_FAST                'words'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  COMPARE_OP               <
          324_326  POP_JUMP_IF_FALSE   340  'to 340'
              328  LOAD_FAST                'words'
              330  LOAD_FAST                'idx'
              332  LOAD_CONST               1
              334  BINARY_ADD       
              336  BINARY_SUBSCR    
              338  JUMP_FORWARD        342  'to 342'
            340_0  COME_FROM           324  '324'
              340  LOAD_STR                 ''
            342_0  COME_FROM           338  '338'
              342  STORE_FAST               'wordNext'

 L. 193       344  LOAD_FAST                'idx'
              346  LOAD_CONST               2
              348  BINARY_ADD       
              350  LOAD_GLOBAL              len
              352  LOAD_FAST                'words'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  COMPARE_OP               <
          358_360  POP_JUMP_IF_FALSE   374  'to 374'
              362  LOAD_FAST                'words'
              364  LOAD_FAST                'idx'
              366  LOAD_CONST               2
              368  BINARY_ADD       
              370  BINARY_SUBSCR    
              372  JUMP_FORWARD        376  'to 376'
            374_0  COME_FROM           358  '358'
              374  LOAD_STR                 ''
            376_0  COME_FROM           372  '372'
              376  STORE_FAST               'wordNextNext'

 L. 196       378  LOAD_FAST                'word'
              380  LOAD_METHOD              rstrip
              382  LOAD_STR                 's'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  STORE_FAST               'word'

 L. 197       388  LOAD_FAST                'idx'
              390  STORE_FAST               'start'

 L. 198       392  LOAD_CONST               0
              394  STORE_FAST               'used'

 L. 200       396  LOAD_FAST                'word'
              398  LOAD_FAST                'timeQualifiersList'
              400  COMPARE_OP               in
          402_404  POP_JUMP_IF_FALSE   414  'to 414'

 L. 201       406  LOAD_FAST                'word'
              408  STORE_FAST               'timeQualifier'
          410_412  JUMP_FORWARD       1466  'to 1466'
            414_0  COME_FROM           402  '402'

 L. 203       414  LOAD_FAST                'word'
              416  LOAD_STR                 'idag'
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   446  'to 446'
              424  LOAD_FAST                'fromFlag'
          426_428  POP_JUMP_IF_TRUE    446  'to 446'

 L. 204       430  LOAD_CONST               0
              432  STORE_DEREF              'dayOffset'

 L. 205       434  LOAD_FAST                'used'
              436  LOAD_CONST               1
              438  INPLACE_ADD      
              440  STORE_FAST               'used'
          442_444  JUMP_FORWARD       1466  'to 1466'
            446_0  COME_FROM           426  '426'
            446_1  COME_FROM           420  '420'

 L. 206       446  LOAD_FAST                'word'
              448  LOAD_STR                 'imorgon'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   478  'to 478'
              456  LOAD_FAST                'fromFlag'
          458_460  POP_JUMP_IF_TRUE    478  'to 478'

 L. 207       462  LOAD_CONST               1
              464  STORE_DEREF              'dayOffset'

 L. 208       466  LOAD_FAST                'used'
              468  LOAD_CONST               1
              470  INPLACE_ADD      
              472  STORE_FAST               'used'
          474_476  JUMP_FORWARD       1466  'to 1466'
            478_0  COME_FROM           458  '458'
            478_1  COME_FROM           452  '452'

 L. 209       478  LOAD_FAST                'word'
              480  LOAD_STR                 'morgondagen'
              482  COMPARE_OP               ==
          484_486  POP_JUMP_IF_TRUE    504  'to 504'
              488  LOAD_FAST                'word'
              490  LOAD_STR                 'morgondagens'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   520  'to 520'
              498  LOAD_FAST                'fromFlag'
          500_502  POP_JUMP_IF_TRUE    520  'to 520'
            504_0  COME_FROM           484  '484'

 L. 210       504  LOAD_CONST               1
              506  STORE_DEREF              'dayOffset'

 L. 211       508  LOAD_FAST                'used'
              510  LOAD_CONST               1
              512  INPLACE_ADD      
              514  STORE_FAST               'used'
          516_518  JUMP_FORWARD       1466  'to 1466'
            520_0  COME_FROM           500  '500'
            520_1  COME_FROM           494  '494'

 L. 212       520  LOAD_FAST                'word'
              522  LOAD_STR                 'övermorgon'
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   552  'to 552'
              530  LOAD_FAST                'fromFlag'
          532_534  POP_JUMP_IF_TRUE    552  'to 552'

 L. 213       536  LOAD_CONST               2
              538  STORE_DEREF              'dayOffset'

 L. 214       540  LOAD_FAST                'used'
              542  LOAD_CONST               1
              544  INPLACE_ADD      
              546  STORE_FAST               'used'
          548_550  JUMP_FORWARD       1466  'to 1466'
            552_0  COME_FROM           532  '532'
            552_1  COME_FROM           526  '526'

 L. 216       552  LOAD_FAST                'word'
              554  LOAD_STR                 'dag'
              556  COMPARE_OP               ==
          558_560  POP_JUMP_IF_TRUE    572  'to 572'
              562  LOAD_FAST                'word'
              564  LOAD_STR                 'dagar'
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_FALSE   614  'to 614'
            572_0  COME_FROM           558  '558'

 L. 217       572  LOAD_FAST                'wordPrev'
              574  LOAD_CONST               0
              576  BINARY_SUBSCR    
              578  LOAD_METHOD              isdigit
              580  CALL_METHOD_0         0  '0 positional arguments'
          582_584  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 218       586  LOAD_DEREF               'dayOffset'
              588  LOAD_GLOBAL              int
              590  LOAD_FAST                'wordPrev'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  INPLACE_ADD      
              596  STORE_DEREF              'dayOffset'

 L. 219       598  LOAD_FAST                'start'
              600  LOAD_CONST               1
              602  INPLACE_SUBTRACT 
              604  STORE_FAST               'start'

 L. 220       606  LOAD_CONST               2
              608  STORE_FAST               'used'
          610_612  JUMP_FORWARD       1466  'to 1466'
            614_0  COME_FROM           568  '568'

 L. 221       614  LOAD_FAST                'word'
              616  LOAD_STR                 'vecka'
              618  COMPARE_OP               ==
          620_622  POP_JUMP_IF_TRUE    640  'to 640'
              624  LOAD_FAST                'word'
              626  LOAD_STR                 'veckor'
              628  COMPARE_OP               ==
          630_632  POP_JUMP_IF_FALSE   742  'to 742'
              634  LOAD_FAST                'fromFlag'
          636_638  POP_JUMP_IF_TRUE    742  'to 742'
            640_0  COME_FROM           620  '620'

 L. 222       640  LOAD_FAST                'wordPrev'
              642  LOAD_CONST               0
              644  BINARY_SUBSCR    
              646  LOAD_METHOD              isdigit
              648  CALL_METHOD_0         0  '0 positional arguments'
          650_652  POP_JUMP_IF_FALSE   684  'to 684'

 L. 223       654  LOAD_DEREF               'dayOffset'
              656  LOAD_GLOBAL              int
              658  LOAD_FAST                'wordPrev'
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  LOAD_CONST               7
              664  BINARY_MULTIPLY  
              666  INPLACE_ADD      
              668  STORE_DEREF              'dayOffset'

 L. 224       670  LOAD_FAST                'start'
              672  LOAD_CONST               1
              674  INPLACE_SUBTRACT 
              676  STORE_FAST               'start'

 L. 225       678  LOAD_CONST               2
              680  STORE_FAST               'used'
              682  JUMP_FORWARD       1466  'to 1466'
            684_0  COME_FROM           650  '650'

 L. 226       684  LOAD_FAST                'wordPrev'
              686  LOAD_STR                 'nästa'
              688  COMPARE_OP               ==
          690_692  POP_JUMP_IF_FALSE   712  'to 712'

 L. 227       694  LOAD_CONST               7
              696  STORE_DEREF              'dayOffset'

 L. 228       698  LOAD_FAST                'start'
              700  LOAD_CONST               1
              702  INPLACE_SUBTRACT 
              704  STORE_FAST               'start'

 L. 229       706  LOAD_CONST               2
              708  STORE_FAST               'used'
              710  JUMP_FORWARD       1466  'to 1466'
            712_0  COME_FROM           690  '690'

 L. 230       712  LOAD_FAST                'wordPrev'
              714  LOAD_STR                 'förra'
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 231       722  LOAD_CONST               -7
              724  STORE_DEREF              'dayOffset'

 L. 232       726  LOAD_FAST                'start'
              728  LOAD_CONST               1
              730  INPLACE_SUBTRACT 
              732  STORE_FAST               'start'

 L. 233       734  LOAD_CONST               2
              736  STORE_FAST               'used'
          738_740  JUMP_FORWARD       1466  'to 1466'
            742_0  COME_FROM           636  '636'
            742_1  COME_FROM           630  '630'

 L. 235       742  LOAD_FAST                'word'
              744  LOAD_STR                 'månad'
              746  COMPARE_OP               ==
          748_750  POP_JUMP_IF_FALSE   852  'to 852'
              752  LOAD_FAST                'fromFlag'
          754_756  POP_JUMP_IF_TRUE    852  'to 852'

 L. 236       758  LOAD_FAST                'wordPrev'
              760  LOAD_CONST               0
              762  BINARY_SUBSCR    
              764  LOAD_METHOD              isdigit
              766  CALL_METHOD_0         0  '0 positional arguments'
          768_770  POP_JUMP_IF_FALSE   794  'to 794'

 L. 237       772  LOAD_GLOBAL              int
              774  LOAD_FAST                'wordPrev'
              776  CALL_FUNCTION_1       1  '1 positional argument'
              778  STORE_DEREF              'monthOffset'

 L. 238       780  LOAD_FAST                'start'
              782  LOAD_CONST               1
              784  INPLACE_SUBTRACT 
              786  STORE_FAST               'start'

 L. 239       788  LOAD_CONST               2
              790  STORE_FAST               'used'
              792  JUMP_FORWARD       1466  'to 1466'
            794_0  COME_FROM           768  '768'

 L. 240       794  LOAD_FAST                'wordPrev'
              796  LOAD_STR                 'nästa'
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   822  'to 822'

 L. 241       804  LOAD_CONST               1
              806  STORE_DEREF              'monthOffset'

 L. 242       808  LOAD_FAST                'start'
              810  LOAD_CONST               1
              812  INPLACE_SUBTRACT 
              814  STORE_FAST               'start'

 L. 243       816  LOAD_CONST               2
              818  STORE_FAST               'used'
              820  JUMP_FORWARD       1466  'to 1466'
            822_0  COME_FROM           800  '800'

 L. 244       822  LOAD_FAST                'wordPrev'
              824  LOAD_STR                 'förra'
              826  COMPARE_OP               ==
          828_830  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 245       832  LOAD_CONST               -1
              834  STORE_DEREF              'monthOffset'

 L. 246       836  LOAD_FAST                'start'
              838  LOAD_CONST               1
              840  INPLACE_SUBTRACT 
              842  STORE_FAST               'start'

 L. 247       844  LOAD_CONST               2
              846  STORE_FAST               'used'
          848_850  JUMP_FORWARD       1466  'to 1466'
            852_0  COME_FROM           754  '754'
            852_1  COME_FROM           748  '748'

 L. 249       852  LOAD_FAST                'word'
              854  LOAD_STR                 'år'
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   962  'to 962'
              862  LOAD_FAST                'fromFlag'
          864_866  POP_JUMP_IF_TRUE    962  'to 962'

 L. 250       868  LOAD_FAST                'wordPrev'
              870  LOAD_CONST               0
              872  BINARY_SUBSCR    
              874  LOAD_METHOD              isdigit
              876  CALL_METHOD_0         0  '0 positional arguments'
          878_880  POP_JUMP_IF_FALSE   904  'to 904'

 L. 251       882  LOAD_GLOBAL              int
              884  LOAD_FAST                'wordPrev'
              886  CALL_FUNCTION_1       1  '1 positional argument'
              888  STORE_DEREF              'yearOffset'

 L. 252       890  LOAD_FAST                'start'
              892  LOAD_CONST               1
              894  INPLACE_SUBTRACT 
              896  STORE_FAST               'start'

 L. 253       898  LOAD_CONST               2
              900  STORE_FAST               'used'
              902  JUMP_FORWARD       1466  'to 1466'
            904_0  COME_FROM           878  '878'

 L. 254       904  LOAD_FAST                'wordPrev'
              906  LOAD_STR                 'nästa'
              908  COMPARE_OP               ==
          910_912  POP_JUMP_IF_FALSE   932  'to 932'

 L. 255       914  LOAD_CONST               1
              916  STORE_DEREF              'yearOffset'

 L. 256       918  LOAD_FAST                'start'
              920  LOAD_CONST               1
              922  INPLACE_SUBTRACT 
              924  STORE_FAST               'start'

 L. 257       926  LOAD_CONST               2
              928  STORE_FAST               'used'
              930  JUMP_FORWARD       1466  'to 1466'
            932_0  COME_FROM           910  '910'

 L. 258       932  LOAD_FAST                'wordPrev'
              934  LOAD_STR                 'förra'
              936  COMPARE_OP               ==
          938_940  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 259       942  LOAD_CONST               -1
              944  STORE_DEREF              'yearOffset'

 L. 260       946  LOAD_FAST                'start'
              948  LOAD_CONST               1
              950  INPLACE_SUBTRACT 
              952  STORE_FAST               'start'

 L. 261       954  LOAD_CONST               2
              956  STORE_FAST               'used'
          958_960  JUMP_FORWARD       1466  'to 1466'
            962_0  COME_FROM           864  '864'
            962_1  COME_FROM           858  '858'

 L. 264       962  LOAD_FAST                'word'
              964  LOAD_FAST                'days'
              966  COMPARE_OP               in
          968_970  POP_JUMP_IF_FALSE  1100  'to 1100'
              972  LOAD_FAST                'fromFlag'
          974_976  POP_JUMP_IF_TRUE   1100  'to 1100'

 L. 265       978  LOAD_FAST                'days'
              980  LOAD_METHOD              index
              982  LOAD_FAST                'word'
              984  CALL_METHOD_1         1  '1 positional argument'
              986  STORE_FAST               'd'

 L. 266       988  LOAD_FAST                'd'
              990  LOAD_CONST               1
              992  BINARY_ADD       
              994  LOAD_GLOBAL              int
              996  LOAD_FAST                'today'
              998  CALL_FUNCTION_1       1  '1 positional argument'
             1000  BINARY_SUBTRACT  
             1002  STORE_DEREF              'dayOffset'

 L. 267      1004  LOAD_CONST               1
             1006  STORE_FAST               'used'

 L. 268      1008  LOAD_DEREF               'dayOffset'
             1010  LOAD_CONST               0
             1012  COMPARE_OP               <
         1014_1016  POP_JUMP_IF_FALSE  1026  'to 1026'

 L. 269      1018  LOAD_DEREF               'dayOffset'
             1020  LOAD_CONST               7
             1022  INPLACE_ADD      
             1024  STORE_DEREF              'dayOffset'
           1026_0  COME_FROM          1014  '1014'

 L. 270      1026  LOAD_FAST                'wordPrev'
             1028  LOAD_STR                 'nästa'
             1030  COMPARE_OP               ==
         1032_1034  POP_JUMP_IF_FALSE  1062  'to 1062'

 L. 271      1036  LOAD_DEREF               'dayOffset'
             1038  LOAD_CONST               7
             1040  INPLACE_ADD      
             1042  STORE_DEREF              'dayOffset'

 L. 272      1044  LOAD_FAST                'used'
             1046  LOAD_CONST               1
             1048  INPLACE_ADD      
             1050  STORE_FAST               'used'

 L. 273      1052  LOAD_FAST                'start'
             1054  LOAD_CONST               1
             1056  INPLACE_SUBTRACT 
             1058  STORE_FAST               'start'
             1060  JUMP_FORWARD       1466  'to 1466'
           1062_0  COME_FROM          1032  '1032'

 L. 274      1062  LOAD_FAST                'wordPrev'
             1064  LOAD_STR                 'förra'
             1066  COMPARE_OP               ==
         1068_1070  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 275      1072  LOAD_DEREF               'dayOffset'
             1074  LOAD_CONST               7
             1076  INPLACE_SUBTRACT 
             1078  STORE_DEREF              'dayOffset'

 L. 276      1080  LOAD_FAST                'used'
             1082  LOAD_CONST               1
             1084  INPLACE_ADD      
             1086  STORE_FAST               'used'

 L. 277      1088  LOAD_FAST                'start'
             1090  LOAD_CONST               1
             1092  INPLACE_SUBTRACT 
             1094  STORE_FAST               'start'
         1096_1098  JUMP_FORWARD       1466  'to 1466'
           1100_0  COME_FROM           974  '974'
           1100_1  COME_FROM           968  '968'

 L. 279      1100  LOAD_FAST                'word'
             1102  LOAD_FAST                'months'
             1104  COMPARE_OP               in
         1106_1108  POP_JUMP_IF_TRUE   1126  'to 1126'
             1110  LOAD_FAST                'word'
             1112  LOAD_FAST                'monthsShort'
             1114  COMPARE_OP               in
         1116_1118  POP_JUMP_IF_FALSE  1466  'to 1466'
             1120  LOAD_FAST                'fromFlag'
         1122_1124  POP_JUMP_IF_TRUE   1466  'to 1466'
           1126_0  COME_FROM          1106  '1106'

 L. 280      1126  SETUP_EXCEPT       1142  'to 1142'

 L. 281      1128  LOAD_FAST                'months'
             1130  LOAD_METHOD              index
             1132  LOAD_FAST                'word'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'm'
             1138  POP_BLOCK        
             1140  JUMP_FORWARD       1174  'to 1174'
           1142_0  COME_FROM_EXCEPT   1126  '1126'

 L. 282      1142  DUP_TOP          
             1144  LOAD_GLOBAL              ValueError
             1146  COMPARE_OP               exception-match
         1148_1150  POP_JUMP_IF_FALSE  1172  'to 1172'
             1152  POP_TOP          
             1154  POP_TOP          
             1156  POP_TOP          

 L. 283      1158  LOAD_FAST                'monthsShort'
             1160  LOAD_METHOD              index
             1162  LOAD_FAST                'word'
             1164  CALL_METHOD_1         1  '1 positional argument'
             1166  STORE_FAST               'm'
             1168  POP_EXCEPT       
             1170  JUMP_FORWARD       1174  'to 1174'
           1172_0  COME_FROM          1148  '1148'
             1172  END_FINALLY      
           1174_0  COME_FROM          1170  '1170'
           1174_1  COME_FROM          1140  '1140'

 L. 284      1174  LOAD_FAST                'used'
             1176  LOAD_CONST               1
             1178  INPLACE_ADD      
             1180  STORE_FAST               'used'

 L. 285      1182  LOAD_FAST                'months'
             1184  LOAD_FAST                'm'
             1186  BINARY_SUBSCR    
             1188  STORE_DEREF              'datestr'

 L. 286      1190  LOAD_FAST                'wordPrev'
         1192_1194  POP_JUMP_IF_FALSE  1376  'to 1376'
             1196  LOAD_FAST                'wordPrev'
             1198  LOAD_CONST               0
             1200  BINARY_SUBSCR    
             1202  LOAD_METHOD              isdigit
             1204  CALL_METHOD_0         0  '0 positional arguments'
         1206_1208  POP_JUMP_IF_TRUE   1234  'to 1234'

 L. 287      1210  LOAD_FAST                'wordPrev'
             1212  LOAD_STR                 'of'
             1214  COMPARE_OP               ==
         1216_1218  POP_JUMP_IF_FALSE  1376  'to 1376'
             1220  LOAD_FAST                'wordPrevPrev'
             1222  LOAD_CONST               0
             1224  BINARY_SUBSCR    
             1226  LOAD_METHOD              isdigit
             1228  CALL_METHOD_0         0  '0 positional arguments'
         1230_1232  POP_JUMP_IF_FALSE  1376  'to 1376'
           1234_0  COME_FROM          1206  '1206'

 L. 288      1234  LOAD_FAST                'wordPrev'
             1236  LOAD_STR                 'of'
             1238  COMPARE_OP               ==
         1240_1242  POP_JUMP_IF_FALSE  1296  'to 1296'
             1244  LOAD_FAST                'wordPrevPrev'
             1246  LOAD_CONST               0
             1248  BINARY_SUBSCR    
             1250  LOAD_METHOD              isdigit
             1252  CALL_METHOD_0         0  '0 positional arguments'
         1254_1256  POP_JUMP_IF_FALSE  1296  'to 1296'

 L. 289      1258  LOAD_DEREF               'datestr'
             1260  LOAD_STR                 ' '
             1262  LOAD_FAST                'words'
             1264  LOAD_FAST                'idx'
             1266  LOAD_CONST               2
             1268  BINARY_SUBTRACT  
             1270  BINARY_SUBSCR    
             1272  BINARY_ADD       
             1274  INPLACE_ADD      
             1276  STORE_DEREF              'datestr'

 L. 290      1278  LOAD_FAST                'used'
             1280  LOAD_CONST               1
             1282  INPLACE_ADD      
             1284  STORE_FAST               'used'

 L. 291      1286  LOAD_FAST                'start'
             1288  LOAD_CONST               1
             1290  INPLACE_SUBTRACT 
             1292  STORE_FAST               'start'
             1294  JUMP_FORWARD       1308  'to 1308'
           1296_0  COME_FROM          1254  '1254'
           1296_1  COME_FROM          1240  '1240'

 L. 293      1296  LOAD_DEREF               'datestr'
             1298  LOAD_STR                 ' '
             1300  LOAD_FAST                'wordPrev'
             1302  BINARY_ADD       
             1304  INPLACE_ADD      
             1306  STORE_DEREF              'datestr'
           1308_0  COME_FROM          1294  '1294'

 L. 294      1308  LOAD_FAST                'start'
             1310  LOAD_CONST               1
             1312  INPLACE_SUBTRACT 
             1314  STORE_FAST               'start'

 L. 295      1316  LOAD_FAST                'used'
             1318  LOAD_CONST               1
             1320  INPLACE_ADD      
             1322  STORE_FAST               'used'

 L. 296      1324  LOAD_FAST                'wordNext'
         1326_1328  POP_JUMP_IF_FALSE  1370  'to 1370'
             1330  LOAD_FAST                'wordNext'
             1332  LOAD_CONST               0
             1334  BINARY_SUBSCR    
             1336  LOAD_METHOD              isdigit
             1338  CALL_METHOD_0         0  '0 positional arguments'
         1340_1342  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 297      1344  LOAD_DEREF               'datestr'
             1346  LOAD_STR                 ' '
             1348  LOAD_FAST                'wordNext'
             1350  BINARY_ADD       
             1352  INPLACE_ADD      
             1354  STORE_DEREF              'datestr'

 L. 298      1356  LOAD_FAST                'used'
             1358  LOAD_CONST               1
             1360  INPLACE_ADD      
             1362  STORE_FAST               'used'

 L. 299      1364  LOAD_CONST               True
             1366  STORE_FAST               'hasYear'
             1368  JUMP_FORWARD       1374  'to 1374'
           1370_0  COME_FROM          1340  '1340'
           1370_1  COME_FROM          1326  '1326'

 L. 301      1370  LOAD_CONST               False
             1372  STORE_FAST               'hasYear'
           1374_0  COME_FROM          1368  '1368'
             1374  JUMP_FORWARD       1466  'to 1466'
           1376_0  COME_FROM          1230  '1230'
           1376_1  COME_FROM          1216  '1216'
           1376_2  COME_FROM          1192  '1192'

 L. 303      1376  LOAD_FAST                'wordNext'
         1378_1380  POP_JUMP_IF_FALSE  1466  'to 1466'
             1382  LOAD_FAST                'wordNext'
             1384  LOAD_CONST               0
             1386  BINARY_SUBSCR    
             1388  LOAD_METHOD              isdigit
             1390  CALL_METHOD_0         0  '0 positional arguments'
         1392_1394  POP_JUMP_IF_FALSE  1466  'to 1466'

 L. 304      1396  LOAD_DEREF               'datestr'
             1398  LOAD_STR                 ' '
             1400  LOAD_FAST                'wordNext'
             1402  BINARY_ADD       
             1404  INPLACE_ADD      
             1406  STORE_DEREF              'datestr'
           1408_0  COME_FROM           902  '902'
           1408_1  COME_FROM           792  '792'
           1408_2  COME_FROM           682  '682'

 L. 305      1408  LOAD_FAST                'used'
             1410  LOAD_CONST               1
             1412  INPLACE_ADD      
             1414  STORE_FAST               'used'

 L. 306      1416  LOAD_FAST                'wordNextNext'
         1418_1420  POP_JUMP_IF_FALSE  1462  'to 1462'
             1422  LOAD_FAST                'wordNextNext'
             1424  LOAD_CONST               0
             1426  BINARY_SUBSCR    
           1428_0  COME_FROM          1060  '1060'
             1428  LOAD_METHOD              isdigit
             1430  CALL_METHOD_0         0  '0 positional arguments'
         1432_1434  POP_JUMP_IF_FALSE  1462  'to 1462'
           1436_0  COME_FROM           930  '930'
           1436_1  COME_FROM           820  '820'
           1436_2  COME_FROM           710  '710'

 L. 307      1436  LOAD_DEREF               'datestr'
             1438  LOAD_STR                 ' '
             1440  LOAD_FAST                'wordNextNext'
             1442  BINARY_ADD       
             1444  INPLACE_ADD      
             1446  STORE_DEREF              'datestr'

 L. 308      1448  LOAD_FAST                'used'
             1450  LOAD_CONST               1
             1452  INPLACE_ADD      
             1454  STORE_FAST               'used'

 L. 309      1456  LOAD_CONST               True
             1458  STORE_FAST               'hasYear'
             1460  JUMP_FORWARD       1466  'to 1466'
           1462_0  COME_FROM          1432  '1432'
           1462_1  COME_FROM          1418  '1418'

 L. 311      1462  LOAD_CONST               False
             1464  STORE_FAST               'hasYear'
           1466_0  COME_FROM          1460  '1460'
           1466_1  COME_FROM          1392  '1392'
           1466_2  COME_FROM          1378  '1378'
           1466_3  COME_FROM          1374  '1374'
           1466_4  COME_FROM          1122  '1122'
           1466_5  COME_FROM          1116  '1116'
           1466_6  COME_FROM          1096  '1096'
           1466_7  COME_FROM          1068  '1068'
           1466_8  COME_FROM           958  '958'
           1466_9  COME_FROM           938  '938'
          1466_10  COME_FROM           848  '848'
          1466_11  COME_FROM           828  '828'
          1466_12  COME_FROM           738  '738'
          1466_13  COME_FROM           718  '718'
          1466_14  COME_FROM           610  '610'
          1466_15  COME_FROM           582  '582'
          1466_16  COME_FROM           548  '548'
          1466_17  COME_FROM           516  '516'
          1466_18  COME_FROM           474  '474'
          1466_19  COME_FROM           442  '442'
          1466_20  COME_FROM           410  '410'

 L. 314      1466  LOAD_FAST                'days'
             1468  LOAD_FAST                'months'
             1470  BINARY_ADD       
             1472  LOAD_FAST                'monthsShort'
             1474  BINARY_ADD       
             1476  STORE_FAST               'validFollowups'

 L. 315      1478  LOAD_FAST                'validFollowups'
             1480  LOAD_METHOD              append
             1482  LOAD_STR                 'idag'
             1484  CALL_METHOD_1         1  '1 positional argument'
             1486  POP_TOP          

 L. 316      1488  LOAD_FAST                'validFollowups'
             1490  LOAD_METHOD              append
             1492  LOAD_STR                 'imorgon'
             1494  CALL_METHOD_1         1  '1 positional argument'
             1496  POP_TOP          

 L. 317      1498  LOAD_FAST                'validFollowups'
             1500  LOAD_METHOD              append
             1502  LOAD_STR                 'nästa'
             1504  CALL_METHOD_1         1  '1 positional argument'
             1506  POP_TOP          

 L. 318      1508  LOAD_FAST                'validFollowups'
             1510  LOAD_METHOD              append
             1512  LOAD_STR                 'förra'
             1514  CALL_METHOD_1         1  '1 positional argument'
             1516  POP_TOP          

 L. 319      1518  LOAD_FAST                'validFollowups'
             1520  LOAD_METHOD              append
             1522  LOAD_STR                 'nu'
             1524  CALL_METHOD_1         1  '1 positional argument'
             1526  POP_TOP          

 L. 320      1528  LOAD_FAST                'word'
             1530  LOAD_STR                 'från'
             1532  COMPARE_OP               ==
         1534_1536  POP_JUMP_IF_TRUE   1548  'to 1548'
             1538  LOAD_FAST                'word'
             1540  LOAD_STR                 'efter'
             1542  COMPARE_OP               ==
         1544_1546  POP_JUMP_IF_FALSE  1778  'to 1778'
           1548_0  COME_FROM          1534  '1534'
             1548  LOAD_FAST                'wordNext'
             1550  LOAD_FAST                'validFollowups'
             1552  COMPARE_OP               in
         1554_1556  POP_JUMP_IF_FALSE  1778  'to 1778'

 L. 321      1558  LOAD_CONST               2
             1560  STORE_FAST               'used'

 L. 322      1562  LOAD_CONST               True
             1564  STORE_FAST               'fromFlag'

 L. 323      1566  LOAD_FAST                'wordNext'
             1568  LOAD_STR                 'imorgon'
             1570  COMPARE_OP               ==
         1572_1574  POP_JUMP_IF_FALSE  1586  'to 1586'

 L. 324      1576  LOAD_DEREF               'dayOffset'
             1578  LOAD_CONST               1
             1580  INPLACE_ADD      
             1582  STORE_DEREF              'dayOffset'
             1584  JUMP_FORWARD       1778  'to 1778'
           1586_0  COME_FROM          1572  '1572'

 L. 325      1586  LOAD_FAST                'wordNext'
             1588  LOAD_FAST                'days'
             1590  COMPARE_OP               in
         1592_1594  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 326      1596  LOAD_FAST                'days'
             1598  LOAD_METHOD              index
             1600  LOAD_FAST                'wordNext'
             1602  CALL_METHOD_1         1  '1 positional argument'
             1604  STORE_FAST               'd'

 L. 327      1606  LOAD_FAST                'd'
             1608  LOAD_CONST               1
             1610  BINARY_ADD       
             1612  LOAD_GLOBAL              int
             1614  LOAD_FAST                'today'
             1616  CALL_FUNCTION_1       1  '1 positional argument'
             1618  BINARY_SUBTRACT  
             1620  STORE_FAST               'tmpOffset'

 L. 328      1622  LOAD_CONST               2
             1624  STORE_FAST               'used'

 L. 329      1626  LOAD_FAST                'tmpOffset'
             1628  LOAD_CONST               0
             1630  COMPARE_OP               <
         1632_1634  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 330      1636  LOAD_FAST                'tmpOffset'
             1638  LOAD_CONST               7
             1640  INPLACE_ADD      
             1642  STORE_FAST               'tmpOffset'
           1644_0  COME_FROM          1632  '1632'

 L. 331      1644  LOAD_DEREF               'dayOffset'
             1646  LOAD_FAST                'tmpOffset'
             1648  INPLACE_ADD      
             1650  STORE_DEREF              'dayOffset'
             1652  JUMP_FORWARD       1778  'to 1778'
           1654_0  COME_FROM          1592  '1592'

 L. 332      1654  LOAD_FAST                'wordNextNext'
         1656_1658  POP_JUMP_IF_FALSE  1778  'to 1778'
             1660  LOAD_FAST                'wordNextNext'
             1662  LOAD_FAST                'days'
             1664  COMPARE_OP               in
         1666_1668  POP_JUMP_IF_FALSE  1778  'to 1778'

 L. 333      1670  LOAD_FAST                'days'
             1672  LOAD_METHOD              index
             1674  LOAD_FAST                'wordNextNext'
             1676  CALL_METHOD_1         1  '1 positional argument'
             1678  STORE_FAST               'd'

 L. 334      1680  LOAD_FAST                'd'
             1682  LOAD_CONST               1
             1684  BINARY_ADD       
             1686  LOAD_GLOBAL              int
             1688  LOAD_FAST                'today'
             1690  CALL_FUNCTION_1       1  '1 positional argument'
             1692  BINARY_SUBTRACT  
             1694  STORE_FAST               'tmpOffset'

 L. 335      1696  LOAD_CONST               3
             1698  STORE_FAST               'used'

 L. 336      1700  LOAD_FAST                'wordNext'
             1702  LOAD_STR                 'nästa'
             1704  COMPARE_OP               ==
         1706_1708  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 337      1710  LOAD_FAST                'tmpOffset'
             1712  LOAD_CONST               7
             1714  INPLACE_ADD      
             1716  STORE_FAST               'tmpOffset'

 L. 338      1718  LOAD_FAST                'used'
             1720  LOAD_CONST               1
             1722  INPLACE_ADD      
             1724  STORE_FAST               'used'

 L. 339      1726  LOAD_FAST                'start'
             1728  LOAD_CONST               1
             1730  INPLACE_SUBTRACT 
             1732  STORE_FAST               'start'
             1734  JUMP_FORWARD       1770  'to 1770'
           1736_0  COME_FROM          1706  '1706'

 L. 340      1736  LOAD_FAST                'wordNext'
             1738  LOAD_STR                 'förra'
             1740  COMPARE_OP               ==
         1742_1744  POP_JUMP_IF_FALSE  1770  'to 1770'

 L. 341      1746  LOAD_FAST                'tmpOffset'
             1748  LOAD_CONST               7
             1750  INPLACE_SUBTRACT 
             1752  STORE_FAST               'tmpOffset'

 L. 342      1754  LOAD_FAST                'used'
             1756  LOAD_CONST               1
             1758  INPLACE_ADD      
             1760  STORE_FAST               'used'

 L. 343      1762  LOAD_FAST                'start'
             1764  LOAD_CONST               1
             1766  INPLACE_SUBTRACT 
             1768  STORE_FAST               'start'
           1770_0  COME_FROM          1742  '1742'
           1770_1  COME_FROM          1734  '1734'

 L. 344      1770  LOAD_DEREF               'dayOffset'
             1772  LOAD_FAST                'tmpOffset'
             1774  INPLACE_ADD      
             1776  STORE_DEREF              'dayOffset'
           1778_0  COME_FROM          1666  '1666'
           1778_1  COME_FROM          1656  '1656'
           1778_2  COME_FROM          1652  '1652'
           1778_3  COME_FROM          1584  '1584'
           1778_4  COME_FROM          1554  '1554'
           1778_5  COME_FROM          1544  '1544'

 L. 345      1778  LOAD_FAST                'used'
             1780  LOAD_CONST               0
             1782  COMPARE_OP               >
             1784  POP_JUMP_IF_FALSE   236  'to 236'

 L. 346      1786  LOAD_FAST                'start'
             1788  LOAD_CONST               1
             1790  BINARY_SUBTRACT  
             1792  LOAD_CONST               0
             1794  COMPARE_OP               >
         1796_1798  POP_JUMP_IF_FALSE  1834  'to 1834'
             1800  LOAD_FAST                'words'
             1802  LOAD_FAST                'start'
             1804  LOAD_CONST               1
             1806  BINARY_SUBTRACT  
             1808  BINARY_SUBSCR    
             1810  LOAD_STR                 'denna'
             1812  COMPARE_OP               ==
         1814_1816  POP_JUMP_IF_FALSE  1834  'to 1834'

 L. 347      1818  LOAD_FAST                'start'
             1820  LOAD_CONST               1
             1822  INPLACE_SUBTRACT 
             1824  STORE_FAST               'start'

 L. 348      1826  LOAD_FAST                'used'
             1828  LOAD_CONST               1
             1830  INPLACE_ADD      
             1832  STORE_FAST               'used'
           1834_0  COME_FROM          1814  '1814'
           1834_1  COME_FROM          1796  '1796'

 L. 350      1834  SETUP_LOOP         1868  'to 1868'
             1836  LOAD_GLOBAL              range
             1838  LOAD_CONST               0
             1840  LOAD_FAST                'used'
             1842  CALL_FUNCTION_2       2  '2 positional arguments'
             1844  GET_ITER         
             1846  FOR_ITER           1866  'to 1866'
             1848  STORE_FAST               'i'

 L. 351      1850  LOAD_STR                 ''
             1852  LOAD_FAST                'words'
             1854  LOAD_FAST                'i'
             1856  LOAD_FAST                'start'
             1858  BINARY_ADD       
             1860  STORE_SUBSCR     
         1862_1864  JUMP_BACK          1846  'to 1846'
             1866  POP_BLOCK        
           1868_0  COME_FROM_LOOP     1834  '1834'

 L. 353      1868  LOAD_FAST                'start'
             1870  LOAD_CONST               1
             1872  BINARY_SUBTRACT  
             1874  LOAD_CONST               0
             1876  COMPARE_OP               >=
         1878_1880  POP_JUMP_IF_FALSE  1912  'to 1912'
             1882  LOAD_FAST                'words'
             1884  LOAD_FAST                'start'
             1886  LOAD_CONST               1
             1888  BINARY_SUBTRACT  
             1890  BINARY_SUBSCR    
             1892  LOAD_FAST                'markers'
             1894  COMPARE_OP               in
         1896_1898  POP_JUMP_IF_FALSE  1912  'to 1912'

 L. 354      1900  LOAD_STR                 ''
             1902  LOAD_FAST                'words'
             1904  LOAD_FAST                'start'
             1906  LOAD_CONST               1
             1908  BINARY_SUBTRACT  
             1910  STORE_SUBSCR     
           1912_0  COME_FROM          1896  '1896'
           1912_1  COME_FROM          1878  '1878'

 L. 355      1912  LOAD_CONST               True
             1914  STORE_DEREF              'found'

 L. 356      1916  LOAD_CONST               True
             1918  STORE_FAST               'daySpecified'
             1920  JUMP_BACK           236  'to 236'
             1922  POP_BLOCK        
           1924_0  COME_FROM_LOOP      224  '224'

 L. 359      1924  LOAD_STR                 ''
             1926  STORE_DEREF              'timeStr'

 L. 360      1928  LOAD_CONST               0
             1930  STORE_DEREF              'hrOffset'

 L. 361      1932  LOAD_CONST               0
             1934  STORE_DEREF              'minOffset'

 L. 362      1936  LOAD_CONST               0
             1938  STORE_DEREF              'secOffset'

 L. 363      1940  LOAD_CONST               None
             1942  STORE_DEREF              'hrAbs'

 L. 364      1944  LOAD_CONST               None
             1946  STORE_DEREF              'minAbs'

 L. 366  1948_1950  SETUP_LOOP         4582  'to 4582'
             1952  LOAD_GLOBAL              enumerate
             1954  LOAD_FAST                'words'
             1956  CALL_FUNCTION_1       1  '1 positional argument'
             1958  GET_ITER         
           1960_0  COME_FROM          4356  '4356'
         1960_1962  FOR_ITER           4580  'to 4580'
             1964  UNPACK_SEQUENCE_2     2 
             1966  STORE_FAST               'idx'
             1968  STORE_FAST               'word'

 L. 367      1970  LOAD_FAST                'word'
             1972  LOAD_STR                 ''
             1974  COMPARE_OP               ==
         1976_1978  POP_JUMP_IF_FALSE  1984  'to 1984'

 L. 368  1980_1982  CONTINUE           1960  'to 1960'
           1984_0  COME_FROM          1976  '1976'

 L. 370      1984  LOAD_FAST                'idx'
             1986  LOAD_CONST               1
             1988  COMPARE_OP               >
         1990_1992  POP_JUMP_IF_FALSE  2006  'to 2006'
             1994  LOAD_FAST                'words'
             1996  LOAD_FAST                'idx'
             1998  LOAD_CONST               2
             2000  BINARY_SUBTRACT  
             2002  BINARY_SUBSCR    
             2004  JUMP_FORWARD       2008  'to 2008'
           2006_0  COME_FROM          1990  '1990'
             2006  LOAD_STR                 ''
           2008_0  COME_FROM          2004  '2004'
             2008  STORE_FAST               'wordPrevPrev'

 L. 371      2010  LOAD_FAST                'idx'
             2012  LOAD_CONST               0
             2014  COMPARE_OP               >
         2016_2018  POP_JUMP_IF_FALSE  2032  'to 2032'
             2020  LOAD_FAST                'words'
             2022  LOAD_FAST                'idx'
             2024  LOAD_CONST               1
             2026  BINARY_SUBTRACT  
             2028  BINARY_SUBSCR    
             2030  JUMP_FORWARD       2034  'to 2034'
           2032_0  COME_FROM          2016  '2016'
             2032  LOAD_STR                 ''
           2034_0  COME_FROM          2030  '2030'
             2034  STORE_FAST               'wordPrev'

 L. 372      2036  LOAD_FAST                'idx'
             2038  LOAD_CONST               1
             2040  BINARY_ADD       
             2042  LOAD_GLOBAL              len
             2044  LOAD_FAST                'words'
             2046  CALL_FUNCTION_1       1  '1 positional argument'
             2048  COMPARE_OP               <
         2050_2052  POP_JUMP_IF_FALSE  2066  'to 2066'
             2054  LOAD_FAST                'words'
             2056  LOAD_FAST                'idx'
             2058  LOAD_CONST               1
             2060  BINARY_ADD       
             2062  BINARY_SUBSCR    
             2064  JUMP_FORWARD       2068  'to 2068'
           2066_0  COME_FROM          2050  '2050'
             2066  LOAD_STR                 ''
           2068_0  COME_FROM          2064  '2064'
             2068  STORE_FAST               'wordNext'

 L. 373      2070  LOAD_FAST                'idx'
             2072  LOAD_CONST               2
             2074  BINARY_ADD       
             2076  LOAD_GLOBAL              len
             2078  LOAD_FAST                'words'
             2080  CALL_FUNCTION_1       1  '1 positional argument'
             2082  COMPARE_OP               <
         2084_2086  POP_JUMP_IF_FALSE  2100  'to 2100'
             2088  LOAD_FAST                'words'
             2090  LOAD_FAST                'idx'
             2092  LOAD_CONST               2
             2094  BINARY_ADD       
             2096  BINARY_SUBSCR    
             2098  JUMP_FORWARD       2102  'to 2102'
           2100_0  COME_FROM          2084  '2084'
             2100  LOAD_STR                 ''
           2102_0  COME_FROM          2098  '2098'
             2102  STORE_FAST               'wordNextNext'

 L. 375      2104  LOAD_CONST               0
             2106  STORE_FAST               'used'

 L. 376      2108  LOAD_FAST                'word'
             2110  LOAD_STR                 'middag'
             2112  COMPARE_OP               ==
         2114_2116  POP_JUMP_IF_FALSE  2134  'to 2134'

 L. 377      2118  LOAD_CONST               12
             2120  STORE_DEREF              'hrAbs'

 L. 378      2122  LOAD_FAST                'used'
             2124  LOAD_CONST               1
             2126  INPLACE_ADD      
             2128  STORE_FAST               'used'
         2130_2132  JUMP_FORWARD       4350  'to 4350'
           2134_0  COME_FROM          2114  '2114'

 L. 379      2134  LOAD_FAST                'word'
             2136  LOAD_STR                 'midnatt'
             2138  COMPARE_OP               ==
         2140_2142  POP_JUMP_IF_FALSE  2160  'to 2160'

 L. 380      2144  LOAD_CONST               0
             2146  STORE_DEREF              'hrAbs'

 L. 381      2148  LOAD_FAST                'used'
             2150  LOAD_CONST               1
             2152  INPLACE_ADD      
             2154  STORE_FAST               'used'
         2156_2158  JUMP_FORWARD       4350  'to 4350'
           2160_0  COME_FROM          2140  '2140'

 L. 382      2160  LOAD_FAST                'word'
             2162  LOAD_STR                 'morgon'
             2164  COMPARE_OP               ==
         2166_2168  POP_JUMP_IF_FALSE  2192  'to 2192'

 L. 383      2170  LOAD_DEREF               'hrAbs'
         2172_2174  POP_JUMP_IF_TRUE   2180  'to 2180'

 L. 384      2176  LOAD_CONST               8
             2178  STORE_DEREF              'hrAbs'
           2180_0  COME_FROM          2172  '2172'

 L. 385      2180  LOAD_FAST                'used'
             2182  LOAD_CONST               1
             2184  INPLACE_ADD      
             2186  STORE_FAST               'used'
         2188_2190  JUMP_FORWARD       4350  'to 4350'
           2192_0  COME_FROM          2166  '2166'

 L. 386      2192  LOAD_FAST                'word'
             2194  LOAD_STR                 'förmiddag'
             2196  COMPARE_OP               ==
         2198_2200  POP_JUMP_IF_FALSE  2224  'to 2224'

 L. 387      2202  LOAD_DEREF               'hrAbs'
         2204_2206  POP_JUMP_IF_TRUE   2212  'to 2212'

 L. 388      2208  LOAD_CONST               10
             2210  STORE_DEREF              'hrAbs'
           2212_0  COME_FROM          2204  '2204'

 L. 389      2212  LOAD_FAST                'used'
             2214  LOAD_CONST               1
             2216  INPLACE_ADD      
             2218  STORE_FAST               'used'
         2220_2222  JUMP_FORWARD       4350  'to 4350'
           2224_0  COME_FROM          2198  '2198'

 L. 390      2224  LOAD_FAST                'word'
             2226  LOAD_STR                 'eftermiddag'
             2228  COMPARE_OP               ==
         2230_2232  POP_JUMP_IF_FALSE  2256  'to 2256'

 L. 391      2234  LOAD_DEREF               'hrAbs'
         2236_2238  POP_JUMP_IF_TRUE   2244  'to 2244'

 L. 392      2240  LOAD_CONST               15
             2242  STORE_DEREF              'hrAbs'
           2244_0  COME_FROM          2236  '2236'

 L. 393      2244  LOAD_FAST                'used'
             2246  LOAD_CONST               1
             2248  INPLACE_ADD      
             2250  STORE_FAST               'used'
         2252_2254  JUMP_FORWARD       4350  'to 4350'
           2256_0  COME_FROM          2230  '2230'

 L. 394      2256  LOAD_FAST                'word'
             2258  LOAD_STR                 'kväll'
             2260  COMPARE_OP               ==
         2262_2264  POP_JUMP_IF_FALSE  2288  'to 2288'

 L. 395      2266  LOAD_DEREF               'hrAbs'
         2268_2270  POP_JUMP_IF_TRUE   2276  'to 2276'

 L. 396      2272  LOAD_CONST               19
             2274  STORE_DEREF              'hrAbs'
           2276_0  COME_FROM          2268  '2268'

 L. 397      2276  LOAD_FAST                'used'
             2278  LOAD_CONST               1
             2280  INPLACE_ADD      
             2282  STORE_FAST               'used'
         2284_2286  JUMP_FORWARD       4350  'to 4350'
           2288_0  COME_FROM          2262  '2262'

 L. 399      2288  LOAD_FAST                'wordPrev'
             2290  LOAD_FAST                'markers'
             2292  COMPARE_OP               in
         2294_2296  POP_JUMP_IF_TRUE   2308  'to 2308'
             2298  LOAD_FAST                'wordPrevPrev'
             2300  LOAD_FAST                'markers'
             2302  COMPARE_OP               in
         2304_2306  POP_JUMP_IF_FALSE  2406  'to 2406'
           2308_0  COME_FROM          2294  '2294'

 L. 400      2308  LOAD_FAST                'word'
             2310  LOAD_STR                 'halvtimme'
             2312  COMPARE_OP               ==
         2314_2316  POP_JUMP_IF_TRUE   2328  'to 2328'
             2318  LOAD_FAST                'word'
             2320  LOAD_STR                 'halvtimma'
             2322  COMPARE_OP               ==
         2324_2326  POP_JUMP_IF_FALSE  2334  'to 2334'
           2328_0  COME_FROM          2314  '2314'

 L. 401      2328  LOAD_CONST               30
             2330  STORE_DEREF              'minOffset'
             2332  JUMP_FORWARD       2374  'to 2374'
           2334_0  COME_FROM          2324  '2324'

 L. 402      2334  LOAD_FAST                'word'
             2336  LOAD_STR                 'kvart'
             2338  COMPARE_OP               ==
         2340_2342  POP_JUMP_IF_FALSE  2350  'to 2350'

 L. 403      2344  LOAD_CONST               15
             2346  STORE_DEREF              'minOffset'
             2348  JUMP_FORWARD       2374  'to 2374'
           2350_0  COME_FROM          2340  '2340'

 L. 404      2350  LOAD_FAST                'word'
             2352  LOAD_STR                 'timme'
             2354  COMPARE_OP               ==
         2356_2358  POP_JUMP_IF_TRUE   2370  'to 2370'
             2360  LOAD_FAST                'word'
             2362  LOAD_STR                 'timma'
             2364  COMPARE_OP               ==
         2366_2368  POP_JUMP_IF_FALSE  2374  'to 2374'
           2370_0  COME_FROM          2356  '2356'

 L. 405      2370  LOAD_CONST               1
             2372  STORE_DEREF              'hrOffset'
           2374_0  COME_FROM          2366  '2366'
           2374_1  COME_FROM          2348  '2348'
           2374_2  COME_FROM          2332  '2332'

 L. 406      2374  LOAD_STR                 ''
             2376  LOAD_FAST                'words'
             2378  LOAD_FAST                'idx'
             2380  LOAD_CONST               1
             2382  BINARY_SUBTRACT  
             2384  STORE_SUBSCR     

 L. 407      2386  LOAD_FAST                'used'
             2388  LOAD_CONST               1
             2390  INPLACE_ADD      
             2392  STORE_FAST               'used'

 L. 408      2394  LOAD_CONST               -1
             2396  STORE_DEREF              'hrAbs'

 L. 409      2398  LOAD_CONST               -1
             2400  STORE_DEREF              'minAbs'
         2402_2404  JUMP_FORWARD       4350  'to 4350'
           2406_0  COME_FROM          2304  '2304'

 L. 411      2406  LOAD_FAST                'word'
             2408  LOAD_CONST               0
             2410  BINARY_SUBSCR    
             2412  LOAD_METHOD              isdigit
             2414  CALL_METHOD_0         0  '0 positional arguments'
         2416_2418  POP_JUMP_IF_FALSE  4350  'to 4350'

 L. 412      2420  LOAD_CONST               True
             2422  STORE_FAST               'isTime'

 L. 413      2424  LOAD_STR                 ''
             2426  STORE_FAST               'strHH'

 L. 414      2428  LOAD_STR                 ''
             2430  STORE_FAST               'strMM'

 L. 415      2432  LOAD_STR                 ''
             2434  STORE_FAST               'remainder'

 L. 416      2436  LOAD_STR                 ':'
             2438  LOAD_FAST                'word'
             2440  COMPARE_OP               in
         2442_2444  POP_JUMP_IF_FALSE  3176  'to 3176'

 L. 419      2446  LOAD_CONST               0
             2448  STORE_FAST               'stage'

 L. 420      2450  LOAD_GLOBAL              len
             2452  LOAD_FAST                'word'
             2454  CALL_FUNCTION_1       1  '1 positional argument'
             2456  STORE_FAST               'length'

 L. 421      2458  SETUP_LOOP         2634  'to 2634'
             2460  LOAD_GLOBAL              range
             2462  LOAD_FAST                'length'
             2464  CALL_FUNCTION_1       1  '1 positional argument'
             2466  GET_ITER         
           2468_0  COME_FROM          2602  '2602'
             2468  FOR_ITER           2632  'to 2632'
             2470  STORE_FAST               'i'

 L. 422      2472  LOAD_FAST                'stage'
             2474  LOAD_CONST               0
             2476  COMPARE_OP               ==
         2478_2480  POP_JUMP_IF_FALSE  2544  'to 2544'

 L. 423      2482  LOAD_FAST                'word'
             2484  LOAD_FAST                'i'
             2486  BINARY_SUBSCR    
             2488  LOAD_METHOD              isdigit
             2490  CALL_METHOD_0         0  '0 positional arguments'
         2492_2494  POP_JUMP_IF_FALSE  2510  'to 2510'

 L. 424      2496  LOAD_FAST                'strHH'
             2498  LOAD_FAST                'word'
             2500  LOAD_FAST                'i'
             2502  BINARY_SUBSCR    
             2504  INPLACE_ADD      
             2506  STORE_FAST               'strHH'
             2508  JUMP_FORWARD       2542  'to 2542'
           2510_0  COME_FROM          2492  '2492'

 L. 425      2510  LOAD_FAST                'word'
             2512  LOAD_FAST                'i'
             2514  BINARY_SUBSCR    
             2516  LOAD_STR                 ':'
             2518  COMPARE_OP               ==
         2520_2522  POP_JUMP_IF_FALSE  2530  'to 2530'

 L. 426      2524  LOAD_CONST               1
             2526  STORE_FAST               'stage'
             2528  JUMP_FORWARD       2542  'to 2542'
           2530_0  COME_FROM          2520  '2520'

 L. 428      2530  LOAD_CONST               2
             2532  STORE_FAST               'stage'

 L. 429      2534  LOAD_FAST                'i'
             2536  LOAD_CONST               1
             2538  INPLACE_SUBTRACT 
             2540  STORE_FAST               'i'
           2542_0  COME_FROM          2528  '2528'
           2542_1  COME_FROM          2508  '2508'
             2542  JUMP_BACK          2468  'to 2468'
           2544_0  COME_FROM          2478  '2478'

 L. 430      2544  LOAD_FAST                'stage'
             2546  LOAD_CONST               1
             2548  COMPARE_OP               ==
         2550_2552  POP_JUMP_IF_FALSE  2596  'to 2596'

 L. 431      2554  LOAD_FAST                'word'
             2556  LOAD_FAST                'i'
             2558  BINARY_SUBSCR    
             2560  LOAD_METHOD              isdigit
             2562  CALL_METHOD_0         0  '0 positional arguments'
         2564_2566  POP_JUMP_IF_FALSE  2582  'to 2582'

 L. 432      2568  LOAD_FAST                'strMM'
             2570  LOAD_FAST                'word'
             2572  LOAD_FAST                'i'
             2574  BINARY_SUBSCR    
             2576  INPLACE_ADD      
             2578  STORE_FAST               'strMM'
             2580  JUMP_FORWARD       2594  'to 2594'
           2582_0  COME_FROM          2564  '2564'

 L. 434      2582  LOAD_CONST               2
             2584  STORE_FAST               'stage'

 L. 435      2586  LOAD_FAST                'i'
             2588  LOAD_CONST               1
             2590  INPLACE_SUBTRACT 
             2592  STORE_FAST               'i'
           2594_0  COME_FROM          2580  '2580'
             2594  JUMP_BACK          2468  'to 2468'
           2596_0  COME_FROM          2550  '2550'

 L. 436      2596  LOAD_FAST                'stage'
             2598  LOAD_CONST               2
             2600  COMPARE_OP               ==
         2602_2604  POP_JUMP_IF_FALSE  2468  'to 2468'

 L. 437      2606  LOAD_FAST                'word'
             2608  LOAD_FAST                'i'
             2610  LOAD_CONST               None
             2612  BUILD_SLICE_2         2 
             2614  BINARY_SUBSCR    
             2616  LOAD_METHOD              replace
             2618  LOAD_STR                 '.'
             2620  LOAD_STR                 ''
             2622  CALL_METHOD_2         2  '2 positional arguments'
             2624  STORE_FAST               'remainder'

 L. 438      2626  BREAK_LOOP       
         2628_2630  JUMP_BACK          2468  'to 2468'
             2632  POP_BLOCK        
           2634_0  COME_FROM_LOOP     2458  '2458'

 L. 439      2634  LOAD_FAST                'remainder'
             2636  LOAD_STR                 ''
             2638  COMPARE_OP               ==
         2640_2642  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 440      2644  LOAD_FAST                'wordNext'
             2646  LOAD_METHOD              replace
             2648  LOAD_STR                 '.'
             2650  LOAD_STR                 ''
             2652  CALL_METHOD_2         2  '2 positional arguments'
             2654  STORE_FAST               'nextWord'

 L. 441      2656  LOAD_FAST                'nextWord'
             2658  LOAD_STR                 'am'
             2660  COMPARE_OP               ==
         2662_2664  POP_JUMP_IF_TRUE   2676  'to 2676'
             2666  LOAD_FAST                'nextWord'
             2668  LOAD_STR                 'pm'
             2670  COMPARE_OP               ==
         2672_2674  POP_JUMP_IF_FALSE  2692  'to 2692'
           2676_0  COME_FROM          2662  '2662'

 L. 442      2676  LOAD_FAST                'nextWord'
             2678  STORE_FAST               'remainder'

 L. 443      2680  LOAD_FAST                'used'
             2682  LOAD_CONST               1
             2684  INPLACE_ADD      
             2686  STORE_FAST               'used'
         2688_2690  JUMP_ABSOLUTE      4192  'to 4192'
           2692_0  COME_FROM          2672  '2672'

 L. 444      2692  LOAD_FAST                'nextWord'
             2694  LOAD_STR                 'tonight'
             2696  COMPARE_OP               ==
         2698_2700  POP_JUMP_IF_FALSE  2718  'to 2718'

 L. 445      2702  LOAD_STR                 'pm'
             2704  STORE_FAST               'remainder'

 L. 446      2706  LOAD_FAST                'used'
             2708  LOAD_CONST               1
             2710  INPLACE_ADD      
             2712  STORE_FAST               'used'
         2714_2716  JUMP_ABSOLUTE      4192  'to 4192'
           2718_0  COME_FROM          2698  '2698'

 L. 447      2718  LOAD_FAST                'wordNext'
             2720  LOAD_STR                 'in'
             2722  COMPARE_OP               ==
         2724_2726  POP_JUMP_IF_FALSE  2772  'to 2772'
             2728  LOAD_FAST                'wordNextNext'
             2730  LOAD_STR                 'the'
             2732  COMPARE_OP               ==
         2734_2736  POP_JUMP_IF_FALSE  2772  'to 2772'

 L. 448      2738  LOAD_FAST                'words'
             2740  LOAD_FAST                'idx'
             2742  LOAD_CONST               3
             2744  BINARY_ADD       
             2746  BINARY_SUBSCR    
             2748  LOAD_STR                 'morning'
             2750  COMPARE_OP               ==
         2752_2754  POP_JUMP_IF_FALSE  2772  'to 2772'

 L. 449      2756  LOAD_STR                 'am'
             2758  STORE_FAST               'remainder'

 L. 450      2760  LOAD_FAST                'used'
             2762  LOAD_CONST               3
             2764  INPLACE_ADD      
             2766  STORE_FAST               'used'
         2768_2770  JUMP_ABSOLUTE      4192  'to 4192'
           2772_0  COME_FROM          2752  '2752'
           2772_1  COME_FROM          2734  '2734'
           2772_2  COME_FROM          2724  '2724'

 L. 451      2772  LOAD_FAST                'wordNext'
             2774  LOAD_STR                 'in'
             2776  COMPARE_OP               ==
         2778_2780  POP_JUMP_IF_FALSE  2826  'to 2826'
             2782  LOAD_FAST                'wordNextNext'
             2784  LOAD_STR                 'the'
             2786  COMPARE_OP               ==
         2788_2790  POP_JUMP_IF_FALSE  2826  'to 2826'

 L. 452      2792  LOAD_FAST                'words'
             2794  LOAD_FAST                'idx'
             2796  LOAD_CONST               3
             2798  BINARY_ADD       
             2800  BINARY_SUBSCR    
             2802  LOAD_STR                 'afternoon'
             2804  COMPARE_OP               ==
         2806_2808  POP_JUMP_IF_FALSE  2826  'to 2826'

 L. 453      2810  LOAD_STR                 'pm'
             2812  STORE_FAST               'remainder'

 L. 454      2814  LOAD_FAST                'used'
             2816  LOAD_CONST               3
             2818  INPLACE_ADD      
             2820  STORE_FAST               'used'
         2822_2824  JUMP_ABSOLUTE      4192  'to 4192'
           2826_0  COME_FROM          2806  '2806'
           2826_1  COME_FROM          2788  '2788'
           2826_2  COME_FROM          2778  '2778'

 L. 455      2826  LOAD_FAST                'wordNext'
             2828  LOAD_STR                 'in'
             2830  COMPARE_OP               ==
         2832_2834  POP_JUMP_IF_FALSE  2880  'to 2880'
             2836  LOAD_FAST                'wordNextNext'
             2838  LOAD_STR                 'the'
             2840  COMPARE_OP               ==
         2842_2844  POP_JUMP_IF_FALSE  2880  'to 2880'

 L. 456      2846  LOAD_FAST                'words'
             2848  LOAD_FAST                'idx'
             2850  LOAD_CONST               3
             2852  BINARY_ADD       
             2854  BINARY_SUBSCR    
             2856  LOAD_STR                 'evening'
             2858  COMPARE_OP               ==
         2860_2862  POP_JUMP_IF_FALSE  2880  'to 2880'

 L. 457      2864  LOAD_STR                 'pm'
             2866  STORE_FAST               'remainder'

 L. 458      2868  LOAD_FAST                'used'
             2870  LOAD_CONST               3
             2872  INPLACE_ADD      
             2874  STORE_FAST               'used'
         2876_2878  JUMP_ABSOLUTE      4192  'to 4192'
           2880_0  COME_FROM          2860  '2860'
           2880_1  COME_FROM          2842  '2842'
           2880_2  COME_FROM          2832  '2832'

 L. 459      2880  LOAD_FAST                'wordNext'
             2882  LOAD_STR                 'in'
             2884  COMPARE_OP               ==
         2886_2888  POP_JUMP_IF_FALSE  2916  'to 2916'
             2890  LOAD_FAST                'wordNextNext'
             2892  LOAD_STR                 'morning'
             2894  COMPARE_OP               ==
         2896_2898  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 460      2900  LOAD_STR                 'am'
             2902  STORE_FAST               'remainder'

 L. 461      2904  LOAD_FAST                'used'
             2906  LOAD_CONST               2
             2908  INPLACE_ADD      
             2910  STORE_FAST               'used'
         2912_2914  JUMP_ABSOLUTE      4192  'to 4192'
           2916_0  COME_FROM          2896  '2896'
           2916_1  COME_FROM          2886  '2886'

 L. 462      2916  LOAD_FAST                'wordNext'
             2918  LOAD_STR                 'in'
             2920  COMPARE_OP               ==
         2922_2924  POP_JUMP_IF_FALSE  2950  'to 2950'
             2926  LOAD_FAST                'wordNextNext'
             2928  LOAD_STR                 'afternoon'
             2930  COMPARE_OP               ==
         2932_2934  POP_JUMP_IF_FALSE  2950  'to 2950'

 L. 463      2936  LOAD_STR                 'pm'
             2938  STORE_FAST               'remainder'

 L. 464      2940  LOAD_FAST                'used'
             2942  LOAD_CONST               2
             2944  INPLACE_ADD      
             2946  STORE_FAST               'used'
             2948  JUMP_FORWARD       4192  'to 4192'
           2950_0  COME_FROM          2932  '2932'
           2950_1  COME_FROM          2922  '2922'

 L. 465      2950  LOAD_FAST                'wordNext'
             2952  LOAD_STR                 'in'
             2954  COMPARE_OP               ==
         2956_2958  POP_JUMP_IF_FALSE  2984  'to 2984'
             2960  LOAD_FAST                'wordNextNext'
             2962  LOAD_STR                 'evening'
             2964  COMPARE_OP               ==
         2966_2968  POP_JUMP_IF_FALSE  2984  'to 2984'

 L. 466      2970  LOAD_STR                 'pm'
             2972  STORE_FAST               'remainder'

 L. 467      2974  LOAD_FAST                'used'
             2976  LOAD_CONST               2
             2978  INPLACE_ADD      
             2980  STORE_FAST               'used'
             2982  JUMP_FORWARD       4192  'to 4192'
           2984_0  COME_FROM          2966  '2966'
           2984_1  COME_FROM          2956  '2956'

 L. 468      2984  LOAD_FAST                'wordNext'
             2986  LOAD_STR                 'this'
             2988  COMPARE_OP               ==
         2990_2992  POP_JUMP_IF_FALSE  3014  'to 3014'
             2994  LOAD_FAST                'wordNextNext'
             2996  LOAD_STR                 'morning'
             2998  COMPARE_OP               ==
         3000_3002  POP_JUMP_IF_FALSE  3014  'to 3014'

 L. 469      3004  LOAD_STR                 'am'
             3006  STORE_FAST               'remainder'

 L. 470      3008  LOAD_CONST               2
             3010  STORE_FAST               'used'
             3012  JUMP_FORWARD       4192  'to 4192'
           3014_0  COME_FROM          3000  '3000'
           3014_1  COME_FROM          2990  '2990'

 L. 471      3014  LOAD_FAST                'wordNext'
             3016  LOAD_STR                 'this'
             3018  COMPARE_OP               ==
         3020_3022  POP_JUMP_IF_FALSE  3044  'to 3044'
             3024  LOAD_FAST                'wordNextNext'
             3026  LOAD_STR                 'afternoon'
             3028  COMPARE_OP               ==
         3030_3032  POP_JUMP_IF_FALSE  3044  'to 3044'

 L. 472      3034  LOAD_STR                 'pm'
             3036  STORE_FAST               'remainder'

 L. 473      3038  LOAD_CONST               2
             3040  STORE_FAST               'used'
             3042  JUMP_FORWARD       4192  'to 4192'
           3044_0  COME_FROM          3030  '3030'
           3044_1  COME_FROM          3020  '3020'

 L. 474      3044  LOAD_FAST                'wordNext'
             3046  LOAD_STR                 'this'
             3048  COMPARE_OP               ==
         3050_3052  POP_JUMP_IF_FALSE  3074  'to 3074'
             3054  LOAD_FAST                'wordNextNext'
             3056  LOAD_STR                 'evening'
             3058  COMPARE_OP               ==
         3060_3062  POP_JUMP_IF_FALSE  3074  'to 3074'

 L. 475      3064  LOAD_STR                 'pm'
             3066  STORE_FAST               'remainder'

 L. 476      3068  LOAD_CONST               2
             3070  STORE_FAST               'used'
             3072  JUMP_FORWARD       4192  'to 4192'
           3074_0  COME_FROM          3060  '3060'
           3074_1  COME_FROM          3050  '3050'

 L. 477      3074  LOAD_FAST                'wordNext'
             3076  LOAD_STR                 'at'
             3078  COMPARE_OP               ==
         3080_3082  POP_JUMP_IF_FALSE  3124  'to 3124'
             3084  LOAD_FAST                'wordNextNext'
             3086  LOAD_STR                 'night'
             3088  COMPARE_OP               ==
         3090_3092  POP_JUMP_IF_FALSE  3124  'to 3124'

 L. 478      3094  LOAD_FAST                'strHH'
             3096  LOAD_CONST               5
             3098  COMPARE_OP               >
         3100_3102  POP_JUMP_IF_FALSE  3110  'to 3110'

 L. 479      3104  LOAD_STR                 'pm'
             3106  STORE_FAST               'remainder'
             3108  JUMP_FORWARD       3114  'to 3114'
           3110_0  COME_FROM          3100  '3100'

 L. 481      3110  LOAD_STR                 'am'
             3112  STORE_FAST               'remainder'
           3114_0  COME_FROM          3108  '3108'

 L. 482      3114  LOAD_FAST                'used'
             3116  LOAD_CONST               2
             3118  INPLACE_ADD      
             3120  STORE_FAST               'used'
             3122  JUMP_FORWARD       4192  'to 4192'
           3124_0  COME_FROM          3090  '3090'
           3124_1  COME_FROM          3080  '3080'

 L. 484      3124  LOAD_FAST                'timeQualifier'
             3126  LOAD_STR                 ''
             3128  COMPARE_OP               !=
         3130_3132  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 485      3134  LOAD_FAST                'strHH'
             3136  LOAD_CONST               12
             3138  COMPARE_OP               <=
         3140_3142  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 486      3144  LOAD_FAST                'timeQualifier'
             3146  LOAD_STR                 'evening'
             3148  COMPARE_OP               ==
         3150_3152  POP_JUMP_IF_TRUE   3164  'to 3164'

 L. 487      3154  LOAD_FAST                'timeQualifier'
             3156  LOAD_STR                 'afternoon'
             3158  COMPARE_OP               ==
         3160_3162  POP_JUMP_IF_FALSE  4192  'to 4192'
           3164_0  COME_FROM          3150  '3150'

 L. 488      3164  LOAD_FAST                'strHH'
             3166  LOAD_CONST               12
             3168  INPLACE_ADD      
             3170  STORE_FAST               'strHH'
         3172_3174  JUMP_FORWARD       4192  'to 4192'
           3176_0  COME_FROM          2442  '2442'

 L. 492      3176  LOAD_GLOBAL              len
             3178  LOAD_FAST                'word'
             3180  CALL_FUNCTION_1       1  '1 positional argument'
             3182  STORE_FAST               'length'

 L. 493      3184  LOAD_STR                 ''
             3186  STORE_FAST               'strNum'

 L. 494      3188  LOAD_STR                 ''
             3190  STORE_FAST               'remainder'

 L. 495      3192  SETUP_LOOP         3252  'to 3252'
             3194  LOAD_GLOBAL              range
             3196  LOAD_FAST                'length'
             3198  CALL_FUNCTION_1       1  '1 positional argument'
             3200  GET_ITER         
             3202  FOR_ITER           3250  'to 3250'
             3204  STORE_FAST               'i'

 L. 496      3206  LOAD_FAST                'word'
             3208  LOAD_FAST                'i'
             3210  BINARY_SUBSCR    
             3212  LOAD_METHOD              isdigit
             3214  CALL_METHOD_0         0  '0 positional arguments'
         3216_3218  POP_JUMP_IF_FALSE  3234  'to 3234'

 L. 497      3220  LOAD_FAST                'strNum'
             3222  LOAD_FAST                'word'
             3224  LOAD_FAST                'i'
             3226  BINARY_SUBSCR    
             3228  INPLACE_ADD      
             3230  STORE_FAST               'strNum'
             3232  JUMP_BACK          3202  'to 3202'
           3234_0  COME_FROM          3216  '3216'

 L. 499      3234  LOAD_FAST                'remainder'
             3236  LOAD_FAST                'word'
             3238  LOAD_FAST                'i'
             3240  BINARY_SUBSCR    
             3242  INPLACE_ADD      
             3244  STORE_FAST               'remainder'
         3246_3248  JUMP_BACK          3202  'to 3202'
             3250  POP_BLOCK        
           3252_0  COME_FROM_LOOP     3192  '3192'

 L. 501      3252  LOAD_FAST                'remainder'
             3254  LOAD_STR                 ''
             3256  COMPARE_OP               ==
         3258_3260  POP_JUMP_IF_FALSE  3282  'to 3282'

 L. 502      3262  LOAD_FAST                'wordNext'
             3264  LOAD_METHOD              replace
             3266  LOAD_STR                 '.'
             3268  LOAD_STR                 ''
             3270  CALL_METHOD_2         2  '2 positional arguments'
             3272  LOAD_METHOD              lstrip
             3274  CALL_METHOD_0         0  '0 positional arguments'
             3276  LOAD_METHOD              rstrip
             3278  CALL_METHOD_0         0  '0 positional arguments'
             3280  STORE_FAST               'remainder'
           3282_0  COME_FROM          3258  '3258'

 L. 505      3282  LOAD_FAST                'remainder'
             3284  LOAD_STR                 'pm'
             3286  COMPARE_OP               ==
         3288_3290  POP_JUMP_IF_TRUE   3322  'to 3322'

 L. 506      3292  LOAD_FAST                'wordNext'
             3294  LOAD_STR                 'pm'
             3296  COMPARE_OP               ==
         3298_3300  POP_JUMP_IF_TRUE   3322  'to 3322'

 L. 507      3302  LOAD_FAST                'remainder'
             3304  LOAD_STR                 'p.m.'
             3306  COMPARE_OP               ==
         3308_3310  POP_JUMP_IF_TRUE   3322  'to 3322'

 L. 508      3312  LOAD_FAST                'wordNext'
             3314  LOAD_STR                 'p.m.'
             3316  COMPARE_OP               ==
         3318_3320  POP_JUMP_IF_FALSE  3338  'to 3338'
           3322_0  COME_FROM          3308  '3308'
           3322_1  COME_FROM          3298  '3298'
           3322_2  COME_FROM          3288  '3288'

 L. 509      3322  LOAD_FAST                'strNum'
             3324  STORE_FAST               'strHH'

 L. 510      3326  LOAD_STR                 'pm'
             3328  STORE_FAST               'remainder'

 L. 511      3330  LOAD_CONST               1
             3332  STORE_FAST               'used'
         3334_3336  JUMP_FORWARD       4192  'to 4192'
           3338_0  COME_FROM          3318  '3318'

 L. 513      3338  LOAD_FAST                'remainder'
             3340  LOAD_STR                 'am'
             3342  COMPARE_OP               ==
         3344_3346  POP_JUMP_IF_TRUE   3378  'to 3378'

 L. 514      3348  LOAD_FAST                'wordNext'
             3350  LOAD_STR                 'am'
             3352  COMPARE_OP               ==
         3354_3356  POP_JUMP_IF_TRUE   3378  'to 3378'

 L. 515      3358  LOAD_FAST                'remainder'
             3360  LOAD_STR                 'a.m.'
             3362  COMPARE_OP               ==
         3364_3366  POP_JUMP_IF_TRUE   3378  'to 3378'

 L. 516      3368  LOAD_FAST                'wordNext'
             3370  LOAD_STR                 'a.m.'
             3372  COMPARE_OP               ==
         3374_3376  POP_JUMP_IF_FALSE  3394  'to 3394'
           3378_0  COME_FROM          3364  '3364'
           3378_1  COME_FROM          3354  '3354'
           3378_2  COME_FROM          3344  '3344'

 L. 517      3378  LOAD_FAST                'strNum'
             3380  STORE_FAST               'strHH'

 L. 518      3382  LOAD_STR                 'am'
             3384  STORE_FAST               'remainder'

 L. 519      3386  LOAD_CONST               1
             3388  STORE_FAST               'used'
         3390_3392  JUMP_FORWARD       4192  'to 4192'
           3394_0  COME_FROM          3374  '3374'

 L. 521      3394  LOAD_FAST                'wordNext'
             3396  LOAD_STR                 'pm'
             3398  COMPARE_OP               ==
         3400_3402  POP_JUMP_IF_TRUE   3414  'to 3414'
             3404  LOAD_FAST                'wordNext'
             3406  LOAD_STR                 'p.m.'
             3408  COMPARE_OP               ==
         3410_3412  POP_JUMP_IF_FALSE  3430  'to 3430'
           3414_0  COME_FROM          3400  '3400'

 L. 522      3414  LOAD_FAST                'strNum'
             3416  STORE_FAST               'strHH'

 L. 523      3418  LOAD_STR                 'pm'
             3420  STORE_FAST               'remainder'

 L. 524      3422  LOAD_CONST               1
             3424  STORE_FAST               'used'
         3426_3428  JUMP_FORWARD       4192  'to 4192'
           3430_0  COME_FROM          3410  '3410'

 L. 525      3430  LOAD_FAST                'wordNext'
             3432  LOAD_STR                 'am'
             3434  COMPARE_OP               ==
         3436_3438  POP_JUMP_IF_TRUE   3450  'to 3450'
             3440  LOAD_FAST                'wordNext'
             3442  LOAD_STR                 'a.m.'
             3444  COMPARE_OP               ==
         3446_3448  POP_JUMP_IF_FALSE  3466  'to 3466'
           3450_0  COME_FROM          3436  '3436'

 L. 526      3450  LOAD_FAST                'strNum'
             3452  STORE_FAST               'strHH'

 L. 527      3454  LOAD_STR                 'am'
             3456  STORE_FAST               'remainder'

 L. 528      3458  LOAD_CONST               1
             3460  STORE_FAST               'used'
         3462_3464  JUMP_FORWARD       4192  'to 4192'
           3466_0  COME_FROM          3446  '3446'

 L. 530      3466  LOAD_GLOBAL              int
             3468  LOAD_FAST                'word'
             3470  CALL_FUNCTION_1       1  '1 positional argument'
             3472  LOAD_CONST               100
             3474  COMPARE_OP               >
         3476_3478  POP_JUMP_IF_FALSE  3550  'to 3550'

 L. 532      3480  LOAD_FAST                'wordPrev'
             3482  LOAD_STR                 'o'
             3484  COMPARE_OP               ==
         3486_3488  POP_JUMP_IF_TRUE   3500  'to 3500'

 L. 533      3490  LOAD_FAST                'wordPrev'
             3492  LOAD_STR                 'oh'
             3494  COMPARE_OP               ==
         3496_3498  POP_JUMP_IF_FALSE  3550  'to 3550'
           3500_0  COME_FROM          3486  '3486'

 L. 536      3500  LOAD_GLOBAL              int
             3502  LOAD_FAST                'word'
             3504  CALL_FUNCTION_1       1  '1 positional argument'
             3506  LOAD_CONST               100
             3508  BINARY_TRUE_DIVIDE
             3510  STORE_FAST               'strHH'

 L. 537      3512  LOAD_GLOBAL              int
             3514  LOAD_FAST                'word'
             3516  CALL_FUNCTION_1       1  '1 positional argument'
             3518  LOAD_FAST                'strHH'
             3520  LOAD_CONST               100
             3522  BINARY_MULTIPLY  
             3524  BINARY_SUBTRACT  
             3526  STORE_FAST               'strMM'

 L. 538      3528  LOAD_FAST                'wordNext'
             3530  LOAD_STR                 'hours'
             3532  COMPARE_OP               ==
         3534_3536  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 539      3538  LOAD_FAST                'used'
             3540  LOAD_CONST               1
             3542  INPLACE_ADD      
             3544  STORE_FAST               'used'
         3546_3548  JUMP_FORWARD       4192  'to 4192'
           3550_0  COME_FROM          3496  '3496'
           3550_1  COME_FROM          3476  '3476'

 L. 541      3550  LOAD_FAST                'wordNext'
             3552  LOAD_STR                 'hours'
             3554  COMPARE_OP               ==
         3556_3558  POP_JUMP_IF_FALSE  3630  'to 3630'

 L. 542      3560  LOAD_FAST                'word'
             3562  LOAD_CONST               0
             3564  BINARY_SUBSCR    
             3566  LOAD_STR                 '0'
             3568  COMPARE_OP               !=
         3570_3572  POP_JUMP_IF_FALSE  3630  'to 3630'

 L. 544      3574  LOAD_GLOBAL              int
             3576  LOAD_FAST                'word'
             3578  CALL_FUNCTION_1       1  '1 positional argument'
             3580  LOAD_CONST               100
             3582  COMPARE_OP               <
         3584_3586  POP_JUMP_IF_FALSE  3630  'to 3630'

 L. 545      3588  LOAD_GLOBAL              int
             3590  LOAD_FAST                'word'
             3592  CALL_FUNCTION_1       1  '1 positional argument'
             3594  LOAD_CONST               2400
             3596  COMPARE_OP               >
         3598_3600  POP_JUMP_IF_FALSE  3630  'to 3630'

 L. 548      3602  LOAD_GLOBAL              int
             3604  LOAD_FAST                'word'
             3606  CALL_FUNCTION_1       1  '1 positional argument'
             3608  STORE_DEREF              'hrOffset'

 L. 549      3610  LOAD_CONST               2
             3612  STORE_FAST               'used'

 L. 550      3614  LOAD_CONST               False
             3616  STORE_FAST               'isTime'

 L. 551      3618  LOAD_CONST               -1
             3620  STORE_DEREF              'hrAbs'

 L. 552      3622  LOAD_CONST               -1
             3624  STORE_DEREF              'minAbs'
         3626_3628  JUMP_FORWARD       4192  'to 4192'
           3630_0  COME_FROM          3598  '3598'
           3630_1  COME_FROM          3584  '3584'
           3630_2  COME_FROM          3570  '3570'
           3630_3  COME_FROM          3556  '3556'

 L. 554      3630  LOAD_FAST                'wordNext'
             3632  LOAD_STR                 'minutes'
             3634  COMPARE_OP               ==
         3636_3638  POP_JUMP_IF_FALSE  3668  'to 3668'

 L. 556      3640  LOAD_GLOBAL              int
             3642  LOAD_FAST                'word'
             3644  CALL_FUNCTION_1       1  '1 positional argument'
             3646  STORE_DEREF              'minOffset'

 L. 557      3648  LOAD_CONST               2
             3650  STORE_FAST               'used'

 L. 558      3652  LOAD_CONST               False
             3654  STORE_FAST               'isTime'

 L. 559      3656  LOAD_CONST               -1
             3658  STORE_DEREF              'hrAbs'

 L. 560      3660  LOAD_CONST               -1
             3662  STORE_DEREF              'minAbs'
         3664_3666  JUMP_FORWARD       4192  'to 4192'
           3668_0  COME_FROM          3636  '3636'

 L. 561      3668  LOAD_FAST                'wordNext'
             3670  LOAD_STR                 'seconds'
             3672  COMPARE_OP               ==
         3674_3676  POP_JUMP_IF_FALSE  3706  'to 3706'

 L. 563      3678  LOAD_GLOBAL              int
             3680  LOAD_FAST                'word'
             3682  CALL_FUNCTION_1       1  '1 positional argument'
             3684  STORE_DEREF              'secOffset'

 L. 564      3686  LOAD_CONST               2
             3688  STORE_FAST               'used'

 L. 565      3690  LOAD_CONST               False
             3692  STORE_FAST               'isTime'

 L. 566      3694  LOAD_CONST               -1
             3696  STORE_DEREF              'hrAbs'

 L. 567      3698  LOAD_CONST               -1
             3700  STORE_DEREF              'minAbs'
         3702_3704  JUMP_FORWARD       4192  'to 4192'
           3706_0  COME_FROM          3674  '3674'

 L. 568      3706  LOAD_GLOBAL              int
             3708  LOAD_FAST                'word'
             3710  CALL_FUNCTION_1       1  '1 positional argument'
             3712  LOAD_CONST               100
             3714  COMPARE_OP               >
         3716_3718  POP_JUMP_IF_FALSE  3770  'to 3770'

 L. 569      3720  LOAD_GLOBAL              int
             3722  LOAD_FAST                'word'
             3724  CALL_FUNCTION_1       1  '1 positional argument'
             3726  LOAD_CONST               100
             3728  BINARY_TRUE_DIVIDE
             3730  STORE_FAST               'strHH'

 L. 570      3732  LOAD_GLOBAL              int
             3734  LOAD_FAST                'word'
             3736  CALL_FUNCTION_1       1  '1 positional argument'
             3738  LOAD_FAST                'strHH'
             3740  LOAD_CONST               100
             3742  BINARY_MULTIPLY  
             3744  BINARY_SUBTRACT  
             3746  STORE_FAST               'strMM'

 L. 571      3748  LOAD_FAST                'wordNext'
             3750  LOAD_STR                 'hours'
             3752  COMPARE_OP               ==
         3754_3756  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 572      3758  LOAD_FAST                'used'
             3760  LOAD_CONST               1
             3762  INPLACE_ADD      
             3764  STORE_FAST               'used'
         3766_3768  JUMP_FORWARD       4192  'to 4192'
           3770_0  COME_FROM          3716  '3716'

 L. 573      3770  LOAD_FAST                'wordNext'
             3772  LOAD_CONST               0
             3774  BINARY_SUBSCR    
             3776  LOAD_METHOD              isdigit
             3778  CALL_METHOD_0         0  '0 positional arguments'
         3780_3782  POP_JUMP_IF_FALSE  3822  'to 3822'

 L. 574      3784  LOAD_FAST                'word'
             3786  STORE_FAST               'strHH'

 L. 575      3788  LOAD_FAST                'wordNext'
             3790  STORE_FAST               'strMM'

 L. 576      3792  LOAD_FAST                'used'
             3794  LOAD_CONST               1
             3796  INPLACE_ADD      
             3798  STORE_FAST               'used'

 L. 577      3800  LOAD_FAST                'wordNextNext'
             3802  LOAD_STR                 'hours'
             3804  COMPARE_OP               ==
         3806_3808  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 578      3810  LOAD_FAST                'used'
             3812  LOAD_CONST               1
             3814  INPLACE_ADD      
             3816  STORE_FAST               'used'
         3818_3820  JUMP_FORWARD       4192  'to 4192'
           3822_0  COME_FROM          3780  '3780'

 L. 580      3822  LOAD_FAST                'wordNext'
             3824  LOAD_STR                 ''
             3826  COMPARE_OP               ==
         3828_3830  POP_JUMP_IF_TRUE   3872  'to 3872'
             3832  LOAD_FAST                'wordNext'
             3834  LOAD_STR                 "o'clock"
             3836  COMPARE_OP               ==
         3838_3840  POP_JUMP_IF_TRUE   3872  'to 3872'

 L. 582      3842  LOAD_FAST                'wordNext'
             3844  LOAD_STR                 'in'
             3846  COMPARE_OP               ==
         3848_3850  POP_JUMP_IF_FALSE  4188  'to 4188'

 L. 584      3852  LOAD_FAST                'wordNextNext'
             3854  LOAD_STR                 'the'
             3856  COMPARE_OP               ==
         3858_3860  POP_JUMP_IF_TRUE   3872  'to 3872'

 L. 585      3862  LOAD_FAST                'wordNextNext'
             3864  LOAD_FAST                'timeQualifier'
             3866  COMPARE_OP               ==
         3868_3870  POP_JUMP_IF_FALSE  4188  'to 4188'
           3872_0  COME_FROM          3858  '3858'
           3872_1  COME_FROM          3838  '3838'
           3872_2  COME_FROM          3828  '3828'

 L. 588      3872  LOAD_FAST                'word'
             3874  STORE_FAST               'strHH'

 L. 589      3876  LOAD_CONST               0
             3878  STORE_FAST               'strMM'

 L. 590      3880  LOAD_FAST                'wordNext'
             3882  LOAD_STR                 "o'clock"
             3884  COMPARE_OP               ==
         3886_3888  POP_JUMP_IF_FALSE  3898  'to 3898'

 L. 591      3890  LOAD_FAST                'used'
             3892  LOAD_CONST               1
             3894  INPLACE_ADD      
             3896  STORE_FAST               'used'
           3898_0  COME_FROM          3886  '3886'

 L. 592      3898  LOAD_FAST                'wordNext'
             3900  LOAD_STR                 'in'
             3902  COMPARE_OP               ==
         3904_3906  POP_JUMP_IF_TRUE   3918  'to 3918'
             3908  LOAD_FAST                'wordNextNext'
             3910  LOAD_STR                 'in'
             3912  COMPARE_OP               ==
         3914_3916  POP_JUMP_IF_FALSE  4192  'to 4192'
           3918_0  COME_FROM          3904  '3904'

 L. 593      3918  LOAD_FAST                'used'
             3920  LOAD_FAST                'wordNext'
             3922  LOAD_STR                 'in'
             3924  COMPARE_OP               ==
         3926_3928  POP_JUMP_IF_FALSE  3934  'to 3934'
             3930  LOAD_CONST               1
             3932  JUMP_FORWARD       3936  'to 3936'
           3934_0  COME_FROM          3926  '3926'
             3934  LOAD_CONST               2
           3936_0  COME_FROM          3932  '3932'
             3936  INPLACE_ADD      
             3938  STORE_FAST               'used'

 L. 594      3940  LOAD_FAST                'wordNextNext'
         3942_3944  POP_JUMP_IF_FALSE  3956  'to 3956'

 L. 595      3946  LOAD_FAST                'wordNextNext'
             3948  LOAD_FAST                'timeQualifier'
             3950  COMPARE_OP               in
         3952_3954  POP_JUMP_IF_TRUE   4000  'to 4000'
           3956_0  COME_FROM          3942  '3942'

 L. 596      3956  LOAD_FAST                'words'
             3958  LOAD_FAST                'words'
             3960  LOAD_METHOD              index
             3962  LOAD_FAST                'wordNextNext'
             3964  CALL_METHOD_1         1  '1 positional argument'
           3966_0  COME_FROM          2948  '2948'
             3966  LOAD_CONST               1
             3968  BINARY_ADD       
             3970  BINARY_SUBSCR    
         3972_3974  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 597      3976  LOAD_FAST                'words'
             3978  LOAD_FAST                'words'
             3980  LOAD_METHOD              index
             3982  LOAD_FAST                'wordNextNext'
             3984  CALL_METHOD_1         1  '1 positional argument'
             3986  LOAD_CONST               1
             3988  BINARY_ADD       
             3990  BINARY_SUBSCR    

 L. 598      3992  LOAD_FAST                'timeQualifier'
             3994  COMPARE_OP               in
         3996_3998  POP_JUMP_IF_FALSE  4192  'to 4192'
           4000_0  COME_FROM          3952  '3952'
           4000_1  COME_FROM          2982  '2982'

 L. 599      4000  LOAD_FAST                'wordNextNext'
             4002  LOAD_STR                 'afternoon'
             4004  COMPARE_OP               ==
         4006_4008  POP_JUMP_IF_TRUE   4058  'to 4058'

 L. 600      4010  LOAD_GLOBAL              len
             4012  LOAD_FAST                'words'
             4014  CALL_FUNCTION_1       1  '1 positional argument'

 L. 601      4016  LOAD_FAST                'words'
             4018  LOAD_METHOD              index
             4020  LOAD_FAST                'wordNextNext'
             4022  CALL_METHOD_1         1  '1 positional argument'
             4024  LOAD_CONST               1
             4026  BINARY_ADD       
             4028  COMPARE_OP               >
           4030_0  COME_FROM          3012  '3012'
         4030_4032  POP_JUMP_IF_FALSE  4062  'to 4062'

 L. 602      4034  LOAD_FAST                'words'
             4036  LOAD_FAST                'words'
             4038  LOAD_METHOD              index

 L. 603      4040  LOAD_FAST                'wordNextNext'
             4042  CALL_METHOD_1         1  '1 positional argument'
             4044  LOAD_CONST               1
             4046  BINARY_ADD       
             4048  BINARY_SUBSCR    
             4050  LOAD_STR                 'afternoon'
             4052  COMPARE_OP               ==
         4054_4056  POP_JUMP_IF_FALSE  4062  'to 4062'
           4058_0  COME_FROM          4006  '4006'

 L. 604      4058  LOAD_STR                 'pm'
           4060_0  COME_FROM          3042  '3042'
             4060  STORE_FAST               'remainder'
           4062_0  COME_FROM          4054  '4054'
           4062_1  COME_FROM          4030  '4030'

 L. 605      4062  LOAD_FAST                'wordNextNext'
             4064  LOAD_STR                 'evening'
             4066  COMPARE_OP               ==
         4068_4070  POP_JUMP_IF_TRUE   4120  'to 4120'

 L. 606      4072  LOAD_GLOBAL              len
             4074  LOAD_FAST                'words'
             4076  CALL_FUNCTION_1       1  '1 positional argument'

 L. 607      4078  LOAD_FAST                'words'
             4080  LOAD_METHOD              index
             4082  LOAD_FAST                'wordNextNext'
             4084  CALL_METHOD_1         1  '1 positional argument'
             4086  LOAD_CONST               1
             4088  BINARY_ADD       
           4090_0  COME_FROM          3072  '3072'
             4090  COMPARE_OP               >
         4092_4094  POP_JUMP_IF_FALSE  4124  'to 4124'

 L. 608      4096  LOAD_FAST                'words'
             4098  LOAD_FAST                'words'
             4100  LOAD_METHOD              index

 L. 609      4102  LOAD_FAST                'wordNextNext'
             4104  CALL_METHOD_1         1  '1 positional argument'
             4106  LOAD_CONST               1
             4108  BINARY_ADD       
             4110  BINARY_SUBSCR    
             4112  LOAD_STR                 'evening'
             4114  COMPARE_OP               ==
         4116_4118  POP_JUMP_IF_FALSE  4124  'to 4124'
           4120_0  COME_FROM          4068  '4068'

 L. 610      4120  LOAD_STR                 'pm'
             4122  STORE_FAST               'remainder'
           4124_0  COME_FROM          4116  '4116'
           4124_1  COME_FROM          4092  '4092'

 L. 611      4124  LOAD_FAST                'wordNextNext'
             4126  LOAD_STR                 'morning'
             4128  COMPARE_OP               ==
         4130_4132  POP_JUMP_IF_TRUE   4182  'to 4182'

 L. 612      4134  LOAD_GLOBAL              len
             4136  LOAD_FAST                'words'
             4138  CALL_FUNCTION_1       1  '1 positional argument'
           4140_0  COME_FROM          3122  '3122'

 L. 613      4140  LOAD_FAST                'words'
             4142  LOAD_METHOD              index
             4144  LOAD_FAST                'wordNextNext'
             4146  CALL_METHOD_1         1  '1 positional argument'
             4148  LOAD_CONST               1
             4150  BINARY_ADD       
             4152  COMPARE_OP               >
         4154_4156  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 614      4158  LOAD_FAST                'words'
             4160  LOAD_FAST                'words'
             4162  LOAD_METHOD              index

 L. 615      4164  LOAD_FAST                'wordNextNext'
             4166  CALL_METHOD_1         1  '1 positional argument'
             4168  LOAD_CONST               1
             4170  BINARY_ADD       
             4172  BINARY_SUBSCR    
             4174  LOAD_STR                 'morning'
             4176  COMPARE_OP               ==
         4178_4180  POP_JUMP_IF_FALSE  4192  'to 4192'
           4182_0  COME_FROM          4130  '4130'

 L. 616      4182  LOAD_STR                 'am'
             4184  STORE_FAST               'remainder'
             4186  JUMP_FORWARD       4192  'to 4192'
           4188_0  COME_FROM          3868  '3868'
           4188_1  COME_FROM          3848  '3848'

 L. 618      4188  LOAD_CONST               False
             4190  STORE_FAST               'isTime'
           4192_0  COME_FROM          4186  '4186'
           4192_1  COME_FROM          4178  '4178'
           4192_2  COME_FROM          4154  '4154'
           4192_3  COME_FROM          3996  '3996'
           4192_4  COME_FROM          3972  '3972'
           4192_5  COME_FROM          3914  '3914'
           4192_6  COME_FROM          3818  '3818'
           4192_7  COME_FROM          3806  '3806'
           4192_8  COME_FROM          3766  '3766'
           4192_9  COME_FROM          3754  '3754'
          4192_10  COME_FROM          3702  '3702'
          4192_11  COME_FROM          3664  '3664'
          4192_12  COME_FROM          3626  '3626'
          4192_13  COME_FROM          3546  '3546'
          4192_14  COME_FROM          3534  '3534'
          4192_15  COME_FROM          3462  '3462'
          4192_16  COME_FROM          3426  '3426'
          4192_17  COME_FROM          3390  '3390'
          4192_18  COME_FROM          3334  '3334'
          4192_19  COME_FROM          3172  '3172'
          4192_20  COME_FROM          3160  '3160'
          4192_21  COME_FROM          3140  '3140'
          4192_22  COME_FROM          3130  '3130'
          4192_23  COME_FROM          2640  '2640'

 L. 620      4192  LOAD_FAST                'strHH'
         4194_4196  POP_JUMP_IF_FALSE  4206  'to 4206'
             4198  LOAD_GLOBAL              int
             4200  LOAD_FAST                'strHH'
             4202  CALL_FUNCTION_1       1  '1 positional argument'
             4204  JUMP_FORWARD       4208  'to 4208'
           4206_0  COME_FROM          4194  '4194'
             4206  LOAD_CONST               0
           4208_0  COME_FROM          4204  '4204'
             4208  STORE_FAST               'strHH'

 L. 621      4210  LOAD_FAST                'strMM'
         4212_4214  POP_JUMP_IF_FALSE  4224  'to 4224'
             4216  LOAD_GLOBAL              int
             4218  LOAD_FAST                'strMM'
             4220  CALL_FUNCTION_1       1  '1 positional argument'
             4222  JUMP_FORWARD       4226  'to 4226'
           4224_0  COME_FROM          4212  '4212'
             4224  LOAD_CONST               0
           4226_0  COME_FROM          4222  '4222'
             4226  STORE_FAST               'strMM'

 L. 622      4228  LOAD_FAST                'remainder'
             4230  LOAD_STR                 'pm'
             4232  COMPARE_OP               ==
         4234_4236  POP_JUMP_IF_FALSE  4256  'to 4256'
             4238  LOAD_FAST                'strHH'
             4240  LOAD_CONST               12
             4242  COMPARE_OP               <
         4244_4246  POP_JUMP_IF_FALSE  4256  'to 4256'
             4248  LOAD_FAST                'strHH'
             4250  LOAD_CONST               12
             4252  BINARY_ADD       
             4254  JUMP_FORWARD       4258  'to 4258'
           4256_0  COME_FROM          4244  '4244'
           4256_1  COME_FROM          4234  '4234'
             4256  LOAD_FAST                'strHH'
           4258_0  COME_FROM          4254  '4254'
             4258  STORE_FAST               'strHH'

 L. 623      4260  LOAD_FAST                'remainder'
             4262  LOAD_STR                 'am'
             4264  COMPARE_OP               ==
         4266_4268  POP_JUMP_IF_FALSE  4288  'to 4288'
             4270  LOAD_FAST                'strHH'
             4272  LOAD_CONST               12
             4274  COMPARE_OP               >=
         4276_4278  POP_JUMP_IF_FALSE  4288  'to 4288'
             4280  LOAD_FAST                'strHH'
             4282  LOAD_CONST               12
             4284  BINARY_SUBTRACT  
             4286  JUMP_FORWARD       4290  'to 4290'
           4288_0  COME_FROM          4276  '4276'
           4288_1  COME_FROM          4266  '4266'
             4288  LOAD_FAST                'strHH'
           4290_0  COME_FROM          4286  '4286'
             4290  STORE_FAST               'strHH'

 L. 624      4292  LOAD_FAST                'strHH'
             4294  LOAD_CONST               24
             4296  COMPARE_OP               >
         4298_4300  POP_JUMP_IF_TRUE   4312  'to 4312'
             4302  LOAD_FAST                'strMM'
             4304  LOAD_CONST               59
             4306  COMPARE_OP               >
         4308_4310  POP_JUMP_IF_FALSE  4320  'to 4320'
           4312_0  COME_FROM          4298  '4298'

 L. 625      4312  LOAD_CONST               False
             4314  STORE_FAST               'isTime'

 L. 626      4316  LOAD_CONST               0
             4318  STORE_FAST               'used'
           4320_0  COME_FROM          4308  '4308'

 L. 627      4320  LOAD_FAST                'isTime'
         4322_4324  POP_JUMP_IF_FALSE  4350  'to 4350'

 L. 628      4326  LOAD_FAST                'strHH'
             4328  LOAD_CONST               1
             4330  BINARY_MULTIPLY  
             4332  STORE_DEREF              'hrAbs'

 L. 629      4334  LOAD_FAST                'strMM'
             4336  LOAD_CONST               1
             4338  BINARY_MULTIPLY  
             4340  STORE_DEREF              'minAbs'

 L. 630      4342  LOAD_FAST                'used'
             4344  LOAD_CONST               1
             4346  INPLACE_ADD      
             4348  STORE_FAST               'used'
           4350_0  COME_FROM          4322  '4322'
           4350_1  COME_FROM          2416  '2416'
           4350_2  COME_FROM          2402  '2402'
           4350_3  COME_FROM          2284  '2284'
           4350_4  COME_FROM          2252  '2252'
           4350_5  COME_FROM          2220  '2220'
           4350_6  COME_FROM          2188  '2188'
           4350_7  COME_FROM          2156  '2156'
           4350_8  COME_FROM          2130  '2130'

 L. 631      4350  LOAD_FAST                'used'
             4352  LOAD_CONST               0
             4354  COMPARE_OP               >
         4356_4358  POP_JUMP_IF_FALSE  1960  'to 1960'

 L. 633      4360  SETUP_LOOP         4392  'to 4392'
             4362  LOAD_GLOBAL              range
             4364  LOAD_FAST                'used'
             4366  CALL_FUNCTION_1       1  '1 positional argument'
             4368  GET_ITER         
             4370  FOR_ITER           4390  'to 4390'
             4372  STORE_FAST               'i'

 L. 634      4374  LOAD_STR                 ''
             4376  LOAD_FAST                'words'
             4378  LOAD_FAST                'idx'
             4380  LOAD_FAST                'i'
             4382  BINARY_ADD       
             4384  STORE_SUBSCR     
         4386_4388  JUMP_BACK          4370  'to 4370'
             4390  POP_BLOCK        
           4392_0  COME_FROM_LOOP     4360  '4360'

 L. 636      4392  LOAD_FAST                'wordPrev'
             4394  LOAD_STR                 'o'
             4396  COMPARE_OP               ==
         4398_4400  POP_JUMP_IF_TRUE   4412  'to 4412'
             4402  LOAD_FAST                'wordPrev'
             4404  LOAD_STR                 'oh'
             4406  COMPARE_OP               ==
         4408_4410  POP_JUMP_IF_FALSE  4426  'to 4426'
           4412_0  COME_FROM          4398  '4398'

 L. 637      4412  LOAD_STR                 ''
             4414  LOAD_FAST                'words'
             4416  LOAD_FAST                'words'
             4418  LOAD_METHOD              index
             4420  LOAD_FAST                'wordPrev'
             4422  CALL_METHOD_1         1  '1 positional argument'
             4424  STORE_SUBSCR     
           4426_0  COME_FROM          4408  '4408'

 L. 639      4426  LOAD_FAST                'wordPrev'
             4428  LOAD_STR                 'early'
             4430  COMPARE_OP               ==
         4432_4434  POP_JUMP_IF_FALSE  4462  'to 4462'

 L. 640      4436  LOAD_CONST               -1
             4438  STORE_DEREF              'hrOffset'

 L. 641      4440  LOAD_STR                 ''
             4442  LOAD_FAST                'words'
             4444  LOAD_FAST                'idx'
             4446  LOAD_CONST               1
             4448  BINARY_SUBTRACT  
             4450  STORE_SUBSCR     

 L. 642      4452  LOAD_FAST                'idx'
             4454  LOAD_CONST               1
             4456  INPLACE_SUBTRACT 
             4458  STORE_FAST               'idx'
             4460  JUMP_FORWARD       4496  'to 4496'
           4462_0  COME_FROM          4432  '4432'

 L. 643      4462  LOAD_FAST                'wordPrev'
             4464  LOAD_STR                 'late'
             4466  COMPARE_OP               ==
         4468_4470  POP_JUMP_IF_FALSE  4496  'to 4496'

 L. 644      4472  LOAD_CONST               1
             4474  STORE_DEREF              'hrOffset'

 L. 645      4476  LOAD_STR                 ''
             4478  LOAD_FAST                'words'
             4480  LOAD_FAST                'idx'
             4482  LOAD_CONST               1
             4484  BINARY_SUBTRACT  
             4486  STORE_SUBSCR     

 L. 646      4488  LOAD_FAST                'idx'
             4490  LOAD_CONST               1
             4492  INPLACE_SUBTRACT 
             4494  STORE_FAST               'idx'
           4496_0  COME_FROM          4468  '4468'
           4496_1  COME_FROM          4460  '4460'

 L. 647      4496  LOAD_FAST                'idx'
             4498  LOAD_CONST               0
             4500  COMPARE_OP               >
         4502_4504  POP_JUMP_IF_FALSE  4528  'to 4528'
             4506  LOAD_FAST                'wordPrev'
             4508  LOAD_FAST                'markers'
             4510  COMPARE_OP               in
         4512_4514  POP_JUMP_IF_FALSE  4528  'to 4528'

 L. 648      4516  LOAD_STR                 ''
             4518  LOAD_FAST                'words'
             4520  LOAD_FAST                'idx'
             4522  LOAD_CONST               1
             4524  BINARY_SUBTRACT  
             4526  STORE_SUBSCR     
           4528_0  COME_FROM          4512  '4512'
           4528_1  COME_FROM          4502  '4502'

 L. 649      4528  LOAD_FAST                'idx'
             4530  LOAD_CONST               1
             4532  COMPARE_OP               >
         4534_4536  POP_JUMP_IF_FALSE  4560  'to 4560'
             4538  LOAD_FAST                'wordPrevPrev'
             4540  LOAD_FAST                'markers'
             4542  COMPARE_OP               in
         4544_4546  POP_JUMP_IF_FALSE  4560  'to 4560'

 L. 650      4548  LOAD_STR                 ''
             4550  LOAD_FAST                'words'
             4552  LOAD_FAST                'idx'
             4554  LOAD_CONST               2
             4556  BINARY_SUBTRACT  
             4558  STORE_SUBSCR     
           4560_0  COME_FROM          4544  '4544'
           4560_1  COME_FROM          4534  '4534'

 L. 652      4560  LOAD_FAST                'idx'
             4562  LOAD_FAST                'used'
             4564  LOAD_CONST               1
             4566  BINARY_SUBTRACT  
             4568  INPLACE_ADD      
             4570  STORE_FAST               'idx'

 L. 653      4572  LOAD_CONST               True
             4574  STORE_DEREF              'found'
         4576_4578  JUMP_BACK          1960  'to 1960'
             4580  POP_BLOCK        
           4582_0  COME_FROM_LOOP     1948  '1948'

 L. 656      4582  LOAD_FAST                'date_found'
         4584_4586  POP_JUMP_IF_TRUE   4592  'to 4592'

 L. 657      4588  LOAD_CONST               None
             4590  RETURN_VALUE     
           4592_0  COME_FROM          4584  '4584'

 L. 659      4592  LOAD_DEREF               'dayOffset'
             4594  LOAD_CONST               False
             4596  COMPARE_OP               is
         4598_4600  POP_JUMP_IF_FALSE  4606  'to 4606'

 L. 660      4602  LOAD_CONST               0
             4604  STORE_DEREF              'dayOffset'
           4606_0  COME_FROM          4598  '4598'

 L. 664      4606  LOAD_FAST                'dateNow'
             4608  STORE_FAST               'extractedDate'

 L. 665      4610  LOAD_FAST                'extractedDate'
             4612  LOAD_ATTR                replace
             4614  LOAD_CONST               0

 L. 666      4616  LOAD_CONST               0

 L. 667      4618  LOAD_CONST               0

 L. 668      4620  LOAD_CONST               0
             4622  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             4624  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4626  STORE_FAST               'extractedDate'

 L. 669      4628  LOAD_DEREF               'datestr'
             4630  LOAD_STR                 ''
             4632  COMPARE_OP               !=
         4634_4636  POP_JUMP_IF_FALSE  4814  'to 4814'

 L. 670      4638  LOAD_GLOBAL              datetime
             4640  LOAD_METHOD              strptime
             4642  LOAD_DEREF               'datestr'
             4644  LOAD_STR                 '%B %d'
             4646  CALL_METHOD_2         2  '2 positional arguments'
             4648  STORE_FAST               'temp'

 L. 671      4650  LOAD_FAST                'hasYear'
         4652_4654  POP_JUMP_IF_TRUE   4768  'to 4768'

 L. 672      4656  LOAD_FAST                'temp'
             4658  LOAD_ATTR                replace
             4660  LOAD_FAST                'extractedDate'
             4662  LOAD_ATTR                year
             4664  LOAD_CONST               ('year',)
             4666  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4668  STORE_FAST               'temp'

 L. 673      4670  LOAD_FAST                'extractedDate'
             4672  LOAD_FAST                'temp'
             4674  COMPARE_OP               <
         4676_4678  POP_JUMP_IF_FALSE  4722  'to 4722'

 L. 674      4680  LOAD_FAST                'extractedDate'
             4682  LOAD_ATTR                replace
             4684  LOAD_GLOBAL              int
             4686  LOAD_FAST                'currentYear'
             4688  CALL_FUNCTION_1       1  '1 positional argument'

 L. 675      4690  LOAD_GLOBAL              int

 L. 676      4692  LOAD_FAST                'temp'
             4694  LOAD_METHOD              strftime

 L. 677      4696  LOAD_STR                 '%m'
             4698  CALL_METHOD_1         1  '1 positional argument'
             4700  CALL_FUNCTION_1       1  '1 positional argument'

 L. 678      4702  LOAD_GLOBAL              int
             4704  LOAD_FAST                'temp'
             4706  LOAD_METHOD              strftime

 L. 679      4708  LOAD_STR                 '%d'
             4710  CALL_METHOD_1         1  '1 positional argument'
             4712  CALL_FUNCTION_1       1  '1 positional argument'
             4714  LOAD_CONST               ('year', 'month', 'day')
             4716  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4718  STORE_FAST               'extractedDate'
             4720  JUMP_FORWARD       4766  'to 4766'
           4722_0  COME_FROM          4676  '4676'

 L. 681      4722  LOAD_FAST                'extractedDate'
             4724  LOAD_ATTR                replace

 L. 682      4726  LOAD_GLOBAL              int
             4728  LOAD_FAST                'currentYear'
             4730  CALL_FUNCTION_1       1  '1 positional argument'
             4732  LOAD_CONST               1
             4734  BINARY_ADD       

 L. 683      4736  LOAD_GLOBAL              int
             4738  LOAD_FAST                'temp'
             4740  LOAD_METHOD              strftime
             4742  LOAD_STR                 '%m'
             4744  CALL_METHOD_1         1  '1 positional argument'
             4746  CALL_FUNCTION_1       1  '1 positional argument'

 L. 684      4748  LOAD_GLOBAL              int
             4750  LOAD_FAST                'temp'
             4752  LOAD_METHOD              strftime
             4754  LOAD_STR                 '%d'
             4756  CALL_METHOD_1         1  '1 positional argument'
             4758  CALL_FUNCTION_1       1  '1 positional argument'
             4760  LOAD_CONST               ('year', 'month', 'day')
             4762  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4764  STORE_FAST               'extractedDate'
           4766_0  COME_FROM          4720  '4720'
             4766  JUMP_FORWARD       4814  'to 4814'
           4768_0  COME_FROM          4652  '4652'

 L. 686      4768  LOAD_FAST                'extractedDate'
             4770  LOAD_ATTR                replace

 L. 687      4772  LOAD_GLOBAL              int
             4774  LOAD_FAST                'temp'
             4776  LOAD_METHOD              strftime
             4778  LOAD_STR                 '%Y'
             4780  CALL_METHOD_1         1  '1 positional argument'
             4782  CALL_FUNCTION_1       1  '1 positional argument'

 L. 688      4784  LOAD_GLOBAL              int
             4786  LOAD_FAST                'temp'
             4788  LOAD_METHOD              strftime
             4790  LOAD_STR                 '%m'
             4792  CALL_METHOD_1         1  '1 positional argument'
             4794  CALL_FUNCTION_1       1  '1 positional argument'

 L. 689      4796  LOAD_GLOBAL              int
             4798  LOAD_FAST                'temp'
             4800  LOAD_METHOD              strftime
             4802  LOAD_STR                 '%d'
             4804  CALL_METHOD_1         1  '1 positional argument'
             4806  CALL_FUNCTION_1       1  '1 positional argument'
             4808  LOAD_CONST               ('year', 'month', 'day')
             4810  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4812  STORE_FAST               'extractedDate'
           4814_0  COME_FROM          4766  '4766'
           4814_1  COME_FROM          4634  '4634'

 L. 691      4814  LOAD_DEREF               'timeStr'
             4816  LOAD_STR                 ''
             4818  COMPARE_OP               !=
         4820_4822  POP_JUMP_IF_FALSE  4866  'to 4866'

 L. 692      4824  LOAD_GLOBAL              datetime
             4826  LOAD_DEREF               'timeStr'
             4828  CALL_FUNCTION_1       1  '1 positional argument'
             4830  STORE_FAST               'temp'

 L. 693      4832  LOAD_FAST                'extractedDate'
             4834  LOAD_ATTR                replace
             4836  LOAD_FAST                'temp'
             4838  LOAD_METHOD              strftime
             4840  LOAD_STR                 '%H'
             4842  CALL_METHOD_1         1  '1 positional argument'

 L. 694      4844  LOAD_FAST                'temp'
             4846  LOAD_METHOD              strftime
             4848  LOAD_STR                 '%M'
             4850  CALL_METHOD_1         1  '1 positional argument'

 L. 695      4852  LOAD_FAST                'temp'
             4854  LOAD_METHOD              strftime
             4856  LOAD_STR                 '%S'
             4858  CALL_METHOD_1         1  '1 positional argument'
             4860  LOAD_CONST               ('hour', 'minute', 'second')
             4862  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4864  STORE_FAST               'extractedDate'
           4866_0  COME_FROM          4820  '4820'

 L. 697      4866  LOAD_DEREF               'yearOffset'
             4868  LOAD_CONST               0
             4870  COMPARE_OP               !=
         4872_4874  POP_JUMP_IF_FALSE  4890  'to 4890'

 L. 698      4876  LOAD_FAST                'extractedDate'
             4878  LOAD_GLOBAL              relativedelta
             4880  LOAD_DEREF               'yearOffset'
             4882  LOAD_CONST               ('years',)
             4884  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4886  BINARY_ADD       
             4888  STORE_FAST               'extractedDate'
           4890_0  COME_FROM          4872  '4872'

 L. 699      4890  LOAD_DEREF               'monthOffset'
             4892  LOAD_CONST               0
             4894  COMPARE_OP               !=
         4896_4898  POP_JUMP_IF_FALSE  4914  'to 4914'

 L. 700      4900  LOAD_FAST                'extractedDate'
             4902  LOAD_GLOBAL              relativedelta
             4904  LOAD_DEREF               'monthOffset'
             4906  LOAD_CONST               ('months',)
             4908  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4910  BINARY_ADD       
             4912  STORE_FAST               'extractedDate'
           4914_0  COME_FROM          4896  '4896'

 L. 701      4914  LOAD_DEREF               'dayOffset'
             4916  LOAD_CONST               0
             4918  COMPARE_OP               !=
         4920_4922  POP_JUMP_IF_FALSE  4938  'to 4938'

 L. 702      4924  LOAD_FAST                'extractedDate'
             4926  LOAD_GLOBAL              relativedelta
             4928  LOAD_DEREF               'dayOffset'
             4930  LOAD_CONST               ('days',)
             4932  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4934  BINARY_ADD       
             4936  STORE_FAST               'extractedDate'
           4938_0  COME_FROM          4920  '4920'

 L. 704      4938  LOAD_DEREF               'hrAbs'
             4940  LOAD_CONST               None
             4942  COMPARE_OP               is
         4944_4946  POP_JUMP_IF_FALSE  4976  'to 4976'
             4948  LOAD_DEREF               'minAbs'
             4950  LOAD_CONST               None
             4952  COMPARE_OP               is
         4954_4956  POP_JUMP_IF_FALSE  4976  'to 4976'
             4958  LOAD_FAST                'default_time'
         4960_4962  POP_JUMP_IF_FALSE  4976  'to 4976'

 L. 705      4964  LOAD_FAST                'default_time'
             4966  LOAD_ATTR                hour
             4968  STORE_DEREF              'hrAbs'

 L. 706      4970  LOAD_FAST                'default_time'
             4972  LOAD_ATTR                minute
             4974  STORE_DEREF              'minAbs'
           4976_0  COME_FROM          4960  '4960'
           4976_1  COME_FROM          4954  '4954'
           4976_2  COME_FROM          4944  '4944'

 L. 707      4976  LOAD_DEREF               'hrAbs'
             4978  LOAD_CONST               -1
             4980  COMPARE_OP               !=
         4982_4984  POP_JUMP_IF_FALSE  5076  'to 5076'
             4986  LOAD_DEREF               'minAbs'
             4988  LOAD_CONST               -1
             4990  COMPARE_OP               !=
         4992_4994  POP_JUMP_IF_FALSE  5076  'to 5076'

 L. 708      4996  LOAD_FAST                'extractedDate'
             4998  LOAD_GLOBAL              relativedelta
             5000  LOAD_DEREF               'hrAbs'
         5002_5004  JUMP_IF_TRUE_OR_POP  5008  'to 5008'
             5006  LOAD_CONST               0
           5008_0  COME_FROM          5002  '5002'

 L. 709      5008  LOAD_DEREF               'minAbs'
         5010_5012  JUMP_IF_TRUE_OR_POP  5016  'to 5016'
             5014  LOAD_CONST               0
           5016_0  COME_FROM          5010  '5010'
             5016  LOAD_CONST               ('hours', 'minutes')
             5018  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5020  BINARY_ADD       
             5022  STORE_FAST               'extractedDate'

 L. 710      5024  LOAD_DEREF               'hrAbs'
         5026_5028  POP_JUMP_IF_TRUE   5036  'to 5036'
             5030  LOAD_DEREF               'minAbs'
         5032_5034  POP_JUMP_IF_FALSE  5076  'to 5076'
           5036_0  COME_FROM          5026  '5026'
             5036  LOAD_DEREF               'datestr'
             5038  LOAD_STR                 ''
             5040  COMPARE_OP               ==
         5042_5044  POP_JUMP_IF_FALSE  5076  'to 5076'

 L. 711      5046  LOAD_FAST                'daySpecified'
         5048_5050  POP_JUMP_IF_TRUE   5076  'to 5076'
             5052  LOAD_FAST                'dateNow'
             5054  LOAD_FAST                'extractedDate'
             5056  COMPARE_OP               >
         5058_5060  POP_JUMP_IF_FALSE  5076  'to 5076'

 L. 712      5062  LOAD_FAST                'extractedDate'
             5064  LOAD_GLOBAL              relativedelta
             5066  LOAD_CONST               1
             5068  LOAD_CONST               ('days',)
             5070  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5072  BINARY_ADD       
             5074  STORE_FAST               'extractedDate'
           5076_0  COME_FROM          5058  '5058'
           5076_1  COME_FROM          5048  '5048'
           5076_2  COME_FROM          5042  '5042'
           5076_3  COME_FROM          5032  '5032'
           5076_4  COME_FROM          4992  '4992'
           5076_5  COME_FROM          4982  '4982'

 L. 713      5076  LOAD_DEREF               'hrOffset'
             5078  LOAD_CONST               0
             5080  COMPARE_OP               !=
         5082_5084  POP_JUMP_IF_FALSE  5100  'to 5100'

 L. 714      5086  LOAD_FAST                'extractedDate'
             5088  LOAD_GLOBAL              relativedelta
             5090  LOAD_DEREF               'hrOffset'
             5092  LOAD_CONST               ('hours',)
             5094  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5096  BINARY_ADD       
             5098  STORE_FAST               'extractedDate'
           5100_0  COME_FROM          5082  '5082'

 L. 715      5100  LOAD_DEREF               'minOffset'
             5102  LOAD_CONST               0
             5104  COMPARE_OP               !=
         5106_5108  POP_JUMP_IF_FALSE  5124  'to 5124'

 L. 716      5110  LOAD_FAST                'extractedDate'
             5112  LOAD_GLOBAL              relativedelta
             5114  LOAD_DEREF               'minOffset'
             5116  LOAD_CONST               ('minutes',)
             5118  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5120  BINARY_ADD       
             5122  STORE_FAST               'extractedDate'
           5124_0  COME_FROM          5106  '5106'

 L. 717      5124  LOAD_DEREF               'secOffset'
             5126  LOAD_CONST               0
             5128  COMPARE_OP               !=
         5130_5132  POP_JUMP_IF_FALSE  5148  'to 5148'

 L. 718      5134  LOAD_FAST                'extractedDate'
             5136  LOAD_GLOBAL              relativedelta
             5138  LOAD_DEREF               'secOffset'
             5140  LOAD_CONST               ('seconds',)
             5142  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5144  BINARY_ADD       
             5146  STORE_FAST               'extractedDate'
           5148_0  COME_FROM          5130  '5130'

 L. 719      5148  SETUP_LOOP         5230  'to 5230'
             5150  LOAD_GLOBAL              enumerate
             5152  LOAD_FAST                'words'
             5154  CALL_FUNCTION_1       1  '1 positional argument'
             5156  GET_ITER         
           5158_0  COME_FROM          5212  '5212'
           5158_1  COME_FROM          5194  '5194'
           5158_2  COME_FROM          5176  '5176'
             5158  FOR_ITER           5228  'to 5228'
             5160  UNPACK_SEQUENCE_2     2 
             5162  STORE_FAST               'idx'
             5164  STORE_FAST               'word'

 L. 720      5166  LOAD_FAST                'words'
             5168  LOAD_FAST                'idx'
             5170  BINARY_SUBSCR    
             5172  LOAD_STR                 'and'
             5174  COMPARE_OP               ==
         5176_5178  POP_JUMP_IF_FALSE  5158  'to 5158'
             5180  LOAD_FAST                'words'
             5182  LOAD_FAST                'idx'
             5184  LOAD_CONST               1
             5186  BINARY_SUBTRACT  
             5188  BINARY_SUBSCR    
             5190  LOAD_STR                 ''
             5192  COMPARE_OP               ==
         5194_5196  POP_JUMP_IF_FALSE  5158  'to 5158'
             5198  LOAD_FAST                'words'

 L. 721      5200  LOAD_FAST                'idx'
             5202  LOAD_CONST               1
             5204  BINARY_ADD       
             5206  BINARY_SUBSCR    
             5208  LOAD_STR                 ''
             5210  COMPARE_OP               ==
         5212_5214  POP_JUMP_IF_FALSE  5158  'to 5158'

 L. 722      5216  LOAD_STR                 ''
             5218  LOAD_FAST                'words'
             5220  LOAD_FAST                'idx'
             5222  STORE_SUBSCR     
         5224_5226  JUMP_BACK          5158  'to 5158'
             5228  POP_BLOCK        
           5230_0  COME_FROM_LOOP     5148  '5148'

 L. 724      5230  LOAD_STR                 ' '
             5232  LOAD_METHOD              join
             5234  LOAD_FAST                'words'
             5236  CALL_METHOD_1         1  '1 positional argument'
             5238  STORE_FAST               'resultStr'

 L. 725      5240  LOAD_STR                 ' '
             5242  LOAD_METHOD              join
             5244  LOAD_FAST                'resultStr'
             5246  LOAD_METHOD              split
             5248  CALL_METHOD_0         0  '0 positional arguments'
             5250  CALL_METHOD_1         1  '1 positional argument'
             5252  STORE_FAST               'resultStr'

 L. 726      5254  LOAD_FAST                'extractedDate'
             5256  LOAD_FAST                'resultStr'
             5258  BUILD_LIST_2          2 
             5260  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_METHOD' instruction at offset 1428


def is_fractional_sv(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith'ars'(-3):
        input_str = input_str[:len(input_str) - 3]
    if input_str.endswith'ar'(-2):
        input_str = input_str[:len(input_str) - 2]
    if input_str.endswith'a'(-1):
        input_str = input_str[:len(input_str) - 1]
    if input_str.endswith's'(-1):
        input_str = input_str[:len(input_str) - 1]
    aFrac = ['hel', 'halv', 'tredjedel', 'fjärdedel', 'femtedel', 'sjättedel',
     'sjundedel', 'åttondel', 'niondel', 'tiondel', 'elftedel',
     'tolftedel']
    if input_str.lower() in aFrac:
        return 1.0 / (aFrac.index(input_str) + 1)
    if input_str == 'kvart':
        return 0.25
    if input_str == 'trekvart':
        return 0.75
    return False


def normalize_sv(text, remove_articles):
    """ English string normalization """
    words = text.split()
    normalized = ''
    for word in words:
        if word == 'en':
            word = 'ett'
        textNumbers = [
         'noll', 'ett', 'två', 'tre', 'fyra', 'fem', 'sex',
         'sju', 'åtta', 'nio', 'tio', 'elva', 'tolv',
         'tretton', 'fjorton', 'femton', 'sexton',
         'sjutton', 'arton', 'nitton', 'tjugo']
        if word in textNumbers:
            word = str(textNumbers.index(word))
        normalized += ' ' + word

    return normalized[1:]