# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_de.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 34523 bytes
from datetime import datetime
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions, extract_numbers_generic
from lingua_franca.lang.format_de import pronounce_number_de
de_numbers = {'null':0, 
 'ein':1, 
 'eins':1, 
 'eine':1, 
 'einer':1, 
 'einem':1, 
 'einen':1, 
 'eines':1, 
 'zwei':2, 
 'drei':3, 
 'vier':4, 
 'fünf':5, 
 'sechs':6, 
 'sieben':7, 
 'acht':8, 
 'neun':9, 
 'zehn':10, 
 'elf':11, 
 'zwölf':12, 
 'dreizehn':13, 
 'vierzehn':14, 
 'fünfzehn':15, 
 'sechzehn':16, 
 'siebzehn':17, 
 'achtzehn':18, 
 'neunzehn':19, 
 'zwanzig':20, 
 'einundzwanzig':21, 
 'zweiundzwanzig':22, 
 'dreiundzwanzig':23, 
 'vierundzwanzig':24, 
 'fünfundzwanzig':25, 
 'sechsundzwanzig':26, 
 'siebenundzwanzig':27, 
 'achtundzwanzig':28, 
 'neunundzwanzig':29, 
 'dreißig':30, 
 'einunddreißig':31, 
 'vierzig':40, 
 'fünfzig':50, 
 'sechzig':60, 
 'siebzig':70, 
 'achtzig':80, 
 'neunzig':90, 
 'hundert':100, 
 'zweihundert':200, 
 'dreihundert':300, 
 'vierhundert':400, 
 'fünfhundert':500, 
 'sechshundert':600, 
 'siebenhundert':700, 
 'achthundert':800, 
 'neunhundert':900, 
 'tausend':1000, 
 'million':1000000}

def extractnumber_de(text, short_scale=True, ordinals=False):
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
    aWords = [word for word in aWords if word not in ('der', 'die', 'das', 'des', 'den',
                                                      'dem')]
    and_pass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            val = float(word)
        else:
            if isFractional_de(word):
                val = isFractional_de(word)
            else:
                if isOrdinal_de(word):
                    val = isOrdinal_de(word)
                else:
                    if word in de_numbers:
                        val = de_numbers[word]
                        if count < len(aWords) - 1:
                            wordNext = aWords[(count + 1)]
                        else:
                            wordNext = ''
                        valNext = isFractional_de(wordNext)
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
            if count + 1 < len(aWords) and aWords[(count + 1)] == 'und':
                and_pass = True
                valPreAnd = val
                val = False
                count += 2
                continue
            else:
                if count + 2 < len(aWords):
                    if aWords[(count + 2)] == 'und':
                        and_pass = True
                        valPreAnd = val
                        val = False
                        count += 3
                        continue
                break

    return val or False


