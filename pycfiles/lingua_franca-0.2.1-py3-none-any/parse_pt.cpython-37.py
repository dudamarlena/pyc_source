# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_pt.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 38856 bytes
"""
    Parse functions for Portuguese (PT-PT)

    TODO: numbers greater than 999999
    TODO: date time pt
"""
from datetime import datetime
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions
from lingua_franca.lang.common_data_pt import _NUMBERS_PT, _FEMALE_DETERMINANTS_PT, _FEMALE_ENDINGS_PT, _MALE_DETERMINANTS_PT, _MALE_ENDINGS_PT, _GENDERS_PT
from lingua_franca import resolve_resource_file
from lingua_franca.lang.parse_common import Normalizer
import json, re

def isFractional_pt(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]
    aFrac = ['meio', 'terço', 'quarto', 'quinto', 'sexto',
     'setimo', 'oitavo', 'nono', 'décimo']
    if input_str.lower() in aFrac:
        return 1.0 / (aFrac.index(input_str) + 2)
    if input_str == 'vigésimo':
        return 0.05
    if input_str == 'trigésimo':
        return 0.03333333333333333
    if input_str == 'centésimo':
        return 0.01
    if input_str == 'milésimo':
        return 0.001
    if input_str == 'sétimo' or input_str == 'septimo' or input_str == 'séptimo':
        return 0.14285714285714285
    return False


def extractnumber_pt(text, short_scale=True, ordinals=False):
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
    count = 0
    result = None
    while count < len(aWords):
        val = 0
        word = aWords[count]
        next_next_word = None
        if count + 1 < len(aWords):
            next_word = aWords[(count + 1)]
            if count + 2 < len(aWords):
                next_next_word = aWords[(count + 2)]
        else:
            next_word = None
        if word in _NUMBERS_PT:
            val = _NUMBERS_PT[word]
        else:
            if word.isdigit():
                val = int(word)
            else:
                if is_numeric(word):
                    val = float(word)
                else:
                    if isFractional_pt(word):
                        if not result:
                            result = 1
                        result = result * isFractional_pt(word)
                        count += 1
                        continue
                    elif not val:
                        aPieces = word.split('/')
                        if look_for_fractions(aPieces):
                            val = float(aPieces[0]) / float(aPieces[1])
                        if val:
                            if result is None:
                                result = 0
                            elif next_word != 'avos':
                                result += val
                            else:
                                result = float(result) / float(val)
                        if next_word is None:
                            break
                        ands = ['e']
                        if next_word in ands:
                            zeros = 0
                            if result is None:
                                count += 1
                                continue
                            newWords = aWords[count + 2:]
                            newText = ''
                            for word in newWords:
                                newText += word + ' '

                            afterAndVal = extractnumber_pt(newText[:-1])
                            if afterAndVal and not result < afterAndVal:
                                if result < 20:
                                    while afterAndVal > 1:
                                        afterAndVal = afterAndVal / 10.0

                                    for word in newWords:
                                        if word == 'zero' or word == '0':
                                            zeros += 1
                                        else:
                                            break

                                for _ in range(0, zeros):
                                    afterAndVal = afterAndVal / 10.0

                                result += afterAndVal
                                break
                    elif next_next_word is not None:
                        if next_next_word in ands:
                            newWords = aWords[count + 3:]
                            newText = ''
                            for word in newWords:
                                newText += word + ' '

                            afterAndVal = extractnumber_pt(newText[:-1])
                            if afterAndVal:
                                if result is None:
                                    result = 0
                                result += afterAndVal
                                break
                    decimals = [
                     'ponto', 'virgula', 'vírgula', '.', ',']
                    if next_word in decimals:
                        zeros = 0
                        newWords = aWords[count + 2:]
                        newText = ''
                        for word in newWords:
                            newText += word + ' '

                        for word in newWords:
                            if word == 'zero' or word == '0':
                                zeros += 1
                            else:
                                break

                        afterDotVal = str(extractnumber_pt(newText[:-1]))
                        afterDotVal = zeros * '0' + afterDotVal
                        result = float(str(result) + '.' + afterDotVal)
                        break
                    count += 1

    if '.' in str(result):
        integer, dec = str(result).split('.')
        if dec == '0':
            result = int(integer)
    return result or False


class PortugueseNormalizer(Normalizer):
    with open(resolve_resource_file('text/pt-pt/normalize.json')) as (f):
        _default_config = json.load(f)

    @staticmethod
    def tokenize(utterance):
        utterance = re.sub('([0-9]+)([\\%])', '\\1 \\2', utterance)
        utterance = re.sub('(\\#)([0-9]+\\b)', '\\1 \\2', utterance)
        utterance = re.sub('([a-zA-Z]+)(-)([a-zA-Z]+\\b)', '\\1 \\2 \\3', utterance)
        tokens = utterance.split()
        if tokens[(-1)] == '-':
            tokens = tokens[:-1]
        return tokens


def normalize_pt(text, remove_articles):
    """ PT string normalization """
    return PortugueseNormalizer().normalize(text, remove_articles)


