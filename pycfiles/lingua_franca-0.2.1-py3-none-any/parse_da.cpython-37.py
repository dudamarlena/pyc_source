# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_da.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 33579 bytes
from datetime import datetime
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions, extract_numbers_generic
from lingua_franca.lang.format_da import pronounce_number_da
da_numbers = {'nul':0, 
 'en':1, 
 'et':1, 
 'to':2, 
 'tre':3, 
 'fire':4, 
 'fem':5, 
 'seks':6, 
 'syv':7, 
 'otte':8, 
 'ni':9, 
 'ti':10, 
 'elve':11, 
 'tolv':12, 
 'tretten':13, 
 'fjorten':14, 
 'femten':15, 
 'seksten':16, 
 'sytten':17, 
 'atten':18, 
 'nitten':19, 
 'tyve':20, 
 'enogtyve':21, 
 'toogtyve':22, 
 'treogtyve':23, 
 'fireogtyve':24, 
 'femogtyve':25, 
 'seksogtyve':26, 
 'syvogtyve':27, 
 'otteogtyve':28, 
 'niogtyve':29, 
 'tredive':30, 
 'enogtredive':31, 
 'fyrrre':40, 
 'halvtres':50, 
 'tres':60, 
 'halvfjers':70, 
 'firs':80, 
 'halvfems':90, 
 'hunderede':100, 
 'tohundrede':200, 
 'trehundrede':300, 
 'firehundrede':400, 
 'femhundrede':500, 
 'sekshundrede':600, 
 'syvhundrede':700, 
 'ottehundrede':800, 
 'nihundrede':900, 
 'tusinde':1000, 
 'million':1000000}