def extract_datetime_de--- This code section failed: ---

 L. 168         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_de.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 191         8  LOAD_CLOSURE             'datestr'
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
               34  LOAD_STR                 'extract_datetime_de.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 201        40  LOAD_FAST                'string'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'currentDate'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 202        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 204        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 205        60  LOAD_CONST               False
               62  STORE_FAST               'daySpecified'

 L. 206        64  LOAD_CONST               False
               66  STORE_DEREF              'dayOffset'

 L. 207        68  LOAD_CONST               0
               70  STORE_DEREF              'monthOffset'

 L. 208        72  LOAD_CONST               0
               74  STORE_DEREF              'yearOffset'

 L. 209        76  LOAD_FAST                'currentDate'
               78  STORE_FAST               'dateNow'

 L. 210        80  LOAD_FAST                'dateNow'
               82  LOAD_METHOD              strftime
               84  LOAD_STR                 '%w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'today'

 L. 211        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%Y'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'currentYear'

 L. 212       100  LOAD_CONST               False
              102  STORE_FAST               'fromFlag'

 L. 213       104  LOAD_STR                 ''
              106  STORE_DEREF              'datestr'

 L. 214       108  LOAD_CONST               False
              110  STORE_FAST               'hasYear'

 L. 215       112  LOAD_STR                 ''
              114  STORE_FAST               'timeQualifier'

 L. 217       116  LOAD_STR                 'früh'
              118  LOAD_STR                 'morgens'
              120  LOAD_STR                 'vormittag'
              122  LOAD_STR                 'vormittags'

 L. 218       124  LOAD_STR                 'nachmittag'
              126  LOAD_STR                 'nachmittags'
              128  LOAD_STR                 'abend'
              130  LOAD_STR                 'abends'

 L. 219       132  LOAD_STR                 'nachts'
              134  BUILD_LIST_9          9 
              136  STORE_FAST               'timeQualifiersList'

 L. 220       138  LOAD_STR                 'in'
              140  LOAD_STR                 'am'
              142  LOAD_STR                 'gegen'
              144  LOAD_STR                 'bis'
              146  LOAD_STR                 'für'
              148  BUILD_LIST_5          5 
              150  STORE_FAST               'markers'

 L. 221       152  LOAD_STR                 'montag'
              154  LOAD_STR                 'dienstag'
              156  LOAD_STR                 'mittwoch'

 L. 222       158  LOAD_STR                 'donnerstag'
              160  LOAD_STR                 'freitag'
              162  LOAD_STR                 'samstag'
              164  LOAD_STR                 'sonntag'
              166  BUILD_LIST_7          7 
              168  STORE_FAST               'days'

 L. 223       170  LOAD_STR                 'januar'
              172  LOAD_STR                 'februar'
              174  LOAD_STR                 'märz'
              176  LOAD_STR                 'april'
              178  LOAD_STR                 'mai'
              180  LOAD_STR                 'juni'

 L. 224       182  LOAD_STR                 'juli'
              184  LOAD_STR                 'august'
              186  LOAD_STR                 'september'
              188  LOAD_STR                 'october'
              190  LOAD_STR                 'november'

 L. 225       192  LOAD_STR                 'dezember'
              194  BUILD_LIST_12        12 
              196  STORE_FAST               'months'

 L. 226       198  LOAD_STR                 'jan'
              200  LOAD_STR                 'feb'
              202  LOAD_STR                 'mär'
              204  LOAD_STR                 'apr'
              206  LOAD_STR                 'mai'
              208  LOAD_STR                 'juni'
              210  LOAD_STR                 'juli'
              212  LOAD_STR                 'aug'

 L. 227       214  LOAD_STR                 'sept'
              216  LOAD_STR                 'oct'
              218  LOAD_STR                 'nov'
              220  LOAD_STR                 'dez'
              222  BUILD_LIST_12        12 
              224  STORE_FAST               'monthsShort'

 L. 229       226  LOAD_FAST                'days'
              228  LOAD_FAST                'months'
              230  BINARY_ADD       
              232  LOAD_FAST                'monthsShort'
              234  BINARY_ADD       
              236  STORE_FAST               'validFollowups'

 L. 230       238  LOAD_FAST                'validFollowups'
              240  LOAD_METHOD              append
              242  LOAD_STR                 'heute'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  POP_TOP          

 L. 231       248  LOAD_FAST                'validFollowups'
              250  LOAD_METHOD              append
              252  LOAD_STR                 'morgen'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  POP_TOP          

 L. 232       258  LOAD_FAST                'validFollowups'
              260  LOAD_METHOD              append
              262  LOAD_STR                 'nächste'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          

 L. 233       268  LOAD_FAST                'validFollowups'
              270  LOAD_METHOD              append
              272  LOAD_STR                 'nächster'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  POP_TOP          

 L. 234       278  LOAD_FAST                'validFollowups'
              280  LOAD_METHOD              append
              282  LOAD_STR                 'nächstes'
              284  CALL_METHOD_1         1  '1 positional argument'
              286  POP_TOP          

 L. 235       288  LOAD_FAST                'validFollowups'
              290  LOAD_METHOD              append
              292  LOAD_STR                 'nächsten'
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          

 L. 236       298  LOAD_FAST                'validFollowups'
              300  LOAD_METHOD              append
              302  LOAD_STR                 'nächstem'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  POP_TOP          

 L. 237       308  LOAD_FAST                'validFollowups'
              310  LOAD_METHOD              append
              312  LOAD_STR                 'letzte'
              314  CALL_METHOD_1         1  '1 positional argument'
              316  POP_TOP          

 L. 238       318  LOAD_FAST                'validFollowups'
              320  LOAD_METHOD              append
              322  LOAD_STR                 'letzter'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  POP_TOP          

 L. 239       328  LOAD_FAST                'validFollowups'
              330  LOAD_METHOD              append
              332  LOAD_STR                 'letztes'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          

 L. 240       338  LOAD_FAST                'validFollowups'
              340  LOAD_METHOD              append
              342  LOAD_STR                 'letzten'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  POP_TOP          

 L. 241       348  LOAD_FAST                'validFollowups'
              350  LOAD_METHOD              append
              352  LOAD_STR                 'letztem'
              354  CALL_METHOD_1         1  '1 positional argument'
              356  POP_TOP          

 L. 242       358  LOAD_FAST                'validFollowups'
              360  LOAD_METHOD              append
              362  LOAD_STR                 'jetzt'
              364  CALL_METHOD_1         1  '1 positional argument'
              366  POP_TOP          

 L. 244       368  LOAD_FAST                'clean_string'
              370  LOAD_FAST                'string'
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  STORE_FAST               'words'

 L. 246   376_378  SETUP_LOOP         2202  'to 2202'
              380  LOAD_GLOBAL              enumerate
              382  LOAD_FAST                'words'
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  GET_ITER         
            388_0  COME_FROM          2056  '2056'
          388_390  FOR_ITER           2200  'to 2200'
              392  UNPACK_SEQUENCE_2     2 
              394  STORE_FAST               'idx'
              396  STORE_FAST               'word'

 L. 247       398  LOAD_FAST                'word'
              400  LOAD_STR                 ''
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   412  'to 412'

 L. 248   408_410  CONTINUE            388  'to 388'
            412_0  COME_FROM           404  '404'

 L. 249       412  LOAD_FAST                'idx'
              414  LOAD_CONST               1
              416  COMPARE_OP               >
          418_420  POP_JUMP_IF_FALSE   434  'to 434'
              422  LOAD_FAST                'words'
              424  LOAD_FAST                'idx'
              426  LOAD_CONST               2
              428  BINARY_SUBTRACT  
              430  BINARY_SUBSCR    
              432  JUMP_FORWARD        436  'to 436'
            434_0  COME_FROM           418  '418'
              434  LOAD_STR                 ''
            436_0  COME_FROM           432  '432'
              436  STORE_FAST               'wordPrevPrev'

 L. 250       438  LOAD_FAST                'idx'
              440  LOAD_CONST               0
              442  COMPARE_OP               >
          444_446  POP_JUMP_IF_FALSE   460  'to 460'
              448  LOAD_FAST                'words'
              450  LOAD_FAST                'idx'
              452  LOAD_CONST               1
              454  BINARY_SUBTRACT  
              456  BINARY_SUBSCR    
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           444  '444'
              460  LOAD_STR                 ''
            462_0  COME_FROM           458  '458'
              462  STORE_FAST               'wordPrev'

 L. 251       464  LOAD_FAST                'idx'
              466  LOAD_CONST               1
              468  BINARY_ADD       
              470  LOAD_GLOBAL              len
              472  LOAD_FAST                'words'
              474  CALL_FUNCTION_1       1  '1 positional argument'
              476  COMPARE_OP               <
          478_480  POP_JUMP_IF_FALSE   494  'to 494'
              482  LOAD_FAST                'words'
              484  LOAD_FAST                'idx'
              486  LOAD_CONST               1
              488  BINARY_ADD       
              490  BINARY_SUBSCR    
              492  JUMP_FORWARD        496  'to 496'
            494_0  COME_FROM           478  '478'
              494  LOAD_STR                 ''
            496_0  COME_FROM           492  '492'
              496  STORE_FAST               'wordNext'

 L. 252       498  LOAD_FAST                'idx'
              500  LOAD_CONST               2
              502  BINARY_ADD       
              504  LOAD_GLOBAL              len
              506  LOAD_FAST                'words'
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  COMPARE_OP               <
          512_514  POP_JUMP_IF_FALSE   528  'to 528'
              516  LOAD_FAST                'words'
              518  LOAD_FAST                'idx'
              520  LOAD_CONST               2
              522  BINARY_ADD       
              524  BINARY_SUBSCR    
              526  JUMP_FORWARD        530  'to 530'
            528_0  COME_FROM           512  '512'
              528  LOAD_STR                 ''
            530_0  COME_FROM           526  '526'
              530  STORE_FAST               'wordNextNext'

 L. 256       532  LOAD_FAST                'word'
              534  LOAD_STR                 'morgen'
              536  COMPARE_OP               !=
          538_540  POP_JUMP_IF_FALSE   582  'to 582'
              542  LOAD_FAST                'word'
              544  LOAD_STR                 'übermorgen'
              546  COMPARE_OP               !=
          548_550  POP_JUMP_IF_FALSE   582  'to 582'

 L. 257       552  LOAD_FAST                'word'
              554  LOAD_CONST               -2
              556  LOAD_CONST               None
              558  BUILD_SLICE_2         2 
              560  BINARY_SUBSCR    
              562  LOAD_STR                 'en'
              564  COMPARE_OP               ==
          566_568  POP_JUMP_IF_FALSE   582  'to 582'

 L. 258       570  LOAD_FAST                'word'
              572  LOAD_CONST               None
              574  LOAD_CONST               -2
              576  BUILD_SLICE_2         2 
              578  BINARY_SUBSCR    
              580  STORE_FAST               'word'
            582_0  COME_FROM           566  '566'
            582_1  COME_FROM           548  '548'
            582_2  COME_FROM           538  '538'

 L. 259       582  LOAD_FAST                'word'
              584  LOAD_STR                 'heute'
              586  COMPARE_OP               !=
          588_590  POP_JUMP_IF_FALSE   622  'to 622'

 L. 260       592  LOAD_FAST                'word'
              594  LOAD_CONST               -1
              596  LOAD_CONST               None
              598  BUILD_SLICE_2         2 
              600  BINARY_SUBSCR    
              602  LOAD_STR                 'e'
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE   622  'to 622'

 L. 261       610  LOAD_FAST                'word'
              612  LOAD_CONST               None
              614  LOAD_CONST               -1
              616  BUILD_SLICE_2         2 
              618  BINARY_SUBSCR    
              620  STORE_FAST               'word'
            622_0  COME_FROM           606  '606'
            622_1  COME_FROM           588  '588'

 L. 263       622  LOAD_FAST                'idx'
              624  STORE_FAST               'start'

 L. 264       626  LOAD_CONST               0
              628  STORE_FAST               'used'

 L. 266       630  LOAD_FAST                'word'
              632  LOAD_FAST                'timeQualifiersList'
              634  COMPARE_OP               in
          636_638  POP_JUMP_IF_FALSE   648  'to 648'

 L. 267       640  LOAD_FAST                'word'
              642  STORE_FAST               'timeQualifier'
          644_646  JUMP_FORWARD       1754  'to 1754'
            648_0  COME_FROM           636  '636'

 L. 269       648  LOAD_FAST                'word'
              650  LOAD_STR                 'heute'
              652  COMPARE_OP               ==
          654_656  POP_JUMP_IF_FALSE   680  'to 680'
              658  LOAD_FAST                'fromFlag'
          660_662  POP_JUMP_IF_TRUE    680  'to 680'

 L. 270       664  LOAD_CONST               0
              666  STORE_DEREF              'dayOffset'

 L. 271       668  LOAD_FAST                'used'
              670  LOAD_CONST               1
              672  INPLACE_ADD      
              674  STORE_FAST               'used'
          676_678  JUMP_FORWARD       1754  'to 1754'
            680_0  COME_FROM           660  '660'
            680_1  COME_FROM           654  '654'

 L. 272       680  LOAD_FAST                'word'
              682  LOAD_STR                 'morgen'
              684  COMPARE_OP               ==
          686_688  POP_JUMP_IF_FALSE   732  'to 732'
              690  LOAD_FAST                'fromFlag'
          692_694  POP_JUMP_IF_TRUE    732  'to 732'
              696  LOAD_FAST                'wordPrev'
              698  LOAD_STR                 'am'
              700  COMPARE_OP               !=
          702_704  POP_JUMP_IF_FALSE   732  'to 732'

 L. 273       706  LOAD_FAST                'wordPrev'
              708  LOAD_FAST                'days'
              710  COMPARE_OP               not-in
          712_714  POP_JUMP_IF_FALSE   732  'to 732'

 L. 275       716  LOAD_CONST               1
              718  STORE_DEREF              'dayOffset'

 L. 276       720  LOAD_FAST                'used'
              722  LOAD_CONST               1
              724  INPLACE_ADD      
              726  STORE_FAST               'used'
          728_730  JUMP_FORWARD       1754  'to 1754'
            732_0  COME_FROM           712  '712'
            732_1  COME_FROM           702  '702'
            732_2  COME_FROM           692  '692'
            732_3  COME_FROM           686  '686'

 L. 277       732  LOAD_FAST                'word'
              734  LOAD_STR                 'übermorgen'
              736  COMPARE_OP               ==
          738_740  POP_JUMP_IF_FALSE   764  'to 764'
              742  LOAD_FAST                'fromFlag'
          744_746  POP_JUMP_IF_TRUE    764  'to 764'

 L. 278       748  LOAD_CONST               2
              750  STORE_DEREF              'dayOffset'

 L. 279       752  LOAD_FAST                'used'
              754  LOAD_CONST               1
              756  INPLACE_ADD      
              758  STORE_FAST               'used'
          760_762  JUMP_FORWARD       1754  'to 1754'
            764_0  COME_FROM           744  '744'
            764_1  COME_FROM           738  '738'

 L. 281       764  LOAD_FAST                'word'
              766  LOAD_STR                 'tag'
              768  COMPARE_OP               ==
          770_772  POP_JUMP_IF_TRUE    784  'to 784'
              774  LOAD_FAST                'word'
              776  LOAD_STR                 'tage'
              778  COMPARE_OP               ==
          780_782  POP_JUMP_IF_FALSE   826  'to 826'
            784_0  COME_FROM           770  '770'

 L. 282       784  LOAD_FAST                'wordPrev'
              786  LOAD_CONST               0
              788  BINARY_SUBSCR    
              790  LOAD_METHOD              isdigit
              792  CALL_METHOD_0         0  '0 positional arguments'
          794_796  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 283       798  LOAD_DEREF               'dayOffset'
              800  LOAD_GLOBAL              int
              802  LOAD_FAST                'wordPrev'
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  INPLACE_ADD      
              808  STORE_DEREF              'dayOffset'

 L. 284       810  LOAD_FAST                'start'
              812  LOAD_CONST               1
              814  INPLACE_SUBTRACT 
              816  STORE_FAST               'start'

 L. 285       818  LOAD_CONST               2
              820  STORE_FAST               'used'
          822_824  JUMP_FORWARD       1754  'to 1754'
            826_0  COME_FROM           780  '780'

 L. 286       826  LOAD_FAST                'word'
              828  LOAD_STR                 'woch'
              830  COMPARE_OP               ==
          832_834  POP_JUMP_IF_FALSE   960  'to 960'
              836  LOAD_FAST                'fromFlag'
          838_840  POP_JUMP_IF_TRUE    960  'to 960'

 L. 287       842  LOAD_FAST                'wordPrev'
              844  LOAD_CONST               0
              846  BINARY_SUBSCR    
              848  LOAD_METHOD              isdigit
              850  CALL_METHOD_0         0  '0 positional arguments'
          852_854  POP_JUMP_IF_FALSE   886  'to 886'

 L. 288       856  LOAD_DEREF               'dayOffset'
              858  LOAD_GLOBAL              int
              860  LOAD_FAST                'wordPrev'
              862  CALL_FUNCTION_1       1  '1 positional argument'
              864  LOAD_CONST               7
              866  BINARY_MULTIPLY  
              868  INPLACE_ADD      
              870  STORE_DEREF              'dayOffset'

 L. 289       872  LOAD_FAST                'start'
              874  LOAD_CONST               1
              876  INPLACE_SUBTRACT 
              878  STORE_FAST               'start'

 L. 290       880  LOAD_CONST               2
              882  STORE_FAST               'used'
              884  JUMP_FORWARD       1754  'to 1754'
            886_0  COME_FROM           852  '852'

 L. 291       886  LOAD_FAST                'wordPrev'
              888  LOAD_CONST               None
              890  LOAD_CONST               6
              892  BUILD_SLICE_2         2 
              894  BINARY_SUBSCR    
              896  LOAD_STR                 'nächst'
              898  COMPARE_OP               ==
          900_902  POP_JUMP_IF_FALSE   922  'to 922'

 L. 292       904  LOAD_CONST               7
              906  STORE_DEREF              'dayOffset'

 L. 293       908  LOAD_FAST                'start'
              910  LOAD_CONST               1
              912  INPLACE_SUBTRACT 
              914  STORE_FAST               'start'

 L. 294       916  LOAD_CONST               2
              918  STORE_FAST               'used'
              920  JUMP_FORWARD       1754  'to 1754'
            922_0  COME_FROM           900  '900'

 L. 295       922  LOAD_FAST                'wordPrev'
              924  LOAD_CONST               None
              926  LOAD_CONST               5
              928  BUILD_SLICE_2         2 
              930  BINARY_SUBSCR    
              932  LOAD_STR                 'letzt'
              934  COMPARE_OP               ==
          936_938  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 296       940  LOAD_CONST               -7
              942  STORE_DEREF              'dayOffset'

 L. 297       944  LOAD_FAST                'start'
              946  LOAD_CONST               1
              948  INPLACE_SUBTRACT 
              950  STORE_FAST               'start'

 L. 298       952  LOAD_CONST               2
              954  STORE_FAST               'used'
          956_958  JUMP_FORWARD       1754  'to 1754'
            960_0  COME_FROM           838  '838'
            960_1  COME_FROM           832  '832'

 L. 300       960  LOAD_FAST                'word'
              962  LOAD_STR                 'monat'
              964  COMPARE_OP               ==
          966_968  POP_JUMP_IF_FALSE  1086  'to 1086'
              970  LOAD_FAST                'fromFlag'
          972_974  POP_JUMP_IF_TRUE   1086  'to 1086'

 L. 301       976  LOAD_FAST                'wordPrev'
              978  LOAD_CONST               0
              980  BINARY_SUBSCR    
              982  LOAD_METHOD              isdigit
              984  CALL_METHOD_0         0  '0 positional arguments'
          986_988  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 302       990  LOAD_GLOBAL              int
              992  LOAD_FAST                'wordPrev'
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  STORE_DEREF              'monthOffset'

 L. 303       998  LOAD_FAST                'start'
             1000  LOAD_CONST               1
             1002  INPLACE_SUBTRACT 
             1004  STORE_FAST               'start'

 L. 304      1006  LOAD_CONST               2
             1008  STORE_FAST               'used'
             1010  JUMP_FORWARD       1754  'to 1754'
           1012_0  COME_FROM           986  '986'

 L. 305      1012  LOAD_FAST                'wordPrev'
             1014  LOAD_CONST               None
             1016  LOAD_CONST               6
             1018  BUILD_SLICE_2         2 
             1020  BINARY_SUBSCR    
             1022  LOAD_STR                 'nächst'
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 306      1030  LOAD_CONST               1
             1032  STORE_DEREF              'monthOffset'

 L. 307      1034  LOAD_FAST                'start'
             1036  LOAD_CONST               1
             1038  INPLACE_SUBTRACT 
             1040  STORE_FAST               'start'

 L. 308      1042  LOAD_CONST               2
             1044  STORE_FAST               'used'
             1046  JUMP_FORWARD       1754  'to 1754'
           1048_0  COME_FROM          1026  '1026'

 L. 309      1048  LOAD_FAST                'wordPrev'
             1050  LOAD_CONST               None
             1052  LOAD_CONST               5
             1054  BUILD_SLICE_2         2 
             1056  BINARY_SUBSCR    
             1058  LOAD_STR                 'letzt'
             1060  COMPARE_OP               ==
         1062_1064  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 310      1066  LOAD_CONST               -1
             1068  STORE_DEREF              'monthOffset'

 L. 311      1070  LOAD_FAST                'start'
             1072  LOAD_CONST               1
             1074  INPLACE_SUBTRACT 
             1076  STORE_FAST               'start'

 L. 312      1078  LOAD_CONST               2
             1080  STORE_FAST               'used'
         1082_1084  JUMP_FORWARD       1754  'to 1754'
           1086_0  COME_FROM           972  '972'
           1086_1  COME_FROM           966  '966'

 L. 314      1086  LOAD_FAST                'word'
             1088  LOAD_STR                 'jahr'
             1090  COMPARE_OP               ==
         1092_1094  POP_JUMP_IF_FALSE  1212  'to 1212'
             1096  LOAD_FAST                'fromFlag'
         1098_1100  POP_JUMP_IF_TRUE   1212  'to 1212'

 L. 315      1102  LOAD_FAST                'wordPrev'
             1104  LOAD_CONST               0
             1106  BINARY_SUBSCR    
             1108  LOAD_METHOD              isdigit
             1110  CALL_METHOD_0         0  '0 positional arguments'
         1112_1114  POP_JUMP_IF_FALSE  1138  'to 1138'

 L. 316      1116  LOAD_GLOBAL              int
             1118  LOAD_FAST                'wordPrev'
             1120  CALL_FUNCTION_1       1  '1 positional argument'
             1122  STORE_DEREF              'yearOffset'

 L. 317      1124  LOAD_FAST                'start'
             1126  LOAD_CONST               1
             1128  INPLACE_SUBTRACT 
             1130  STORE_FAST               'start'

 L. 318      1132  LOAD_CONST               2
             1134  STORE_FAST               'used'
             1136  JUMP_FORWARD       1754  'to 1754'
           1138_0  COME_FROM          1112  '1112'

 L. 319      1138  LOAD_FAST                'wordPrev'
             1140  LOAD_CONST               None
             1142  LOAD_CONST               6
             1144  BUILD_SLICE_2         2 
             1146  BINARY_SUBSCR    
             1148  LOAD_STR                 'nächst'
             1150  COMPARE_OP               ==
         1152_1154  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 320      1156  LOAD_CONST               1
             1158  STORE_DEREF              'yearOffset'

 L. 321      1160  LOAD_FAST                'start'
             1162  LOAD_CONST               1
             1164  INPLACE_SUBTRACT 
             1166  STORE_FAST               'start'

 L. 322      1168  LOAD_CONST               2
             1170  STORE_FAST               'used'
             1172  JUMP_FORWARD       1754  'to 1754'
           1174_0  COME_FROM          1152  '1152'

 L. 323      1174  LOAD_FAST                'wordPrev'
             1176  LOAD_CONST               None
             1178  LOAD_CONST               6
             1180  BUILD_SLICE_2         2 
             1182  BINARY_SUBSCR    
             1184  LOAD_STR                 'nächst'
             1186  COMPARE_OP               ==
         1188_1190  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 324      1192  LOAD_CONST               -1
             1194  STORE_DEREF              'yearOffset'

 L. 325      1196  LOAD_FAST                'start'
             1198  LOAD_CONST               1
             1200  INPLACE_SUBTRACT 
             1202  STORE_FAST               'start'

 L. 326      1204  LOAD_CONST               2
             1206  STORE_FAST               'used'
         1208_1210  JUMP_FORWARD       1754  'to 1754'
           1212_0  COME_FROM          1098  '1098'
           1212_1  COME_FROM          1092  '1092'

 L. 329      1212  LOAD_FAST                'word'
             1214  LOAD_FAST                'days'
             1216  COMPARE_OP               in
         1218_1220  POP_JUMP_IF_FALSE  1388  'to 1388'
             1222  LOAD_FAST                'fromFlag'
         1224_1226  POP_JUMP_IF_TRUE   1388  'to 1388'

 L. 330      1228  LOAD_FAST                'days'
             1230  LOAD_METHOD              index
             1232  LOAD_FAST                'word'
             1234  CALL_METHOD_1         1  '1 positional argument'
             1236  STORE_FAST               'd'

 L. 331      1238  LOAD_FAST                'd'
             1240  LOAD_CONST               1
             1242  BINARY_ADD       
             1244  LOAD_GLOBAL              int
             1246  LOAD_FAST                'today'
             1248  CALL_FUNCTION_1       1  '1 positional argument'
             1250  BINARY_SUBTRACT  
             1252  STORE_DEREF              'dayOffset'

 L. 332      1254  LOAD_CONST               1
             1256  STORE_FAST               'used'

 L. 333      1258  LOAD_DEREF               'dayOffset'
             1260  LOAD_CONST               0
             1262  COMPARE_OP               <
         1264_1266  POP_JUMP_IF_FALSE  1276  'to 1276'

 L. 334      1268  LOAD_DEREF               'dayOffset'
             1270  LOAD_CONST               7
             1272  INPLACE_ADD      
             1274  STORE_DEREF              'dayOffset'
           1276_0  COME_FROM          1264  '1264'

 L. 335      1276  LOAD_FAST                'wordNext'
             1278  LOAD_STR                 'morgen'
             1280  COMPARE_OP               ==
         1282_1284  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 337      1286  LOAD_STR                 'früh'
             1288  LOAD_FAST                'words'
             1290  LOAD_FAST                'idx'
             1292  LOAD_CONST               1
             1294  BINARY_ADD       
             1296  STORE_SUBSCR     
           1298_0  COME_FROM          1282  '1282'

 L. 338      1298  LOAD_FAST                'wordPrev'
             1300  LOAD_CONST               None
             1302  LOAD_CONST               6
             1304  BUILD_SLICE_2         2 
             1306  BINARY_SUBSCR    
             1308  LOAD_STR                 'nächst'
             1310  COMPARE_OP               ==
         1312_1314  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 339      1316  LOAD_DEREF               'dayOffset'
             1318  LOAD_CONST               7
             1320  INPLACE_ADD      
             1322  STORE_DEREF              'dayOffset'

 L. 340      1324  LOAD_FAST                'used'
             1326  LOAD_CONST               1
             1328  INPLACE_ADD      
             1330  STORE_FAST               'used'

 L. 341      1332  LOAD_FAST                'start'
             1334  LOAD_CONST               1
             1336  INPLACE_SUBTRACT 
             1338  STORE_FAST               'start'
             1340  JUMP_FORWARD       1754  'to 1754'
           1342_0  COME_FROM          1312  '1312'

 L. 342      1342  LOAD_FAST                'wordPrev'
             1344  LOAD_CONST               None
             1346  LOAD_CONST               5
             1348  BUILD_SLICE_2         2 
             1350  BINARY_SUBSCR    
             1352  LOAD_STR                 'letzt'
             1354  COMPARE_OP               ==
         1356_1358  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 343      1360  LOAD_DEREF               'dayOffset'
             1362  LOAD_CONST               7
             1364  INPLACE_SUBTRACT 
             1366  STORE_DEREF              'dayOffset'

 L. 344      1368  LOAD_FAST                'used'
             1370  LOAD_CONST               1
             1372  INPLACE_ADD      
             1374  STORE_FAST               'used'

 L. 345      1376  LOAD_FAST                'start'
             1378  LOAD_CONST               1
             1380  INPLACE_SUBTRACT 
             1382  STORE_FAST               'start'
         1384_1386  JUMP_FORWARD       1754  'to 1754'
           1388_0  COME_FROM          1224  '1224'
           1388_1  COME_FROM          1218  '1218'

 L. 347      1388  LOAD_FAST                'word'
             1390  LOAD_FAST                'months'
             1392  COMPARE_OP               in
         1394_1396  POP_JUMP_IF_TRUE   1414  'to 1414'
             1398  LOAD_FAST                'word'
             1400  LOAD_FAST                'monthsShort'
             1402  COMPARE_OP               in
         1404_1406  POP_JUMP_IF_FALSE  1754  'to 1754'
             1408  LOAD_FAST                'fromFlag'
         1410_1412  POP_JUMP_IF_TRUE   1754  'to 1754'
           1414_0  COME_FROM          1394  '1394'

 L. 348      1414  SETUP_EXCEPT       1430  'to 1430'

 L. 349      1416  LOAD_FAST                'months'
             1418  LOAD_METHOD              index
             1420  LOAD_FAST                'word'
             1422  CALL_METHOD_1         1  '1 positional argument'
             1424  STORE_FAST               'm'
             1426  POP_BLOCK        
             1428  JUMP_FORWARD       1462  'to 1462'
           1430_0  COME_FROM_EXCEPT   1414  '1414'

 L. 350      1430  DUP_TOP          
             1432  LOAD_GLOBAL              ValueError
             1434  COMPARE_OP               exception-match
         1436_1438  POP_JUMP_IF_FALSE  1460  'to 1460'
             1440  POP_TOP          
             1442  POP_TOP          
             1444  POP_TOP          

 L. 351      1446  LOAD_FAST                'monthsShort'
             1448  LOAD_METHOD              index
             1450  LOAD_FAST                'word'
             1452  CALL_METHOD_1         1  '1 positional argument'
             1454  STORE_FAST               'm'
             1456  POP_EXCEPT       
             1458  JUMP_FORWARD       1462  'to 1462'
           1460_0  COME_FROM          1436  '1436'
             1460  END_FINALLY      
           1462_0  COME_FROM          1458  '1458'
           1462_1  COME_FROM          1428  '1428'

 L. 352      1462  LOAD_FAST                'used'
             1464  LOAD_CONST               1
             1466  INPLACE_ADD      
             1468  STORE_FAST               'used'

 L. 353      1470  LOAD_FAST                'months'
             1472  LOAD_FAST                'm'
             1474  BINARY_SUBSCR    
             1476  STORE_DEREF              'datestr'

 L. 354      1478  LOAD_FAST                'wordPrev'
         1480_1482  POP_JUMP_IF_FALSE  1664  'to 1664'
             1484  LOAD_FAST                'wordPrev'
             1486  LOAD_CONST               0
             1488  BINARY_SUBSCR    
             1490  LOAD_METHOD              isdigit
             1492  CALL_METHOD_0         0  '0 positional arguments'
         1494_1496  POP_JUMP_IF_TRUE   1522  'to 1522'

 L. 355      1498  LOAD_FAST                'wordPrev'
             1500  LOAD_STR                 'of'
             1502  COMPARE_OP               ==
         1504_1506  POP_JUMP_IF_FALSE  1664  'to 1664'
             1508  LOAD_FAST                'wordPrevPrev'
             1510  LOAD_CONST               0
             1512  BINARY_SUBSCR    
             1514  LOAD_METHOD              isdigit
             1516  CALL_METHOD_0         0  '0 positional arguments'
         1518_1520  POP_JUMP_IF_FALSE  1664  'to 1664'
           1522_0  COME_FROM          1494  '1494'

 L. 356      1522  LOAD_FAST                'wordPrev'
             1524  LOAD_STR                 'of'
             1526  COMPARE_OP               ==
         1528_1530  POP_JUMP_IF_FALSE  1584  'to 1584'
             1532  LOAD_FAST                'wordPrevPrev'
             1534  LOAD_CONST               0
             1536  BINARY_SUBSCR    
             1538  LOAD_METHOD              isdigit
             1540  CALL_METHOD_0         0  '0 positional arguments'
         1542_1544  POP_JUMP_IF_FALSE  1584  'to 1584'

 L. 357      1546  LOAD_DEREF               'datestr'
             1548  LOAD_STR                 ' '
             1550  LOAD_FAST                'words'
             1552  LOAD_FAST                'idx'
             1554  LOAD_CONST               2
             1556  BINARY_SUBTRACT  
             1558  BINARY_SUBSCR    
             1560  BINARY_ADD       
             1562  INPLACE_ADD      
             1564  STORE_DEREF              'datestr'

 L. 358      1566  LOAD_FAST                'used'
             1568  LOAD_CONST               1
             1570  INPLACE_ADD      
             1572  STORE_FAST               'used'

 L. 359      1574  LOAD_FAST                'start'
             1576  LOAD_CONST               1
             1578  INPLACE_SUBTRACT 
             1580  STORE_FAST               'start'
             1582  JUMP_FORWARD       1596  'to 1596'
           1584_0  COME_FROM          1542  '1542'
           1584_1  COME_FROM          1528  '1528'

 L. 361      1584  LOAD_DEREF               'datestr'
             1586  LOAD_STR                 ' '
             1588  LOAD_FAST                'wordPrev'
             1590  BINARY_ADD       
             1592  INPLACE_ADD      
             1594  STORE_DEREF              'datestr'
           1596_0  COME_FROM          1582  '1582'

 L. 362      1596  LOAD_FAST                'start'
             1598  LOAD_CONST               1
             1600  INPLACE_SUBTRACT 
             1602  STORE_FAST               'start'

 L. 363      1604  LOAD_FAST                'used'
             1606  LOAD_CONST               1
             1608  INPLACE_ADD      
             1610  STORE_FAST               'used'

 L. 364      1612  LOAD_FAST                'wordNext'
         1614_1616  POP_JUMP_IF_FALSE  1658  'to 1658'
             1618  LOAD_FAST                'wordNext'
             1620  LOAD_CONST               0
             1622  BINARY_SUBSCR    
             1624  LOAD_METHOD              isdigit
             1626  CALL_METHOD_0         0  '0 positional arguments'
         1628_1630  POP_JUMP_IF_FALSE  1658  'to 1658'

 L. 365      1632  LOAD_DEREF               'datestr'
             1634  LOAD_STR                 ' '
             1636  LOAD_FAST                'wordNext'
             1638  BINARY_ADD       
             1640  INPLACE_ADD      
             1642  STORE_DEREF              'datestr'

 L. 366      1644  LOAD_FAST                'used'
             1646  LOAD_CONST               1
             1648  INPLACE_ADD      
             1650  STORE_FAST               'used'

 L. 367      1652  LOAD_CONST               True
             1654  STORE_FAST               'hasYear'
             1656  JUMP_FORWARD       1662  'to 1662'
           1658_0  COME_FROM          1628  '1628'
           1658_1  COME_FROM          1614  '1614'

 L. 369      1658  LOAD_CONST               False
             1660  STORE_FAST               'hasYear'
           1662_0  COME_FROM          1656  '1656'
             1662  JUMP_FORWARD       1754  'to 1754'
           1664_0  COME_FROM          1518  '1518'
           1664_1  COME_FROM          1504  '1504'
           1664_2  COME_FROM          1480  '1480'

 L. 371      1664  LOAD_FAST                'wordNext'
         1666_1668  POP_JUMP_IF_FALSE  1754  'to 1754'
             1670  LOAD_FAST                'wordNext'
             1672  LOAD_CONST               0
             1674  BINARY_SUBSCR    
             1676  LOAD_METHOD              isdigit
             1678  CALL_METHOD_0         0  '0 positional arguments'
           1680_0  COME_FROM          1136  '1136'
           1680_1  COME_FROM          1010  '1010'
           1680_2  COME_FROM           884  '884'
         1680_1682  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 372      1684  LOAD_DEREF               'datestr'
             1686  LOAD_STR                 ' '
             1688  LOAD_FAST                'wordNext'
             1690  BINARY_ADD       
             1692  INPLACE_ADD      
             1694  STORE_DEREF              'datestr'

 L. 373      1696  LOAD_FAST                'used'
             1698  LOAD_CONST               1
             1700  INPLACE_ADD      
             1702  STORE_FAST               'used'

 L. 374      1704  LOAD_FAST                'wordNextNext'
         1706_1708  POP_JUMP_IF_FALSE  1750  'to 1750'
             1710  LOAD_FAST                'wordNextNext'
             1712  LOAD_CONST               0
             1714  BINARY_SUBSCR    
           1716_0  COME_FROM          1172  '1172'
           1716_1  COME_FROM          1046  '1046'
           1716_2  COME_FROM           920  '920'
             1716  LOAD_METHOD              isdigit
             1718  CALL_METHOD_0         0  '0 positional arguments'
         1720_1722  POP_JUMP_IF_FALSE  1750  'to 1750'

 L. 375      1724  LOAD_DEREF               'datestr'
             1726  LOAD_STR                 ' '
             1728  LOAD_FAST                'wordNextNext'
             1730  BINARY_ADD       
             1732  INPLACE_ADD      
             1734  STORE_DEREF              'datestr'

 L. 376      1736  LOAD_FAST                'used'
             1738  LOAD_CONST               1
             1740  INPLACE_ADD      
             1742  STORE_FAST               'used'

 L. 377      1744  LOAD_CONST               True
             1746  STORE_FAST               'hasYear'
             1748  JUMP_FORWARD       1754  'to 1754'
           1750_0  COME_FROM          1720  '1720'
           1750_1  COME_FROM          1706  '1706'

 L. 379      1750  LOAD_CONST               False
             1752  STORE_FAST               'hasYear'
           1754_0  COME_FROM          1748  '1748'
           1754_1  COME_FROM          1680  '1680'
           1754_2  COME_FROM          1666  '1666'
           1754_3  COME_FROM          1662  '1662'
           1754_4  COME_FROM          1410  '1410'
           1754_5  COME_FROM          1404  '1404'
           1754_6  COME_FROM          1384  '1384'
           1754_7  COME_FROM          1356  '1356'
           1754_8  COME_FROM          1208  '1208'
           1754_9  COME_FROM          1188  '1188'
          1754_10  COME_FROM          1082  '1082'
          1754_11  COME_FROM          1062  '1062'
          1754_12  COME_FROM           956  '956'
          1754_13  COME_FROM           936  '936'
          1754_14  COME_FROM           822  '822'
          1754_15  COME_FROM           794  '794'
          1754_16  COME_FROM           760  '760'
          1754_17  COME_FROM           728  '728'
          1754_18  COME_FROM           676  '676'
          1754_19  COME_FROM           644  '644'

 L. 384      1754  LOAD_FAST                'word'
             1756  LOAD_STR                 'von'
             1758  COMPARE_OP               ==
         1760_1762  POP_JUMP_IF_TRUE   1784  'to 1784'
             1764  LOAD_FAST                'word'
             1766  LOAD_STR                 'nach'
             1768  COMPARE_OP               ==
         1770_1772  POP_JUMP_IF_TRUE   1784  'to 1784'
             1774  LOAD_FAST                'word'
             1776  LOAD_STR                 'ab'
             1778  COMPARE_OP               ==
         1780_1782  POP_JUMP_IF_FALSE  2050  'to 2050'
           1784_0  COME_FROM          1770  '1770'
           1784_1  COME_FROM          1760  '1760'
             1784  LOAD_FAST                'wordNext'

 L. 385      1786  LOAD_FAST                'validFollowups'
             1788  COMPARE_OP               in
         1790_1792  POP_JUMP_IF_FALSE  2050  'to 2050'

 L. 386      1794  LOAD_CONST               2
             1796  STORE_FAST               'used'

 L. 387      1798  LOAD_CONST               True
             1800  STORE_FAST               'fromFlag'

 L. 388      1802  LOAD_FAST                'wordNext'
             1804  LOAD_STR                 'morgen'
             1806  COMPARE_OP               ==
         1808_1810  POP_JUMP_IF_FALSE  1842  'to 1842'
             1812  LOAD_FAST                'wordPrev'
             1814  LOAD_STR                 'am'
             1816  COMPARE_OP               !=
         1818_1820  POP_JUMP_IF_FALSE  1842  'to 1842'

 L. 389      1822  LOAD_FAST                'wordPrev'
             1824  LOAD_FAST                'days'
             1826  COMPARE_OP               not-in
         1828_1830  POP_JUMP_IF_FALSE  1842  'to 1842'

 L. 391      1832  LOAD_DEREF               'dayOffset'
             1834  LOAD_CONST               1
             1836  INPLACE_ADD      
             1838  STORE_DEREF              'dayOffset'
             1840  JUMP_FORWARD       2050  'to 2050'
           1842_0  COME_FROM          1828  '1828'
           1842_1  COME_FROM          1818  '1818'
           1842_2  COME_FROM          1808  '1808'

 L. 392      1842  LOAD_FAST                'wordNext'
             1844  LOAD_FAST                'days'
             1846  COMPARE_OP               in
         1848_1850  POP_JUMP_IF_FALSE  1910  'to 1910'

 L. 393      1852  LOAD_FAST                'days'
             1854  LOAD_METHOD              index
             1856  LOAD_FAST                'wordNext'
             1858  CALL_METHOD_1         1  '1 positional argument'
             1860  STORE_FAST               'd'

 L. 394      1862  LOAD_FAST                'd'
             1864  LOAD_CONST               1
             1866  BINARY_ADD       
             1868  LOAD_GLOBAL              int
             1870  LOAD_FAST                'today'
             1872  CALL_FUNCTION_1       1  '1 positional argument'
             1874  BINARY_SUBTRACT  
             1876  STORE_FAST               'tmpOffset'

 L. 395      1878  LOAD_CONST               2
             1880  STORE_FAST               'used'

 L. 396      1882  LOAD_FAST                'tmpOffset'
             1884  LOAD_CONST               0
             1886  COMPARE_OP               <
         1888_1890  POP_JUMP_IF_FALSE  1900  'to 1900'

 L. 397      1892  LOAD_FAST                'tmpOffset'
             1894  LOAD_CONST               7
             1896  INPLACE_ADD      
             1898  STORE_FAST               'tmpOffset'
           1900_0  COME_FROM          1888  '1888'

 L. 398      1900  LOAD_DEREF               'dayOffset'
             1902  LOAD_FAST                'tmpOffset'
             1904  INPLACE_ADD      
             1906  STORE_DEREF              'dayOffset'
             1908  JUMP_FORWARD       2050  'to 2050'
           1910_0  COME_FROM          1848  '1848'

 L. 399      1910  LOAD_FAST                'wordNextNext'
         1912_1914  POP_JUMP_IF_FALSE  2050  'to 2050'
             1916  LOAD_FAST                'wordNextNext'
             1918  LOAD_FAST                'days'
             1920  COMPARE_OP               in
         1922_1924  POP_JUMP_IF_FALSE  2050  'to 2050'

 L. 400      1926  LOAD_FAST                'days'
             1928  LOAD_METHOD              index
             1930  LOAD_FAST                'wordNextNext'
             1932  CALL_METHOD_1         1  '1 positional argument'
             1934  STORE_FAST               'd'

 L. 401      1936  LOAD_FAST                'd'
             1938  LOAD_CONST               1
             1940  BINARY_ADD       
             1942  LOAD_GLOBAL              int
             1944  LOAD_FAST                'today'
             1946  CALL_FUNCTION_1       1  '1 positional argument'
             1948  BINARY_SUBTRACT  
             1950  STORE_FAST               'tmpOffset'

 L. 402      1952  LOAD_CONST               3
             1954  STORE_FAST               'used'

 L. 403      1956  LOAD_FAST                'wordNext'
             1958  LOAD_CONST               None
             1960  LOAD_CONST               6
             1962  BUILD_SLICE_2         2 
             1964  BINARY_SUBSCR    
             1966  LOAD_STR                 'nächst'
             1968  COMPARE_OP               ==
         1970_1972  POP_JUMP_IF_FALSE  2000  'to 2000'

 L. 404      1974  LOAD_FAST                'tmpOffset'
             1976  LOAD_CONST               7
             1978  INPLACE_ADD      
             1980  STORE_FAST               'tmpOffset'

 L. 405      1982  LOAD_FAST                'used'
             1984  LOAD_CONST               1
             1986  INPLACE_ADD      
             1988  STORE_FAST               'used'

 L. 406      1990  LOAD_FAST                'start'
             1992  LOAD_CONST               1
             1994  INPLACE_SUBTRACT 
             1996  STORE_FAST               'start'
             1998  JUMP_FORWARD       2042  'to 2042'
           2000_0  COME_FROM          1970  '1970'

 L. 407      2000  LOAD_FAST                'wordNext'
             2002  LOAD_CONST               None
             2004  LOAD_CONST               5
             2006  BUILD_SLICE_2         2 
             2008  BINARY_SUBSCR    
             2010  LOAD_STR                 'letzt'
             2012  COMPARE_OP               ==
         2014_2016  POP_JUMP_IF_FALSE  2042  'to 2042'

 L. 408      2018  LOAD_FAST                'tmpOffset'
             2020  LOAD_CONST               7
             2022  INPLACE_SUBTRACT 
             2024  STORE_FAST               'tmpOffset'

 L. 409      2026  LOAD_FAST                'used'
             2028  LOAD_CONST               1
             2030  INPLACE_ADD      
             2032  STORE_FAST               'used'

 L. 410      2034  LOAD_FAST                'start'
             2036  LOAD_CONST               1
             2038  INPLACE_SUBTRACT 
             2040  STORE_FAST               'start'
           2042_0  COME_FROM          2014  '2014'
           2042_1  COME_FROM          1998  '1998'

 L. 411      2042  LOAD_DEREF               'dayOffset'
             2044  LOAD_FAST                'tmpOffset'
             2046  INPLACE_ADD      
             2048  STORE_DEREF              'dayOffset'
           2050_0  COME_FROM          1922  '1922'
           2050_1  COME_FROM          1912  '1912'
           2050_2  COME_FROM          1908  '1908'
           2050_3  COME_FROM          1840  '1840'
           2050_4  COME_FROM          1790  '1790'
           2050_5  COME_FROM          1780  '1780'

 L. 412      2050  LOAD_FAST                'used'
             2052  LOAD_CONST               0
             2054  COMPARE_OP               >
         2056_2058  POP_JUMP_IF_FALSE   388  'to 388'

 L. 413      2060  LOAD_FAST                'start'
             2062  LOAD_CONST               1
             2064  BINARY_SUBTRACT  
             2066  LOAD_CONST               0
             2068  COMPARE_OP               >
         2070_2072  POP_JUMP_IF_FALSE  2110  'to 2110'
             2074  LOAD_FAST                'words'
             2076  LOAD_FAST                'start'
             2078  LOAD_CONST               1
             2080  BINARY_SUBTRACT  
             2082  BINARY_SUBSCR    
             2084  LOAD_METHOD              startswith
             2086  LOAD_STR                 'diese'
             2088  CALL_METHOD_1         1  '1 positional argument'
         2090_2092  POP_JUMP_IF_FALSE  2110  'to 2110'

 L. 414      2094  LOAD_FAST                'start'
             2096  LOAD_CONST               1
             2098  INPLACE_SUBTRACT 
             2100  STORE_FAST               'start'

 L. 415      2102  LOAD_FAST                'used'
             2104  LOAD_CONST               1
             2106  INPLACE_ADD      
             2108  STORE_FAST               'used'
           2110_0  COME_FROM          2090  '2090'
           2110_1  COME_FROM          2070  '2070'

 L. 417      2110  SETUP_LOOP         2144  'to 2144'
             2112  LOAD_GLOBAL              range
             2114  LOAD_CONST               0
             2116  LOAD_FAST                'used'
             2118  CALL_FUNCTION_2       2  '2 positional arguments'
             2120  GET_ITER         
             2122  FOR_ITER           2142  'to 2142'
             2124  STORE_FAST               'i'

 L. 418      2126  LOAD_STR                 ''
             2128  LOAD_FAST                'words'
             2130  LOAD_FAST                'i'
             2132  LOAD_FAST                'start'
             2134  BINARY_ADD       
             2136  STORE_SUBSCR     
         2138_2140  JUMP_BACK          2122  'to 2122'
             2142  POP_BLOCK        
           2144_0  COME_FROM_LOOP     2110  '2110'

 L. 420      2144  LOAD_FAST                'start'
             2146  LOAD_CONST               1
             2148  BINARY_SUBTRACT  
             2150  LOAD_CONST               0
             2152  COMPARE_OP               >=
         2154_2156  POP_JUMP_IF_FALSE  2188  'to 2188'
             2158  LOAD_FAST                'words'
             2160  LOAD_FAST                'start'
             2162  LOAD_CONST               1
             2164  BINARY_SUBTRACT  
             2166  BINARY_SUBSCR    
             2168  LOAD_FAST                'markers'
             2170  COMPARE_OP               in
         2172_2174  POP_JUMP_IF_FALSE  2188  'to 2188'

 L. 421      2176  LOAD_STR                 ''
             2178  LOAD_FAST                'words'
             2180  LOAD_FAST                'start'
             2182  LOAD_CONST               1
             2184  BINARY_SUBTRACT  
             2186  STORE_SUBSCR     
           2188_0  COME_FROM          2172  '2172'
           2188_1  COME_FROM          2154  '2154'

 L. 422      2188  LOAD_CONST               True
             2190  STORE_DEREF              'found'

 L. 423      2192  LOAD_CONST               True
             2194  STORE_FAST               'daySpecified'
         2196_2198  JUMP_BACK           388  'to 388'
             2200  POP_BLOCK        
           2202_0  COME_FROM_LOOP      376  '376'

 L. 426      2202  LOAD_STR                 ''
             2204  STORE_DEREF              'timeStr'

 L. 427      2206  LOAD_CONST               0
             2208  STORE_DEREF              'hrOffset'

 L. 428      2210  LOAD_CONST               0
             2212  STORE_DEREF              'minOffset'

 L. 429      2214  LOAD_CONST               0
             2216  STORE_DEREF              'secOffset'

 L. 430      2218  LOAD_CONST               None
             2220  STORE_DEREF              'hrAbs'

 L. 431      2222  LOAD_CONST               None
             2224  STORE_DEREF              'minAbs'

 L. 433  2226_2228  SETUP_LOOP         5082  'to 5082'
             2230  LOAD_GLOBAL              enumerate
             2232  LOAD_FAST                'words'
             2234  CALL_FUNCTION_1       1  '1 positional argument'
             2236  GET_ITER         
           2238_0  COME_FROM          4866  '4866'
         2238_2240  FOR_ITER           5080  'to 5080'
             2242  UNPACK_SEQUENCE_2     2 
             2244  STORE_FAST               'idx'
             2246  STORE_FAST               'word'

 L. 434      2248  LOAD_FAST                'word'
             2250  LOAD_STR                 ''
             2252  COMPARE_OP               ==
         2254_2256  POP_JUMP_IF_FALSE  2262  'to 2262'

 L. 435  2258_2260  CONTINUE           2238  'to 2238'
           2262_0  COME_FROM          2254  '2254'

 L. 437      2262  LOAD_FAST                'idx'
             2264  LOAD_CONST               1
             2266  COMPARE_OP               >
         2268_2270  POP_JUMP_IF_FALSE  2284  'to 2284'
             2272  LOAD_FAST                'words'
             2274  LOAD_FAST                'idx'
             2276  LOAD_CONST               2
             2278  BINARY_SUBTRACT  
             2280  BINARY_SUBSCR    
             2282  JUMP_FORWARD       2286  'to 2286'
           2284_0  COME_FROM          2268  '2268'
             2284  LOAD_STR                 ''
           2286_0  COME_FROM          2282  '2282'
             2286  STORE_FAST               'wordPrevPrev'

 L. 438      2288  LOAD_FAST                'idx'
             2290  LOAD_CONST               0
             2292  COMPARE_OP               >
         2294_2296  POP_JUMP_IF_FALSE  2310  'to 2310'
             2298  LOAD_FAST                'words'
             2300  LOAD_FAST                'idx'
             2302  LOAD_CONST               1
             2304  BINARY_SUBTRACT  
             2306  BINARY_SUBSCR    
             2308  JUMP_FORWARD       2312  'to 2312'
           2310_0  COME_FROM          2294  '2294'
             2310  LOAD_STR                 ''
           2312_0  COME_FROM          2308  '2308'
             2312  STORE_FAST               'wordPrev'

 L. 439      2314  LOAD_FAST                'idx'
             2316  LOAD_CONST               1
             2318  BINARY_ADD       
             2320  LOAD_GLOBAL              len
             2322  LOAD_FAST                'words'
             2324  CALL_FUNCTION_1       1  '1 positional argument'
             2326  COMPARE_OP               <
         2328_2330  POP_JUMP_IF_FALSE  2344  'to 2344'
             2332  LOAD_FAST                'words'
             2334  LOAD_FAST                'idx'
             2336  LOAD_CONST               1
             2338  BINARY_ADD       
             2340  BINARY_SUBSCR    
             2342  JUMP_FORWARD       2346  'to 2346'
           2344_0  COME_FROM          2328  '2328'
             2344  LOAD_STR                 ''
           2346_0  COME_FROM          2342  '2342'
             2346  STORE_FAST               'wordNext'

 L. 440      2348  LOAD_FAST                'idx'
             2350  LOAD_CONST               2
             2352  BINARY_ADD       
             2354  LOAD_GLOBAL              len
             2356  LOAD_FAST                'words'
             2358  CALL_FUNCTION_1       1  '1 positional argument'
             2360  COMPARE_OP               <
         2362_2364  POP_JUMP_IF_FALSE  2378  'to 2378'
             2366  LOAD_FAST                'words'
             2368  LOAD_FAST                'idx'
             2370  LOAD_CONST               2
             2372  BINARY_ADD       
             2374  BINARY_SUBSCR    
             2376  JUMP_FORWARD       2380  'to 2380'
           2378_0  COME_FROM          2362  '2362'
             2378  LOAD_STR                 ''
           2380_0  COME_FROM          2376  '2376'
             2380  STORE_FAST               'wordNextNext'

 L. 441      2382  LOAD_FAST                'idx'
             2384  LOAD_CONST               3
             2386  BINARY_ADD       
             2388  LOAD_GLOBAL              len
             2390  LOAD_FAST                'words'
             2392  CALL_FUNCTION_1       1  '1 positional argument'
             2394  COMPARE_OP               <
         2396_2398  POP_JUMP_IF_FALSE  2412  'to 2412'
             2400  LOAD_FAST                'words'
             2402  LOAD_FAST                'idx'
             2404  LOAD_CONST               3
             2406  BINARY_ADD       
             2408  BINARY_SUBSCR    
             2410  JUMP_FORWARD       2414  'to 2414'
           2412_0  COME_FROM          2396  '2396'
             2412  LOAD_STR                 ''
           2414_0  COME_FROM          2410  '2410'
             2414  STORE_FAST               'wordNextNextNext'

 L. 442      2416  LOAD_FAST                'idx'
             2418  LOAD_CONST               4
             2420  BINARY_ADD       
             2422  LOAD_GLOBAL              len
             2424  LOAD_FAST                'words'
             2426  CALL_FUNCTION_1       1  '1 positional argument'
             2428  COMPARE_OP               <
         2430_2432  POP_JUMP_IF_FALSE  2446  'to 2446'
             2434  LOAD_FAST                'words'
             2436  LOAD_FAST                'idx'
             2438  LOAD_CONST               4
             2440  BINARY_ADD       
             2442  BINARY_SUBSCR    
             2444  JUMP_FORWARD       2448  'to 2448'
           2446_0  COME_FROM          2430  '2430'
             2446  LOAD_STR                 ''
           2448_0  COME_FROM          2444  '2444'
             2448  STORE_FAST               'wordNextNextNextNext'

 L. 445      2450  LOAD_CONST               0
             2452  STORE_FAST               'used'

 L. 446      2454  LOAD_FAST                'word'
             2456  LOAD_CONST               None
             2458  LOAD_CONST               6
             2460  BUILD_SLICE_2         2 
             2462  BINARY_SUBSCR    
             2464  LOAD_STR                 'mittag'
             2466  COMPARE_OP               ==
         2468_2470  POP_JUMP_IF_FALSE  2488  'to 2488'

 L. 447      2472  LOAD_CONST               12
             2474  STORE_DEREF              'hrAbs'

 L. 448      2476  LOAD_FAST                'used'
             2478  LOAD_CONST               1
             2480  INPLACE_ADD      
             2482  STORE_FAST               'used'
         2484_2486  JUMP_FORWARD       4860  'to 4860'
           2488_0  COME_FROM          2468  '2468'

 L. 449      2488  LOAD_FAST                'word'
             2490  LOAD_CONST               None
             2492  LOAD_CONST               11
             2494  BUILD_SLICE_2         2 
             2496  BINARY_SUBSCR    
             2498  LOAD_STR                 'mitternacht'
             2500  COMPARE_OP               ==
         2502_2504  POP_JUMP_IF_FALSE  2522  'to 2522'

 L. 450      2506  LOAD_CONST               0
             2508  STORE_DEREF              'hrAbs'

 L. 451      2510  LOAD_FAST                'used'
             2512  LOAD_CONST               1
             2514  INPLACE_ADD      
             2516  STORE_FAST               'used'
         2518_2520  JUMP_FORWARD       4860  'to 4860'
           2522_0  COME_FROM          2502  '2502'

 L. 452      2522  LOAD_FAST                'word'
             2524  LOAD_STR                 'morgens'
             2526  COMPARE_OP               ==
         2528_2530  POP_JUMP_IF_TRUE   2562  'to 2562'

 L. 453      2532  LOAD_FAST                'wordPrev'
             2534  LOAD_STR                 'am'
             2536  COMPARE_OP               ==
         2538_2540  POP_JUMP_IF_FALSE  2552  'to 2552'
             2542  LOAD_FAST                'word'
             2544  LOAD_STR                 'morgen'
             2546  COMPARE_OP               ==
         2548_2550  POP_JUMP_IF_TRUE   2562  'to 2562'
           2552_0  COME_FROM          2538  '2538'
             2552  LOAD_FAST                'word'
             2554  LOAD_STR                 'früh'
             2556  COMPARE_OP               ==
         2558_2560  POP_JUMP_IF_FALSE  2584  'to 2584'
           2562_0  COME_FROM          2548  '2548'
           2562_1  COME_FROM          2528  '2528'

 L. 454      2562  LOAD_DEREF               'hrAbs'
         2564_2566  POP_JUMP_IF_TRUE   2572  'to 2572'

 L. 455      2568  LOAD_CONST               8
             2570  STORE_DEREF              'hrAbs'
           2572_0  COME_FROM          2564  '2564'

 L. 456      2572  LOAD_FAST                'used'
             2574  LOAD_CONST               1
             2576  INPLACE_ADD      
             2578  STORE_FAST               'used'
         2580_2582  JUMP_FORWARD       4860  'to 4860'
           2584_0  COME_FROM          2558  '2558'

 L. 457      2584  LOAD_FAST                'word'
             2586  LOAD_CONST               None
             2588  LOAD_CONST               10
             2590  BUILD_SLICE_2         2 
             2592  BINARY_SUBSCR    
             2594  LOAD_STR                 'nachmittag'
             2596  COMPARE_OP               ==
         2598_2600  POP_JUMP_IF_FALSE  2624  'to 2624'

 L. 458      2602  LOAD_DEREF               'hrAbs'
         2604_2606  POP_JUMP_IF_TRUE   2612  'to 2612'

 L. 459      2608  LOAD_CONST               15
             2610  STORE_DEREF              'hrAbs'
           2612_0  COME_FROM          2604  '2604'

 L. 460      2612  LOAD_FAST                'used'
             2614  LOAD_CONST               1
             2616  INPLACE_ADD      
             2618  STORE_FAST               'used'
         2620_2622  JUMP_FORWARD       4860  'to 4860'
           2624_0  COME_FROM          2598  '2598'

 L. 461      2624  LOAD_FAST                'word'
             2626  LOAD_CONST               None
             2628  LOAD_CONST               5
             2630  BUILD_SLICE_2         2 
             2632  BINARY_SUBSCR    
             2634  LOAD_STR                 'abend'
             2636  COMPARE_OP               ==
         2638_2640  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 462      2642  LOAD_DEREF               'hrAbs'
         2644_2646  POP_JUMP_IF_TRUE   2652  'to 2652'

 L. 463      2648  LOAD_CONST               19
             2650  STORE_DEREF              'hrAbs'
           2652_0  COME_FROM          2644  '2644'

 L. 464      2652  LOAD_FAST                'used'
             2654  LOAD_CONST               1
             2656  INPLACE_ADD      
             2658  STORE_FAST               'used'
         2660_2662  JUMP_FORWARD       4860  'to 4860'
           2664_0  COME_FROM          2638  '2638'

 L. 466      2664  LOAD_FAST                'word'
             2666  LOAD_STR                 'stunde'
             2668  COMPARE_OP               ==
         2670_2672  POP_JUMP_IF_FALSE  2808  'to 2808'

 L. 467      2674  LOAD_FAST                'wordPrev'
             2676  LOAD_FAST                'markers'
             2678  COMPARE_OP               in
         2680_2682  POP_JUMP_IF_TRUE   2694  'to 2694'
             2684  LOAD_FAST                'wordPrevPrev'
             2686  LOAD_FAST                'markers'
             2688  COMPARE_OP               in
         2690_2692  POP_JUMP_IF_FALSE  2808  'to 2808'
           2694_0  COME_FROM          2680  '2680'

 L. 468      2694  LOAD_FAST                'wordPrev'
             2696  LOAD_CONST               None
             2698  LOAD_CONST               4
             2700  BUILD_SLICE_2         2 
             2702  BINARY_SUBSCR    
             2704  LOAD_STR                 'halb'
             2706  COMPARE_OP               ==
         2708_2710  POP_JUMP_IF_FALSE  2718  'to 2718'

 L. 469      2712  LOAD_CONST               30
             2714  STORE_DEREF              'minOffset'
             2716  JUMP_FORWARD       2754  'to 2754'
           2718_0  COME_FROM          2708  '2708'

 L. 470      2718  LOAD_FAST                'wordPrev'
             2720  LOAD_STR                 'viertel'
             2722  COMPARE_OP               ==
         2724_2726  POP_JUMP_IF_FALSE  2734  'to 2734'

 L. 471      2728  LOAD_CONST               15
             2730  STORE_DEREF              'minOffset'
             2732  JUMP_FORWARD       2754  'to 2754'
           2734_0  COME_FROM          2724  '2724'

 L. 472      2734  LOAD_FAST                'wordPrev'
             2736  LOAD_STR                 'dreiviertel'
             2738  COMPARE_OP               ==
         2740_2742  POP_JUMP_IF_FALSE  2750  'to 2750'

 L. 473      2744  LOAD_CONST               45
             2746  STORE_DEREF              'minOffset'
             2748  JUMP_FORWARD       2754  'to 2754'
           2750_0  COME_FROM          2740  '2740'

 L. 475      2750  LOAD_CONST               1
             2752  STORE_DEREF              'hrOffset'
           2754_0  COME_FROM          2748  '2748'
           2754_1  COME_FROM          2732  '2732'
           2754_2  COME_FROM          2716  '2716'

 L. 476      2754  LOAD_FAST                'wordPrevPrev'
             2756  LOAD_FAST                'markers'
             2758  COMPARE_OP               in
         2760_2762  POP_JUMP_IF_FALSE  2776  'to 2776'

 L. 477      2764  LOAD_STR                 ''
             2766  LOAD_FAST                'words'
             2768  LOAD_FAST                'idx'
             2770  LOAD_CONST               2
             2772  BINARY_SUBTRACT  
             2774  STORE_SUBSCR     
           2776_0  COME_FROM          2760  '2760'

 L. 478      2776  LOAD_STR                 ''
             2778  LOAD_FAST                'words'
             2780  LOAD_FAST                'idx'
             2782  LOAD_CONST               1
             2784  BINARY_SUBTRACT  
             2786  STORE_SUBSCR     

 L. 479      2788  LOAD_FAST                'used'
             2790  LOAD_CONST               1
             2792  INPLACE_ADD      
             2794  STORE_FAST               'used'

 L. 480      2796  LOAD_CONST               -1
             2798  STORE_DEREF              'hrAbs'

 L. 481      2800  LOAD_CONST               -1
             2802  STORE_DEREF              'minAbs'
         2804_2806  JUMP_FORWARD       4860  'to 4860'
           2808_0  COME_FROM          2690  '2690'
           2808_1  COME_FROM          2670  '2670'

 L. 483      2808  LOAD_FAST                'word'
             2810  LOAD_CONST               0
             2812  BINARY_SUBSCR    
             2814  LOAD_METHOD              isdigit
             2816  CALL_METHOD_0         0  '0 positional arguments'
         2818_2820  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 484      2822  LOAD_CONST               True
             2824  STORE_FAST               'isTime'

 L. 485      2826  LOAD_STR                 ''
             2828  STORE_FAST               'strHH'

 L. 486      2830  LOAD_STR                 ''
             2832  STORE_FAST               'strMM'

 L. 487      2834  LOAD_STR                 ''
             2836  STORE_FAST               'remainder'

 L. 488      2838  LOAD_STR                 ':'
             2840  LOAD_FAST                'word'
             2842  COMPARE_OP               in
         2844_2846  POP_JUMP_IF_FALSE  3480  'to 3480'

 L. 491      2848  LOAD_CONST               0
             2850  STORE_FAST               'stage'

 L. 492      2852  LOAD_GLOBAL              len
             2854  LOAD_FAST                'word'
             2856  CALL_FUNCTION_1       1  '1 positional argument'
             2858  STORE_FAST               'length'

 L. 493      2860  SETUP_LOOP         3036  'to 3036'
             2862  LOAD_GLOBAL              range
             2864  LOAD_FAST                'length'
             2866  CALL_FUNCTION_1       1  '1 positional argument'
             2868  GET_ITER         
           2870_0  COME_FROM          3004  '3004'
             2870  FOR_ITER           3034  'to 3034'
             2872  STORE_FAST               'i'

 L. 494      2874  LOAD_FAST                'stage'
             2876  LOAD_CONST               0
             2878  COMPARE_OP               ==
         2880_2882  POP_JUMP_IF_FALSE  2946  'to 2946'

 L. 495      2884  LOAD_FAST                'word'
             2886  LOAD_FAST                'i'
             2888  BINARY_SUBSCR    
             2890  LOAD_METHOD              isdigit
             2892  CALL_METHOD_0         0  '0 positional arguments'
         2894_2896  POP_JUMP_IF_FALSE  2912  'to 2912'

 L. 496      2898  LOAD_FAST                'strHH'
             2900  LOAD_FAST                'word'
             2902  LOAD_FAST                'i'
             2904  BINARY_SUBSCR    
             2906  INPLACE_ADD      
             2908  STORE_FAST               'strHH'
             2910  JUMP_FORWARD       2944  'to 2944'
           2912_0  COME_FROM          2894  '2894'

 L. 497      2912  LOAD_FAST                'word'
             2914  LOAD_FAST                'i'
             2916  BINARY_SUBSCR    
             2918  LOAD_STR                 ':'
             2920  COMPARE_OP               ==
         2922_2924  POP_JUMP_IF_FALSE  2932  'to 2932'

 L. 498      2926  LOAD_CONST               1
             2928  STORE_FAST               'stage'
             2930  JUMP_FORWARD       2944  'to 2944'
           2932_0  COME_FROM          2922  '2922'

 L. 500      2932  LOAD_CONST               2
             2934  STORE_FAST               'stage'

 L. 501      2936  LOAD_FAST                'i'
             2938  LOAD_CONST               1
             2940  INPLACE_SUBTRACT 
             2942  STORE_FAST               'i'
           2944_0  COME_FROM          2930  '2930'
           2944_1  COME_FROM          2910  '2910'
             2944  JUMP_BACK          2870  'to 2870'
           2946_0  COME_FROM          2880  '2880'

 L. 502      2946  LOAD_FAST                'stage'
             2948  LOAD_CONST               1
             2950  COMPARE_OP               ==
         2952_2954  POP_JUMP_IF_FALSE  2998  'to 2998'

 L. 503      2956  LOAD_FAST                'word'
             2958  LOAD_FAST                'i'
             2960  BINARY_SUBSCR    
             2962  LOAD_METHOD              isdigit
             2964  CALL_METHOD_0         0  '0 positional arguments'
         2966_2968  POP_JUMP_IF_FALSE  2984  'to 2984'

 L. 504      2970  LOAD_FAST                'strMM'
             2972  LOAD_FAST                'word'
             2974  LOAD_FAST                'i'
             2976  BINARY_SUBSCR    
             2978  INPLACE_ADD      
             2980  STORE_FAST               'strMM'
             2982  JUMP_FORWARD       2996  'to 2996'
           2984_0  COME_FROM          2966  '2966'

 L. 506      2984  LOAD_CONST               2
             2986  STORE_FAST               'stage'

 L. 507      2988  LOAD_FAST                'i'
             2990  LOAD_CONST               1
             2992  INPLACE_SUBTRACT 
             2994  STORE_FAST               'i'
           2996_0  COME_FROM          2982  '2982'
             2996  JUMP_BACK          2870  'to 2870'
           2998_0  COME_FROM          2952  '2952'

 L. 508      2998  LOAD_FAST                'stage'
             3000  LOAD_CONST               2
             3002  COMPARE_OP               ==
         3004_3006  POP_JUMP_IF_FALSE  2870  'to 2870'

 L. 509      3008  LOAD_FAST                'word'
             3010  LOAD_FAST                'i'
             3012  LOAD_CONST               None
             3014  BUILD_SLICE_2         2 
             3016  BINARY_SUBSCR    
             3018  LOAD_METHOD              replace
             3020  LOAD_STR                 '.'
             3022  LOAD_STR                 ''
             3024  CALL_METHOD_2         2  '2 positional arguments'
             3026  STORE_FAST               'remainder'

 L. 510      3028  BREAK_LOOP       
         3030_3032  JUMP_BACK          2870  'to 2870'
             3034  POP_BLOCK        
           3036_0  COME_FROM_LOOP     2860  '2860'

 L. 511      3036  LOAD_FAST                'remainder'
             3038  LOAD_STR                 ''
             3040  COMPARE_OP               ==
         3042_3044  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 512      3046  LOAD_FAST                'wordNext'
             3048  LOAD_METHOD              replace
             3050  LOAD_STR                 '.'
             3052  LOAD_STR                 ''
             3054  CALL_METHOD_2         2  '2 positional arguments'
             3056  STORE_FAST               'nextWord'

 L. 513      3058  LOAD_FAST                'nextWord'
             3060  LOAD_STR                 'am'
             3062  COMPARE_OP               ==
         3064_3066  POP_JUMP_IF_TRUE   3078  'to 3078'
             3068  LOAD_FAST                'nextWord'
             3070  LOAD_STR                 'pm'
             3072  COMPARE_OP               ==
         3074_3076  POP_JUMP_IF_FALSE  3094  'to 3094'
           3078_0  COME_FROM          3064  '3064'

 L. 514      3078  LOAD_FAST                'nextWord'
             3080  STORE_FAST               'remainder'

 L. 515      3082  LOAD_FAST                'used'
             3084  LOAD_CONST               1
             3086  INPLACE_ADD      
             3088  STORE_FAST               'used'
         3090_3092  JUMP_ABSOLUTE      4702  'to 4702'
           3094_0  COME_FROM          3074  '3074'

 L. 516      3094  LOAD_FAST                'nextWord'
             3096  LOAD_STR                 'abends'
             3098  COMPARE_OP               ==
         3100_3102  POP_JUMP_IF_FALSE  3120  'to 3120'

 L. 517      3104  LOAD_STR                 'pm'
             3106  STORE_FAST               'remainder'

 L. 518      3108  LOAD_FAST                'used'
             3110  LOAD_CONST               1
             3112  INPLACE_ADD      
             3114  STORE_FAST               'used'
         3116_3118  JUMP_ABSOLUTE      4702  'to 4702'
           3120_0  COME_FROM          3100  '3100'

 L. 519      3120  LOAD_FAST                'wordNext'
             3122  LOAD_STR                 'am'
             3124  COMPARE_OP               ==
         3126_3128  POP_JUMP_IF_FALSE  3156  'to 3156'
             3130  LOAD_FAST                'wordNextNext'
             3132  LOAD_STR                 'morgen'
             3134  COMPARE_OP               ==
         3136_3138  POP_JUMP_IF_FALSE  3156  'to 3156'

 L. 520      3140  LOAD_STR                 'am'
             3142  STORE_FAST               'remainder'

 L. 521      3144  LOAD_FAST                'used'
             3146  LOAD_CONST               2
             3148  INPLACE_ADD      
             3150  STORE_FAST               'used'
         3152_3154  JUMP_ABSOLUTE      4702  'to 4702'
           3156_0  COME_FROM          3136  '3136'
           3156_1  COME_FROM          3126  '3126'

 L. 522      3156  LOAD_FAST                'wordNext'
             3158  LOAD_STR                 'am'
             3160  COMPARE_OP               ==
         3162_3164  POP_JUMP_IF_FALSE  3192  'to 3192'
             3166  LOAD_FAST                'wordNextNext'
             3168  LOAD_STR                 'nachmittag'
             3170  COMPARE_OP               ==
         3172_3174  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 523      3176  LOAD_STR                 'pm'
             3178  STORE_FAST               'remainder'

 L. 524      3180  LOAD_FAST                'used'
             3182  LOAD_CONST               2
             3184  INPLACE_ADD      
             3186  STORE_FAST               'used'
         3188_3190  JUMP_ABSOLUTE      4702  'to 4702'
           3192_0  COME_FROM          3172  '3172'
           3192_1  COME_FROM          3162  '3162'

 L. 525      3192  LOAD_FAST                'wordNext'
             3194  LOAD_STR                 'am'
             3196  COMPARE_OP               ==
         3198_3200  POP_JUMP_IF_FALSE  3226  'to 3226'
             3202  LOAD_FAST                'wordNextNext'
             3204  LOAD_STR                 'abend'
             3206  COMPARE_OP               ==
         3208_3210  POP_JUMP_IF_FALSE  3226  'to 3226'

 L. 526      3212  LOAD_STR                 'pm'
             3214  STORE_FAST               'remainder'

 L. 527      3216  LOAD_FAST                'used'
             3218  LOAD_CONST               2
             3220  INPLACE_ADD      
             3222  STORE_FAST               'used'
             3224  JUMP_FORWARD       4702  'to 4702'
           3226_0  COME_FROM          3208  '3208'
           3226_1  COME_FROM          3198  '3198'

 L. 528      3226  LOAD_FAST                'wordNext'
             3228  LOAD_STR                 'morgens'
             3230  COMPARE_OP               ==
         3232_3234  POP_JUMP_IF_FALSE  3250  'to 3250'

 L. 529      3236  LOAD_STR                 'am'
             3238  STORE_FAST               'remainder'

 L. 530      3240  LOAD_FAST                'used'
             3242  LOAD_CONST               1
             3244  INPLACE_ADD      
             3246  STORE_FAST               'used'
             3248  JUMP_FORWARD       4702  'to 4702'
           3250_0  COME_FROM          3232  '3232'

 L. 531      3250  LOAD_FAST                'wordNext'
             3252  LOAD_STR                 'nachmittags'
             3254  COMPARE_OP               ==
         3256_3258  POP_JUMP_IF_FALSE  3274  'to 3274'

 L. 532      3260  LOAD_STR                 'pm'
             3262  STORE_FAST               'remainder'

 L. 533      3264  LOAD_FAST                'used'
             3266  LOAD_CONST               1
             3268  INPLACE_ADD      
             3270  STORE_FAST               'used'
             3272  JUMP_FORWARD       4702  'to 4702'
           3274_0  COME_FROM          3256  '3256'

 L. 534      3274  LOAD_FAST                'wordNext'
             3276  LOAD_STR                 'abends'
             3278  COMPARE_OP               ==
         3280_3282  POP_JUMP_IF_FALSE  3298  'to 3298'

 L. 535      3284  LOAD_STR                 'pm'
             3286  STORE_FAST               'remainder'

 L. 536      3288  LOAD_FAST                'used'
             3290  LOAD_CONST               1
             3292  INPLACE_ADD      
             3294  STORE_FAST               'used'
             3296  JUMP_FORWARD       4702  'to 4702'
           3298_0  COME_FROM          3280  '3280'

 L. 537      3298  LOAD_FAST                'wordNext'
             3300  LOAD_STR                 'heute'
             3302  COMPARE_OP               ==
         3304_3306  POP_JUMP_IF_FALSE  3328  'to 3328'
             3308  LOAD_FAST                'wordNextNext'
             3310  LOAD_STR                 'morgen'
             3312  COMPARE_OP               ==
         3314_3316  POP_JUMP_IF_FALSE  3328  'to 3328'

 L. 538      3318  LOAD_STR                 'am'
             3320  STORE_FAST               'remainder'

 L. 539      3322  LOAD_CONST               2
             3324  STORE_FAST               'used'
             3326  JUMP_FORWARD       4702  'to 4702'
           3328_0  COME_FROM          3314  '3314'
           3328_1  COME_FROM          3304  '3304'

 L. 540      3328  LOAD_FAST                'wordNext'
             3330  LOAD_STR                 'heute'
             3332  COMPARE_OP               ==
         3334_3336  POP_JUMP_IF_FALSE  3358  'to 3358'
             3338  LOAD_FAST                'wordNextNext'
             3340  LOAD_STR                 'nachmittag'
             3342  COMPARE_OP               ==
         3344_3346  POP_JUMP_IF_FALSE  3358  'to 3358'

 L. 541      3348  LOAD_STR                 'pm'
             3350  STORE_FAST               'remainder'

 L. 542      3352  LOAD_CONST               2
             3354  STORE_FAST               'used'
             3356  JUMP_FORWARD       4702  'to 4702'
           3358_0  COME_FROM          3344  '3344'
           3358_1  COME_FROM          3334  '3334'

 L. 543      3358  LOAD_FAST                'wordNext'
             3360  LOAD_STR                 'heute'
             3362  COMPARE_OP               ==
         3364_3366  POP_JUMP_IF_FALSE  3388  'to 3388'
             3368  LOAD_FAST                'wordNextNext'
             3370  LOAD_STR                 'abend'
             3372  COMPARE_OP               ==
         3374_3376  POP_JUMP_IF_FALSE  3388  'to 3388'

 L. 544      3378  LOAD_STR                 'pm'
             3380  STORE_FAST               'remainder'

 L. 545      3382  LOAD_CONST               2
             3384  STORE_FAST               'used'
             3386  JUMP_FORWARD       4702  'to 4702'
           3388_0  COME_FROM          3374  '3374'
           3388_1  COME_FROM          3364  '3364'

 L. 546      3388  LOAD_FAST                'wordNext'
             3390  LOAD_STR                 'nachts'
             3392  COMPARE_OP               ==
         3394_3396  POP_JUMP_IF_FALSE  3428  'to 3428'

 L. 547      3398  LOAD_FAST                'strHH'
             3400  LOAD_CONST               4
             3402  COMPARE_OP               >
         3404_3406  POP_JUMP_IF_FALSE  3414  'to 3414'

 L. 548      3408  LOAD_STR                 'pm'
             3410  STORE_FAST               'remainder'
             3412  JUMP_FORWARD       3418  'to 3418'
           3414_0  COME_FROM          3404  '3404'

 L. 550      3414  LOAD_STR                 'am'
             3416  STORE_FAST               'remainder'
           3418_0  COME_FROM          3412  '3412'

 L. 551      3418  LOAD_FAST                'used'
             3420  LOAD_CONST               1
             3422  INPLACE_ADD      
             3424  STORE_FAST               'used'
             3426  JUMP_FORWARD       4702  'to 4702'
           3428_0  COME_FROM          3394  '3394'

 L. 553      3428  LOAD_FAST                'timeQualifier'
             3430  LOAD_STR                 ''
             3432  COMPARE_OP               !=
         3434_3436  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 554      3438  LOAD_FAST                'strHH'
             3440  LOAD_CONST               12
             3442  COMPARE_OP               <=
         3444_3446  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 555      3448  LOAD_FAST                'timeQualifier'
             3450  LOAD_STR                 'abends'
             3452  COMPARE_OP               ==
         3454_3456  POP_JUMP_IF_TRUE   3468  'to 3468'

 L. 556      3458  LOAD_FAST                'timeQualifier'
             3460  LOAD_STR                 'nachmittags'
             3462  COMPARE_OP               ==
         3464_3466  POP_JUMP_IF_FALSE  4702  'to 4702'
           3468_0  COME_FROM          3454  '3454'

 L. 557      3468  LOAD_FAST                'strHH'
             3470  LOAD_CONST               12
             3472  INPLACE_ADD      
             3474  STORE_FAST               'strHH'
         3476_3478  JUMP_FORWARD       4702  'to 4702'
           3480_0  COME_FROM          2844  '2844'

 L. 561      3480  LOAD_GLOBAL              len
             3482  LOAD_FAST                'word'
             3484  CALL_FUNCTION_1       1  '1 positional argument'
             3486  STORE_FAST               'length'

 L. 562      3488  LOAD_STR                 ''
             3490  STORE_FAST               'strNum'

 L. 563      3492  LOAD_STR                 ''
             3494  STORE_FAST               'remainder'

 L. 564      3496  SETUP_LOOP         3556  'to 3556'
             3498  LOAD_GLOBAL              range
             3500  LOAD_FAST                'length'
             3502  CALL_FUNCTION_1       1  '1 positional argument'
             3504  GET_ITER         
             3506  FOR_ITER           3554  'to 3554'
             3508  STORE_FAST               'i'

 L. 565      3510  LOAD_FAST                'word'
             3512  LOAD_FAST                'i'
             3514  BINARY_SUBSCR    
             3516  LOAD_METHOD              isdigit
             3518  CALL_METHOD_0         0  '0 positional arguments'
         3520_3522  POP_JUMP_IF_FALSE  3538  'to 3538'

 L. 566      3524  LOAD_FAST                'strNum'
             3526  LOAD_FAST                'word'
             3528  LOAD_FAST                'i'
             3530  BINARY_SUBSCR    
             3532  INPLACE_ADD      
             3534  STORE_FAST               'strNum'
             3536  JUMP_BACK          3506  'to 3506'
           3538_0  COME_FROM          3520  '3520'

 L. 568      3538  LOAD_FAST                'remainder'
             3540  LOAD_FAST                'word'
             3542  LOAD_FAST                'i'
             3544  BINARY_SUBSCR    
             3546  INPLACE_ADD      
             3548  STORE_FAST               'remainder'
         3550_3552  JUMP_BACK          3506  'to 3506'
             3554  POP_BLOCK        
           3556_0  COME_FROM_LOOP     3496  '3496'

 L. 570      3556  LOAD_FAST                'remainder'
             3558  LOAD_STR                 ''
             3560  COMPARE_OP               ==
         3562_3564  POP_JUMP_IF_FALSE  3586  'to 3586'

 L. 571      3566  LOAD_FAST                'wordNext'
             3568  LOAD_METHOD              replace
             3570  LOAD_STR                 '.'
             3572  LOAD_STR                 ''
             3574  CALL_METHOD_2         2  '2 positional arguments'
             3576  LOAD_METHOD              lstrip
             3578  CALL_METHOD_0         0  '0 positional arguments'
             3580  LOAD_METHOD              rstrip
             3582  CALL_METHOD_0         0  '0 positional arguments'
             3584  STORE_FAST               'remainder'
           3586_0  COME_FROM          3562  '3562'

 L. 574      3586  LOAD_FAST                'remainder'
             3588  LOAD_STR                 'pm'
             3590  COMPARE_OP               ==
         3592_3594  POP_JUMP_IF_TRUE   3626  'to 3626'

 L. 575      3596  LOAD_FAST                'wordNext'
             3598  LOAD_STR                 'pm'
             3600  COMPARE_OP               ==
         3602_3604  POP_JUMP_IF_TRUE   3626  'to 3626'

 L. 576      3606  LOAD_FAST                'remainder'
             3608  LOAD_STR                 'p.m.'
             3610  COMPARE_OP               ==
         3612_3614  POP_JUMP_IF_TRUE   3626  'to 3626'

 L. 577      3616  LOAD_FAST                'wordNext'
             3618  LOAD_STR                 'p.m.'
             3620  COMPARE_OP               ==
         3622_3624  POP_JUMP_IF_FALSE  3642  'to 3642'
           3626_0  COME_FROM          3612  '3612'
           3626_1  COME_FROM          3602  '3602'
           3626_2  COME_FROM          3592  '3592'

 L. 578      3626  LOAD_FAST                'strNum'
             3628  STORE_FAST               'strHH'

 L. 579      3630  LOAD_STR                 'pm'
             3632  STORE_FAST               'remainder'

 L. 580      3634  LOAD_CONST               1
             3636  STORE_FAST               'used'
         3638_3640  JUMP_FORWARD       4702  'to 4702'
           3642_0  COME_FROM          3622  '3622'

 L. 582      3642  LOAD_FAST                'remainder'
             3644  LOAD_STR                 'am'
             3646  COMPARE_OP               ==
         3648_3650  POP_JUMP_IF_TRUE   3682  'to 3682'

 L. 583      3652  LOAD_FAST                'wordNext'
             3654  LOAD_STR                 'am'
             3656  COMPARE_OP               ==
         3658_3660  POP_JUMP_IF_TRUE   3682  'to 3682'

 L. 584      3662  LOAD_FAST                'remainder'
             3664  LOAD_STR                 'a.m.'
             3666  COMPARE_OP               ==
         3668_3670  POP_JUMP_IF_TRUE   3682  'to 3682'

 L. 585      3672  LOAD_FAST                'wordNext'
             3674  LOAD_STR                 'a.m.'
             3676  COMPARE_OP               ==
         3678_3680  POP_JUMP_IF_FALSE  3698  'to 3698'
           3682_0  COME_FROM          3668  '3668'
           3682_1  COME_FROM          3658  '3658'
           3682_2  COME_FROM          3648  '3648'

 L. 586      3682  LOAD_FAST                'strNum'
             3684  STORE_FAST               'strHH'

 L. 587      3686  LOAD_STR                 'am'
             3688  STORE_FAST               'remainder'

 L. 588      3690  LOAD_CONST               1
             3692  STORE_FAST               'used'
         3694_3696  JUMP_FORWARD       4702  'to 4702'
           3698_0  COME_FROM          3678  '3678'

 L. 590      3698  LOAD_FAST                'wordNext'
             3700  LOAD_STR                 'stund'
             3702  COMPARE_OP               ==
         3704_3706  POP_JUMP_IF_FALSE  3750  'to 3750'
             3708  LOAD_GLOBAL              int
             3710  LOAD_FAST                'word'
             3712  CALL_FUNCTION_1       1  '1 positional argument'
             3714  LOAD_CONST               100
             3716  COMPARE_OP               <
         3718_3720  POP_JUMP_IF_FALSE  3750  'to 3750'

 L. 592      3722  LOAD_GLOBAL              int
             3724  LOAD_FAST                'word'
             3726  CALL_FUNCTION_1       1  '1 positional argument'
             3728  STORE_DEREF              'hrOffset'

 L. 593      3730  LOAD_CONST               2
             3732  STORE_FAST               'used'

 L. 594      3734  LOAD_CONST               False
             3736  STORE_FAST               'isTime'

 L. 595      3738  LOAD_CONST               -1
             3740  STORE_DEREF              'hrAbs'

 L. 596      3742  LOAD_CONST               -1
             3744  STORE_DEREF              'minAbs'
         3746_3748  JUMP_FORWARD       4702  'to 4702'
           3750_0  COME_FROM          3718  '3718'
           3750_1  COME_FROM          3704  '3704'

 L. 597      3750  LOAD_FAST                'wordNext'
             3752  LOAD_STR                 'minut'
             3754  COMPARE_OP               ==
         3756_3758  POP_JUMP_IF_FALSE  3788  'to 3788'

 L. 599      3760  LOAD_GLOBAL              int
             3762  LOAD_FAST                'word'
             3764  CALL_FUNCTION_1       1  '1 positional argument'
             3766  STORE_DEREF              'minOffset'

 L. 600      3768  LOAD_CONST               2
             3770  STORE_FAST               'used'

 L. 601      3772  LOAD_CONST               False
             3774  STORE_FAST               'isTime'

 L. 602      3776  LOAD_CONST               -1
             3778  STORE_DEREF              'hrAbs'

 L. 603      3780  LOAD_CONST               -1
             3782  STORE_DEREF              'minAbs'
         3784_3786  JUMP_FORWARD       4702  'to 4702'
           3788_0  COME_FROM          3756  '3756'

 L. 604      3788  LOAD_FAST                'wordNext'
             3790  LOAD_STR                 'sekund'
             3792  COMPARE_OP               ==
         3794_3796  POP_JUMP_IF_FALSE  3826  'to 3826'

 L. 606      3798  LOAD_GLOBAL              int
             3800  LOAD_FAST                'word'
             3802  CALL_FUNCTION_1       1  '1 positional argument'
             3804  STORE_DEREF              'secOffset'

 L. 607      3806  LOAD_CONST               2
             3808  STORE_FAST               'used'

 L. 608      3810  LOAD_CONST               False
             3812  STORE_FAST               'isTime'

 L. 609      3814  LOAD_CONST               -1
             3816  STORE_DEREF              'hrAbs'

 L. 610      3818  LOAD_CONST               -1
             3820  STORE_DEREF              'minAbs'
         3822_3824  JUMP_FORWARD       4702  'to 4702'
           3826_0  COME_FROM          3794  '3794'

 L. 612      3826  LOAD_FAST                'wordNext'
             3828  LOAD_STR                 'uhr'
             3830  COMPARE_OP               ==
         3832_3834  POP_JUMP_IF_FALSE  4422  'to 4422'

 L. 613      3836  LOAD_FAST                'word'
             3838  STORE_FAST               'strHH'

 L. 614      3840  LOAD_FAST                'used'
             3842  LOAD_CONST               1
             3844  INPLACE_ADD      
             3846  STORE_FAST               'used'

 L. 615      3848  LOAD_CONST               True
             3850  STORE_FAST               'isTime'

 L. 616      3852  LOAD_FAST                'wordNextNext'
             3854  LOAD_FAST                'timeQualifier'
             3856  COMPARE_OP               ==
         3858_3860  POP_JUMP_IF_FALSE  4128  'to 4128'

 L. 617      3862  LOAD_STR                 ''
             3864  STORE_FAST               'strMM'

 L. 618      3866  LOAD_FAST                'wordNextNext'
             3868  LOAD_CONST               None
             3870  LOAD_CONST               10
             3872  BUILD_SLICE_2         2 
             3874  BINARY_SUBSCR    
             3876  LOAD_STR                 'nachmittag'
             3878  COMPARE_OP               ==
         3880_3882  POP_JUMP_IF_FALSE  3898  'to 3898'

 L. 619      3884  LOAD_FAST                'used'
             3886  LOAD_CONST               1
             3888  INPLACE_ADD      
             3890  STORE_FAST               'used'

 L. 620      3892  LOAD_STR                 'pm'
             3894  STORE_FAST               'remainder'
             3896  JUMP_ABSOLUTE      4702  'to 4702'
           3898_0  COME_FROM          3880  '3880'

 L. 621      3898  LOAD_FAST                'wordNextNext'
             3900  LOAD_STR                 'am'
             3902  COMPARE_OP               ==
         3904_3906  POP_JUMP_IF_FALSE  3932  'to 3932'
             3908  LOAD_FAST                'wordNextNextNext'

 L. 622      3910  LOAD_STR                 'nachmittag'
             3912  COMPARE_OP               ==
         3914_3916  POP_JUMP_IF_FALSE  3932  'to 3932'

 L. 623      3918  LOAD_FAST                'used'
             3920  LOAD_CONST               2
             3922  INPLACE_ADD      
             3924  STORE_FAST               'used'

 L. 624      3926  LOAD_STR                 'pm'
             3928  STORE_FAST               'remainder'
             3930  JUMP_ABSOLUTE      4702  'to 4702'
           3932_0  COME_FROM          3914  '3914'
           3932_1  COME_FROM          3904  '3904'

 L. 625      3932  LOAD_FAST                'wordNextNext'
             3934  LOAD_CONST               None
             3936  LOAD_CONST               5
             3938  BUILD_SLICE_2         2 
             3940  BINARY_SUBSCR    
             3942  LOAD_STR                 'abend'
             3944  COMPARE_OP               ==
         3946_3948  POP_JUMP_IF_FALSE  3964  'to 3964'

 L. 626      3950  LOAD_FAST                'used'
             3952  LOAD_CONST               1
             3954  INPLACE_ADD      
             3956  STORE_FAST               'used'

 L. 627      3958  LOAD_STR                 'pm'
             3960  STORE_FAST               'remainder'
             3962  JUMP_ABSOLUTE      4702  'to 4702'
           3964_0  COME_FROM          3946  '3946'

 L. 628      3964  LOAD_FAST                'wordNextNext'
             3966  LOAD_STR                 'am'
             3968  COMPARE_OP               ==
         3970_3972  POP_JUMP_IF_FALSE  3998  'to 3998'
             3974  LOAD_FAST                'wordNextNextNext'

 L. 629      3976  LOAD_STR                 'abend'
             3978  COMPARE_OP               ==
         3980_3982  POP_JUMP_IF_FALSE  3998  'to 3998'

 L. 630      3984  LOAD_FAST                'used'
             3986  LOAD_CONST               2
             3988  INPLACE_ADD      
             3990  STORE_FAST               'used'

 L. 631      3992  LOAD_STR                 'pm'
             3994  STORE_FAST               'remainder'
             3996  JUMP_ABSOLUTE      4702  'to 4702'
           3998_0  COME_FROM          3980  '3980'
           3998_1  COME_FROM          3970  '3970'

 L. 632      3998  LOAD_FAST                'wordNextNext'
             4000  LOAD_CONST               None
             4002  LOAD_CONST               7
             4004  BUILD_SLICE_2         2 
             4006  BINARY_SUBSCR    
             4008  LOAD_STR                 'morgens'
             4010  COMPARE_OP               ==
         4012_4014  POP_JUMP_IF_FALSE  4030  'to 4030'

 L. 633      4016  LOAD_FAST                'used'
             4018  LOAD_CONST               1
             4020  INPLACE_ADD      
             4022  STORE_FAST               'used'

 L. 634      4024  LOAD_STR                 'am'
             4026  STORE_FAST               'remainder'
             4028  JUMP_ABSOLUTE      4702  'to 4702'
           4030_0  COME_FROM          4012  '4012'

 L. 635      4030  LOAD_FAST                'wordNextNext'
             4032  LOAD_STR                 'am'
             4034  COMPARE_OP               ==
         4036_4038  POP_JUMP_IF_FALSE  4064  'to 4064'
             4040  LOAD_FAST                'wordNextNextNext'

 L. 636      4042  LOAD_STR                 'morgen'
             4044  COMPARE_OP               ==
         4046_4048  POP_JUMP_IF_FALSE  4064  'to 4064'

 L. 637      4050  LOAD_FAST                'used'
             4052  LOAD_CONST               2
             4054  INPLACE_ADD      
             4056  STORE_FAST               'used'

 L. 638      4058  LOAD_STR                 'am'
             4060  STORE_FAST               'remainder'
             4062  JUMP_ABSOLUTE      4702  'to 4702'
           4064_0  COME_FROM          4046  '4046'
           4064_1  COME_FROM          4036  '4036'

 L. 639      4064  LOAD_FAST                'wordNextNext'
             4066  LOAD_STR                 'nachts'
             4068  COMPARE_OP               ==
         4070_4072  POP_JUMP_IF_FALSE  4418  'to 4418'

 L. 640      4074  LOAD_FAST                'used'
             4076  LOAD_CONST               1
             4078  INPLACE_ADD      
             4080  STORE_FAST               'used'

 L. 641      4082  LOAD_CONST               8
             4084  LOAD_GLOBAL              int
             4086  LOAD_FAST                'word'
             4088  CALL_FUNCTION_1       1  '1 positional argument'
             4090  DUP_TOP          
             4092  ROT_THREE        
             4094  COMPARE_OP               <=
         4096_4098  POP_JUMP_IF_FALSE  4110  'to 4110'
             4100  LOAD_CONST               12
             4102  COMPARE_OP               <=
         4104_4106  POP_JUMP_IF_FALSE  4120  'to 4120'
             4108  JUMP_FORWARD       4114  'to 4114'
           4110_0  COME_FROM          4096  '4096'
             4110  POP_TOP          
             4112  JUMP_FORWARD       4120  'to 4120'
           4114_0  COME_FROM          4108  '4108'

 L. 642      4114  LOAD_STR                 'pm'
             4116  STORE_FAST               'remainder'
             4118  JUMP_ABSOLUTE      4702  'to 4702'
           4120_0  COME_FROM          4112  '4112'
           4120_1  COME_FROM          4104  '4104'

 L. 644      4120  LOAD_STR                 'am'
             4122  STORE_FAST               'remainder'
         4124_4126  JUMP_ABSOLUTE      4702  'to 4702'
           4128_0  COME_FROM          3858  '3858'

 L. 646      4128  LOAD_GLOBAL              is_numeric
             4130  LOAD_FAST                'wordNextNext'
             4132  CALL_FUNCTION_1       1  '1 positional argument'
         4134_4136  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 647      4138  LOAD_FAST                'wordNextNext'
             4140  STORE_FAST               'strMM'

 L. 648      4142  LOAD_FAST                'used'
             4144  LOAD_CONST               1
             4146  INPLACE_ADD      
             4148  STORE_FAST               'used'

 L. 649      4150  LOAD_FAST                'wordNextNextNext'
             4152  LOAD_FAST                'timeQualifier'
             4154  COMPARE_OP               ==
         4156_4158  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 650      4160  LOAD_FAST                'wordNextNextNext'
             4162  LOAD_CONST               None
             4164  LOAD_CONST               10
             4166  BUILD_SLICE_2         2 
             4168  BINARY_SUBSCR    
             4170  LOAD_STR                 'nachmittag'
             4172  COMPARE_OP               ==
         4174_4176  POP_JUMP_IF_FALSE  4192  'to 4192'

 L. 651      4178  LOAD_FAST                'used'
             4180  LOAD_CONST               1
             4182  INPLACE_ADD      
             4184  STORE_FAST               'used'

 L. 652      4186  LOAD_STR                 'pm'
             4188  STORE_FAST               'remainder'
             4190  JUMP_FORWARD       4702  'to 4702'
           4192_0  COME_FROM          4174  '4174'

 L. 653      4192  LOAD_FAST                'wordNextNextNext'
             4194  LOAD_STR                 'am'
             4196  COMPARE_OP               ==
         4198_4200  POP_JUMP_IF_FALSE  4226  'to 4226'

 L. 654      4202  LOAD_FAST                'wordNextNextNextNext'
             4204  LOAD_STR                 'nachmittag'
             4206  COMPARE_OP               ==
         4208_4210  POP_JUMP_IF_FALSE  4226  'to 4226'

 L. 655      4212  LOAD_FAST                'used'
             4214  LOAD_CONST               2
             4216  INPLACE_ADD      
             4218  STORE_FAST               'used'

 L. 656      4220  LOAD_STR                 'pm'
             4222  STORE_FAST               'remainder'
             4224  JUMP_FORWARD       4702  'to 4702'
           4226_0  COME_FROM          4208  '4208'
           4226_1  COME_FROM          4198  '4198'

 L. 657      4226  LOAD_FAST                'wordNextNextNext'
             4228  LOAD_CONST               None
             4230  LOAD_CONST               5
             4232  BUILD_SLICE_2         2 
             4234  BINARY_SUBSCR    
             4236  LOAD_STR                 'abend'
             4238  COMPARE_OP               ==
         4240_4242  POP_JUMP_IF_FALSE  4258  'to 4258'

 L. 658      4244  LOAD_FAST                'used'
             4246  LOAD_CONST               1
             4248  INPLACE_ADD      
             4250  STORE_FAST               'used'

 L. 659      4252  LOAD_STR                 'pm'
             4254  STORE_FAST               'remainder'
             4256  JUMP_FORWARD       4702  'to 4702'
           4258_0  COME_FROM          4240  '4240'

 L. 660      4258  LOAD_FAST                'wordNextNextNext'
             4260  LOAD_STR                 'am'
             4262  COMPARE_OP               ==
         4264_4266  POP_JUMP_IF_FALSE  4292  'to 4292'

 L. 661      4268  LOAD_FAST                'wordNextNextNextNext'
             4270  LOAD_STR                 'abend'
             4272  COMPARE_OP               ==
         4274_4276  POP_JUMP_IF_FALSE  4292  'to 4292'

 L. 662      4278  LOAD_FAST                'used'
             4280  LOAD_CONST               2
             4282  INPLACE_ADD      
             4284  STORE_FAST               'used'

 L. 663      4286  LOAD_STR                 'pm'
             4288  STORE_FAST               'remainder'
             4290  JUMP_FORWARD       4702  'to 4702'
           4292_0  COME_FROM          4274  '4274'
           4292_1  COME_FROM          4264  '4264'

 L. 664      4292  LOAD_FAST                'wordNextNextNext'
             4294  LOAD_CONST               None
             4296  LOAD_CONST               7
             4298  BUILD_SLICE_2         2 
             4300  BINARY_SUBSCR    
             4302  LOAD_STR                 'morgens'
             4304  COMPARE_OP               ==
         4306_4308  POP_JUMP_IF_FALSE  4324  'to 4324'

 L. 665      4310  LOAD_FAST                'used'
             4312  LOAD_CONST               1
             4314  INPLACE_ADD      
             4316  STORE_FAST               'used'

 L. 666      4318  LOAD_STR                 'am'
             4320  STORE_FAST               'remainder'
             4322  JUMP_FORWARD       4702  'to 4702'
           4324_0  COME_FROM          4306  '4306'

 L. 667      4324  LOAD_FAST                'wordNextNextNext'
             4326  LOAD_STR                 'am'
             4328  COMPARE_OP               ==
         4330_4332  POP_JUMP_IF_FALSE  4358  'to 4358'

 L. 668      4334  LOAD_FAST                'wordNextNextNextNext'
             4336  LOAD_STR                 'morgen'
             4338  COMPARE_OP               ==
         4340_4342  POP_JUMP_IF_FALSE  4358  'to 4358'

 L. 669      4344  LOAD_FAST                'used'
             4346  LOAD_CONST               2
             4348  INPLACE_ADD      
             4350  STORE_FAST               'used'

 L. 670      4352  LOAD_STR                 'am'
             4354  STORE_FAST               'remainder'
             4356  JUMP_FORWARD       4702  'to 4702'
           4358_0  COME_FROM          4340  '4340'
           4358_1  COME_FROM          4330  '4330'

 L. 671      4358  LOAD_FAST                'wordNextNextNext'
             4360  LOAD_STR                 'nachts'
             4362  COMPARE_OP               ==
         4364_4366  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 672      4368  LOAD_FAST                'used'
             4370  LOAD_CONST               1
             4372  INPLACE_ADD      
             4374  STORE_FAST               'used'

 L. 673      4376  LOAD_CONST               8
             4378  LOAD_GLOBAL              int
             4380  LOAD_FAST                'word'
             4382  CALL_FUNCTION_1       1  '1 positional argument'
             4384  DUP_TOP          
             4386  ROT_THREE        
             4388  COMPARE_OP               <=
         4390_4392  POP_JUMP_IF_FALSE  4404  'to 4404'
             4394  LOAD_CONST               12
             4396  COMPARE_OP               <=
         4398_4400  POP_JUMP_IF_FALSE  4414  'to 4414'
             4402  JUMP_FORWARD       4408  'to 4408'
           4404_0  COME_FROM          4390  '4390'
             4404  POP_TOP          
             4406  JUMP_FORWARD       4414  'to 4414'
           4408_0  COME_FROM          4402  '4402'

 L. 674      4408  LOAD_STR                 'pm'
             4410  STORE_FAST               'remainder'
             4412  JUMP_FORWARD       4702  'to 4702'
           4414_0  COME_FROM          4406  '4406'
           4414_1  COME_FROM          4398  '4398'

 L. 676      4414  LOAD_STR                 'am'
             4416  STORE_FAST               'remainder'
           4418_0  COME_FROM          4070  '4070'
         4418_4420  JUMP_FORWARD       4702  'to 4702'
           4422_0  COME_FROM          3832  '3832'

 L. 678      4422  LOAD_FAST                'wordNext'
             4424  LOAD_FAST                'timeQualifier'
             4426  COMPARE_OP               ==
         4428_4430  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 679      4432  LOAD_FAST                'word'
             4434  STORE_FAST               'strHH'

 L. 680      4436  LOAD_CONST               0
             4438  STORE_FAST               'strMM'

 L. 681      4440  LOAD_CONST               True
             4442  STORE_FAST               'isTime'

 L. 682      4444  LOAD_FAST                'wordNext'
             4446  LOAD_CONST               None
           4448_0  COME_FROM          3224  '3224'
             4448  LOAD_CONST               10
             4450  BUILD_SLICE_2         2 
             4452  BINARY_SUBSCR    
             4454  LOAD_STR                 'nachmittag'
             4456  COMPARE_OP               ==
         4458_4460  POP_JUMP_IF_FALSE  4476  'to 4476'

 L. 683      4462  LOAD_FAST                'used'
             4464  LOAD_CONST               1
             4466  INPLACE_ADD      
             4468  STORE_FAST               'used'

 L. 684      4470  LOAD_STR                 'pm'
           4472_0  COME_FROM          4190  '4190'
           4472_1  COME_FROM          3248  '3248'
             4472  STORE_FAST               'remainder'
             4474  JUMP_FORWARD       4702  'to 4702'
           4476_0  COME_FROM          4458  '4458'

 L. 685      4476  LOAD_FAST                'wordNext'
             4478  LOAD_STR                 'am'
             4480  COMPARE_OP               ==
         4482_4484  POP_JUMP_IF_FALSE  4510  'to 4510'
             4486  LOAD_FAST                'wordNextNext'
             4488  LOAD_STR                 'nachmittag'
             4490  COMPARE_OP               ==
         4492_4494  POP_JUMP_IF_FALSE  4510  'to 4510'
           4496_0  COME_FROM          3272  '3272'

 L. 686      4496  LOAD_FAST                'used'
             4498  LOAD_CONST               2
             4500  INPLACE_ADD      
             4502  STORE_FAST               'used'

 L. 687      4504  LOAD_STR                 'pm'
           4506_0  COME_FROM          4224  '4224'
             4506  STORE_FAST               'remainder'
             4508  JUMP_FORWARD       4702  'to 4702'
           4510_0  COME_FROM          4492  '4492'
           4510_1  COME_FROM          4482  '4482'

 L. 688      4510  LOAD_FAST                'wordNext'
             4512  LOAD_CONST               None
             4514  LOAD_CONST               5
             4516  BUILD_SLICE_2         2 
             4518  BINARY_SUBSCR    
           4520_0  COME_FROM          3296  '3296'
             4520  LOAD_STR                 'abend'
             4522  COMPARE_OP               ==
         4524_4526  POP_JUMP_IF_FALSE  4542  'to 4542'

 L. 689      4528  LOAD_FAST                'used'
             4530  LOAD_CONST               1
             4532  INPLACE_ADD      
             4534  STORE_FAST               'used'

 L. 690      4536  LOAD_STR                 'pm'
           4538_0  COME_FROM          4256  '4256'
             4538  STORE_FAST               'remainder'
             4540  JUMP_FORWARD       4702  'to 4702'
           4542_0  COME_FROM          4524  '4524'

 L. 691      4542  LOAD_FAST                'wordNext'
             4544  LOAD_STR                 'am'
             4546  COMPARE_OP               ==
         4548_4550  POP_JUMP_IF_FALSE  4576  'to 4576'
             4552  LOAD_FAST                'wordNextNext'
             4554  LOAD_STR                 'abend'
             4556  COMPARE_OP               ==
         4558_4560  POP_JUMP_IF_FALSE  4576  'to 4576'

 L. 692      4562  LOAD_FAST                'used'
             4564  LOAD_CONST               2
             4566  INPLACE_ADD      
             4568  STORE_FAST               'used'

 L. 693      4570  LOAD_STR                 'pm'
           4572_0  COME_FROM          4290  '4290'
             4572  STORE_FAST               'remainder'
             4574  JUMP_FORWARD       4702  'to 4702'
           4576_0  COME_FROM          4558  '4558'
           4576_1  COME_FROM          4548  '4548'

 L. 694      4576  LOAD_FAST                'wordNext'
             4578  LOAD_CONST               None
           4580_0  COME_FROM          3356  '3356'
             4580  LOAD_CONST               7
             4582  BUILD_SLICE_2         2 
             4584  BINARY_SUBSCR    
             4586  LOAD_STR                 'morgens'
             4588  COMPARE_OP               ==
         4590_4592  POP_JUMP_IF_FALSE  4608  'to 4608'

 L. 695      4594  LOAD_FAST                'used'
             4596  LOAD_CONST               1
             4598  INPLACE_ADD      
             4600  STORE_FAST               'used'

 L. 696      4602  LOAD_STR                 'am'
           4604_0  COME_FROM          4322  '4322'
             4604  STORE_FAST               'remainder'
             4606  JUMP_FORWARD       4702  'to 4702'
           4608_0  COME_FROM          4590  '4590'

 L. 697      4608  LOAD_FAST                'wordNext'
           4610_0  COME_FROM          3386  '3386'
             4610  LOAD_STR                 'am'
             4612  COMPARE_OP               ==
         4614_4616  POP_JUMP_IF_FALSE  4642  'to 4642'
             4618  LOAD_FAST                'wordNextNext'
             4620  LOAD_STR                 'morgen'
             4622  COMPARE_OP               ==
         4624_4626  POP_JUMP_IF_FALSE  4642  'to 4642'

 L. 698      4628  LOAD_FAST                'used'
             4630  LOAD_CONST               2
             4632  INPLACE_ADD      
             4634  STORE_FAST               'used'

 L. 699      4636  LOAD_STR                 'am'
           4638_0  COME_FROM          4356  '4356'
             4638  STORE_FAST               'remainder'
             4640  JUMP_FORWARD       4702  'to 4702'
           4642_0  COME_FROM          4624  '4624'
           4642_1  COME_FROM          4614  '4614'

 L. 700      4642  LOAD_FAST                'wordNext'
             4644  LOAD_STR                 'nachts'
             4646  COMPARE_OP               ==
         4648_4650  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 701      4652  LOAD_FAST                'used'
             4654  LOAD_CONST               1
             4656  INPLACE_ADD      
             4658  STORE_FAST               'used'

 L. 702      4660  LOAD_CONST               8
             4662  LOAD_GLOBAL              int
             4664  LOAD_FAST                'word'
             4666  CALL_FUNCTION_1       1  '1 positional argument'
             4668  DUP_TOP          
             4670  ROT_THREE        
             4672  COMPARE_OP               <=
         4674_4676  POP_JUMP_IF_FALSE  4688  'to 4688'
             4678  LOAD_CONST               12
             4680  COMPARE_OP               <=
         4682_4684  POP_JUMP_IF_FALSE  4698  'to 4698'
             4686  JUMP_FORWARD       4692  'to 4692'
           4688_0  COME_FROM          4674  '4674'
             4688  POP_TOP          
             4690  JUMP_FORWARD       4698  'to 4698'
           4692_0  COME_FROM          4686  '4686'

 L. 703      4692  LOAD_STR                 'pm'
           4694_0  COME_FROM          4412  '4412'
             4694  STORE_FAST               'remainder'
             4696  JUMP_FORWARD       4702  'to 4702'
           4698_0  COME_FROM          4690  '4690'
           4698_1  COME_FROM          4682  '4682'

 L. 705      4698  LOAD_STR                 'am'
             4700  STORE_FAST               'remainder'
           4702_0  COME_FROM          4696  '4696'
           4702_1  COME_FROM          4648  '4648'
           4702_2  COME_FROM          4640  '4640'
           4702_3  COME_FROM          4606  '4606'
           4702_4  COME_FROM          4574  '4574'
           4702_5  COME_FROM          4540  '4540'
           4702_6  COME_FROM          4508  '4508'
           4702_7  COME_FROM          4474  '4474'
           4702_8  COME_FROM          4428  '4428'
           4702_9  COME_FROM          4418  '4418'
          4702_10  COME_FROM          4364  '4364'
          4702_11  COME_FROM          4156  '4156'
          4702_12  COME_FROM          4134  '4134'
          4702_13  COME_FROM          3822  '3822'
          4702_14  COME_FROM          3784  '3784'
          4702_15  COME_FROM          3746  '3746'
          4702_16  COME_FROM          3694  '3694'
          4702_17  COME_FROM          3638  '3638'
          4702_18  COME_FROM          3476  '3476'
          4702_19  COME_FROM          3464  '3464'
          4702_20  COME_FROM          3444  '3444'
          4702_21  COME_FROM          3434  '3434'
          4702_22  COME_FROM          3042  '3042'

 L. 712      4702  LOAD_FAST                'strHH'
         4704_4706  POP_JUMP_IF_FALSE  4716  'to 4716'
             4708  LOAD_GLOBAL              int
             4710  LOAD_FAST                'strHH'
             4712  CALL_FUNCTION_1       1  '1 positional argument'
             4714  JUMP_FORWARD       4718  'to 4718'
           4716_0  COME_FROM          4704  '4704'
             4716  LOAD_CONST               0
           4718_0  COME_FROM          4714  '4714'
             4718  STORE_FAST               'strHH'

 L. 713      4720  LOAD_FAST                'strMM'
         4722_4724  POP_JUMP_IF_FALSE  4734  'to 4734'
             4726  LOAD_GLOBAL              int
             4728  LOAD_FAST                'strMM'
             4730  CALL_FUNCTION_1       1  '1 positional argument'
             4732  JUMP_FORWARD       4736  'to 4736'
           4734_0  COME_FROM          4722  '4722'
             4734  LOAD_CONST               0
           4736_0  COME_FROM          4732  '4732'
             4736  STORE_FAST               'strMM'

 L. 714      4738  LOAD_FAST                'remainder'
             4740  LOAD_STR                 'pm'
             4742  COMPARE_OP               ==
         4744_4746  POP_JUMP_IF_FALSE  4766  'to 4766'
             4748  LOAD_FAST                'strHH'
             4750  LOAD_CONST               12
             4752  COMPARE_OP               <
         4754_4756  POP_JUMP_IF_FALSE  4766  'to 4766'
             4758  LOAD_FAST                'strHH'
             4760  LOAD_CONST               12
             4762  BINARY_ADD       
             4764  JUMP_FORWARD       4768  'to 4768'
           4766_0  COME_FROM          4754  '4754'
           4766_1  COME_FROM          4744  '4744'
             4766  LOAD_FAST                'strHH'
           4768_0  COME_FROM          4764  '4764'
             4768  STORE_FAST               'strHH'

 L. 715      4770  LOAD_FAST                'remainder'
             4772  LOAD_STR                 'am'
             4774  COMPARE_OP               ==
         4776_4778  POP_JUMP_IF_FALSE  4798  'to 4798'
             4780  LOAD_FAST                'strHH'
             4782  LOAD_CONST               12
             4784  COMPARE_OP               >=
         4786_4788  POP_JUMP_IF_FALSE  4798  'to 4798'
             4790  LOAD_FAST                'strHH'
             4792  LOAD_CONST               12
             4794  BINARY_SUBTRACT  
             4796  JUMP_FORWARD       4800  'to 4800'
           4798_0  COME_FROM          4786  '4786'
           4798_1  COME_FROM          4776  '4776'
             4798  LOAD_FAST                'strHH'
           4800_0  COME_FROM          4796  '4796'
             4800  STORE_FAST               'strHH'

 L. 716      4802  LOAD_FAST                'strHH'
             4804  LOAD_CONST               24
             4806  COMPARE_OP               >
         4808_4810  POP_JUMP_IF_TRUE   4822  'to 4822'
             4812  LOAD_FAST                'strMM'
             4814  LOAD_CONST               59
             4816  COMPARE_OP               >
         4818_4820  POP_JUMP_IF_FALSE  4830  'to 4830'
           4822_0  COME_FROM          4808  '4808'

 L. 717      4822  LOAD_CONST               False
             4824  STORE_FAST               'isTime'

 L. 718      4826  LOAD_CONST               0
             4828  STORE_FAST               'used'
           4830_0  COME_FROM          4818  '4818'

 L. 719      4830  LOAD_FAST                'isTime'
         4832_4834  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 720      4836  LOAD_FAST                'strHH'
             4838  LOAD_CONST               1
             4840  BINARY_MULTIPLY  
             4842  STORE_DEREF              'hrAbs'

 L. 721      4844  LOAD_FAST                'strMM'
             4846  LOAD_CONST               1
             4848  BINARY_MULTIPLY  
             4850  STORE_DEREF              'minAbs'

 L. 722      4852  LOAD_FAST                'used'
             4854  LOAD_CONST               1
             4856  INPLACE_ADD      
             4858  STORE_FAST               'used'
           4860_0  COME_FROM          4832  '4832'
           4860_1  COME_FROM          2818  '2818'
           4860_2  COME_FROM          2804  '2804'
           4860_3  COME_FROM          2660  '2660'
           4860_4  COME_FROM          2620  '2620'
           4860_5  COME_FROM          2580  '2580'
           4860_6  COME_FROM          2518  '2518'
           4860_7  COME_FROM          2484  '2484'

 L. 723      4860  LOAD_FAST                'used'
             4862  LOAD_CONST               0
             4864  COMPARE_OP               >
         4866_4868  POP_JUMP_IF_FALSE  2238  'to 2238'

 L. 725      4870  SETUP_LOOP         4902  'to 4902'
             4872  LOAD_GLOBAL              range
             4874  LOAD_FAST                'used'
             4876  CALL_FUNCTION_1       1  '1 positional argument'
             4878  GET_ITER         
             4880  FOR_ITER           4900  'to 4900'
             4882  STORE_FAST               'i'

 L. 726      4884  LOAD_STR                 ''
             4886  LOAD_FAST                'words'
             4888  LOAD_FAST                'idx'
             4890  LOAD_FAST                'i'
             4892  BINARY_ADD       
             4894  STORE_SUBSCR     
         4896_4898  JUMP_BACK          4880  'to 4880'
             4900  POP_BLOCK        
           4902_0  COME_FROM_LOOP     4870  '4870'

 L. 728      4902  LOAD_FAST                'wordPrev'
             4904  LOAD_STR                 'Uhr'
             4906  COMPARE_OP               ==
         4908_4910  POP_JUMP_IF_FALSE  4926  'to 4926'

 L. 729      4912  LOAD_STR                 ''
             4914  LOAD_FAST                'words'
             4916  LOAD_FAST                'words'
             4918  LOAD_METHOD              index
             4920  LOAD_FAST                'wordPrev'
             4922  CALL_METHOD_1         1  '1 positional argument'
             4924  STORE_SUBSCR     
           4926_0  COME_FROM          4908  '4908'

 L. 731      4926  LOAD_FAST                'wordPrev'
             4928  LOAD_STR                 'früh'
             4930  COMPARE_OP               ==
         4932_4934  POP_JUMP_IF_FALSE  4962  'to 4962'

 L. 732      4936  LOAD_CONST               -1
             4938  STORE_DEREF              'hrOffset'

 L. 733      4940  LOAD_STR                 ''
             4942  LOAD_FAST                'words'
             4944  LOAD_FAST                'idx'
             4946  LOAD_CONST               1
             4948  BINARY_SUBTRACT  
             4950  STORE_SUBSCR     

 L. 734      4952  LOAD_FAST                'idx'
             4954  LOAD_CONST               1
             4956  INPLACE_SUBTRACT 
             4958  STORE_FAST               'idx'
             4960  JUMP_FORWARD       4996  'to 4996'
           4962_0  COME_FROM          4932  '4932'

 L. 735      4962  LOAD_FAST                'wordPrev'
             4964  LOAD_STR                 'spät'
             4966  COMPARE_OP               ==
         4968_4970  POP_JUMP_IF_FALSE  4996  'to 4996'

 L. 736      4972  LOAD_CONST               1
             4974  STORE_DEREF              'hrOffset'

 L. 737      4976  LOAD_STR                 ''
             4978  LOAD_FAST                'words'
             4980  LOAD_FAST                'idx'
             4982  LOAD_CONST               1
             4984  BINARY_SUBTRACT  
             4986  STORE_SUBSCR     

 L. 738      4988  LOAD_FAST                'idx'
             4990  LOAD_CONST               1
             4992  INPLACE_SUBTRACT 
             4994  STORE_FAST               'idx'
           4996_0  COME_FROM          4968  '4968'
           4996_1  COME_FROM          4960  '4960'

 L. 739      4996  LOAD_FAST                'idx'
             4998  LOAD_CONST               0
             5000  COMPARE_OP               >
         5002_5004  POP_JUMP_IF_FALSE  5028  'to 5028'
             5006  LOAD_FAST                'wordPrev'
             5008  LOAD_FAST                'markers'
             5010  COMPARE_OP               in
         5012_5014  POP_JUMP_IF_FALSE  5028  'to 5028'

 L. 740      5016  LOAD_STR                 ''
             5018  LOAD_FAST                'words'
             5020  LOAD_FAST                'idx'
             5022  LOAD_CONST               1
             5024  BINARY_SUBTRACT  
             5026  STORE_SUBSCR     
           5028_0  COME_FROM          5012  '5012'
           5028_1  COME_FROM          5002  '5002'

 L. 741      5028  LOAD_FAST                'idx'
             5030  LOAD_CONST               1
             5032  COMPARE_OP               >
         5034_5036  POP_JUMP_IF_FALSE  5060  'to 5060'
             5038  LOAD_FAST                'wordPrevPrev'
             5040  LOAD_FAST                'markers'
             5042  COMPARE_OP               in
         5044_5046  POP_JUMP_IF_FALSE  5060  'to 5060'

 L. 742      5048  LOAD_STR                 ''
             5050  LOAD_FAST                'words'
             5052  LOAD_FAST                'idx'
             5054  LOAD_CONST               2
             5056  BINARY_SUBTRACT  
             5058  STORE_SUBSCR     
           5060_0  COME_FROM          5044  '5044'
           5060_1  COME_FROM          5034  '5034'

 L. 744      5060  LOAD_FAST                'idx'
             5062  LOAD_FAST                'used'
             5064  LOAD_CONST               1
             5066  BINARY_SUBTRACT  
             5068  INPLACE_ADD      
             5070  STORE_FAST               'idx'

 L. 745      5072  LOAD_CONST               True
             5074  STORE_DEREF              'found'
         5076_5078  JUMP_BACK          2238  'to 2238'
             5080  POP_BLOCK        
           5082_0  COME_FROM_LOOP     2226  '2226'

 L. 748      5082  LOAD_FAST                'date_found'
         5084_5086  POP_JUMP_IF_TRUE   5092  'to 5092'

 L. 749      5088  LOAD_CONST               None
             5090  RETURN_VALUE     
           5092_0  COME_FROM          5084  '5084'

 L. 751      5092  LOAD_DEREF               'dayOffset'
             5094  LOAD_CONST               False
             5096  COMPARE_OP               is
         5098_5100  POP_JUMP_IF_FALSE  5106  'to 5106'

 L. 752      5102  LOAD_CONST               0
             5104  STORE_DEREF              'dayOffset'
           5106_0  COME_FROM          5098  '5098'

 L. 756      5106  LOAD_FAST                'dateNow'
             5108  STORE_FAST               'extractedDate'

 L. 757      5110  LOAD_FAST                'extractedDate'
             5112  LOAD_ATTR                replace
             5114  LOAD_CONST               0

 L. 758      5116  LOAD_CONST               0

 L. 759      5118  LOAD_CONST               0

 L. 760      5120  LOAD_CONST               0
             5122  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             5124  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5126  STORE_FAST               'extractedDate'

 L. 761      5128  LOAD_DEREF               'datestr'
             5130  LOAD_STR                 ''
             5132  COMPARE_OP               !=
         5134_5136  POP_JUMP_IF_FALSE  5450  'to 5450'

 L. 762      5138  LOAD_STR                 'january'
             5140  LOAD_STR                 'february'
             5142  LOAD_STR                 'march'
             5144  LOAD_STR                 'april'
             5146  LOAD_STR                 'may'
             5148  LOAD_STR                 'june'

 L. 763      5150  LOAD_STR                 'july'
             5152  LOAD_STR                 'august'
             5154  LOAD_STR                 'september'
             5156  LOAD_STR                 'october'
             5158  LOAD_STR                 'november'

 L. 764      5160  LOAD_STR                 'december'
             5162  BUILD_LIST_12        12 
             5164  STORE_FAST               'en_months'

 L. 765      5166  LOAD_STR                 'jan'
             5168  LOAD_STR                 'feb'
             5170  LOAD_STR                 'mar'
             5172  LOAD_STR                 'apr'
             5174  LOAD_STR                 'may'
             5176  LOAD_STR                 'june'
             5178  LOAD_STR                 'july'

 L. 766      5180  LOAD_STR                 'aug'

 L. 767      5182  LOAD_STR                 'sept'
             5184  LOAD_STR                 'oct'
             5186  LOAD_STR                 'nov'
             5188  LOAD_STR                 'dec'
             5190  BUILD_LIST_12        12 
             5192  STORE_FAST               'en_monthsShort'

 L. 768      5194  SETUP_LOOP         5234  'to 5234'
             5196  LOAD_GLOBAL              enumerate
             5198  LOAD_FAST                'en_months'
             5200  CALL_FUNCTION_1       1  '1 positional argument'
             5202  GET_ITER         
             5204  FOR_ITER           5232  'to 5232'
             5206  UNPACK_SEQUENCE_2     2 
             5208  STORE_FAST               'idx'
             5210  STORE_FAST               'en_month'

 L. 769      5212  LOAD_DEREF               'datestr'
             5214  LOAD_METHOD              replace
             5216  LOAD_FAST                'months'
             5218  LOAD_FAST                'idx'
             5220  BINARY_SUBSCR    
             5222  LOAD_FAST                'en_month'
             5224  CALL_METHOD_2         2  '2 positional arguments'
             5226  STORE_DEREF              'datestr'
         5228_5230  JUMP_BACK          5204  'to 5204'
             5232  POP_BLOCK        
           5234_0  COME_FROM_LOOP     5194  '5194'

 L. 770      5234  SETUP_LOOP         5274  'to 5274'
             5236  LOAD_GLOBAL              enumerate
             5238  LOAD_FAST                'en_monthsShort'
             5240  CALL_FUNCTION_1       1  '1 positional argument'
             5242  GET_ITER         
             5244  FOR_ITER           5272  'to 5272'
             5246  UNPACK_SEQUENCE_2     2 
             5248  STORE_FAST               'idx'
             5250  STORE_FAST               'en_month'

 L. 771      5252  LOAD_DEREF               'datestr'
             5254  LOAD_METHOD              replace
             5256  LOAD_FAST                'monthsShort'
             5258  LOAD_FAST                'idx'
             5260  BINARY_SUBSCR    
             5262  LOAD_FAST                'en_month'
             5264  CALL_METHOD_2         2  '2 positional arguments'
             5266  STORE_DEREF              'datestr'
         5268_5270  JUMP_BACK          5244  'to 5244'
             5272  POP_BLOCK        
           5274_0  COME_FROM_LOOP     5234  '5234'

 L. 773      5274  LOAD_GLOBAL              datetime
             5276  LOAD_METHOD              strptime
             5278  LOAD_DEREF               'datestr'
             5280  LOAD_STR                 '%B %d'
             5282  CALL_METHOD_2         2  '2 positional arguments'
             5284  STORE_FAST               'temp'

 L. 774      5286  LOAD_FAST                'hasYear'
         5288_5290  POP_JUMP_IF_TRUE   5404  'to 5404'

 L. 775      5292  LOAD_FAST                'temp'
             5294  LOAD_ATTR                replace
             5296  LOAD_FAST                'extractedDate'
             5298  LOAD_ATTR                year
             5300  LOAD_CONST               ('year',)
             5302  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5304  STORE_FAST               'temp'

 L. 776      5306  LOAD_FAST                'extractedDate'
             5308  LOAD_FAST                'temp'
             5310  COMPARE_OP               <
         5312_5314  POP_JUMP_IF_FALSE  5358  'to 5358'

 L. 777      5316  LOAD_FAST                'extractedDate'
             5318  LOAD_ATTR                replace
             5320  LOAD_GLOBAL              int
             5322  LOAD_FAST                'currentYear'
             5324  CALL_FUNCTION_1       1  '1 positional argument'

 L. 778      5326  LOAD_GLOBAL              int

 L. 779      5328  LOAD_FAST                'temp'
             5330  LOAD_METHOD              strftime

 L. 780      5332  LOAD_STR                 '%m'
             5334  CALL_METHOD_1         1  '1 positional argument'
             5336  CALL_FUNCTION_1       1  '1 positional argument'

 L. 781      5338  LOAD_GLOBAL              int
             5340  LOAD_FAST                'temp'
             5342  LOAD_METHOD              strftime

 L. 782      5344  LOAD_STR                 '%d'
             5346  CALL_METHOD_1         1  '1 positional argument'
             5348  CALL_FUNCTION_1       1  '1 positional argument'
             5350  LOAD_CONST               ('year', 'month', 'day')
             5352  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5354  STORE_FAST               'extractedDate'
             5356  JUMP_FORWARD       5402  'to 5402'
           5358_0  COME_FROM          5312  '5312'

 L. 784      5358  LOAD_FAST                'extractedDate'
             5360  LOAD_ATTR                replace

 L. 785      5362  LOAD_GLOBAL              int
             5364  LOAD_FAST                'currentYear'
             5366  CALL_FUNCTION_1       1  '1 positional argument'
             5368  LOAD_CONST               1
             5370  BINARY_ADD       

 L. 786      5372  LOAD_GLOBAL              int
             5374  LOAD_FAST                'temp'
             5376  LOAD_METHOD              strftime
             5378  LOAD_STR                 '%m'
             5380  CALL_METHOD_1         1  '1 positional argument'
             5382  CALL_FUNCTION_1       1  '1 positional argument'

 L. 787      5384  LOAD_GLOBAL              int
             5386  LOAD_FAST                'temp'
             5388  LOAD_METHOD              strftime
             5390  LOAD_STR                 '%d'
             5392  CALL_METHOD_1         1  '1 positional argument'
             5394  CALL_FUNCTION_1       1  '1 positional argument'
             5396  LOAD_CONST               ('year', 'month', 'day')
             5398  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5400  STORE_FAST               'extractedDate'
           5402_0  COME_FROM          5356  '5356'
             5402  JUMP_FORWARD       5450  'to 5450'
           5404_0  COME_FROM          5288  '5288'

 L. 789      5404  LOAD_FAST                'extractedDate'
             5406  LOAD_ATTR                replace

 L. 790      5408  LOAD_GLOBAL              int
             5410  LOAD_FAST                'temp'
             5412  LOAD_METHOD              strftime
             5414  LOAD_STR                 '%Y'
             5416  CALL_METHOD_1         1  '1 positional argument'
             5418  CALL_FUNCTION_1       1  '1 positional argument'

 L. 791      5420  LOAD_GLOBAL              int
             5422  LOAD_FAST                'temp'
             5424  LOAD_METHOD              strftime
             5426  LOAD_STR                 '%m'
             5428  CALL_METHOD_1         1  '1 positional argument'
             5430  CALL_FUNCTION_1       1  '1 positional argument'

 L. 792      5432  LOAD_GLOBAL              int
             5434  LOAD_FAST                'temp'
             5436  LOAD_METHOD              strftime
             5438  LOAD_STR                 '%d'
             5440  CALL_METHOD_1         1  '1 positional argument'
             5442  CALL_FUNCTION_1       1  '1 positional argument'
             5444  LOAD_CONST               ('year', 'month', 'day')
             5446  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5448  STORE_FAST               'extractedDate'
           5450_0  COME_FROM          5402  '5402'
           5450_1  COME_FROM          5134  '5134'

 L. 794      5450  LOAD_DEREF               'timeStr'
             5452  LOAD_STR                 ''
             5454  COMPARE_OP               !=
         5456_5458  POP_JUMP_IF_FALSE  5502  'to 5502'

 L. 795      5460  LOAD_GLOBAL              datetime
             5462  LOAD_DEREF               'timeStr'
             5464  CALL_FUNCTION_1       1  '1 positional argument'
             5466  STORE_FAST               'temp'

 L. 796      5468  LOAD_FAST                'extractedDate'
             5470  LOAD_ATTR                replace
             5472  LOAD_FAST                'temp'
             5474  LOAD_METHOD              strftime
             5476  LOAD_STR                 '%H'
             5478  CALL_METHOD_1         1  '1 positional argument'

 L. 797      5480  LOAD_FAST                'temp'
             5482  LOAD_METHOD              strftime
             5484  LOAD_STR                 '%M'
             5486  CALL_METHOD_1         1  '1 positional argument'

 L. 798      5488  LOAD_FAST                'temp'
             5490  LOAD_METHOD              strftime
             5492  LOAD_STR                 '%S'
             5494  CALL_METHOD_1         1  '1 positional argument'
             5496  LOAD_CONST               ('hour', 'minute', 'second')
             5498  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5500  STORE_FAST               'extractedDate'
           5502_0  COME_FROM          5456  '5456'

 L. 800      5502  LOAD_DEREF               'yearOffset'
             5504  LOAD_CONST               0
             5506  COMPARE_OP               !=
         5508_5510  POP_JUMP_IF_FALSE  5526  'to 5526'

 L. 801      5512  LOAD_FAST                'extractedDate'
             5514  LOAD_GLOBAL              relativedelta
             5516  LOAD_DEREF               'yearOffset'
             5518  LOAD_CONST               ('years',)
             5520  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5522  BINARY_ADD       
             5524  STORE_FAST               'extractedDate'
           5526_0  COME_FROM          5508  '5508'

 L. 802      5526  LOAD_DEREF               'monthOffset'
             5528  LOAD_CONST               0
             5530  COMPARE_OP               !=
         5532_5534  POP_JUMP_IF_FALSE  5550  'to 5550'

 L. 803      5536  LOAD_FAST                'extractedDate'
             5538  LOAD_GLOBAL              relativedelta
             5540  LOAD_DEREF               'monthOffset'
             5542  LOAD_CONST               ('months',)
             5544  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5546  BINARY_ADD       
             5548  STORE_FAST               'extractedDate'
           5550_0  COME_FROM          5532  '5532'

 L. 804      5550  LOAD_DEREF               'dayOffset'
             5552  LOAD_CONST               0
             5554  COMPARE_OP               !=
         5556_5558  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 805      5560  LOAD_FAST                'extractedDate'
             5562  LOAD_GLOBAL              relativedelta
             5564  LOAD_DEREF               'dayOffset'
             5566  LOAD_CONST               ('days',)
             5568  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5570  BINARY_ADD       
             5572  STORE_FAST               'extractedDate'
           5574_0  COME_FROM          5556  '5556'

 L. 807      5574  LOAD_DEREF               'hrAbs'
             5576  LOAD_CONST               None
             5578  COMPARE_OP               is
         5580_5582  POP_JUMP_IF_FALSE  5612  'to 5612'
             5584  LOAD_DEREF               'minAbs'
             5586  LOAD_CONST               None
             5588  COMPARE_OP               is
         5590_5592  POP_JUMP_IF_FALSE  5612  'to 5612'
             5594  LOAD_FAST                'default_time'
         5596_5598  POP_JUMP_IF_FALSE  5612  'to 5612'

 L. 808      5600  LOAD_FAST                'default_time'
             5602  LOAD_ATTR                hour
             5604  STORE_DEREF              'hrAbs'

 L. 809      5606  LOAD_FAST                'default_time'
             5608  LOAD_ATTR                minute
             5610  STORE_DEREF              'minAbs'
           5612_0  COME_FROM          5596  '5596'
           5612_1  COME_FROM          5590  '5590'
           5612_2  COME_FROM          5580  '5580'

 L. 811      5612  LOAD_DEREF               'hrAbs'
             5614  LOAD_CONST               -1
             5616  COMPARE_OP               !=
         5618_5620  POP_JUMP_IF_FALSE  5712  'to 5712'
             5622  LOAD_DEREF               'minAbs'
             5624  LOAD_CONST               -1
             5626  COMPARE_OP               !=
         5628_5630  POP_JUMP_IF_FALSE  5712  'to 5712'

 L. 813      5632  LOAD_FAST                'extractedDate'
             5634  LOAD_GLOBAL              relativedelta
             5636  LOAD_DEREF               'hrAbs'
         5638_5640  JUMP_IF_TRUE_OR_POP  5644  'to 5644'
             5642  LOAD_CONST               0
           5644_0  COME_FROM          5638  '5638'

 L. 814      5644  LOAD_DEREF               'minAbs'
         5646_5648  JUMP_IF_TRUE_OR_POP  5652  'to 5652'
             5650  LOAD_CONST               0
           5652_0  COME_FROM          5646  '5646'
             5652  LOAD_CONST               ('hours', 'minutes')
             5654  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5656  BINARY_ADD       
             5658  STORE_FAST               'extractedDate'

 L. 815      5660  LOAD_DEREF               'hrAbs'
         5662_5664  POP_JUMP_IF_TRUE   5672  'to 5672'
             5666  LOAD_DEREF               'minAbs'
         5668_5670  POP_JUMP_IF_FALSE  5712  'to 5712'
           5672_0  COME_FROM          5662  '5662'
             5672  LOAD_DEREF               'datestr'
             5674  LOAD_STR                 ''
             5676  COMPARE_OP               ==
         5678_5680  POP_JUMP_IF_FALSE  5712  'to 5712'

 L. 816      5682  LOAD_FAST                'daySpecified'
         5684_5686  POP_JUMP_IF_TRUE   5712  'to 5712'
             5688  LOAD_FAST                'dateNow'
             5690  LOAD_FAST                'extractedDate'
             5692  COMPARE_OP               >
         5694_5696  POP_JUMP_IF_FALSE  5712  'to 5712'

 L. 817      5698  LOAD_FAST                'extractedDate'
             5700  LOAD_GLOBAL              relativedelta
             5702  LOAD_CONST               1
             5704  LOAD_CONST               ('days',)
             5706  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5708  BINARY_ADD       
             5710  STORE_FAST               'extractedDate'
           5712_0  COME_FROM          5694  '5694'
           5712_1  COME_FROM          5684  '5684'
           5712_2  COME_FROM          5678  '5678'
           5712_3  COME_FROM          5668  '5668'
           5712_4  COME_FROM          5628  '5628'
           5712_5  COME_FROM          5618  '5618'

 L. 818      5712  LOAD_DEREF               'hrOffset'
             5714  LOAD_CONST               0
             5716  COMPARE_OP               !=
         5718_5720  POP_JUMP_IF_FALSE  5736  'to 5736'

 L. 819      5722  LOAD_FAST                'extractedDate'
             5724  LOAD_GLOBAL              relativedelta
             5726  LOAD_DEREF               'hrOffset'
             5728  LOAD_CONST               ('hours',)
             5730  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5732  BINARY_ADD       
             5734  STORE_FAST               'extractedDate'
           5736_0  COME_FROM          5718  '5718'

 L. 820      5736  LOAD_DEREF               'minOffset'
             5738  LOAD_CONST               0
             5740  COMPARE_OP               !=
         5742_5744  POP_JUMP_IF_FALSE  5760  'to 5760'

 L. 821      5746  LOAD_FAST                'extractedDate'
             5748  LOAD_GLOBAL              relativedelta
             5750  LOAD_DEREF               'minOffset'
             5752  LOAD_CONST               ('minutes',)
             5754  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5756  BINARY_ADD       
             5758  STORE_FAST               'extractedDate'
           5760_0  COME_FROM          5742  '5742'

 L. 822      5760  LOAD_DEREF               'secOffset'
             5762  LOAD_CONST               0
             5764  COMPARE_OP               !=
         5766_5768  POP_JUMP_IF_FALSE  5784  'to 5784'

 L. 823      5770  LOAD_FAST                'extractedDate'
             5772  LOAD_GLOBAL              relativedelta
             5774  LOAD_DEREF               'secOffset'
             5776  LOAD_CONST               ('seconds',)
             5778  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5780  BINARY_ADD       
             5782  STORE_FAST               'extractedDate'
           5784_0  COME_FROM          5766  '5766'

 L. 824      5784  SETUP_LOOP         5866  'to 5866'
             5786  LOAD_GLOBAL              enumerate
             5788  LOAD_FAST                'words'
             5790  CALL_FUNCTION_1       1  '1 positional argument'
             5792  GET_ITER         
           5794_0  COME_FROM          5848  '5848'
           5794_1  COME_FROM          5830  '5830'
           5794_2  COME_FROM          5812  '5812'
             5794  FOR_ITER           5864  'to 5864'
             5796  UNPACK_SEQUENCE_2     2 
             5798  STORE_FAST               'idx'
             5800  STORE_FAST               'word'

 L. 825      5802  LOAD_FAST                'words'
             5804  LOAD_FAST                'idx'
             5806  BINARY_SUBSCR    
             5808  LOAD_STR                 'und'
             5810  COMPARE_OP               ==
         5812_5814  POP_JUMP_IF_FALSE  5794  'to 5794'
             5816  LOAD_FAST                'words'
             5818  LOAD_FAST                'idx'
             5820  LOAD_CONST               1
             5822  BINARY_SUBTRACT  
             5824  BINARY_SUBSCR    
             5826  LOAD_STR                 ''
             5828  COMPARE_OP               ==
         5830_5832  POP_JUMP_IF_FALSE  5794  'to 5794'

 L. 826      5834  LOAD_FAST                'words'
             5836  LOAD_FAST                'idx'
             5838  LOAD_CONST               1
             5840  BINARY_ADD       
             5842  BINARY_SUBSCR    
             5844  LOAD_STR                 ''
             5846  COMPARE_OP               ==
         5848_5850  POP_JUMP_IF_FALSE  5794  'to 5794'

 L. 827      5852  LOAD_STR                 ''
             5854  LOAD_FAST                'words'
             5856  LOAD_FAST                'idx'
             5858  STORE_SUBSCR     
         5860_5862  JUMP_BACK          5794  'to 5794'
             5864  POP_BLOCK        
           5866_0  COME_FROM_LOOP     5784  '5784'

 L. 829      5866  LOAD_STR                 ' '
             5868  LOAD_METHOD              join
             5870  LOAD_FAST                'words'
             5872  CALL_METHOD_1         1  '1 positional argument'
             5874  STORE_FAST               'resultStr'

 L. 830      5876  LOAD_STR                 ' '
             5878  LOAD_METHOD              join
             5880  LOAD_FAST                'resultStr'
             5882  LOAD_METHOD              split
             5884  CALL_METHOD_0         0  '0 positional arguments'
             5886  CALL_METHOD_1         1  '1 positional argument'
             5888  STORE_FAST               'resultStr'

 L. 832      5890  LOAD_FAST                'extractedDate'
             5892  LOAD_FAST                'resultStr'
             5894  BUILD_LIST_2          2 
             5896  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 1680_1682