def extract_datetime_pt--- This code section failed: ---

 L. 226         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_pt.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 278         8  LOAD_CLOSURE             'datestr'
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
               34  LOAD_STR                 'extract_datetime_pt.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 288        40  LOAD_FAST                'input_str'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'currentDate'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 289        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 291        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 292        60  LOAD_CONST               False
               62  STORE_FAST               'daySpecified'

 L. 293        64  LOAD_CONST               False
               66  STORE_DEREF              'dayOffset'

 L. 294        68  LOAD_CONST               0
               70  STORE_DEREF              'monthOffset'

 L. 295        72  LOAD_CONST               0
               74  STORE_DEREF              'yearOffset'

 L. 296        76  LOAD_FAST                'currentDate'
               78  STORE_FAST               'dateNow'

 L. 297        80  LOAD_FAST                'dateNow'
               82  LOAD_METHOD              strftime
               84  LOAD_STR                 '%w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'today'

 L. 298        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%Y'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'currentYear'

 L. 299       100  LOAD_CONST               False
              102  STORE_FAST               'fromFlag'

 L. 300       104  LOAD_STR                 ''
              106  STORE_DEREF              'datestr'

 L. 301       108  LOAD_CONST               False
              110  STORE_FAST               'hasYear'

 L. 302       112  LOAD_STR                 ''
              114  STORE_FAST               'timeQualifier'

 L. 304       116  LOAD_FAST                'clean_string'
              118  LOAD_FAST                'input_str'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_METHOD              split
              124  LOAD_STR                 ' '
              126  CALL_METHOD_1         1  '1 positional argument'
              128  STORE_FAST               'words'

 L. 305       130  LOAD_STR                 'manha'
              132  LOAD_STR                 'tarde'
              134  LOAD_STR                 'noite'
              136  BUILD_LIST_3          3 
              138  STORE_FAST               'timeQualifiersList'

 L. 306       140  LOAD_STR                 'em'
              142  LOAD_STR                 'as'
              144  LOAD_STR                 'nas'
              146  LOAD_STR                 'pelas'
              148  LOAD_STR                 'volta'
              150  LOAD_STR                 'depois'
              152  LOAD_STR                 'estas'

 L. 307       154  LOAD_STR                 'no'
              156  LOAD_STR                 'dia'
              158  LOAD_STR                 'hora'
              160  BUILD_LIST_10        10 
              162  STORE_FAST               'time_indicators'

 L. 308       164  LOAD_STR                 'segunda'
              166  LOAD_STR                 'terca'
              168  LOAD_STR                 'quarta'

 L. 309       170  LOAD_STR                 'quinta'
              172  LOAD_STR                 'sexta'
              174  LOAD_STR                 'sabado'
              176  LOAD_STR                 'domingo'
              178  BUILD_LIST_7          7 
              180  STORE_FAST               'days'

 L. 310       182  LOAD_STR                 'janeiro'
              184  LOAD_STR                 'febreiro'
              186  LOAD_STR                 'marco'
              188  LOAD_STR                 'abril'
              190  LOAD_STR                 'maio'
              192  LOAD_STR                 'junho'

 L. 311       194  LOAD_STR                 'julho'
              196  LOAD_STR                 'agosto'
              198  LOAD_STR                 'setembro'
              200  LOAD_STR                 'outubro'
              202  LOAD_STR                 'novembro'

 L. 312       204  LOAD_STR                 'dezembro'
              206  BUILD_LIST_12        12 
              208  STORE_FAST               'months'

 L. 313       210  LOAD_STR                 'jan'
              212  LOAD_STR                 'feb'
              214  LOAD_STR                 'mar'
              216  LOAD_STR                 'abr'
              218  LOAD_STR                 'mai'
              220  LOAD_STR                 'jun'
              222  LOAD_STR                 'jul'
              224  LOAD_STR                 'ag'

 L. 314       226  LOAD_STR                 'set'
              228  LOAD_STR                 'out'
              230  LOAD_STR                 'nov'
              232  LOAD_STR                 'dec'
              234  BUILD_LIST_12        12 
              236  STORE_FAST               'monthsShort'

 L. 315       238  LOAD_STR                 'proximo'
              240  LOAD_STR                 'proxima'
              242  BUILD_LIST_2          2 
              244  STORE_FAST               'nexts'

 L. 316       246  LOAD_STR                 'seguinte'
              248  LOAD_STR                 'subsequente'
              250  LOAD_STR                 'seguir'
              252  BUILD_LIST_3          3 
              254  STORE_FAST               'suffix_nexts'

 L. 317       256  LOAD_STR                 'ultimo'
              258  LOAD_STR                 'ultima'
              260  BUILD_LIST_2          2 
              262  STORE_FAST               'lasts'

 L. 318       264  LOAD_STR                 'passada'
              266  LOAD_STR                 'passado'
              268  LOAD_STR                 'anterior'
              270  LOAD_STR                 'antes'
              272  BUILD_LIST_4          4 
              274  STORE_FAST               'suffix_lasts'

 L. 319       276  LOAD_STR                 'depois'
              278  LOAD_STR                 'seguir'
              280  LOAD_STR                 'seguida'
              282  LOAD_STR                 'seguinte'
              284  LOAD_STR                 'proxima'
              286  LOAD_STR                 'proximo'
              288  BUILD_LIST_6          6 
              290  STORE_FAST               'nxts'

 L. 320       292  LOAD_STR                 'antes'
              294  LOAD_STR                 'ante'
              296  LOAD_STR                 'previa'
              298  LOAD_STR                 'previamente'
              300  LOAD_STR                 'anterior'
              302  BUILD_LIST_5          5 
              304  STORE_FAST               'prevs'

 L. 321       306  LOAD_STR                 'partir'
              308  LOAD_STR                 'em'
              310  LOAD_STR                 'para'
              312  LOAD_STR                 'na'
              314  LOAD_STR                 'no'
              316  LOAD_STR                 'daqui'
              318  LOAD_STR                 'seguir'

 L. 322       320  LOAD_STR                 'depois'
              322  LOAD_STR                 'por'
              324  LOAD_STR                 'proxima'
              326  LOAD_STR                 'proximo'
              328  LOAD_STR                 'da'
              330  LOAD_STR                 'do'
              332  LOAD_STR                 'de'
              334  BUILD_LIST_14        14 
              336  STORE_FAST               'froms'

 L. 323       338  LOAD_STR                 'este'
              340  LOAD_STR                 'esta'
              342  LOAD_STR                 'deste'
              344  LOAD_STR                 'desta'
              346  LOAD_STR                 'neste'
              348  LOAD_STR                 'nesta'
              350  LOAD_STR                 'nesse'

 L. 324       352  LOAD_STR                 'nessa'
              354  BUILD_LIST_8          8 
              356  STORE_FAST               'thises'

 L. 325       358  LOAD_FAST                'froms'
              360  LOAD_FAST                'thises'
              362  INPLACE_ADD      
              364  STORE_FAST               'froms'

 L. 326       366  LOAD_FAST                'nxts'
              368  LOAD_FAST                'prevs'
              370  BINARY_ADD       
              372  LOAD_FAST                'froms'
              374  BINARY_ADD       
              376  LOAD_FAST                'time_indicators'
              378  BINARY_ADD       
              380  STORE_FAST               'lists'

 L. 327   382_384  SETUP_LOOP         3376  'to 3376'
              386  LOAD_GLOBAL              enumerate
              388  LOAD_FAST                'words'
              390  CALL_FUNCTION_1       1  '1 positional argument'
              392  GET_ITER         
            394_0  COME_FROM          3232  '3232'
          394_396  FOR_ITER           3374  'to 3374'
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'idx'
              402  STORE_FAST               'word'

 L. 328       404  LOAD_FAST                'word'
              406  LOAD_STR                 ''
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   418  'to 418'

 L. 329   414_416  CONTINUE            394  'to 394'
            418_0  COME_FROM           410  '410'

 L. 330       418  LOAD_FAST                'idx'
              420  LOAD_CONST               1
              422  COMPARE_OP               >
          424_426  POP_JUMP_IF_FALSE   440  'to 440'
              428  LOAD_FAST                'words'
              430  LOAD_FAST                'idx'
              432  LOAD_CONST               2
              434  BINARY_SUBTRACT  
              436  BINARY_SUBSCR    
              438  JUMP_FORWARD        442  'to 442'
            440_0  COME_FROM           424  '424'
              440  LOAD_STR                 ''
            442_0  COME_FROM           438  '438'
              442  STORE_FAST               'wordPrevPrev'

 L. 331       444  LOAD_FAST                'idx'
              446  LOAD_CONST               0
              448  COMPARE_OP               >
          450_452  POP_JUMP_IF_FALSE   466  'to 466'
              454  LOAD_FAST                'words'
              456  LOAD_FAST                'idx'
              458  LOAD_CONST               1
              460  BINARY_SUBTRACT  
              462  BINARY_SUBSCR    
              464  JUMP_FORWARD        468  'to 468'
            466_0  COME_FROM           450  '450'
              466  LOAD_STR                 ''
            468_0  COME_FROM           464  '464'
              468  STORE_FAST               'wordPrev'

 L. 332       470  LOAD_FAST                'idx'
              472  LOAD_CONST               1
              474  BINARY_ADD       
              476  LOAD_GLOBAL              len
              478  LOAD_FAST                'words'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  COMPARE_OP               <
          484_486  POP_JUMP_IF_FALSE   500  'to 500'
              488  LOAD_FAST                'words'
              490  LOAD_FAST                'idx'
              492  LOAD_CONST               1
              494  BINARY_ADD       
              496  BINARY_SUBSCR    
              498  JUMP_FORWARD        502  'to 502'
            500_0  COME_FROM           484  '484'
              500  LOAD_STR                 ''
            502_0  COME_FROM           498  '498'
              502  STORE_FAST               'wordNext'

 L. 333       504  LOAD_FAST                'idx'
              506  LOAD_CONST               2
              508  BINARY_ADD       
              510  LOAD_GLOBAL              len
              512  LOAD_FAST                'words'
              514  CALL_FUNCTION_1       1  '1 positional argument'
              516  COMPARE_OP               <
          518_520  POP_JUMP_IF_FALSE   534  'to 534'
              522  LOAD_FAST                'words'
              524  LOAD_FAST                'idx'
              526  LOAD_CONST               2
              528  BINARY_ADD       
              530  BINARY_SUBSCR    
              532  JUMP_FORWARD        536  'to 536'
            534_0  COME_FROM           518  '518'
              534  LOAD_STR                 ''
            536_0  COME_FROM           532  '532'
              536  STORE_FAST               'wordNextNext'

 L. 334       538  LOAD_FAST                'idx'
              540  LOAD_CONST               3
              542  BINARY_ADD       
              544  LOAD_GLOBAL              len
              546  LOAD_FAST                'words'
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  COMPARE_OP               <
          552_554  POP_JUMP_IF_FALSE   568  'to 568'
              556  LOAD_FAST                'words'
              558  LOAD_FAST                'idx'
              560  LOAD_CONST               3
              562  BINARY_ADD       
              564  BINARY_SUBSCR    
              566  JUMP_FORWARD        570  'to 570'
            568_0  COME_FROM           552  '552'
              568  LOAD_STR                 ''
            570_0  COME_FROM           566  '566'
              570  STORE_FAST               'wordNextNextNext'

 L. 336       572  LOAD_FAST                'idx'
              574  STORE_FAST               'start'

 L. 337       576  LOAD_CONST               0
              578  STORE_FAST               'used'

 L. 339       580  LOAD_FAST                'word'
              582  LOAD_FAST                'timeQualifiersList'
              584  COMPARE_OP               in
          586_588  POP_JUMP_IF_FALSE   598  'to 598'

 L. 340       590  LOAD_FAST                'word'
              592  STORE_FAST               'timeQualifier'
          594_596  JUMP_FORWARD       2620  'to 2620'
            598_0  COME_FROM           586  '586'

 L. 343       598  LOAD_FAST                'word'
              600  LOAD_STR                 'hoje'
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_FALSE   630  'to 630'
              608  LOAD_FAST                'fromFlag'
          610_612  POP_JUMP_IF_TRUE    630  'to 630'

 L. 344       614  LOAD_CONST               0
              616  STORE_DEREF              'dayOffset'

 L. 345       618  LOAD_FAST                'used'
              620  LOAD_CONST               1
              622  INPLACE_ADD      
              624  STORE_FAST               'used'
          626_628  JUMP_FORWARD       2620  'to 2620'
            630_0  COME_FROM           610  '610'
            630_1  COME_FROM           604  '604'

 L. 346       630  LOAD_FAST                'word'
              632  LOAD_STR                 'amanha'
              634  COMPARE_OP               ==
          636_638  POP_JUMP_IF_FALSE   662  'to 662'
              640  LOAD_FAST                'fromFlag'
          642_644  POP_JUMP_IF_TRUE    662  'to 662'

 L. 347       646  LOAD_CONST               1
              648  STORE_DEREF              'dayOffset'

 L. 348       650  LOAD_FAST                'used'
              652  LOAD_CONST               1
              654  INPLACE_ADD      
              656  STORE_FAST               'used'
          658_660  JUMP_FORWARD       2620  'to 2620'
            662_0  COME_FROM           642  '642'
            662_1  COME_FROM           636  '636'

 L. 349       662  LOAD_FAST                'word'
              664  LOAD_STR                 'ontem'
              666  COMPARE_OP               ==
          668_670  POP_JUMP_IF_FALSE   698  'to 698'
              672  LOAD_FAST                'fromFlag'
          674_676  POP_JUMP_IF_TRUE    698  'to 698'

 L. 350       678  LOAD_DEREF               'dayOffset'
              680  LOAD_CONST               1
              682  INPLACE_SUBTRACT 
              684  STORE_DEREF              'dayOffset'

 L. 351       686  LOAD_FAST                'used'
              688  LOAD_CONST               1
              690  INPLACE_ADD      
              692  STORE_FAST               'used'
          694_696  JUMP_FORWARD       2620  'to 2620'
            698_0  COME_FROM           674  '674'
            698_1  COME_FROM           668  '668'

 L. 353       698  LOAD_FAST                'word'
              700  LOAD_STR                 'anteontem'
              702  COMPARE_OP               ==
          704_706  POP_JUMP_IF_TRUE    728  'to 728'

 L. 354       708  LOAD_FAST                'word'
              710  LOAD_STR                 'ante'
              712  COMPARE_OP               ==
          714_716  POP_JUMP_IF_FALSE   772  'to 772'
              718  LOAD_FAST                'wordNext'
              720  LOAD_STR                 'ontem'
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   772  'to 772'
            728_0  COME_FROM           704  '704'
              728  LOAD_FAST                'fromFlag'
          730_732  POP_JUMP_IF_TRUE    772  'to 772'

 L. 355       734  LOAD_DEREF               'dayOffset'
              736  LOAD_CONST               2
              738  INPLACE_SUBTRACT 
              740  STORE_DEREF              'dayOffset'

 L. 356       742  LOAD_FAST                'used'
              744  LOAD_CONST               1
              746  INPLACE_ADD      
              748  STORE_FAST               'used'

 L. 357       750  LOAD_FAST                'wordNext'
              752  LOAD_STR                 'ontem'
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 358       760  LOAD_FAST                'used'
              762  LOAD_CONST               1
              764  INPLACE_ADD      
              766  STORE_FAST               'used'
          768_770  JUMP_FORWARD       2620  'to 2620'
            772_0  COME_FROM           730  '730'
            772_1  COME_FROM           724  '724'
            772_2  COME_FROM           714  '714'

 L. 359       772  LOAD_FAST                'word'
              774  LOAD_STR                 'ante'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   828  'to 828'
              782  LOAD_FAST                'wordNext'
              784  LOAD_STR                 'ante'
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   828  'to 828'
              792  LOAD_FAST                'wordNextNext'

 L. 360       794  LOAD_STR                 'ontem'
              796  COMPARE_OP               ==
          798_800  POP_JUMP_IF_FALSE   828  'to 828'
              802  LOAD_FAST                'fromFlag'
          804_806  POP_JUMP_IF_TRUE    828  'to 828'

 L. 361       808  LOAD_DEREF               'dayOffset'
              810  LOAD_CONST               3
              812  INPLACE_SUBTRACT 
              814  STORE_DEREF              'dayOffset'

 L. 362       816  LOAD_FAST                'used'
              818  LOAD_CONST               3
              820  INPLACE_ADD      
              822  STORE_FAST               'used'
          824_826  JUMP_FORWARD       2620  'to 2620'
            828_0  COME_FROM           804  '804'
            828_1  COME_FROM           798  '798'
            828_2  COME_FROM           788  '788'
            828_3  COME_FROM           778  '778'

 L. 363       828  LOAD_FAST                'word'
              830  LOAD_STR                 'anteanteontem'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   864  'to 864'
              838  LOAD_FAST                'fromFlag'
          840_842  POP_JUMP_IF_TRUE    864  'to 864'

 L. 364       844  LOAD_DEREF               'dayOffset'
              846  LOAD_CONST               3
              848  INPLACE_SUBTRACT 
              850  STORE_DEREF              'dayOffset'

 L. 365       852  LOAD_FAST                'used'
              854  LOAD_CONST               1
              856  INPLACE_ADD      
              858  STORE_FAST               'used'
          860_862  JUMP_FORWARD       2620  'to 2620'
            864_0  COME_FROM           840  '840'
            864_1  COME_FROM           834  '834'

 L. 367       864  LOAD_FAST                'word'
              866  LOAD_STR                 'depois'
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   906  'to 906'
              874  LOAD_FAST                'wordNext'
              876  LOAD_STR                 'amanha'
              878  COMPARE_OP               ==
          880_882  POP_JUMP_IF_FALSE   906  'to 906'
              884  LOAD_FAST                'fromFlag'
          886_888  POP_JUMP_IF_TRUE    906  'to 906'

 L. 368       890  LOAD_DEREF               'dayOffset'
              892  LOAD_CONST               2
              894  INPLACE_ADD      
              896  STORE_DEREF              'dayOffset'

 L. 369       898  LOAD_CONST               2
              900  STORE_FAST               'used'
          902_904  JUMP_FORWARD       2620  'to 2620'
            906_0  COME_FROM           886  '886'
            906_1  COME_FROM           880  '880'
            906_2  COME_FROM           870  '870'

 L. 371       906  LOAD_FAST                'word'
              908  LOAD_STR                 'antes'
              910  COMPARE_OP               ==
          912_914  POP_JUMP_IF_FALSE   948  'to 948'
              916  LOAD_FAST                'wordNext'
              918  LOAD_STR                 'ontem'
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   948  'to 948'
              926  LOAD_FAST                'fromFlag'
          928_930  POP_JUMP_IF_TRUE    948  'to 948'

 L. 372       932  LOAD_DEREF               'dayOffset'
              934  LOAD_CONST               2
              936  INPLACE_SUBTRACT 
              938  STORE_DEREF              'dayOffset'

 L. 373       940  LOAD_CONST               2
              942  STORE_FAST               'used'
          944_946  JUMP_FORWARD       2620  'to 2620'
            948_0  COME_FROM           928  '928'
            948_1  COME_FROM           922  '922'
            948_2  COME_FROM           912  '912'

 L. 375       948  LOAD_FAST                'word'
              950  LOAD_STR                 'dia'
              952  COMPARE_OP               ==
          954_956  POP_JUMP_IF_FALSE  1178  'to 1178'

 L. 376       958  LOAD_FAST                'wordNext'
              960  LOAD_STR                 'depois'
              962  COMPARE_OP               ==
          964_966  POP_JUMP_IF_TRUE    978  'to 978'
              968  LOAD_FAST                'wordNext'
              970  LOAD_STR                 'antes'
              972  COMPARE_OP               ==
          974_976  POP_JUMP_IF_FALSE  1036  'to 1036'
            978_0  COME_FROM           964  '964'

 L. 377       978  LOAD_FAST                'used'
              980  LOAD_CONST               1
              982  INPLACE_ADD      
              984  STORE_FAST               'used'

 L. 378       986  LOAD_FAST                'wordPrev'
          988_990  POP_JUMP_IF_FALSE  1174  'to 1174'
              992  LOAD_FAST                'wordPrev'
              994  LOAD_CONST               0
              996  BINARY_SUBSCR    
              998  LOAD_METHOD              isdigit
             1000  CALL_METHOD_0         0  '0 positional arguments'
         1002_1004  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 379      1006  LOAD_DEREF               'dayOffset'
             1008  LOAD_GLOBAL              int
             1010  LOAD_FAST                'wordPrev'
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  INPLACE_ADD      
             1016  STORE_DEREF              'dayOffset'

 L. 380      1018  LOAD_FAST                'start'
             1020  LOAD_CONST               1
             1022  INPLACE_SUBTRACT 
             1024  STORE_FAST               'start'

 L. 381      1026  LOAD_FAST                'used'
             1028  LOAD_CONST               1
             1030  INPLACE_ADD      
             1032  STORE_FAST               'used'
             1034  JUMP_FORWARD       2620  'to 2620'
           1036_0  COME_FROM           974  '974'

 L. 382      1036  LOAD_FAST                'wordPrev'
         1038_1040  POP_JUMP_IF_FALSE  1106  'to 1106'
             1042  LOAD_FAST                'wordPrev'
             1044  LOAD_CONST               0
             1046  BINARY_SUBSCR    
             1048  LOAD_METHOD              isdigit
             1050  CALL_METHOD_0         0  '0 positional arguments'
         1052_1054  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 383      1056  LOAD_FAST                'wordNext'
             1058  LOAD_FAST                'months'
             1060  COMPARE_OP               not-in
         1062_1064  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 384      1066  LOAD_FAST                'wordNext'
             1068  LOAD_FAST                'monthsShort'
             1070  COMPARE_OP               not-in
         1072_1074  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 385      1076  LOAD_DEREF               'dayOffset'
             1078  LOAD_GLOBAL              int
             1080  LOAD_FAST                'wordPrev'
             1082  CALL_FUNCTION_1       1  '1 positional argument'
             1084  INPLACE_ADD      
             1086  STORE_DEREF              'dayOffset'

 L. 386      1088  LOAD_FAST                'start'
             1090  LOAD_CONST               1
             1092  INPLACE_SUBTRACT 
             1094  STORE_FAST               'start'

 L. 387      1096  LOAD_FAST                'used'
             1098  LOAD_CONST               2
             1100  INPLACE_ADD      
             1102  STORE_FAST               'used'
             1104  JUMP_FORWARD       2620  'to 2620'
           1106_0  COME_FROM          1072  '1072'
           1106_1  COME_FROM          1062  '1062'
           1106_2  COME_FROM          1052  '1052'
           1106_3  COME_FROM          1038  '1038'

 L. 388      1106  LOAD_FAST                'wordNext'
         1108_1110  POP_JUMP_IF_FALSE  2620  'to 2620'
             1112  LOAD_FAST                'wordNext'
             1114  LOAD_CONST               0
             1116  BINARY_SUBSCR    
             1118  LOAD_METHOD              isdigit
             1120  CALL_METHOD_0         0  '0 positional arguments'
         1122_1124  POP_JUMP_IF_FALSE  2620  'to 2620'
             1126  LOAD_FAST                'wordNextNext'

 L. 389      1128  LOAD_FAST                'months'
             1130  COMPARE_OP               not-in
         1132_1134  POP_JUMP_IF_FALSE  2620  'to 2620'
             1136  LOAD_FAST                'wordNextNext'
             1138  LOAD_FAST                'monthsShort'
             1140  COMPARE_OP               not-in
         1142_1144  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 390      1146  LOAD_DEREF               'dayOffset'
             1148  LOAD_GLOBAL              int
             1150  LOAD_FAST                'wordNext'
             1152  CALL_FUNCTION_1       1  '1 positional argument'
             1154  INPLACE_ADD      
             1156  STORE_DEREF              'dayOffset'

 L. 391      1158  LOAD_FAST                'start'
             1160  LOAD_CONST               1
             1162  INPLACE_SUBTRACT 
             1164  STORE_FAST               'start'

 L. 392      1166  LOAD_FAST                'used'
             1168  LOAD_CONST               2
             1170  INPLACE_ADD      
             1172  STORE_FAST               'used'
           1174_0  COME_FROM          1002  '1002'
           1174_1  COME_FROM           988  '988'
         1174_1176  JUMP_FORWARD       2620  'to 2620'
           1178_0  COME_FROM           954  '954'

 L. 394      1178  LOAD_FAST                'word'
             1180  LOAD_STR                 'semana'
             1182  COMPARE_OP               ==
         1184_1186  POP_JUMP_IF_FALSE  1408  'to 1408'
             1188  LOAD_FAST                'fromFlag'
         1190_1192  POP_JUMP_IF_TRUE   1408  'to 1408'

 L. 395      1194  LOAD_FAST                'wordPrev'
             1196  LOAD_CONST               0
             1198  BINARY_SUBSCR    
             1200  LOAD_METHOD              isdigit
             1202  CALL_METHOD_0         0  '0 positional arguments'
         1204_1206  POP_JUMP_IF_FALSE  1236  'to 1236'

 L. 396      1208  LOAD_DEREF               'dayOffset'
             1210  LOAD_GLOBAL              int
             1212  LOAD_FAST                'wordPrev'
             1214  CALL_FUNCTION_1       1  '1 positional argument'
             1216  LOAD_CONST               7
             1218  BINARY_MULTIPLY  
             1220  INPLACE_ADD      
             1222  STORE_DEREF              'dayOffset'

 L. 397      1224  LOAD_FAST                'start'
             1226  LOAD_CONST               1
             1228  INPLACE_SUBTRACT 
             1230  STORE_FAST               'start'

 L. 398      1232  LOAD_CONST               2
             1234  STORE_FAST               'used'
           1236_0  COME_FROM          1204  '1204'

 L. 399      1236  SETUP_LOOP         1278  'to 1278'
             1238  LOAD_FAST                'nexts'
             1240  GET_ITER         
           1242_0  COME_FROM          1252  '1252'
             1242  FOR_ITER           1276  'to 1276'
             1244  STORE_FAST               'w'

 L. 400      1246  LOAD_FAST                'wordPrev'
             1248  LOAD_FAST                'w'
             1250  COMPARE_OP               ==
         1252_1254  POP_JUMP_IF_FALSE  1242  'to 1242'

 L. 401      1256  LOAD_CONST               7
             1258  STORE_DEREF              'dayOffset'

 L. 402      1260  LOAD_FAST                'start'
             1262  LOAD_CONST               1
             1264  INPLACE_SUBTRACT 
             1266  STORE_FAST               'start'

 L. 403      1268  LOAD_CONST               2
             1270  STORE_FAST               'used'
         1272_1274  JUMP_BACK          1242  'to 1242'
             1276  POP_BLOCK        
           1278_0  COME_FROM_LOOP     1236  '1236'

 L. 404      1278  SETUP_LOOP         1320  'to 1320'
             1280  LOAD_FAST                'lasts'
             1282  GET_ITER         
           1284_0  COME_FROM          1294  '1294'
             1284  FOR_ITER           1318  'to 1318'
             1286  STORE_FAST               'w'

 L. 405      1288  LOAD_FAST                'wordPrev'
             1290  LOAD_FAST                'w'
             1292  COMPARE_OP               ==
         1294_1296  POP_JUMP_IF_FALSE  1284  'to 1284'

 L. 406      1298  LOAD_CONST               -7
             1300  STORE_DEREF              'dayOffset'

 L. 407      1302  LOAD_FAST                'start'
             1304  LOAD_CONST               1
             1306  INPLACE_SUBTRACT 
             1308  STORE_FAST               'start'

 L. 408      1310  LOAD_CONST               2
             1312  STORE_FAST               'used'
         1314_1316  JUMP_BACK          1284  'to 1284'
             1318  POP_BLOCK        
           1320_0  COME_FROM_LOOP     1278  '1278'

 L. 409      1320  SETUP_LOOP         1362  'to 1362'
             1322  LOAD_FAST                'suffix_nexts'
             1324  GET_ITER         
           1326_0  COME_FROM          1336  '1336'
             1326  FOR_ITER           1360  'to 1360'
             1328  STORE_FAST               'w'

 L. 410      1330  LOAD_FAST                'wordNext'
             1332  LOAD_FAST                'w'
             1334  COMPARE_OP               ==
         1336_1338  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 411      1340  LOAD_CONST               7
             1342  STORE_DEREF              'dayOffset'

 L. 412      1344  LOAD_FAST                'start'
             1346  LOAD_CONST               1
             1348  INPLACE_SUBTRACT 
             1350  STORE_FAST               'start'

 L. 413      1352  LOAD_CONST               2
             1354  STORE_FAST               'used'
         1356_1358  JUMP_BACK          1326  'to 1326'
             1360  POP_BLOCK        
           1362_0  COME_FROM_LOOP     1320  '1320'

 L. 414      1362  SETUP_LOOP         1404  'to 1404'
             1364  LOAD_FAST                'suffix_lasts'
             1366  GET_ITER         
           1368_0  COME_FROM          1378  '1378'
             1368  FOR_ITER           1402  'to 1402'
             1370  STORE_FAST               'w'

 L. 415      1372  LOAD_FAST                'wordNext'
             1374  LOAD_FAST                'w'
             1376  COMPARE_OP               ==
         1378_1380  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 416      1382  LOAD_CONST               -7
             1384  STORE_DEREF              'dayOffset'

 L. 417      1386  LOAD_FAST                'start'
             1388  LOAD_CONST               1
             1390  INPLACE_SUBTRACT 
             1392  STORE_FAST               'start'

 L. 418      1394  LOAD_CONST               2
             1396  STORE_FAST               'used'
         1398_1400  JUMP_BACK          1368  'to 1368'
             1402  POP_BLOCK        
           1404_0  COME_FROM_LOOP     1362  '1362'
         1404_1406  JUMP_FORWARD       2620  'to 2620'
           1408_0  COME_FROM          1190  '1190'
           1408_1  COME_FROM          1184  '1184'

 L. 420      1408  LOAD_FAST                'word'
             1410  LOAD_STR                 'mes'
             1412  COMPARE_OP               ==
         1414_1416  POP_JUMP_IF_FALSE  1630  'to 1630'
             1418  LOAD_FAST                'fromFlag'
         1420_1422  POP_JUMP_IF_TRUE   1630  'to 1630'

 L. 421      1424  LOAD_FAST                'wordPrev'
             1426  LOAD_CONST               0
             1428  BINARY_SUBSCR    
             1430  LOAD_METHOD              isdigit
             1432  CALL_METHOD_0         0  '0 positional arguments'
         1434_1436  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 422      1438  LOAD_GLOBAL              int
             1440  LOAD_FAST                'wordPrev'
             1442  CALL_FUNCTION_1       1  '1 positional argument'
             1444  STORE_DEREF              'monthOffset'

 L. 423      1446  LOAD_FAST                'start'
             1448  LOAD_CONST               1
             1450  INPLACE_SUBTRACT 
             1452  STORE_FAST               'start'

 L. 424      1454  LOAD_CONST               2
             1456  STORE_FAST               'used'
           1458_0  COME_FROM          1434  '1434'

 L. 425      1458  SETUP_LOOP         1500  'to 1500'
             1460  LOAD_FAST                'nexts'
             1462  GET_ITER         
           1464_0  COME_FROM          1474  '1474'
             1464  FOR_ITER           1498  'to 1498'
             1466  STORE_FAST               'w'

 L. 426      1468  LOAD_FAST                'wordPrev'
             1470  LOAD_FAST                'w'
             1472  COMPARE_OP               ==
         1474_1476  POP_JUMP_IF_FALSE  1464  'to 1464'

 L. 427      1478  LOAD_CONST               7
             1480  STORE_DEREF              'monthOffset'

 L. 428      1482  LOAD_FAST                'start'
             1484  LOAD_CONST               1
             1486  INPLACE_SUBTRACT 
             1488  STORE_FAST               'start'

 L. 429      1490  LOAD_CONST               2
             1492  STORE_FAST               'used'
         1494_1496  JUMP_BACK          1464  'to 1464'
             1498  POP_BLOCK        
           1500_0  COME_FROM_LOOP     1458  '1458'

 L. 430      1500  SETUP_LOOP         1542  'to 1542'
             1502  LOAD_FAST                'lasts'
             1504  GET_ITER         
           1506_0  COME_FROM          1516  '1516'
             1506  FOR_ITER           1540  'to 1540'
             1508  STORE_FAST               'w'

 L. 431      1510  LOAD_FAST                'wordPrev'
             1512  LOAD_FAST                'w'
             1514  COMPARE_OP               ==
         1516_1518  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 432      1520  LOAD_CONST               -7
             1522  STORE_DEREF              'monthOffset'

 L. 433      1524  LOAD_FAST                'start'
             1526  LOAD_CONST               1
             1528  INPLACE_SUBTRACT 
             1530  STORE_FAST               'start'

 L. 434      1532  LOAD_CONST               2
             1534  STORE_FAST               'used'
         1536_1538  JUMP_BACK          1506  'to 1506'
             1540  POP_BLOCK        
           1542_0  COME_FROM_LOOP     1500  '1500'

 L. 435      1542  SETUP_LOOP         1584  'to 1584'
             1544  LOAD_FAST                'suffix_nexts'
             1546  GET_ITER         
           1548_0  COME_FROM          1558  '1558'
             1548  FOR_ITER           1582  'to 1582'
             1550  STORE_FAST               'w'

 L. 436      1552  LOAD_FAST                'wordNext'
             1554  LOAD_FAST                'w'
             1556  COMPARE_OP               ==
         1558_1560  POP_JUMP_IF_FALSE  1548  'to 1548'

 L. 437      1562  LOAD_CONST               7
             1564  STORE_DEREF              'monthOffset'

 L. 438      1566  LOAD_FAST                'start'
             1568  LOAD_CONST               1
             1570  INPLACE_SUBTRACT 
             1572  STORE_FAST               'start'

 L. 439      1574  LOAD_CONST               2
             1576  STORE_FAST               'used'
         1578_1580  JUMP_BACK          1548  'to 1548'
             1582  POP_BLOCK        
           1584_0  COME_FROM_LOOP     1542  '1542'

 L. 440      1584  SETUP_LOOP         1626  'to 1626'
             1586  LOAD_FAST                'suffix_lasts'
             1588  GET_ITER         
           1590_0  COME_FROM          1600  '1600'
             1590  FOR_ITER           1624  'to 1624'
             1592  STORE_FAST               'w'

 L. 441      1594  LOAD_FAST                'wordNext'
             1596  LOAD_FAST                'w'
             1598  COMPARE_OP               ==
         1600_1602  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 442      1604  LOAD_CONST               -7
             1606  STORE_DEREF              'monthOffset'

 L. 443      1608  LOAD_FAST                'start'
             1610  LOAD_CONST               1
             1612  INPLACE_SUBTRACT 
             1614  STORE_FAST               'start'

 L. 444      1616  LOAD_CONST               2
             1618  STORE_FAST               'used'
         1620_1622  JUMP_BACK          1590  'to 1590'
             1624  POP_BLOCK        
           1626_0  COME_FROM_LOOP     1584  '1584'
         1626_1628  JUMP_FORWARD       2620  'to 2620'
           1630_0  COME_FROM          1420  '1420'
           1630_1  COME_FROM          1414  '1414'

 L. 446      1630  LOAD_FAST                'word'
             1632  LOAD_STR                 'ano'
             1634  COMPARE_OP               ==
         1636_1638  POP_JUMP_IF_FALSE  1852  'to 1852'
             1640  LOAD_FAST                'fromFlag'
         1642_1644  POP_JUMP_IF_TRUE   1852  'to 1852'

 L. 447      1646  LOAD_FAST                'wordPrev'
             1648  LOAD_CONST               0
             1650  BINARY_SUBSCR    
             1652  LOAD_METHOD              isdigit
             1654  CALL_METHOD_0         0  '0 positional arguments'
         1656_1658  POP_JUMP_IF_FALSE  1680  'to 1680'

 L. 448      1660  LOAD_GLOBAL              int
             1662  LOAD_FAST                'wordPrev'
             1664  CALL_FUNCTION_1       1  '1 positional argument'
             1666  STORE_DEREF              'yearOffset'

 L. 449      1668  LOAD_FAST                'start'
             1670  LOAD_CONST               1
             1672  INPLACE_SUBTRACT 
             1674  STORE_FAST               'start'

 L. 450      1676  LOAD_CONST               2
             1678  STORE_FAST               'used'
           1680_0  COME_FROM          1656  '1656'

 L. 451      1680  SETUP_LOOP         1722  'to 1722'
             1682  LOAD_FAST                'nexts'
             1684  GET_ITER         
           1686_0  COME_FROM          1696  '1696'
             1686  FOR_ITER           1720  'to 1720'
             1688  STORE_FAST               'w'

 L. 452      1690  LOAD_FAST                'wordPrev'
             1692  LOAD_FAST                'w'
             1694  COMPARE_OP               ==
         1696_1698  POP_JUMP_IF_FALSE  1686  'to 1686'

 L. 453      1700  LOAD_CONST               7
             1702  STORE_DEREF              'yearOffset'

 L. 454      1704  LOAD_FAST                'start'
             1706  LOAD_CONST               1
             1708  INPLACE_SUBTRACT 
             1710  STORE_FAST               'start'

 L. 455      1712  LOAD_CONST               2
             1714  STORE_FAST               'used'
         1716_1718  JUMP_BACK          1686  'to 1686'
             1720  POP_BLOCK        
           1722_0  COME_FROM_LOOP     1680  '1680'

 L. 456      1722  SETUP_LOOP         1764  'to 1764'
             1724  LOAD_FAST                'lasts'
             1726  GET_ITER         
           1728_0  COME_FROM          1738  '1738'
             1728  FOR_ITER           1762  'to 1762'
             1730  STORE_FAST               'w'

 L. 457      1732  LOAD_FAST                'wordPrev'
             1734  LOAD_FAST                'w'
             1736  COMPARE_OP               ==
         1738_1740  POP_JUMP_IF_FALSE  1728  'to 1728'

 L. 458      1742  LOAD_CONST               -7
             1744  STORE_DEREF              'yearOffset'

 L. 459      1746  LOAD_FAST                'start'
             1748  LOAD_CONST               1
             1750  INPLACE_SUBTRACT 
             1752  STORE_FAST               'start'

 L. 460      1754  LOAD_CONST               2
             1756  STORE_FAST               'used'
         1758_1760  JUMP_BACK          1728  'to 1728'
             1762  POP_BLOCK        
           1764_0  COME_FROM_LOOP     1722  '1722'

 L. 461      1764  SETUP_LOOP         1806  'to 1806'
             1766  LOAD_FAST                'suffix_nexts'
             1768  GET_ITER         
           1770_0  COME_FROM          1780  '1780'
             1770  FOR_ITER           1804  'to 1804'
             1772  STORE_FAST               'w'

 L. 462      1774  LOAD_FAST                'wordNext'
             1776  LOAD_FAST                'w'
             1778  COMPARE_OP               ==
         1780_1782  POP_JUMP_IF_FALSE  1770  'to 1770'

 L. 463      1784  LOAD_CONST               7
             1786  STORE_DEREF              'yearOffset'

 L. 464      1788  LOAD_FAST                'start'
             1790  LOAD_CONST               1
             1792  INPLACE_SUBTRACT 
             1794  STORE_FAST               'start'

 L. 465      1796  LOAD_CONST               2
             1798  STORE_FAST               'used'
         1800_1802  JUMP_BACK          1770  'to 1770'
             1804  POP_BLOCK        
           1806_0  COME_FROM_LOOP     1764  '1764'

 L. 466      1806  SETUP_LOOP         1848  'to 1848'
             1808  LOAD_FAST                'suffix_lasts'
             1810  GET_ITER         
           1812_0  COME_FROM          1822  '1822'
             1812  FOR_ITER           1846  'to 1846'
             1814  STORE_FAST               'w'

 L. 467      1816  LOAD_FAST                'wordNext'
             1818  LOAD_FAST                'w'
             1820  COMPARE_OP               ==
         1822_1824  POP_JUMP_IF_FALSE  1812  'to 1812'

 L. 468      1826  LOAD_CONST               -7
             1828  STORE_DEREF              'yearOffset'

 L. 469      1830  LOAD_FAST                'start'
             1832  LOAD_CONST               1
             1834  INPLACE_SUBTRACT 
             1836  STORE_FAST               'start'

 L. 470      1838  LOAD_CONST               2
             1840  STORE_FAST               'used'
         1842_1844  JUMP_BACK          1812  'to 1812'
             1846  POP_BLOCK        
           1848_0  COME_FROM_LOOP     1806  '1806'
         1848_1850  JUMP_FORWARD       2620  'to 2620'
           1852_0  COME_FROM          1642  '1642'
           1852_1  COME_FROM          1636  '1636'

 L. 473      1852  LOAD_FAST                'word'
             1854  LOAD_FAST                'days'
             1856  COMPARE_OP               in
         1858_1860  POP_JUMP_IF_FALSE  2138  'to 2138'
             1862  LOAD_FAST                'fromFlag'
         1864_1866  POP_JUMP_IF_TRUE   2138  'to 2138'

 L. 475      1868  LOAD_FAST                'days'
             1870  LOAD_METHOD              index
             1872  LOAD_FAST                'word'
             1874  CALL_METHOD_1         1  '1 positional argument'
             1876  STORE_FAST               'd'

 L. 476      1878  LOAD_FAST                'd'
             1880  LOAD_CONST               1
             1882  BINARY_ADD       
             1884  LOAD_GLOBAL              int
             1886  LOAD_FAST                'today'
             1888  CALL_FUNCTION_1       1  '1 positional argument'
             1890  BINARY_SUBTRACT  
             1892  STORE_DEREF              'dayOffset'

 L. 477      1894  LOAD_CONST               1
             1896  STORE_FAST               'used'

 L. 478      1898  LOAD_DEREF               'dayOffset'
             1900  LOAD_CONST               0
             1902  COMPARE_OP               <
         1904_1906  POP_JUMP_IF_FALSE  1916  'to 1916'

 L. 479      1908  LOAD_DEREF               'dayOffset'
             1910  LOAD_CONST               7
             1912  INPLACE_ADD      
             1914  STORE_DEREF              'dayOffset'
           1916_0  COME_FROM          1904  '1904'

 L. 480      1916  SETUP_LOOP         1966  'to 1966'
             1918  LOAD_FAST                'nexts'
             1920  GET_ITER         
           1922_0  COME_FROM          1932  '1932'
             1922  FOR_ITER           1964  'to 1964'
             1924  STORE_FAST               'w'

 L. 481      1926  LOAD_FAST                'wordPrev'
             1928  LOAD_FAST                'w'
             1930  COMPARE_OP               ==
         1932_1934  POP_JUMP_IF_FALSE  1922  'to 1922'

 L. 482      1936  LOAD_DEREF               'dayOffset'
             1938  LOAD_CONST               7
             1940  INPLACE_ADD      
             1942  STORE_DEREF              'dayOffset'

 L. 483      1944  LOAD_FAST                'used'
             1946  LOAD_CONST               1
             1948  INPLACE_ADD      
             1950  STORE_FAST               'used'

 L. 484      1952  LOAD_FAST                'start'
             1954  LOAD_CONST               1
             1956  INPLACE_SUBTRACT 
             1958  STORE_FAST               'start'
         1960_1962  JUMP_BACK          1922  'to 1922'
             1964  POP_BLOCK        
           1966_0  COME_FROM_LOOP     1916  '1916'

 L. 485      1966  SETUP_LOOP         2016  'to 2016'
             1968  LOAD_FAST                'lasts'
             1970  GET_ITER         
           1972_0  COME_FROM          1982  '1982'
             1972  FOR_ITER           2014  'to 2014'
             1974  STORE_FAST               'w'

 L. 486      1976  LOAD_FAST                'wordPrev'
             1978  LOAD_FAST                'w'
             1980  COMPARE_OP               ==
         1982_1984  POP_JUMP_IF_FALSE  1972  'to 1972'

 L. 487      1986  LOAD_DEREF               'dayOffset'
             1988  LOAD_CONST               7
             1990  INPLACE_SUBTRACT 
             1992  STORE_DEREF              'dayOffset'

 L. 488      1994  LOAD_FAST                'used'
             1996  LOAD_CONST               1
             1998  INPLACE_ADD      
             2000  STORE_FAST               'used'

 L. 489      2002  LOAD_FAST                'start'
             2004  LOAD_CONST               1
             2006  INPLACE_SUBTRACT 
             2008  STORE_FAST               'start'
         2010_2012  JUMP_BACK          1972  'to 1972'
             2014  POP_BLOCK        
           2016_0  COME_FROM_LOOP     1966  '1966'

 L. 490      2016  SETUP_LOOP         2066  'to 2066'
             2018  LOAD_FAST                'suffix_nexts'
             2020  GET_ITER         
           2022_0  COME_FROM          2032  '2032'
             2022  FOR_ITER           2064  'to 2064'
             2024  STORE_FAST               'w'

 L. 491      2026  LOAD_FAST                'wordNext'
             2028  LOAD_FAST                'w'
             2030  COMPARE_OP               ==
         2032_2034  POP_JUMP_IF_FALSE  2022  'to 2022'

 L. 492      2036  LOAD_DEREF               'dayOffset'
             2038  LOAD_CONST               7
             2040  INPLACE_ADD      
             2042  STORE_DEREF              'dayOffset'

 L. 493      2044  LOAD_FAST                'used'
             2046  LOAD_CONST               1
             2048  INPLACE_ADD      
             2050  STORE_FAST               'used'

 L. 494      2052  LOAD_FAST                'start'
             2054  LOAD_CONST               1
             2056  INPLACE_SUBTRACT 
             2058  STORE_FAST               'start'
         2060_2062  JUMP_BACK          2022  'to 2022'
             2064  POP_BLOCK        
           2066_0  COME_FROM_LOOP     2016  '2016'

 L. 495      2066  SETUP_LOOP         2116  'to 2116'
             2068  LOAD_FAST                'suffix_lasts'
             2070  GET_ITER         
           2072_0  COME_FROM          2082  '2082'
             2072  FOR_ITER           2114  'to 2114'
             2074  STORE_FAST               'w'

 L. 496      2076  LOAD_FAST                'wordNext'
             2078  LOAD_FAST                'w'
             2080  COMPARE_OP               ==
         2082_2084  POP_JUMP_IF_FALSE  2072  'to 2072'

 L. 497      2086  LOAD_DEREF               'dayOffset'
             2088  LOAD_CONST               7
             2090  INPLACE_SUBTRACT 
             2092  STORE_DEREF              'dayOffset'

 L. 498      2094  LOAD_FAST                'used'
             2096  LOAD_CONST               1
             2098  INPLACE_ADD      
             2100  STORE_FAST               'used'

 L. 499      2102  LOAD_FAST                'start'
             2104  LOAD_CONST               1
             2106  INPLACE_SUBTRACT 
             2108  STORE_FAST               'start'
         2110_2112  JUMP_BACK          2072  'to 2072'
             2114  POP_BLOCK        
           2116_0  COME_FROM_LOOP     2066  '2066'

 L. 500      2116  LOAD_FAST                'wordNext'
             2118  LOAD_STR                 'feira'
             2120  COMPARE_OP               ==
         2122_2124  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 501      2126  LOAD_FAST                'used'
             2128  LOAD_CONST               1
             2130  INPLACE_ADD      
             2132  STORE_FAST               'used'
         2134_2136  JUMP_FORWARD       2620  'to 2620'
           2138_0  COME_FROM          1864  '1864'
           2138_1  COME_FROM          1858  '1858'

 L. 503      2138  LOAD_FAST                'word'
             2140  LOAD_FAST                'months'
             2142  COMPARE_OP               in
         2144_2146  POP_JUMP_IF_TRUE   2158  'to 2158'
             2148  LOAD_FAST                'word'
             2150  LOAD_FAST                'monthsShort'
             2152  COMPARE_OP               in
         2154_2156  POP_JUMP_IF_FALSE  2620  'to 2620'
           2158_0  COME_FROM          2144  '2144'

 L. 504      2158  SETUP_EXCEPT       2174  'to 2174'

 L. 505      2160  LOAD_FAST                'months'
             2162  LOAD_METHOD              index
             2164  LOAD_FAST                'word'
             2166  CALL_METHOD_1         1  '1 positional argument'
             2168  STORE_FAST               'm'
             2170  POP_BLOCK        
             2172  JUMP_FORWARD       2206  'to 2206'
           2174_0  COME_FROM_EXCEPT   2158  '2158'

 L. 506      2174  DUP_TOP          
             2176  LOAD_GLOBAL              ValueError
             2178  COMPARE_OP               exception-match
         2180_2182  POP_JUMP_IF_FALSE  2204  'to 2204'
             2184  POP_TOP          
             2186  POP_TOP          
             2188  POP_TOP          

 L. 507      2190  LOAD_FAST                'monthsShort'
             2192  LOAD_METHOD              index
             2194  LOAD_FAST                'word'
             2196  CALL_METHOD_1         1  '1 positional argument'
             2198  STORE_FAST               'm'
             2200  POP_EXCEPT       
             2202  JUMP_FORWARD       2206  'to 2206'
           2204_0  COME_FROM          2180  '2180'
             2204  END_FINALLY      
           2206_0  COME_FROM          2202  '2202'
           2206_1  COME_FROM          2172  '2172'

 L. 508      2206  LOAD_FAST                'used'
             2208  LOAD_CONST               1
             2210  INPLACE_ADD      
             2212  STORE_FAST               'used'

 L. 509      2214  LOAD_FAST                'months'
             2216  LOAD_FAST                'm'
             2218  BINARY_SUBSCR    
             2220  STORE_DEREF              'datestr'

 L. 510      2222  LOAD_FAST                'wordPrev'
         2224_2226  POP_JUMP_IF_FALSE  2324  'to 2324'
             2228  LOAD_FAST                'wordPrev'
             2230  LOAD_CONST               0
             2232  BINARY_SUBSCR    
             2234  LOAD_METHOD              isdigit
             2236  CALL_METHOD_0         0  '0 positional arguments'
         2238_2240  POP_JUMP_IF_FALSE  2324  'to 2324'

 L. 512      2242  LOAD_DEREF               'datestr'
             2244  LOAD_STR                 ' '
             2246  LOAD_FAST                'wordPrev'
             2248  BINARY_ADD       
             2250  INPLACE_ADD      
             2252  STORE_DEREF              'datestr'

 L. 513      2254  LOAD_FAST                'start'
             2256  LOAD_CONST               1
             2258  INPLACE_SUBTRACT 
             2260  STORE_FAST               'start'

 L. 514      2262  LOAD_FAST                'used'
             2264  LOAD_CONST               1
             2266  INPLACE_ADD      
             2268  STORE_FAST               'used'

 L. 515      2270  LOAD_FAST                'wordNext'
         2272_2274  POP_JUMP_IF_FALSE  2316  'to 2316'
             2276  LOAD_FAST                'wordNext'
             2278  LOAD_CONST               0
             2280  BINARY_SUBSCR    
             2282  LOAD_METHOD              isdigit
             2284  CALL_METHOD_0         0  '0 positional arguments'
         2286_2288  POP_JUMP_IF_FALSE  2316  'to 2316'

 L. 516      2290  LOAD_DEREF               'datestr'
             2292  LOAD_STR                 ' '
             2294  LOAD_FAST                'wordNext'
             2296  BINARY_ADD       
             2298  INPLACE_ADD      
             2300  STORE_DEREF              'datestr'

 L. 517      2302  LOAD_FAST                'used'
             2304  LOAD_CONST               1
             2306  INPLACE_ADD      
             2308  STORE_FAST               'used'

 L. 518      2310  LOAD_CONST               True
             2312  STORE_FAST               'hasYear'
             2314  JUMP_FORWARD       2606  'to 2606'
           2316_0  COME_FROM          2286  '2286'
           2316_1  COME_FROM          2272  '2272'

 L. 520      2316  LOAD_CONST               False
             2318  STORE_FAST               'hasYear'
         2320_2322  JUMP_FORWARD       2606  'to 2606'
           2324_0  COME_FROM          2238  '2238'
           2324_1  COME_FROM          2224  '2224'

 L. 522      2324  LOAD_FAST                'wordNext'
         2326_2328  POP_JUMP_IF_FALSE  2416  'to 2416'
             2330  LOAD_FAST                'wordNext'
             2332  LOAD_CONST               0
             2334  BINARY_SUBSCR    
             2336  LOAD_METHOD              isdigit
             2338  CALL_METHOD_0         0  '0 positional arguments'
         2340_2342  POP_JUMP_IF_FALSE  2416  'to 2416'

 L. 524      2344  LOAD_DEREF               'datestr'
             2346  LOAD_STR                 ' '
             2348  LOAD_FAST                'wordNext'
             2350  BINARY_ADD       
             2352  INPLACE_ADD      
             2354  STORE_DEREF              'datestr'

 L. 525      2356  LOAD_FAST                'used'
             2358  LOAD_CONST               1
             2360  INPLACE_ADD      
             2362  STORE_FAST               'used'

 L. 526      2364  LOAD_FAST                'wordNextNext'
         2366_2368  POP_JUMP_IF_FALSE  2410  'to 2410'
             2370  LOAD_FAST                'wordNextNext'
             2372  LOAD_CONST               0
             2374  BINARY_SUBSCR    
             2376  LOAD_METHOD              isdigit
             2378  CALL_METHOD_0         0  '0 positional arguments'
         2380_2382  POP_JUMP_IF_FALSE  2410  'to 2410'

 L. 527      2384  LOAD_DEREF               'datestr'
             2386  LOAD_STR                 ' '
             2388  LOAD_FAST                'wordNextNext'
             2390  BINARY_ADD       
             2392  INPLACE_ADD      
             2394  STORE_DEREF              'datestr'

 L. 528      2396  LOAD_FAST                'used'
             2398  LOAD_CONST               1
             2400  INPLACE_ADD      
             2402  STORE_FAST               'used'

 L. 529      2404  LOAD_CONST               True
             2406  STORE_FAST               'hasYear'
             2408  JUMP_FORWARD       2414  'to 2414'
           2410_0  COME_FROM          2380  '2380'
           2410_1  COME_FROM          2366  '2366'

 L. 531      2410  LOAD_CONST               False
             2412  STORE_FAST               'hasYear'
           2414_0  COME_FROM          2408  '2408'
             2414  JUMP_FORWARD       2606  'to 2606'
           2416_0  COME_FROM          2340  '2340'
           2416_1  COME_FROM          2326  '2326'

 L. 533      2416  LOAD_FAST                'wordPrevPrev'
         2418_2420  POP_JUMP_IF_FALSE  2516  'to 2516'
             2422  LOAD_FAST                'wordPrevPrev'
             2424  LOAD_CONST               0
             2426  BINARY_SUBSCR    
             2428  LOAD_METHOD              isdigit
             2430  CALL_METHOD_0         0  '0 positional arguments'
         2432_2434  POP_JUMP_IF_FALSE  2516  'to 2516'

 L. 535      2436  LOAD_DEREF               'datestr'
             2438  LOAD_STR                 ' '
             2440  LOAD_FAST                'wordPrevPrev'
             2442  BINARY_ADD       
             2444  INPLACE_ADD      
             2446  STORE_DEREF              'datestr'

 L. 537      2448  LOAD_FAST                'start'
             2450  LOAD_CONST               2
             2452  INPLACE_SUBTRACT 
             2454  STORE_FAST               'start'

 L. 538      2456  LOAD_FAST                'used'
             2458  LOAD_CONST               2
             2460  INPLACE_ADD      
             2462  STORE_FAST               'used'

 L. 539      2464  LOAD_FAST                'wordNext'
         2466_2468  POP_JUMP_IF_FALSE  2510  'to 2510'
             2470  LOAD_FAST                'word'
             2472  LOAD_CONST               0
             2474  BINARY_SUBSCR    
             2476  LOAD_METHOD              isdigit
           2478_0  COME_FROM          1034  '1034'
             2478  CALL_METHOD_0         0  '0 positional arguments'
         2480_2482  POP_JUMP_IF_FALSE  2510  'to 2510'

 L. 540      2484  LOAD_DEREF               'datestr'
             2486  LOAD_STR                 ' '
             2488  LOAD_FAST                'wordNext'
             2490  BINARY_ADD       
             2492  INPLACE_ADD      
             2494  STORE_DEREF              'datestr'

 L. 541      2496  LOAD_FAST                'used'
             2498  LOAD_CONST               1
             2500  INPLACE_ADD      
             2502  STORE_FAST               'used'

 L. 542      2504  LOAD_CONST               True
             2506  STORE_FAST               'hasYear'
             2508  JUMP_FORWARD       2514  'to 2514'
           2510_0  COME_FROM          2480  '2480'
           2510_1  COME_FROM          2466  '2466'

 L. 544      2510  LOAD_CONST               False
             2512  STORE_FAST               'hasYear'
           2514_0  COME_FROM          2508  '2508'
             2514  JUMP_FORWARD       2606  'to 2606'
           2516_0  COME_FROM          2432  '2432'
           2516_1  COME_FROM          2418  '2418'

 L. 546      2516  LOAD_FAST                'wordNextNext'
         2518_2520  POP_JUMP_IF_FALSE  2606  'to 2606'
             2522  LOAD_FAST                'wordNextNext'
             2524  LOAD_CONST               0
             2526  BINARY_SUBSCR    
             2528  LOAD_METHOD              isdigit
             2530  CALL_METHOD_0         0  '0 positional arguments'
         2532_2534  POP_JUMP_IF_FALSE  2606  'to 2606'

 L. 548      2536  LOAD_DEREF               'datestr'
             2538  LOAD_STR                 ' '
             2540  LOAD_FAST                'wordNextNext'
             2542  BINARY_ADD       
             2544  INPLACE_ADD      
             2546  STORE_DEREF              'datestr'
           2548_0  COME_FROM          1104  '1104'

 L. 549      2548  LOAD_FAST                'used'
             2550  LOAD_CONST               2
             2552  INPLACE_ADD      
             2554  STORE_FAST               'used'

 L. 550      2556  LOAD_FAST                'wordNextNextNext'
         2558_2560  POP_JUMP_IF_FALSE  2602  'to 2602'
             2562  LOAD_FAST                'wordNextNextNext'
             2564  LOAD_CONST               0
             2566  BINARY_SUBSCR    
             2568  LOAD_METHOD              isdigit
             2570  CALL_METHOD_0         0  '0 positional arguments'
         2572_2574  POP_JUMP_IF_FALSE  2602  'to 2602'

 L. 551      2576  LOAD_DEREF               'datestr'
             2578  LOAD_STR                 ' '
             2580  LOAD_FAST                'wordNextNextNext'
             2582  BINARY_ADD       
             2584  INPLACE_ADD      
             2586  STORE_DEREF              'datestr'

 L. 552      2588  LOAD_FAST                'used'
             2590  LOAD_CONST               1
             2592  INPLACE_ADD      
             2594  STORE_FAST               'used'

 L. 553      2596  LOAD_CONST               True
           2598_0  COME_FROM          2314  '2314'
             2598  STORE_FAST               'hasYear'
             2600  JUMP_FORWARD       2606  'to 2606'
           2602_0  COME_FROM          2572  '2572'
           2602_1  COME_FROM          2558  '2558'

 L. 555      2602  LOAD_CONST               False
             2604  STORE_FAST               'hasYear'
           2606_0  COME_FROM          2600  '2600'
           2606_1  COME_FROM          2532  '2532'
           2606_2  COME_FROM          2518  '2518'
           2606_3  COME_FROM          2514  '2514'
           2606_4  COME_FROM          2414  '2414'
           2606_5  COME_FROM          2320  '2320'

 L. 557      2606  LOAD_DEREF               'datestr'
             2608  LOAD_FAST                'months'
             2610  COMPARE_OP               in
         2612_2614  POP_JUMP_IF_FALSE  2620  'to 2620'

 L. 558      2616  LOAD_STR                 ''
             2618  STORE_DEREF              'datestr'
           2620_0  COME_FROM          2612  '2612'
           2620_1  COME_FROM          2154  '2154'
           2620_2  COME_FROM          2134  '2134'
           2620_3  COME_FROM          2122  '2122'
           2620_4  COME_FROM          1848  '1848'
           2620_5  COME_FROM          1626  '1626'
           2620_6  COME_FROM          1404  '1404'
           2620_7  COME_FROM          1174  '1174'
           2620_8  COME_FROM          1142  '1142'
           2620_9  COME_FROM          1132  '1132'
          2620_10  COME_FROM          1122  '1122'
          2620_11  COME_FROM          1108  '1108'
          2620_12  COME_FROM           944  '944'
          2620_13  COME_FROM           902  '902'
          2620_14  COME_FROM           860  '860'
          2620_15  COME_FROM           824  '824'
          2620_16  COME_FROM           768  '768'
          2620_17  COME_FROM           756  '756'
          2620_18  COME_FROM           694  '694'
          2620_19  COME_FROM           658  '658'
          2620_20  COME_FROM           626  '626'
          2620_21  COME_FROM           594  '594'

 L. 562      2620  LOAD_FAST                'days'
             2622  LOAD_FAST                'months'
             2624  BINARY_ADD       
             2626  LOAD_FAST                'monthsShort'
             2628  BINARY_ADD       
             2630  STORE_FAST               'validFollowups'

 L. 563      2632  LOAD_FAST                'validFollowups'
             2634  LOAD_METHOD              append
             2636  LOAD_STR                 'hoje'
             2638  CALL_METHOD_1         1  '1 positional argument'
             2640  POP_TOP          

 L. 564      2642  LOAD_FAST                'validFollowups'
             2644  LOAD_METHOD              append
             2646  LOAD_STR                 'amanha'
             2648  CALL_METHOD_1         1  '1 positional argument'
             2650  POP_TOP          

 L. 565      2652  LOAD_FAST                'validFollowups'
             2654  LOAD_METHOD              append
             2656  LOAD_STR                 'ontem'
             2658  CALL_METHOD_1         1  '1 positional argument'
             2660  POP_TOP          

 L. 566      2662  LOAD_FAST                'validFollowups'
             2664  LOAD_METHOD              append
             2666  LOAD_STR                 'anteontem'
             2668  CALL_METHOD_1         1  '1 positional argument'
             2670  POP_TOP          

 L. 567      2672  LOAD_FAST                'validFollowups'
             2674  LOAD_METHOD              append
             2676  LOAD_STR                 'agora'
             2678  CALL_METHOD_1         1  '1 positional argument'
             2680  POP_TOP          

 L. 568      2682  LOAD_FAST                'validFollowups'
             2684  LOAD_METHOD              append
             2686  LOAD_STR                 'ja'
             2688  CALL_METHOD_1         1  '1 positional argument'
             2690  POP_TOP          

 L. 569      2692  LOAD_FAST                'validFollowups'
             2694  LOAD_METHOD              append
             2696  LOAD_STR                 'ante'
             2698  CALL_METHOD_1         1  '1 positional argument'
             2700  POP_TOP          

 L. 572      2702  LOAD_FAST                'word'
             2704  LOAD_FAST                'froms'
             2706  COMPARE_OP               in
         2708_2710  POP_JUMP_IF_FALSE  3208  'to 3208'
             2712  LOAD_FAST                'wordNext'
             2714  LOAD_FAST                'validFollowups'
             2716  COMPARE_OP               in
         2718_2720  POP_JUMP_IF_FALSE  3208  'to 3208'

 L. 574      2722  LOAD_FAST                'wordNext'
             2724  LOAD_STR                 'amanha'
             2726  COMPARE_OP               ==
         2728_2730  POP_JUMP_IF_FALSE  2742  'to 2742'
             2732  LOAD_FAST                'wordNext'
             2734  LOAD_STR                 'ontem'
             2736  COMPARE_OP               ==
         2738_2740  POP_JUMP_IF_TRUE   2780  'to 2780'
           2742_0  COME_FROM          2728  '2728'

 L. 575      2742  LOAD_FAST                'word'
             2744  LOAD_STR                 'depois'
             2746  COMPARE_OP               ==
         2748_2750  POP_JUMP_IF_TRUE   2780  'to 2780'
             2752  LOAD_FAST                'word'
             2754  LOAD_STR                 'antes'
             2756  COMPARE_OP               ==
         2758_2760  POP_JUMP_IF_TRUE   2780  'to 2780'
             2762  LOAD_FAST                'word'
             2764  LOAD_STR                 'em'
             2766  COMPARE_OP               ==
         2768_2770  POP_JUMP_IF_TRUE   2780  'to 2780'

 L. 576      2772  LOAD_CONST               2
             2774  STORE_FAST               'used'

 L. 577      2776  LOAD_CONST               True
             2778  STORE_FAST               'fromFlag'
           2780_0  COME_FROM          2768  '2768'
           2780_1  COME_FROM          2758  '2758'
           2780_2  COME_FROM          2748  '2748'
           2780_3  COME_FROM          2738  '2738'

 L. 578      2780  LOAD_FAST                'wordNext'
             2782  LOAD_STR                 'amanha'
             2784  COMPARE_OP               ==
         2786_2788  POP_JUMP_IF_FALSE  2812  'to 2812'
             2790  LOAD_FAST                'word'
             2792  LOAD_STR                 'depois'
             2794  COMPARE_OP               !=
         2796_2798  POP_JUMP_IF_FALSE  2812  'to 2812'

 L. 579      2800  LOAD_DEREF               'dayOffset'
             2802  LOAD_CONST               1
             2804  INPLACE_ADD      
             2806  STORE_DEREF              'dayOffset'
         2808_2810  JUMP_FORWARD       3208  'to 3208'
           2812_0  COME_FROM          2796  '2796'
           2812_1  COME_FROM          2786  '2786'

 L. 580      2812  LOAD_FAST                'wordNext'
             2814  LOAD_STR                 'ontem'
             2816  COMPARE_OP               ==
         2818_2820  POP_JUMP_IF_FALSE  2834  'to 2834'

 L. 581      2822  LOAD_DEREF               'dayOffset'
             2824  LOAD_CONST               1
             2826  INPLACE_SUBTRACT 
             2828  STORE_DEREF              'dayOffset'
         2830_2832  JUMP_FORWARD       3208  'to 3208'
           2834_0  COME_FROM          2818  '2818'

 L. 582      2834  LOAD_FAST                'wordNext'
             2836  LOAD_STR                 'anteontem'
             2838  COMPARE_OP               ==
         2840_2842  POP_JUMP_IF_FALSE  2856  'to 2856'

 L. 583      2844  LOAD_DEREF               'dayOffset'
             2846  LOAD_CONST               2
             2848  INPLACE_SUBTRACT 
             2850  STORE_DEREF              'dayOffset'
         2852_2854  JUMP_FORWARD       3208  'to 3208'
           2856_0  COME_FROM          2840  '2840'

 L. 584      2856  LOAD_FAST                'wordNext'
             2858  LOAD_STR                 'ante'
             2860  COMPARE_OP               ==
         2862_2864  POP_JUMP_IF_FALSE  2888  'to 2888'
             2866  LOAD_FAST                'wordNextNext'
             2868  LOAD_STR                 'ontem'
             2870  COMPARE_OP               ==
         2872_2874  POP_JUMP_IF_FALSE  2888  'to 2888'

 L. 585      2876  LOAD_DEREF               'dayOffset'
             2878  LOAD_CONST               2
             2880  INPLACE_SUBTRACT 
             2882  STORE_DEREF              'dayOffset'
         2884_2886  JUMP_FORWARD       3208  'to 3208'
           2888_0  COME_FROM          2872  '2872'
           2888_1  COME_FROM          2862  '2862'

 L. 586      2888  LOAD_FAST                'wordNext'
             2890  LOAD_STR                 'ante'
             2892  COMPARE_OP               ==
         2894_2896  POP_JUMP_IF_FALSE  2930  'to 2930'
             2898  LOAD_FAST                'wordNextNext'
             2900  LOAD_STR                 'ante'
             2902  COMPARE_OP               ==
         2904_2906  POP_JUMP_IF_FALSE  2930  'to 2930'

 L. 587      2908  LOAD_FAST                'wordNextNextNext'
             2910  LOAD_STR                 'ontem'
             2912  COMPARE_OP               ==
         2914_2916  POP_JUMP_IF_FALSE  2930  'to 2930'

 L. 588      2918  LOAD_DEREF               'dayOffset'
             2920  LOAD_CONST               3
             2922  INPLACE_SUBTRACT 
             2924  STORE_DEREF              'dayOffset'
         2926_2928  JUMP_FORWARD       3208  'to 3208'
           2930_0  COME_FROM          2914  '2914'
           2930_1  COME_FROM          2904  '2904'
           2930_2  COME_FROM          2894  '2894'

 L. 589      2930  LOAD_FAST                'wordNext'
             2932  LOAD_FAST                'days'
             2934  COMPARE_OP               in
         2936_2938  POP_JUMP_IF_FALSE  3076  'to 3076'

 L. 590      2940  LOAD_FAST                'days'
             2942  LOAD_METHOD              index
             2944  LOAD_FAST                'wordNext'
             2946  CALL_METHOD_1         1  '1 positional argument'
             2948  STORE_FAST               'd'

 L. 591      2950  LOAD_FAST                'd'
             2952  LOAD_CONST               1
             2954  BINARY_ADD       
             2956  LOAD_GLOBAL              int
             2958  LOAD_FAST                'today'
             2960  CALL_FUNCTION_1       1  '1 positional argument'
             2962  BINARY_SUBTRACT  
             2964  STORE_FAST               'tmpOffset'

 L. 592      2966  LOAD_CONST               2
             2968  STORE_FAST               'used'

 L. 593      2970  LOAD_FAST                'wordNextNext'
             2972  LOAD_STR                 'feira'
             2974  COMPARE_OP               ==
         2976_2978  POP_JUMP_IF_FALSE  2988  'to 2988'

 L. 594      2980  LOAD_FAST                'used'
             2982  LOAD_CONST               1
             2984  INPLACE_ADD      
             2986  STORE_FAST               'used'
           2988_0  COME_FROM          2976  '2976'

 L. 595      2988  LOAD_FAST                'tmpOffset'
             2990  LOAD_CONST               0
             2992  COMPARE_OP               <
         2994_2996  POP_JUMP_IF_FALSE  3006  'to 3006'

 L. 596      2998  LOAD_FAST                'tmpOffset'
             3000  LOAD_CONST               7
             3002  INPLACE_ADD      
             3004  STORE_FAST               'tmpOffset'
           3006_0  COME_FROM          2994  '2994'

 L. 597      3006  LOAD_FAST                'wordNextNext'
         3008_3010  POP_JUMP_IF_FALSE  3066  'to 3066'

 L. 598      3012  LOAD_FAST                'wordNextNext'
             3014  LOAD_FAST                'nxts'
             3016  COMPARE_OP               in
         3018_3020  POP_JUMP_IF_FALSE  3040  'to 3040'

 L. 599      3022  LOAD_FAST                'tmpOffset'
             3024  LOAD_CONST               7
             3026  INPLACE_ADD      
             3028  STORE_FAST               'tmpOffset'

 L. 600      3030  LOAD_FAST                'used'
             3032  LOAD_CONST               1
             3034  INPLACE_ADD      
             3036  STORE_FAST               'used'
             3038  JUMP_FORWARD       3066  'to 3066'
           3040_0  COME_FROM          3018  '3018'

 L. 601      3040  LOAD_FAST                'wordNextNext'
             3042  LOAD_FAST                'prevs'
             3044  COMPARE_OP               in
         3046_3048  POP_JUMP_IF_FALSE  3066  'to 3066'

 L. 602      3050  LOAD_FAST                'tmpOffset'
             3052  LOAD_CONST               7
             3054  INPLACE_SUBTRACT 
             3056  STORE_FAST               'tmpOffset'

 L. 603      3058  LOAD_FAST                'used'
             3060  LOAD_CONST               1
             3062  INPLACE_ADD      
             3064  STORE_FAST               'used'
           3066_0  COME_FROM          3046  '3046'
           3066_1  COME_FROM          3038  '3038'
           3066_2  COME_FROM          3008  '3008'

 L. 604      3066  LOAD_DEREF               'dayOffset'
             3068  LOAD_FAST                'tmpOffset'
             3070  INPLACE_ADD      
             3072  STORE_DEREF              'dayOffset'
             3074  JUMP_FORWARD       3208  'to 3208'
           3076_0  COME_FROM          2936  '2936'

 L. 605      3076  LOAD_FAST                'wordNextNext'
         3078_3080  POP_JUMP_IF_FALSE  3208  'to 3208'
             3082  LOAD_FAST                'wordNextNext'
             3084  LOAD_FAST                'days'
             3086  COMPARE_OP               in
         3088_3090  POP_JUMP_IF_FALSE  3208  'to 3208'

 L. 606      3092  LOAD_FAST                'days'
             3094  LOAD_METHOD              index
             3096  LOAD_FAST                'wordNextNext'
             3098  CALL_METHOD_1         1  '1 positional argument'
             3100  STORE_FAST               'd'

 L. 607      3102  LOAD_FAST                'd'
             3104  LOAD_CONST               1
             3106  BINARY_ADD       
             3108  LOAD_GLOBAL              int
             3110  LOAD_FAST                'today'
             3112  CALL_FUNCTION_1       1  '1 positional argument'
             3114  BINARY_SUBTRACT  
             3116  STORE_FAST               'tmpOffset'

 L. 608      3118  LOAD_CONST               3
             3120  STORE_FAST               'used'

 L. 609      3122  LOAD_FAST                'wordNextNextNext'
         3124_3126  POP_JUMP_IF_FALSE  3182  'to 3182'

 L. 610      3128  LOAD_FAST                'wordNextNextNext'
             3130  LOAD_FAST                'nxts'
             3132  COMPARE_OP               in
         3134_3136  POP_JUMP_IF_FALSE  3156  'to 3156'

 L. 611      3138  LOAD_FAST                'tmpOffset'
             3140  LOAD_CONST               7
             3142  INPLACE_ADD      
             3144  STORE_FAST               'tmpOffset'

 L. 612      3146  LOAD_FAST                'used'
             3148  LOAD_CONST               1
             3150  INPLACE_ADD      
             3152  STORE_FAST               'used'
             3154  JUMP_FORWARD       3182  'to 3182'
           3156_0  COME_FROM          3134  '3134'

 L. 613      3156  LOAD_FAST                'wordNextNextNext'
             3158  LOAD_FAST                'prevs'
             3160  COMPARE_OP               in
         3162_3164  POP_JUMP_IF_FALSE  3182  'to 3182'

 L. 614      3166  LOAD_FAST                'tmpOffset'
             3168  LOAD_CONST               7
             3170  INPLACE_SUBTRACT 
             3172  STORE_FAST               'tmpOffset'

 L. 615      3174  LOAD_FAST                'used'
             3176  LOAD_CONST               1
             3178  INPLACE_ADD      
             3180  STORE_FAST               'used'
           3182_0  COME_FROM          3162  '3162'
           3182_1  COME_FROM          3154  '3154'
           3182_2  COME_FROM          3124  '3124'

 L. 616      3182  LOAD_DEREF               'dayOffset'
             3184  LOAD_FAST                'tmpOffset'
             3186  INPLACE_ADD      
             3188  STORE_DEREF              'dayOffset'

 L. 617      3190  LOAD_FAST                'wordNextNextNext'
             3192  LOAD_STR                 'feira'
             3194  COMPARE_OP               ==
         3196_3198  POP_JUMP_IF_FALSE  3208  'to 3208'

 L. 618      3200  LOAD_FAST                'used'
             3202  LOAD_CONST               1
             3204  INPLACE_ADD      
             3206  STORE_FAST               'used'
           3208_0  COME_FROM          3196  '3196'
           3208_1  COME_FROM          3088  '3088'
           3208_2  COME_FROM          3078  '3078'
           3208_3  COME_FROM          3074  '3074'
           3208_4  COME_FROM          2926  '2926'
           3208_5  COME_FROM          2884  '2884'
           3208_6  COME_FROM          2852  '2852'
           3208_7  COME_FROM          2830  '2830'
           3208_8  COME_FROM          2808  '2808'
           3208_9  COME_FROM          2718  '2718'
          3208_10  COME_FROM          2708  '2708'

 L. 619      3208  LOAD_FAST                'wordNext'
             3210  LOAD_FAST                'months'
             3212  COMPARE_OP               in
         3214_3216  POP_JUMP_IF_FALSE  3226  'to 3226'

 L. 620      3218  LOAD_FAST                'used'
             3220  LOAD_CONST               1
             3222  INPLACE_SUBTRACT 
             3224  STORE_FAST               'used'
           3226_0  COME_FROM          3214  '3214'

 L. 621      3226  LOAD_FAST                'used'
             3228  LOAD_CONST               0
             3230  COMPARE_OP               >
         3232_3234  POP_JUMP_IF_FALSE   394  'to 394'

 L. 623      3236  LOAD_FAST                'start'
             3238  LOAD_CONST               1
             3240  BINARY_SUBTRACT  
             3242  LOAD_CONST               0
             3244  COMPARE_OP               >
         3246_3248  POP_JUMP_IF_FALSE  3284  'to 3284'
             3250  LOAD_FAST                'words'
             3252  LOAD_FAST                'start'
             3254  LOAD_CONST               1
             3256  BINARY_SUBTRACT  
             3258  BINARY_SUBSCR    
             3260  LOAD_FAST                'lists'
             3262  COMPARE_OP               in
         3264_3266  POP_JUMP_IF_FALSE  3284  'to 3284'

 L. 624      3268  LOAD_FAST                'start'
             3270  LOAD_CONST               1
             3272  INPLACE_SUBTRACT 
             3274  STORE_FAST               'start'

 L. 625      3276  LOAD_FAST                'used'
             3278  LOAD_CONST               1
             3280  INPLACE_ADD      
             3282  STORE_FAST               'used'
           3284_0  COME_FROM          3264  '3264'
           3284_1  COME_FROM          3246  '3246'

 L. 627      3284  SETUP_LOOP         3318  'to 3318'
             3286  LOAD_GLOBAL              range
             3288  LOAD_CONST               0
             3290  LOAD_FAST                'used'
             3292  CALL_FUNCTION_2       2  '2 positional arguments'
             3294  GET_ITER         
             3296  FOR_ITER           3316  'to 3316'
             3298  STORE_FAST               'i'

 L. 628      3300  LOAD_STR                 ''
             3302  LOAD_FAST                'words'
             3304  LOAD_FAST                'i'
             3306  LOAD_FAST                'start'
             3308  BINARY_ADD       
             3310  STORE_SUBSCR     
         3312_3314  JUMP_BACK          3296  'to 3296'
             3316  POP_BLOCK        
           3318_0  COME_FROM_LOOP     3284  '3284'

 L. 630      3318  LOAD_FAST                'start'
             3320  LOAD_CONST               1
             3322  BINARY_SUBTRACT  
             3324  LOAD_CONST               0
             3326  COMPARE_OP               >=
         3328_3330  POP_JUMP_IF_FALSE  3362  'to 3362'
             3332  LOAD_FAST                'words'
             3334  LOAD_FAST                'start'
             3336  LOAD_CONST               1
             3338  BINARY_SUBTRACT  
             3340  BINARY_SUBSCR    
             3342  LOAD_FAST                'lists'
             3344  COMPARE_OP               in
         3346_3348  POP_JUMP_IF_FALSE  3362  'to 3362'

 L. 631      3350  LOAD_STR                 ''
             3352  LOAD_FAST                'words'
             3354  LOAD_FAST                'start'
             3356  LOAD_CONST               1
             3358  BINARY_SUBTRACT  
             3360  STORE_SUBSCR     
           3362_0  COME_FROM          3346  '3346'
           3362_1  COME_FROM          3328  '3328'

 L. 632      3362  LOAD_CONST               True
             3364  STORE_DEREF              'found'

 L. 633      3366  LOAD_CONST               True
             3368  STORE_FAST               'daySpecified'
         3370_3372  JUMP_BACK           394  'to 394'
             3374  POP_BLOCK        
           3376_0  COME_FROM_LOOP      382  '382'

 L. 636      3376  LOAD_STR                 ''
             3378  STORE_DEREF              'timeStr'

 L. 637      3380  LOAD_CONST               0
             3382  STORE_DEREF              'hrOffset'

 L. 638      3384  LOAD_CONST               0
             3386  STORE_DEREF              'minOffset'

 L. 639      3388  LOAD_CONST               0
             3390  STORE_DEREF              'secOffset'

 L. 640      3392  LOAD_CONST               None
             3394  STORE_DEREF              'hrAbs'

 L. 641      3396  LOAD_CONST               None
             3398  STORE_DEREF              'minAbs'

 L. 642      3400  LOAD_CONST               False
             3402  STORE_FAST               'military'

 L. 644  3404_3406  SETUP_LOOP         5930  'to 5930'
             3408  LOAD_GLOBAL              enumerate
             3410  LOAD_FAST                'words'
             3412  CALL_FUNCTION_1       1  '1 positional argument'
             3414  GET_ITER         
           3416_0  COME_FROM          5774  '5774'
         3416_3418  FOR_ITER           5928  'to 5928'
             3420  UNPACK_SEQUENCE_2     2 
             3422  STORE_FAST               'idx'
             3424  STORE_FAST               'word'

 L. 645      3426  LOAD_FAST                'word'
             3428  LOAD_STR                 ''
             3430  COMPARE_OP               ==
         3432_3434  POP_JUMP_IF_FALSE  3440  'to 3440'

 L. 646  3436_3438  CONTINUE           3416  'to 3416'
           3440_0  COME_FROM          3432  '3432'

 L. 648      3440  LOAD_FAST                'idx'
             3442  LOAD_CONST               1
             3444  COMPARE_OP               >
         3446_3448  POP_JUMP_IF_FALSE  3462  'to 3462'
             3450  LOAD_FAST                'words'
             3452  LOAD_FAST                'idx'
             3454  LOAD_CONST               2
             3456  BINARY_SUBTRACT  
             3458  BINARY_SUBSCR    
             3460  JUMP_FORWARD       3464  'to 3464'
           3462_0  COME_FROM          3446  '3446'
             3462  LOAD_STR                 ''
           3464_0  COME_FROM          3460  '3460'
             3464  STORE_FAST               'wordPrevPrev'

 L. 649      3466  LOAD_FAST                'idx'
             3468  LOAD_CONST               0
             3470  COMPARE_OP               >
         3472_3474  POP_JUMP_IF_FALSE  3488  'to 3488'
             3476  LOAD_FAST                'words'
             3478  LOAD_FAST                'idx'
             3480  LOAD_CONST               1
             3482  BINARY_SUBTRACT  
             3484  BINARY_SUBSCR    
             3486  JUMP_FORWARD       3490  'to 3490'
           3488_0  COME_FROM          3472  '3472'
             3488  LOAD_STR                 ''
           3490_0  COME_FROM          3486  '3486'
             3490  STORE_FAST               'wordPrev'

 L. 650      3492  LOAD_FAST                'idx'
             3494  LOAD_CONST               1
             3496  BINARY_ADD       
             3498  LOAD_GLOBAL              len
             3500  LOAD_FAST                'words'
             3502  CALL_FUNCTION_1       1  '1 positional argument'
             3504  COMPARE_OP               <
         3506_3508  POP_JUMP_IF_FALSE  3522  'to 3522'
             3510  LOAD_FAST                'words'
             3512  LOAD_FAST                'idx'
             3514  LOAD_CONST               1
             3516  BINARY_ADD       
             3518  BINARY_SUBSCR    
             3520  JUMP_FORWARD       3524  'to 3524'
           3522_0  COME_FROM          3506  '3506'
             3522  LOAD_STR                 ''
           3524_0  COME_FROM          3520  '3520'
             3524  STORE_FAST               'wordNext'

 L. 651      3526  LOAD_FAST                'idx'
             3528  LOAD_CONST               2
             3530  BINARY_ADD       
             3532  LOAD_GLOBAL              len
             3534  LOAD_FAST                'words'
             3536  CALL_FUNCTION_1       1  '1 positional argument'
             3538  COMPARE_OP               <
         3540_3542  POP_JUMP_IF_FALSE  3556  'to 3556'
             3544  LOAD_FAST                'words'
             3546  LOAD_FAST                'idx'
             3548  LOAD_CONST               2
             3550  BINARY_ADD       
             3552  BINARY_SUBSCR    
             3554  JUMP_FORWARD       3558  'to 3558'
           3556_0  COME_FROM          3540  '3540'
             3556  LOAD_STR                 ''
           3558_0  COME_FROM          3554  '3554'
             3558  STORE_FAST               'wordNextNext'

 L. 652      3560  LOAD_FAST                'idx'
             3562  LOAD_CONST               3
             3564  BINARY_ADD       
             3566  LOAD_GLOBAL              len
             3568  LOAD_FAST                'words'
             3570  CALL_FUNCTION_1       1  '1 positional argument'
             3572  COMPARE_OP               <
         3574_3576  POP_JUMP_IF_FALSE  3590  'to 3590'
             3578  LOAD_FAST                'words'
             3580  LOAD_FAST                'idx'
             3582  LOAD_CONST               3
             3584  BINARY_ADD       
             3586  BINARY_SUBSCR    
             3588  JUMP_FORWARD       3592  'to 3592'
           3590_0  COME_FROM          3574  '3574'
             3590  LOAD_STR                 ''
           3592_0  COME_FROM          3588  '3588'
             3592  STORE_FAST               'wordNextNextNext'

 L. 654      3594  LOAD_CONST               0
             3596  STORE_FAST               'used'

 L. 655      3598  LOAD_FAST                'word'
             3600  LOAD_STR                 'meio'
             3602  COMPARE_OP               ==
         3604_3606  POP_JUMP_IF_FALSE  3634  'to 3634'
             3608  LOAD_FAST                'wordNext'
             3610  LOAD_STR                 'dia'
             3612  COMPARE_OP               ==
         3614_3616  POP_JUMP_IF_FALSE  3634  'to 3634'

 L. 656      3618  LOAD_CONST               12
             3620  STORE_DEREF              'hrAbs'

 L. 657      3622  LOAD_FAST                'used'
             3624  LOAD_CONST               2
             3626  INPLACE_ADD      
             3628  STORE_FAST               'used'
         3630_3632  JUMP_FORWARD       5768  'to 5768'
           3634_0  COME_FROM          3614  '3614'
           3634_1  COME_FROM          3604  '3604'

 L. 658      3634  LOAD_FAST                'word'
             3636  LOAD_STR                 'meia'
             3638  COMPARE_OP               ==
         3640_3642  POP_JUMP_IF_FALSE  3670  'to 3670'
             3644  LOAD_FAST                'wordNext'
             3646  LOAD_STR                 'noite'
             3648  COMPARE_OP               ==
         3650_3652  POP_JUMP_IF_FALSE  3670  'to 3670'

 L. 659      3654  LOAD_CONST               0
             3656  STORE_DEREF              'hrAbs'

 L. 660      3658  LOAD_FAST                'used'
             3660  LOAD_CONST               2
             3662  INPLACE_ADD      
             3664  STORE_FAST               'used'
         3666_3668  JUMP_FORWARD       5768  'to 5768'
           3670_0  COME_FROM          3650  '3650'
           3670_1  COME_FROM          3640  '3640'

 L. 661      3670  LOAD_FAST                'word'
             3672  LOAD_STR                 'manha'
             3674  COMPARE_OP               ==
         3676_3678  POP_JUMP_IF_FALSE  3702  'to 3702'

 L. 662      3680  LOAD_DEREF               'hrAbs'
         3682_3684  POP_JUMP_IF_TRUE   3690  'to 3690'

 L. 663      3686  LOAD_CONST               8
             3688  STORE_DEREF              'hrAbs'
           3690_0  COME_FROM          3682  '3682'

 L. 664      3690  LOAD_FAST                'used'
             3692  LOAD_CONST               1
             3694  INPLACE_ADD      
             3696  STORE_FAST               'used'
         3698_3700  JUMP_FORWARD       5768  'to 5768'
           3702_0  COME_FROM          3676  '3676'

 L. 665      3702  LOAD_FAST                'word'
             3704  LOAD_STR                 'tarde'
             3706  COMPARE_OP               ==
         3708_3710  POP_JUMP_IF_FALSE  3734  'to 3734'

 L. 666      3712  LOAD_DEREF               'hrAbs'
         3714_3716  POP_JUMP_IF_TRUE   3722  'to 3722'

 L. 667      3718  LOAD_CONST               15
             3720  STORE_DEREF              'hrAbs'
           3722_0  COME_FROM          3714  '3714'

 L. 668      3722  LOAD_FAST                'used'
             3724  LOAD_CONST               1
             3726  INPLACE_ADD      
             3728  STORE_FAST               'used'
         3730_3732  JUMP_FORWARD       5768  'to 5768'
           3734_0  COME_FROM          3708  '3708'

 L. 669      3734  LOAD_FAST                'word'
             3736  LOAD_STR                 'meio'
             3738  COMPARE_OP               ==
         3740_3742  POP_JUMP_IF_FALSE  3776  'to 3776'
             3744  LOAD_FAST                'wordNext'
             3746  LOAD_STR                 'tarde'
             3748  COMPARE_OP               ==
         3750_3752  POP_JUMP_IF_FALSE  3776  'to 3776'

 L. 670      3754  LOAD_DEREF               'hrAbs'
         3756_3758  POP_JUMP_IF_TRUE   3764  'to 3764'

 L. 671      3760  LOAD_CONST               17
             3762  STORE_DEREF              'hrAbs'
           3764_0  COME_FROM          3756  '3756'

 L. 672      3764  LOAD_FAST                'used'
             3766  LOAD_CONST               2
             3768  INPLACE_ADD      
             3770  STORE_FAST               'used'
         3772_3774  JUMP_FORWARD       5768  'to 5768'
           3776_0  COME_FROM          3750  '3750'
           3776_1  COME_FROM          3740  '3740'

 L. 673      3776  LOAD_FAST                'word'
             3778  LOAD_STR                 'meio'
             3780  COMPARE_OP               ==
         3782_3784  POP_JUMP_IF_FALSE  3818  'to 3818'
             3786  LOAD_FAST                'wordNext'
             3788  LOAD_STR                 'manha'
             3790  COMPARE_OP               ==
         3792_3794  POP_JUMP_IF_FALSE  3818  'to 3818'

 L. 674      3796  LOAD_DEREF               'hrAbs'
         3798_3800  POP_JUMP_IF_TRUE   3806  'to 3806'

 L. 675      3802  LOAD_CONST               10
             3804  STORE_DEREF              'hrAbs'
           3806_0  COME_FROM          3798  '3798'

 L. 676      3806  LOAD_FAST                'used'
             3808  LOAD_CONST               2
             3810  INPLACE_ADD      
             3812  STORE_FAST               'used'
         3814_3816  JUMP_FORWARD       5768  'to 5768'
           3818_0  COME_FROM          3792  '3792'
           3818_1  COME_FROM          3782  '3782'

 L. 677      3818  LOAD_FAST                'word'
             3820  LOAD_STR                 'fim'
             3822  COMPARE_OP               ==
         3824_3826  POP_JUMP_IF_FALSE  3860  'to 3860'
             3828  LOAD_FAST                'wordNext'
             3830  LOAD_STR                 'tarde'
             3832  COMPARE_OP               ==
         3834_3836  POP_JUMP_IF_FALSE  3860  'to 3860'

 L. 678      3838  LOAD_DEREF               'hrAbs'
         3840_3842  POP_JUMP_IF_TRUE   3848  'to 3848'

 L. 679      3844  LOAD_CONST               19
             3846  STORE_DEREF              'hrAbs'
           3848_0  COME_FROM          3840  '3840'

 L. 680      3848  LOAD_FAST                'used'
             3850  LOAD_CONST               2
             3852  INPLACE_ADD      
             3854  STORE_FAST               'used'
         3856_3858  JUMP_FORWARD       5768  'to 5768'
           3860_0  COME_FROM          3834  '3834'
           3860_1  COME_FROM          3824  '3824'

 L. 681      3860  LOAD_FAST                'word'
             3862  LOAD_STR                 'fim'
             3864  COMPARE_OP               ==
         3866_3868  POP_JUMP_IF_FALSE  3902  'to 3902'
             3870  LOAD_FAST                'wordNext'
             3872  LOAD_STR                 'manha'
             3874  COMPARE_OP               ==
         3876_3878  POP_JUMP_IF_FALSE  3902  'to 3902'

 L. 682      3880  LOAD_DEREF               'hrAbs'
         3882_3884  POP_JUMP_IF_TRUE   3890  'to 3890'

 L. 683      3886  LOAD_CONST               11
             3888  STORE_DEREF              'hrAbs'
           3890_0  COME_FROM          3882  '3882'

 L. 684      3890  LOAD_FAST                'used'
             3892  LOAD_CONST               2
             3894  INPLACE_ADD      
             3896  STORE_FAST               'used'
         3898_3900  JUMP_FORWARD       5768  'to 5768'
           3902_0  COME_FROM          3876  '3876'
           3902_1  COME_FROM          3866  '3866'

 L. 685      3902  LOAD_FAST                'word'
             3904  LOAD_STR                 'tantas'
             3906  COMPARE_OP               ==
         3908_3910  POP_JUMP_IF_FALSE  3944  'to 3944'
             3912  LOAD_FAST                'wordNext'
             3914  LOAD_STR                 'manha'
             3916  COMPARE_OP               ==
         3918_3920  POP_JUMP_IF_FALSE  3944  'to 3944'

 L. 686      3922  LOAD_DEREF               'hrAbs'
         3924_3926  POP_JUMP_IF_TRUE   3932  'to 3932'

 L. 687      3928  LOAD_CONST               4
             3930  STORE_DEREF              'hrAbs'
           3932_0  COME_FROM          3924  '3924'

 L. 688      3932  LOAD_FAST                'used'
             3934  LOAD_CONST               2
             3936  INPLACE_ADD      
             3938  STORE_FAST               'used'
         3940_3942  JUMP_FORWARD       5768  'to 5768'
           3944_0  COME_FROM          3918  '3918'
           3944_1  COME_FROM          3908  '3908'

 L. 689      3944  LOAD_FAST                'word'
             3946  LOAD_STR                 'noite'
             3948  COMPARE_OP               ==
         3950_3952  POP_JUMP_IF_FALSE  3976  'to 3976'

 L. 690      3954  LOAD_DEREF               'hrAbs'
         3956_3958  POP_JUMP_IF_TRUE   3964  'to 3964'

 L. 691      3960  LOAD_CONST               22
             3962  STORE_DEREF              'hrAbs'
           3964_0  COME_FROM          3956  '3956'

 L. 692      3964  LOAD_FAST                'used'
             3966  LOAD_CONST               1
             3968  INPLACE_ADD      
             3970  STORE_FAST               'used'
         3972_3974  JUMP_FORWARD       5768  'to 5768'
           3976_0  COME_FROM          3950  '3950'

 L. 694      3976  LOAD_FAST                'word'
             3978  LOAD_STR                 'hora'
             3980  COMPARE_OP               ==
         3982_3984  POP_JUMP_IF_FALSE  4164  'to 4164'

 L. 695      3986  LOAD_FAST                'wordPrev'
             3988  LOAD_FAST                'time_indicators'
             3990  COMPARE_OP               in
         3992_3994  POP_JUMP_IF_TRUE   4006  'to 4006'
             3996  LOAD_FAST                'wordPrevPrev'

 L. 696      3998  LOAD_FAST                'time_indicators'
             4000  COMPARE_OP               in
         4002_4004  POP_JUMP_IF_FALSE  4164  'to 4164'
           4006_0  COME_FROM          3992  '3992'

 L. 697      4006  LOAD_FAST                'wordPrev'
             4008  LOAD_STR                 'meia'
             4010  COMPARE_OP               ==
         4012_4014  POP_JUMP_IF_FALSE  4022  'to 4022'

 L. 698      4016  LOAD_CONST               30
             4018  STORE_DEREF              'minOffset'
             4020  JUMP_FORWARD       4110  'to 4110'
           4022_0  COME_FROM          4012  '4012'

 L. 699      4022  LOAD_FAST                'wordPrev'
             4024  LOAD_STR                 'quarto'
             4026  COMPARE_OP               ==
         4028_4030  POP_JUMP_IF_FALSE  4038  'to 4038'

 L. 700      4032  LOAD_CONST               15
             4034  STORE_DEREF              'minOffset'
             4036  JUMP_FORWARD       4110  'to 4110'
           4038_0  COME_FROM          4028  '4028'

 L. 701      4038  LOAD_FAST                'wordPrevPrev'
             4040  LOAD_STR                 'quarto'
             4042  COMPARE_OP               ==
         4044_4046  POP_JUMP_IF_FALSE  4106  'to 4106'

 L. 702      4048  LOAD_CONST               15
             4050  STORE_DEREF              'minOffset'

 L. 703      4052  LOAD_FAST                'idx'
             4054  LOAD_CONST               2
             4056  COMPARE_OP               >
         4058_4060  POP_JUMP_IF_FALSE  4092  'to 4092'
             4062  LOAD_FAST                'words'
             4064  LOAD_FAST                'idx'
             4066  LOAD_CONST               3
             4068  BINARY_SUBTRACT  
             4070  BINARY_SUBSCR    
             4072  LOAD_FAST                'time_indicators'
             4074  COMPARE_OP               in
         4076_4078  POP_JUMP_IF_FALSE  4092  'to 4092'

 L. 704      4080  LOAD_STR                 ''
             4082  LOAD_FAST                'words'
             4084  LOAD_FAST                'idx'
             4086  LOAD_CONST               3
             4088  BINARY_SUBTRACT  
             4090  STORE_SUBSCR     
           4092_0  COME_FROM          4076  '4076'
           4092_1  COME_FROM          4058  '4058'

 L. 705      4092  LOAD_STR                 ''
             4094  LOAD_FAST                'words'
             4096  LOAD_FAST                'idx'
             4098  LOAD_CONST               2
             4100  BINARY_SUBTRACT  
             4102  STORE_SUBSCR     
             4104  JUMP_FORWARD       4110  'to 4110'
           4106_0  COME_FROM          4044  '4044'

 L. 707      4106  LOAD_CONST               1
             4108  STORE_DEREF              'hrOffset'
           4110_0  COME_FROM          4104  '4104'
           4110_1  COME_FROM          4036  '4036'
           4110_2  COME_FROM          4020  '4020'

 L. 708      4110  LOAD_FAST                'wordPrevPrev'
             4112  LOAD_FAST                'time_indicators'
             4114  COMPARE_OP               in
         4116_4118  POP_JUMP_IF_FALSE  4132  'to 4132'

 L. 709      4120  LOAD_STR                 ''
             4122  LOAD_FAST                'words'
             4124  LOAD_FAST                'idx'
             4126  LOAD_CONST               2
             4128  BINARY_SUBTRACT  
             4130  STORE_SUBSCR     
           4132_0  COME_FROM          4116  '4116'

 L. 710      4132  LOAD_STR                 ''
             4134  LOAD_FAST                'words'
             4136  LOAD_FAST                'idx'
             4138  LOAD_CONST               1
             4140  BINARY_SUBTRACT  
             4142  STORE_SUBSCR     

 L. 711      4144  LOAD_FAST                'used'
             4146  LOAD_CONST               1
             4148  INPLACE_ADD      
             4150  STORE_FAST               'used'

 L. 712      4152  LOAD_CONST               -1
             4154  STORE_DEREF              'hrAbs'

 L. 713      4156  LOAD_CONST               -1
             4158  STORE_DEREF              'minAbs'
         4160_4162  JUMP_FORWARD       5768  'to 5768'
           4164_0  COME_FROM          4002  '4002'
           4164_1  COME_FROM          3982  '3982'

 L. 715      4164  LOAD_FAST                'word'
             4166  LOAD_CONST               0
             4168  BINARY_SUBSCR    
             4170  LOAD_METHOD              isdigit
             4172  CALL_METHOD_0         0  '0 positional arguments'
         4174_4176  POP_JUMP_IF_FALSE  5768  'to 5768'

 L. 716      4178  LOAD_CONST               True
             4180  STORE_FAST               'isTime'

 L. 717      4182  LOAD_STR                 ''
             4184  STORE_FAST               'strHH'

 L. 718      4186  LOAD_STR                 ''
             4188  STORE_FAST               'strMM'

 L. 719      4190  LOAD_STR                 ''
             4192  STORE_FAST               'remainder'

 L. 720      4194  LOAD_STR                 ':'
             4196  LOAD_FAST                'word'
             4198  COMPARE_OP               in
         4200_4202  POP_JUMP_IF_FALSE  4710  'to 4710'

 L. 723      4204  LOAD_CONST               0
             4206  STORE_FAST               'stage'

 L. 724      4208  LOAD_GLOBAL              len
             4210  LOAD_FAST                'word'
             4212  CALL_FUNCTION_1       1  '1 positional argument'
             4214  STORE_FAST               'length'

 L. 725      4216  SETUP_LOOP         4392  'to 4392'
             4218  LOAD_GLOBAL              range
             4220  LOAD_FAST                'length'
             4222  CALL_FUNCTION_1       1  '1 positional argument'
             4224  GET_ITER         
           4226_0  COME_FROM          4360  '4360'
             4226  FOR_ITER           4390  'to 4390'
             4228  STORE_FAST               'i'

 L. 726      4230  LOAD_FAST                'stage'
             4232  LOAD_CONST               0
             4234  COMPARE_OP               ==
         4236_4238  POP_JUMP_IF_FALSE  4302  'to 4302'

 L. 727      4240  LOAD_FAST                'word'
             4242  LOAD_FAST                'i'
             4244  BINARY_SUBSCR    
             4246  LOAD_METHOD              isdigit
             4248  CALL_METHOD_0         0  '0 positional arguments'
         4250_4252  POP_JUMP_IF_FALSE  4268  'to 4268'

 L. 728      4254  LOAD_FAST                'strHH'
             4256  LOAD_FAST                'word'
             4258  LOAD_FAST                'i'
             4260  BINARY_SUBSCR    
             4262  INPLACE_ADD      
             4264  STORE_FAST               'strHH'
             4266  JUMP_FORWARD       4300  'to 4300'
           4268_0  COME_FROM          4250  '4250'

 L. 729      4268  LOAD_FAST                'word'
             4270  LOAD_FAST                'i'
             4272  BINARY_SUBSCR    
             4274  LOAD_STR                 ':'
             4276  COMPARE_OP               ==
         4278_4280  POP_JUMP_IF_FALSE  4288  'to 4288'

 L. 730      4282  LOAD_CONST               1
             4284  STORE_FAST               'stage'
             4286  JUMP_FORWARD       4300  'to 4300'
           4288_0  COME_FROM          4278  '4278'

 L. 732      4288  LOAD_CONST               2
             4290  STORE_FAST               'stage'

 L. 733      4292  LOAD_FAST                'i'
             4294  LOAD_CONST               1
             4296  INPLACE_SUBTRACT 
             4298  STORE_FAST               'i'
           4300_0  COME_FROM          4286  '4286'
           4300_1  COME_FROM          4266  '4266'
             4300  JUMP_BACK          4226  'to 4226'
           4302_0  COME_FROM          4236  '4236'

 L. 734      4302  LOAD_FAST                'stage'
             4304  LOAD_CONST               1
             4306  COMPARE_OP               ==
         4308_4310  POP_JUMP_IF_FALSE  4354  'to 4354'

 L. 735      4312  LOAD_FAST                'word'
             4314  LOAD_FAST                'i'
             4316  BINARY_SUBSCR    
             4318  LOAD_METHOD              isdigit
             4320  CALL_METHOD_0         0  '0 positional arguments'
         4322_4324  POP_JUMP_IF_FALSE  4340  'to 4340'

 L. 736      4326  LOAD_FAST                'strMM'
             4328  LOAD_FAST                'word'
             4330  LOAD_FAST                'i'
             4332  BINARY_SUBSCR    
             4334  INPLACE_ADD      
             4336  STORE_FAST               'strMM'
             4338  JUMP_FORWARD       4352  'to 4352'
           4340_0  COME_FROM          4322  '4322'

 L. 738      4340  LOAD_CONST               2
             4342  STORE_FAST               'stage'

 L. 739      4344  LOAD_FAST                'i'
             4346  LOAD_CONST               1
             4348  INPLACE_SUBTRACT 
             4350  STORE_FAST               'i'
           4352_0  COME_FROM          4338  '4338'
             4352  JUMP_BACK          4226  'to 4226'
           4354_0  COME_FROM          4308  '4308'

 L. 740      4354  LOAD_FAST                'stage'
             4356  LOAD_CONST               2
             4358  COMPARE_OP               ==
         4360_4362  POP_JUMP_IF_FALSE  4226  'to 4226'

 L. 741      4364  LOAD_FAST                'word'
             4366  LOAD_FAST                'i'
             4368  LOAD_CONST               None
             4370  BUILD_SLICE_2         2 
             4372  BINARY_SUBSCR    
             4374  LOAD_METHOD              replace
             4376  LOAD_STR                 '.'
             4378  LOAD_STR                 ''
             4380  CALL_METHOD_2         2  '2 positional arguments'
             4382  STORE_FAST               'remainder'

 L. 742      4384  BREAK_LOOP       
         4386_4388  JUMP_BACK          4226  'to 4226'
             4390  POP_BLOCK        
           4392_0  COME_FROM_LOOP     4216  '4216'

 L. 743      4392  LOAD_FAST                'remainder'
             4394  LOAD_STR                 ''
             4396  COMPARE_OP               ==
         4398_4400  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 744      4402  LOAD_FAST                'wordNext'
             4404  LOAD_METHOD              replace
             4406  LOAD_STR                 '.'
             4408  LOAD_STR                 ''
             4410  CALL_METHOD_2         2  '2 positional arguments'
             4412  STORE_FAST               'nextWord'

 L. 745      4414  LOAD_FAST                'nextWord'
             4416  LOAD_STR                 'am'
             4418  COMPARE_OP               ==
         4420_4422  POP_JUMP_IF_TRUE   4434  'to 4434'
             4424  LOAD_FAST                'nextWord'
             4426  LOAD_STR                 'pm'
             4428  COMPARE_OP               ==
         4430_4432  POP_JUMP_IF_FALSE  4450  'to 4450'
           4434_0  COME_FROM          4420  '4420'

 L. 746      4434  LOAD_FAST                'nextWord'
             4436  STORE_FAST               'remainder'

 L. 747      4438  LOAD_FAST                'used'
             4440  LOAD_CONST               1
             4442  INPLACE_ADD      
             4444  STORE_FAST               'used'
         4446_4448  JUMP_ABSOLUTE      5574  'to 5574'
           4450_0  COME_FROM          4430  '4430'

 L. 748      4450  LOAD_FAST                'wordNext'
             4452  LOAD_STR                 'manha'
             4454  COMPARE_OP               ==
         4456_4458  POP_JUMP_IF_FALSE  4474  'to 4474'

 L. 749      4460  LOAD_STR                 'am'
             4462  STORE_FAST               'remainder'

 L. 750      4464  LOAD_FAST                'used'
             4466  LOAD_CONST               1
             4468  INPLACE_ADD      
             4470  STORE_FAST               'used'
             4472  JUMP_FORWARD       5574  'to 5574'
           4474_0  COME_FROM          4456  '4456'

 L. 751      4474  LOAD_FAST                'wordNext'
             4476  LOAD_STR                 'tarde'
             4478  COMPARE_OP               ==
         4480_4482  POP_JUMP_IF_FALSE  4498  'to 4498'

 L. 752      4484  LOAD_STR                 'pm'
             4486  STORE_FAST               'remainder'

 L. 753      4488  LOAD_FAST                'used'
             4490  LOAD_CONST               1
             4492  INPLACE_ADD      
             4494  STORE_FAST               'used'
             4496  JUMP_FORWARD       5574  'to 5574'
           4498_0  COME_FROM          4480  '4480'

 L. 754      4498  LOAD_FAST                'wordNext'
             4500  LOAD_STR                 'noite'
             4502  COMPARE_OP               ==
         4504_4506  POP_JUMP_IF_FALSE  4564  'to 4564'

 L. 755      4508  LOAD_CONST               0
             4510  LOAD_GLOBAL              int
             4512  LOAD_FAST                'word'
             4514  LOAD_CONST               0
             4516  BINARY_SUBSCR    
             4518  CALL_FUNCTION_1       1  '1 positional argument'
             4520  DUP_TOP          
             4522  ROT_THREE        
             4524  COMPARE_OP               <
         4526_4528  POP_JUMP_IF_FALSE  4540  'to 4540'
             4530  LOAD_CONST               6
             4532  COMPARE_OP               <
         4534_4536  POP_JUMP_IF_FALSE  4550  'to 4550'
             4538  JUMP_FORWARD       4544  'to 4544'
           4540_0  COME_FROM          4526  '4526'
             4540  POP_TOP          
             4542  JUMP_FORWARD       4550  'to 4550'
           4544_0  COME_FROM          4538  '4538'

 L. 756      4544  LOAD_STR                 'am'
             4546  STORE_FAST               'remainder'
             4548  JUMP_FORWARD       4554  'to 4554'
           4550_0  COME_FROM          4542  '4542'
           4550_1  COME_FROM          4534  '4534'

 L. 758      4550  LOAD_STR                 'pm'
             4552  STORE_FAST               'remainder'
           4554_0  COME_FROM          4548  '4548'

 L. 759      4554  LOAD_FAST                'used'
             4556  LOAD_CONST               1
             4558  INPLACE_ADD      
             4560  STORE_FAST               'used'
             4562  JUMP_FORWARD       5574  'to 5574'
           4564_0  COME_FROM          4504  '4504'

 L. 760      4564  LOAD_FAST                'wordNext'
             4566  LOAD_FAST                'thises'
             4568  COMPARE_OP               in
         4570_4572  POP_JUMP_IF_FALSE  4594  'to 4594'
             4574  LOAD_FAST                'wordNextNext'
             4576  LOAD_STR                 'manha'
             4578  COMPARE_OP               ==
         4580_4582  POP_JUMP_IF_FALSE  4594  'to 4594'

 L. 761      4584  LOAD_STR                 'am'
             4586  STORE_FAST               'remainder'

 L. 762      4588  LOAD_CONST               2
             4590  STORE_FAST               'used'
             4592  JUMP_FORWARD       5574  'to 5574'
           4594_0  COME_FROM          4580  '4580'
           4594_1  COME_FROM          4570  '4570'

 L. 763      4594  LOAD_FAST                'wordNext'
             4596  LOAD_FAST                'thises'
             4598  COMPARE_OP               in
         4600_4602  POP_JUMP_IF_FALSE  4624  'to 4624'
             4604  LOAD_FAST                'wordNextNext'
             4606  LOAD_STR                 'tarde'
             4608  COMPARE_OP               ==
         4610_4612  POP_JUMP_IF_FALSE  4624  'to 4624'

 L. 764      4614  LOAD_STR                 'pm'
             4616  STORE_FAST               'remainder'

 L. 765      4618  LOAD_CONST               2
             4620  STORE_FAST               'used'
             4622  JUMP_FORWARD       5574  'to 5574'
           4624_0  COME_FROM          4610  '4610'
           4624_1  COME_FROM          4600  '4600'

 L. 766      4624  LOAD_FAST                'wordNext'
             4626  LOAD_FAST                'thises'
             4628  COMPARE_OP               in
         4630_4632  POP_JUMP_IF_FALSE  4654  'to 4654'
             4634  LOAD_FAST                'wordNextNext'
             4636  LOAD_STR                 'noite'
             4638  COMPARE_OP               ==
         4640_4642  POP_JUMP_IF_FALSE  4654  'to 4654'

 L. 767      4644  LOAD_STR                 'pm'
             4646  STORE_FAST               'remainder'

 L. 768      4648  LOAD_CONST               2
             4650  STORE_FAST               'used'
             4652  JUMP_FORWARD       5574  'to 5574'
           4654_0  COME_FROM          4640  '4640'
           4654_1  COME_FROM          4630  '4630'

 L. 770      4654  LOAD_FAST                'timeQualifier'
             4656  LOAD_STR                 ''
             4658  COMPARE_OP               !=
         4660_4662  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 771      4664  LOAD_CONST               True
             4666  STORE_FAST               'military'

 L. 772      4668  LOAD_FAST                'strHH'
             4670  LOAD_CONST               12
             4672  COMPARE_OP               <=
         4674_4676  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 773      4678  LOAD_FAST                'timeQualifier'
             4680  LOAD_STR                 'manha'
             4682  COMPARE_OP               ==
         4684_4686  POP_JUMP_IF_TRUE   4698  'to 4698'

 L. 774      4688  LOAD_FAST                'timeQualifier'
             4690  LOAD_STR                 'tarde'
             4692  COMPARE_OP               ==
         4694_4696  POP_JUMP_IF_FALSE  5574  'to 5574'
           4698_0  COME_FROM          4684  '4684'

 L. 775      4698  LOAD_FAST                'strHH'
             4700  LOAD_CONST               12
             4702  INPLACE_ADD      
             4704  STORE_FAST               'strHH'
         4706_4708  JUMP_FORWARD       5574  'to 5574'
           4710_0  COME_FROM          4200  '4200'

 L. 780      4710  LOAD_GLOBAL              len
             4712  LOAD_FAST                'word'
             4714  CALL_FUNCTION_1       1  '1 positional argument'
             4716  STORE_FAST               'length'

 L. 781      4718  LOAD_STR                 ''
             4720  STORE_FAST               'strNum'

 L. 782      4722  LOAD_STR                 ''
             4724  STORE_FAST               'remainder'

 L. 783      4726  SETUP_LOOP         4786  'to 4786'
             4728  LOAD_GLOBAL              range
             4730  LOAD_FAST                'length'
             4732  CALL_FUNCTION_1       1  '1 positional argument'
             4734  GET_ITER         
             4736  FOR_ITER           4784  'to 4784'
             4738  STORE_FAST               'i'

 L. 784      4740  LOAD_FAST                'word'
             4742  LOAD_FAST                'i'
             4744  BINARY_SUBSCR    
             4746  LOAD_METHOD              isdigit
             4748  CALL_METHOD_0         0  '0 positional arguments'
         4750_4752  POP_JUMP_IF_FALSE  4768  'to 4768'

 L. 785      4754  LOAD_FAST                'strNum'
             4756  LOAD_FAST                'word'
             4758  LOAD_FAST                'i'
             4760  BINARY_SUBSCR    
             4762  INPLACE_ADD      
             4764  STORE_FAST               'strNum'
             4766  JUMP_BACK          4736  'to 4736'
           4768_0  COME_FROM          4750  '4750'

 L. 787      4768  LOAD_FAST                'remainder'
             4770  LOAD_FAST                'word'
             4772  LOAD_FAST                'i'
             4774  BINARY_SUBSCR    
             4776  INPLACE_ADD      
             4778  STORE_FAST               'remainder'
         4780_4782  JUMP_BACK          4736  'to 4736'
             4784  POP_BLOCK        
           4786_0  COME_FROM_LOOP     4726  '4726'

 L. 789      4786  LOAD_FAST                'remainder'
             4788  LOAD_STR                 ''
             4790  COMPARE_OP               ==
         4792_4794  POP_JUMP_IF_FALSE  4816  'to 4816'

 L. 790      4796  LOAD_FAST                'wordNext'
             4798  LOAD_METHOD              replace
             4800  LOAD_STR                 '.'
             4802  LOAD_STR                 ''
             4804  CALL_METHOD_2         2  '2 positional arguments'
             4806  LOAD_METHOD              lstrip
             4808  CALL_METHOD_0         0  '0 positional arguments'
             4810  LOAD_METHOD              rstrip
             4812  CALL_METHOD_0         0  '0 positional arguments'
             4814  STORE_FAST               'remainder'
           4816_0  COME_FROM          4792  '4792'

 L. 793      4816  LOAD_FAST                'remainder'
             4818  LOAD_STR                 'pm'
             4820  COMPARE_OP               ==
         4822_4824  POP_JUMP_IF_TRUE   4856  'to 4856'

 L. 794      4826  LOAD_FAST                'wordNext'
             4828  LOAD_STR                 'pm'
             4830  COMPARE_OP               ==
         4832_4834  POP_JUMP_IF_TRUE   4856  'to 4856'

 L. 795      4836  LOAD_FAST                'remainder'
             4838  LOAD_STR                 'p.m.'
             4840  COMPARE_OP               ==
         4842_4844  POP_JUMP_IF_TRUE   4856  'to 4856'

 L. 796      4846  LOAD_FAST                'wordNext'
             4848  LOAD_STR                 'p.m.'
             4850  COMPARE_OP               ==
         4852_4854  POP_JUMP_IF_FALSE  4872  'to 4872'
           4856_0  COME_FROM          4842  '4842'
           4856_1  COME_FROM          4832  '4832'
           4856_2  COME_FROM          4822  '4822'

 L. 797      4856  LOAD_FAST                'strNum'
             4858  STORE_FAST               'strHH'

 L. 798      4860  LOAD_STR                 'pm'
             4862  STORE_FAST               'remainder'

 L. 799      4864  LOAD_CONST               1
             4866  STORE_FAST               'used'
         4868_4870  JUMP_FORWARD       5574  'to 5574'
           4872_0  COME_FROM          4852  '4852'

 L. 801      4872  LOAD_FAST                'remainder'
             4874  LOAD_STR                 'am'
             4876  COMPARE_OP               ==
         4878_4880  POP_JUMP_IF_TRUE   4912  'to 4912'

 L. 802      4882  LOAD_FAST                'wordNext'
             4884  LOAD_STR                 'am'
             4886  COMPARE_OP               ==
         4888_4890  POP_JUMP_IF_TRUE   4912  'to 4912'

 L. 803      4892  LOAD_FAST                'remainder'
             4894  LOAD_STR                 'a.m.'
             4896  COMPARE_OP               ==
         4898_4900  POP_JUMP_IF_TRUE   4912  'to 4912'

 L. 804      4902  LOAD_FAST                'wordNext'
             4904  LOAD_STR                 'a.m.'
             4906  COMPARE_OP               ==
         4908_4910  POP_JUMP_IF_FALSE  4928  'to 4928'
           4912_0  COME_FROM          4898  '4898'
           4912_1  COME_FROM          4888  '4888'
           4912_2  COME_FROM          4878  '4878'

 L. 805      4912  LOAD_FAST                'strNum'
             4914  STORE_FAST               'strHH'

 L. 806      4916  LOAD_STR                 'am'
             4918  STORE_FAST               'remainder'

 L. 807      4920  LOAD_CONST               1
             4922  STORE_FAST               'used'
         4924_4926  JUMP_FORWARD       5574  'to 5574'
           4928_0  COME_FROM          4908  '4908'

 L. 809      4928  LOAD_FAST                'wordNext'
             4930  LOAD_STR                 'pm'
             4932  COMPARE_OP               ==
         4934_4936  POP_JUMP_IF_TRUE   4958  'to 4958'

 L. 810      4938  LOAD_FAST                'wordNext'
             4940  LOAD_STR                 'p.m.'
             4942  COMPARE_OP               ==
         4944_4946  POP_JUMP_IF_TRUE   4958  'to 4958'

 L. 811      4948  LOAD_FAST                'wordNext'
             4950  LOAD_STR                 'tarde'
             4952  COMPARE_OP               ==
         4954_4956  POP_JUMP_IF_FALSE  4974  'to 4974'
           4958_0  COME_FROM          4944  '4944'
           4958_1  COME_FROM          4934  '4934'

 L. 812      4958  LOAD_FAST                'strNum'
             4960  STORE_FAST               'strHH'

 L. 813      4962  LOAD_STR                 'pm'
             4964  STORE_FAST               'remainder'

 L. 814      4966  LOAD_CONST               1
             4968  STORE_FAST               'used'
         4970_4972  JUMP_FORWARD       5574  'to 5574'
           4974_0  COME_FROM          4954  '4954'

 L. 815      4974  LOAD_FAST                'wordNext'
             4976  LOAD_STR                 'am'
             4978  COMPARE_OP               ==
         4980_4982  POP_JUMP_IF_TRUE   5004  'to 5004'

 L. 816      4984  LOAD_FAST                'wordNext'
             4986  LOAD_STR                 'a.m.'
             4988  COMPARE_OP               ==
         4990_4992  POP_JUMP_IF_TRUE   5004  'to 5004'

 L. 817      4994  LOAD_FAST                'wordNext'
             4996  LOAD_STR                 'manha'
             4998  COMPARE_OP               ==
         5000_5002  POP_JUMP_IF_FALSE  5020  'to 5020'
           5004_0  COME_FROM          4990  '4990'
           5004_1  COME_FROM          4980  '4980'

 L. 818      5004  LOAD_FAST                'strNum'
             5006  STORE_FAST               'strHH'

 L. 819      5008  LOAD_STR                 'am'
             5010  STORE_FAST               'remainder'

 L. 820      5012  LOAD_CONST               1
             5014  STORE_FAST               'used'
         5016_5018  JUMP_FORWARD       5574  'to 5574'
           5020_0  COME_FROM          5000  '5000'

 L. 821      5020  LOAD_GLOBAL              int
             5022  LOAD_FAST                'word'
             5024  CALL_FUNCTION_1       1  '1 positional argument'
             5026  LOAD_CONST               100
             5028  COMPARE_OP               >
         5030_5032  POP_JUMP_IF_FALSE  5118  'to 5118'

 L. 823      5034  LOAD_FAST                'wordPrev'
             5036  LOAD_STR                 'o'
             5038  COMPARE_OP               ==
         5040_5042  POP_JUMP_IF_TRUE   5064  'to 5064'

 L. 824      5044  LOAD_FAST                'wordPrev'
             5046  LOAD_STR                 'oh'
             5048  COMPARE_OP               ==
         5050_5052  POP_JUMP_IF_TRUE   5064  'to 5064'

 L. 825      5054  LOAD_FAST                'wordPrev'
             5056  LOAD_STR                 'zero'
             5058  COMPARE_OP               ==
         5060_5062  POP_JUMP_IF_FALSE  5118  'to 5118'
           5064_0  COME_FROM          5050  '5050'
           5064_1  COME_FROM          5040  '5040'

 L. 828      5064  LOAD_GLOBAL              int
             5066  LOAD_FAST                'word'
             5068  CALL_FUNCTION_1       1  '1 positional argument'
             5070  LOAD_CONST               100
             5072  BINARY_TRUE_DIVIDE
             5074  STORE_FAST               'strHH'

 L. 829      5076  LOAD_GLOBAL              int
             5078  LOAD_FAST                'word'
             5080  CALL_FUNCTION_1       1  '1 positional argument'
             5082  LOAD_FAST                'strHH'
             5084  LOAD_CONST               100
             5086  BINARY_MULTIPLY  
             5088  BINARY_SUBTRACT  
             5090  STORE_FAST               'strMM'

 L. 830      5092  LOAD_CONST               True
             5094  STORE_FAST               'military'

 L. 831      5096  LOAD_FAST                'wordNext'
             5098  LOAD_STR                 'hora'
             5100  COMPARE_OP               ==
         5102_5104  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 832      5106  LOAD_FAST                'used'
             5108  LOAD_CONST               1
             5110  INPLACE_ADD      
             5112  STORE_FAST               'used'
         5114_5116  JUMP_FORWARD       5574  'to 5574'
           5118_0  COME_FROM          5060  '5060'
           5118_1  COME_FROM          5030  '5030'

 L. 834      5118  LOAD_FAST                'wordNext'
             5120  LOAD_STR                 'hora'
             5122  COMPARE_OP               ==
         5124_5126  POP_JUMP_IF_FALSE  5198  'to 5198'

 L. 835      5128  LOAD_FAST                'word'
             5130  LOAD_CONST               0
             5132  BINARY_SUBSCR    
             5134  LOAD_STR                 '0'
             5136  COMPARE_OP               !=
         5138_5140  POP_JUMP_IF_FALSE  5198  'to 5198'

 L. 837      5142  LOAD_GLOBAL              int
             5144  LOAD_FAST                'word'
             5146  CALL_FUNCTION_1       1  '1 positional argument'
             5148  LOAD_CONST               100
             5150  COMPARE_OP               <
         5152_5154  POP_JUMP_IF_FALSE  5198  'to 5198'

 L. 838      5156  LOAD_GLOBAL              int
             5158  LOAD_FAST                'word'
             5160  CALL_FUNCTION_1       1  '1 positional argument'
             5162  LOAD_CONST               2400
             5164  COMPARE_OP               >
         5166_5168  POP_JUMP_IF_FALSE  5198  'to 5198'

 L. 842      5170  LOAD_GLOBAL              int
             5172  LOAD_FAST                'word'
             5174  CALL_FUNCTION_1       1  '1 positional argument'
             5176  STORE_DEREF              'hrOffset'

 L. 843      5178  LOAD_CONST               2
             5180  STORE_FAST               'used'

 L. 844      5182  LOAD_CONST               False
             5184  STORE_FAST               'isTime'

 L. 845      5186  LOAD_CONST               -1
             5188  STORE_DEREF              'hrAbs'

 L. 846      5190  LOAD_CONST               -1
             5192  STORE_DEREF              'minAbs'
         5194_5196  JUMP_FORWARD       5574  'to 5574'
           5198_0  COME_FROM          5166  '5166'
           5198_1  COME_FROM          5152  '5152'
           5198_2  COME_FROM          5138  '5138'
           5198_3  COME_FROM          5124  '5124'

 L. 848      5198  LOAD_FAST                'wordNext'
             5200  LOAD_STR                 'minuto'
             5202  COMPARE_OP               ==
         5204_5206  POP_JUMP_IF_FALSE  5236  'to 5236'

 L. 850      5208  LOAD_GLOBAL              int
             5210  LOAD_FAST                'word'
             5212  CALL_FUNCTION_1       1  '1 positional argument'
             5214  STORE_DEREF              'minOffset'

 L. 851      5216  LOAD_CONST               2
             5218  STORE_FAST               'used'

 L. 852      5220  LOAD_CONST               False
             5222  STORE_FAST               'isTime'

 L. 853      5224  LOAD_CONST               -1
             5226  STORE_DEREF              'hrAbs'

 L. 854      5228  LOAD_CONST               -1
             5230  STORE_DEREF              'minAbs'
         5232_5234  JUMP_FORWARD       5574  'to 5574'
           5236_0  COME_FROM          5204  '5204'

 L. 855      5236  LOAD_FAST                'wordNext'
             5238  LOAD_STR                 'segundo'
             5240  COMPARE_OP               ==
         5242_5244  POP_JUMP_IF_FALSE  5274  'to 5274'

 L. 857      5246  LOAD_GLOBAL              int
             5248  LOAD_FAST                'word'
             5250  CALL_FUNCTION_1       1  '1 positional argument'
             5252  STORE_DEREF              'secOffset'

 L. 858      5254  LOAD_CONST               2
             5256  STORE_FAST               'used'

 L. 859      5258  LOAD_CONST               False
             5260  STORE_FAST               'isTime'

 L. 860      5262  LOAD_CONST               -1
             5264  STORE_DEREF              'hrAbs'

 L. 861      5266  LOAD_CONST               -1
             5268  STORE_DEREF              'minAbs'
         5270_5272  JUMP_FORWARD       5574  'to 5574'
           5274_0  COME_FROM          5242  '5242'

 L. 862      5274  LOAD_GLOBAL              int
             5276  LOAD_FAST                'word'
             5278  CALL_FUNCTION_1       1  '1 positional argument'
             5280  LOAD_CONST               100
             5282  COMPARE_OP               >
         5284_5286  POP_JUMP_IF_FALSE  5340  'to 5340'

 L. 863      5288  LOAD_GLOBAL              int
             5290  LOAD_FAST                'word'
             5292  CALL_FUNCTION_1       1  '1 positional argument'
             5294  LOAD_CONST               100
             5296  BINARY_TRUE_DIVIDE
             5298  STORE_FAST               'strHH'

 L. 864      5300  LOAD_GLOBAL              int
             5302  LOAD_FAST                'word'
             5304  CALL_FUNCTION_1       1  '1 positional argument'
             5306  LOAD_FAST                'strHH'
             5308  LOAD_CONST               100
             5310  BINARY_MULTIPLY  
             5312  BINARY_SUBTRACT  
             5314  STORE_FAST               'strMM'

 L. 865      5316  LOAD_CONST               True
             5318  STORE_FAST               'military'

 L. 866      5320  LOAD_FAST                'wordNext'
             5322  LOAD_STR                 'hora'
             5324  COMPARE_OP               ==
         5326_5328  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 867      5330  LOAD_FAST                'used'
             5332  LOAD_CONST               1
             5334  INPLACE_ADD      
             5336  STORE_FAST               'used'
           5338_0  COME_FROM          4472  '4472'
             5338  JUMP_FORWARD       5574  'to 5574'
           5340_0  COME_FROM          5284  '5284'

 L. 869      5340  LOAD_FAST                'wordNext'
             5342  LOAD_STR                 ''
             5344  COMPARE_OP               ==
         5346_5348  POP_JUMP_IF_TRUE   5370  'to 5370'

 L. 870      5350  LOAD_FAST                'wordNext'
             5352  LOAD_STR                 'em'
             5354  COMPARE_OP               ==
         5356_5358  POP_JUMP_IF_FALSE  5516  'to 5516'
             5360  LOAD_FAST                'wordNextNext'
           5362_0  COME_FROM          4496  '4496'
             5362  LOAD_STR                 'ponto'
             5364  COMPARE_OP               ==
         5366_5368  POP_JUMP_IF_FALSE  5516  'to 5516'
           5370_0  COME_FROM          5346  '5346'

 L. 871      5370  LOAD_FAST                'word'
             5372  STORE_FAST               'strHH'

 L. 872      5374  LOAD_CONST               0
             5376  STORE_FAST               'strMM'

 L. 873      5378  LOAD_FAST                'wordNext'
             5380  LOAD_STR                 'em'
             5382  COMPARE_OP               ==
         5384_5386  POP_JUMP_IF_FALSE  5574  'to 5574'
             5388  LOAD_FAST                'wordNextNext'
             5390  LOAD_STR                 'ponto'
             5392  COMPARE_OP               ==
         5394_5396  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 874      5398  LOAD_FAST                'used'
             5400  LOAD_CONST               2
             5402  INPLACE_ADD      
             5404  STORE_FAST               'used'

 L. 875      5406  LOAD_FAST                'wordNextNextNext'
             5408  LOAD_STR                 'tarde'
             5410  COMPARE_OP               ==
         5412_5414  POP_JUMP_IF_FALSE  5430  'to 5430'

 L. 876      5416  LOAD_STR                 'pm'
             5418  STORE_FAST               'remainder'

 L. 877      5420  LOAD_FAST                'used'
             5422  LOAD_CONST               1
             5424  INPLACE_ADD      
             5426  STORE_FAST               'used'
           5428_0  COME_FROM          4562  '4562'
             5428  JUMP_FORWARD       5514  'to 5514'
           5430_0  COME_FROM          5412  '5412'

 L. 878      5430  LOAD_FAST                'wordNextNextNext'
             5432  LOAD_STR                 'manha'
             5434  COMPARE_OP               ==
         5436_5438  POP_JUMP_IF_FALSE  5454  'to 5454'

 L. 879      5440  LOAD_STR                 'am'
             5442  STORE_FAST               'remainder'

 L. 880      5444  LOAD_FAST                'used'
             5446  LOAD_CONST               1
             5448  INPLACE_ADD      
             5450  STORE_FAST               'used'
             5452  JUMP_FORWARD       5514  'to 5514'
           5454_0  COME_FROM          5436  '5436'

 L. 881      5454  LOAD_FAST                'wordNextNextNext'
             5456  LOAD_STR                 'noite'
           5458_0  COME_FROM          4592  '4592'
             5458  COMPARE_OP               ==
         5460_5462  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 882      5464  LOAD_CONST               0
             5466  LOAD_GLOBAL              int
             5468  LOAD_FAST                'strHH'
             5470  CALL_FUNCTION_1       1  '1 positional argument'
             5472  DUP_TOP          
             5474  ROT_THREE        
             5476  COMPARE_OP               >
         5478_5480  POP_JUMP_IF_FALSE  5492  'to 5492'
             5482  LOAD_CONST               6
             5484  COMPARE_OP               >
         5486_5488  POP_JUMP_IF_FALSE  5502  'to 5502'
             5490  JUMP_FORWARD       5496  'to 5496'
           5492_0  COME_FROM          5478  '5478'
             5492  POP_TOP          
             5494  JUMP_FORWARD       5502  'to 5502'
           5496_0  COME_FROM          5490  '5490'

 L. 883      5496  LOAD_STR                 'am'
             5498  STORE_FAST               'remainder'
             5500  JUMP_FORWARD       5506  'to 5506'
           5502_0  COME_FROM          5494  '5494'
           5502_1  COME_FROM          5486  '5486'

 L. 885      5502  LOAD_STR                 'pm'
             5504  STORE_FAST               'remainder'
           5506_0  COME_FROM          5500  '5500'

 L. 886      5506  LOAD_FAST                'used'
             5508  LOAD_CONST               1
             5510  INPLACE_ADD      
             5512  STORE_FAST               'used'
           5514_0  COME_FROM          5452  '5452'
           5514_1  COME_FROM          5428  '5428'
             5514  JUMP_FORWARD       5574  'to 5574'
           5516_0  COME_FROM          5366  '5366'
           5516_1  COME_FROM          5356  '5356'

 L. 888      5516  LOAD_FAST                'wordNext'
           5518_0  COME_FROM          4652  '4652'
             5518  LOAD_CONST               0
             5520  BINARY_SUBSCR    
             5522  LOAD_METHOD              isdigit
             5524  CALL_METHOD_0         0  '0 positional arguments'
         5526_5528  POP_JUMP_IF_FALSE  5570  'to 5570'

 L. 889      5530  LOAD_FAST                'word'
             5532  STORE_FAST               'strHH'

 L. 890      5534  LOAD_FAST                'wordNext'
             5536  STORE_FAST               'strMM'

 L. 891      5538  LOAD_CONST               True
             5540  STORE_FAST               'military'

 L. 892      5542  LOAD_FAST                'used'
             5544  LOAD_CONST               1
             5546  INPLACE_ADD      
             5548  STORE_FAST               'used'

 L. 893      5550  LOAD_FAST                'wordNextNext'
             5552  LOAD_STR                 'hora'
             5554  COMPARE_OP               ==
         5556_5558  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 894      5560  LOAD_FAST                'used'
             5562  LOAD_CONST               1
             5564  INPLACE_ADD      
             5566  STORE_FAST               'used'
             5568  JUMP_FORWARD       5574  'to 5574'
           5570_0  COME_FROM          5526  '5526'

 L. 896      5570  LOAD_CONST               False
             5572  STORE_FAST               'isTime'
           5574_0  COME_FROM          5568  '5568'
           5574_1  COME_FROM          5556  '5556'
           5574_2  COME_FROM          5514  '5514'
           5574_3  COME_FROM          5460  '5460'
           5574_4  COME_FROM          5394  '5394'
           5574_5  COME_FROM          5384  '5384'
           5574_6  COME_FROM          5338  '5338'
           5574_7  COME_FROM          5326  '5326'
           5574_8  COME_FROM          5270  '5270'
           5574_9  COME_FROM          5232  '5232'
          5574_10  COME_FROM          5194  '5194'
          5574_11  COME_FROM          5114  '5114'
          5574_12  COME_FROM          5102  '5102'
          5574_13  COME_FROM          5016  '5016'
          5574_14  COME_FROM          4970  '4970'
          5574_15  COME_FROM          4924  '4924'
          5574_16  COME_FROM          4868  '4868'
          5574_17  COME_FROM          4706  '4706'
          5574_18  COME_FROM          4694  '4694'
          5574_19  COME_FROM          4674  '4674'
          5574_20  COME_FROM          4660  '4660'
          5574_21  COME_FROM          4398  '4398'

 L. 898      5574  LOAD_FAST                'strHH'
         5576_5578  POP_JUMP_IF_FALSE  5588  'to 5588'
             5580  LOAD_GLOBAL              int
             5582  LOAD_FAST                'strHH'
             5584  CALL_FUNCTION_1       1  '1 positional argument'
             5586  JUMP_FORWARD       5590  'to 5590'
           5588_0  COME_FROM          5576  '5576'
             5588  LOAD_CONST               0
           5590_0  COME_FROM          5586  '5586'
             5590  STORE_FAST               'strHH'

 L. 899      5592  LOAD_FAST                'strMM'
         5594_5596  POP_JUMP_IF_FALSE  5606  'to 5606'
             5598  LOAD_GLOBAL              int
             5600  LOAD_FAST                'strMM'
             5602  CALL_FUNCTION_1       1  '1 positional argument'
             5604  JUMP_FORWARD       5608  'to 5608'
           5606_0  COME_FROM          5594  '5594'
             5606  LOAD_CONST               0
           5608_0  COME_FROM          5604  '5604'
             5608  STORE_FAST               'strMM'

 L. 900      5610  LOAD_FAST                'remainder'
             5612  LOAD_STR                 'pm'
             5614  COMPARE_OP               ==
         5616_5618  POP_JUMP_IF_FALSE  5656  'to 5656'

 L. 901      5620  LOAD_CONST               0
             5622  LOAD_FAST                'strHH'
             5624  DUP_TOP          
             5626  ROT_THREE        
             5628  COMPARE_OP               <
         5630_5632  POP_JUMP_IF_FALSE  5644  'to 5644'
             5634  LOAD_CONST               12
             5636  COMPARE_OP               <
         5638_5640  POP_JUMP_IF_FALSE  5656  'to 5656'
             5642  JUMP_FORWARD       5648  'to 5648'
           5644_0  COME_FROM          5630  '5630'
             5644  POP_TOP          
             5646  JUMP_FORWARD       5656  'to 5656'
           5648_0  COME_FROM          5642  '5642'
             5648  LOAD_FAST                'strHH'
             5650  LOAD_CONST               12
             5652  BINARY_ADD       
             5654  JUMP_FORWARD       5658  'to 5658'
           5656_0  COME_FROM          5646  '5646'
           5656_1  COME_FROM          5638  '5638'
           5656_2  COME_FROM          5616  '5616'
             5656  LOAD_FAST                'strHH'
           5658_0  COME_FROM          5654  '5654'
             5658  STORE_FAST               'strHH'

 L. 902      5660  LOAD_FAST                'remainder'
             5662  LOAD_STR                 'am'
             5664  COMPARE_OP               ==
         5666_5668  POP_JUMP_IF_FALSE  5706  'to 5706'

 L. 903      5670  LOAD_CONST               0
             5672  LOAD_FAST                'strHH'
             5674  DUP_TOP          
             5676  ROT_THREE        
             5678  COMPARE_OP               <
         5680_5682  POP_JUMP_IF_FALSE  5694  'to 5694'
             5684  LOAD_CONST               12
             5686  COMPARE_OP               >=
         5688_5690  POP_JUMP_IF_FALSE  5706  'to 5706'
             5692  JUMP_FORWARD       5698  'to 5698'
           5694_0  COME_FROM          5680  '5680'
             5694  POP_TOP          
             5696  JUMP_FORWARD       5706  'to 5706'
           5698_0  COME_FROM          5692  '5692'
             5698  LOAD_FAST                'strHH'
             5700  LOAD_CONST               12
             5702  BINARY_SUBTRACT  
             5704  JUMP_FORWARD       5708  'to 5708'
           5706_0  COME_FROM          5696  '5696'
           5706_1  COME_FROM          5688  '5688'
           5706_2  COME_FROM          5666  '5666'
             5706  LOAD_FAST                'strHH'
           5708_0  COME_FROM          5704  '5704'
             5708  STORE_FAST               'strHH'

 L. 904      5710  LOAD_FAST                'strHH'
             5712  LOAD_CONST               24
             5714  COMPARE_OP               >
         5716_5718  POP_JUMP_IF_TRUE   5730  'to 5730'
             5720  LOAD_FAST                'strMM'
             5722  LOAD_CONST               59
             5724  COMPARE_OP               >
         5726_5728  POP_JUMP_IF_FALSE  5738  'to 5738'
           5730_0  COME_FROM          5716  '5716'

 L. 905      5730  LOAD_CONST               False
             5732  STORE_FAST               'isTime'

 L. 906      5734  LOAD_CONST               0
             5736  STORE_FAST               'used'
           5738_0  COME_FROM          5726  '5726'

 L. 907      5738  LOAD_FAST                'isTime'
         5740_5742  POP_JUMP_IF_FALSE  5768  'to 5768'

 L. 908      5744  LOAD_FAST                'strHH'
             5746  LOAD_CONST               1
             5748  BINARY_MULTIPLY  
             5750  STORE_DEREF              'hrAbs'

 L. 909      5752  LOAD_FAST                'strMM'
             5754  LOAD_CONST               1
             5756  BINARY_MULTIPLY  
             5758  STORE_DEREF              'minAbs'

 L. 910      5760  LOAD_FAST                'used'
             5762  LOAD_CONST               1
             5764  INPLACE_ADD      
             5766  STORE_FAST               'used'
           5768_0  COME_FROM          5740  '5740'
           5768_1  COME_FROM          4174  '4174'
           5768_2  COME_FROM          4160  '4160'
           5768_3  COME_FROM          3972  '3972'
           5768_4  COME_FROM          3940  '3940'
           5768_5  COME_FROM          3898  '3898'
           5768_6  COME_FROM          3856  '3856'
           5768_7  COME_FROM          3814  '3814'
           5768_8  COME_FROM          3772  '3772'
           5768_9  COME_FROM          3730  '3730'
          5768_10  COME_FROM          3698  '3698'
          5768_11  COME_FROM          3666  '3666'
          5768_12  COME_FROM          3630  '3630'

 L. 912      5768  LOAD_FAST                'used'
             5770  LOAD_CONST               0
             5772  COMPARE_OP               >
         5774_5776  POP_JUMP_IF_FALSE  3416  'to 3416'

 L. 914      5778  SETUP_LOOP         5810  'to 5810'
             5780  LOAD_GLOBAL              range
             5782  LOAD_FAST                'used'
             5784  CALL_FUNCTION_1       1  '1 positional argument'
             5786  GET_ITER         
             5788  FOR_ITER           5808  'to 5808'
             5790  STORE_FAST               'i'

 L. 915      5792  LOAD_STR                 ''
             5794  LOAD_FAST                'words'
             5796  LOAD_FAST                'idx'
             5798  LOAD_FAST                'i'
             5800  BINARY_ADD       
             5802  STORE_SUBSCR     
         5804_5806  JUMP_BACK          5788  'to 5788'
             5808  POP_BLOCK        
           5810_0  COME_FROM_LOOP     5778  '5778'

 L. 917      5810  LOAD_FAST                'wordPrev'
             5812  LOAD_STR                 'em'
             5814  COMPARE_OP               ==
         5816_5818  POP_JUMP_IF_TRUE   5830  'to 5830'
             5820  LOAD_FAST                'wordPrev'
             5822  LOAD_STR                 'ponto'
             5824  COMPARE_OP               ==
         5826_5828  POP_JUMP_IF_FALSE  5844  'to 5844'
           5830_0  COME_FROM          5816  '5816'

 L. 918      5830  LOAD_STR                 ''
             5832  LOAD_FAST                'words'
             5834  LOAD_FAST                'words'
             5836  LOAD_METHOD              index
             5838  LOAD_FAST                'wordPrev'
             5840  CALL_METHOD_1         1  '1 positional argument'
             5842  STORE_SUBSCR     
           5844_0  COME_FROM          5826  '5826'

 L. 920      5844  LOAD_FAST                'idx'
             5846  LOAD_CONST               0
             5848  COMPARE_OP               >
         5850_5852  POP_JUMP_IF_FALSE  5876  'to 5876'
             5854  LOAD_FAST                'wordPrev'
             5856  LOAD_FAST                'time_indicators'
             5858  COMPARE_OP               in
         5860_5862  POP_JUMP_IF_FALSE  5876  'to 5876'

 L. 921      5864  LOAD_STR                 ''
             5866  LOAD_FAST                'words'
             5868  LOAD_FAST                'idx'
             5870  LOAD_CONST               1
             5872  BINARY_SUBTRACT  
             5874  STORE_SUBSCR     
           5876_0  COME_FROM          5860  '5860'
           5876_1  COME_FROM          5850  '5850'

 L. 922      5876  LOAD_FAST                'idx'
             5878  LOAD_CONST               1
             5880  COMPARE_OP               >
         5882_5884  POP_JUMP_IF_FALSE  5908  'to 5908'
             5886  LOAD_FAST                'wordPrevPrev'
             5888  LOAD_FAST                'time_indicators'
             5890  COMPARE_OP               in
         5892_5894  POP_JUMP_IF_FALSE  5908  'to 5908'

 L. 923      5896  LOAD_STR                 ''
             5898  LOAD_FAST                'words'
             5900  LOAD_FAST                'idx'
             5902  LOAD_CONST               2
             5904  BINARY_SUBTRACT  
             5906  STORE_SUBSCR     
           5908_0  COME_FROM          5892  '5892'
           5908_1  COME_FROM          5882  '5882'

 L. 925      5908  LOAD_FAST                'idx'
             5910  LOAD_FAST                'used'
             5912  LOAD_CONST               1
             5914  BINARY_SUBTRACT  
             5916  INPLACE_ADD      
             5918  STORE_FAST               'idx'

 L. 926      5920  LOAD_CONST               True
             5922  STORE_DEREF              'found'
         5924_5926  JUMP_BACK          3416  'to 3416'
             5928  POP_BLOCK        
           5930_0  COME_FROM_LOOP     3404  '3404'

 L. 929      5930  LOAD_FAST                'date_found'
         5932_5934  POP_JUMP_IF_TRUE   5940  'to 5940'

 L. 930      5936  LOAD_CONST               None
             5938  RETURN_VALUE     
           5940_0  COME_FROM          5932  '5932'

 L. 932      5940  LOAD_DEREF               'dayOffset'
             5942  LOAD_CONST               False
             5944  COMPARE_OP               is
         5946_5948  POP_JUMP_IF_FALSE  5954  'to 5954'

 L. 933      5950  LOAD_CONST               0
             5952  STORE_DEREF              'dayOffset'
           5954_0  COME_FROM          5946  '5946'

 L. 937      5954  LOAD_FAST                'dateNow'
             5956  STORE_FAST               'extractedDate'

 L. 938      5958  LOAD_FAST                'extractedDate'
             5960  LOAD_ATTR                replace
             5962  LOAD_CONST               0

 L. 939      5964  LOAD_CONST               0

 L. 940      5966  LOAD_CONST               0

 L. 941      5968  LOAD_CONST               0
             5970  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             5972  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5974  STORE_FAST               'extractedDate'

 L. 942      5976  LOAD_DEREF               'datestr'
             5978  LOAD_STR                 ''
             5980  COMPARE_OP               !=
         5982_5984  POP_JUMP_IF_FALSE  6298  'to 6298'

 L. 943      5986  LOAD_STR                 'january'
             5988  LOAD_STR                 'february'
             5990  LOAD_STR                 'march'
             5992  LOAD_STR                 'april'
             5994  LOAD_STR                 'may'
             5996  LOAD_STR                 'june'

 L. 944      5998  LOAD_STR                 'july'
             6000  LOAD_STR                 'august'
             6002  LOAD_STR                 'september'
             6004  LOAD_STR                 'october'
             6006  LOAD_STR                 'november'

 L. 945      6008  LOAD_STR                 'december'
             6010  BUILD_LIST_12        12 
             6012  STORE_FAST               'en_months'

 L. 946      6014  LOAD_STR                 'jan'
             6016  LOAD_STR                 'feb'
             6018  LOAD_STR                 'mar'
             6020  LOAD_STR                 'apr'
             6022  LOAD_STR                 'may'
             6024  LOAD_STR                 'june'
             6026  LOAD_STR                 'july'

 L. 947      6028  LOAD_STR                 'aug'

 L. 948      6030  LOAD_STR                 'sept'
             6032  LOAD_STR                 'oct'
             6034  LOAD_STR                 'nov'
             6036  LOAD_STR                 'dec'
             6038  BUILD_LIST_12        12 
             6040  STORE_FAST               'en_monthsShort'

 L. 949      6042  SETUP_LOOP         6082  'to 6082'
             6044  LOAD_GLOBAL              enumerate
             6046  LOAD_FAST                'en_months'
             6048  CALL_FUNCTION_1       1  '1 positional argument'
             6050  GET_ITER         
             6052  FOR_ITER           6080  'to 6080'
             6054  UNPACK_SEQUENCE_2     2 
             6056  STORE_FAST               'idx'
             6058  STORE_FAST               'en_month'

 L. 950      6060  LOAD_DEREF               'datestr'
             6062  LOAD_METHOD              replace
             6064  LOAD_FAST                'months'
             6066  LOAD_FAST                'idx'
             6068  BINARY_SUBSCR    
             6070  LOAD_FAST                'en_month'
             6072  CALL_METHOD_2         2  '2 positional arguments'
             6074  STORE_DEREF              'datestr'
         6076_6078  JUMP_BACK          6052  'to 6052'
             6080  POP_BLOCK        
           6082_0  COME_FROM_LOOP     6042  '6042'

 L. 951      6082  SETUP_LOOP         6122  'to 6122'
             6084  LOAD_GLOBAL              enumerate
             6086  LOAD_FAST                'en_monthsShort'
             6088  CALL_FUNCTION_1       1  '1 positional argument'
             6090  GET_ITER         
             6092  FOR_ITER           6120  'to 6120'
             6094  UNPACK_SEQUENCE_2     2 
             6096  STORE_FAST               'idx'
             6098  STORE_FAST               'en_month'

 L. 952      6100  LOAD_DEREF               'datestr'
             6102  LOAD_METHOD              replace
             6104  LOAD_FAST                'monthsShort'
             6106  LOAD_FAST                'idx'
             6108  BINARY_SUBSCR    
             6110  LOAD_FAST                'en_month'
             6112  CALL_METHOD_2         2  '2 positional arguments'
             6114  STORE_DEREF              'datestr'
         6116_6118  JUMP_BACK          6092  'to 6092'
             6120  POP_BLOCK        
           6122_0  COME_FROM_LOOP     6082  '6082'

 L. 954      6122  LOAD_GLOBAL              datetime
             6124  LOAD_METHOD              strptime
             6126  LOAD_DEREF               'datestr'
             6128  LOAD_STR                 '%B %d'
             6130  CALL_METHOD_2         2  '2 positional arguments'
             6132  STORE_FAST               'temp'

 L. 955      6134  LOAD_FAST                'hasYear'
         6136_6138  POP_JUMP_IF_TRUE   6252  'to 6252'

 L. 956      6140  LOAD_FAST                'temp'
             6142  LOAD_ATTR                replace
             6144  LOAD_FAST                'extractedDate'
             6146  LOAD_ATTR                year
             6148  LOAD_CONST               ('year',)
             6150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6152  STORE_FAST               'temp'

 L. 957      6154  LOAD_FAST                'extractedDate'
             6156  LOAD_FAST                'temp'
             6158  COMPARE_OP               <
         6160_6162  POP_JUMP_IF_FALSE  6206  'to 6206'

 L. 958      6164  LOAD_FAST                'extractedDate'
             6166  LOAD_ATTR                replace
             6168  LOAD_GLOBAL              int
             6170  LOAD_FAST                'currentYear'
             6172  CALL_FUNCTION_1       1  '1 positional argument'

 L. 959      6174  LOAD_GLOBAL              int

 L. 960      6176  LOAD_FAST                'temp'
             6178  LOAD_METHOD              strftime

 L. 961      6180  LOAD_STR                 '%m'
             6182  CALL_METHOD_1         1  '1 positional argument'
             6184  CALL_FUNCTION_1       1  '1 positional argument'

 L. 962      6186  LOAD_GLOBAL              int
             6188  LOAD_FAST                'temp'
             6190  LOAD_METHOD              strftime

 L. 963      6192  LOAD_STR                 '%d'
             6194  CALL_METHOD_1         1  '1 positional argument'
             6196  CALL_FUNCTION_1       1  '1 positional argument'
             6198  LOAD_CONST               ('year', 'month', 'day')
             6200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6202  STORE_FAST               'extractedDate'
             6204  JUMP_FORWARD       6250  'to 6250'
           6206_0  COME_FROM          6160  '6160'

 L. 965      6206  LOAD_FAST                'extractedDate'
             6208  LOAD_ATTR                replace

 L. 966      6210  LOAD_GLOBAL              int
             6212  LOAD_FAST                'currentYear'
             6214  CALL_FUNCTION_1       1  '1 positional argument'
             6216  LOAD_CONST               1
             6218  BINARY_ADD       

 L. 967      6220  LOAD_GLOBAL              int
             6222  LOAD_FAST                'temp'
             6224  LOAD_METHOD              strftime
             6226  LOAD_STR                 '%m'
             6228  CALL_METHOD_1         1  '1 positional argument'
             6230  CALL_FUNCTION_1       1  '1 positional argument'

 L. 968      6232  LOAD_GLOBAL              int
             6234  LOAD_FAST                'temp'
             6236  LOAD_METHOD              strftime
             6238  LOAD_STR                 '%d'
             6240  CALL_METHOD_1         1  '1 positional argument'
             6242  CALL_FUNCTION_1       1  '1 positional argument'
             6244  LOAD_CONST               ('year', 'month', 'day')
             6246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6248  STORE_FAST               'extractedDate'
           6250_0  COME_FROM          6204  '6204'
             6250  JUMP_FORWARD       6298  'to 6298'
           6252_0  COME_FROM          6136  '6136'

 L. 970      6252  LOAD_FAST                'extractedDate'
             6254  LOAD_ATTR                replace

 L. 971      6256  LOAD_GLOBAL              int
             6258  LOAD_FAST                'temp'
             6260  LOAD_METHOD              strftime
             6262  LOAD_STR                 '%Y'
             6264  CALL_METHOD_1         1  '1 positional argument'
             6266  CALL_FUNCTION_1       1  '1 positional argument'

 L. 972      6268  LOAD_GLOBAL              int
             6270  LOAD_FAST                'temp'
             6272  LOAD_METHOD              strftime
             6274  LOAD_STR                 '%m'
             6276  CALL_METHOD_1         1  '1 positional argument'
             6278  CALL_FUNCTION_1       1  '1 positional argument'

 L. 973      6280  LOAD_GLOBAL              int
             6282  LOAD_FAST                'temp'
             6284  LOAD_METHOD              strftime
             6286  LOAD_STR                 '%d'
             6288  CALL_METHOD_1         1  '1 positional argument'
             6290  CALL_FUNCTION_1       1  '1 positional argument'
             6292  LOAD_CONST               ('year', 'month', 'day')
             6294  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6296  STORE_FAST               'extractedDate'
           6298_0  COME_FROM          6250  '6250'
           6298_1  COME_FROM          5982  '5982'

 L. 975      6298  LOAD_DEREF               'timeStr'
             6300  LOAD_STR                 ''
             6302  COMPARE_OP               !=
         6304_6306  POP_JUMP_IF_FALSE  6350  'to 6350'

 L. 976      6308  LOAD_GLOBAL              datetime
             6310  LOAD_DEREF               'timeStr'
             6312  CALL_FUNCTION_1       1  '1 positional argument'
             6314  STORE_FAST               'temp'

 L. 977      6316  LOAD_FAST                'extractedDate'
             6318  LOAD_ATTR                replace
             6320  LOAD_FAST                'temp'
             6322  LOAD_METHOD              strftime
             6324  LOAD_STR                 '%H'
             6326  CALL_METHOD_1         1  '1 positional argument'

 L. 978      6328  LOAD_FAST                'temp'
             6330  LOAD_METHOD              strftime
             6332  LOAD_STR                 '%M'
             6334  CALL_METHOD_1         1  '1 positional argument'

 L. 979      6336  LOAD_FAST                'temp'
             6338  LOAD_METHOD              strftime
             6340  LOAD_STR                 '%S'
             6342  CALL_METHOD_1         1  '1 positional argument'
             6344  LOAD_CONST               ('hour', 'minute', 'second')
             6346  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6348  STORE_FAST               'extractedDate'
           6350_0  COME_FROM          6304  '6304'

 L. 981      6350  LOAD_DEREF               'yearOffset'
             6352  LOAD_CONST               0
             6354  COMPARE_OP               !=
         6356_6358  POP_JUMP_IF_FALSE  6374  'to 6374'

 L. 982      6360  LOAD_FAST                'extractedDate'
             6362  LOAD_GLOBAL              relativedelta
             6364  LOAD_DEREF               'yearOffset'
             6366  LOAD_CONST               ('years',)
             6368  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6370  BINARY_ADD       
             6372  STORE_FAST               'extractedDate'
           6374_0  COME_FROM          6356  '6356'

 L. 983      6374  LOAD_DEREF               'monthOffset'
             6376  LOAD_CONST               0
             6378  COMPARE_OP               !=
         6380_6382  POP_JUMP_IF_FALSE  6398  'to 6398'

 L. 984      6384  LOAD_FAST                'extractedDate'
             6386  LOAD_GLOBAL              relativedelta
             6388  LOAD_DEREF               'monthOffset'
             6390  LOAD_CONST               ('months',)
             6392  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6394  BINARY_ADD       
             6396  STORE_FAST               'extractedDate'
           6398_0  COME_FROM          6380  '6380'

 L. 985      6398  LOAD_DEREF               'dayOffset'
             6400  LOAD_CONST               0
             6402  COMPARE_OP               !=
         6404_6406  POP_JUMP_IF_FALSE  6422  'to 6422'

 L. 986      6408  LOAD_FAST                'extractedDate'
             6410  LOAD_GLOBAL              relativedelta
             6412  LOAD_DEREF               'dayOffset'
             6414  LOAD_CONST               ('days',)
             6416  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6418  BINARY_ADD       
             6420  STORE_FAST               'extractedDate'
           6422_0  COME_FROM          6404  '6404'

 L. 987      6422  LOAD_DEREF               'hrAbs'
         6424_6426  JUMP_IF_TRUE_OR_POP  6430  'to 6430'
             6428  LOAD_CONST               0
           6430_0  COME_FROM          6424  '6424'
             6430  LOAD_CONST               -1
             6432  COMPARE_OP               !=
         6434_6436  POP_JUMP_IF_FALSE  6572  'to 6572'
             6438  LOAD_DEREF               'minAbs'
         6440_6442  JUMP_IF_TRUE_OR_POP  6446  'to 6446'
             6444  LOAD_CONST               0
           6446_0  COME_FROM          6440  '6440'
             6446  LOAD_CONST               -1
             6448  COMPARE_OP               !=
         6450_6452  POP_JUMP_IF_FALSE  6572  'to 6572'

 L. 988      6454  LOAD_DEREF               'hrAbs'
             6456  LOAD_CONST               None
             6458  COMPARE_OP               is
         6460_6462  POP_JUMP_IF_FALSE  6492  'to 6492'
             6464  LOAD_DEREF               'minAbs'
             6466  LOAD_CONST               None
             6468  COMPARE_OP               is
         6470_6472  POP_JUMP_IF_FALSE  6492  'to 6492'
             6474  LOAD_FAST                'default_time'
         6476_6478  POP_JUMP_IF_FALSE  6492  'to 6492'

 L. 989      6480  LOAD_FAST                'default_time'
             6482  LOAD_ATTR                hour
             6484  STORE_DEREF              'hrAbs'

 L. 990      6486  LOAD_FAST                'default_time'
             6488  LOAD_ATTR                minute
             6490  STORE_DEREF              'minAbs'
           6492_0  COME_FROM          6476  '6476'
           6492_1  COME_FROM          6470  '6470'
           6492_2  COME_FROM          6460  '6460'

 L. 991      6492  LOAD_FAST                'extractedDate'
             6494  LOAD_GLOBAL              relativedelta
             6496  LOAD_DEREF               'hrAbs'
         6498_6500  JUMP_IF_TRUE_OR_POP  6504  'to 6504'
             6502  LOAD_CONST               0
           6504_0  COME_FROM          6498  '6498'

 L. 992      6504  LOAD_DEREF               'minAbs'
         6506_6508  JUMP_IF_TRUE_OR_POP  6512  'to 6512'
             6510  LOAD_CONST               0
           6512_0  COME_FROM          6506  '6506'
             6512  LOAD_CONST               ('hours', 'minutes')
             6514  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6516  BINARY_ADD       
             6518  STORE_FAST               'extractedDate'

 L. 993      6520  LOAD_DEREF               'hrAbs'
         6522_6524  POP_JUMP_IF_TRUE   6532  'to 6532'
             6526  LOAD_DEREF               'minAbs'
         6528_6530  POP_JUMP_IF_FALSE  6572  'to 6572'
           6532_0  COME_FROM          6522  '6522'
             6532  LOAD_DEREF               'datestr'
             6534  LOAD_STR                 ''
             6536  COMPARE_OP               ==
         6538_6540  POP_JUMP_IF_FALSE  6572  'to 6572'

 L. 994      6542  LOAD_FAST                'daySpecified'
         6544_6546  POP_JUMP_IF_TRUE   6572  'to 6572'
             6548  LOAD_FAST                'dateNow'
             6550  LOAD_FAST                'extractedDate'
             6552  COMPARE_OP               >
         6554_6556  POP_JUMP_IF_FALSE  6572  'to 6572'

 L. 995      6558  LOAD_FAST                'extractedDate'
             6560  LOAD_GLOBAL              relativedelta
             6562  LOAD_CONST               1
             6564  LOAD_CONST               ('days',)
             6566  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6568  BINARY_ADD       
             6570  STORE_FAST               'extractedDate'
           6572_0  COME_FROM          6554  '6554'
           6572_1  COME_FROM          6544  '6544'
           6572_2  COME_FROM          6538  '6538'
           6572_3  COME_FROM          6528  '6528'
           6572_4  COME_FROM          6450  '6450'
           6572_5  COME_FROM          6434  '6434'

 L. 996      6572  LOAD_DEREF               'hrOffset'
             6574  LOAD_CONST               0
             6576  COMPARE_OP               !=
         6578_6580  POP_JUMP_IF_FALSE  6596  'to 6596'

 L. 997      6582  LOAD_FAST                'extractedDate'
             6584  LOAD_GLOBAL              relativedelta
             6586  LOAD_DEREF               'hrOffset'
             6588  LOAD_CONST               ('hours',)
             6590  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6592  BINARY_ADD       
             6594  STORE_FAST               'extractedDate'
           6596_0  COME_FROM          6578  '6578'

 L. 998      6596  LOAD_DEREF               'minOffset'
             6598  LOAD_CONST               0
             6600  COMPARE_OP               !=
         6602_6604  POP_JUMP_IF_FALSE  6620  'to 6620'

 L. 999      6606  LOAD_FAST                'extractedDate'
             6608  LOAD_GLOBAL              relativedelta
             6610  LOAD_DEREF               'minOffset'
             6612  LOAD_CONST               ('minutes',)
             6614  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6616  BINARY_ADD       
             6618  STORE_FAST               'extractedDate'
           6620_0  COME_FROM          6602  '6602'

 L.1000      6620  LOAD_DEREF               'secOffset'
             6622  LOAD_CONST               0
             6624  COMPARE_OP               !=
         6626_6628  POP_JUMP_IF_FALSE  6644  'to 6644'

 L.1001      6630  LOAD_FAST                'extractedDate'
             6632  LOAD_GLOBAL              relativedelta
             6634  LOAD_DEREF               'secOffset'
             6636  LOAD_CONST               ('seconds',)
             6638  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6640  BINARY_ADD       
             6642  STORE_FAST               'extractedDate'
           6644_0  COME_FROM          6626  '6626'

 L.1003      6644  LOAD_STR                 ' '
             6646  LOAD_METHOD              join
             6648  LOAD_FAST                'words'
             6650  CALL_METHOD_1         1  '1 positional argument'
             6652  STORE_FAST               'resultStr'

 L.1004      6654  LOAD_STR                 ' '
             6656  LOAD_METHOD              join
             6658  LOAD_FAST                'resultStr'
             6660  LOAD_METHOD              split
             6662  CALL_METHOD_0         0  '0 positional arguments'
             6664  CALL_METHOD_1         1  '1 positional argument'
             6666  STORE_FAST               'resultStr'

 L.1005      6668  LOAD_GLOBAL              pt_pruning
             6670  LOAD_FAST                'resultStr'
             6672  CALL_FUNCTION_1       1  '1 positional argument'
             6674  STORE_FAST               'resultStr'

 L.1006      6676  LOAD_FAST                'extractedDate'
             6678  LOAD_FAST                'resultStr'
             6680  BUILD_LIST_2          2 
             6682  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_METHOD_0' instruction at offset 2478