def extractnumber_da(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number

    undefined articles cannot be suppressed in German:
    'ein Pferd' means 'one horse' and 'a horse'

    """
    text = text.lower()
    aWords = text.split()
    aWords = [word for word in aWords if word not in ('den', 'det')]
    and_pass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            if word.isdigit():
                val = float(word)
        elif isFractional_da(word):
            val = isFractional_da(word)
        else:
            if isOrdinal_da(word):
                val = isOrdinal_da(word)
            else:
                if word in da_numbers:
                    val = da_numbers[word]
                    if count < len(aWords) - 1:
                        wordNext = aWords[(count + 1)]
                    else:
                        wordNext = ''
                    valNext = isFractional_da(wordNext)
                    if valNext:
                        val = val * valNext
                        aWords[count + 1] = ''
                elif not val:
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
            if count + 1 < len(aWords) and aWords[(count + 1)] == 'og':
                and_pass = True
                valPreAnd = val
                val = False
                count += 2
                continue
            else:
                if count + 2 < len(aWords):
                    if aWords[(count + 2)] == 'og':
                        and_pass = True
                        valPreAnd = val
                        val = False
                        count += 3
                        continue
                break

    return val or False


def extract_datetime_da--- This code section failed: ---

 L. 163         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_da.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 186         8  LOAD_CLOSURE             'datestr'
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
               34  LOAD_STR                 'extract_datetime_da.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 196        40  LOAD_FAST                'string'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'currentDate'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 197        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 199        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 200        60  LOAD_CONST               False
               62  STORE_FAST               'daySpecified'

 L. 201        64  LOAD_CONST               False
               66  STORE_DEREF              'dayOffset'

 L. 202        68  LOAD_CONST               0
               70  STORE_DEREF              'monthOffset'

 L. 203        72  LOAD_CONST               0
               74  STORE_DEREF              'yearOffset'

 L. 204        76  LOAD_FAST                'currentDate'
               78  STORE_FAST               'dateNow'

 L. 205        80  LOAD_FAST                'dateNow'
               82  LOAD_METHOD              strftime
               84  LOAD_STR                 '%w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'today'

 L. 206        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%Y'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'currentYear'

 L. 207       100  LOAD_CONST               False
              102  STORE_FAST               'fromFlag'

 L. 208       104  LOAD_STR                 ''
              106  STORE_DEREF              'datestr'

 L. 209       108  LOAD_CONST               False
              110  STORE_FAST               'hasYear'

 L. 210       112  LOAD_STR                 ''
              114  STORE_FAST               'timeQualifier'

 L. 212       116  LOAD_STR                 'tidlig'

 L. 213       118  LOAD_STR                 'morgen'

 L. 214       120  LOAD_STR                 'morgenen'

 L. 215       122  LOAD_STR                 'formidag'

 L. 216       124  LOAD_STR                 'formiddagen'

 L. 217       126  LOAD_STR                 'eftermiddag'

 L. 218       128  LOAD_STR                 'eftermiddagen'

 L. 219       130  LOAD_STR                 'aften'

 L. 220       132  LOAD_STR                 'aftenen'

 L. 221       134  LOAD_STR                 'nat'

 L. 222       136  LOAD_STR                 'natten'
              138  BUILD_LIST_11        11 
              140  STORE_FAST               'timeQualifiersList'

 L. 223       142  LOAD_STR                 'i'
              144  LOAD_STR                 'om'
              146  LOAD_STR                 'på'
              148  LOAD_STR                 'klokken'
              150  LOAD_STR                 'ved'
              152  BUILD_LIST_5          5 
              154  STORE_FAST               'markers'

 L. 224       156  LOAD_STR                 'mandag'
              158  LOAD_STR                 'tirsdag'
              160  LOAD_STR                 'onsdag'

 L. 225       162  LOAD_STR                 'torsdag'
              164  LOAD_STR                 'fredag'
              166  LOAD_STR                 'lørdag'
              168  LOAD_STR                 'søndag'
              170  BUILD_LIST_7          7 
              172  STORE_FAST               'days'

 L. 226       174  LOAD_STR                 'januar'
              176  LOAD_STR                 'februar'
              178  LOAD_STR                 'marts'
              180  LOAD_STR                 'april'
              182  LOAD_STR                 'maj'
              184  LOAD_STR                 'juni'

 L. 227       186  LOAD_STR                 'juli'
              188  LOAD_STR                 'august'
              190  LOAD_STR                 'september'
              192  LOAD_STR                 'oktober'
              194  LOAD_STR                 'november'

 L. 228       196  LOAD_STR                 'desember'
              198  BUILD_LIST_12        12 
              200  STORE_FAST               'months'

 L. 229       202  LOAD_STR                 'jan'
              204  LOAD_STR                 'feb'
              206  LOAD_STR                 'mar'
              208  LOAD_STR                 'apr'
              210  LOAD_STR                 'maj'
              212  LOAD_STR                 'juni'
              214  LOAD_STR                 'juli'
              216  LOAD_STR                 'aug'

 L. 230       218  LOAD_STR                 'sep'
              220  LOAD_STR                 'okt'
              222  LOAD_STR                 'nov'
              224  LOAD_STR                 'des'
              226  BUILD_LIST_12        12 
              228  STORE_FAST               'monthsShort'

 L. 232       230  LOAD_FAST                'days'
              232  LOAD_FAST                'months'
              234  BINARY_ADD       
              236  LOAD_FAST                'monthsShort'
              238  BINARY_ADD       
              240  STORE_FAST               'validFollowups'

 L. 233       242  LOAD_FAST                'validFollowups'
              244  LOAD_METHOD              append
              246  LOAD_STR                 'i dag'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          

 L. 234       252  LOAD_FAST                'validFollowups'
              254  LOAD_METHOD              append
              256  LOAD_STR                 'morgen'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  POP_TOP          

 L. 235       262  LOAD_FAST                'validFollowups'
              264  LOAD_METHOD              append
              266  LOAD_STR                 'næste'
              268  CALL_METHOD_1         1  '1 positional argument'
              270  POP_TOP          

 L. 236       272  LOAD_FAST                'validFollowups'
              274  LOAD_METHOD              append
              276  LOAD_STR                 'forige'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  POP_TOP          

 L. 237       282  LOAD_FAST                'validFollowups'
              284  LOAD_METHOD              append
              286  LOAD_STR                 'nu'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          

 L. 239       292  LOAD_FAST                'clean_string'
              294  LOAD_FAST                'string'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  STORE_FAST               'words'

 L. 241   300_302  SETUP_LOOP         2046  'to 2046'
              304  LOAD_GLOBAL              enumerate
              306  LOAD_FAST                'words'
              308  CALL_FUNCTION_1       1  '1 positional argument'
              310  GET_ITER         
            312_0  COME_FROM          1900  '1900'
          312_314  FOR_ITER           2044  'to 2044'
              316  UNPACK_SEQUENCE_2     2 
              318  STORE_FAST               'idx'
              320  STORE_FAST               'word'

 L. 242       322  LOAD_FAST                'word'
              324  LOAD_STR                 ''
              326  COMPARE_OP               ==
          328_330  POP_JUMP_IF_FALSE   336  'to 336'

 L. 243   332_334  CONTINUE            312  'to 312'
            336_0  COME_FROM           328  '328'

 L. 244       336  LOAD_FAST                'idx'
              338  LOAD_CONST               1
              340  COMPARE_OP               >
          342_344  POP_JUMP_IF_FALSE   358  'to 358'
              346  LOAD_FAST                'words'
              348  LOAD_FAST                'idx'
              350  LOAD_CONST               2
              352  BINARY_SUBTRACT  
              354  BINARY_SUBSCR    
              356  JUMP_FORWARD        360  'to 360'
            358_0  COME_FROM           342  '342'
              358  LOAD_STR                 ''
            360_0  COME_FROM           356  '356'
              360  STORE_FAST               'wordPrevPrev'

 L. 245       362  LOAD_FAST                'idx'
              364  LOAD_CONST               0
              366  COMPARE_OP               >
          368_370  POP_JUMP_IF_FALSE   384  'to 384'
              372  LOAD_FAST                'words'
              374  LOAD_FAST                'idx'
              376  LOAD_CONST               1
              378  BINARY_SUBTRACT  
              380  BINARY_SUBSCR    
              382  JUMP_FORWARD        386  'to 386'
            384_0  COME_FROM           368  '368'
              384  LOAD_STR                 ''
            386_0  COME_FROM           382  '382'
              386  STORE_FAST               'wordPrev'

 L. 246       388  LOAD_FAST                'idx'
              390  LOAD_CONST               1
              392  BINARY_ADD       
              394  LOAD_GLOBAL              len
              396  LOAD_FAST                'words'
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  COMPARE_OP               <
          402_404  POP_JUMP_IF_FALSE   418  'to 418'
              406  LOAD_FAST                'words'
              408  LOAD_FAST                'idx'
              410  LOAD_CONST               1
              412  BINARY_ADD       
              414  BINARY_SUBSCR    
              416  JUMP_FORWARD        420  'to 420'
            418_0  COME_FROM           402  '402'
              418  LOAD_STR                 ''
            420_0  COME_FROM           416  '416'
              420  STORE_FAST               'wordNext'

 L. 247       422  LOAD_FAST                'idx'
              424  LOAD_CONST               2
              426  BINARY_ADD       
              428  LOAD_GLOBAL              len
              430  LOAD_FAST                'words'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_FALSE   452  'to 452'
              440  LOAD_FAST                'words'
              442  LOAD_FAST                'idx'
              444  LOAD_CONST               2
              446  BINARY_ADD       
              448  BINARY_SUBSCR    
              450  JUMP_FORWARD        454  'to 454'
            452_0  COME_FROM           436  '436'
              452  LOAD_STR                 ''
            454_0  COME_FROM           450  '450'
              454  STORE_FAST               'wordNextNext'

 L. 249       456  LOAD_FAST                'idx'
              458  STORE_FAST               'start'

 L. 250       460  LOAD_CONST               0
              462  STORE_FAST               'used'

 L. 252       464  LOAD_FAST                'word'
              466  LOAD_FAST                'timeQualifiersList'
              468  COMPARE_OP               in
          470_472  POP_JUMP_IF_FALSE   482  'to 482'

 L. 253       474  LOAD_FAST                'word'
              476  STORE_FAST               'timeQualifier'
          478_480  JUMP_FORWARD       1598  'to 1598'
            482_0  COME_FROM           470  '470'

 L. 255       482  LOAD_FAST                'word'
              484  LOAD_STR                 'dag'
              486  COMPARE_OP               ==
          488_490  POP_JUMP_IF_FALSE   514  'to 514'
              492  LOAD_FAST                'fromFlag'
          494_496  POP_JUMP_IF_TRUE    514  'to 514'

 L. 256       498  LOAD_CONST               0
              500  STORE_DEREF              'dayOffset'

 L. 257       502  LOAD_FAST                'used'
              504  LOAD_CONST               1
              506  INPLACE_ADD      
              508  STORE_FAST               'used'
          510_512  JUMP_FORWARD       1598  'to 1598'
            514_0  COME_FROM           494  '494'
            514_1  COME_FROM           488  '488'

 L. 258       514  LOAD_FAST                'word'
              516  LOAD_STR                 'morgen'
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   566  'to 566'
              524  LOAD_FAST                'fromFlag'
          526_528  POP_JUMP_IF_TRUE    566  'to 566'
              530  LOAD_FAST                'wordPrev'
              532  LOAD_STR                 'om'
              534  COMPARE_OP               !=
          536_538  POP_JUMP_IF_FALSE   566  'to 566'

 L. 259       540  LOAD_FAST                'wordPrev'
              542  LOAD_FAST                'days'
              544  COMPARE_OP               not-in
          546_548  POP_JUMP_IF_FALSE   566  'to 566'

 L. 261       550  LOAD_CONST               1
              552  STORE_DEREF              'dayOffset'

 L. 262       554  LOAD_FAST                'used'
              556  LOAD_CONST               1
              558  INPLACE_ADD      
              560  STORE_FAST               'used'
          562_564  JUMP_FORWARD       1598  'to 1598'
            566_0  COME_FROM           546  '546'
            566_1  COME_FROM           536  '536'
            566_2  COME_FROM           526  '526'
            566_3  COME_FROM           520  '520'

 L. 263       566  LOAD_FAST                'word'
              568  LOAD_STR                 'overmorgen'
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   598  'to 598'
              576  LOAD_FAST                'fromFlag'
          578_580  POP_JUMP_IF_TRUE    598  'to 598'

 L. 264       582  LOAD_CONST               2
              584  STORE_DEREF              'dayOffset'

 L. 265       586  LOAD_FAST                'used'
              588  LOAD_CONST               1
              590  INPLACE_ADD      
              592  STORE_FAST               'used'
          594_596  JUMP_FORWARD       1598  'to 1598'
            598_0  COME_FROM           578  '578'
            598_1  COME_FROM           572  '572'

 L. 267       598  LOAD_FAST                'word'
              600  LOAD_STR                 'dag'
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_TRUE    618  'to 618'
              608  LOAD_FAST                'word'
              610  LOAD_STR                 'dage'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   660  'to 660'
            618_0  COME_FROM           604  '604'

 L. 268       618  LOAD_FAST                'wordPrev'
              620  LOAD_CONST               0
              622  BINARY_SUBSCR    
              624  LOAD_METHOD              isdigit
              626  CALL_METHOD_0         0  '0 positional arguments'
          628_630  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 269       632  LOAD_DEREF               'dayOffset'
              634  LOAD_GLOBAL              int
              636  LOAD_FAST                'wordPrev'
              638  CALL_FUNCTION_1       1  '1 positional argument'
              640  INPLACE_ADD      
              642  STORE_DEREF              'dayOffset'

 L. 270       644  LOAD_FAST                'start'
              646  LOAD_CONST               1
              648  INPLACE_SUBTRACT 
              650  STORE_FAST               'start'

 L. 271       652  LOAD_CONST               2
              654  STORE_FAST               'used'
          656_658  JUMP_FORWARD       1598  'to 1598'
            660_0  COME_FROM           614  '614'

 L. 272       660  LOAD_FAST                'word'
              662  LOAD_STR                 'uge'
              664  COMPARE_OP               ==
          666_668  POP_JUMP_IF_TRUE    686  'to 686'
              670  LOAD_FAST                'word'
              672  LOAD_STR                 'uger'
              674  COMPARE_OP               ==
          676_678  POP_JUMP_IF_FALSE   804  'to 804'
              680  LOAD_FAST                'fromFlag'
          682_684  POP_JUMP_IF_TRUE    804  'to 804'
            686_0  COME_FROM           666  '666'

 L. 273       686  LOAD_FAST                'wordPrev'
              688  LOAD_CONST               0
              690  BINARY_SUBSCR    
              692  LOAD_METHOD              isdigit
              694  CALL_METHOD_0         0  '0 positional arguments'
          696_698  POP_JUMP_IF_FALSE   730  'to 730'

 L. 274       700  LOAD_DEREF               'dayOffset'
              702  LOAD_GLOBAL              int
              704  LOAD_FAST                'wordPrev'
              706  CALL_FUNCTION_1       1  '1 positional argument'
              708  LOAD_CONST               7
              710  BINARY_MULTIPLY  
              712  INPLACE_ADD      
              714  STORE_DEREF              'dayOffset'

 L. 275       716  LOAD_FAST                'start'
              718  LOAD_CONST               1
              720  INPLACE_SUBTRACT 
              722  STORE_FAST               'start'

 L. 276       724  LOAD_CONST               2
              726  STORE_FAST               'used'
              728  JUMP_FORWARD       1598  'to 1598'
            730_0  COME_FROM           696  '696'

 L. 277       730  LOAD_FAST                'wordPrev'
              732  LOAD_CONST               None
              734  LOAD_CONST               6
              736  BUILD_SLICE_2         2 
              738  BINARY_SUBSCR    
              740  LOAD_STR                 'næste'
              742  COMPARE_OP               ==
          744_746  POP_JUMP_IF_FALSE   766  'to 766'

 L. 278       748  LOAD_CONST               7
              750  STORE_DEREF              'dayOffset'

 L. 279       752  LOAD_FAST                'start'
              754  LOAD_CONST               1
              756  INPLACE_SUBTRACT 
              758  STORE_FAST               'start'

 L. 280       760  LOAD_CONST               2
              762  STORE_FAST               'used'
              764  JUMP_FORWARD       1598  'to 1598'
            766_0  COME_FROM           744  '744'

 L. 281       766  LOAD_FAST                'wordPrev'
              768  LOAD_CONST               None
              770  LOAD_CONST               5
              772  BUILD_SLICE_2         2 
              774  BINARY_SUBSCR    
              776  LOAD_STR                 'forige'
              778  COMPARE_OP               ==
          780_782  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 282       784  LOAD_CONST               -7
              786  STORE_DEREF              'dayOffset'

 L. 283       788  LOAD_FAST                'start'
              790  LOAD_CONST               1
              792  INPLACE_SUBTRACT 
              794  STORE_FAST               'start'

 L. 284       796  LOAD_CONST               2
              798  STORE_FAST               'used'
          800_802  JUMP_FORWARD       1598  'to 1598'
            804_0  COME_FROM           682  '682'
            804_1  COME_FROM           676  '676'

 L. 286       804  LOAD_FAST                'word'
              806  LOAD_STR                 'måned'
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   930  'to 930'
              814  LOAD_FAST                'fromFlag'
          816_818  POP_JUMP_IF_TRUE    930  'to 930'

 L. 287       820  LOAD_FAST                'wordPrev'
              822  LOAD_CONST               0
              824  BINARY_SUBSCR    
              826  LOAD_METHOD              isdigit
              828  CALL_METHOD_0         0  '0 positional arguments'
          830_832  POP_JUMP_IF_FALSE   856  'to 856'

 L. 288       834  LOAD_GLOBAL              int
              836  LOAD_FAST                'wordPrev'
              838  CALL_FUNCTION_1       1  '1 positional argument'
              840  STORE_DEREF              'monthOffset'

 L. 289       842  LOAD_FAST                'start'
              844  LOAD_CONST               1
              846  INPLACE_SUBTRACT 
              848  STORE_FAST               'start'

 L. 290       850  LOAD_CONST               2
              852  STORE_FAST               'used'
              854  JUMP_FORWARD       1598  'to 1598'
            856_0  COME_FROM           830  '830'

 L. 291       856  LOAD_FAST                'wordPrev'
              858  LOAD_CONST               None
              860  LOAD_CONST               6
              862  BUILD_SLICE_2         2 
              864  BINARY_SUBSCR    
              866  LOAD_STR                 'næste'
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   892  'to 892'

 L. 292       874  LOAD_CONST               1
              876  STORE_DEREF              'monthOffset'

 L. 293       878  LOAD_FAST                'start'
              880  LOAD_CONST               1
              882  INPLACE_SUBTRACT 
              884  STORE_FAST               'start'

 L. 294       886  LOAD_CONST               2
              888  STORE_FAST               'used'
              890  JUMP_FORWARD       1598  'to 1598'
            892_0  COME_FROM           870  '870'

 L. 295       892  LOAD_FAST                'wordPrev'
              894  LOAD_CONST               None
              896  LOAD_CONST               5
              898  BUILD_SLICE_2         2 
              900  BINARY_SUBSCR    
              902  LOAD_STR                 'forige'
              904  COMPARE_OP               ==
          906_908  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 296       910  LOAD_CONST               -1
              912  STORE_DEREF              'monthOffset'

 L. 297       914  LOAD_FAST                'start'
              916  LOAD_CONST               1
              918  INPLACE_SUBTRACT 
              920  STORE_FAST               'start'

 L. 298       922  LOAD_CONST               2
              924  STORE_FAST               'used'
          926_928  JUMP_FORWARD       1598  'to 1598'
            930_0  COME_FROM           816  '816'
            930_1  COME_FROM           810  '810'

 L. 300       930  LOAD_FAST                'word'
              932  LOAD_STR                 'år'
              934  COMPARE_OP               ==
          936_938  POP_JUMP_IF_FALSE  1056  'to 1056'
              940  LOAD_FAST                'fromFlag'
          942_944  POP_JUMP_IF_TRUE   1056  'to 1056'

 L. 301       946  LOAD_FAST                'wordPrev'
              948  LOAD_CONST               0
              950  BINARY_SUBSCR    
              952  LOAD_METHOD              isdigit
              954  CALL_METHOD_0         0  '0 positional arguments'
          956_958  POP_JUMP_IF_FALSE   982  'to 982'

 L. 302       960  LOAD_GLOBAL              int
              962  LOAD_FAST                'wordPrev'
              964  CALL_FUNCTION_1       1  '1 positional argument'
              966  STORE_DEREF              'yearOffset'

 L. 303       968  LOAD_FAST                'start'
              970  LOAD_CONST               1
              972  INPLACE_SUBTRACT 
              974  STORE_FAST               'start'

 L. 304       976  LOAD_CONST               2
              978  STORE_FAST               'used'
              980  JUMP_FORWARD       1598  'to 1598'
            982_0  COME_FROM           956  '956'

 L. 305       982  LOAD_FAST                'wordPrev'
              984  LOAD_CONST               None
              986  LOAD_CONST               6
              988  BUILD_SLICE_2         2 
              990  BINARY_SUBSCR    
              992  LOAD_STR                 ' næste'
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 306      1000  LOAD_CONST               1
             1002  STORE_DEREF              'yearOffset'

 L. 307      1004  LOAD_FAST                'start'
             1006  LOAD_CONST               1
             1008  INPLACE_SUBTRACT 
             1010  STORE_FAST               'start'

 L. 308      1012  LOAD_CONST               2
             1014  STORE_FAST               'used'
             1016  JUMP_FORWARD       1598  'to 1598'
           1018_0  COME_FROM           996  '996'

 L. 309      1018  LOAD_FAST                'wordPrev'
             1020  LOAD_CONST               None
             1022  LOAD_CONST               6
             1024  BUILD_SLICE_2         2 
             1026  BINARY_SUBSCR    
             1028  LOAD_STR                 'næste'
             1030  COMPARE_OP               ==
         1032_1034  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 310      1036  LOAD_CONST               -1
             1038  STORE_DEREF              'yearOffset'

 L. 311      1040  LOAD_FAST                'start'
             1042  LOAD_CONST               1
             1044  INPLACE_SUBTRACT 
             1046  STORE_FAST               'start'

 L. 312      1048  LOAD_CONST               2
             1050  STORE_FAST               'used'
         1052_1054  JUMP_FORWARD       1598  'to 1598'
           1056_0  COME_FROM           942  '942'
           1056_1  COME_FROM           936  '936'

 L. 315      1056  LOAD_FAST                'word'
             1058  LOAD_FAST                'days'
             1060  COMPARE_OP               in
         1062_1064  POP_JUMP_IF_FALSE  1232  'to 1232'
             1066  LOAD_FAST                'fromFlag'
         1068_1070  POP_JUMP_IF_TRUE   1232  'to 1232'

 L. 316      1072  LOAD_FAST                'days'
             1074  LOAD_METHOD              index
             1076  LOAD_FAST                'word'
             1078  CALL_METHOD_1         1  '1 positional argument'
             1080  STORE_FAST               'd'

 L. 317      1082  LOAD_FAST                'd'
             1084  LOAD_CONST               1
             1086  BINARY_ADD       
             1088  LOAD_GLOBAL              int
             1090  LOAD_FAST                'today'
             1092  CALL_FUNCTION_1       1  '1 positional argument'
             1094  BINARY_SUBTRACT  
             1096  STORE_DEREF              'dayOffset'

 L. 318      1098  LOAD_CONST               1
             1100  STORE_FAST               'used'

 L. 319      1102  LOAD_DEREF               'dayOffset'
             1104  LOAD_CONST               0
             1106  COMPARE_OP               <
         1108_1110  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 320      1112  LOAD_DEREF               'dayOffset'
             1114  LOAD_CONST               7
             1116  INPLACE_ADD      
             1118  STORE_DEREF              'dayOffset'
           1120_0  COME_FROM          1108  '1108'

 L. 321      1120  LOAD_FAST                'wordNext'
             1122  LOAD_STR                 'morgen'
             1124  COMPARE_OP               ==
         1126_1128  POP_JUMP_IF_FALSE  1142  'to 1142'

 L. 324      1130  LOAD_STR                 'tidlig'
             1132  LOAD_FAST                'words'
             1134  LOAD_FAST                'idx'
             1136  LOAD_CONST               1
             1138  BINARY_ADD       
             1140  STORE_SUBSCR     
           1142_0  COME_FROM          1126  '1126'

 L. 325      1142  LOAD_FAST                'wordPrev'
             1144  LOAD_CONST               None
             1146  LOAD_CONST               6
             1148  BUILD_SLICE_2         2 
             1150  BINARY_SUBSCR    
             1152  LOAD_STR                 'næste'
             1154  COMPARE_OP               ==
         1156_1158  POP_JUMP_IF_FALSE  1186  'to 1186'

 L. 326      1160  LOAD_DEREF               'dayOffset'
             1162  LOAD_CONST               7
             1164  INPLACE_ADD      
             1166  STORE_DEREF              'dayOffset'

 L. 327      1168  LOAD_FAST                'used'
             1170  LOAD_CONST               1
             1172  INPLACE_ADD      
             1174  STORE_FAST               'used'

 L. 328      1176  LOAD_FAST                'start'
             1178  LOAD_CONST               1
             1180  INPLACE_SUBTRACT 
             1182  STORE_FAST               'start'
             1184  JUMP_FORWARD       1598  'to 1598'
           1186_0  COME_FROM          1156  '1156'

 L. 329      1186  LOAD_FAST                'wordPrev'
             1188  LOAD_CONST               None
             1190  LOAD_CONST               5
             1192  BUILD_SLICE_2         2 
             1194  BINARY_SUBSCR    
             1196  LOAD_STR                 'forige'
             1198  COMPARE_OP               ==
         1200_1202  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 330      1204  LOAD_DEREF               'dayOffset'
             1206  LOAD_CONST               7
             1208  INPLACE_SUBTRACT 
             1210  STORE_DEREF              'dayOffset'

 L. 331      1212  LOAD_FAST                'used'
             1214  LOAD_CONST               1
             1216  INPLACE_ADD      
             1218  STORE_FAST               'used'

 L. 332      1220  LOAD_FAST                'start'
             1222  LOAD_CONST               1
             1224  INPLACE_SUBTRACT 
             1226  STORE_FAST               'start'
         1228_1230  JUMP_FORWARD       1598  'to 1598'
           1232_0  COME_FROM          1068  '1068'
           1232_1  COME_FROM          1062  '1062'

 L. 334      1232  LOAD_FAST                'word'
             1234  LOAD_FAST                'months'
             1236  COMPARE_OP               in
         1238_1240  POP_JUMP_IF_TRUE   1258  'to 1258'
             1242  LOAD_FAST                'word'
             1244  LOAD_FAST                'monthsShort'
             1246  COMPARE_OP               in
         1248_1250  POP_JUMP_IF_FALSE  1598  'to 1598'
             1252  LOAD_FAST                'fromFlag'
         1254_1256  POP_JUMP_IF_TRUE   1598  'to 1598'
           1258_0  COME_FROM          1238  '1238'

 L. 335      1258  SETUP_EXCEPT       1274  'to 1274'

 L. 336      1260  LOAD_FAST                'months'
             1262  LOAD_METHOD              index
             1264  LOAD_FAST                'word'
             1266  CALL_METHOD_1         1  '1 positional argument'
             1268  STORE_FAST               'm'
             1270  POP_BLOCK        
             1272  JUMP_FORWARD       1306  'to 1306'
           1274_0  COME_FROM_EXCEPT   1258  '1258'

 L. 337      1274  DUP_TOP          
             1276  LOAD_GLOBAL              ValueError
             1278  COMPARE_OP               exception-match
         1280_1282  POP_JUMP_IF_FALSE  1304  'to 1304'
             1284  POP_TOP          
             1286  POP_TOP          
             1288  POP_TOP          

 L. 338      1290  LOAD_FAST                'monthsShort'
             1292  LOAD_METHOD              index
             1294  LOAD_FAST                'word'
             1296  CALL_METHOD_1         1  '1 positional argument'
             1298  STORE_FAST               'm'
             1300  POP_EXCEPT       
             1302  JUMP_FORWARD       1306  'to 1306'
           1304_0  COME_FROM          1280  '1280'
             1304  END_FINALLY      
           1306_0  COME_FROM          1302  '1302'
           1306_1  COME_FROM          1272  '1272'

 L. 339      1306  LOAD_FAST                'used'
             1308  LOAD_CONST               1
             1310  INPLACE_ADD      
             1312  STORE_FAST               'used'

 L. 340      1314  LOAD_FAST                'months'
             1316  LOAD_FAST                'm'
             1318  BINARY_SUBSCR    
             1320  STORE_DEREF              'datestr'

 L. 341      1322  LOAD_FAST                'wordPrev'
         1324_1326  POP_JUMP_IF_FALSE  1508  'to 1508'
             1328  LOAD_FAST                'wordPrev'
             1330  LOAD_CONST               0
             1332  BINARY_SUBSCR    
             1334  LOAD_METHOD              isdigit
             1336  CALL_METHOD_0         0  '0 positional arguments'
         1338_1340  POP_JUMP_IF_TRUE   1366  'to 1366'

 L. 342      1342  LOAD_FAST                'wordPrev'
             1344  LOAD_STR                 'of'
             1346  COMPARE_OP               ==
         1348_1350  POP_JUMP_IF_FALSE  1508  'to 1508'
             1352  LOAD_FAST                'wordPrevPrev'
             1354  LOAD_CONST               0
             1356  BINARY_SUBSCR    
             1358  LOAD_METHOD              isdigit
             1360  CALL_METHOD_0         0  '0 positional arguments'
         1362_1364  POP_JUMP_IF_FALSE  1508  'to 1508'
           1366_0  COME_FROM          1338  '1338'

 L. 343      1366  LOAD_FAST                'wordPrev'
             1368  LOAD_STR                 'of'
             1370  COMPARE_OP               ==
         1372_1374  POP_JUMP_IF_FALSE  1428  'to 1428'
             1376  LOAD_FAST                'wordPrevPrev'
             1378  LOAD_CONST               0
             1380  BINARY_SUBSCR    
             1382  LOAD_METHOD              isdigit
             1384  CALL_METHOD_0         0  '0 positional arguments'
         1386_1388  POP_JUMP_IF_FALSE  1428  'to 1428'

 L. 344      1390  LOAD_DEREF               'datestr'
             1392  LOAD_STR                 ' '
             1394  LOAD_FAST                'words'
             1396  LOAD_FAST                'idx'
             1398  LOAD_CONST               2
             1400  BINARY_SUBTRACT  
             1402  BINARY_SUBSCR    
             1404  BINARY_ADD       
             1406  INPLACE_ADD      
             1408  STORE_DEREF              'datestr'

 L. 345      1410  LOAD_FAST                'used'
             1412  LOAD_CONST               1
             1414  INPLACE_ADD      
             1416  STORE_FAST               'used'

 L. 346      1418  LOAD_FAST                'start'
             1420  LOAD_CONST               1
             1422  INPLACE_SUBTRACT 
             1424  STORE_FAST               'start'
             1426  JUMP_FORWARD       1440  'to 1440'
           1428_0  COME_FROM          1386  '1386'
           1428_1  COME_FROM          1372  '1372'

 L. 348      1428  LOAD_DEREF               'datestr'
             1430  LOAD_STR                 ' '
             1432  LOAD_FAST                'wordPrev'
             1434  BINARY_ADD       
             1436  INPLACE_ADD      
             1438  STORE_DEREF              'datestr'
           1440_0  COME_FROM          1426  '1426'

 L. 349      1440  LOAD_FAST                'start'
             1442  LOAD_CONST               1
             1444  INPLACE_SUBTRACT 
             1446  STORE_FAST               'start'

 L. 350      1448  LOAD_FAST                'used'
             1450  LOAD_CONST               1
             1452  INPLACE_ADD      
             1454  STORE_FAST               'used'

 L. 351      1456  LOAD_FAST                'wordNext'
         1458_1460  POP_JUMP_IF_FALSE  1502  'to 1502'
             1462  LOAD_FAST                'wordNext'
             1464  LOAD_CONST               0
             1466  BINARY_SUBSCR    
             1468  LOAD_METHOD              isdigit
             1470  CALL_METHOD_0         0  '0 positional arguments'
         1472_1474  POP_JUMP_IF_FALSE  1502  'to 1502'

 L. 352      1476  LOAD_DEREF               'datestr'
             1478  LOAD_STR                 ' '
             1480  LOAD_FAST                'wordNext'
             1482  BINARY_ADD       
             1484  INPLACE_ADD      
             1486  STORE_DEREF              'datestr'

 L. 353      1488  LOAD_FAST                'used'
             1490  LOAD_CONST               1
             1492  INPLACE_ADD      
             1494  STORE_FAST               'used'

 L. 354      1496  LOAD_CONST               True
             1498  STORE_FAST               'hasYear'
             1500  JUMP_FORWARD       1506  'to 1506'
           1502_0  COME_FROM          1472  '1472'
           1502_1  COME_FROM          1458  '1458'

 L. 356      1502  LOAD_CONST               False
             1504  STORE_FAST               'hasYear'
           1506_0  COME_FROM          1500  '1500'
             1506  JUMP_FORWARD       1598  'to 1598'
           1508_0  COME_FROM          1362  '1362'
           1508_1  COME_FROM          1348  '1348'
           1508_2  COME_FROM          1324  '1324'

 L. 358      1508  LOAD_FAST                'wordNext'
         1510_1512  POP_JUMP_IF_FALSE  1598  'to 1598'
             1514  LOAD_FAST                'wordNext'
             1516  LOAD_CONST               0
             1518  BINARY_SUBSCR    
             1520  LOAD_METHOD              isdigit
             1522  CALL_METHOD_0         0  '0 positional arguments'
           1524_0  COME_FROM           980  '980'
           1524_1  COME_FROM           854  '854'
           1524_2  COME_FROM           728  '728'
         1524_1526  POP_JUMP_IF_FALSE  1598  'to 1598'

 L. 359      1528  LOAD_DEREF               'datestr'
             1530  LOAD_STR                 ' '
             1532  LOAD_FAST                'wordNext'
             1534  BINARY_ADD       
             1536  INPLACE_ADD      
             1538  STORE_DEREF              'datestr'

 L. 360      1540  LOAD_FAST                'used'
             1542  LOAD_CONST               1
             1544  INPLACE_ADD      
             1546  STORE_FAST               'used'

 L. 361      1548  LOAD_FAST                'wordNextNext'
         1550_1552  POP_JUMP_IF_FALSE  1594  'to 1594'
             1554  LOAD_FAST                'wordNextNext'
             1556  LOAD_CONST               0
             1558  BINARY_SUBSCR    
           1560_0  COME_FROM          1016  '1016'
           1560_1  COME_FROM           890  '890'
           1560_2  COME_FROM           764  '764'
             1560  LOAD_METHOD              isdigit
             1562  CALL_METHOD_0         0  '0 positional arguments'
         1564_1566  POP_JUMP_IF_FALSE  1594  'to 1594'

 L. 362      1568  LOAD_DEREF               'datestr'
             1570  LOAD_STR                 ' '
             1572  LOAD_FAST                'wordNextNext'
             1574  BINARY_ADD       
             1576  INPLACE_ADD      
             1578  STORE_DEREF              'datestr'

 L. 363      1580  LOAD_FAST                'used'
             1582  LOAD_CONST               1
             1584  INPLACE_ADD      
             1586  STORE_FAST               'used'

 L. 364      1588  LOAD_CONST               True
             1590  STORE_FAST               'hasYear'
             1592  JUMP_FORWARD       1598  'to 1598'
           1594_0  COME_FROM          1564  '1564'
           1594_1  COME_FROM          1550  '1550'

 L. 366      1594  LOAD_CONST               False
             1596  STORE_FAST               'hasYear'
           1598_0  COME_FROM          1592  '1592'
           1598_1  COME_FROM          1524  '1524'
           1598_2  COME_FROM          1510  '1510'
           1598_3  COME_FROM          1506  '1506'
           1598_4  COME_FROM          1254  '1254'
           1598_5  COME_FROM          1248  '1248'
           1598_6  COME_FROM          1228  '1228'
           1598_7  COME_FROM          1200  '1200'
           1598_8  COME_FROM          1052  '1052'
           1598_9  COME_FROM          1032  '1032'
          1598_10  COME_FROM           926  '926'
          1598_11  COME_FROM           906  '906'
          1598_12  COME_FROM           800  '800'
          1598_13  COME_FROM           780  '780'
          1598_14  COME_FROM           656  '656'
          1598_15  COME_FROM           628  '628'
          1598_16  COME_FROM           594  '594'
          1598_17  COME_FROM           562  '562'
          1598_18  COME_FROM           510  '510'
          1598_19  COME_FROM           478  '478'

 L. 371      1598  LOAD_FAST                'word'
             1600  LOAD_STR                 'fra'
             1602  COMPARE_OP               ==
         1604_1606  POP_JUMP_IF_TRUE   1628  'to 1628'
             1608  LOAD_FAST                'word'
             1610  LOAD_STR                 'til'
             1612  COMPARE_OP               ==
         1614_1616  POP_JUMP_IF_TRUE   1628  'to 1628'
             1618  LOAD_FAST                'word'
             1620  LOAD_STR                 'om'
             1622  COMPARE_OP               ==
         1624_1626  POP_JUMP_IF_FALSE  1894  'to 1894'
           1628_0  COME_FROM          1614  '1614'
           1628_1  COME_FROM          1604  '1604'
             1628  LOAD_FAST                'wordNext'

 L. 372      1630  LOAD_FAST                'validFollowups'
             1632  COMPARE_OP               in
         1634_1636  POP_JUMP_IF_FALSE  1894  'to 1894'

 L. 373      1638  LOAD_CONST               2
             1640  STORE_FAST               'used'

 L. 374      1642  LOAD_CONST               True
             1644  STORE_FAST               'fromFlag'

 L. 375      1646  LOAD_FAST                'wordNext'
             1648  LOAD_STR                 'morgenen'
             1650  COMPARE_OP               ==
         1652_1654  POP_JUMP_IF_FALSE  1686  'to 1686'

 L. 376      1656  LOAD_FAST                'wordPrev'
             1658  LOAD_STR                 'om'
             1660  COMPARE_OP               !=
         1662_1664  POP_JUMP_IF_FALSE  1686  'to 1686'

 L. 377      1666  LOAD_FAST                'wordPrev'
             1668  LOAD_FAST                'days'
             1670  COMPARE_OP               not-in
         1672_1674  POP_JUMP_IF_FALSE  1686  'to 1686'

 L. 380      1676  LOAD_DEREF               'dayOffset'
             1678  LOAD_CONST               1
             1680  INPLACE_ADD      
             1682  STORE_DEREF              'dayOffset'
             1684  JUMP_FORWARD       1894  'to 1894'
           1686_0  COME_FROM          1672  '1672'
           1686_1  COME_FROM          1662  '1662'
           1686_2  COME_FROM          1652  '1652'

 L. 381      1686  LOAD_FAST                'wordNext'
             1688  LOAD_FAST                'days'
             1690  COMPARE_OP               in
         1692_1694  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 382      1696  LOAD_FAST                'days'
             1698  LOAD_METHOD              index
             1700  LOAD_FAST                'wordNext'
             1702  CALL_METHOD_1         1  '1 positional argument'
             1704  STORE_FAST               'd'

 L. 383      1706  LOAD_FAST                'd'
             1708  LOAD_CONST               1
             1710  BINARY_ADD       
             1712  LOAD_GLOBAL              int
             1714  LOAD_FAST                'today'
             1716  CALL_FUNCTION_1       1  '1 positional argument'
             1718  BINARY_SUBTRACT  
             1720  STORE_FAST               'tmpOffset'

 L. 384      1722  LOAD_CONST               2
             1724  STORE_FAST               'used'

 L. 385      1726  LOAD_FAST                'tmpOffset'
             1728  LOAD_CONST               0
             1730  COMPARE_OP               <
         1732_1734  POP_JUMP_IF_FALSE  1744  'to 1744'

 L. 386      1736  LOAD_FAST                'tmpOffset'
             1738  LOAD_CONST               7
             1740  INPLACE_ADD      
             1742  STORE_FAST               'tmpOffset'
           1744_0  COME_FROM          1732  '1732'

 L. 387      1744  LOAD_DEREF               'dayOffset'
             1746  LOAD_FAST                'tmpOffset'
             1748  INPLACE_ADD      
             1750  STORE_DEREF              'dayOffset'
             1752  JUMP_FORWARD       1894  'to 1894'
           1754_0  COME_FROM          1692  '1692'

 L. 388      1754  LOAD_FAST                'wordNextNext'
         1756_1758  POP_JUMP_IF_FALSE  1894  'to 1894'
             1760  LOAD_FAST                'wordNextNext'
             1762  LOAD_FAST                'days'
             1764  COMPARE_OP               in
         1766_1768  POP_JUMP_IF_FALSE  1894  'to 1894'

 L. 389      1770  LOAD_FAST                'days'
             1772  LOAD_METHOD              index
             1774  LOAD_FAST                'wordNextNext'
             1776  CALL_METHOD_1         1  '1 positional argument'
             1778  STORE_FAST               'd'

 L. 390      1780  LOAD_FAST                'd'
             1782  LOAD_CONST               1
             1784  BINARY_ADD       
             1786  LOAD_GLOBAL              int
             1788  LOAD_FAST                'today'
             1790  CALL_FUNCTION_1       1  '1 positional argument'
             1792  BINARY_SUBTRACT  
             1794  STORE_FAST               'tmpOffset'

 L. 391      1796  LOAD_CONST               3
             1798  STORE_FAST               'used'

 L. 392      1800  LOAD_FAST                'wordNext'
             1802  LOAD_CONST               None
             1804  LOAD_CONST               6
             1806  BUILD_SLICE_2         2 
             1808  BINARY_SUBSCR    
             1810  LOAD_STR                 'næste'
             1812  COMPARE_OP               ==
         1814_1816  POP_JUMP_IF_FALSE  1844  'to 1844'

 L. 393      1818  LOAD_FAST                'tmpOffset'
             1820  LOAD_CONST               7
             1822  INPLACE_ADD      
             1824  STORE_FAST               'tmpOffset'

 L. 394      1826  LOAD_FAST                'used'
             1828  LOAD_CONST               1
             1830  INPLACE_ADD      
             1832  STORE_FAST               'used'

 L. 395      1834  LOAD_FAST                'start'
             1836  LOAD_CONST               1
             1838  INPLACE_SUBTRACT 
             1840  STORE_FAST               'start'
             1842  JUMP_FORWARD       1886  'to 1886'
           1844_0  COME_FROM          1814  '1814'

 L. 396      1844  LOAD_FAST                'wordNext'
             1846  LOAD_CONST               None
             1848  LOAD_CONST               5
             1850  BUILD_SLICE_2         2 
             1852  BINARY_SUBSCR    
             1854  LOAD_STR                 'forige'
             1856  COMPARE_OP               ==
         1858_1860  POP_JUMP_IF_FALSE  1886  'to 1886'

 L. 397      1862  LOAD_FAST                'tmpOffset'
             1864  LOAD_CONST               7
             1866  INPLACE_SUBTRACT 
             1868  STORE_FAST               'tmpOffset'

 L. 398      1870  LOAD_FAST                'used'
             1872  LOAD_CONST               1
             1874  INPLACE_ADD      
             1876  STORE_FAST               'used'

 L. 399      1878  LOAD_FAST                'start'
             1880  LOAD_CONST               1
             1882  INPLACE_SUBTRACT 
             1884  STORE_FAST               'start'
           1886_0  COME_FROM          1858  '1858'
           1886_1  COME_FROM          1842  '1842'

 L. 400      1886  LOAD_DEREF               'dayOffset'
             1888  LOAD_FAST                'tmpOffset'
             1890  INPLACE_ADD      
             1892  STORE_DEREF              'dayOffset'
           1894_0  COME_FROM          1766  '1766'
           1894_1  COME_FROM          1756  '1756'
           1894_2  COME_FROM          1752  '1752'
           1894_3  COME_FROM          1684  '1684'
           1894_4  COME_FROM          1634  '1634'
           1894_5  COME_FROM          1624  '1624'

 L. 401      1894  LOAD_FAST                'used'
             1896  LOAD_CONST               0
             1898  COMPARE_OP               >
         1900_1902  POP_JUMP_IF_FALSE   312  'to 312'

 L. 402      1904  LOAD_FAST                'start'
             1906  LOAD_CONST               1
             1908  BINARY_SUBTRACT  
             1910  LOAD_CONST               0
             1912  COMPARE_OP               >
         1914_1916  POP_JUMP_IF_FALSE  1954  'to 1954'
             1918  LOAD_FAST                'words'
             1920  LOAD_FAST                'start'
             1922  LOAD_CONST               1
             1924  BINARY_SUBTRACT  
             1926  BINARY_SUBSCR    
             1928  LOAD_METHOD              startswith
             1930  LOAD_STR                 'denne'
             1932  CALL_METHOD_1         1  '1 positional argument'
         1934_1936  POP_JUMP_IF_FALSE  1954  'to 1954'

 L. 403      1938  LOAD_FAST                'start'
             1940  LOAD_CONST               1
             1942  INPLACE_SUBTRACT 
             1944  STORE_FAST               'start'

 L. 404      1946  LOAD_FAST                'used'
             1948  LOAD_CONST               1
             1950  INPLACE_ADD      
             1952  STORE_FAST               'used'
           1954_0  COME_FROM          1934  '1934'
           1954_1  COME_FROM          1914  '1914'

 L. 406      1954  SETUP_LOOP         1988  'to 1988'
             1956  LOAD_GLOBAL              range
             1958  LOAD_CONST               0
             1960  LOAD_FAST                'used'
             1962  CALL_FUNCTION_2       2  '2 positional arguments'
             1964  GET_ITER         
             1966  FOR_ITER           1986  'to 1986'
             1968  STORE_FAST               'i'

 L. 407      1970  LOAD_STR                 ''
             1972  LOAD_FAST                'words'
             1974  LOAD_FAST                'i'
             1976  LOAD_FAST                'start'
             1978  BINARY_ADD       
             1980  STORE_SUBSCR     
         1982_1984  JUMP_BACK          1966  'to 1966'
             1986  POP_BLOCK        
           1988_0  COME_FROM_LOOP     1954  '1954'

 L. 409      1988  LOAD_FAST                'start'
             1990  LOAD_CONST               1
             1992  BINARY_SUBTRACT  
             1994  LOAD_CONST               0
             1996  COMPARE_OP               >=
         1998_2000  POP_JUMP_IF_FALSE  2032  'to 2032'
             2002  LOAD_FAST                'words'
             2004  LOAD_FAST                'start'
             2006  LOAD_CONST               1
             2008  BINARY_SUBTRACT  
             2010  BINARY_SUBSCR    
             2012  LOAD_FAST                'markers'
             2014  COMPARE_OP               in
         2016_2018  POP_JUMP_IF_FALSE  2032  'to 2032'

 L. 410      2020  LOAD_STR                 ''
             2022  LOAD_FAST                'words'
             2024  LOAD_FAST                'start'
             2026  LOAD_CONST               1
             2028  BINARY_SUBTRACT  
             2030  STORE_SUBSCR     
           2032_0  COME_FROM          2016  '2016'
           2032_1  COME_FROM          1998  '1998'

 L. 411      2032  LOAD_CONST               True
             2034  STORE_DEREF              'found'

 L. 412      2036  LOAD_CONST               True
             2038  STORE_FAST               'daySpecified'
         2040_2042  JUMP_BACK           312  'to 312'
             2044  POP_BLOCK        
           2046_0  COME_FROM_LOOP      300  '300'

 L. 415      2046  LOAD_STR                 ''
             2048  STORE_DEREF              'timeStr'

 L. 416      2050  LOAD_CONST               0
             2052  STORE_DEREF              'hrOffset'

 L. 417      2054  LOAD_CONST               0
             2056  STORE_DEREF              'minOffset'

 L. 418      2058  LOAD_CONST               0
             2060  STORE_DEREF              'secOffset'

 L. 419      2062  LOAD_CONST               None
             2064  STORE_DEREF              'hrAbs'

 L. 420      2066  LOAD_CONST               None
             2068  STORE_DEREF              'minAbs'

 L. 422  2070_2072  SETUP_LOOP         4902  'to 4902'
             2074  LOAD_GLOBAL              enumerate
             2076  LOAD_FAST                'words'
             2078  CALL_FUNCTION_1       1  '1 positional argument'
             2080  GET_ITER         
           2082_0  COME_FROM          4710  '4710'
         2082_2084  FOR_ITER           4900  'to 4900'
             2086  UNPACK_SEQUENCE_2     2 
             2088  STORE_FAST               'idx'
             2090  STORE_FAST               'word'

 L. 423      2092  LOAD_FAST                'word'
             2094  LOAD_STR                 ''
             2096  COMPARE_OP               ==
         2098_2100  POP_JUMP_IF_FALSE  2106  'to 2106'

 L. 424  2102_2104  CONTINUE           2082  'to 2082'
           2106_0  COME_FROM          2098  '2098'

 L. 426      2106  LOAD_FAST                'idx'
             2108  LOAD_CONST               1
             2110  COMPARE_OP               >
         2112_2114  POP_JUMP_IF_FALSE  2128  'to 2128'
             2116  LOAD_FAST                'words'
             2118  LOAD_FAST                'idx'
             2120  LOAD_CONST               2
             2122  BINARY_SUBTRACT  
             2124  BINARY_SUBSCR    
             2126  JUMP_FORWARD       2130  'to 2130'
           2128_0  COME_FROM          2112  '2112'
             2128  LOAD_STR                 ''
           2130_0  COME_FROM          2126  '2126'
             2130  STORE_FAST               'wordPrevPrev'

 L. 427      2132  LOAD_FAST                'idx'
             2134  LOAD_CONST               0
             2136  COMPARE_OP               >
         2138_2140  POP_JUMP_IF_FALSE  2154  'to 2154'
             2142  LOAD_FAST                'words'
             2144  LOAD_FAST                'idx'
             2146  LOAD_CONST               1
             2148  BINARY_SUBTRACT  
             2150  BINARY_SUBSCR    
             2152  JUMP_FORWARD       2156  'to 2156'
           2154_0  COME_FROM          2138  '2138'
             2154  LOAD_STR                 ''
           2156_0  COME_FROM          2152  '2152'
             2156  STORE_FAST               'wordPrev'

 L. 428      2158  LOAD_FAST                'idx'
             2160  LOAD_CONST               1
             2162  BINARY_ADD       
             2164  LOAD_GLOBAL              len
             2166  LOAD_FAST                'words'
             2168  CALL_FUNCTION_1       1  '1 positional argument'
             2170  COMPARE_OP               <
         2172_2174  POP_JUMP_IF_FALSE  2188  'to 2188'
             2176  LOAD_FAST                'words'
             2178  LOAD_FAST                'idx'
             2180  LOAD_CONST               1
             2182  BINARY_ADD       
             2184  BINARY_SUBSCR    
             2186  JUMP_FORWARD       2190  'to 2190'
           2188_0  COME_FROM          2172  '2172'
             2188  LOAD_STR                 ''
           2190_0  COME_FROM          2186  '2186'
             2190  STORE_FAST               'wordNext'

 L. 429      2192  LOAD_FAST                'idx'
             2194  LOAD_CONST               2
             2196  BINARY_ADD       
             2198  LOAD_GLOBAL              len
             2200  LOAD_FAST                'words'
             2202  CALL_FUNCTION_1       1  '1 positional argument'
             2204  COMPARE_OP               <
         2206_2208  POP_JUMP_IF_FALSE  2222  'to 2222'
             2210  LOAD_FAST                'words'
             2212  LOAD_FAST                'idx'
             2214  LOAD_CONST               2
             2216  BINARY_ADD       
             2218  BINARY_SUBSCR    
             2220  JUMP_FORWARD       2224  'to 2224'
           2222_0  COME_FROM          2206  '2206'
             2222  LOAD_STR                 ''
           2224_0  COME_FROM          2220  '2220'
             2224  STORE_FAST               'wordNextNext'

 L. 430      2226  LOAD_FAST                'idx'
             2228  LOAD_CONST               3
             2230  BINARY_ADD       
             2232  LOAD_GLOBAL              len
             2234  LOAD_FAST                'words'
             2236  CALL_FUNCTION_1       1  '1 positional argument'
             2238  COMPARE_OP               <
         2240_2242  POP_JUMP_IF_FALSE  2256  'to 2256'
             2244  LOAD_FAST                'words'
             2246  LOAD_FAST                'idx'
             2248  LOAD_CONST               3
             2250  BINARY_ADD       
             2252  BINARY_SUBSCR    
             2254  JUMP_FORWARD       2258  'to 2258'
           2256_0  COME_FROM          2240  '2240'
             2256  LOAD_STR                 ''
           2258_0  COME_FROM          2254  '2254'
             2258  STORE_FAST               'wordNextNextNext'

 L. 431      2260  LOAD_FAST                'idx'
             2262  LOAD_CONST               4
             2264  BINARY_ADD       
             2266  LOAD_GLOBAL              len
             2268  LOAD_FAST                'words'
             2270  CALL_FUNCTION_1       1  '1 positional argument'
             2272  COMPARE_OP               <
         2274_2276  POP_JUMP_IF_FALSE  2290  'to 2290'
             2278  LOAD_FAST                'words'
             2280  LOAD_FAST                'idx'
             2282  LOAD_CONST               4
             2284  BINARY_ADD       
             2286  BINARY_SUBSCR    
             2288  JUMP_FORWARD       2292  'to 2292'
           2290_0  COME_FROM          2274  '2274'
             2290  LOAD_STR                 ''
           2292_0  COME_FROM          2288  '2288'
             2292  STORE_FAST               'wordNextNextNextNext'

 L. 434      2294  LOAD_CONST               0
             2296  STORE_FAST               'used'

 L. 435      2298  LOAD_FAST                'word'
             2300  LOAD_CONST               None
             2302  LOAD_CONST               6
             2304  BUILD_SLICE_2         2 
             2306  BINARY_SUBSCR    
             2308  LOAD_STR                 'middag'
             2310  COMPARE_OP               ==
         2312_2314  POP_JUMP_IF_FALSE  2332  'to 2332'

 L. 436      2316  LOAD_CONST               12
             2318  STORE_DEREF              'hrAbs'

 L. 437      2320  LOAD_FAST                'used'
             2322  LOAD_CONST               1
             2324  INPLACE_ADD      
             2326  STORE_FAST               'used'
         2328_2330  JUMP_FORWARD       4704  'to 4704'
           2332_0  COME_FROM          2312  '2312'

 L. 438      2332  LOAD_FAST                'word'
             2334  LOAD_CONST               None
             2336  LOAD_CONST               11
             2338  BUILD_SLICE_2         2 
             2340  BINARY_SUBSCR    
             2342  LOAD_STR                 'midnat'
             2344  COMPARE_OP               ==
         2346_2348  POP_JUMP_IF_FALSE  2366  'to 2366'

 L. 439      2350  LOAD_CONST               0
             2352  STORE_DEREF              'hrAbs'

 L. 440      2354  LOAD_FAST                'used'
             2356  LOAD_CONST               1
             2358  INPLACE_ADD      
             2360  STORE_FAST               'used'
         2362_2364  JUMP_FORWARD       4704  'to 4704'
           2366_0  COME_FROM          2346  '2346'

 L. 441      2366  LOAD_FAST                'word'
             2368  LOAD_STR                 'morgenen'
             2370  COMPARE_OP               ==
         2372_2374  POP_JUMP_IF_TRUE   2406  'to 2406'

 L. 442      2376  LOAD_FAST                'wordPrev'
             2378  LOAD_STR                 'om'
             2380  COMPARE_OP               ==
         2382_2384  POP_JUMP_IF_FALSE  2396  'to 2396'
             2386  LOAD_FAST                'word'
             2388  LOAD_STR                 'morgenen'
             2390  COMPARE_OP               ==
         2392_2394  POP_JUMP_IF_TRUE   2406  'to 2406'
           2396_0  COME_FROM          2382  '2382'
             2396  LOAD_FAST                'word'
             2398  LOAD_STR                 'tidlig'
             2400  COMPARE_OP               ==
         2402_2404  POP_JUMP_IF_FALSE  2428  'to 2428'
           2406_0  COME_FROM          2392  '2392'
           2406_1  COME_FROM          2372  '2372'

 L. 443      2406  LOAD_DEREF               'hrAbs'
         2408_2410  POP_JUMP_IF_TRUE   2416  'to 2416'

 L. 444      2412  LOAD_CONST               8
             2414  STORE_DEREF              'hrAbs'
           2416_0  COME_FROM          2408  '2408'

 L. 445      2416  LOAD_FAST                'used'
             2418  LOAD_CONST               1
             2420  INPLACE_ADD      
             2422  STORE_FAST               'used'
         2424_2426  JUMP_FORWARD       4704  'to 4704'
           2428_0  COME_FROM          2402  '2402'

 L. 446      2428  LOAD_FAST                'word'
             2430  LOAD_CONST               None
             2432  LOAD_CONST               11
             2434  BUILD_SLICE_2         2 
             2436  BINARY_SUBSCR    
             2438  LOAD_STR                 'eftermiddag'
             2440  COMPARE_OP               ==
         2442_2444  POP_JUMP_IF_FALSE  2468  'to 2468'

 L. 447      2446  LOAD_DEREF               'hrAbs'
         2448_2450  POP_JUMP_IF_TRUE   2456  'to 2456'

 L. 448      2452  LOAD_CONST               15
             2454  STORE_DEREF              'hrAbs'
           2456_0  COME_FROM          2448  '2448'

 L. 449      2456  LOAD_FAST                'used'
             2458  LOAD_CONST               1
             2460  INPLACE_ADD      
             2462  STORE_FAST               'used'
         2464_2466  JUMP_FORWARD       4704  'to 4704'
           2468_0  COME_FROM          2442  '2442'

 L. 450      2468  LOAD_FAST                'word'
             2470  LOAD_CONST               None
             2472  LOAD_CONST               5
             2474  BUILD_SLICE_2         2 
             2476  BINARY_SUBSCR    
             2478  LOAD_STR                 'aften'
             2480  COMPARE_OP               ==
         2482_2484  POP_JUMP_IF_FALSE  2508  'to 2508'

 L. 451      2486  LOAD_DEREF               'hrAbs'
         2488_2490  POP_JUMP_IF_TRUE   2496  'to 2496'

 L. 452      2492  LOAD_CONST               19
             2494  STORE_DEREF              'hrAbs'
           2496_0  COME_FROM          2488  '2488'

 L. 453      2496  LOAD_FAST                'used'
             2498  LOAD_CONST               1
             2500  INPLACE_ADD      
             2502  STORE_FAST               'used'
         2504_2506  JUMP_FORWARD       4704  'to 4704'
           2508_0  COME_FROM          2482  '2482'

 L. 455      2508  LOAD_FAST                'word'
             2510  LOAD_STR                 'time'
             2512  COMPARE_OP               ==
         2514_2516  POP_JUMP_IF_FALSE  2652  'to 2652'

 L. 456      2518  LOAD_FAST                'wordPrev'
             2520  LOAD_FAST                'markers'
             2522  COMPARE_OP               in
         2524_2526  POP_JUMP_IF_TRUE   2538  'to 2538'
             2528  LOAD_FAST                'wordPrevPrev'
             2530  LOAD_FAST                'markers'
             2532  COMPARE_OP               in
         2534_2536  POP_JUMP_IF_FALSE  2652  'to 2652'
           2538_0  COME_FROM          2524  '2524'

 L. 457      2538  LOAD_FAST                'wordPrev'
             2540  LOAD_CONST               None
             2542  LOAD_CONST               4
             2544  BUILD_SLICE_2         2 
             2546  BINARY_SUBSCR    
             2548  LOAD_STR                 'halv'
             2550  COMPARE_OP               ==
         2552_2554  POP_JUMP_IF_FALSE  2562  'to 2562'

 L. 458      2556  LOAD_CONST               30
             2558  STORE_DEREF              'minOffset'
             2560  JUMP_FORWARD       2598  'to 2598'
           2562_0  COME_FROM          2552  '2552'

 L. 459      2562  LOAD_FAST                'wordPrev'
             2564  LOAD_STR                 'kvarter'
             2566  COMPARE_OP               ==
         2568_2570  POP_JUMP_IF_FALSE  2578  'to 2578'

 L. 460      2572  LOAD_CONST               15
             2574  STORE_DEREF              'minOffset'
             2576  JUMP_FORWARD       2598  'to 2598'
           2578_0  COME_FROM          2568  '2568'

 L. 461      2578  LOAD_FAST                'wordPrev'
             2580  LOAD_STR                 'trekvarter'
             2582  COMPARE_OP               ==
         2584_2586  POP_JUMP_IF_FALSE  2594  'to 2594'

 L. 462      2588  LOAD_CONST               45
             2590  STORE_DEREF              'minOffset'
             2592  JUMP_FORWARD       2598  'to 2598'
           2594_0  COME_FROM          2584  '2584'

 L. 464      2594  LOAD_CONST               1
             2596  STORE_DEREF              'hrOffset'
           2598_0  COME_FROM          2592  '2592'
           2598_1  COME_FROM          2576  '2576'
           2598_2  COME_FROM          2560  '2560'

 L. 465      2598  LOAD_FAST                'wordPrevPrev'
             2600  LOAD_FAST                'markers'
             2602  COMPARE_OP               in
         2604_2606  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 466      2608  LOAD_STR                 ''
             2610  LOAD_FAST                'words'
             2612  LOAD_FAST                'idx'
             2614  LOAD_CONST               2
             2616  BINARY_SUBTRACT  
             2618  STORE_SUBSCR     
           2620_0  COME_FROM          2604  '2604'

 L. 467      2620  LOAD_STR                 ''
             2622  LOAD_FAST                'words'
             2624  LOAD_FAST                'idx'
             2626  LOAD_CONST               1
             2628  BINARY_SUBTRACT  
             2630  STORE_SUBSCR     

 L. 468      2632  LOAD_FAST                'used'
             2634  LOAD_CONST               1
             2636  INPLACE_ADD      
             2638  STORE_FAST               'used'

 L. 469      2640  LOAD_CONST               -1
             2642  STORE_DEREF              'hrAbs'

 L. 470      2644  LOAD_CONST               -1
             2646  STORE_DEREF              'minAbs'
         2648_2650  JUMP_FORWARD       4704  'to 4704'
           2652_0  COME_FROM          2534  '2534'
           2652_1  COME_FROM          2514  '2514'

 L. 472      2652  LOAD_FAST                'word'
             2654  LOAD_CONST               0
             2656  BINARY_SUBSCR    
             2658  LOAD_METHOD              isdigit
             2660  CALL_METHOD_0         0  '0 positional arguments'
         2662_2664  POP_JUMP_IF_FALSE  4704  'to 4704'

 L. 473      2666  LOAD_CONST               True
             2668  STORE_FAST               'isTime'

 L. 474      2670  LOAD_STR                 ''
             2672  STORE_FAST               'strHH'

 L. 475      2674  LOAD_STR                 ''
             2676  STORE_FAST               'strMM'

 L. 476      2678  LOAD_STR                 ''
             2680  STORE_FAST               'remainder'

 L. 477      2682  LOAD_STR                 ':'
             2684  LOAD_FAST                'word'
             2686  COMPARE_OP               in
         2688_2690  POP_JUMP_IF_FALSE  3324  'to 3324'

 L. 480      2692  LOAD_CONST               0
             2694  STORE_FAST               'stage'

 L. 481      2696  LOAD_GLOBAL              len
             2698  LOAD_FAST                'word'
             2700  CALL_FUNCTION_1       1  '1 positional argument'
             2702  STORE_FAST               'length'

 L. 482      2704  SETUP_LOOP         2880  'to 2880'
             2706  LOAD_GLOBAL              range
             2708  LOAD_FAST                'length'
             2710  CALL_FUNCTION_1       1  '1 positional argument'
             2712  GET_ITER         
           2714_0  COME_FROM          2848  '2848'
             2714  FOR_ITER           2878  'to 2878'
             2716  STORE_FAST               'i'

 L. 483      2718  LOAD_FAST                'stage'
             2720  LOAD_CONST               0
             2722  COMPARE_OP               ==
         2724_2726  POP_JUMP_IF_FALSE  2790  'to 2790'

 L. 484      2728  LOAD_FAST                'word'
             2730  LOAD_FAST                'i'
             2732  BINARY_SUBSCR    
             2734  LOAD_METHOD              isdigit
             2736  CALL_METHOD_0         0  '0 positional arguments'
         2738_2740  POP_JUMP_IF_FALSE  2756  'to 2756'

 L. 485      2742  LOAD_FAST                'strHH'
             2744  LOAD_FAST                'word'
             2746  LOAD_FAST                'i'
             2748  BINARY_SUBSCR    
             2750  INPLACE_ADD      
             2752  STORE_FAST               'strHH'
             2754  JUMP_FORWARD       2788  'to 2788'
           2756_0  COME_FROM          2738  '2738'

 L. 486      2756  LOAD_FAST                'word'
             2758  LOAD_FAST                'i'
             2760  BINARY_SUBSCR    
             2762  LOAD_STR                 ':'
             2764  COMPARE_OP               ==
         2766_2768  POP_JUMP_IF_FALSE  2776  'to 2776'

 L. 487      2770  LOAD_CONST               1
             2772  STORE_FAST               'stage'
             2774  JUMP_FORWARD       2788  'to 2788'
           2776_0  COME_FROM          2766  '2766'

 L. 489      2776  LOAD_CONST               2
             2778  STORE_FAST               'stage'

 L. 490      2780  LOAD_FAST                'i'
             2782  LOAD_CONST               1
             2784  INPLACE_SUBTRACT 
             2786  STORE_FAST               'i'
           2788_0  COME_FROM          2774  '2774'
           2788_1  COME_FROM          2754  '2754'
             2788  JUMP_BACK          2714  'to 2714'
           2790_0  COME_FROM          2724  '2724'

 L. 491      2790  LOAD_FAST                'stage'
             2792  LOAD_CONST               1
             2794  COMPARE_OP               ==
         2796_2798  POP_JUMP_IF_FALSE  2842  'to 2842'

 L. 492      2800  LOAD_FAST                'word'
             2802  LOAD_FAST                'i'
             2804  BINARY_SUBSCR    
             2806  LOAD_METHOD              isdigit
             2808  CALL_METHOD_0         0  '0 positional arguments'
         2810_2812  POP_JUMP_IF_FALSE  2828  'to 2828'

 L. 493      2814  LOAD_FAST                'strMM'
             2816  LOAD_FAST                'word'
             2818  LOAD_FAST                'i'
             2820  BINARY_SUBSCR    
             2822  INPLACE_ADD      
             2824  STORE_FAST               'strMM'
             2826  JUMP_FORWARD       2840  'to 2840'
           2828_0  COME_FROM          2810  '2810'

 L. 495      2828  LOAD_CONST               2
             2830  STORE_FAST               'stage'

 L. 496      2832  LOAD_FAST                'i'
             2834  LOAD_CONST               1
             2836  INPLACE_SUBTRACT 
             2838  STORE_FAST               'i'
           2840_0  COME_FROM          2826  '2826'
             2840  JUMP_BACK          2714  'to 2714'
           2842_0  COME_FROM          2796  '2796'

 L. 497      2842  LOAD_FAST                'stage'
             2844  LOAD_CONST               2
             2846  COMPARE_OP               ==
         2848_2850  POP_JUMP_IF_FALSE  2714  'to 2714'

 L. 498      2852  LOAD_FAST                'word'
             2854  LOAD_FAST                'i'
             2856  LOAD_CONST               None
             2858  BUILD_SLICE_2         2 
             2860  BINARY_SUBSCR    
             2862  LOAD_METHOD              replace
             2864  LOAD_STR                 '.'
             2866  LOAD_STR                 ''
             2868  CALL_METHOD_2         2  '2 positional arguments'
             2870  STORE_FAST               'remainder'

 L. 499      2872  BREAK_LOOP       
         2874_2876  JUMP_BACK          2714  'to 2714'
             2878  POP_BLOCK        
           2880_0  COME_FROM_LOOP     2704  '2704'

 L. 500      2880  LOAD_FAST                'remainder'
             2882  LOAD_STR                 ''
             2884  COMPARE_OP               ==
         2886_2888  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 501      2890  LOAD_FAST                'wordNext'
             2892  LOAD_METHOD              replace
             2894  LOAD_STR                 '.'
             2896  LOAD_STR                 ''
             2898  CALL_METHOD_2         2  '2 positional arguments'
             2900  STORE_FAST               'nextWord'

 L. 502      2902  LOAD_FAST                'nextWord'
             2904  LOAD_STR                 'am'
             2906  COMPARE_OP               ==
         2908_2910  POP_JUMP_IF_TRUE   2922  'to 2922'
             2912  LOAD_FAST                'nextWord'
             2914  LOAD_STR                 'pm'
             2916  COMPARE_OP               ==
         2918_2920  POP_JUMP_IF_FALSE  2938  'to 2938'
           2922_0  COME_FROM          2908  '2908'

 L. 503      2922  LOAD_FAST                'nextWord'
             2924  STORE_FAST               'remainder'

 L. 504      2926  LOAD_FAST                'used'
             2928  LOAD_CONST               1
             2930  INPLACE_ADD      
             2932  STORE_FAST               'used'
         2934_2936  JUMP_ABSOLUTE      4546  'to 4546'
           2938_0  COME_FROM          2918  '2918'

 L. 505      2938  LOAD_FAST                'nextWord'
             2940  LOAD_STR                 'aften'
             2942  COMPARE_OP               ==
         2944_2946  POP_JUMP_IF_FALSE  2964  'to 2964'

 L. 506      2948  LOAD_STR                 'pm'
             2950  STORE_FAST               'remainder'

 L. 507      2952  LOAD_FAST                'used'
             2954  LOAD_CONST               1
             2956  INPLACE_ADD      
             2958  STORE_FAST               'used'
         2960_2962  JUMP_ABSOLUTE      4546  'to 4546'
           2964_0  COME_FROM          2944  '2944'

 L. 508      2964  LOAD_FAST                'wordNext'
             2966  LOAD_STR                 'om'
             2968  COMPARE_OP               ==
         2970_2972  POP_JUMP_IF_FALSE  3000  'to 3000'
             2974  LOAD_FAST                'wordNextNext'
             2976  LOAD_STR                 'morgenen'
             2978  COMPARE_OP               ==
         2980_2982  POP_JUMP_IF_FALSE  3000  'to 3000'

 L. 509      2984  LOAD_STR                 'am'
             2986  STORE_FAST               'remainder'

 L. 510      2988  LOAD_FAST                'used'
             2990  LOAD_CONST               2
             2992  INPLACE_ADD      
             2994  STORE_FAST               'used'
         2996_2998  JUMP_ABSOLUTE      4546  'to 4546'
           3000_0  COME_FROM          2980  '2980'
           3000_1  COME_FROM          2970  '2970'

 L. 511      3000  LOAD_FAST                'wordNext'
             3002  LOAD_STR                 'om'
             3004  COMPARE_OP               ==
         3006_3008  POP_JUMP_IF_FALSE  3036  'to 3036'
             3010  LOAD_FAST                'wordNextNext'
             3012  LOAD_STR                 'eftermiddagen'
             3014  COMPARE_OP               ==
         3016_3018  POP_JUMP_IF_FALSE  3036  'to 3036'

 L. 512      3020  LOAD_STR                 'pm'
             3022  STORE_FAST               'remainder'

 L. 513      3024  LOAD_FAST                'used'
             3026  LOAD_CONST               2
             3028  INPLACE_ADD      
             3030  STORE_FAST               'used'
         3032_3034  JUMP_ABSOLUTE      4546  'to 4546'
           3036_0  COME_FROM          3016  '3016'
           3036_1  COME_FROM          3006  '3006'

 L. 514      3036  LOAD_FAST                'wordNext'
             3038  LOAD_STR                 'om'
             3040  COMPARE_OP               ==
         3042_3044  POP_JUMP_IF_FALSE  3070  'to 3070'
             3046  LOAD_FAST                'wordNextNext'
             3048  LOAD_STR                 'aftenen'
             3050  COMPARE_OP               ==
         3052_3054  POP_JUMP_IF_FALSE  3070  'to 3070'

 L. 515      3056  LOAD_STR                 'pm'
             3058  STORE_FAST               'remainder'

 L. 516      3060  LOAD_FAST                'used'
             3062  LOAD_CONST               2
             3064  INPLACE_ADD      
             3066  STORE_FAST               'used'
             3068  JUMP_FORWARD       4546  'to 4546'
           3070_0  COME_FROM          3052  '3052'
           3070_1  COME_FROM          3042  '3042'

 L. 517      3070  LOAD_FAST                'wordNext'
             3072  LOAD_STR                 'morgen'
             3074  COMPARE_OP               ==
         3076_3078  POP_JUMP_IF_FALSE  3094  'to 3094'

 L. 518      3080  LOAD_STR                 'am'
             3082  STORE_FAST               'remainder'

 L. 519      3084  LOAD_FAST                'used'
             3086  LOAD_CONST               1
             3088  INPLACE_ADD      
             3090  STORE_FAST               'used'
             3092  JUMP_FORWARD       4546  'to 4546'
           3094_0  COME_FROM          3076  '3076'

 L. 520      3094  LOAD_FAST                'wordNext'
             3096  LOAD_STR                 'eftermiddag'
             3098  COMPARE_OP               ==
         3100_3102  POP_JUMP_IF_FALSE  3118  'to 3118'

 L. 521      3104  LOAD_STR                 'pm'
             3106  STORE_FAST               'remainder'

 L. 522      3108  LOAD_FAST                'used'
             3110  LOAD_CONST               1
             3112  INPLACE_ADD      
             3114  STORE_FAST               'used'
             3116  JUMP_FORWARD       4546  'to 4546'
           3118_0  COME_FROM          3100  '3100'

 L. 523      3118  LOAD_FAST                'wordNext'
             3120  LOAD_STR                 'aften'
             3122  COMPARE_OP               ==
         3124_3126  POP_JUMP_IF_FALSE  3142  'to 3142'

 L. 524      3128  LOAD_STR                 'pm'
             3130  STORE_FAST               'remainder'

 L. 525      3132  LOAD_FAST                'used'
             3134  LOAD_CONST               1
             3136  INPLACE_ADD      
             3138  STORE_FAST               'used'
             3140  JUMP_FORWARD       4546  'to 4546'
           3142_0  COME_FROM          3124  '3124'

 L. 526      3142  LOAD_FAST                'wordNext'
             3144  LOAD_STR                 'i'
             3146  COMPARE_OP               ==
         3148_3150  POP_JUMP_IF_FALSE  3172  'to 3172'
             3152  LOAD_FAST                'wordNextNext'
             3154  LOAD_STR                 'morgen'
             3156  COMPARE_OP               ==
         3158_3160  POP_JUMP_IF_FALSE  3172  'to 3172'

 L. 527      3162  LOAD_STR                 'am'
             3164  STORE_FAST               'remainder'

 L. 528      3166  LOAD_CONST               2
             3168  STORE_FAST               'used'
             3170  JUMP_FORWARD       4546  'to 4546'
           3172_0  COME_FROM          3158  '3158'
           3172_1  COME_FROM          3148  '3148'

 L. 529      3172  LOAD_FAST                'wordNext'
             3174  LOAD_STR                 'i'
             3176  COMPARE_OP               ==
         3178_3180  POP_JUMP_IF_FALSE  3202  'to 3202'
             3182  LOAD_FAST                'wordNextNext'
             3184  LOAD_STR                 'eftermiddag'
             3186  COMPARE_OP               ==
         3188_3190  POP_JUMP_IF_FALSE  3202  'to 3202'

 L. 530      3192  LOAD_STR                 'pm'
             3194  STORE_FAST               'remainder'

 L. 531      3196  LOAD_CONST               2
             3198  STORE_FAST               'used'
             3200  JUMP_FORWARD       4546  'to 4546'
           3202_0  COME_FROM          3188  '3188'
           3202_1  COME_FROM          3178  '3178'

 L. 532      3202  LOAD_FAST                'wordNext'
             3204  LOAD_STR                 'i'
             3206  COMPARE_OP               ==
         3208_3210  POP_JUMP_IF_FALSE  3232  'to 3232'
             3212  LOAD_FAST                'wordNextNext'
             3214  LOAD_STR                 'aften'
             3216  COMPARE_OP               ==
         3218_3220  POP_JUMP_IF_FALSE  3232  'to 3232'

 L. 533      3222  LOAD_STR                 'pm'
             3224  STORE_FAST               'remainder'

 L. 534      3226  LOAD_CONST               2
             3228  STORE_FAST               'used'
             3230  JUMP_FORWARD       4546  'to 4546'
           3232_0  COME_FROM          3218  '3218'
           3232_1  COME_FROM          3208  '3208'

 L. 535      3232  LOAD_FAST                'wordNext'
             3234  LOAD_STR                 'natten'
             3236  COMPARE_OP               ==
         3238_3240  POP_JUMP_IF_FALSE  3272  'to 3272'

 L. 536      3242  LOAD_FAST                'strHH'
             3244  LOAD_CONST               4
             3246  COMPARE_OP               >
         3248_3250  POP_JUMP_IF_FALSE  3258  'to 3258'

 L. 537      3252  LOAD_STR                 'pm'
             3254  STORE_FAST               'remainder'
             3256  JUMP_FORWARD       3262  'to 3262'
           3258_0  COME_FROM          3248  '3248'

 L. 539      3258  LOAD_STR                 'am'
             3260  STORE_FAST               'remainder'
           3262_0  COME_FROM          3256  '3256'

 L. 540      3262  LOAD_FAST                'used'
             3264  LOAD_CONST               1
             3266  INPLACE_ADD      
             3268  STORE_FAST               'used'
             3270  JUMP_FORWARD       4546  'to 4546'
           3272_0  COME_FROM          3238  '3238'

 L. 542      3272  LOAD_FAST                'timeQualifier'
             3274  LOAD_STR                 ''
             3276  COMPARE_OP               !=
         3278_3280  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 543      3282  LOAD_FAST                'strHH'
             3284  LOAD_CONST               12
             3286  COMPARE_OP               <=
         3288_3290  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 544      3292  LOAD_FAST                'timeQualifier'
             3294  LOAD_STR                 'aftenen'
             3296  COMPARE_OP               ==
         3298_3300  POP_JUMP_IF_TRUE   3312  'to 3312'

 L. 545      3302  LOAD_FAST                'timeQualifier'
             3304  LOAD_STR                 'eftermiddagen'
             3306  COMPARE_OP               ==
         3308_3310  POP_JUMP_IF_FALSE  4546  'to 4546'
           3312_0  COME_FROM          3298  '3298'

 L. 546      3312  LOAD_FAST                'strHH'
             3314  LOAD_CONST               12
             3316  INPLACE_ADD      
             3318  STORE_FAST               'strHH'
         3320_3322  JUMP_FORWARD       4546  'to 4546'
           3324_0  COME_FROM          2688  '2688'

 L. 550      3324  LOAD_GLOBAL              len
             3326  LOAD_FAST                'word'
             3328  CALL_FUNCTION_1       1  '1 positional argument'
             3330  STORE_FAST               'length'

 L. 551      3332  LOAD_STR                 ''
             3334  STORE_FAST               'strNum'

 L. 552      3336  LOAD_STR                 ''
             3338  STORE_FAST               'remainder'

 L. 553      3340  SETUP_LOOP         3400  'to 3400'
             3342  LOAD_GLOBAL              range
             3344  LOAD_FAST                'length'
             3346  CALL_FUNCTION_1       1  '1 positional argument'
             3348  GET_ITER         
             3350  FOR_ITER           3398  'to 3398'
             3352  STORE_FAST               'i'

 L. 554      3354  LOAD_FAST                'word'
             3356  LOAD_FAST                'i'
             3358  BINARY_SUBSCR    
             3360  LOAD_METHOD              isdigit
             3362  CALL_METHOD_0         0  '0 positional arguments'
         3364_3366  POP_JUMP_IF_FALSE  3382  'to 3382'

 L. 555      3368  LOAD_FAST                'strNum'
             3370  LOAD_FAST                'word'
             3372  LOAD_FAST                'i'
             3374  BINARY_SUBSCR    
             3376  INPLACE_ADD      
             3378  STORE_FAST               'strNum'
             3380  JUMP_BACK          3350  'to 3350'
           3382_0  COME_FROM          3364  '3364'

 L. 557      3382  LOAD_FAST                'remainder'
             3384  LOAD_FAST                'word'
             3386  LOAD_FAST                'i'
             3388  BINARY_SUBSCR    
             3390  INPLACE_ADD      
             3392  STORE_FAST               'remainder'
         3394_3396  JUMP_BACK          3350  'to 3350'
             3398  POP_BLOCK        
           3400_0  COME_FROM_LOOP     3340  '3340'

 L. 559      3400  LOAD_FAST                'remainder'
             3402  LOAD_STR                 ''
             3404  COMPARE_OP               ==
         3406_3408  POP_JUMP_IF_FALSE  3430  'to 3430'

 L. 560      3410  LOAD_FAST                'wordNext'
             3412  LOAD_METHOD              replace
             3414  LOAD_STR                 '.'
             3416  LOAD_STR                 ''
             3418  CALL_METHOD_2         2  '2 positional arguments'
             3420  LOAD_METHOD              lstrip
             3422  CALL_METHOD_0         0  '0 positional arguments'
             3424  LOAD_METHOD              rstrip
             3426  CALL_METHOD_0         0  '0 positional arguments'
             3428  STORE_FAST               'remainder'
           3430_0  COME_FROM          3406  '3406'

 L. 563      3430  LOAD_FAST                'remainder'
             3432  LOAD_STR                 'pm'
             3434  COMPARE_OP               ==
         3436_3438  POP_JUMP_IF_TRUE   3470  'to 3470'

 L. 564      3440  LOAD_FAST                'wordNext'
             3442  LOAD_STR                 'pm'
             3444  COMPARE_OP               ==
         3446_3448  POP_JUMP_IF_TRUE   3470  'to 3470'

 L. 565      3450  LOAD_FAST                'remainder'
             3452  LOAD_STR                 'p.m.'
             3454  COMPARE_OP               ==
         3456_3458  POP_JUMP_IF_TRUE   3470  'to 3470'

 L. 566      3460  LOAD_FAST                'wordNext'
             3462  LOAD_STR                 'p.m.'
             3464  COMPARE_OP               ==
         3466_3468  POP_JUMP_IF_FALSE  3486  'to 3486'
           3470_0  COME_FROM          3456  '3456'
           3470_1  COME_FROM          3446  '3446'
           3470_2  COME_FROM          3436  '3436'

 L. 567      3470  LOAD_FAST                'strNum'
             3472  STORE_FAST               'strHH'

 L. 568      3474  LOAD_STR                 'pm'
             3476  STORE_FAST               'remainder'

 L. 569      3478  LOAD_CONST               1
             3480  STORE_FAST               'used'
         3482_3484  JUMP_FORWARD       4546  'to 4546'
           3486_0  COME_FROM          3466  '3466'

 L. 571      3486  LOAD_FAST                'remainder'
             3488  LOAD_STR                 'am'
             3490  COMPARE_OP               ==
         3492_3494  POP_JUMP_IF_TRUE   3526  'to 3526'

 L. 572      3496  LOAD_FAST                'wordNext'
             3498  LOAD_STR                 'am'
             3500  COMPARE_OP               ==
         3502_3504  POP_JUMP_IF_TRUE   3526  'to 3526'

 L. 573      3506  LOAD_FAST                'remainder'
             3508  LOAD_STR                 'a.m.'
             3510  COMPARE_OP               ==
         3512_3514  POP_JUMP_IF_TRUE   3526  'to 3526'

 L. 574      3516  LOAD_FAST                'wordNext'
             3518  LOAD_STR                 'a.m.'
             3520  COMPARE_OP               ==
         3522_3524  POP_JUMP_IF_FALSE  3542  'to 3542'
           3526_0  COME_FROM          3512  '3512'
           3526_1  COME_FROM          3502  '3502'
           3526_2  COME_FROM          3492  '3492'

 L. 575      3526  LOAD_FAST                'strNum'
             3528  STORE_FAST               'strHH'

 L. 576      3530  LOAD_STR                 'am'
             3532  STORE_FAST               'remainder'

 L. 577      3534  LOAD_CONST               1
             3536  STORE_FAST               'used'
         3538_3540  JUMP_FORWARD       4546  'to 4546'
           3542_0  COME_FROM          3522  '3522'

 L. 579      3542  LOAD_FAST                'wordNext'
             3544  LOAD_STR                 'time'
             3546  COMPARE_OP               ==
         3548_3550  POP_JUMP_IF_FALSE  3594  'to 3594'
             3552  LOAD_GLOBAL              int
             3554  LOAD_FAST                'word'
             3556  CALL_FUNCTION_1       1  '1 positional argument'
             3558  LOAD_CONST               100
             3560  COMPARE_OP               <
         3562_3564  POP_JUMP_IF_FALSE  3594  'to 3594'

 L. 581      3566  LOAD_GLOBAL              int
             3568  LOAD_FAST                'word'
             3570  CALL_FUNCTION_1       1  '1 positional argument'
             3572  STORE_DEREF              'hrOffset'

 L. 582      3574  LOAD_CONST               2
             3576  STORE_FAST               'used'

 L. 583      3578  LOAD_CONST               False
             3580  STORE_FAST               'isTime'

 L. 584      3582  LOAD_CONST               -1
             3584  STORE_DEREF              'hrAbs'

 L. 585      3586  LOAD_CONST               -1
             3588  STORE_DEREF              'minAbs'
         3590_3592  JUMP_FORWARD       4546  'to 4546'
           3594_0  COME_FROM          3562  '3562'
           3594_1  COME_FROM          3548  '3548'

 L. 586      3594  LOAD_FAST                'wordNext'
             3596  LOAD_STR                 'minut'
             3598  COMPARE_OP               ==
         3600_3602  POP_JUMP_IF_FALSE  3632  'to 3632'

 L. 588      3604  LOAD_GLOBAL              int
             3606  LOAD_FAST                'word'
             3608  CALL_FUNCTION_1       1  '1 positional argument'
             3610  STORE_DEREF              'minOffset'

 L. 589      3612  LOAD_CONST               2
             3614  STORE_FAST               'used'

 L. 590      3616  LOAD_CONST               False
             3618  STORE_FAST               'isTime'

 L. 591      3620  LOAD_CONST               -1
             3622  STORE_DEREF              'hrAbs'

 L. 592      3624  LOAD_CONST               -1
             3626  STORE_DEREF              'minAbs'
         3628_3630  JUMP_FORWARD       4546  'to 4546'
           3632_0  COME_FROM          3600  '3600'

 L. 593      3632  LOAD_FAST                'wordNext'
             3634  LOAD_STR                 'sekund'
             3636  COMPARE_OP               ==
         3638_3640  POP_JUMP_IF_FALSE  3670  'to 3670'

 L. 595      3642  LOAD_GLOBAL              int
             3644  LOAD_FAST                'word'
             3646  CALL_FUNCTION_1       1  '1 positional argument'
             3648  STORE_DEREF              'secOffset'

 L. 596      3650  LOAD_CONST               2
             3652  STORE_FAST               'used'

 L. 597      3654  LOAD_CONST               False
             3656  STORE_FAST               'isTime'

 L. 598      3658  LOAD_CONST               -1
             3660  STORE_DEREF              'hrAbs'

 L. 599      3662  LOAD_CONST               -1
             3664  STORE_DEREF              'minAbs'
         3666_3668  JUMP_FORWARD       4546  'to 4546'
           3670_0  COME_FROM          3638  '3638'

 L. 601      3670  LOAD_FAST                'wordNext'
             3672  LOAD_STR                 'time'
             3674  COMPARE_OP               ==
         3676_3678  POP_JUMP_IF_FALSE  4266  'to 4266'

 L. 602      3680  LOAD_FAST                'word'
             3682  STORE_FAST               'strHH'

 L. 603      3684  LOAD_FAST                'used'
             3686  LOAD_CONST               1
             3688  INPLACE_ADD      
             3690  STORE_FAST               'used'

 L. 604      3692  LOAD_CONST               True
             3694  STORE_FAST               'isTime'

 L. 605      3696  LOAD_FAST                'wordNextNext'
             3698  LOAD_FAST                'timeQualifier'
             3700  COMPARE_OP               ==
         3702_3704  POP_JUMP_IF_FALSE  3972  'to 3972'

 L. 606      3706  LOAD_STR                 ''
             3708  STORE_FAST               'strMM'

 L. 607      3710  LOAD_FAST                'wordNextNext'
             3712  LOAD_CONST               None
             3714  LOAD_CONST               11
             3716  BUILD_SLICE_2         2 
             3718  BINARY_SUBSCR    
             3720  LOAD_STR                 'eftermiddag'
             3722  COMPARE_OP               ==
         3724_3726  POP_JUMP_IF_FALSE  3742  'to 3742'

 L. 608      3728  LOAD_FAST                'used'
             3730  LOAD_CONST               1
             3732  INPLACE_ADD      
             3734  STORE_FAST               'used'

 L. 609      3736  LOAD_STR                 'pm'
             3738  STORE_FAST               'remainder'
             3740  JUMP_ABSOLUTE      4546  'to 4546'
           3742_0  COME_FROM          3724  '3724'

 L. 610      3742  LOAD_FAST                'wordNextNext'
             3744  LOAD_STR                 'om'
             3746  COMPARE_OP               ==
         3748_3750  POP_JUMP_IF_FALSE  3776  'to 3776'
             3752  LOAD_FAST                'wordNextNextNext'

 L. 611      3754  LOAD_STR                 'eftermiddagen'
             3756  COMPARE_OP               ==
         3758_3760  POP_JUMP_IF_FALSE  3776  'to 3776'

 L. 612      3762  LOAD_FAST                'used'
             3764  LOAD_CONST               2
             3766  INPLACE_ADD      
             3768  STORE_FAST               'used'

 L. 613      3770  LOAD_STR                 'pm'
             3772  STORE_FAST               'remainder'
             3774  JUMP_ABSOLUTE      4546  'to 4546'
           3776_0  COME_FROM          3758  '3758'
           3776_1  COME_FROM          3748  '3748'

 L. 614      3776  LOAD_FAST                'wordNextNext'
             3778  LOAD_CONST               None
             3780  LOAD_CONST               5
             3782  BUILD_SLICE_2         2 
             3784  BINARY_SUBSCR    
             3786  LOAD_STR                 'aften'
             3788  COMPARE_OP               ==
         3790_3792  POP_JUMP_IF_FALSE  3808  'to 3808'

 L. 615      3794  LOAD_FAST                'used'
             3796  LOAD_CONST               1
             3798  INPLACE_ADD      
             3800  STORE_FAST               'used'

 L. 616      3802  LOAD_STR                 'pm'
             3804  STORE_FAST               'remainder'
             3806  JUMP_ABSOLUTE      4546  'to 4546'
           3808_0  COME_FROM          3790  '3790'

 L. 617      3808  LOAD_FAST                'wordNextNext'
             3810  LOAD_STR                 'om'
             3812  COMPARE_OP               ==
         3814_3816  POP_JUMP_IF_FALSE  3842  'to 3842'
             3818  LOAD_FAST                'wordNextNextNext'

 L. 618      3820  LOAD_STR                 'aftenen'
             3822  COMPARE_OP               ==
         3824_3826  POP_JUMP_IF_FALSE  3842  'to 3842'

 L. 619      3828  LOAD_FAST                'used'
             3830  LOAD_CONST               2
             3832  INPLACE_ADD      
             3834  STORE_FAST               'used'

 L. 620      3836  LOAD_STR                 'pm'
             3838  STORE_FAST               'remainder'
             3840  JUMP_ABSOLUTE      4546  'to 4546'
           3842_0  COME_FROM          3824  '3824'
           3842_1  COME_FROM          3814  '3814'

 L. 621      3842  LOAD_FAST                'wordNextNext'
             3844  LOAD_CONST               None
             3846  LOAD_CONST               6
             3848  BUILD_SLICE_2         2 
             3850  BINARY_SUBSCR    
             3852  LOAD_STR                 'morgen'
             3854  COMPARE_OP               ==
         3856_3858  POP_JUMP_IF_FALSE  3874  'to 3874'

 L. 622      3860  LOAD_FAST                'used'
             3862  LOAD_CONST               1
             3864  INPLACE_ADD      
             3866  STORE_FAST               'used'

 L. 623      3868  LOAD_STR                 'am'
             3870  STORE_FAST               'remainder'
             3872  JUMP_ABSOLUTE      4546  'to 4546'
           3874_0  COME_FROM          3856  '3856'

 L. 624      3874  LOAD_FAST                'wordNextNext'
             3876  LOAD_STR                 'om'
             3878  COMPARE_OP               ==
         3880_3882  POP_JUMP_IF_FALSE  3908  'to 3908'
             3884  LOAD_FAST                'wordNextNextNext'

 L. 625      3886  LOAD_STR                 'morgenen'
             3888  COMPARE_OP               ==
         3890_3892  POP_JUMP_IF_FALSE  3908  'to 3908'

 L. 626      3894  LOAD_FAST                'used'
             3896  LOAD_CONST               2
             3898  INPLACE_ADD      
             3900  STORE_FAST               'used'

 L. 627      3902  LOAD_STR                 'am'
             3904  STORE_FAST               'remainder'
             3906  JUMP_ABSOLUTE      4546  'to 4546'
           3908_0  COME_FROM          3890  '3890'
           3908_1  COME_FROM          3880  '3880'

 L. 628      3908  LOAD_FAST                'wordNextNext'
             3910  LOAD_STR                 'natten'
             3912  COMPARE_OP               ==
         3914_3916  POP_JUMP_IF_FALSE  4262  'to 4262'

 L. 629      3918  LOAD_FAST                'used'
             3920  LOAD_CONST               1
             3922  INPLACE_ADD      
             3924  STORE_FAST               'used'

 L. 630      3926  LOAD_CONST               8
             3928  LOAD_GLOBAL              int
             3930  LOAD_FAST                'word'
             3932  CALL_FUNCTION_1       1  '1 positional argument'
             3934  DUP_TOP          
             3936  ROT_THREE        
             3938  COMPARE_OP               <=
         3940_3942  POP_JUMP_IF_FALSE  3954  'to 3954'
             3944  LOAD_CONST               12
             3946  COMPARE_OP               <=
         3948_3950  POP_JUMP_IF_FALSE  3964  'to 3964'
             3952  JUMP_FORWARD       3958  'to 3958'
           3954_0  COME_FROM          3940  '3940'
             3954  POP_TOP          
             3956  JUMP_FORWARD       3964  'to 3964'
           3958_0  COME_FROM          3952  '3952'

 L. 631      3958  LOAD_STR                 'pm'
             3960  STORE_FAST               'remainder'
             3962  JUMP_ABSOLUTE      4546  'to 4546'
           3964_0  COME_FROM          3956  '3956'
           3964_1  COME_FROM          3948  '3948'

 L. 633      3964  LOAD_STR                 'am'
             3966  STORE_FAST               'remainder'
         3968_3970  JUMP_ABSOLUTE      4546  'to 4546'
           3972_0  COME_FROM          3702  '3702'

 L. 635      3972  LOAD_GLOBAL              is_numeric
             3974  LOAD_FAST                'wordNextNext'
             3976  CALL_FUNCTION_1       1  '1 positional argument'
         3978_3980  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 636      3982  LOAD_FAST                'wordNextNext'
             3984  STORE_FAST               'strMM'

 L. 637      3986  LOAD_FAST                'used'
             3988  LOAD_CONST               1
             3990  INPLACE_ADD      
             3992  STORE_FAST               'used'

 L. 638      3994  LOAD_FAST                'wordNextNextNext'
             3996  LOAD_FAST                'timeQualifier'
             3998  COMPARE_OP               ==
         4000_4002  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 639      4004  LOAD_FAST                'wordNextNextNext'
             4006  LOAD_CONST               None
             4008  LOAD_CONST               11
             4010  BUILD_SLICE_2         2 
             4012  BINARY_SUBSCR    
             4014  LOAD_STR                 'eftermiddag'
             4016  COMPARE_OP               ==
         4018_4020  POP_JUMP_IF_FALSE  4036  'to 4036'

 L. 640      4022  LOAD_FAST                'used'
             4024  LOAD_CONST               1
             4026  INPLACE_ADD      
             4028  STORE_FAST               'used'

 L. 641      4030  LOAD_STR                 'pm'
             4032  STORE_FAST               'remainder'
             4034  JUMP_FORWARD       4546  'to 4546'
           4036_0  COME_FROM          4018  '4018'

 L. 642      4036  LOAD_FAST                'wordNextNextNext'
             4038  LOAD_STR                 'om'
             4040  COMPARE_OP               ==
         4042_4044  POP_JUMP_IF_FALSE  4070  'to 4070'

 L. 643      4046  LOAD_FAST                'wordNextNextNextNext'

 L. 644      4048  LOAD_STR                 'eftermiddagen'
             4050  COMPARE_OP               ==
         4052_4054  POP_JUMP_IF_FALSE  4070  'to 4070'

 L. 645      4056  LOAD_FAST                'used'
             4058  LOAD_CONST               2
             4060  INPLACE_ADD      
             4062  STORE_FAST               'used'

 L. 646      4064  LOAD_STR                 'pm'
             4066  STORE_FAST               'remainder'
             4068  JUMP_FORWARD       4546  'to 4546'
           4070_0  COME_FROM          4052  '4052'
           4070_1  COME_FROM          4042  '4042'

 L. 647      4070  LOAD_FAST                'wordNextNextNext'
             4072  LOAD_CONST               None
             4074  LOAD_CONST               6
             4076  BUILD_SLICE_2         2 
             4078  BINARY_SUBSCR    
             4080  LOAD_STR                 'natten'
             4082  COMPARE_OP               ==
         4084_4086  POP_JUMP_IF_FALSE  4102  'to 4102'

 L. 648      4088  LOAD_FAST                'used'
             4090  LOAD_CONST               1
             4092  INPLACE_ADD      
             4094  STORE_FAST               'used'

 L. 649      4096  LOAD_STR                 'pm'
             4098  STORE_FAST               'remainder'
             4100  JUMP_FORWARD       4546  'to 4546'
           4102_0  COME_FROM          4084  '4084'

 L. 650      4102  LOAD_FAST                'wordNextNextNext'
             4104  LOAD_STR                 'am'
             4106  COMPARE_OP               ==
         4108_4110  POP_JUMP_IF_FALSE  4136  'to 4136'

 L. 651      4112  LOAD_FAST                'wordNextNextNextNext'
             4114  LOAD_STR                 'natten'
             4116  COMPARE_OP               ==
         4118_4120  POP_JUMP_IF_FALSE  4136  'to 4136'

 L. 652      4122  LOAD_FAST                'used'
             4124  LOAD_CONST               2
             4126  INPLACE_ADD      
             4128  STORE_FAST               'used'

 L. 653      4130  LOAD_STR                 'pm'
             4132  STORE_FAST               'remainder'
             4134  JUMP_FORWARD       4546  'to 4546'
           4136_0  COME_FROM          4118  '4118'
           4136_1  COME_FROM          4108  '4108'

 L. 654      4136  LOAD_FAST                'wordNextNextNext'
             4138  LOAD_CONST               None
             4140  LOAD_CONST               7
             4142  BUILD_SLICE_2         2 
             4144  BINARY_SUBSCR    
             4146  LOAD_STR                 'morgenen'
             4148  COMPARE_OP               ==
         4150_4152  POP_JUMP_IF_FALSE  4168  'to 4168'

 L. 655      4154  LOAD_FAST                'used'
             4156  LOAD_CONST               1
             4158  INPLACE_ADD      
             4160  STORE_FAST               'used'

 L. 656      4162  LOAD_STR                 'am'
             4164  STORE_FAST               'remainder'
             4166  JUMP_FORWARD       4546  'to 4546'
           4168_0  COME_FROM          4150  '4150'

 L. 657      4168  LOAD_FAST                'wordNextNextNext'
             4170  LOAD_STR                 'om'
             4172  COMPARE_OP               ==
         4174_4176  POP_JUMP_IF_FALSE  4202  'to 4202'

 L. 658      4178  LOAD_FAST                'wordNextNextNextNext'
             4180  LOAD_STR                 'morgenen'
             4182  COMPARE_OP               ==
         4184_4186  POP_JUMP_IF_FALSE  4202  'to 4202'

 L. 659      4188  LOAD_FAST                'used'
             4190  LOAD_CONST               2
             4192  INPLACE_ADD      
             4194  STORE_FAST               'used'

 L. 660      4196  LOAD_STR                 'am'
             4198  STORE_FAST               'remainder'
             4200  JUMP_FORWARD       4546  'to 4546'
           4202_0  COME_FROM          4184  '4184'
           4202_1  COME_FROM          4174  '4174'

 L. 661      4202  LOAD_FAST                'wordNextNextNext'
             4204  LOAD_STR                 'natten'
             4206  COMPARE_OP               ==
         4208_4210  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 662      4212  LOAD_FAST                'used'
             4214  LOAD_CONST               1
             4216  INPLACE_ADD      
             4218  STORE_FAST               'used'

 L. 663      4220  LOAD_CONST               8
             4222  LOAD_GLOBAL              int
             4224  LOAD_FAST                'word'
             4226  CALL_FUNCTION_1       1  '1 positional argument'
             4228  DUP_TOP          
             4230  ROT_THREE        
             4232  COMPARE_OP               <=
         4234_4236  POP_JUMP_IF_FALSE  4248  'to 4248'
             4238  LOAD_CONST               12
             4240  COMPARE_OP               <=
         4242_4244  POP_JUMP_IF_FALSE  4258  'to 4258'
             4246  JUMP_FORWARD       4252  'to 4252'
           4248_0  COME_FROM          4234  '4234'
             4248  POP_TOP          
             4250  JUMP_FORWARD       4258  'to 4258'
           4252_0  COME_FROM          4246  '4246'

 L. 664      4252  LOAD_STR                 'pm'
             4254  STORE_FAST               'remainder'
             4256  JUMP_FORWARD       4546  'to 4546'
           4258_0  COME_FROM          4250  '4250'
           4258_1  COME_FROM          4242  '4242'

 L. 666      4258  LOAD_STR                 'am'
             4260  STORE_FAST               'remainder'
           4262_0  COME_FROM          3914  '3914'
         4262_4264  JUMP_FORWARD       4546  'to 4546'
           4266_0  COME_FROM          3676  '3676'

 L. 668      4266  LOAD_FAST                'wordNext'
             4268  LOAD_FAST                'timeQualifier'
             4270  COMPARE_OP               ==
         4272_4274  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 669      4276  LOAD_FAST                'word'
             4278  STORE_FAST               'strHH'

 L. 670      4280  LOAD_CONST               0
             4282  STORE_FAST               'strMM'

 L. 671      4284  LOAD_CONST               True
             4286  STORE_FAST               'isTime'

 L. 672      4288  LOAD_FAST                'wordNext'
             4290  LOAD_CONST               None
           4292_0  COME_FROM          3068  '3068'
             4292  LOAD_CONST               10
             4294  BUILD_SLICE_2         2 
             4296  BINARY_SUBSCR    
             4298  LOAD_STR                 'eftermidag'
             4300  COMPARE_OP               ==
         4302_4304  POP_JUMP_IF_FALSE  4320  'to 4320'

 L. 673      4306  LOAD_FAST                'used'
             4308  LOAD_CONST               1
             4310  INPLACE_ADD      
             4312  STORE_FAST               'used'

 L. 674      4314  LOAD_STR                 'pm'
           4316_0  COME_FROM          4034  '4034'
           4316_1  COME_FROM          3092  '3092'
             4316  STORE_FAST               'remainder'
             4318  JUMP_FORWARD       4546  'to 4546'
           4320_0  COME_FROM          4302  '4302'

 L. 675      4320  LOAD_FAST                'wordNext'
             4322  LOAD_STR                 'om'
             4324  COMPARE_OP               ==
         4326_4328  POP_JUMP_IF_FALSE  4354  'to 4354'

 L. 676      4330  LOAD_FAST                'wordNextNext'
             4332  LOAD_STR                 'eftermiddanen'
             4334  COMPARE_OP               ==
         4336_4338  POP_JUMP_IF_FALSE  4354  'to 4354'
           4340_0  COME_FROM          3116  '3116'

 L. 677      4340  LOAD_FAST                'used'
             4342  LOAD_CONST               2
             4344  INPLACE_ADD      
             4346  STORE_FAST               'used'

 L. 678      4348  LOAD_STR                 'pm'
           4350_0  COME_FROM          4068  '4068'
             4350  STORE_FAST               'remainder'
             4352  JUMP_FORWARD       4546  'to 4546'
           4354_0  COME_FROM          4336  '4336'
           4354_1  COME_FROM          4326  '4326'

 L. 679      4354  LOAD_FAST                'wordNext'
             4356  LOAD_CONST               None
             4358  LOAD_CONST               7
             4360  BUILD_SLICE_2         2 
             4362  BINARY_SUBSCR    
           4364_0  COME_FROM          3140  '3140'
             4364  LOAD_STR                 'aftenen'
             4366  COMPARE_OP               ==
         4368_4370  POP_JUMP_IF_FALSE  4386  'to 4386'

 L. 680      4372  LOAD_FAST                'used'
             4374  LOAD_CONST               1
             4376  INPLACE_ADD      
             4378  STORE_FAST               'used'

 L. 681      4380  LOAD_STR                 'pm'
           4382_0  COME_FROM          4100  '4100'
             4382  STORE_FAST               'remainder'
             4384  JUMP_FORWARD       4546  'to 4546'
           4386_0  COME_FROM          4368  '4368'

 L. 682      4386  LOAD_FAST                'wordNext'
             4388  LOAD_STR                 'om'
             4390  COMPARE_OP               ==
         4392_4394  POP_JUMP_IF_FALSE  4420  'to 4420'
             4396  LOAD_FAST                'wordNextNext'
             4398  LOAD_STR                 'aftenen'
             4400  COMPARE_OP               ==
         4402_4404  POP_JUMP_IF_FALSE  4420  'to 4420'

 L. 683      4406  LOAD_FAST                'used'
             4408  LOAD_CONST               2
             4410  INPLACE_ADD      
             4412  STORE_FAST               'used'

 L. 684      4414  LOAD_STR                 'pm'
           4416_0  COME_FROM          4134  '4134'
             4416  STORE_FAST               'remainder'
             4418  JUMP_FORWARD       4546  'to 4546'
           4420_0  COME_FROM          4402  '4402'
           4420_1  COME_FROM          4392  '4392'

 L. 685      4420  LOAD_FAST                'wordNext'
             4422  LOAD_CONST               None
           4424_0  COME_FROM          3200  '3200'
             4424  LOAD_CONST               7
             4426  BUILD_SLICE_2         2 
             4428  BINARY_SUBSCR    
             4430  LOAD_STR                 'morgenen'
             4432  COMPARE_OP               ==
         4434_4436  POP_JUMP_IF_FALSE  4452  'to 4452'

 L. 686      4438  LOAD_FAST                'used'
             4440  LOAD_CONST               1
             4442  INPLACE_ADD      
             4444  STORE_FAST               'used'

 L. 687      4446  LOAD_STR                 'am'
           4448_0  COME_FROM          4166  '4166'
             4448  STORE_FAST               'remainder'
             4450  JUMP_FORWARD       4546  'to 4546'
           4452_0  COME_FROM          4434  '4434'

 L. 688      4452  LOAD_FAST                'wordNext'
           4454_0  COME_FROM          3230  '3230'
             4454  LOAD_STR                 'ao'
             4456  COMPARE_OP               ==
         4458_4460  POP_JUMP_IF_FALSE  4486  'to 4486'
             4462  LOAD_FAST                'wordNextNext'
             4464  LOAD_STR                 'morgenen'
             4466  COMPARE_OP               ==
         4468_4470  POP_JUMP_IF_FALSE  4486  'to 4486'

 L. 689      4472  LOAD_FAST                'used'
             4474  LOAD_CONST               2
             4476  INPLACE_ADD      
             4478  STORE_FAST               'used'

 L. 690      4480  LOAD_STR                 'am'
           4482_0  COME_FROM          4200  '4200'
             4482  STORE_FAST               'remainder'
             4484  JUMP_FORWARD       4546  'to 4546'
           4486_0  COME_FROM          4468  '4468'
           4486_1  COME_FROM          4458  '4458'

 L. 691      4486  LOAD_FAST                'wordNext'
             4488  LOAD_STR                 'natten'
             4490  COMPARE_OP               ==
         4492_4494  POP_JUMP_IF_FALSE  4546  'to 4546'

 L. 692      4496  LOAD_FAST                'used'
             4498  LOAD_CONST               1
             4500  INPLACE_ADD      
             4502  STORE_FAST               'used'

 L. 693      4504  LOAD_CONST               8
             4506  LOAD_GLOBAL              int
             4508  LOAD_FAST                'word'
             4510  CALL_FUNCTION_1       1  '1 positional argument'
             4512  DUP_TOP          
             4514  ROT_THREE        
             4516  COMPARE_OP               <=
         4518_4520  POP_JUMP_IF_FALSE  4532  'to 4532'
             4522  LOAD_CONST               12
             4524  COMPARE_OP               <=
         4526_4528  POP_JUMP_IF_FALSE  4542  'to 4542'
             4530  JUMP_FORWARD       4536  'to 4536'
           4532_0  COME_FROM          4518  '4518'
             4532  POP_TOP          
             4534  JUMP_FORWARD       4542  'to 4542'
           4536_0  COME_FROM          4530  '4530'

 L. 694      4536  LOAD_STR                 'pm'
           4538_0  COME_FROM          4256  '4256'
             4538  STORE_FAST               'remainder'
             4540  JUMP_FORWARD       4546  'to 4546'
           4542_0  COME_FROM          4534  '4534'
           4542_1  COME_FROM          4526  '4526'

 L. 696      4542  LOAD_STR                 'am'
             4544  STORE_FAST               'remainder'
           4546_0  COME_FROM          4540  '4540'
           4546_1  COME_FROM          4492  '4492'
           4546_2  COME_FROM          4484  '4484'
           4546_3  COME_FROM          4450  '4450'
           4546_4  COME_FROM          4418  '4418'
           4546_5  COME_FROM          4384  '4384'
           4546_6  COME_FROM          4352  '4352'
           4546_7  COME_FROM          4318  '4318'
           4546_8  COME_FROM          4272  '4272'
           4546_9  COME_FROM          4262  '4262'
          4546_10  COME_FROM          4208  '4208'
          4546_11  COME_FROM          4000  '4000'
          4546_12  COME_FROM          3978  '3978'
          4546_13  COME_FROM          3666  '3666'
          4546_14  COME_FROM          3628  '3628'
          4546_15  COME_FROM          3590  '3590'
          4546_16  COME_FROM          3538  '3538'
          4546_17  COME_FROM          3482  '3482'
          4546_18  COME_FROM          3320  '3320'
          4546_19  COME_FROM          3308  '3308'
          4546_20  COME_FROM          3288  '3288'
          4546_21  COME_FROM          3278  '3278'
          4546_22  COME_FROM          2886  '2886'

 L. 703      4546  LOAD_FAST                'strHH'
         4548_4550  POP_JUMP_IF_FALSE  4560  'to 4560'
             4552  LOAD_GLOBAL              int
             4554  LOAD_FAST                'strHH'
             4556  CALL_FUNCTION_1       1  '1 positional argument'
             4558  JUMP_FORWARD       4562  'to 4562'
           4560_0  COME_FROM          4548  '4548'
             4560  LOAD_CONST               0
           4562_0  COME_FROM          4558  '4558'
             4562  STORE_FAST               'strHH'

 L. 704      4564  LOAD_FAST                'strMM'
         4566_4568  POP_JUMP_IF_FALSE  4578  'to 4578'
             4570  LOAD_GLOBAL              int
             4572  LOAD_FAST                'strMM'
             4574  CALL_FUNCTION_1       1  '1 positional argument'
             4576  JUMP_FORWARD       4580  'to 4580'
           4578_0  COME_FROM          4566  '4566'
             4578  LOAD_CONST               0
           4580_0  COME_FROM          4576  '4576'
             4580  STORE_FAST               'strMM'

 L. 705      4582  LOAD_FAST                'remainder'
             4584  LOAD_STR                 'pm'
             4586  COMPARE_OP               ==
         4588_4590  POP_JUMP_IF_FALSE  4610  'to 4610'
             4592  LOAD_FAST                'strHH'
             4594  LOAD_CONST               12
             4596  COMPARE_OP               <
         4598_4600  POP_JUMP_IF_FALSE  4610  'to 4610'
             4602  LOAD_FAST                'strHH'
             4604  LOAD_CONST               12
             4606  BINARY_ADD       
             4608  JUMP_FORWARD       4612  'to 4612'
           4610_0  COME_FROM          4598  '4598'
           4610_1  COME_FROM          4588  '4588'
             4610  LOAD_FAST                'strHH'
           4612_0  COME_FROM          4608  '4608'
             4612  STORE_FAST               'strHH'

 L. 706      4614  LOAD_FAST                'remainder'
             4616  LOAD_STR                 'am'
             4618  COMPARE_OP               ==
         4620_4622  POP_JUMP_IF_FALSE  4642  'to 4642'
             4624  LOAD_FAST                'strHH'
             4626  LOAD_CONST               12
             4628  COMPARE_OP               >=
         4630_4632  POP_JUMP_IF_FALSE  4642  'to 4642'
             4634  LOAD_FAST                'strHH'
             4636  LOAD_CONST               12
             4638  BINARY_SUBTRACT  
             4640  JUMP_FORWARD       4644  'to 4644'
           4642_0  COME_FROM          4630  '4630'
           4642_1  COME_FROM          4620  '4620'
             4642  LOAD_FAST                'strHH'
           4644_0  COME_FROM          4640  '4640'
             4644  STORE_FAST               'strHH'

 L. 707      4646  LOAD_FAST                'strHH'
             4648  LOAD_CONST               24
             4650  COMPARE_OP               >
         4652_4654  POP_JUMP_IF_TRUE   4666  'to 4666'
             4656  LOAD_FAST                'strMM'
             4658  LOAD_CONST               59
             4660  COMPARE_OP               >
         4662_4664  POP_JUMP_IF_FALSE  4674  'to 4674'
           4666_0  COME_FROM          4652  '4652'

 L. 708      4666  LOAD_CONST               False
             4668  STORE_FAST               'isTime'

 L. 709      4670  LOAD_CONST               0
             4672  STORE_FAST               'used'
           4674_0  COME_FROM          4662  '4662'

 L. 710      4674  LOAD_FAST                'isTime'
         4676_4678  POP_JUMP_IF_FALSE  4704  'to 4704'

 L. 711      4680  LOAD_FAST                'strHH'
             4682  LOAD_CONST               1
             4684  BINARY_MULTIPLY  
             4686  STORE_DEREF              'hrAbs'

 L. 712      4688  LOAD_FAST                'strMM'
             4690  LOAD_CONST               1
             4692  BINARY_MULTIPLY  
             4694  STORE_DEREF              'minAbs'

 L. 713      4696  LOAD_FAST                'used'
             4698  LOAD_CONST               1
             4700  INPLACE_ADD      
             4702  STORE_FAST               'used'
           4704_0  COME_FROM          4676  '4676'
           4704_1  COME_FROM          2662  '2662'
           4704_2  COME_FROM          2648  '2648'
           4704_3  COME_FROM          2504  '2504'
           4704_4  COME_FROM          2464  '2464'
           4704_5  COME_FROM          2424  '2424'
           4704_6  COME_FROM          2362  '2362'
           4704_7  COME_FROM          2328  '2328'

 L. 714      4704  LOAD_FAST                'used'
             4706  LOAD_CONST               0
             4708  COMPARE_OP               >
         4710_4712  POP_JUMP_IF_FALSE  2082  'to 2082'

 L. 716      4714  SETUP_LOOP         4746  'to 4746'
             4716  LOAD_GLOBAL              range
             4718  LOAD_FAST                'used'
             4720  CALL_FUNCTION_1       1  '1 positional argument'
             4722  GET_ITER         
             4724  FOR_ITER           4744  'to 4744'
             4726  STORE_FAST               'i'

 L. 717      4728  LOAD_STR                 ''
             4730  LOAD_FAST                'words'
             4732  LOAD_FAST                'idx'
             4734  LOAD_FAST                'i'
             4736  BINARY_ADD       
             4738  STORE_SUBSCR     
         4740_4742  JUMP_BACK          4724  'to 4724'
             4744  POP_BLOCK        
           4746_0  COME_FROM_LOOP     4714  '4714'

 L. 719      4746  LOAD_FAST                'wordPrev'
             4748  LOAD_STR                 'tidlig'
             4750  COMPARE_OP               ==
         4752_4754  POP_JUMP_IF_FALSE  4782  'to 4782'

 L. 720      4756  LOAD_CONST               -1
             4758  STORE_DEREF              'hrOffset'

 L. 721      4760  LOAD_STR                 ''
             4762  LOAD_FAST                'words'
             4764  LOAD_FAST                'idx'
             4766  LOAD_CONST               1
             4768  BINARY_SUBTRACT  
             4770  STORE_SUBSCR     

 L. 722      4772  LOAD_FAST                'idx'
             4774  LOAD_CONST               1
             4776  INPLACE_SUBTRACT 
             4778  STORE_FAST               'idx'
             4780  JUMP_FORWARD       4816  'to 4816'
           4782_0  COME_FROM          4752  '4752'

 L. 723      4782  LOAD_FAST                'wordPrev'
             4784  LOAD_STR                 'sen'
             4786  COMPARE_OP               ==
         4788_4790  POP_JUMP_IF_FALSE  4816  'to 4816'

 L. 724      4792  LOAD_CONST               1
             4794  STORE_DEREF              'hrOffset'

 L. 725      4796  LOAD_STR                 ''
             4798  LOAD_FAST                'words'
             4800  LOAD_FAST                'idx'
             4802  LOAD_CONST               1
             4804  BINARY_SUBTRACT  
             4806  STORE_SUBSCR     

 L. 726      4808  LOAD_FAST                'idx'
             4810  LOAD_CONST               1
             4812  INPLACE_SUBTRACT 
             4814  STORE_FAST               'idx'
           4816_0  COME_FROM          4788  '4788'
           4816_1  COME_FROM          4780  '4780'

 L. 727      4816  LOAD_FAST                'idx'
             4818  LOAD_CONST               0
             4820  COMPARE_OP               >
         4822_4824  POP_JUMP_IF_FALSE  4848  'to 4848'
             4826  LOAD_FAST                'wordPrev'
             4828  LOAD_FAST                'markers'
             4830  COMPARE_OP               in
         4832_4834  POP_JUMP_IF_FALSE  4848  'to 4848'

 L. 728      4836  LOAD_STR                 ''
             4838  LOAD_FAST                'words'
             4840  LOAD_FAST                'idx'
             4842  LOAD_CONST               1
             4844  BINARY_SUBTRACT  
             4846  STORE_SUBSCR     
           4848_0  COME_FROM          4832  '4832'
           4848_1  COME_FROM          4822  '4822'

 L. 729      4848  LOAD_FAST                'idx'
             4850  LOAD_CONST               1
             4852  COMPARE_OP               >
         4854_4856  POP_JUMP_IF_FALSE  4880  'to 4880'
             4858  LOAD_FAST                'wordPrevPrev'
             4860  LOAD_FAST                'markers'
             4862  COMPARE_OP               in
         4864_4866  POP_JUMP_IF_FALSE  4880  'to 4880'

 L. 730      4868  LOAD_STR                 ''
             4870  LOAD_FAST                'words'
             4872  LOAD_FAST                'idx'
             4874  LOAD_CONST               2
             4876  BINARY_SUBTRACT  
             4878  STORE_SUBSCR     
           4880_0  COME_FROM          4864  '4864'
           4880_1  COME_FROM          4854  '4854'

 L. 732      4880  LOAD_FAST                'idx'
             4882  LOAD_FAST                'used'
             4884  LOAD_CONST               1
             4886  BINARY_SUBTRACT  
             4888  INPLACE_ADD      
             4890  STORE_FAST               'idx'

 L. 733      4892  LOAD_CONST               True
             4894  STORE_DEREF              'found'
         4896_4898  JUMP_BACK          2082  'to 2082'
             4900  POP_BLOCK        
           4902_0  COME_FROM_LOOP     2070  '2070'

 L. 736      4902  LOAD_FAST                'date_found'
         4904_4906  POP_JUMP_IF_TRUE   4912  'to 4912'

 L. 737      4908  LOAD_CONST               None
             4910  RETURN_VALUE     
           4912_0  COME_FROM          4904  '4904'

 L. 739      4912  LOAD_DEREF               'dayOffset'
             4914  LOAD_CONST               False
             4916  COMPARE_OP               is
         4918_4920  POP_JUMP_IF_FALSE  4926  'to 4926'

 L. 740      4922  LOAD_CONST               0
             4924  STORE_DEREF              'dayOffset'
           4926_0  COME_FROM          4918  '4918'

 L. 744      4926  LOAD_FAST                'dateNow'
             4928  STORE_FAST               'extractedDate'

 L. 745      4930  LOAD_FAST                'extractedDate'
             4932  LOAD_ATTR                replace
             4934  LOAD_CONST               0

 L. 746      4936  LOAD_CONST               0

 L. 747      4938  LOAD_CONST               0

 L. 748      4940  LOAD_CONST               0
             4942  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             4944  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4946  STORE_FAST               'extractedDate'

 L. 749      4948  LOAD_DEREF               'datestr'
             4950  LOAD_STR                 ''
             4952  COMPARE_OP               !=
         4954_4956  POP_JUMP_IF_FALSE  5270  'to 5270'

 L. 750      4958  LOAD_STR                 'january'
             4960  LOAD_STR                 'february'
             4962  LOAD_STR                 'march'
             4964  LOAD_STR                 'april'
             4966  LOAD_STR                 'may'
             4968  LOAD_STR                 'june'

 L. 751      4970  LOAD_STR                 'july'
             4972  LOAD_STR                 'august'
             4974  LOAD_STR                 'september'
             4976  LOAD_STR                 'october'
             4978  LOAD_STR                 'november'

 L. 752      4980  LOAD_STR                 'december'
             4982  BUILD_LIST_12        12 
             4984  STORE_FAST               'en_months'

 L. 753      4986  LOAD_STR                 'jan'
             4988  LOAD_STR                 'feb'
             4990  LOAD_STR                 'mar'
             4992  LOAD_STR                 'apr'
             4994  LOAD_STR                 'may'
             4996  LOAD_STR                 'june'
             4998  LOAD_STR                 'july'

 L. 754      5000  LOAD_STR                 'aug'

 L. 755      5002  LOAD_STR                 'sept'
             5004  LOAD_STR                 'oct'
             5006  LOAD_STR                 'nov'
             5008  LOAD_STR                 'dec'
             5010  BUILD_LIST_12        12 
             5012  STORE_FAST               'en_monthsShort'

 L. 756      5014  SETUP_LOOP         5054  'to 5054'
             5016  LOAD_GLOBAL              enumerate
             5018  LOAD_FAST                'en_months'
             5020  CALL_FUNCTION_1       1  '1 positional argument'
             5022  GET_ITER         
             5024  FOR_ITER           5052  'to 5052'
             5026  UNPACK_SEQUENCE_2     2 
             5028  STORE_FAST               'idx'
             5030  STORE_FAST               'en_month'

 L. 757      5032  LOAD_DEREF               'datestr'
             5034  LOAD_METHOD              replace
             5036  LOAD_FAST                'months'
             5038  LOAD_FAST                'idx'
             5040  BINARY_SUBSCR    
             5042  LOAD_FAST                'en_month'
             5044  CALL_METHOD_2         2  '2 positional arguments'
             5046  STORE_DEREF              'datestr'
         5048_5050  JUMP_BACK          5024  'to 5024'
             5052  POP_BLOCK        
           5054_0  COME_FROM_LOOP     5014  '5014'

 L. 758      5054  SETUP_LOOP         5094  'to 5094'
             5056  LOAD_GLOBAL              enumerate
             5058  LOAD_FAST                'en_monthsShort'
             5060  CALL_FUNCTION_1       1  '1 positional argument'
             5062  GET_ITER         
             5064  FOR_ITER           5092  'to 5092'
             5066  UNPACK_SEQUENCE_2     2 
             5068  STORE_FAST               'idx'
             5070  STORE_FAST               'en_month'

 L. 759      5072  LOAD_DEREF               'datestr'
             5074  LOAD_METHOD              replace
             5076  LOAD_FAST                'monthsShort'
             5078  LOAD_FAST                'idx'
             5080  BINARY_SUBSCR    
             5082  LOAD_FAST                'en_month'
             5084  CALL_METHOD_2         2  '2 positional arguments'
             5086  STORE_DEREF              'datestr'
         5088_5090  JUMP_BACK          5064  'to 5064'
             5092  POP_BLOCK        
           5094_0  COME_FROM_LOOP     5054  '5054'

 L. 761      5094  LOAD_GLOBAL              datetime
             5096  LOAD_METHOD              strptime
             5098  LOAD_DEREF               'datestr'
             5100  LOAD_STR                 '%B %d'
             5102  CALL_METHOD_2         2  '2 positional arguments'
             5104  STORE_FAST               'temp'

 L. 762      5106  LOAD_FAST                'hasYear'
         5108_5110  POP_JUMP_IF_TRUE   5224  'to 5224'

 L. 763      5112  LOAD_FAST                'temp'
             5114  LOAD_ATTR                replace
             5116  LOAD_FAST                'extractedDate'
             5118  LOAD_ATTR                year
             5120  LOAD_CONST               ('year',)
             5122  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5124  STORE_FAST               'temp'

 L. 764      5126  LOAD_FAST                'extractedDate'
             5128  LOAD_FAST                'temp'
             5130  COMPARE_OP               <
         5132_5134  POP_JUMP_IF_FALSE  5178  'to 5178'

 L. 765      5136  LOAD_FAST                'extractedDate'
             5138  LOAD_ATTR                replace
             5140  LOAD_GLOBAL              int
             5142  LOAD_FAST                'currentYear'
             5144  CALL_FUNCTION_1       1  '1 positional argument'

 L. 766      5146  LOAD_GLOBAL              int

 L. 767      5148  LOAD_FAST                'temp'
             5150  LOAD_METHOD              strftime

 L. 768      5152  LOAD_STR                 '%m'
             5154  CALL_METHOD_1         1  '1 positional argument'
             5156  CALL_FUNCTION_1       1  '1 positional argument'

 L. 769      5158  LOAD_GLOBAL              int
             5160  LOAD_FAST                'temp'
             5162  LOAD_METHOD              strftime

 L. 770      5164  LOAD_STR                 '%d'
             5166  CALL_METHOD_1         1  '1 positional argument'
             5168  CALL_FUNCTION_1       1  '1 positional argument'
             5170  LOAD_CONST               ('year', 'month', 'day')
             5172  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5174  STORE_FAST               'extractedDate'
             5176  JUMP_FORWARD       5222  'to 5222'
           5178_0  COME_FROM          5132  '5132'

 L. 772      5178  LOAD_FAST                'extractedDate'
             5180  LOAD_ATTR                replace

 L. 773      5182  LOAD_GLOBAL              int
             5184  LOAD_FAST                'currentYear'
             5186  CALL_FUNCTION_1       1  '1 positional argument'
             5188  LOAD_CONST               1
             5190  BINARY_ADD       

 L. 774      5192  LOAD_GLOBAL              int
             5194  LOAD_FAST                'temp'
             5196  LOAD_METHOD              strftime
             5198  LOAD_STR                 '%m'
             5200  CALL_METHOD_1         1  '1 positional argument'
             5202  CALL_FUNCTION_1       1  '1 positional argument'

 L. 775      5204  LOAD_GLOBAL              int
             5206  LOAD_FAST                'temp'
             5208  LOAD_METHOD              strftime
             5210  LOAD_STR                 '%d'
             5212  CALL_METHOD_1         1  '1 positional argument'
             5214  CALL_FUNCTION_1       1  '1 positional argument'
             5216  LOAD_CONST               ('year', 'month', 'day')
             5218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5220  STORE_FAST               'extractedDate'
           5222_0  COME_FROM          5176  '5176'
             5222  JUMP_FORWARD       5270  'to 5270'
           5224_0  COME_FROM          5108  '5108'

 L. 777      5224  LOAD_FAST                'extractedDate'
             5226  LOAD_ATTR                replace

 L. 778      5228  LOAD_GLOBAL              int
             5230  LOAD_FAST                'temp'
             5232  LOAD_METHOD              strftime
             5234  LOAD_STR                 '%Y'
             5236  CALL_METHOD_1         1  '1 positional argument'
             5238  CALL_FUNCTION_1       1  '1 positional argument'

 L. 779      5240  LOAD_GLOBAL              int
             5242  LOAD_FAST                'temp'
             5244  LOAD_METHOD              strftime
             5246  LOAD_STR                 '%m'
             5248  CALL_METHOD_1         1  '1 positional argument'
             5250  CALL_FUNCTION_1       1  '1 positional argument'

 L. 780      5252  LOAD_GLOBAL              int
             5254  LOAD_FAST                'temp'
             5256  LOAD_METHOD              strftime
             5258  LOAD_STR                 '%d'
             5260  CALL_METHOD_1         1  '1 positional argument'
             5262  CALL_FUNCTION_1       1  '1 positional argument'
             5264  LOAD_CONST               ('year', 'month', 'day')
             5266  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5268  STORE_FAST               'extractedDate'
           5270_0  COME_FROM          5222  '5222'
           5270_1  COME_FROM          4954  '4954'

 L. 782      5270  LOAD_DEREF               'timeStr'
             5272  LOAD_STR                 ''
             5274  COMPARE_OP               !=
         5276_5278  POP_JUMP_IF_FALSE  5322  'to 5322'

 L. 783      5280  LOAD_GLOBAL              datetime
             5282  LOAD_DEREF               'timeStr'
             5284  CALL_FUNCTION_1       1  '1 positional argument'
             5286  STORE_FAST               'temp'

 L. 784      5288  LOAD_FAST                'extractedDate'
             5290  LOAD_ATTR                replace
             5292  LOAD_FAST                'temp'
             5294  LOAD_METHOD              strftime
             5296  LOAD_STR                 '%H'
             5298  CALL_METHOD_1         1  '1 positional argument'

 L. 785      5300  LOAD_FAST                'temp'
             5302  LOAD_METHOD              strftime
             5304  LOAD_STR                 '%M'
             5306  CALL_METHOD_1         1  '1 positional argument'

 L. 786      5308  LOAD_FAST                'temp'
             5310  LOAD_METHOD              strftime
             5312  LOAD_STR                 '%S'
             5314  CALL_METHOD_1         1  '1 positional argument'
             5316  LOAD_CONST               ('hour', 'minute', 'second')
             5318  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5320  STORE_FAST               'extractedDate'
           5322_0  COME_FROM          5276  '5276'

 L. 788      5322  LOAD_DEREF               'yearOffset'
             5324  LOAD_CONST               0
             5326  COMPARE_OP               !=
         5328_5330  POP_JUMP_IF_FALSE  5346  'to 5346'

 L. 789      5332  LOAD_FAST                'extractedDate'
             5334  LOAD_GLOBAL              relativedelta
             5336  LOAD_DEREF               'yearOffset'
             5338  LOAD_CONST               ('years',)
             5340  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5342  BINARY_ADD       
             5344  STORE_FAST               'extractedDate'
           5346_0  COME_FROM          5328  '5328'

 L. 790      5346  LOAD_DEREF               'monthOffset'
             5348  LOAD_CONST               0
             5350  COMPARE_OP               !=
         5352_5354  POP_JUMP_IF_FALSE  5370  'to 5370'

 L. 791      5356  LOAD_FAST                'extractedDate'
             5358  LOAD_GLOBAL              relativedelta
             5360  LOAD_DEREF               'monthOffset'
             5362  LOAD_CONST               ('months',)
             5364  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5366  BINARY_ADD       
             5368  STORE_FAST               'extractedDate'
           5370_0  COME_FROM          5352  '5352'

 L. 792      5370  LOAD_DEREF               'dayOffset'
             5372  LOAD_CONST               0
             5374  COMPARE_OP               !=
         5376_5378  POP_JUMP_IF_FALSE  5394  'to 5394'

 L. 793      5380  LOAD_FAST                'extractedDate'
             5382  LOAD_GLOBAL              relativedelta
             5384  LOAD_DEREF               'dayOffset'
             5386  LOAD_CONST               ('days',)
             5388  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5390  BINARY_ADD       
             5392  STORE_FAST               'extractedDate'
           5394_0  COME_FROM          5376  '5376'

 L. 795      5394  LOAD_DEREF               'hrAbs'
             5396  LOAD_CONST               None
             5398  COMPARE_OP               is
         5400_5402  POP_JUMP_IF_FALSE  5432  'to 5432'
             5404  LOAD_DEREF               'minAbs'
             5406  LOAD_CONST               None
             5408  COMPARE_OP               is
         5410_5412  POP_JUMP_IF_FALSE  5432  'to 5432'
             5414  LOAD_FAST                'default_time'
         5416_5418  POP_JUMP_IF_FALSE  5432  'to 5432'

 L. 796      5420  LOAD_FAST                'default_time'
             5422  LOAD_ATTR                hour
             5424  STORE_DEREF              'hrAbs'

 L. 797      5426  LOAD_FAST                'default_time'
             5428  LOAD_ATTR                minute
             5430  STORE_DEREF              'minAbs'
           5432_0  COME_FROM          5416  '5416'
           5432_1  COME_FROM          5410  '5410'
           5432_2  COME_FROM          5400  '5400'

 L. 799      5432  LOAD_DEREF               'hrAbs'
             5434  LOAD_CONST               -1
             5436  COMPARE_OP               !=
         5438_5440  POP_JUMP_IF_FALSE  5532  'to 5532'
             5442  LOAD_DEREF               'minAbs'
             5444  LOAD_CONST               -1
             5446  COMPARE_OP               !=
         5448_5450  POP_JUMP_IF_FALSE  5532  'to 5532'

 L. 801      5452  LOAD_FAST                'extractedDate'
             5454  LOAD_GLOBAL              relativedelta
             5456  LOAD_DEREF               'hrAbs'
         5458_5460  JUMP_IF_TRUE_OR_POP  5464  'to 5464'
             5462  LOAD_CONST               0
           5464_0  COME_FROM          5458  '5458'

 L. 802      5464  LOAD_DEREF               'minAbs'
         5466_5468  JUMP_IF_TRUE_OR_POP  5472  'to 5472'
             5470  LOAD_CONST               0
           5472_0  COME_FROM          5466  '5466'
             5472  LOAD_CONST               ('hours', 'minutes')
             5474  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5476  BINARY_ADD       
             5478  STORE_FAST               'extractedDate'

 L. 803      5480  LOAD_DEREF               'hrAbs'
         5482_5484  POP_JUMP_IF_TRUE   5492  'to 5492'
             5486  LOAD_DEREF               'minAbs'
         5488_5490  POP_JUMP_IF_FALSE  5532  'to 5532'
           5492_0  COME_FROM          5482  '5482'
             5492  LOAD_DEREF               'datestr'
             5494  LOAD_STR                 ''
             5496  COMPARE_OP               ==
         5498_5500  POP_JUMP_IF_FALSE  5532  'to 5532'

 L. 804      5502  LOAD_FAST                'daySpecified'
         5504_5506  POP_JUMP_IF_TRUE   5532  'to 5532'
             5508  LOAD_FAST                'dateNow'
             5510  LOAD_FAST                'extractedDate'
             5512  COMPARE_OP               >
         5514_5516  POP_JUMP_IF_FALSE  5532  'to 5532'

 L. 805      5518  LOAD_FAST                'extractedDate'
             5520  LOAD_GLOBAL              relativedelta
             5522  LOAD_CONST               1
             5524  LOAD_CONST               ('days',)
             5526  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5528  BINARY_ADD       
             5530  STORE_FAST               'extractedDate'
           5532_0  COME_FROM          5514  '5514'
           5532_1  COME_FROM          5504  '5504'
           5532_2  COME_FROM          5498  '5498'
           5532_3  COME_FROM          5488  '5488'
           5532_4  COME_FROM          5448  '5448'
           5532_5  COME_FROM          5438  '5438'

 L. 806      5532  LOAD_DEREF               'hrOffset'
             5534  LOAD_CONST               0
             5536  COMPARE_OP               !=
         5538_5540  POP_JUMP_IF_FALSE  5556  'to 5556'

 L. 807      5542  LOAD_FAST                'extractedDate'
             5544  LOAD_GLOBAL              relativedelta
             5546  LOAD_DEREF               'hrOffset'
             5548  LOAD_CONST               ('hours',)
             5550  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5552  BINARY_ADD       
             5554  STORE_FAST               'extractedDate'
           5556_0  COME_FROM          5538  '5538'

 L. 808      5556  LOAD_DEREF               'minOffset'
             5558  LOAD_CONST               0
             5560  COMPARE_OP               !=
         5562_5564  POP_JUMP_IF_FALSE  5580  'to 5580'

 L. 809      5566  LOAD_FAST                'extractedDate'
             5568  LOAD_GLOBAL              relativedelta
             5570  LOAD_DEREF               'minOffset'
             5572  LOAD_CONST               ('minutes',)
             5574  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5576  BINARY_ADD       
             5578  STORE_FAST               'extractedDate'
           5580_0  COME_FROM          5562  '5562'

 L. 810      5580  LOAD_DEREF               'secOffset'
             5582  LOAD_CONST               0
             5584  COMPARE_OP               !=
         5586_5588  POP_JUMP_IF_FALSE  5604  'to 5604'

 L. 811      5590  LOAD_FAST                'extractedDate'
             5592  LOAD_GLOBAL              relativedelta
             5594  LOAD_DEREF               'secOffset'
             5596  LOAD_CONST               ('seconds',)
             5598  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5600  BINARY_ADD       
             5602  STORE_FAST               'extractedDate'
           5604_0  COME_FROM          5586  '5586'

 L. 812      5604  SETUP_LOOP         5686  'to 5686'
             5606  LOAD_GLOBAL              enumerate
             5608  LOAD_FAST                'words'
             5610  CALL_FUNCTION_1       1  '1 positional argument'
             5612  GET_ITER         
           5614_0  COME_FROM          5668  '5668'
           5614_1  COME_FROM          5650  '5650'
           5614_2  COME_FROM          5632  '5632'
             5614  FOR_ITER           5684  'to 5684'
             5616  UNPACK_SEQUENCE_2     2 
             5618  STORE_FAST               'idx'
             5620  STORE_FAST               'word'

 L. 813      5622  LOAD_FAST                'words'
             5624  LOAD_FAST                'idx'
             5626  BINARY_SUBSCR    
             5628  LOAD_STR                 'og'
             5630  COMPARE_OP               ==
         5632_5634  POP_JUMP_IF_FALSE  5614  'to 5614'
             5636  LOAD_FAST                'words'
             5638  LOAD_FAST                'idx'
             5640  LOAD_CONST               1
             5642  BINARY_SUBTRACT  
             5644  BINARY_SUBSCR    
             5646  LOAD_STR                 ''
             5648  COMPARE_OP               ==
         5650_5652  POP_JUMP_IF_FALSE  5614  'to 5614'

 L. 814      5654  LOAD_FAST                'words'
             5656  LOAD_FAST                'idx'
             5658  LOAD_CONST               1
             5660  BINARY_ADD       
             5662  BINARY_SUBSCR    
             5664  LOAD_STR                 ''
             5666  COMPARE_OP               ==
         5668_5670  POP_JUMP_IF_FALSE  5614  'to 5614'

 L. 815      5672  LOAD_STR                 ''
             5674  LOAD_FAST                'words'
             5676  LOAD_FAST                'idx'
             5678  STORE_SUBSCR     
         5680_5682  JUMP_BACK          5614  'to 5614'
             5684  POP_BLOCK        
           5686_0  COME_FROM_LOOP     5604  '5604'

 L. 817      5686  LOAD_STR                 ' '
             5688  LOAD_METHOD              join
             5690  LOAD_FAST                'words'
             5692  CALL_METHOD_1         1  '1 positional argument'
             5694  STORE_FAST               'resultStr'

 L. 818      5696  LOAD_STR                 ' '
             5698  LOAD_METHOD              join
             5700  LOAD_FAST                'resultStr'
             5702  LOAD_METHOD              split
             5704  CALL_METHOD_0         0  '0 positional arguments'
             5706  CALL_METHOD_1         1  '1 positional argument'
             5708  STORE_FAST               'resultStr'

 L. 820      5710  LOAD_FAST                'extractedDate'
             5712  LOAD_FAST                'resultStr'
             5714  BUILD_LIST_2          2 
             5716  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 1524_1526


def isFractional_da(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.lower().startswith('halv'):
        return 0.5
    else:
        if input_str.lower() == 'trediedel':
            return 0.3333333333333333
        if input_str.endswith('del'):
            input_str = input_str[:len(input_str) - 3]
            if input_str.lower() in da_numbers:
                return 1.0 / da_numbers[input_str.lower()]
    return False


def isOrdinal_da(input_str):
    """
    This function takes the given text and checks if it is an ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (float): False if not an ordinal, otherwise the number
        corresponding to the ordinal

    ordinals for 1, 3, 7 and 8 are irregular

    only works for ordinals corresponding to the numbers in da_numbers

    """
    lowerstr = input_str.lower()
    if lowerstr.startswith('første'):
        return 1
    if lowerstr.startswith('anden'):
        return 2
    if lowerstr.startswith('tredie'):
        return 3
    if lowerstr.startswith('fjerde'):
        return 4
    if lowerstr.startswith('femte'):
        return 5
    if lowerstr.startswith('sjette'):
        return 6
    if lowerstr.startswith('elfte'):
        return 1
    if lowerstr.startswith('tolvfte'):
        return 12
    if lowerstr[-3:] == 'nde':
        lowerstr = lowerstr[:-3]
        if lowerstr in da_numbers:
            return da_numbers[lowerstr]
    if lowerstr[-4:] in ('ende', ):
        lowerstr = lowerstr[:-4]
        if lowerstr in da_numbers:
            return da_numbers[lowerstr]
    if lowerstr[-2:] == 'te':
        lowerstr = lowerstr[:-2]
        if lowerstr in da_numbers:
            return da_numbers[lowerstr]
    return False


def normalize_da(text, remove_articles):
    """ German string normalization """
    words = text.split()
    normalized = ''
    for word in words:
        if remove_articles:
            if word in ('den', 'det'):
                continue
        if word in da_numbers:
            word = str(da_numbers[word])
        normalized += ' ' + word

    return normalized[1:]


def extract_numbers_da(text, short_scale=True, ordinals=False):
    """
        Takes in a string and extracts a list of numbers.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): Use "short scale" or "long scale" for large
            numbers -- over a million.  The default is short scale, which
            is now common in most English speaking countries.
            See https://en.wikipedia.org/wiki/Names_of_large_numbers
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
    Returns:
        list: list of extracted numbers as floats
    """
    return extract_numbers_generic(text, pronounce_number_da, extractnumber_da, short_scale=short_scale,
      ordinals=ordinals)