def isFractional_de(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.lower().startswith('halb'):
        return 0.5
    if input_str.lower() == 'drittel':
        return 0.3333333333333333
    if input_str.endswith('tel'):
        if input_str.endswith('stel'):
            input_str = input_str[:len(input_str) - 4]
        else:
            input_str = input_str[:len(input_str) - 3]
        if input_str.lower() in de_numbers:
            return 1.0 / de_numbers[input_str.lower()]
    return False


def isOrdinal_de(input_str):
    """
    This function takes the given text and checks if it is an ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (float): False if not an ordinal, otherwise the number
        corresponding to the ordinal

    ordinals for 1, 3, 7 and 8 are irregular

    only works for ordinals corresponding to the numbers in de_numbers

    """
    lowerstr = input_str.lower()
    if lowerstr.startswith('erste'):
        return 1
    if lowerstr.startswith('dritte'):
        return 3
    if lowerstr.startswith('siebte'):
        return 7
    if lowerstr.startswith('achte'):
        return 8
    if lowerstr[-3:] == 'ste':
        lowerstr = lowerstr[:-3]
        if lowerstr in de_numbers:
            return de_numbers[lowerstr]
    if lowerstr[-4:] in ('ster', 'stes', 'sten', 'stem'):
        lowerstr = lowerstr[:-4]
        if lowerstr in de_numbers:
            return de_numbers[lowerstr]
    if lowerstr[-2:] == 'te':
        lowerstr = lowerstr[:-2]
        if lowerstr in de_numbers:
            return de_numbers[lowerstr]
    if lowerstr[-3:] in ('ter', 'tes', 'ten', 'tem'):
        lowerstr = lowerstr[:-3]
        if lowerstr in de_numbers:
            return de_numbers[lowerstr]
    return False


def normalize_de(text, remove_articles):
    """ German string normalization """
    words = text.split()
    normalized = ''
    for word in words:
        if remove_articles:
            if word in ('der', 'die', 'das', 'des', 'den', 'dem'):
                continue
        contraction = [
         'net', 'nett']
        if word in contraction:
            expansion = [
             'nicht', 'nicht']
            word = expansion[contraction.index(word)]
        if word in de_numbers:
            word = str(de_numbers[word])
        normalized += ' ' + word

    return normalized[1:]


def extract_numbers_de(text, short_scale=True, ordinals=False):
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
    return extract_numbers_generic(text, pronounce_number_de, extractnumber_de, short_scale=short_scale,
      ordinals=ordinals)