def pt_pruning(text, symbols=True, accents=True, agressive=True):
    words = [
     'a', 'o', 'os', 'as', 'de', 'dos', 'das',
     'lhe', 'lhes', 'me', 'e', 'no', 'nas', 'na', 'nos', 'em', 'para',
     'este',
     'esta', 'deste', 'desta', 'neste', 'nesta', 'nesse',
     'nessa', 'foi', 'que']
    if symbols:
        symbols = [
         '.', ',', ';', ':', '!', '?', 'ï¿½', 'ï¿½']
        for symbol in symbols:
            text = text.replace(symbol, '')

        text = text.replace('-', ' ').replace('_', ' ')
    if accents:
        accents = {'a':[
          'á', 'à', 'ã', 'â'], 
         'e':[
          'ê', 'è', 'é'], 
         'i':[
          'í', 'ì'], 
         'o':[
          'ò', 'ó'], 
         'u':[
          'ú', 'ù'], 
         'c':[
          'ç']}
        for char in accents:
            for acc in accents[char]:
                text = text.replace(acc, char)

    if agressive:
        text_words = text.split(' ')
        for idx, word in enumerate(text_words):
            if word in words:
                text_words[idx] = ''

        text = ' '.join(text_words)
        text = ' '.join(text.split())
    return text


def get_gender_pt(word, text=''):
    word = word.lower()
    words = text.lower().split(' ')
    for idx, w in enumerate(words):
        if w == word:
            if idx != 0:
                previous = words[(idx - 1)].lower()
                if previous in _MALE_DETERMINANTS_PT:
                    return 'm'
            if previous in _FEMALE_DETERMINANTS_PT:
                return 'f'

    if word in _GENDERS_PT:
        return _GENDERS_PT[word]
    singular = word.rstrip('s')
    if singular in _GENDERS_PT:
        return _GENDERS_PT[singular]
    for end_str in _FEMALE_ENDINGS_PT:
        if word.endswith(end_str):
            return 'f'

    for end_str in _MALE_ENDINGS_PT:
        if word.endswith(end_str):
            return 'm'