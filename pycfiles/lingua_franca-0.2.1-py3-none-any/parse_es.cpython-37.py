# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_es.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 38837 bytes
"""
    Parse functions for spanish (es)
    TODO: numbers greater than 999999
"""
from datetime import datetime
import dateutil.relativedelta as relativedelta
from dateutil.tz import gettz
from lingua_franca.lang.format_es import pronounce_number_es
from lingua_franca.lang.parse_common import *
from lingua_franca.lang.common_data_es import _ARTICLES_ES, _NUM_STRING_ES

def isFractional_es(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]
    aFrac = {'medio':2,  'media':2,  'tercio':3,  'cuarto':4,  'cuarta':4, 
     'quinto':5,  'quinta':5,  'sexto':6,  'sexta':6,  'séptimo':7, 
     'séptima':7,  'octavo':8,  'octava':8,  'noveno':9, 
     'novena':9,  'décimo':10,  'décima':10,  'onceavo':11, 
     'onceava':11,  'doceavo':12,  'doceava':12}
    if input_str.lower() in aFrac:
        return 1.0 / aFrac[input_str]
    if input_str == 'vigésimo' or input_str == 'vigésima':
        return 0.05
    if input_str == 'trigésimo' or input_str == 'trigésima':
        return 0.03333333333333333
    if input_str == 'centésimo' or input_str == 'centésima':
        return 0.01
    if input_str == 'milésimo' or input_str == 'milésima':
        return 0.001
    return False


def extractnumber_es(text, short_scale=True, ordinals=False):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number

    """
    aWords = text.lower().split()
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
        if word in _NUM_STRING_ES:
            val = _NUM_STRING_ES[word]
        else:
            if word.isdigit():
                val = int(word)
            else:
                if is_numeric(word):
                    val = float(word)
                else:
                    if isFractional_es(word):
                        if not result:
                            result = 1
                        result = result * isFractional_es(word)
                        count += 1
                        continue
                    elif not val:
                        aPieces = word.split('/')
                        if look_for_fractions(aPieces):
                            val = float(aPieces[0]) / float(aPieces[1])
                        elif val:
                            if result is None:
                                result = 0
                            if next_word != 'avos':
                                result = val
                            else:
                                result = float(result) / float(val)
                        if next_word is None:
                            break
                        ands = ['y']
                        if next_word in ands:
                            zeros = 0
                            if result is None:
                                count += 1
                                continue
                            newWords = aWords[count + 2:]
                            newText = ''
                            for word in newWords:
                                newText += word + ' '

                            afterAndVal = extractnumber_es(newText[:-1])
                            if afterAndVal and not result < afterAndVal:
                                if result < 20:
                                    while afterAndVal > 1:
                                        afterAndVal = afterAndVal / 10.0

                                    for word in newWords:
                                        if word == 'cero' or word == '0':
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

                            afterAndVal = extractnumber_es(newText[:-1])
                            if afterAndVal:
                                if result is None:
                                    result = 0
                                result += afterAndVal
                                break
                    decimals = [
                     'punto', 'coma', '.', ',']
                    if next_word in decimals:
                        zeros = 0
                        newWords = aWords[count + 2:]
                        newText = ''
                        for word in newWords:
                            newText += word + ' '

                        for word in newWords:
                            if word == 'cero' or word == '0':
                                zeros += 1
                            else:
                                break

                        afterDotVal = str(extractnumber_es(newText[:-1]))
                        afterDotVal = zeros * '0' + afterDotVal
                        result = float(str(result) + '.' + afterDotVal)
                        break
                    count += 1

    if '.' in str(result):
        integer, dec = str(result).split('.')
        if dec == '0':
            result = int(integer)
    return result or False


def es_number_parse(words, i):

    def es_cte(i, s):
        if i < len(words):
            if s == words[i]:
                return (
                 s, i + 1)

    def es_number_word(i, mi, ma):
        if i < len(words):
            v = _NUM_STRING_ES.get(words[i])
            if v:
                if v >= mi:
                    if v <= ma:
                        return (
                         v, i + 1)

    def es_number_1_99(i):
        r1 = es_number_word(i, 1, 29)
        if r1:
            return r1
        r1 = es_number_word(i, 30, 90)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, 'y')
            if r2:
                i2 = r2[1]
                r3 = es_number_word(i2, 1, 9)
                if r3:
                    v3, i3 = r3
                    return (v1 + v3, i3)
            return r1

    def es_number_1_999(i):
        r1 = es_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = es_number_1_99(i1)
            if r2:
                v2, i2 = r2
                return (v1 + v2, i2)
            return r1
        r1 = es_number_1_99(i)
        if r1:
            return r1

    def es_number(i):
        r1 = es_number_word(i, 0, 0)
        if r1:
            return r1
        r1 = es_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, 'mil')
            if r2:
                i2 = r2[1]
                r3 = es_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return (v1 * 1000 + v3, i3)
                return (v1 * 1000, i2)
            else:
                return r1

    return es_number(i)


def extract_numbers_es(text, short_scale=True, ordinals=False):
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
    return extract_numbers_generic(text, pronounce_number_es, extractnumber_es, short_scale=short_scale,
      ordinals=ordinals)


def normalize_es(text, remove_articles):
    """ Spanish string normalization """
    words = text.split()
    normalized = ''
    i = 0
    while i < len(words):
        word = words[i]
        if remove_articles:
            if word in _ARTICLES_ES:
                i += 1
                continue
        r = es_number_parse(words, i)
        if r:
            v, i = r
            normalized += ' ' + str(v)
            continue
        normalized += ' ' + word
        i += 1

    return normalized[1:]


def extract_datetime_es--- This code section failed: ---

 L. 317         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_es.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 356         8  LOAD_CLOSURE             'datestr'
               10  LOAD_CLOSURE             'dayOffset'
               12  LOAD_CLOSURE             'found'
               14  LOAD_CLOSURE             'hrAbs'
               16  LOAD_CLOSURE             'hrOffset'
               18  LOAD_CLOSURE             'minAbs'
               20  LOAD_CLOSURE             'minOffset'
               22  LOAD_CLOSURE             'monthOffset'
               24  LOAD_CLOSURE             'secOffset'
               26  LOAD_CLOSURE             'yearOffset'
               28  BUILD_TUPLE_10       10 
               30  LOAD_CODE                <code_object date_found>
               32  LOAD_STR                 'extract_datetime_es.<locals>.date_found'
               34  MAKE_FUNCTION_8          'closure'
               36  STORE_FAST               'date_found'

 L. 366        38  LOAD_FAST                'input_str'
               40  LOAD_STR                 ''
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 367        46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'

 L. 368        50  LOAD_FAST                'currentDate'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 369        58  LOAD_GLOBAL              datetime
               60  LOAD_METHOD              now
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  STORE_FAST               'currentDate'
             66_0  COME_FROM            56  '56'

 L. 371        66  LOAD_CONST               False
               68  STORE_DEREF              'found'

 L. 372        70  LOAD_CONST               False
               72  STORE_FAST               'daySpecified'

 L. 373        74  LOAD_CONST               False
               76  STORE_DEREF              'dayOffset'

 L. 374        78  LOAD_CONST               0
               80  STORE_DEREF              'monthOffset'

 L. 375        82  LOAD_CONST               0
               84  STORE_DEREF              'yearOffset'

 L. 376        86  LOAD_FAST                'currentDate'
               88  STORE_FAST               'dateNow'

 L. 377        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%w'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'today'

 L. 378       100  LOAD_FAST                'dateNow'
              102  LOAD_METHOD              strftime
              104  LOAD_STR                 '%Y'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               'currentYear'

 L. 379       110  LOAD_CONST               False
              112  STORE_FAST               'fromFlag'

 L. 380       114  LOAD_STR                 ''
              116  STORE_DEREF              'datestr'

 L. 381       118  LOAD_CONST               False
              120  STORE_FAST               'hasYear'

 L. 382       122  LOAD_STR                 ''
              124  STORE_FAST               'timeQualifier'

 L. 384       126  LOAD_FAST                'clean_string'
              128  LOAD_FAST                'input_str'
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  LOAD_METHOD              split
              134  LOAD_STR                 ' '
              136  CALL_METHOD_1         1  '1 positional argument'
              138  STORE_FAST               'words'

 L. 385       140  LOAD_STR                 'mañana'
              142  LOAD_STR                 'tarde'
              144  LOAD_STR                 'noche'
              146  BUILD_LIST_3          3 
              148  STORE_FAST               'timeQualifiersList'

 L. 386       150  LOAD_STR                 'en'
              152  LOAD_STR                 'la'
              154  LOAD_STR                 'al'
              156  LOAD_STR                 'por'
              158  LOAD_STR                 'pasados'

 L. 387       160  LOAD_STR                 'pasadas'
              162  LOAD_STR                 'día'
              164  LOAD_STR                 'hora'
              166  BUILD_LIST_8          8 
              168  STORE_FAST               'time_indicators'

 L. 388       170  LOAD_STR                 'lunes'
              172  LOAD_STR                 'martes'
              174  LOAD_STR                 'miércoles'

 L. 389       176  LOAD_STR                 'jueves'
              178  LOAD_STR                 'viernes'
              180  LOAD_STR                 'sábado'
              182  LOAD_STR                 'domingo'
              184  BUILD_LIST_7          7 
              186  STORE_FAST               'days'

 L. 390       188  LOAD_STR                 'enero'
              190  LOAD_STR                 'febrero'
              192  LOAD_STR                 'marzo'
              194  LOAD_STR                 'abril'
              196  LOAD_STR                 'mayo'
              198  LOAD_STR                 'junio'

 L. 391       200  LOAD_STR                 'julio'
              202  LOAD_STR                 'agosto'
              204  LOAD_STR                 'septiembre'
              206  LOAD_STR                 'octubre'
              208  LOAD_STR                 'noviembre'

 L. 392       210  LOAD_STR                 'diciembre'
              212  BUILD_LIST_12        12 
              214  STORE_FAST               'months'

 L. 393       216  LOAD_STR                 'ene'
              218  LOAD_STR                 'feb'
              220  LOAD_STR                 'mar'
              222  LOAD_STR                 'abr'
              224  LOAD_STR                 'may'
              226  LOAD_STR                 'jun'
              228  LOAD_STR                 'jul'
              230  LOAD_STR                 'ago'

 L. 394       232  LOAD_STR                 'sep'
              234  LOAD_STR                 'oct'
              236  LOAD_STR                 'nov'
              238  LOAD_STR                 'dic'
              240  BUILD_LIST_12        12 
              242  STORE_FAST               'monthsShort'

 L. 395       244  LOAD_STR                 'siguiente'
              246  LOAD_STR                 'próximo'
              248  LOAD_STR                 'próxima'
              250  BUILD_LIST_3          3 
              252  STORE_FAST               'nexts'

 L. 396       254  LOAD_STR                 'siguientes'
              256  LOAD_STR                 'subsecuentes'
              258  BUILD_LIST_2          2 
              260  STORE_FAST               'suffix_nexts'

 L. 397       262  LOAD_STR                 'último'
              264  LOAD_STR                 'última'
              266  BUILD_LIST_2          2 
              268  STORE_FAST               'lasts'

 L. 398       270  LOAD_STR                 'pasada'
              272  LOAD_STR                 'pasado'
              274  LOAD_STR                 'anterior'
              276  LOAD_STR                 'antes'
              278  BUILD_LIST_4          4 
              280  STORE_FAST               'suffix_lasts'

 L. 399       282  LOAD_STR                 'después'
              284  LOAD_STR                 'siguiente'
              286  LOAD_STR                 'próximo'
              288  LOAD_STR                 'próxima'
              290  BUILD_LIST_4          4 
              292  STORE_FAST               'nxts'

 L. 400       294  LOAD_STR                 'antes'
              296  LOAD_STR                 'previa'
              298  LOAD_STR                 'previo'
              300  LOAD_STR                 'anterior'
              302  BUILD_LIST_4          4 
              304  STORE_FAST               'prevs'

 L. 401       306  LOAD_STR                 'desde'
              308  LOAD_STR                 'en'
              310  LOAD_STR                 'para'
              312  LOAD_STR                 'después de'
              314  LOAD_STR                 'por'
              316  LOAD_STR                 'próximo'

 L. 402       318  LOAD_STR                 'próxima'
              320  LOAD_STR                 'de'
              322  BUILD_LIST_8          8 
              324  STORE_FAST               'froms'

 L. 403       326  LOAD_STR                 'este'
              328  LOAD_STR                 'esta'
              330  BUILD_LIST_2          2 
              332  STORE_FAST               'thises'

 L. 404       334  LOAD_FAST                'froms'
              336  LOAD_FAST                'thises'
              338  INPLACE_ADD      
              340  STORE_FAST               'froms'

 L. 405       342  LOAD_FAST                'nxts'
              344  LOAD_FAST                'prevs'
              346  BINARY_ADD       
              348  LOAD_FAST                'froms'
              350  BINARY_ADD       
              352  LOAD_FAST                'time_indicators'
              354  BINARY_ADD       
              356  STORE_FAST               'lists'

 L. 406   358_360  SETUP_LOOP         3194  'to 3194'
              362  LOAD_GLOBAL              enumerate
              364  LOAD_FAST                'words'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  GET_ITER         
            370_0  COME_FROM          3050  '3050'
          370_372  FOR_ITER           3192  'to 3192'
              374  UNPACK_SEQUENCE_2     2 
              376  STORE_FAST               'idx'
              378  STORE_FAST               'word'

 L. 407       380  LOAD_FAST                'word'
              382  LOAD_STR                 ''
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   394  'to 394'

 L. 408   390_392  CONTINUE            370  'to 370'
            394_0  COME_FROM           386  '386'

 L. 409       394  LOAD_FAST                'idx'
              396  LOAD_CONST               1
              398  COMPARE_OP               >
          400_402  POP_JUMP_IF_FALSE   416  'to 416'
              404  LOAD_FAST                'words'
              406  LOAD_FAST                'idx'
              408  LOAD_CONST               2
              410  BINARY_SUBTRACT  
              412  BINARY_SUBSCR    
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           400  '400'
              416  LOAD_STR                 ''
            418_0  COME_FROM           414  '414'
              418  STORE_FAST               'wordPrevPrev'

 L. 410       420  LOAD_FAST                'idx'
              422  LOAD_CONST               0
              424  COMPARE_OP               >
          426_428  POP_JUMP_IF_FALSE   442  'to 442'
              430  LOAD_FAST                'words'
              432  LOAD_FAST                'idx'
              434  LOAD_CONST               1
              436  BINARY_SUBTRACT  
              438  BINARY_SUBSCR    
              440  JUMP_FORWARD        444  'to 444'
            442_0  COME_FROM           426  '426'
              442  LOAD_STR                 ''
            444_0  COME_FROM           440  '440'
              444  STORE_FAST               'wordPrev'

 L. 411       446  LOAD_FAST                'idx'
              448  LOAD_CONST               1
              450  BINARY_ADD       
              452  LOAD_GLOBAL              len
              454  LOAD_FAST                'words'
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  COMPARE_OP               <
          460_462  POP_JUMP_IF_FALSE   476  'to 476'
              464  LOAD_FAST                'words'
              466  LOAD_FAST                'idx'
              468  LOAD_CONST               1
              470  BINARY_ADD       
              472  BINARY_SUBSCR    
              474  JUMP_FORWARD        478  'to 478'
            476_0  COME_FROM           460  '460'
              476  LOAD_STR                 ''
            478_0  COME_FROM           474  '474'
              478  STORE_FAST               'wordNext'

 L. 412       480  LOAD_FAST                'idx'
              482  LOAD_CONST               2
              484  BINARY_ADD       
              486  LOAD_GLOBAL              len
              488  LOAD_FAST                'words'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  COMPARE_OP               <
          494_496  POP_JUMP_IF_FALSE   510  'to 510'
              498  LOAD_FAST                'words'
              500  LOAD_FAST                'idx'
              502  LOAD_CONST               2
              504  BINARY_ADD       
              506  BINARY_SUBSCR    
              508  JUMP_FORWARD        512  'to 512'
            510_0  COME_FROM           494  '494'
              510  LOAD_STR                 ''
            512_0  COME_FROM           508  '508'
              512  STORE_FAST               'wordNextNext'

 L. 413       514  LOAD_FAST                'idx'
              516  LOAD_CONST               3
              518  BINARY_ADD       
              520  LOAD_GLOBAL              len
              522  LOAD_FAST                'words'
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  COMPARE_OP               <
          528_530  POP_JUMP_IF_FALSE   544  'to 544'
              532  LOAD_FAST                'words'
              534  LOAD_FAST                'idx'
              536  LOAD_CONST               3
              538  BINARY_ADD       
              540  BINARY_SUBSCR    
              542  JUMP_FORWARD        546  'to 546'
            544_0  COME_FROM           528  '528'
              544  LOAD_STR                 ''
            546_0  COME_FROM           542  '542'
              546  STORE_FAST               'wordNextNextNext'

 L. 415       548  LOAD_FAST                'idx'
              550  STORE_FAST               'start'

 L. 416       552  LOAD_CONST               0
              554  STORE_FAST               'used'

 L. 418       556  LOAD_FAST                'word'
              558  LOAD_FAST                'timeQualifiersList'
              560  COMPARE_OP               in
          562_564  POP_JUMP_IF_FALSE   574  'to 574'

 L. 419       566  LOAD_FAST                'word'
              568  STORE_FAST               'timeQualifier'
          570_572  JUMP_FORWARD       2486  'to 2486'
            574_0  COME_FROM           562  '562'

 L. 422       574  LOAD_FAST                'word'
              576  LOAD_STR                 'hoy'
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_FALSE   606  'to 606'
              584  LOAD_FAST                'fromFlag'
          586_588  POP_JUMP_IF_TRUE    606  'to 606'

 L. 423       590  LOAD_CONST               0
              592  STORE_DEREF              'dayOffset'

 L. 424       594  LOAD_FAST                'used'
              596  LOAD_CONST               1
              598  INPLACE_ADD      
              600  STORE_FAST               'used'
          602_604  JUMP_FORWARD       2486  'to 2486'
            606_0  COME_FROM           586  '586'
            606_1  COME_FROM           580  '580'

 L. 425       606  LOAD_FAST                'word'
              608  LOAD_STR                 'mañana'
              610  COMPARE_OP               ==
          612_614  POP_JUMP_IF_FALSE   638  'to 638'
              616  LOAD_FAST                'fromFlag'
          618_620  POP_JUMP_IF_TRUE    638  'to 638'

 L. 426       622  LOAD_CONST               1
              624  STORE_DEREF              'dayOffset'

 L. 427       626  LOAD_FAST                'used'
              628  LOAD_CONST               1
              630  INPLACE_ADD      
              632  STORE_FAST               'used'
          634_636  JUMP_FORWARD       2486  'to 2486'
            638_0  COME_FROM           618  '618'
            638_1  COME_FROM           612  '612'

 L. 428       638  LOAD_FAST                'word'
              640  LOAD_STR                 'ayer'
              642  COMPARE_OP               ==
          644_646  POP_JUMP_IF_FALSE   674  'to 674'
              648  LOAD_FAST                'fromFlag'
          650_652  POP_JUMP_IF_TRUE    674  'to 674'

 L. 429       654  LOAD_DEREF               'dayOffset'
              656  LOAD_CONST               1
              658  INPLACE_SUBTRACT 
              660  STORE_DEREF              'dayOffset'

 L. 430       662  LOAD_FAST                'used'
              664  LOAD_CONST               1
              666  INPLACE_ADD      
              668  STORE_FAST               'used'
          670_672  JUMP_FORWARD       2486  'to 2486'
            674_0  COME_FROM           650  '650'
            674_1  COME_FROM           644  '644'

 L. 432       674  LOAD_FAST                'word'
              676  LOAD_STR                 'anteayer'
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_TRUE    704  'to 704'

 L. 433       684  LOAD_FAST                'word'
              686  LOAD_STR                 'ante'
              688  COMPARE_OP               ==
          690_692  POP_JUMP_IF_FALSE   748  'to 748'
              694  LOAD_FAST                'wordNext'
              696  LOAD_STR                 'ayer'
              698  COMPARE_OP               ==
          700_702  POP_JUMP_IF_FALSE   748  'to 748'
            704_0  COME_FROM           680  '680'
              704  LOAD_FAST                'fromFlag'
          706_708  POP_JUMP_IF_TRUE    748  'to 748'

 L. 434       710  LOAD_DEREF               'dayOffset'
              712  LOAD_CONST               2
              714  INPLACE_SUBTRACT 
              716  STORE_DEREF              'dayOffset'

 L. 435       718  LOAD_FAST                'used'
              720  LOAD_CONST               1
              722  INPLACE_ADD      
              724  STORE_FAST               'used'

 L. 436       726  LOAD_FAST                'wordNext'
              728  LOAD_STR                 'ayer'
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_FALSE  2486  'to 2486'

 L. 437       736  LOAD_FAST                'used'
              738  LOAD_CONST               1
              740  INPLACE_ADD      
              742  STORE_FAST               'used'
          744_746  JUMP_FORWARD       2486  'to 2486'
            748_0  COME_FROM           706  '706'
            748_1  COME_FROM           700  '700'
            748_2  COME_FROM           690  '690'

 L. 438       748  LOAD_FAST                'word'
              750  LOAD_STR                 'ante'
              752  COMPARE_OP               ==
          754_756  POP_JUMP_IF_FALSE   804  'to 804'
              758  LOAD_FAST                'wordNext'
              760  LOAD_STR                 'ante'
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   804  'to 804'
              768  LOAD_FAST                'wordNextNext'

 L. 439       770  LOAD_STR                 'ayer'
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_FALSE   804  'to 804'
              778  LOAD_FAST                'fromFlag'
          780_782  POP_JUMP_IF_TRUE    804  'to 804'

 L. 440       784  LOAD_DEREF               'dayOffset'
              786  LOAD_CONST               3
              788  INPLACE_SUBTRACT 
              790  STORE_DEREF              'dayOffset'

 L. 441       792  LOAD_FAST                'used'
              794  LOAD_CONST               3
              796  INPLACE_ADD      
              798  STORE_FAST               'used'
          800_802  JUMP_FORWARD       2486  'to 2486'
            804_0  COME_FROM           780  '780'
            804_1  COME_FROM           774  '774'
            804_2  COME_FROM           764  '764'
            804_3  COME_FROM           754  '754'

 L. 442       804  LOAD_FAST                'word'
              806  LOAD_STR                 'ante anteayer'
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   840  'to 840'
              814  LOAD_FAST                'fromFlag'
          816_818  POP_JUMP_IF_TRUE    840  'to 840'

 L. 443       820  LOAD_DEREF               'dayOffset'
              822  LOAD_CONST               3
              824  INPLACE_SUBTRACT 
              826  STORE_DEREF              'dayOffset'

 L. 444       828  LOAD_FAST                'used'
              830  LOAD_CONST               1
              832  INPLACE_ADD      
              834  STORE_FAST               'used'
          836_838  JUMP_FORWARD       2486  'to 2486'
            840_0  COME_FROM           816  '816'
            840_1  COME_FROM           810  '810'

 L. 446       840  LOAD_FAST                'word'
              842  LOAD_STR                 'pasado'
              844  COMPARE_OP               ==
          846_848  POP_JUMP_IF_FALSE   882  'to 882'
              850  LOAD_FAST                'wordNext'
              852  LOAD_STR                 'mañana'
              854  COMPARE_OP               ==
          856_858  POP_JUMP_IF_FALSE   882  'to 882'
              860  LOAD_FAST                'fromFlag'
          862_864  POP_JUMP_IF_TRUE    882  'to 882'

 L. 447       866  LOAD_DEREF               'dayOffset'
              868  LOAD_CONST               2
              870  INPLACE_ADD      
              872  STORE_DEREF              'dayOffset'

 L. 448       874  LOAD_CONST               2
              876  STORE_FAST               'used'
          878_880  JUMP_FORWARD       2486  'to 2486'
            882_0  COME_FROM           862  '862'
            882_1  COME_FROM           856  '856'
            882_2  COME_FROM           846  '846'

 L. 450       882  LOAD_FAST                'word'
              884  LOAD_STR                 'ante'
              886  COMPARE_OP               ==
          888_890  POP_JUMP_IF_FALSE   924  'to 924'
              892  LOAD_FAST                'wordNext'
              894  LOAD_STR                 'ayer'
              896  COMPARE_OP               ==
          898_900  POP_JUMP_IF_FALSE   924  'to 924'
              902  LOAD_FAST                'fromFlag'
          904_906  POP_JUMP_IF_TRUE    924  'to 924'

 L. 451       908  LOAD_DEREF               'dayOffset'
              910  LOAD_CONST               2
              912  INPLACE_SUBTRACT 
              914  STORE_DEREF              'dayOffset'

 L. 452       916  LOAD_CONST               2
              918  STORE_FAST               'used'
          920_922  JUMP_FORWARD       2486  'to 2486'
            924_0  COME_FROM           904  '904'
            924_1  COME_FROM           898  '898'
            924_2  COME_FROM           888  '888'

 L. 454       924  LOAD_FAST                'word'
              926  LOAD_STR                 'día'
              928  COMPARE_OP               ==
          930_932  POP_JUMP_IF_FALSE  1154  'to 1154'

 L. 455       934  LOAD_FAST                'wordNext'
              936  LOAD_STR                 'pasado'
              938  COMPARE_OP               ==
          940_942  POP_JUMP_IF_TRUE    954  'to 954'
              944  LOAD_FAST                'wordNext'
              946  LOAD_STR                 'ante'
              948  COMPARE_OP               ==
          950_952  POP_JUMP_IF_FALSE  1012  'to 1012'
            954_0  COME_FROM           940  '940'

 L. 456       954  LOAD_FAST                'used'
              956  LOAD_CONST               1
              958  INPLACE_ADD      
              960  STORE_FAST               'used'

 L. 457       962  LOAD_FAST                'wordPrev'
          964_966  POP_JUMP_IF_FALSE  1150  'to 1150'
              968  LOAD_FAST                'wordPrev'
              970  LOAD_CONST               0
              972  BINARY_SUBSCR    
              974  LOAD_METHOD              isdigit
              976  CALL_METHOD_0         0  '0 positional arguments'
          978_980  POP_JUMP_IF_FALSE  1150  'to 1150'

 L. 458       982  LOAD_DEREF               'dayOffset'
              984  LOAD_GLOBAL              int
              986  LOAD_FAST                'wordPrev'
              988  CALL_FUNCTION_1       1  '1 positional argument'
              990  INPLACE_ADD      
              992  STORE_DEREF              'dayOffset'

 L. 459       994  LOAD_FAST                'start'
              996  LOAD_CONST               1
              998  INPLACE_SUBTRACT 
             1000  STORE_FAST               'start'

 L. 460      1002  LOAD_FAST                'used'
             1004  LOAD_CONST               1
             1006  INPLACE_ADD      
             1008  STORE_FAST               'used'
             1010  JUMP_FORWARD       2486  'to 2486'
           1012_0  COME_FROM           950  '950'

 L. 461      1012  LOAD_FAST                'wordPrev'
         1014_1016  POP_JUMP_IF_FALSE  1082  'to 1082'
             1018  LOAD_FAST                'wordPrev'
             1020  LOAD_CONST               0
             1022  BINARY_SUBSCR    
             1024  LOAD_METHOD              isdigit
             1026  CALL_METHOD_0         0  '0 positional arguments'
         1028_1030  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 462      1032  LOAD_FAST                'wordNext'
             1034  LOAD_FAST                'months'
             1036  COMPARE_OP               not-in
         1038_1040  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 463      1042  LOAD_FAST                'wordNext'
             1044  LOAD_FAST                'monthsShort'
             1046  COMPARE_OP               not-in
         1048_1050  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 464      1052  LOAD_DEREF               'dayOffset'
             1054  LOAD_GLOBAL              int
             1056  LOAD_FAST                'wordPrev'
             1058  CALL_FUNCTION_1       1  '1 positional argument'
             1060  INPLACE_ADD      
             1062  STORE_DEREF              'dayOffset'

 L. 465      1064  LOAD_FAST                'start'
             1066  LOAD_CONST               1
             1068  INPLACE_SUBTRACT 
             1070  STORE_FAST               'start'

 L. 466      1072  LOAD_FAST                'used'
             1074  LOAD_CONST               2
             1076  INPLACE_ADD      
             1078  STORE_FAST               'used'
             1080  JUMP_FORWARD       2486  'to 2486'
           1082_0  COME_FROM          1048  '1048'
           1082_1  COME_FROM          1038  '1038'
           1082_2  COME_FROM          1028  '1028'
           1082_3  COME_FROM          1014  '1014'

 L. 467      1082  LOAD_FAST                'wordNext'
         1084_1086  POP_JUMP_IF_FALSE  2486  'to 2486'
             1088  LOAD_FAST                'wordNext'
             1090  LOAD_CONST               0
             1092  BINARY_SUBSCR    
             1094  LOAD_METHOD              isdigit
             1096  CALL_METHOD_0         0  '0 positional arguments'
         1098_1100  POP_JUMP_IF_FALSE  2486  'to 2486'
             1102  LOAD_FAST                'wordNextNext'

 L. 468      1104  LOAD_FAST                'months'
             1106  COMPARE_OP               not-in
         1108_1110  POP_JUMP_IF_FALSE  2486  'to 2486'
             1112  LOAD_FAST                'wordNextNext'
             1114  LOAD_FAST                'monthsShort'
             1116  COMPARE_OP               not-in
         1118_1120  POP_JUMP_IF_FALSE  2486  'to 2486'

 L. 469      1122  LOAD_DEREF               'dayOffset'
             1124  LOAD_GLOBAL              int
             1126  LOAD_FAST                'wordNext'
             1128  CALL_FUNCTION_1       1  '1 positional argument'
             1130  INPLACE_ADD      
             1132  STORE_DEREF              'dayOffset'

 L. 470      1134  LOAD_FAST                'start'
             1136  LOAD_CONST               1
             1138  INPLACE_SUBTRACT 
             1140  STORE_FAST               'start'

 L. 471      1142  LOAD_FAST                'used'
             1144  LOAD_CONST               2
             1146  INPLACE_ADD      
             1148  STORE_FAST               'used'
           1150_0  COME_FROM           978  '978'
           1150_1  COME_FROM           964  '964'
         1150_1152  JUMP_FORWARD       2486  'to 2486'
           1154_0  COME_FROM           930  '930'

 L. 473      1154  LOAD_FAST                'word'
             1156  LOAD_STR                 'semana'
             1158  COMPARE_OP               ==
         1160_1162  POP_JUMP_IF_FALSE  1384  'to 1384'
             1164  LOAD_FAST                'fromFlag'
         1166_1168  POP_JUMP_IF_TRUE   1384  'to 1384'

 L. 474      1170  LOAD_FAST                'wordPrev'
             1172  LOAD_CONST               0
             1174  BINARY_SUBSCR    
             1176  LOAD_METHOD              isdigit
             1178  CALL_METHOD_0         0  '0 positional arguments'
         1180_1182  POP_JUMP_IF_FALSE  1212  'to 1212'

 L. 475      1184  LOAD_DEREF               'dayOffset'
             1186  LOAD_GLOBAL              int
             1188  LOAD_FAST                'wordPrev'
             1190  CALL_FUNCTION_1       1  '1 positional argument'
             1192  LOAD_CONST               7
             1194  BINARY_MULTIPLY  
             1196  INPLACE_ADD      
             1198  STORE_DEREF              'dayOffset'

 L. 476      1200  LOAD_FAST                'start'
             1202  LOAD_CONST               1
             1204  INPLACE_SUBTRACT 
             1206  STORE_FAST               'start'

 L. 477      1208  LOAD_CONST               2
             1210  STORE_FAST               'used'
           1212_0  COME_FROM          1180  '1180'

 L. 478      1212  SETUP_LOOP         1254  'to 1254'
             1214  LOAD_FAST                'nexts'
             1216  GET_ITER         
           1218_0  COME_FROM          1228  '1228'
             1218  FOR_ITER           1252  'to 1252'
             1220  STORE_FAST               'w'

 L. 479      1222  LOAD_FAST                'wordPrev'
             1224  LOAD_FAST                'w'
             1226  COMPARE_OP               ==
         1228_1230  POP_JUMP_IF_FALSE  1218  'to 1218'

 L. 480      1232  LOAD_CONST               7
             1234  STORE_DEREF              'dayOffset'

 L. 481      1236  LOAD_FAST                'start'
             1238  LOAD_CONST               1
             1240  INPLACE_SUBTRACT 
             1242  STORE_FAST               'start'

 L. 482      1244  LOAD_CONST               2
             1246  STORE_FAST               'used'
         1248_1250  JUMP_BACK          1218  'to 1218'
             1252  POP_BLOCK        
           1254_0  COME_FROM_LOOP     1212  '1212'

 L. 483      1254  SETUP_LOOP         1296  'to 1296'
             1256  LOAD_FAST                'lasts'
             1258  GET_ITER         
           1260_0  COME_FROM          1270  '1270'
             1260  FOR_ITER           1294  'to 1294'
             1262  STORE_FAST               'w'

 L. 484      1264  LOAD_FAST                'wordPrev'
             1266  LOAD_FAST                'w'
             1268  COMPARE_OP               ==
         1270_1272  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 485      1274  LOAD_CONST               -7
             1276  STORE_DEREF              'dayOffset'

 L. 486      1278  LOAD_FAST                'start'
             1280  LOAD_CONST               1
             1282  INPLACE_SUBTRACT 
             1284  STORE_FAST               'start'

 L. 487      1286  LOAD_CONST               2
             1288  STORE_FAST               'used'
         1290_1292  JUMP_BACK          1260  'to 1260'
             1294  POP_BLOCK        
           1296_0  COME_FROM_LOOP     1254  '1254'

 L. 488      1296  SETUP_LOOP         1338  'to 1338'
             1298  LOAD_FAST                'suffix_nexts'
             1300  GET_ITER         
           1302_0  COME_FROM          1312  '1312'
             1302  FOR_ITER           1336  'to 1336'
             1304  STORE_FAST               'w'

 L. 489      1306  LOAD_FAST                'wordNext'
             1308  LOAD_FAST                'w'
             1310  COMPARE_OP               ==
         1312_1314  POP_JUMP_IF_FALSE  1302  'to 1302'

 L. 490      1316  LOAD_CONST               7
             1318  STORE_DEREF              'dayOffset'

 L. 491      1320  LOAD_FAST                'start'
             1322  LOAD_CONST               1
             1324  INPLACE_SUBTRACT 
             1326  STORE_FAST               'start'

 L. 492      1328  LOAD_CONST               2
             1330  STORE_FAST               'used'
         1332_1334  JUMP_BACK          1302  'to 1302'
             1336  POP_BLOCK        
           1338_0  COME_FROM_LOOP     1296  '1296'

 L. 493      1338  SETUP_LOOP         1380  'to 1380'
             1340  LOAD_FAST                'suffix_lasts'
             1342  GET_ITER         
           1344_0  COME_FROM          1354  '1354'
             1344  FOR_ITER           1378  'to 1378'
             1346  STORE_FAST               'w'

 L. 494      1348  LOAD_FAST                'wordNext'
             1350  LOAD_FAST                'w'
             1352  COMPARE_OP               ==
         1354_1356  POP_JUMP_IF_FALSE  1344  'to 1344'

 L. 495      1358  LOAD_CONST               -7
             1360  STORE_DEREF              'dayOffset'

 L. 496      1362  LOAD_FAST                'start'
             1364  LOAD_CONST               1
             1366  INPLACE_SUBTRACT 
             1368  STORE_FAST               'start'

 L. 497      1370  LOAD_CONST               2
             1372  STORE_FAST               'used'
         1374_1376  JUMP_BACK          1344  'to 1344'
             1378  POP_BLOCK        
           1380_0  COME_FROM_LOOP     1338  '1338'
         1380_1382  JUMP_FORWARD       2486  'to 2486'
           1384_0  COME_FROM          1166  '1166'
           1384_1  COME_FROM          1160  '1160'

 L. 499      1384  LOAD_FAST                'word'
             1386  LOAD_STR                 'mes'
             1388  COMPARE_OP               ==
         1390_1392  POP_JUMP_IF_FALSE  1606  'to 1606'
             1394  LOAD_FAST                'fromFlag'
         1396_1398  POP_JUMP_IF_TRUE   1606  'to 1606'

 L. 500      1400  LOAD_FAST                'wordPrev'
             1402  LOAD_CONST               0
             1404  BINARY_SUBSCR    
             1406  LOAD_METHOD              isdigit
             1408  CALL_METHOD_0         0  '0 positional arguments'
         1410_1412  POP_JUMP_IF_FALSE  1434  'to 1434'

 L. 501      1414  LOAD_GLOBAL              int
             1416  LOAD_FAST                'wordPrev'
             1418  CALL_FUNCTION_1       1  '1 positional argument'
             1420  STORE_DEREF              'monthOffset'

 L. 502      1422  LOAD_FAST                'start'
             1424  LOAD_CONST               1
             1426  INPLACE_SUBTRACT 
             1428  STORE_FAST               'start'

 L. 503      1430  LOAD_CONST               2
             1432  STORE_FAST               'used'
           1434_0  COME_FROM          1410  '1410'

 L. 504      1434  SETUP_LOOP         1476  'to 1476'
             1436  LOAD_FAST                'nexts'
             1438  GET_ITER         
           1440_0  COME_FROM          1450  '1450'
             1440  FOR_ITER           1474  'to 1474'
             1442  STORE_FAST               'w'

 L. 505      1444  LOAD_FAST                'wordPrev'
             1446  LOAD_FAST                'w'
             1448  COMPARE_OP               ==
         1450_1452  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 506      1454  LOAD_CONST               7
             1456  STORE_DEREF              'monthOffset'

 L. 507      1458  LOAD_FAST                'start'
             1460  LOAD_CONST               1
             1462  INPLACE_SUBTRACT 
             1464  STORE_FAST               'start'

 L. 508      1466  LOAD_CONST               2
             1468  STORE_FAST               'used'
         1470_1472  JUMP_BACK          1440  'to 1440'
             1474  POP_BLOCK        
           1476_0  COME_FROM_LOOP     1434  '1434'

 L. 509      1476  SETUP_LOOP         1518  'to 1518'
             1478  LOAD_FAST                'lasts'
             1480  GET_ITER         
           1482_0  COME_FROM          1492  '1492'
             1482  FOR_ITER           1516  'to 1516'
             1484  STORE_FAST               'w'

 L. 510      1486  LOAD_FAST                'wordPrev'
             1488  LOAD_FAST                'w'
             1490  COMPARE_OP               ==
         1492_1494  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 511      1496  LOAD_CONST               -7
             1498  STORE_DEREF              'monthOffset'

 L. 512      1500  LOAD_FAST                'start'
             1502  LOAD_CONST               1
             1504  INPLACE_SUBTRACT 
             1506  STORE_FAST               'start'

 L. 513      1508  LOAD_CONST               2
             1510  STORE_FAST               'used'
         1512_1514  JUMP_BACK          1482  'to 1482'
             1516  POP_BLOCK        
           1518_0  COME_FROM_LOOP     1476  '1476'

 L. 514      1518  SETUP_LOOP         1560  'to 1560'
             1520  LOAD_FAST                'suffix_nexts'
             1522  GET_ITER         
           1524_0  COME_FROM          1534  '1534'
             1524  FOR_ITER           1558  'to 1558'
             1526  STORE_FAST               'w'

 L. 515      1528  LOAD_FAST                'wordNext'
             1530  LOAD_FAST                'w'
             1532  COMPARE_OP               ==
         1534_1536  POP_JUMP_IF_FALSE  1524  'to 1524'

 L. 516      1538  LOAD_CONST               7
             1540  STORE_DEREF              'monthOffset'

 L. 517      1542  LOAD_FAST                'start'
             1544  LOAD_CONST               1
             1546  INPLACE_SUBTRACT 
             1548  STORE_FAST               'start'

 L. 518      1550  LOAD_CONST               2
             1552  STORE_FAST               'used'
         1554_1556  JUMP_BACK          1524  'to 1524'
             1558  POP_BLOCK        
           1560_0  COME_FROM_LOOP     1518  '1518'

 L. 519      1560  SETUP_LOOP         1602  'to 1602'
             1562  LOAD_FAST                'suffix_lasts'
             1564  GET_ITER         
           1566_0  COME_FROM          1576  '1576'
             1566  FOR_ITER           1600  'to 1600'
             1568  STORE_FAST               'w'

 L. 520      1570  LOAD_FAST                'wordNext'
             1572  LOAD_FAST                'w'
             1574  COMPARE_OP               ==
         1576_1578  POP_JUMP_IF_FALSE  1566  'to 1566'

 L. 521      1580  LOAD_CONST               -7
             1582  STORE_DEREF              'monthOffset'

 L. 522      1584  LOAD_FAST                'start'
             1586  LOAD_CONST               1
             1588  INPLACE_SUBTRACT 
             1590  STORE_FAST               'start'

 L. 523      1592  LOAD_CONST               2
             1594  STORE_FAST               'used'
         1596_1598  JUMP_BACK          1566  'to 1566'
             1600  POP_BLOCK        
           1602_0  COME_FROM_LOOP     1560  '1560'
         1602_1604  JUMP_FORWARD       2486  'to 2486'
           1606_0  COME_FROM          1396  '1396'
           1606_1  COME_FROM          1390  '1390'

 L. 525      1606  LOAD_FAST                'word'
             1608  LOAD_STR                 'año'
             1610  COMPARE_OP               ==
         1612_1614  POP_JUMP_IF_FALSE  1828  'to 1828'
             1616  LOAD_FAST                'fromFlag'
         1618_1620  POP_JUMP_IF_TRUE   1828  'to 1828'

 L. 526      1622  LOAD_FAST                'wordPrev'
             1624  LOAD_CONST               0
             1626  BINARY_SUBSCR    
             1628  LOAD_METHOD              isdigit
             1630  CALL_METHOD_0         0  '0 positional arguments'
         1632_1634  POP_JUMP_IF_FALSE  1656  'to 1656'

 L. 527      1636  LOAD_GLOBAL              int
             1638  LOAD_FAST                'wordPrev'
             1640  CALL_FUNCTION_1       1  '1 positional argument'
             1642  STORE_DEREF              'yearOffset'

 L. 528      1644  LOAD_FAST                'start'
             1646  LOAD_CONST               1
             1648  INPLACE_SUBTRACT 
             1650  STORE_FAST               'start'

 L. 529      1652  LOAD_CONST               2
             1654  STORE_FAST               'used'
           1656_0  COME_FROM          1632  '1632'

 L. 530      1656  SETUP_LOOP         1698  'to 1698'
             1658  LOAD_FAST                'nexts'
             1660  GET_ITER         
           1662_0  COME_FROM          1672  '1672'
             1662  FOR_ITER           1696  'to 1696'
             1664  STORE_FAST               'w'

 L. 531      1666  LOAD_FAST                'wordPrev'
             1668  LOAD_FAST                'w'
             1670  COMPARE_OP               ==
         1672_1674  POP_JUMP_IF_FALSE  1662  'to 1662'

 L. 532      1676  LOAD_CONST               7
             1678  STORE_DEREF              'yearOffset'

 L. 533      1680  LOAD_FAST                'start'
             1682  LOAD_CONST               1
             1684  INPLACE_SUBTRACT 
             1686  STORE_FAST               'start'

 L. 534      1688  LOAD_CONST               2
             1690  STORE_FAST               'used'
         1692_1694  JUMP_BACK          1662  'to 1662'
             1696  POP_BLOCK        
           1698_0  COME_FROM_LOOP     1656  '1656'

 L. 535      1698  SETUP_LOOP         1740  'to 1740'
             1700  LOAD_FAST                'lasts'
             1702  GET_ITER         
           1704_0  COME_FROM          1714  '1714'
             1704  FOR_ITER           1738  'to 1738'
             1706  STORE_FAST               'w'

 L. 536      1708  LOAD_FAST                'wordPrev'
             1710  LOAD_FAST                'w'
             1712  COMPARE_OP               ==
         1714_1716  POP_JUMP_IF_FALSE  1704  'to 1704'

 L. 537      1718  LOAD_CONST               -7
             1720  STORE_DEREF              'yearOffset'

 L. 538      1722  LOAD_FAST                'start'
             1724  LOAD_CONST               1
             1726  INPLACE_SUBTRACT 
             1728  STORE_FAST               'start'

 L. 539      1730  LOAD_CONST               2
             1732  STORE_FAST               'used'
         1734_1736  JUMP_BACK          1704  'to 1704'
             1738  POP_BLOCK        
           1740_0  COME_FROM_LOOP     1698  '1698'

 L. 540      1740  SETUP_LOOP         1782  'to 1782'
             1742  LOAD_FAST                'suffix_nexts'
             1744  GET_ITER         
           1746_0  COME_FROM          1756  '1756'
             1746  FOR_ITER           1780  'to 1780'
             1748  STORE_FAST               'w'

 L. 541      1750  LOAD_FAST                'wordNext'
             1752  LOAD_FAST                'w'
             1754  COMPARE_OP               ==
         1756_1758  POP_JUMP_IF_FALSE  1746  'to 1746'

 L. 542      1760  LOAD_CONST               7
             1762  STORE_DEREF              'yearOffset'

 L. 543      1764  LOAD_FAST                'start'
             1766  LOAD_CONST               1
             1768  INPLACE_SUBTRACT 
             1770  STORE_FAST               'start'

 L. 544      1772  LOAD_CONST               2
             1774  STORE_FAST               'used'
         1776_1778  JUMP_BACK          1746  'to 1746'
             1780  POP_BLOCK        
           1782_0  COME_FROM_LOOP     1740  '1740'

 L. 545      1782  SETUP_LOOP         1824  'to 1824'
             1784  LOAD_FAST                'suffix_lasts'
             1786  GET_ITER         
           1788_0  COME_FROM          1798  '1798'
             1788  FOR_ITER           1822  'to 1822'
             1790  STORE_FAST               'w'

 L. 546      1792  LOAD_FAST                'wordNext'
             1794  LOAD_FAST                'w'
             1796  COMPARE_OP               ==
         1798_1800  POP_JUMP_IF_FALSE  1788  'to 1788'

 L. 547      1802  LOAD_CONST               -7
             1804  STORE_DEREF              'yearOffset'

 L. 548      1806  LOAD_FAST                'start'
             1808  LOAD_CONST               1
             1810  INPLACE_SUBTRACT 
             1812  STORE_FAST               'start'

 L. 549      1814  LOAD_CONST               2
             1816  STORE_FAST               'used'
         1818_1820  JUMP_BACK          1788  'to 1788'
             1822  POP_BLOCK        
           1824_0  COME_FROM_LOOP     1782  '1782'
         1824_1826  JUMP_FORWARD       2486  'to 2486'
           1828_0  COME_FROM          1618  '1618'
           1828_1  COME_FROM          1612  '1612'

 L. 552      1828  LOAD_FAST                'word'
             1830  LOAD_FAST                'days'
             1832  COMPARE_OP               in
         1834_1836  POP_JUMP_IF_FALSE  2004  'to 2004'
             1838  LOAD_FAST                'fromFlag'
         1840_1842  POP_JUMP_IF_TRUE   2004  'to 2004'

 L. 553      1844  LOAD_FAST                'days'
             1846  LOAD_METHOD              index
             1848  LOAD_FAST                'word'
             1850  CALL_METHOD_1         1  '1 positional argument'
             1852  STORE_FAST               'd'

 L. 554      1854  LOAD_FAST                'd'
             1856  LOAD_CONST               1
             1858  BINARY_ADD       
             1860  LOAD_GLOBAL              int
             1862  LOAD_FAST                'today'
             1864  CALL_FUNCTION_1       1  '1 positional argument'
             1866  BINARY_SUBTRACT  
             1868  STORE_DEREF              'dayOffset'

 L. 555      1870  LOAD_CONST               1
             1872  STORE_FAST               'used'

 L. 556      1874  LOAD_DEREF               'dayOffset'
             1876  LOAD_CONST               0
             1878  COMPARE_OP               <
         1880_1882  POP_JUMP_IF_FALSE  1892  'to 1892'

 L. 557      1884  LOAD_DEREF               'dayOffset'
             1886  LOAD_CONST               7
             1888  INPLACE_ADD      
             1890  STORE_DEREF              'dayOffset'
           1892_0  COME_FROM          1880  '1880'

 L. 558      1892  LOAD_FAST                'wordPrev'
             1894  LOAD_STR                 'siguiente'
             1896  COMPARE_OP               ==
         1898_1900  POP_JUMP_IF_FALSE  1928  'to 1928'

 L. 559      1902  LOAD_DEREF               'dayOffset'
             1904  LOAD_CONST               7
             1906  INPLACE_ADD      
             1908  STORE_DEREF              'dayOffset'

 L. 560      1910  LOAD_FAST                'used'
             1912  LOAD_CONST               1
             1914  INPLACE_ADD      
             1916  STORE_FAST               'used'

 L. 561      1918  LOAD_FAST                'start'
             1920  LOAD_CONST               1
             1922  INPLACE_SUBTRACT 
             1924  STORE_FAST               'start'
             1926  JUMP_FORWARD       1962  'to 1962'
           1928_0  COME_FROM          1898  '1898'

 L. 562      1928  LOAD_FAST                'wordPrev'
             1930  LOAD_STR                 'pasado'
             1932  COMPARE_OP               ==
         1934_1936  POP_JUMP_IF_FALSE  1962  'to 1962'

 L. 563      1938  LOAD_DEREF               'dayOffset'
             1940  LOAD_CONST               7
             1942  INPLACE_SUBTRACT 
             1944  STORE_DEREF              'dayOffset'

 L. 564      1946  LOAD_FAST                'used'
             1948  LOAD_CONST               1
             1950  INPLACE_ADD      
             1952  STORE_FAST               'used'

 L. 565      1954  LOAD_FAST                'start'
             1956  LOAD_CONST               1
             1958  INPLACE_SUBTRACT 
             1960  STORE_FAST               'start'
           1962_0  COME_FROM          1934  '1934'
           1962_1  COME_FROM          1926  '1926'

 L. 566      1962  LOAD_FAST                'wordNext'
             1964  LOAD_STR                 'siguiente'
             1966  COMPARE_OP               ==
         1968_1970  POP_JUMP_IF_FALSE  1982  'to 1982'

 L. 568      1972  LOAD_FAST                'used'
             1974  LOAD_CONST               1
             1976  INPLACE_ADD      
             1978  STORE_FAST               'used'
             1980  JUMP_FORWARD       2486  'to 2486'
           1982_0  COME_FROM          1968  '1968'

 L. 569      1982  LOAD_FAST                'wordNext'
             1984  LOAD_STR                 'pasado'
             1986  COMPARE_OP               ==
         1988_1990  POP_JUMP_IF_FALSE  2486  'to 2486'

 L. 571      1992  LOAD_FAST                'used'
             1994  LOAD_CONST               1
             1996  INPLACE_ADD      
             1998  STORE_FAST               'used'
         2000_2002  JUMP_FORWARD       2486  'to 2486'
           2004_0  COME_FROM          1840  '1840'
           2004_1  COME_FROM          1834  '1834'

 L. 573      2004  LOAD_FAST                'word'
             2006  LOAD_FAST                'months'
             2008  COMPARE_OP               in
         2010_2012  POP_JUMP_IF_TRUE   2024  'to 2024'
             2014  LOAD_FAST                'word'
             2016  LOAD_FAST                'monthsShort'
             2018  COMPARE_OP               in
         2020_2022  POP_JUMP_IF_FALSE  2486  'to 2486'
           2024_0  COME_FROM          2010  '2010'

 L. 574      2024  SETUP_EXCEPT       2040  'to 2040'

 L. 575      2026  LOAD_FAST                'months'
             2028  LOAD_METHOD              index
             2030  LOAD_FAST                'word'
             2032  CALL_METHOD_1         1  '1 positional argument'
             2034  STORE_FAST               'm'
             2036  POP_BLOCK        
             2038  JUMP_FORWARD       2072  'to 2072'
           2040_0  COME_FROM_EXCEPT   2024  '2024'

 L. 576      2040  DUP_TOP          
             2042  LOAD_GLOBAL              ValueError
             2044  COMPARE_OP               exception-match
         2046_2048  POP_JUMP_IF_FALSE  2070  'to 2070'
             2050  POP_TOP          
             2052  POP_TOP          
             2054  POP_TOP          

 L. 577      2056  LOAD_FAST                'monthsShort'
             2058  LOAD_METHOD              index
             2060  LOAD_FAST                'word'
             2062  CALL_METHOD_1         1  '1 positional argument'
             2064  STORE_FAST               'm'
             2066  POP_EXCEPT       
             2068  JUMP_FORWARD       2072  'to 2072'
           2070_0  COME_FROM          2046  '2046'
             2070  END_FINALLY      
           2072_0  COME_FROM          2068  '2068'
           2072_1  COME_FROM          2038  '2038'

 L. 578      2072  LOAD_FAST                'used'
             2074  LOAD_CONST               1
             2076  INPLACE_ADD      
             2078  STORE_FAST               'used'

 L. 579      2080  LOAD_FAST                'months'
             2082  LOAD_FAST                'm'
             2084  BINARY_SUBSCR    
             2086  STORE_DEREF              'datestr'

 L. 580      2088  LOAD_FAST                'wordPrev'
         2090_2092  POP_JUMP_IF_FALSE  2190  'to 2190'
             2094  LOAD_FAST                'wordPrev'
             2096  LOAD_CONST               0
             2098  BINARY_SUBSCR    
             2100  LOAD_METHOD              isdigit
             2102  CALL_METHOD_0         0  '0 positional arguments'
         2104_2106  POP_JUMP_IF_FALSE  2190  'to 2190'

 L. 582      2108  LOAD_DEREF               'datestr'
             2110  LOAD_STR                 ' '
             2112  LOAD_FAST                'wordPrev'
             2114  BINARY_ADD       
             2116  INPLACE_ADD      
             2118  STORE_DEREF              'datestr'

 L. 583      2120  LOAD_FAST                'start'
             2122  LOAD_CONST               1
             2124  INPLACE_SUBTRACT 
             2126  STORE_FAST               'start'

 L. 584      2128  LOAD_FAST                'used'
             2130  LOAD_CONST               1
             2132  INPLACE_ADD      
             2134  STORE_FAST               'used'

 L. 585      2136  LOAD_FAST                'wordNext'
         2138_2140  POP_JUMP_IF_FALSE  2182  'to 2182'
             2142  LOAD_FAST                'wordNext'
             2144  LOAD_CONST               0
             2146  BINARY_SUBSCR    
             2148  LOAD_METHOD              isdigit
             2150  CALL_METHOD_0         0  '0 positional arguments'
         2152_2154  POP_JUMP_IF_FALSE  2182  'to 2182'

 L. 586      2156  LOAD_DEREF               'datestr'
             2158  LOAD_STR                 ' '
             2160  LOAD_FAST                'wordNext'
             2162  BINARY_ADD       
             2164  INPLACE_ADD      
             2166  STORE_DEREF              'datestr'

 L. 587      2168  LOAD_FAST                'used'
             2170  LOAD_CONST               1
             2172  INPLACE_ADD      
             2174  STORE_FAST               'used'

 L. 588      2176  LOAD_CONST               True
             2178  STORE_FAST               'hasYear'
             2180  JUMP_FORWARD       2472  'to 2472'
           2182_0  COME_FROM          2152  '2152'
           2182_1  COME_FROM          2138  '2138'

 L. 590      2182  LOAD_CONST               False
             2184  STORE_FAST               'hasYear'
         2186_2188  JUMP_FORWARD       2472  'to 2472'
           2190_0  COME_FROM          2104  '2104'
           2190_1  COME_FROM          2090  '2090'

 L. 592      2190  LOAD_FAST                'wordNext'
         2192_2194  POP_JUMP_IF_FALSE  2282  'to 2282'
             2196  LOAD_FAST                'wordNext'
             2198  LOAD_CONST               0
             2200  BINARY_SUBSCR    
             2202  LOAD_METHOD              isdigit
             2204  CALL_METHOD_0         0  '0 positional arguments'
         2206_2208  POP_JUMP_IF_FALSE  2282  'to 2282'

 L. 594      2210  LOAD_DEREF               'datestr'
             2212  LOAD_STR                 ' '
             2214  LOAD_FAST                'wordNext'
             2216  BINARY_ADD       
             2218  INPLACE_ADD      
             2220  STORE_DEREF              'datestr'

 L. 595      2222  LOAD_FAST                'used'
             2224  LOAD_CONST               1
             2226  INPLACE_ADD      
             2228  STORE_FAST               'used'

 L. 596      2230  LOAD_FAST                'wordNextNext'
         2232_2234  POP_JUMP_IF_FALSE  2276  'to 2276'
             2236  LOAD_FAST                'wordNextNext'
             2238  LOAD_CONST               0
             2240  BINARY_SUBSCR    
             2242  LOAD_METHOD              isdigit
             2244  CALL_METHOD_0         0  '0 positional arguments'
         2246_2248  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 597      2250  LOAD_DEREF               'datestr'
             2252  LOAD_STR                 ' '
             2254  LOAD_FAST                'wordNextNext'
             2256  BINARY_ADD       
             2258  INPLACE_ADD      
             2260  STORE_DEREF              'datestr'

 L. 598      2262  LOAD_FAST                'used'
             2264  LOAD_CONST               1
             2266  INPLACE_ADD      
             2268  STORE_FAST               'used'

 L. 599      2270  LOAD_CONST               True
             2272  STORE_FAST               'hasYear'
             2274  JUMP_FORWARD       2280  'to 2280'
           2276_0  COME_FROM          2246  '2246'
           2276_1  COME_FROM          2232  '2232'

 L. 601      2276  LOAD_CONST               False
             2278  STORE_FAST               'hasYear'
           2280_0  COME_FROM          2274  '2274'
             2280  JUMP_FORWARD       2472  'to 2472'
           2282_0  COME_FROM          2206  '2206'
           2282_1  COME_FROM          2192  '2192'

 L. 603      2282  LOAD_FAST                'wordPrevPrev'
         2284_2286  POP_JUMP_IF_FALSE  2382  'to 2382'
             2288  LOAD_FAST                'wordPrevPrev'
             2290  LOAD_CONST               0
             2292  BINARY_SUBSCR    
             2294  LOAD_METHOD              isdigit
             2296  CALL_METHOD_0         0  '0 positional arguments'
         2298_2300  POP_JUMP_IF_FALSE  2382  'to 2382'

 L. 605      2302  LOAD_DEREF               'datestr'
             2304  LOAD_STR                 ' '
             2306  LOAD_FAST                'wordPrevPrev'
             2308  BINARY_ADD       
             2310  INPLACE_ADD      
             2312  STORE_DEREF              'datestr'

 L. 607      2314  LOAD_FAST                'start'
             2316  LOAD_CONST               2
             2318  INPLACE_SUBTRACT 
             2320  STORE_FAST               'start'

 L. 608      2322  LOAD_FAST                'used'
             2324  LOAD_CONST               2
             2326  INPLACE_ADD      
             2328  STORE_FAST               'used'

 L. 609      2330  LOAD_FAST                'wordNext'
         2332_2334  POP_JUMP_IF_FALSE  2376  'to 2376'
             2336  LOAD_FAST                'word'
             2338  LOAD_CONST               0
             2340  BINARY_SUBSCR    
             2342  LOAD_METHOD              isdigit
           2344_0  COME_FROM          1010  '1010'
             2344  CALL_METHOD_0         0  '0 positional arguments'
         2346_2348  POP_JUMP_IF_FALSE  2376  'to 2376'

 L. 610      2350  LOAD_DEREF               'datestr'
             2352  LOAD_STR                 ' '
             2354  LOAD_FAST                'wordNext'
             2356  BINARY_ADD       
             2358  INPLACE_ADD      
             2360  STORE_DEREF              'datestr'

 L. 611      2362  LOAD_FAST                'used'
             2364  LOAD_CONST               1
             2366  INPLACE_ADD      
             2368  STORE_FAST               'used'

 L. 612      2370  LOAD_CONST               True
             2372  STORE_FAST               'hasYear'
             2374  JUMP_FORWARD       2380  'to 2380'
           2376_0  COME_FROM          2346  '2346'
           2376_1  COME_FROM          2332  '2332'

 L. 614      2376  LOAD_CONST               False
             2378  STORE_FAST               'hasYear'
           2380_0  COME_FROM          2374  '2374'
             2380  JUMP_FORWARD       2472  'to 2472'
           2382_0  COME_FROM          2298  '2298'
           2382_1  COME_FROM          2284  '2284'

 L. 616      2382  LOAD_FAST                'wordNextNext'
         2384_2386  POP_JUMP_IF_FALSE  2472  'to 2472'
             2388  LOAD_FAST                'wordNextNext'
             2390  LOAD_CONST               0
             2392  BINARY_SUBSCR    
             2394  LOAD_METHOD              isdigit
             2396  CALL_METHOD_0         0  '0 positional arguments'
         2398_2400  POP_JUMP_IF_FALSE  2472  'to 2472'

 L. 618      2402  LOAD_DEREF               'datestr'
             2404  LOAD_STR                 ' '
             2406  LOAD_FAST                'wordNextNext'
             2408  BINARY_ADD       
             2410  INPLACE_ADD      
             2412  STORE_DEREF              'datestr'
           2414_0  COME_FROM          1080  '1080'

 L. 619      2414  LOAD_FAST                'used'
             2416  LOAD_CONST               2
             2418  INPLACE_ADD      
             2420  STORE_FAST               'used'

 L. 620      2422  LOAD_FAST                'wordNextNextNext'
         2424_2426  POP_JUMP_IF_FALSE  2468  'to 2468'
             2428  LOAD_FAST                'wordNextNextNext'
             2430  LOAD_CONST               0
             2432  BINARY_SUBSCR    
             2434  LOAD_METHOD              isdigit
             2436  CALL_METHOD_0         0  '0 positional arguments'
         2438_2440  POP_JUMP_IF_FALSE  2468  'to 2468'

 L. 621      2442  LOAD_DEREF               'datestr'
             2444  LOAD_STR                 ' '
             2446  LOAD_FAST                'wordNextNextNext'
             2448  BINARY_ADD       
             2450  INPLACE_ADD      
             2452  STORE_DEREF              'datestr'

 L. 622      2454  LOAD_FAST                'used'
             2456  LOAD_CONST               1
             2458  INPLACE_ADD      
             2460  STORE_FAST               'used'

 L. 623      2462  LOAD_CONST               True
           2464_0  COME_FROM          2180  '2180'
           2464_1  COME_FROM          1980  '1980'
             2464  STORE_FAST               'hasYear'
             2466  JUMP_FORWARD       2472  'to 2472'
           2468_0  COME_FROM          2438  '2438'
           2468_1  COME_FROM          2424  '2424'

 L. 625      2468  LOAD_CONST               False
             2470  STORE_FAST               'hasYear'
           2472_0  COME_FROM          2466  '2466'
           2472_1  COME_FROM          2398  '2398'
           2472_2  COME_FROM          2384  '2384'
           2472_3  COME_FROM          2380  '2380'
           2472_4  COME_FROM          2280  '2280'
           2472_5  COME_FROM          2186  '2186'

 L. 627      2472  LOAD_DEREF               'datestr'
             2474  LOAD_FAST                'months'
             2476  COMPARE_OP               in
         2478_2480  POP_JUMP_IF_FALSE  2486  'to 2486'

 L. 628      2482  LOAD_STR                 ''
             2484  STORE_DEREF              'datestr'
           2486_0  COME_FROM          2478  '2478'
           2486_1  COME_FROM          2020  '2020'
           2486_2  COME_FROM          2000  '2000'
           2486_3  COME_FROM          1988  '1988'
           2486_4  COME_FROM          1824  '1824'
           2486_5  COME_FROM          1602  '1602'
           2486_6  COME_FROM          1380  '1380'
           2486_7  COME_FROM          1150  '1150'
           2486_8  COME_FROM          1118  '1118'
           2486_9  COME_FROM          1108  '1108'
          2486_10  COME_FROM          1098  '1098'
          2486_11  COME_FROM          1084  '1084'
          2486_12  COME_FROM           920  '920'
          2486_13  COME_FROM           878  '878'
          2486_14  COME_FROM           836  '836'
          2486_15  COME_FROM           800  '800'
          2486_16  COME_FROM           744  '744'
          2486_17  COME_FROM           732  '732'
          2486_18  COME_FROM           670  '670'
          2486_19  COME_FROM           634  '634'
          2486_20  COME_FROM           602  '602'
          2486_21  COME_FROM           570  '570'

 L. 632      2486  LOAD_FAST                'days'
             2488  LOAD_FAST                'months'
             2490  BINARY_ADD       
             2492  LOAD_FAST                'monthsShort'
             2494  BINARY_ADD       
             2496  STORE_FAST               'validFollowups'

 L. 633      2498  LOAD_FAST                'validFollowups'
             2500  LOAD_METHOD              append
             2502  LOAD_STR                 'hoy'
             2504  CALL_METHOD_1         1  '1 positional argument'
             2506  POP_TOP          

 L. 634      2508  LOAD_FAST                'validFollowups'
             2510  LOAD_METHOD              append
             2512  LOAD_STR                 'mañana'
             2514  CALL_METHOD_1         1  '1 positional argument'
             2516  POP_TOP          

 L. 635      2518  LOAD_FAST                'validFollowups'
             2520  LOAD_METHOD              append
             2522  LOAD_STR                 'ayer'
             2524  CALL_METHOD_1         1  '1 positional argument'
             2526  POP_TOP          

 L. 636      2528  LOAD_FAST                'validFollowups'
             2530  LOAD_METHOD              append
             2532  LOAD_STR                 'anteayer'
             2534  CALL_METHOD_1         1  '1 positional argument'
             2536  POP_TOP          

 L. 637      2538  LOAD_FAST                'validFollowups'
             2540  LOAD_METHOD              append
             2542  LOAD_STR                 'ahora'
             2544  CALL_METHOD_1         1  '1 positional argument'
             2546  POP_TOP          

 L. 638      2548  LOAD_FAST                'validFollowups'
             2550  LOAD_METHOD              append
             2552  LOAD_STR                 'ya'
             2554  CALL_METHOD_1         1  '1 positional argument'
             2556  POP_TOP          

 L. 639      2558  LOAD_FAST                'validFollowups'
             2560  LOAD_METHOD              append
             2562  LOAD_STR                 'ante'
             2564  CALL_METHOD_1         1  '1 positional argument'
             2566  POP_TOP          

 L. 642      2568  LOAD_FAST                'word'
             2570  LOAD_FAST                'froms'
             2572  COMPARE_OP               in
         2574_2576  POP_JUMP_IF_FALSE  3026  'to 3026'
             2578  LOAD_FAST                'wordNext'
             2580  LOAD_FAST                'validFollowups'
             2582  COMPARE_OP               in
         2584_2586  POP_JUMP_IF_FALSE  3026  'to 3026'

 L. 644      2588  LOAD_FAST                'wordNext'
             2590  LOAD_STR                 'mañana'
             2592  COMPARE_OP               ==
         2594_2596  POP_JUMP_IF_FALSE  2608  'to 2608'
             2598  LOAD_FAST                'wordNext'
             2600  LOAD_STR                 'ayer'
             2602  COMPARE_OP               ==
         2604_2606  POP_JUMP_IF_TRUE   2636  'to 2636'
           2608_0  COME_FROM          2594  '2594'

 L. 645      2608  LOAD_FAST                'word'
             2610  LOAD_STR                 'pasado'
             2612  COMPARE_OP               ==
         2614_2616  POP_JUMP_IF_TRUE   2636  'to 2636'
             2618  LOAD_FAST                'word'
             2620  LOAD_STR                 'antes'
             2622  COMPARE_OP               ==
         2624_2626  POP_JUMP_IF_TRUE   2636  'to 2636'

 L. 646      2628  LOAD_CONST               2
             2630  STORE_FAST               'used'

 L. 647      2632  LOAD_CONST               True
             2634  STORE_FAST               'fromFlag'
           2636_0  COME_FROM          2624  '2624'
           2636_1  COME_FROM          2614  '2614'
           2636_2  COME_FROM          2604  '2604'

 L. 648      2636  LOAD_FAST                'wordNext'
             2638  LOAD_STR                 'mañana'
             2640  COMPARE_OP               ==
         2642_2644  POP_JUMP_IF_FALSE  2668  'to 2668'
             2646  LOAD_FAST                'word'
             2648  LOAD_STR                 'pasado'
             2650  COMPARE_OP               !=
         2652_2654  POP_JUMP_IF_FALSE  2668  'to 2668'

 L. 649      2656  LOAD_DEREF               'dayOffset'
             2658  LOAD_CONST               1
             2660  INPLACE_ADD      
             2662  STORE_DEREF              'dayOffset'
         2664_2666  JUMP_FORWARD       3026  'to 3026'
           2668_0  COME_FROM          2652  '2652'
           2668_1  COME_FROM          2642  '2642'

 L. 650      2668  LOAD_FAST                'wordNext'
             2670  LOAD_STR                 'ayer'
             2672  COMPARE_OP               ==
         2674_2676  POP_JUMP_IF_FALSE  2690  'to 2690'

 L. 651      2678  LOAD_DEREF               'dayOffset'
             2680  LOAD_CONST               1
             2682  INPLACE_SUBTRACT 
             2684  STORE_DEREF              'dayOffset'
         2686_2688  JUMP_FORWARD       3026  'to 3026'
           2690_0  COME_FROM          2674  '2674'

 L. 652      2690  LOAD_FAST                'wordNext'
             2692  LOAD_STR                 'anteayer'
             2694  COMPARE_OP               ==
         2696_2698  POP_JUMP_IF_FALSE  2712  'to 2712'

 L. 653      2700  LOAD_DEREF               'dayOffset'
             2702  LOAD_CONST               2
             2704  INPLACE_SUBTRACT 
             2706  STORE_DEREF              'dayOffset'
         2708_2710  JUMP_FORWARD       3026  'to 3026'
           2712_0  COME_FROM          2696  '2696'

 L. 654      2712  LOAD_FAST                'wordNext'
             2714  LOAD_STR                 'ante'
             2716  COMPARE_OP               ==
         2718_2720  POP_JUMP_IF_FALSE  2744  'to 2744'
             2722  LOAD_FAST                'wordNextNext'
             2724  LOAD_STR                 'ayer'
             2726  COMPARE_OP               ==
         2728_2730  POP_JUMP_IF_FALSE  2744  'to 2744'

 L. 655      2732  LOAD_DEREF               'dayOffset'
             2734  LOAD_CONST               2
             2736  INPLACE_SUBTRACT 
             2738  STORE_DEREF              'dayOffset'
         2740_2742  JUMP_FORWARD       3026  'to 3026'
           2744_0  COME_FROM          2728  '2728'
           2744_1  COME_FROM          2718  '2718'

 L. 656      2744  LOAD_FAST                'wordNext'
             2746  LOAD_STR                 'ante'
             2748  COMPARE_OP               ==
         2750_2752  POP_JUMP_IF_FALSE  2784  'to 2784'
             2754  LOAD_FAST                'wordNext'
             2756  LOAD_STR                 'ante'
             2758  COMPARE_OP               ==
         2760_2762  POP_JUMP_IF_FALSE  2784  'to 2784'

 L. 657      2764  LOAD_FAST                'wordNextNextNext'
             2766  LOAD_STR                 'ayer'
             2768  COMPARE_OP               ==
         2770_2772  POP_JUMP_IF_FALSE  2784  'to 2784'

 L. 658      2774  LOAD_DEREF               'dayOffset'
             2776  LOAD_CONST               3
             2778  INPLACE_SUBTRACT 
             2780  STORE_DEREF              'dayOffset'
             2782  JUMP_FORWARD       3026  'to 3026'
           2784_0  COME_FROM          2770  '2770'
           2784_1  COME_FROM          2760  '2760'
           2784_2  COME_FROM          2750  '2750'

 L. 659      2784  LOAD_FAST                'wordNext'
             2786  LOAD_FAST                'days'
             2788  COMPARE_OP               in
         2790_2792  POP_JUMP_IF_FALSE  2912  'to 2912'

 L. 660      2794  LOAD_FAST                'days'
             2796  LOAD_METHOD              index
             2798  LOAD_FAST                'wordNext'
             2800  CALL_METHOD_1         1  '1 positional argument'
             2802  STORE_FAST               'd'

 L. 661      2804  LOAD_FAST                'd'
             2806  LOAD_CONST               1
             2808  BINARY_ADD       
             2810  LOAD_GLOBAL              int
             2812  LOAD_FAST                'today'
             2814  CALL_FUNCTION_1       1  '1 positional argument'
             2816  BINARY_SUBTRACT  
             2818  STORE_FAST               'tmpOffset'

 L. 662      2820  LOAD_CONST               2
             2822  STORE_FAST               'used'

 L. 665      2824  LOAD_FAST                'tmpOffset'
             2826  LOAD_CONST               0
             2828  COMPARE_OP               <
         2830_2832  POP_JUMP_IF_FALSE  2842  'to 2842'

 L. 666      2834  LOAD_FAST                'tmpOffset'
             2836  LOAD_CONST               7
             2838  INPLACE_ADD      
             2840  STORE_FAST               'tmpOffset'
           2842_0  COME_FROM          2830  '2830'

 L. 667      2842  LOAD_FAST                'wordNextNext'
         2844_2846  POP_JUMP_IF_FALSE  2902  'to 2902'

 L. 668      2848  LOAD_FAST                'wordNextNext'
             2850  LOAD_FAST                'nxts'
             2852  COMPARE_OP               in
         2854_2856  POP_JUMP_IF_FALSE  2876  'to 2876'

 L. 669      2858  LOAD_FAST                'tmpOffset'
             2860  LOAD_CONST               7
             2862  INPLACE_ADD      
             2864  STORE_FAST               'tmpOffset'

 L. 670      2866  LOAD_FAST                'used'
             2868  LOAD_CONST               1
             2870  INPLACE_ADD      
             2872  STORE_FAST               'used'
             2874  JUMP_FORWARD       2902  'to 2902'
           2876_0  COME_FROM          2854  '2854'

 L. 671      2876  LOAD_FAST                'wordNextNext'
             2878  LOAD_FAST                'prevs'
             2880  COMPARE_OP               in
         2882_2884  POP_JUMP_IF_FALSE  2902  'to 2902'

 L. 672      2886  LOAD_FAST                'tmpOffset'
             2888  LOAD_CONST               7
             2890  INPLACE_SUBTRACT 
             2892  STORE_FAST               'tmpOffset'

 L. 673      2894  LOAD_FAST                'used'
             2896  LOAD_CONST               1
             2898  INPLACE_ADD      
             2900  STORE_FAST               'used'
           2902_0  COME_FROM          2882  '2882'
           2902_1  COME_FROM          2874  '2874'
           2902_2  COME_FROM          2844  '2844'

 L. 674      2902  LOAD_DEREF               'dayOffset'
             2904  LOAD_FAST                'tmpOffset'
             2906  INPLACE_ADD      
             2908  STORE_DEREF              'dayOffset'
             2910  JUMP_FORWARD       3026  'to 3026'
           2912_0  COME_FROM          2790  '2790'

 L. 675      2912  LOAD_FAST                'wordNextNext'
         2914_2916  POP_JUMP_IF_FALSE  3026  'to 3026'
             2918  LOAD_FAST                'wordNextNext'
             2920  LOAD_FAST                'days'
             2922  COMPARE_OP               in
         2924_2926  POP_JUMP_IF_FALSE  3026  'to 3026'

 L. 676      2928  LOAD_FAST                'days'
             2930  LOAD_METHOD              index
             2932  LOAD_FAST                'wordNextNext'
             2934  CALL_METHOD_1         1  '1 positional argument'
             2936  STORE_FAST               'd'

 L. 677      2938  LOAD_FAST                'd'
             2940  LOAD_CONST               1
             2942  BINARY_ADD       
             2944  LOAD_GLOBAL              int
             2946  LOAD_FAST                'today'
             2948  CALL_FUNCTION_1       1  '1 positional argument'
             2950  BINARY_SUBTRACT  
             2952  STORE_FAST               'tmpOffset'

 L. 678      2954  LOAD_CONST               3
             2956  STORE_FAST               'used'

 L. 679      2958  LOAD_FAST                'wordNextNextNext'
         2960_2962  POP_JUMP_IF_FALSE  3018  'to 3018'

 L. 680      2964  LOAD_FAST                'wordNextNextNext'
             2966  LOAD_FAST                'nxts'
             2968  COMPARE_OP               in
         2970_2972  POP_JUMP_IF_FALSE  2992  'to 2992'

 L. 681      2974  LOAD_FAST                'tmpOffset'
             2976  LOAD_CONST               7
             2978  INPLACE_ADD      
             2980  STORE_FAST               'tmpOffset'

 L. 682      2982  LOAD_FAST                'used'
             2984  LOAD_CONST               1
             2986  INPLACE_ADD      
             2988  STORE_FAST               'used'
             2990  JUMP_FORWARD       3018  'to 3018'
           2992_0  COME_FROM          2970  '2970'

 L. 683      2992  LOAD_FAST                'wordNextNextNext'
             2994  LOAD_FAST                'prevs'
             2996  COMPARE_OP               in
         2998_3000  POP_JUMP_IF_FALSE  3018  'to 3018'

 L. 684      3002  LOAD_FAST                'tmpOffset'
             3004  LOAD_CONST               7
             3006  INPLACE_SUBTRACT 
             3008  STORE_FAST               'tmpOffset'

 L. 685      3010  LOAD_FAST                'used'
             3012  LOAD_CONST               1
             3014  INPLACE_ADD      
             3016  STORE_FAST               'used'
           3018_0  COME_FROM          2998  '2998'
           3018_1  COME_FROM          2990  '2990'
           3018_2  COME_FROM          2960  '2960'

 L. 686      3018  LOAD_DEREF               'dayOffset'
             3020  LOAD_FAST                'tmpOffset'
             3022  INPLACE_ADD      
             3024  STORE_DEREF              'dayOffset'
           3026_0  COME_FROM          2924  '2924'
           3026_1  COME_FROM          2914  '2914'
           3026_2  COME_FROM          2910  '2910'
           3026_3  COME_FROM          2782  '2782'
           3026_4  COME_FROM          2740  '2740'
           3026_5  COME_FROM          2708  '2708'
           3026_6  COME_FROM          2686  '2686'
           3026_7  COME_FROM          2664  '2664'
           3026_8  COME_FROM          2584  '2584'
           3026_9  COME_FROM          2574  '2574'

 L. 689      3026  LOAD_FAST                'wordNext'
             3028  LOAD_FAST                'months'
             3030  COMPARE_OP               in
         3032_3034  POP_JUMP_IF_FALSE  3044  'to 3044'

 L. 690      3036  LOAD_FAST                'used'
             3038  LOAD_CONST               1
             3040  INPLACE_SUBTRACT 
             3042  STORE_FAST               'used'
           3044_0  COME_FROM          3032  '3032'

 L. 691      3044  LOAD_FAST                'used'
             3046  LOAD_CONST               0
             3048  COMPARE_OP               >
         3050_3052  POP_JUMP_IF_FALSE   370  'to 370'

 L. 692      3054  LOAD_FAST                'start'
             3056  LOAD_CONST               1
             3058  BINARY_SUBTRACT  
             3060  LOAD_CONST               0
             3062  COMPARE_OP               >
         3064_3066  POP_JUMP_IF_FALSE  3102  'to 3102'
             3068  LOAD_FAST                'words'
             3070  LOAD_FAST                'start'
             3072  LOAD_CONST               1
             3074  BINARY_SUBTRACT  
             3076  BINARY_SUBSCR    
             3078  LOAD_FAST                'lists'
             3080  COMPARE_OP               in
         3082_3084  POP_JUMP_IF_FALSE  3102  'to 3102'

 L. 693      3086  LOAD_FAST                'start'
             3088  LOAD_CONST               1
             3090  INPLACE_SUBTRACT 
             3092  STORE_FAST               'start'

 L. 694      3094  LOAD_FAST                'used'
             3096  LOAD_CONST               1
             3098  INPLACE_ADD      
             3100  STORE_FAST               'used'
           3102_0  COME_FROM          3082  '3082'
           3102_1  COME_FROM          3064  '3064'

 L. 696      3102  SETUP_LOOP         3136  'to 3136'
             3104  LOAD_GLOBAL              range
             3106  LOAD_CONST               0
             3108  LOAD_FAST                'used'
             3110  CALL_FUNCTION_2       2  '2 positional arguments'
             3112  GET_ITER         
             3114  FOR_ITER           3134  'to 3134'
             3116  STORE_FAST               'i'

 L. 697      3118  LOAD_STR                 ''
             3120  LOAD_FAST                'words'
             3122  LOAD_FAST                'i'
             3124  LOAD_FAST                'start'
             3126  BINARY_ADD       
             3128  STORE_SUBSCR     
         3130_3132  JUMP_BACK          3114  'to 3114'
             3134  POP_BLOCK        
           3136_0  COME_FROM_LOOP     3102  '3102'

 L. 699      3136  LOAD_FAST                'start'
             3138  LOAD_CONST               1
             3140  BINARY_SUBTRACT  
             3142  LOAD_CONST               0
             3144  COMPARE_OP               >=
         3146_3148  POP_JUMP_IF_FALSE  3180  'to 3180'
             3150  LOAD_FAST                'words'
             3152  LOAD_FAST                'start'
             3154  LOAD_CONST               1
             3156  BINARY_SUBTRACT  
             3158  BINARY_SUBSCR    
             3160  LOAD_FAST                'lists'
             3162  COMPARE_OP               in
         3164_3166  POP_JUMP_IF_FALSE  3180  'to 3180'

 L. 700      3168  LOAD_STR                 ''
             3170  LOAD_FAST                'words'
             3172  LOAD_FAST                'start'
             3174  LOAD_CONST               1
             3176  BINARY_SUBTRACT  
             3178  STORE_SUBSCR     
           3180_0  COME_FROM          3164  '3164'
           3180_1  COME_FROM          3146  '3146'

 L. 701      3180  LOAD_CONST               True
             3182  STORE_DEREF              'found'

 L. 702      3184  LOAD_CONST               True
             3186  STORE_FAST               'daySpecified'
         3188_3190  JUMP_BACK           370  'to 370'
             3192  POP_BLOCK        
           3194_0  COME_FROM_LOOP      358  '358'

 L. 705      3194  LOAD_CONST               0
             3196  STORE_DEREF              'hrOffset'

 L. 706      3198  LOAD_CONST               0
             3200  STORE_DEREF              'minOffset'

 L. 707      3202  LOAD_CONST               0
             3204  STORE_DEREF              'secOffset'

 L. 708      3206  LOAD_CONST               None
             3208  STORE_DEREF              'hrAbs'

 L. 709      3210  LOAD_CONST               None
             3212  STORE_DEREF              'minAbs'

 L. 711  3214_3216  SETUP_LOOP         5658  'to 5658'
             3218  LOAD_GLOBAL              enumerate
             3220  LOAD_FAST                'words'
             3222  CALL_FUNCTION_1       1  '1 positional argument'
             3224  GET_ITER         
           3226_0  COME_FROM          5502  '5502'
         3226_3228  FOR_ITER           5656  'to 5656'
             3230  UNPACK_SEQUENCE_2     2 
             3232  STORE_FAST               'idx'
             3234  STORE_FAST               'word'

 L. 712      3236  LOAD_FAST                'word'
             3238  LOAD_STR                 ''
             3240  COMPARE_OP               ==
         3242_3244  POP_JUMP_IF_FALSE  3250  'to 3250'

 L. 713  3246_3248  CONTINUE           3226  'to 3226'
           3250_0  COME_FROM          3242  '3242'

 L. 715      3250  LOAD_FAST                'idx'
             3252  LOAD_CONST               1
             3254  COMPARE_OP               >
         3256_3258  POP_JUMP_IF_FALSE  3272  'to 3272'
             3260  LOAD_FAST                'words'
             3262  LOAD_FAST                'idx'
             3264  LOAD_CONST               2
             3266  BINARY_SUBTRACT  
             3268  BINARY_SUBSCR    
             3270  JUMP_FORWARD       3274  'to 3274'
           3272_0  COME_FROM          3256  '3256'
             3272  LOAD_STR                 ''
           3274_0  COME_FROM          3270  '3270'
             3274  STORE_FAST               'wordPrevPrev'

 L. 716      3276  LOAD_FAST                'idx'
             3278  LOAD_CONST               0
             3280  COMPARE_OP               >
         3282_3284  POP_JUMP_IF_FALSE  3298  'to 3298'
             3286  LOAD_FAST                'words'
             3288  LOAD_FAST                'idx'
             3290  LOAD_CONST               1
             3292  BINARY_SUBTRACT  
             3294  BINARY_SUBSCR    
             3296  JUMP_FORWARD       3300  'to 3300'
           3298_0  COME_FROM          3282  '3282'
             3298  LOAD_STR                 ''
           3300_0  COME_FROM          3296  '3296'
             3300  STORE_FAST               'wordPrev'

 L. 717      3302  LOAD_FAST                'idx'
             3304  LOAD_CONST               1
             3306  BINARY_ADD       
             3308  LOAD_GLOBAL              len
             3310  LOAD_FAST                'words'
             3312  CALL_FUNCTION_1       1  '1 positional argument'
             3314  COMPARE_OP               <
         3316_3318  POP_JUMP_IF_FALSE  3332  'to 3332'
             3320  LOAD_FAST                'words'
             3322  LOAD_FAST                'idx'
             3324  LOAD_CONST               1
             3326  BINARY_ADD       
             3328  BINARY_SUBSCR    
             3330  JUMP_FORWARD       3334  'to 3334'
           3332_0  COME_FROM          3316  '3316'
             3332  LOAD_STR                 ''
           3334_0  COME_FROM          3330  '3330'
             3334  STORE_FAST               'wordNext'

 L. 718      3336  LOAD_FAST                'idx'
             3338  LOAD_CONST               2
             3340  BINARY_ADD       
             3342  LOAD_GLOBAL              len
             3344  LOAD_FAST                'words'
             3346  CALL_FUNCTION_1       1  '1 positional argument'
             3348  COMPARE_OP               <
         3350_3352  POP_JUMP_IF_FALSE  3366  'to 3366'
             3354  LOAD_FAST                'words'
             3356  LOAD_FAST                'idx'
             3358  LOAD_CONST               2
             3360  BINARY_ADD       
             3362  BINARY_SUBSCR    
             3364  JUMP_FORWARD       3368  'to 3368'
           3366_0  COME_FROM          3350  '3350'
             3366  LOAD_STR                 ''
           3368_0  COME_FROM          3364  '3364'
             3368  STORE_FAST               'wordNextNext'

 L. 719      3370  LOAD_FAST                'idx'
             3372  LOAD_CONST               3
             3374  BINARY_ADD       
             3376  LOAD_GLOBAL              len
             3378  LOAD_FAST                'words'
             3380  CALL_FUNCTION_1       1  '1 positional argument'
             3382  COMPARE_OP               <
         3384_3386  POP_JUMP_IF_FALSE  3400  'to 3400'
             3388  LOAD_FAST                'words'
             3390  LOAD_FAST                'idx'
             3392  LOAD_CONST               3
             3394  BINARY_ADD       
             3396  BINARY_SUBSCR    
             3398  JUMP_FORWARD       3402  'to 3402'
           3400_0  COME_FROM          3384  '3384'
             3400  LOAD_STR                 ''
           3402_0  COME_FROM          3398  '3398'
             3402  STORE_FAST               'wordNextNextNext'

 L. 721      3404  LOAD_CONST               0
             3406  STORE_FAST               'used'

 L. 722      3408  LOAD_FAST                'word'
             3410  LOAD_STR                 'medio'
             3412  COMPARE_OP               ==
         3414_3416  POP_JUMP_IF_FALSE  3444  'to 3444'
             3418  LOAD_FAST                'wordNext'
             3420  LOAD_STR                 'día'
             3422  COMPARE_OP               ==
         3424_3426  POP_JUMP_IF_FALSE  3444  'to 3444'

 L. 723      3428  LOAD_CONST               12
             3430  STORE_DEREF              'hrAbs'

 L. 724      3432  LOAD_FAST                'used'
             3434  LOAD_CONST               2
             3436  INPLACE_ADD      
             3438  STORE_FAST               'used'
         3440_3442  JUMP_FORWARD       5496  'to 5496'
           3444_0  COME_FROM          3424  '3424'
           3444_1  COME_FROM          3414  '3414'

 L. 725      3444  LOAD_FAST                'word'
             3446  LOAD_STR                 'media'
             3448  COMPARE_OP               ==
         3450_3452  POP_JUMP_IF_FALSE  3480  'to 3480'
             3454  LOAD_FAST                'wordNext'
             3456  LOAD_STR                 'noche'
             3458  COMPARE_OP               ==
         3460_3462  POP_JUMP_IF_FALSE  3480  'to 3480'

 L. 726      3464  LOAD_CONST               0
             3466  STORE_DEREF              'hrAbs'

 L. 727      3468  LOAD_FAST                'used'
             3470  LOAD_CONST               2
             3472  INPLACE_ADD      
             3474  STORE_FAST               'used'
         3476_3478  JUMP_FORWARD       5496  'to 5496'
           3480_0  COME_FROM          3460  '3460'
           3480_1  COME_FROM          3450  '3450'

 L. 728      3480  LOAD_FAST                'word'
             3482  LOAD_STR                 'mañana'
             3484  COMPARE_OP               ==
         3486_3488  POP_JUMP_IF_FALSE  3512  'to 3512'

 L. 729      3490  LOAD_DEREF               'hrAbs'
         3492_3494  POP_JUMP_IF_TRUE   3500  'to 3500'

 L. 730      3496  LOAD_CONST               8
             3498  STORE_DEREF              'hrAbs'
           3500_0  COME_FROM          3492  '3492'

 L. 731      3500  LOAD_FAST                'used'
             3502  LOAD_CONST               1
             3504  INPLACE_ADD      
             3506  STORE_FAST               'used'
         3508_3510  JUMP_FORWARD       5496  'to 5496'
           3512_0  COME_FROM          3486  '3486'

 L. 732      3512  LOAD_FAST                'word'
             3514  LOAD_STR                 'tarde'
             3516  COMPARE_OP               ==
         3518_3520  POP_JUMP_IF_FALSE  3544  'to 3544'

 L. 733      3522  LOAD_DEREF               'hrAbs'
         3524_3526  POP_JUMP_IF_TRUE   3532  'to 3532'

 L. 734      3528  LOAD_CONST               15
             3530  STORE_DEREF              'hrAbs'
           3532_0  COME_FROM          3524  '3524'

 L. 735      3532  LOAD_FAST                'used'
             3534  LOAD_CONST               1
             3536  INPLACE_ADD      
             3538  STORE_FAST               'used'
         3540_3542  JUMP_FORWARD       5496  'to 5496'
           3544_0  COME_FROM          3518  '3518'

 L. 736      3544  LOAD_FAST                'word'
             3546  LOAD_STR                 'media'
             3548  COMPARE_OP               ==
         3550_3552  POP_JUMP_IF_FALSE  3586  'to 3586'
             3554  LOAD_FAST                'wordNext'
             3556  LOAD_STR                 'tarde'
             3558  COMPARE_OP               ==
         3560_3562  POP_JUMP_IF_FALSE  3586  'to 3586'

 L. 737      3564  LOAD_DEREF               'hrAbs'
         3566_3568  POP_JUMP_IF_TRUE   3574  'to 3574'

 L. 738      3570  LOAD_CONST               17
             3572  STORE_DEREF              'hrAbs'
           3574_0  COME_FROM          3566  '3566'

 L. 739      3574  LOAD_FAST                'used'
             3576  LOAD_CONST               2
             3578  INPLACE_ADD      
             3580  STORE_FAST               'used'
         3582_3584  JUMP_FORWARD       5496  'to 5496'
           3586_0  COME_FROM          3560  '3560'
           3586_1  COME_FROM          3550  '3550'

 L. 740      3586  LOAD_FAST                'word'
             3588  LOAD_STR                 'tarde'
             3590  COMPARE_OP               ==
         3592_3594  POP_JUMP_IF_FALSE  3628  'to 3628'
             3596  LOAD_FAST                'wordNext'
             3598  LOAD_STR                 'noche'
             3600  COMPARE_OP               ==
         3602_3604  POP_JUMP_IF_FALSE  3628  'to 3628'

 L. 741      3606  LOAD_DEREF               'hrAbs'
         3608_3610  POP_JUMP_IF_TRUE   3616  'to 3616'

 L. 742      3612  LOAD_CONST               20
             3614  STORE_DEREF              'hrAbs'
           3616_0  COME_FROM          3608  '3608'

 L. 743      3616  LOAD_FAST                'used'
             3618  LOAD_CONST               2
             3620  INPLACE_ADD      
             3622  STORE_FAST               'used'
         3624_3626  JUMP_FORWARD       5496  'to 5496'
           3628_0  COME_FROM          3602  '3602'
           3628_1  COME_FROM          3592  '3592'

 L. 744      3628  LOAD_FAST                'word'
             3630  LOAD_STR                 'media'
             3632  COMPARE_OP               ==
         3634_3636  POP_JUMP_IF_FALSE  3670  'to 3670'
             3638  LOAD_FAST                'wordNext'
             3640  LOAD_STR                 'mañana'
             3642  COMPARE_OP               ==
         3644_3646  POP_JUMP_IF_FALSE  3670  'to 3670'

 L. 745      3648  LOAD_DEREF               'hrAbs'
         3650_3652  POP_JUMP_IF_TRUE   3658  'to 3658'

 L. 746      3654  LOAD_CONST               10
             3656  STORE_DEREF              'hrAbs'
           3658_0  COME_FROM          3650  '3650'

 L. 747      3658  LOAD_FAST                'used'
             3660  LOAD_CONST               2
             3662  INPLACE_ADD      
             3664  STORE_FAST               'used'
         3666_3668  JUMP_FORWARD       5496  'to 5496'
           3670_0  COME_FROM          3644  '3644'
           3670_1  COME_FROM          3634  '3634'

 L. 756      3670  LOAD_FAST                'word'
             3672  LOAD_STR                 'madrugada'
             3674  COMPARE_OP               ==
         3676_3678  POP_JUMP_IF_FALSE  3702  'to 3702'

 L. 757      3680  LOAD_DEREF               'hrAbs'
         3682_3684  POP_JUMP_IF_TRUE   3690  'to 3690'

 L. 758      3686  LOAD_CONST               1
             3688  STORE_DEREF              'hrAbs'
           3690_0  COME_FROM          3682  '3682'

 L. 759      3690  LOAD_FAST                'used'
             3692  LOAD_CONST               2
             3694  INPLACE_ADD      
             3696  STORE_FAST               'used'
         3698_3700  JUMP_FORWARD       5496  'to 5496'
           3702_0  COME_FROM          3676  '3676'

 L. 760      3702  LOAD_FAST                'word'
             3704  LOAD_STR                 'noche'
             3706  COMPARE_OP               ==
         3708_3710  POP_JUMP_IF_FALSE  3734  'to 3734'

 L. 761      3712  LOAD_DEREF               'hrAbs'
         3714_3716  POP_JUMP_IF_TRUE   3722  'to 3722'

 L. 762      3718  LOAD_CONST               21
             3720  STORE_DEREF              'hrAbs'
           3722_0  COME_FROM          3714  '3714'

 L. 763      3722  LOAD_FAST                'used'
             3724  LOAD_CONST               1
             3726  INPLACE_ADD      
             3728  STORE_FAST               'used'
         3730_3732  JUMP_FORWARD       5496  'to 5496'
           3734_0  COME_FROM          3708  '3708'

 L. 765      3734  LOAD_FAST                'word'
             3736  LOAD_STR                 'hora'
             3738  COMPARE_OP               ==
         3740_3742  POP_JUMP_IF_FALSE  3922  'to 3922'

 L. 766      3744  LOAD_FAST                'wordPrev'
             3746  LOAD_FAST                'time_indicators'
             3748  COMPARE_OP               in
         3750_3752  POP_JUMP_IF_TRUE   3764  'to 3764'
             3754  LOAD_FAST                'wordPrevPrev'

 L. 767      3756  LOAD_FAST                'time_indicators'
             3758  COMPARE_OP               in
         3760_3762  POP_JUMP_IF_FALSE  3922  'to 3922'
           3764_0  COME_FROM          3750  '3750'

 L. 768      3764  LOAD_FAST                'wordPrev'
             3766  LOAD_STR                 'media'
             3768  COMPARE_OP               ==
         3770_3772  POP_JUMP_IF_FALSE  3780  'to 3780'

 L. 769      3774  LOAD_CONST               30
             3776  STORE_DEREF              'minOffset'
             3778  JUMP_FORWARD       3868  'to 3868'
           3780_0  COME_FROM          3770  '3770'

 L. 770      3780  LOAD_FAST                'wordPrev'
             3782  LOAD_STR                 'cuarto'
             3784  COMPARE_OP               ==
         3786_3788  POP_JUMP_IF_FALSE  3796  'to 3796'

 L. 771      3790  LOAD_CONST               15
             3792  STORE_DEREF              'minOffset'
             3794  JUMP_FORWARD       3868  'to 3868'
           3796_0  COME_FROM          3786  '3786'

 L. 772      3796  LOAD_FAST                'wordPrevPrev'
             3798  LOAD_STR                 'cuarto'
             3800  COMPARE_OP               ==
         3802_3804  POP_JUMP_IF_FALSE  3864  'to 3864'

 L. 773      3806  LOAD_CONST               15
             3808  STORE_DEREF              'minOffset'

 L. 774      3810  LOAD_FAST                'idx'
             3812  LOAD_CONST               2
             3814  COMPARE_OP               >
         3816_3818  POP_JUMP_IF_FALSE  3850  'to 3850'
             3820  LOAD_FAST                'words'
             3822  LOAD_FAST                'idx'
             3824  LOAD_CONST               3
             3826  BINARY_SUBTRACT  
             3828  BINARY_SUBSCR    
             3830  LOAD_FAST                'time_indicators'
             3832  COMPARE_OP               in
         3834_3836  POP_JUMP_IF_FALSE  3850  'to 3850'

 L. 775      3838  LOAD_STR                 ''
             3840  LOAD_FAST                'words'
             3842  LOAD_FAST                'idx'
             3844  LOAD_CONST               3
             3846  BINARY_SUBTRACT  
             3848  STORE_SUBSCR     
           3850_0  COME_FROM          3834  '3834'
           3850_1  COME_FROM          3816  '3816'

 L. 776      3850  LOAD_STR                 ''
             3852  LOAD_FAST                'words'
             3854  LOAD_FAST                'idx'
             3856  LOAD_CONST               2
             3858  BINARY_SUBTRACT  
             3860  STORE_SUBSCR     
             3862  JUMP_FORWARD       3868  'to 3868'
           3864_0  COME_FROM          3802  '3802'

 L. 778      3864  LOAD_CONST               1
             3866  STORE_DEREF              'hrOffset'
           3868_0  COME_FROM          3862  '3862'
           3868_1  COME_FROM          3794  '3794'
           3868_2  COME_FROM          3778  '3778'

 L. 779      3868  LOAD_FAST                'wordPrevPrev'
             3870  LOAD_FAST                'time_indicators'
             3872  COMPARE_OP               in
         3874_3876  POP_JUMP_IF_FALSE  3890  'to 3890'

 L. 780      3878  LOAD_STR                 ''
             3880  LOAD_FAST                'words'
             3882  LOAD_FAST                'idx'
             3884  LOAD_CONST               2
             3886  BINARY_SUBTRACT  
             3888  STORE_SUBSCR     
           3890_0  COME_FROM          3874  '3874'

 L. 781      3890  LOAD_STR                 ''
             3892  LOAD_FAST                'words'
             3894  LOAD_FAST                'idx'
             3896  LOAD_CONST               1
             3898  BINARY_SUBTRACT  
             3900  STORE_SUBSCR     

 L. 782      3902  LOAD_FAST                'used'
             3904  LOAD_CONST               1
             3906  INPLACE_ADD      
             3908  STORE_FAST               'used'

 L. 783      3910  LOAD_CONST               -1
             3912  STORE_DEREF              'hrAbs'

 L. 784      3914  LOAD_CONST               -1
             3916  STORE_DEREF              'minAbs'
         3918_3920  JUMP_FORWARD       5496  'to 5496'
           3922_0  COME_FROM          3760  '3760'
           3922_1  COME_FROM          3740  '3740'

 L. 786      3922  LOAD_FAST                'word'
             3924  LOAD_CONST               0
             3926  BINARY_SUBSCR    
             3928  LOAD_METHOD              isdigit
             3930  CALL_METHOD_0         0  '0 positional arguments'
         3932_3934  POP_JUMP_IF_FALSE  5496  'to 5496'

 L. 787      3936  LOAD_CONST               True
             3938  STORE_FAST               'isTime'

 L. 788      3940  LOAD_STR                 ''
             3942  STORE_FAST               'strHH'

 L. 789      3944  LOAD_STR                 ''
             3946  STORE_FAST               'strMM'

 L. 790      3948  LOAD_STR                 ''
             3950  STORE_FAST               'remainder'

 L. 791      3952  LOAD_STR                 ':'
             3954  LOAD_FAST                'word'
             3956  COMPARE_OP               in
         3958_3960  POP_JUMP_IF_FALSE  4474  'to 4474'

 L. 794      3962  LOAD_CONST               0
             3964  STORE_FAST               'stage'

 L. 795      3966  LOAD_GLOBAL              len
             3968  LOAD_FAST                'word'
             3970  CALL_FUNCTION_1       1  '1 positional argument'
             3972  STORE_FAST               'length'

 L. 796      3974  SETUP_LOOP         4150  'to 4150'
             3976  LOAD_GLOBAL              range
             3978  LOAD_FAST                'length'
             3980  CALL_FUNCTION_1       1  '1 positional argument'
             3982  GET_ITER         
           3984_0  COME_FROM          4118  '4118'
             3984  FOR_ITER           4148  'to 4148'
             3986  STORE_FAST               'i'

 L. 797      3988  LOAD_FAST                'stage'
             3990  LOAD_CONST               0
             3992  COMPARE_OP               ==
         3994_3996  POP_JUMP_IF_FALSE  4060  'to 4060'

 L. 798      3998  LOAD_FAST                'word'
             4000  LOAD_FAST                'i'
             4002  BINARY_SUBSCR    
             4004  LOAD_METHOD              isdigit
             4006  CALL_METHOD_0         0  '0 positional arguments'
         4008_4010  POP_JUMP_IF_FALSE  4026  'to 4026'

 L. 799      4012  LOAD_FAST                'strHH'
             4014  LOAD_FAST                'word'
             4016  LOAD_FAST                'i'
             4018  BINARY_SUBSCR    
             4020  INPLACE_ADD      
             4022  STORE_FAST               'strHH'
             4024  JUMP_FORWARD       4058  'to 4058'
           4026_0  COME_FROM          4008  '4008'

 L. 800      4026  LOAD_FAST                'word'
             4028  LOAD_FAST                'i'
             4030  BINARY_SUBSCR    
             4032  LOAD_STR                 ':'
             4034  COMPARE_OP               ==
         4036_4038  POP_JUMP_IF_FALSE  4046  'to 4046'

 L. 801      4040  LOAD_CONST               1
             4042  STORE_FAST               'stage'
             4044  JUMP_FORWARD       4058  'to 4058'
           4046_0  COME_FROM          4036  '4036'

 L. 803      4046  LOAD_CONST               2
             4048  STORE_FAST               'stage'

 L. 804      4050  LOAD_FAST                'i'
             4052  LOAD_CONST               1
             4054  INPLACE_SUBTRACT 
             4056  STORE_FAST               'i'
           4058_0  COME_FROM          4044  '4044'
           4058_1  COME_FROM          4024  '4024'
             4058  JUMP_BACK          3984  'to 3984'
           4060_0  COME_FROM          3994  '3994'

 L. 805      4060  LOAD_FAST                'stage'
             4062  LOAD_CONST               1
             4064  COMPARE_OP               ==
         4066_4068  POP_JUMP_IF_FALSE  4112  'to 4112'

 L. 806      4070  LOAD_FAST                'word'
             4072  LOAD_FAST                'i'
             4074  BINARY_SUBSCR    
             4076  LOAD_METHOD              isdigit
             4078  CALL_METHOD_0         0  '0 positional arguments'
         4080_4082  POP_JUMP_IF_FALSE  4098  'to 4098'

 L. 807      4084  LOAD_FAST                'strMM'
             4086  LOAD_FAST                'word'
             4088  LOAD_FAST                'i'
             4090  BINARY_SUBSCR    
             4092  INPLACE_ADD      
             4094  STORE_FAST               'strMM'
             4096  JUMP_FORWARD       4110  'to 4110'
           4098_0  COME_FROM          4080  '4080'

 L. 809      4098  LOAD_CONST               2
             4100  STORE_FAST               'stage'

 L. 810      4102  LOAD_FAST                'i'
             4104  LOAD_CONST               1
             4106  INPLACE_SUBTRACT 
             4108  STORE_FAST               'i'
           4110_0  COME_FROM          4096  '4096'
             4110  JUMP_BACK          3984  'to 3984'
           4112_0  COME_FROM          4066  '4066'

 L. 811      4112  LOAD_FAST                'stage'
             4114  LOAD_CONST               2
             4116  COMPARE_OP               ==
         4118_4120  POP_JUMP_IF_FALSE  3984  'to 3984'

 L. 812      4122  LOAD_FAST                'word'
             4124  LOAD_FAST                'i'
             4126  LOAD_CONST               None
             4128  BUILD_SLICE_2         2 
             4130  BINARY_SUBSCR    
             4132  LOAD_METHOD              replace
             4134  LOAD_STR                 '.'
             4136  LOAD_STR                 ''
             4138  CALL_METHOD_2         2  '2 positional arguments'
             4140  STORE_FAST               'remainder'

 L. 813      4142  BREAK_LOOP       
         4144_4146  JUMP_BACK          3984  'to 3984'
             4148  POP_BLOCK        
           4150_0  COME_FROM_LOOP     3974  '3974'

 L. 814      4150  LOAD_FAST                'remainder'
             4152  LOAD_STR                 ''
             4154  COMPARE_OP               ==
         4156_4158  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 815      4160  LOAD_FAST                'wordNext'
             4162  LOAD_METHOD              replace
             4164  LOAD_STR                 '.'
             4166  LOAD_STR                 ''
             4168  CALL_METHOD_2         2  '2 positional arguments'
             4170  STORE_FAST               'nextWord'

 L. 816      4172  LOAD_FAST                'nextWord'
             4174  LOAD_STR                 'am'
             4176  COMPARE_OP               ==
         4178_4180  POP_JUMP_IF_TRUE   4192  'to 4192'
             4182  LOAD_FAST                'nextWord'
             4184  LOAD_STR                 'pm'
             4186  COMPARE_OP               ==
         4188_4190  POP_JUMP_IF_FALSE  4208  'to 4208'
           4192_0  COME_FROM          4178  '4178'

 L. 817      4192  LOAD_FAST                'nextWord'
             4194  STORE_FAST               'remainder'

 L. 818      4196  LOAD_FAST                'used'
             4198  LOAD_CONST               1
             4200  INPLACE_ADD      
             4202  STORE_FAST               'used'
         4204_4206  JUMP_ABSOLUTE      5302  'to 5302'
           4208_0  COME_FROM          4188  '4188'

 L. 819      4208  LOAD_FAST                'wordNext'
             4210  LOAD_STR                 'mañana'
             4212  COMPARE_OP               ==
         4214_4216  POP_JUMP_IF_TRUE   4228  'to 4228'
             4218  LOAD_FAST                'wordNext'
             4220  LOAD_STR                 'madrugada'
             4222  COMPARE_OP               ==
         4224_4226  POP_JUMP_IF_FALSE  4242  'to 4242'
           4228_0  COME_FROM          4214  '4214'

 L. 820      4228  LOAD_STR                 'am'
             4230  STORE_FAST               'remainder'

 L. 821      4232  LOAD_FAST                'used'
             4234  LOAD_CONST               1
             4236  INPLACE_ADD      
             4238  STORE_FAST               'used'
             4240  JUMP_FORWARD       5302  'to 5302'
           4242_0  COME_FROM          4224  '4224'

 L. 822      4242  LOAD_FAST                'wordNext'
             4244  LOAD_STR                 'tarde'
             4246  COMPARE_OP               ==
         4248_4250  POP_JUMP_IF_FALSE  4266  'to 4266'

 L. 823      4252  LOAD_STR                 'pm'
             4254  STORE_FAST               'remainder'

 L. 824      4256  LOAD_FAST                'used'
             4258  LOAD_CONST               1
             4260  INPLACE_ADD      
             4262  STORE_FAST               'used'
             4264  JUMP_FORWARD       5302  'to 5302'
           4266_0  COME_FROM          4248  '4248'

 L. 825      4266  LOAD_FAST                'wordNext'
             4268  LOAD_STR                 'noche'
             4270  COMPARE_OP               ==
         4272_4274  POP_JUMP_IF_FALSE  4332  'to 4332'

 L. 826      4276  LOAD_CONST               0
             4278  LOAD_GLOBAL              int
             4280  LOAD_FAST                'word'
             4282  LOAD_CONST               0
             4284  BINARY_SUBSCR    
             4286  CALL_FUNCTION_1       1  '1 positional argument'
             4288  DUP_TOP          
             4290  ROT_THREE        
             4292  COMPARE_OP               <
         4294_4296  POP_JUMP_IF_FALSE  4308  'to 4308'
             4298  LOAD_CONST               6
             4300  COMPARE_OP               <
         4302_4304  POP_JUMP_IF_FALSE  4318  'to 4318'
             4306  JUMP_FORWARD       4312  'to 4312'
           4308_0  COME_FROM          4294  '4294'
             4308  POP_TOP          
             4310  JUMP_FORWARD       4318  'to 4318'
           4312_0  COME_FROM          4306  '4306'

 L. 827      4312  LOAD_STR                 'am'
             4314  STORE_FAST               'remainder'
             4316  JUMP_FORWARD       4322  'to 4322'
           4318_0  COME_FROM          4310  '4310'
           4318_1  COME_FROM          4302  '4302'

 L. 829      4318  LOAD_STR                 'pm'
             4320  STORE_FAST               'remainder'
           4322_0  COME_FROM          4316  '4316'

 L. 830      4322  LOAD_FAST                'used'
             4324  LOAD_CONST               1
             4326  INPLACE_ADD      
             4328  STORE_FAST               'used'
             4330  JUMP_FORWARD       5302  'to 5302'
           4332_0  COME_FROM          4272  '4272'

 L. 831      4332  LOAD_FAST                'wordNext'
             4334  LOAD_FAST                'thises'
             4336  COMPARE_OP               in
         4338_4340  POP_JUMP_IF_FALSE  4362  'to 4362'
             4342  LOAD_FAST                'wordNextNext'
             4344  LOAD_STR                 'mañana'
             4346  COMPARE_OP               ==
         4348_4350  POP_JUMP_IF_FALSE  4362  'to 4362'

 L. 832      4352  LOAD_STR                 'am'
             4354  STORE_FAST               'remainder'

 L. 833      4356  LOAD_CONST               2
             4358  STORE_FAST               'used'
             4360  JUMP_FORWARD       5302  'to 5302'
           4362_0  COME_FROM          4348  '4348'
           4362_1  COME_FROM          4338  '4338'

 L. 834      4362  LOAD_FAST                'wordNext'
             4364  LOAD_FAST                'thises'
             4366  COMPARE_OP               in
         4368_4370  POP_JUMP_IF_FALSE  4392  'to 4392'
             4372  LOAD_FAST                'wordNextNext'
             4374  LOAD_STR                 'tarde'
             4376  COMPARE_OP               ==
         4378_4380  POP_JUMP_IF_FALSE  4392  'to 4392'

 L. 835      4382  LOAD_STR                 'pm'
             4384  STORE_FAST               'remainder'

 L. 836      4386  LOAD_CONST               2
             4388  STORE_FAST               'used'
             4390  JUMP_FORWARD       5302  'to 5302'
           4392_0  COME_FROM          4378  '4378'
           4392_1  COME_FROM          4368  '4368'

 L. 837      4392  LOAD_FAST                'wordNext'
             4394  LOAD_FAST                'thises'
             4396  COMPARE_OP               in
         4398_4400  POP_JUMP_IF_FALSE  4422  'to 4422'
             4402  LOAD_FAST                'wordNextNext'
             4404  LOAD_STR                 'noche'
             4406  COMPARE_OP               ==
         4408_4410  POP_JUMP_IF_FALSE  4422  'to 4422'

 L. 838      4412  LOAD_STR                 'pm'
             4414  STORE_FAST               'remainder'

 L. 839      4416  LOAD_CONST               2
             4418  STORE_FAST               'used'
             4420  JUMP_FORWARD       5302  'to 5302'
           4422_0  COME_FROM          4408  '4408'
           4422_1  COME_FROM          4398  '4398'

 L. 841      4422  LOAD_FAST                'timeQualifier'
             4424  LOAD_STR                 ''
             4426  COMPARE_OP               !=
         4428_4430  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 842      4432  LOAD_FAST                'strHH'
             4434  LOAD_CONST               12
             4436  COMPARE_OP               <=
         4438_4440  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 843      4442  LOAD_FAST                'timeQualifier'
             4444  LOAD_STR                 'mañana'
             4446  COMPARE_OP               ==
         4448_4450  POP_JUMP_IF_TRUE   4462  'to 4462'

 L. 844      4452  LOAD_FAST                'timeQualifier'
             4454  LOAD_STR                 'tarde'
             4456  COMPARE_OP               ==
         4458_4460  POP_JUMP_IF_FALSE  5302  'to 5302'
           4462_0  COME_FROM          4448  '4448'

 L. 845      4462  LOAD_FAST                'strHH'
             4464  LOAD_CONST               12
             4466  INPLACE_ADD      
             4468  STORE_FAST               'strHH'
         4470_4472  JUMP_FORWARD       5302  'to 5302'
           4474_0  COME_FROM          3958  '3958'

 L. 850      4474  LOAD_GLOBAL              len
             4476  LOAD_FAST                'word'
             4478  CALL_FUNCTION_1       1  '1 positional argument'
             4480  STORE_FAST               'length'

 L. 851      4482  LOAD_STR                 ''
             4484  STORE_FAST               'strNum'

 L. 852      4486  LOAD_STR                 ''
             4488  STORE_FAST               'remainder'

 L. 853      4490  SETUP_LOOP         4550  'to 4550'
             4492  LOAD_GLOBAL              range
             4494  LOAD_FAST                'length'
             4496  CALL_FUNCTION_1       1  '1 positional argument'
             4498  GET_ITER         
             4500  FOR_ITER           4548  'to 4548'
             4502  STORE_FAST               'i'

 L. 854      4504  LOAD_FAST                'word'
             4506  LOAD_FAST                'i'
             4508  BINARY_SUBSCR    
             4510  LOAD_METHOD              isdigit
             4512  CALL_METHOD_0         0  '0 positional arguments'
         4514_4516  POP_JUMP_IF_FALSE  4532  'to 4532'

 L. 855      4518  LOAD_FAST                'strNum'
             4520  LOAD_FAST                'word'
             4522  LOAD_FAST                'i'
             4524  BINARY_SUBSCR    
             4526  INPLACE_ADD      
             4528  STORE_FAST               'strNum'
             4530  JUMP_BACK          4500  'to 4500'
           4532_0  COME_FROM          4514  '4514'

 L. 857      4532  LOAD_FAST                'remainder'
             4534  LOAD_FAST                'word'
             4536  LOAD_FAST                'i'
             4538  BINARY_SUBSCR    
             4540  INPLACE_ADD      
             4542  STORE_FAST               'remainder'
         4544_4546  JUMP_BACK          4500  'to 4500'
             4548  POP_BLOCK        
           4550_0  COME_FROM_LOOP     4490  '4490'

 L. 859      4550  LOAD_FAST                'remainder'
             4552  LOAD_STR                 ''
             4554  COMPARE_OP               ==
         4556_4558  POP_JUMP_IF_FALSE  4580  'to 4580'

 L. 860      4560  LOAD_FAST                'wordNext'
             4562  LOAD_METHOD              replace
             4564  LOAD_STR                 '.'
             4566  LOAD_STR                 ''
             4568  CALL_METHOD_2         2  '2 positional arguments'
             4570  LOAD_METHOD              lstrip
             4572  CALL_METHOD_0         0  '0 positional arguments'
             4574  LOAD_METHOD              rstrip
             4576  CALL_METHOD_0         0  '0 positional arguments'
             4578  STORE_FAST               'remainder'
           4580_0  COME_FROM          4556  '4556'

 L. 863      4580  LOAD_FAST                'remainder'
             4582  LOAD_STR                 'pm'
             4584  COMPARE_OP               ==
         4586_4588  POP_JUMP_IF_TRUE   4620  'to 4620'

 L. 864      4590  LOAD_FAST                'wordNext'
             4592  LOAD_STR                 'pm'
             4594  COMPARE_OP               ==
         4596_4598  POP_JUMP_IF_TRUE   4620  'to 4620'

 L. 865      4600  LOAD_FAST                'remainder'
             4602  LOAD_STR                 'p.m.'
             4604  COMPARE_OP               ==
         4606_4608  POP_JUMP_IF_TRUE   4620  'to 4620'

 L. 866      4610  LOAD_FAST                'wordNext'
             4612  LOAD_STR                 'p.m.'
             4614  COMPARE_OP               ==
         4616_4618  POP_JUMP_IF_FALSE  4636  'to 4636'
           4620_0  COME_FROM          4606  '4606'
           4620_1  COME_FROM          4596  '4596'
           4620_2  COME_FROM          4586  '4586'

 L. 867      4620  LOAD_FAST                'strNum'
             4622  STORE_FAST               'strHH'

 L. 868      4624  LOAD_STR                 'pm'
             4626  STORE_FAST               'remainder'

 L. 869      4628  LOAD_CONST               1
             4630  STORE_FAST               'used'
         4632_4634  JUMP_FORWARD       5302  'to 5302'
           4636_0  COME_FROM          4616  '4616'

 L. 871      4636  LOAD_FAST                'remainder'
             4638  LOAD_STR                 'am'
             4640  COMPARE_OP               ==
         4642_4644  POP_JUMP_IF_TRUE   4676  'to 4676'

 L. 872      4646  LOAD_FAST                'wordNext'
             4648  LOAD_STR                 'am'
             4650  COMPARE_OP               ==
         4652_4654  POP_JUMP_IF_TRUE   4676  'to 4676'

 L. 873      4656  LOAD_FAST                'remainder'
             4658  LOAD_STR                 'a.m.'
             4660  COMPARE_OP               ==
         4662_4664  POP_JUMP_IF_TRUE   4676  'to 4676'

 L. 874      4666  LOAD_FAST                'wordNext'
             4668  LOAD_STR                 'a.m.'
             4670  COMPARE_OP               ==
         4672_4674  POP_JUMP_IF_FALSE  4692  'to 4692'
           4676_0  COME_FROM          4662  '4662'
           4676_1  COME_FROM          4652  '4652'
           4676_2  COME_FROM          4642  '4642'

 L. 875      4676  LOAD_FAST                'strNum'
             4678  STORE_FAST               'strHH'

 L. 876      4680  LOAD_STR                 'am'
             4682  STORE_FAST               'remainder'

 L. 877      4684  LOAD_CONST               1
             4686  STORE_FAST               'used'
         4688_4690  JUMP_FORWARD       5302  'to 5302'
           4692_0  COME_FROM          4672  '4672'

 L. 879      4692  LOAD_FAST                'wordNext'
             4694  LOAD_STR                 'pm'
             4696  COMPARE_OP               ==
         4698_4700  POP_JUMP_IF_TRUE   4722  'to 4722'

 L. 880      4702  LOAD_FAST                'wordNext'
             4704  LOAD_STR                 'p.m.'
             4706  COMPARE_OP               ==
         4708_4710  POP_JUMP_IF_TRUE   4722  'to 4722'

 L. 881      4712  LOAD_FAST                'wordNext'
             4714  LOAD_STR                 'tarde'
             4716  COMPARE_OP               ==
         4718_4720  POP_JUMP_IF_FALSE  4738  'to 4738'
           4722_0  COME_FROM          4708  '4708'
           4722_1  COME_FROM          4698  '4698'

 L. 882      4722  LOAD_FAST                'strNum'
             4724  STORE_FAST               'strHH'

 L. 883      4726  LOAD_STR                 'pm'
             4728  STORE_FAST               'remainder'

 L. 884      4730  LOAD_CONST               1
             4732  STORE_FAST               'used'
         4734_4736  JUMP_FORWARD       5302  'to 5302'
           4738_0  COME_FROM          4718  '4718'

 L. 885      4738  LOAD_FAST                'wordNext'
             4740  LOAD_STR                 'am'
             4742  COMPARE_OP               ==
         4744_4746  POP_JUMP_IF_TRUE   4768  'to 4768'

 L. 886      4748  LOAD_FAST                'wordNext'
             4750  LOAD_STR                 'a.m.'
             4752  COMPARE_OP               ==
         4754_4756  POP_JUMP_IF_TRUE   4768  'to 4768'

 L. 887      4758  LOAD_FAST                'wordNext'
             4760  LOAD_STR                 'mañana'
             4762  COMPARE_OP               ==
         4764_4766  POP_JUMP_IF_FALSE  4784  'to 4784'
           4768_0  COME_FROM          4754  '4754'
           4768_1  COME_FROM          4744  '4744'

 L. 888      4768  LOAD_FAST                'strNum'
             4770  STORE_FAST               'strHH'

 L. 889      4772  LOAD_STR                 'am'
             4774  STORE_FAST               'remainder'

 L. 890      4776  LOAD_CONST               1
             4778  STORE_FAST               'used'
         4780_4782  JUMP_FORWARD       5302  'to 5302'
           4784_0  COME_FROM          4764  '4764'

 L. 891      4784  LOAD_GLOBAL              int
             4786  LOAD_FAST                'word'
             4788  CALL_FUNCTION_1       1  '1 positional argument'
             4790  LOAD_CONST               100
             4792  COMPARE_OP               >
         4794_4796  POP_JUMP_IF_FALSE  4858  'to 4858'

 L. 895      4798  LOAD_FAST                'wordPrev'
             4800  LOAD_STR                 'cero'
             4802  COMPARE_OP               ==
         4804_4806  POP_JUMP_IF_FALSE  4858  'to 4858'

 L. 898      4808  LOAD_GLOBAL              int
             4810  LOAD_FAST                'word'
             4812  CALL_FUNCTION_1       1  '1 positional argument'
             4814  LOAD_CONST               100
             4816  BINARY_TRUE_DIVIDE
             4818  STORE_FAST               'strHH'

 L. 899      4820  LOAD_GLOBAL              int
             4822  LOAD_FAST                'word'
             4824  CALL_FUNCTION_1       1  '1 positional argument'
             4826  LOAD_FAST                'strHH'
             4828  LOAD_CONST               100
             4830  BINARY_MULTIPLY  
             4832  BINARY_SUBTRACT  
             4834  STORE_FAST               'strMM'

 L. 900      4836  LOAD_FAST                'wordNext'
             4838  LOAD_STR                 'hora'
             4840  COMPARE_OP               ==
         4842_4844  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 901      4846  LOAD_FAST                'used'
             4848  LOAD_CONST               1
             4850  INPLACE_ADD      
             4852  STORE_FAST               'used'
         4854_4856  JUMP_FORWARD       5302  'to 5302'
           4858_0  COME_FROM          4804  '4804'
           4858_1  COME_FROM          4794  '4794'

 L. 903      4858  LOAD_FAST                'wordNext'
             4860  LOAD_STR                 'hora'
             4862  COMPARE_OP               ==
         4864_4866  POP_JUMP_IF_FALSE  4938  'to 4938'

 L. 904      4868  LOAD_FAST                'word'
             4870  LOAD_CONST               0
             4872  BINARY_SUBSCR    
             4874  LOAD_STR                 '0'
             4876  COMPARE_OP               !=
         4878_4880  POP_JUMP_IF_FALSE  4938  'to 4938'

 L. 906      4882  LOAD_GLOBAL              int
             4884  LOAD_FAST                'word'
             4886  CALL_FUNCTION_1       1  '1 positional argument'
             4888  LOAD_CONST               100
             4890  COMPARE_OP               <
         4892_4894  POP_JUMP_IF_FALSE  4938  'to 4938'

 L. 907      4896  LOAD_GLOBAL              int
             4898  LOAD_FAST                'word'
             4900  CALL_FUNCTION_1       1  '1 positional argument'
             4902  LOAD_CONST               2400
             4904  COMPARE_OP               >
         4906_4908  POP_JUMP_IF_FALSE  4938  'to 4938'

 L. 911      4910  LOAD_GLOBAL              int
             4912  LOAD_FAST                'word'
             4914  CALL_FUNCTION_1       1  '1 positional argument'
             4916  STORE_DEREF              'hrOffset'

 L. 912      4918  LOAD_CONST               2
             4920  STORE_FAST               'used'

 L. 913      4922  LOAD_CONST               False
             4924  STORE_FAST               'isTime'

 L. 914      4926  LOAD_CONST               -1
             4928  STORE_DEREF              'hrAbs'

 L. 915      4930  LOAD_CONST               -1
             4932  STORE_DEREF              'minAbs'
         4934_4936  JUMP_FORWARD       5302  'to 5302'
           4938_0  COME_FROM          4906  '4906'
           4938_1  COME_FROM          4892  '4892'
           4938_2  COME_FROM          4878  '4878'
           4938_3  COME_FROM          4864  '4864'

 L. 917      4938  LOAD_FAST                'wordNext'
             4940  LOAD_STR                 'minuto'
             4942  COMPARE_OP               ==
         4944_4946  POP_JUMP_IF_FALSE  4976  'to 4976'

 L. 919      4948  LOAD_GLOBAL              int
             4950  LOAD_FAST                'word'
             4952  CALL_FUNCTION_1       1  '1 positional argument'
             4954  STORE_DEREF              'minOffset'

 L. 920      4956  LOAD_CONST               2
             4958  STORE_FAST               'used'

 L. 921      4960  LOAD_CONST               False
             4962  STORE_FAST               'isTime'

 L. 922      4964  LOAD_CONST               -1
             4966  STORE_DEREF              'hrAbs'

 L. 923      4968  LOAD_CONST               -1
             4970  STORE_DEREF              'minAbs'
         4972_4974  JUMP_FORWARD       5302  'to 5302'
           4976_0  COME_FROM          4944  '4944'

 L. 924      4976  LOAD_FAST                'wordNext'
             4978  LOAD_STR                 'segundo'
             4980  COMPARE_OP               ==
         4982_4984  POP_JUMP_IF_FALSE  5014  'to 5014'

 L. 926      4986  LOAD_GLOBAL              int
             4988  LOAD_FAST                'word'
             4990  CALL_FUNCTION_1       1  '1 positional argument'
             4992  STORE_DEREF              'secOffset'

 L. 927      4994  LOAD_CONST               2
             4996  STORE_FAST               'used'

 L. 928      4998  LOAD_CONST               False
             5000  STORE_FAST               'isTime'

 L. 929      5002  LOAD_CONST               -1
             5004  STORE_DEREF              'hrAbs'

 L. 930      5006  LOAD_CONST               -1
             5008  STORE_DEREF              'minAbs'
         5010_5012  JUMP_FORWARD       5302  'to 5302'
           5014_0  COME_FROM          4982  '4982'

 L. 931      5014  LOAD_GLOBAL              int
             5016  LOAD_FAST                'word'
             5018  CALL_FUNCTION_1       1  '1 positional argument'
             5020  LOAD_CONST               100
             5022  COMPARE_OP               >
         5024_5026  POP_JUMP_IF_FALSE  5076  'to 5076'

 L. 932      5028  LOAD_GLOBAL              int
             5030  LOAD_FAST                'word'
             5032  CALL_FUNCTION_1       1  '1 positional argument'
             5034  LOAD_CONST               100
             5036  BINARY_TRUE_DIVIDE
             5038  STORE_FAST               'strHH'

 L. 933      5040  LOAD_GLOBAL              int
             5042  LOAD_FAST                'word'
             5044  CALL_FUNCTION_1       1  '1 positional argument'
             5046  LOAD_FAST                'strHH'
             5048  LOAD_CONST               100
             5050  BINARY_MULTIPLY  
             5052  BINARY_SUBTRACT  
             5054  STORE_FAST               'strMM'

 L. 934      5056  LOAD_FAST                'wordNext'
             5058  LOAD_STR                 'hora'
             5060  COMPARE_OP               ==
         5062_5064  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 935      5066  LOAD_FAST                'used'
             5068  LOAD_CONST               1
           5070_0  COME_FROM          4240  '4240'
             5070  INPLACE_ADD      
             5072  STORE_FAST               'used'
             5074  JUMP_FORWARD       5302  'to 5302'
           5076_0  COME_FROM          5024  '5024'

 L. 937      5076  LOAD_FAST                'wordNext'
             5078  LOAD_STR                 ''
             5080  COMPARE_OP               ==
         5082_5084  POP_JUMP_IF_TRUE   5106  'to 5106'

 L. 938      5086  LOAD_FAST                'wordNext'
             5088  LOAD_STR                 'en'
             5090  COMPARE_OP               ==
         5092_5094  POP_JUMP_IF_FALSE  5248  'to 5248'
             5096  LOAD_FAST                'wordNextNext'
             5098  LOAD_STR                 'punto'
             5100  COMPARE_OP               ==
         5102_5104  POP_JUMP_IF_FALSE  5248  'to 5248'
           5106_0  COME_FROM          5082  '5082'

 L. 939      5106  LOAD_FAST                'word'
             5108  STORE_FAST               'strHH'

 L. 940      5110  LOAD_CONST               0
             5112  STORE_FAST               'strMM'

 L. 941      5114  LOAD_FAST                'wordNext'
             5116  LOAD_STR                 'en'
             5118  COMPARE_OP               ==
         5120_5122  POP_JUMP_IF_FALSE  5302  'to 5302'
             5124  LOAD_FAST                'wordNextNext'
             5126  LOAD_STR                 'punto'
             5128  COMPARE_OP               ==
         5130_5132  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 942      5134  LOAD_FAST                'used'
             5136  LOAD_CONST               2
             5138  INPLACE_ADD      
             5140  STORE_FAST               'used'

 L. 943      5142  LOAD_FAST                'wordNextNextNext'
             5144  LOAD_STR                 'tarde'
             5146  COMPARE_OP               ==
         5148_5150  POP_JUMP_IF_FALSE  5166  'to 5166'

 L. 944      5152  LOAD_STR                 'pm'
             5154  STORE_FAST               'remainder'

 L. 945      5156  LOAD_FAST                'used'
             5158  LOAD_CONST               1
           5160_0  COME_FROM          4330  '4330'
             5160  INPLACE_ADD      
             5162  STORE_FAST               'used'
             5164  JUMP_FORWARD       5246  'to 5246'
           5166_0  COME_FROM          5148  '5148'

 L. 946      5166  LOAD_FAST                'wordNextNextNext'
             5168  LOAD_STR                 'mañana'
             5170  COMPARE_OP               ==
         5172_5174  POP_JUMP_IF_FALSE  5190  'to 5190'

 L. 947      5176  LOAD_STR                 'am'
             5178  STORE_FAST               'remainder'

 L. 948      5180  LOAD_FAST                'used'
             5182  LOAD_CONST               1
             5184  INPLACE_ADD      
             5186  STORE_FAST               'used'
             5188  JUMP_FORWARD       5246  'to 5246'
           5190_0  COME_FROM          5172  '5172'
           5190_1  COME_FROM          4360  '4360'

 L. 949      5190  LOAD_FAST                'wordNextNextNext'
             5192  LOAD_STR                 'noche'
             5194  COMPARE_OP               ==
         5196_5198  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 950      5200  LOAD_CONST               0
             5202  LOAD_FAST                'strHH'
             5204  DUP_TOP          
             5206  ROT_THREE        
             5208  COMPARE_OP               >
         5210_5212  POP_JUMP_IF_FALSE  5224  'to 5224'
             5214  LOAD_CONST               6
             5216  COMPARE_OP               >
         5218_5220  POP_JUMP_IF_FALSE  5234  'to 5234'
             5222  JUMP_FORWARD       5228  'to 5228'
           5224_0  COME_FROM          5210  '5210'
             5224  POP_TOP          
             5226  JUMP_FORWARD       5234  'to 5234'
           5228_0  COME_FROM          5222  '5222'

 L. 951      5228  LOAD_STR                 'am'
             5230  STORE_FAST               'remainder'
             5232  JUMP_FORWARD       5238  'to 5238'
           5234_0  COME_FROM          5226  '5226'
           5234_1  COME_FROM          5218  '5218'

 L. 953      5234  LOAD_STR                 'pm'
             5236  STORE_FAST               'remainder'
           5238_0  COME_FROM          5232  '5232'

 L. 954      5238  LOAD_FAST                'used'
             5240  LOAD_CONST               1
             5242  INPLACE_ADD      
             5244  STORE_FAST               'used'
           5246_0  COME_FROM          5188  '5188'
           5246_1  COME_FROM          5164  '5164'
             5246  JUMP_FORWARD       5302  'to 5302'
           5248_0  COME_FROM          5102  '5102'
           5248_1  COME_FROM          5092  '5092'

 L. 956      5248  LOAD_FAST                'wordNext'
           5250_0  COME_FROM          4420  '4420'
             5250  LOAD_CONST               0
             5252  BINARY_SUBSCR    
             5254  LOAD_METHOD              isdigit
             5256  CALL_METHOD_0         0  '0 positional arguments'
         5258_5260  POP_JUMP_IF_FALSE  5298  'to 5298'

 L. 957      5262  LOAD_FAST                'word'
             5264  STORE_FAST               'strHH'

 L. 958      5266  LOAD_FAST                'wordNext'
             5268  STORE_FAST               'strMM'

 L. 959      5270  LOAD_FAST                'used'
             5272  LOAD_CONST               1
             5274  INPLACE_ADD      
             5276  STORE_FAST               'used'

 L. 960      5278  LOAD_FAST                'wordNextNext'
             5280  LOAD_STR                 'hora'
             5282  COMPARE_OP               ==
         5284_5286  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 961      5288  LOAD_FAST                'used'
             5290  LOAD_CONST               1
             5292  INPLACE_ADD      
             5294  STORE_FAST               'used'
             5296  JUMP_FORWARD       5302  'to 5302'
           5298_0  COME_FROM          5258  '5258'

 L. 963      5298  LOAD_CONST               False
             5300  STORE_FAST               'isTime'
           5302_0  COME_FROM          5296  '5296'
           5302_1  COME_FROM          5284  '5284'
           5302_2  COME_FROM          5246  '5246'
           5302_3  COME_FROM          5196  '5196'
           5302_4  COME_FROM          5130  '5130'
           5302_5  COME_FROM          5120  '5120'
           5302_6  COME_FROM          5074  '5074'
           5302_7  COME_FROM          5062  '5062'
           5302_8  COME_FROM          5010  '5010'
           5302_9  COME_FROM          4972  '4972'
          5302_10  COME_FROM          4934  '4934'
          5302_11  COME_FROM          4854  '4854'
          5302_12  COME_FROM          4842  '4842'
          5302_13  COME_FROM          4780  '4780'
          5302_14  COME_FROM          4734  '4734'
          5302_15  COME_FROM          4688  '4688'
          5302_16  COME_FROM          4632  '4632'
          5302_17  COME_FROM          4470  '4470'
          5302_18  COME_FROM          4458  '4458'
          5302_19  COME_FROM          4438  '4438'
          5302_20  COME_FROM          4428  '4428'
          5302_21  COME_FROM          4156  '4156'

 L. 965      5302  LOAD_FAST                'strHH'
         5304_5306  POP_JUMP_IF_FALSE  5316  'to 5316'
             5308  LOAD_GLOBAL              int
             5310  LOAD_FAST                'strHH'
             5312  CALL_FUNCTION_1       1  '1 positional argument'
             5314  JUMP_FORWARD       5318  'to 5318'
           5316_0  COME_FROM          5304  '5304'
             5316  LOAD_CONST               0
           5318_0  COME_FROM          5314  '5314'
             5318  STORE_FAST               'strHH'

 L. 966      5320  LOAD_FAST                'strMM'
         5322_5324  POP_JUMP_IF_FALSE  5334  'to 5334'
             5326  LOAD_GLOBAL              int
             5328  LOAD_FAST                'strMM'
             5330  CALL_FUNCTION_1       1  '1 positional argument'
             5332  JUMP_FORWARD       5336  'to 5336'
           5334_0  COME_FROM          5322  '5322'
             5334  LOAD_CONST               0
           5336_0  COME_FROM          5332  '5332'
             5336  STORE_FAST               'strMM'

 L. 967      5338  LOAD_FAST                'remainder'
             5340  LOAD_STR                 'pm'
             5342  COMPARE_OP               ==
         5344_5346  POP_JUMP_IF_FALSE  5384  'to 5384'

 L. 968      5348  LOAD_CONST               0
             5350  LOAD_FAST                'strHH'
             5352  DUP_TOP          
             5354  ROT_THREE        
             5356  COMPARE_OP               <
         5358_5360  POP_JUMP_IF_FALSE  5372  'to 5372'
             5362  LOAD_CONST               12
             5364  COMPARE_OP               <
         5366_5368  POP_JUMP_IF_FALSE  5384  'to 5384'
             5370  JUMP_FORWARD       5376  'to 5376'
           5372_0  COME_FROM          5358  '5358'
             5372  POP_TOP          
             5374  JUMP_FORWARD       5384  'to 5384'
           5376_0  COME_FROM          5370  '5370'
             5376  LOAD_FAST                'strHH'
             5378  LOAD_CONST               12
             5380  BINARY_ADD       
             5382  JUMP_FORWARD       5386  'to 5386'
           5384_0  COME_FROM          5374  '5374'
           5384_1  COME_FROM          5366  '5366'
           5384_2  COME_FROM          5344  '5344'
             5384  LOAD_FAST                'strHH'
           5386_0  COME_FROM          5382  '5382'
             5386  STORE_FAST               'strHH'

 L. 969      5388  LOAD_FAST                'remainder'
             5390  LOAD_STR                 'am'
             5392  COMPARE_OP               ==
         5394_5396  POP_JUMP_IF_FALSE  5434  'to 5434'

 L. 970      5398  LOAD_CONST               0
             5400  LOAD_FAST                'strHH'
             5402  DUP_TOP          
             5404  ROT_THREE        
             5406  COMPARE_OP               <
         5408_5410  POP_JUMP_IF_FALSE  5422  'to 5422'
             5412  LOAD_CONST               12
             5414  COMPARE_OP               >=
         5416_5418  POP_JUMP_IF_FALSE  5434  'to 5434'
             5420  JUMP_FORWARD       5426  'to 5426'
           5422_0  COME_FROM          5408  '5408'
             5422  POP_TOP          
             5424  JUMP_FORWARD       5434  'to 5434'
           5426_0  COME_FROM          5420  '5420'
             5426  LOAD_FAST                'strHH'
             5428  LOAD_CONST               12
             5430  BINARY_SUBTRACT  
             5432  JUMP_FORWARD       5436  'to 5436'
           5434_0  COME_FROM          5424  '5424'
           5434_1  COME_FROM          5416  '5416'
           5434_2  COME_FROM          5394  '5394'
             5434  LOAD_FAST                'strHH'
           5436_0  COME_FROM          5432  '5432'
             5436  STORE_FAST               'strHH'

 L. 971      5438  LOAD_FAST                'strHH'
             5440  LOAD_CONST               24
             5442  COMPARE_OP               >
         5444_5446  POP_JUMP_IF_TRUE   5458  'to 5458'
             5448  LOAD_FAST                'strMM'
             5450  LOAD_CONST               59
             5452  COMPARE_OP               >
         5454_5456  POP_JUMP_IF_FALSE  5466  'to 5466'
           5458_0  COME_FROM          5444  '5444'

 L. 972      5458  LOAD_CONST               False
             5460  STORE_FAST               'isTime'

 L. 973      5462  LOAD_CONST               0
             5464  STORE_FAST               'used'
           5466_0  COME_FROM          5454  '5454'

 L. 974      5466  LOAD_FAST                'isTime'
         5468_5470  POP_JUMP_IF_FALSE  5496  'to 5496'

 L. 975      5472  LOAD_FAST                'strHH'
             5474  LOAD_CONST               1
             5476  BINARY_MULTIPLY  
             5478  STORE_DEREF              'hrAbs'

 L. 976      5480  LOAD_FAST                'strMM'
             5482  LOAD_CONST               1
             5484  BINARY_MULTIPLY  
             5486  STORE_DEREF              'minAbs'

 L. 977      5488  LOAD_FAST                'used'
             5490  LOAD_CONST               1
             5492  INPLACE_ADD      
             5494  STORE_FAST               'used'
           5496_0  COME_FROM          5468  '5468'
           5496_1  COME_FROM          3932  '3932'
           5496_2  COME_FROM          3918  '3918'
           5496_3  COME_FROM          3730  '3730'
           5496_4  COME_FROM          3698  '3698'
           5496_5  COME_FROM          3666  '3666'
           5496_6  COME_FROM          3624  '3624'
           5496_7  COME_FROM          3582  '3582'
           5496_8  COME_FROM          3540  '3540'
           5496_9  COME_FROM          3508  '3508'
          5496_10  COME_FROM          3476  '3476'
          5496_11  COME_FROM          3440  '3440'

 L. 979      5496  LOAD_FAST                'used'
             5498  LOAD_CONST               0
             5500  COMPARE_OP               >
         5502_5504  POP_JUMP_IF_FALSE  3226  'to 3226'

 L. 981      5506  SETUP_LOOP         5538  'to 5538'
             5508  LOAD_GLOBAL              range
             5510  LOAD_FAST                'used'
             5512  CALL_FUNCTION_1       1  '1 positional argument'
             5514  GET_ITER         
             5516  FOR_ITER           5536  'to 5536'
             5518  STORE_FAST               'i'

 L. 982      5520  LOAD_STR                 ''
             5522  LOAD_FAST                'words'
             5524  LOAD_FAST                'idx'
             5526  LOAD_FAST                'i'
             5528  BINARY_ADD       
             5530  STORE_SUBSCR     
         5532_5534  JUMP_BACK          5516  'to 5516'
             5536  POP_BLOCK        
           5538_0  COME_FROM_LOOP     5506  '5506'

 L. 984      5538  LOAD_FAST                'wordPrev'
             5540  LOAD_STR                 'en'
             5542  COMPARE_OP               ==
         5544_5546  POP_JUMP_IF_TRUE   5558  'to 5558'
             5548  LOAD_FAST                'wordPrev'
             5550  LOAD_STR                 'punto'
             5552  COMPARE_OP               ==
         5554_5556  POP_JUMP_IF_FALSE  5572  'to 5572'
           5558_0  COME_FROM          5544  '5544'

 L. 985      5558  LOAD_STR                 ''
             5560  LOAD_FAST                'words'
             5562  LOAD_FAST                'words'
             5564  LOAD_METHOD              index
             5566  LOAD_FAST                'wordPrev'
             5568  CALL_METHOD_1         1  '1 positional argument'
             5570  STORE_SUBSCR     
           5572_0  COME_FROM          5554  '5554'

 L. 987      5572  LOAD_FAST                'idx'
             5574  LOAD_CONST               0
             5576  COMPARE_OP               >
         5578_5580  POP_JUMP_IF_FALSE  5604  'to 5604'
             5582  LOAD_FAST                'wordPrev'
             5584  LOAD_FAST                'time_indicators'
             5586  COMPARE_OP               in
         5588_5590  POP_JUMP_IF_FALSE  5604  'to 5604'

 L. 988      5592  LOAD_STR                 ''
             5594  LOAD_FAST                'words'
             5596  LOAD_FAST                'idx'
             5598  LOAD_CONST               1
             5600  BINARY_SUBTRACT  
             5602  STORE_SUBSCR     
           5604_0  COME_FROM          5588  '5588'
           5604_1  COME_FROM          5578  '5578'

 L. 989      5604  LOAD_FAST                'idx'
             5606  LOAD_CONST               1
             5608  COMPARE_OP               >
         5610_5612  POP_JUMP_IF_FALSE  5636  'to 5636'
             5614  LOAD_FAST                'wordPrevPrev'
             5616  LOAD_FAST                'time_indicators'
             5618  COMPARE_OP               in
         5620_5622  POP_JUMP_IF_FALSE  5636  'to 5636'

 L. 990      5624  LOAD_STR                 ''
             5626  LOAD_FAST                'words'
             5628  LOAD_FAST                'idx'
             5630  LOAD_CONST               2
             5632  BINARY_SUBTRACT  
             5634  STORE_SUBSCR     
           5636_0  COME_FROM          5620  '5620'
           5636_1  COME_FROM          5610  '5610'

 L. 992      5636  LOAD_FAST                'idx'
             5638  LOAD_FAST                'used'
             5640  LOAD_CONST               1
             5642  BINARY_SUBTRACT  
             5644  INPLACE_ADD      
             5646  STORE_FAST               'idx'

 L. 993      5648  LOAD_CONST               True
             5650  STORE_DEREF              'found'
         5652_5654  JUMP_BACK          3226  'to 3226'
             5656  POP_BLOCK        
           5658_0  COME_FROM_LOOP     3214  '3214'

 L. 996      5658  LOAD_FAST                'date_found'
         5660_5662  POP_JUMP_IF_TRUE   5668  'to 5668'

 L. 997      5664  LOAD_CONST               None
             5666  RETURN_VALUE     
           5668_0  COME_FROM          5660  '5660'

 L. 999      5668  LOAD_DEREF               'dayOffset'
             5670  LOAD_CONST               False
             5672  COMPARE_OP               is
         5674_5676  POP_JUMP_IF_FALSE  5682  'to 5682'

 L.1000      5678  LOAD_CONST               0
             5680  STORE_DEREF              'dayOffset'
           5682_0  COME_FROM          5674  '5674'

 L.1004      5682  LOAD_FAST                'dateNow'
             5684  STORE_FAST               'extractedDate'

 L.1005      5686  LOAD_FAST                'extractedDate'
             5688  LOAD_ATTR                replace
             5690  LOAD_CONST               0

 L.1006      5692  LOAD_CONST               0

 L.1007      5694  LOAD_CONST               0

 L.1008      5696  LOAD_CONST               0
             5698  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             5700  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5702  STORE_FAST               'extractedDate'

 L.1009      5704  LOAD_DEREF               'datestr'
             5706  LOAD_STR                 ''
             5708  COMPARE_OP               !=
         5710_5712  POP_JUMP_IF_FALSE  6072  'to 6072'

 L.1010      5714  LOAD_STR                 'january'
             5716  LOAD_STR                 'february'
             5718  LOAD_STR                 'march'
             5720  LOAD_STR                 'april'
             5722  LOAD_STR                 'may'
             5724  LOAD_STR                 'june'

 L.1011      5726  LOAD_STR                 'july'
             5728  LOAD_STR                 'august'
             5730  LOAD_STR                 'september'
             5732  LOAD_STR                 'october'
             5734  LOAD_STR                 'november'

 L.1012      5736  LOAD_STR                 'december'
             5738  BUILD_LIST_12        12 
             5740  STORE_FAST               'en_months'

 L.1013      5742  LOAD_STR                 'jan'
             5744  LOAD_STR                 'feb'
             5746  LOAD_STR                 'mar'
             5748  LOAD_STR                 'apr'
             5750  LOAD_STR                 'may'
             5752  LOAD_STR                 'june'
             5754  LOAD_STR                 'july'

 L.1014      5756  LOAD_STR                 'aug'

 L.1015      5758  LOAD_STR                 'sept'
             5760  LOAD_STR                 'oct'
             5762  LOAD_STR                 'nov'
             5764  LOAD_STR                 'dec'
             5766  BUILD_LIST_12        12 
             5768  STORE_FAST               'en_monthsShort'

 L.1016      5770  SETUP_LOOP         5810  'to 5810'
             5772  LOAD_GLOBAL              enumerate
             5774  LOAD_FAST                'en_months'
             5776  CALL_FUNCTION_1       1  '1 positional argument'
             5778  GET_ITER         
             5780  FOR_ITER           5808  'to 5808'
             5782  UNPACK_SEQUENCE_2     2 
             5784  STORE_FAST               'idx'
             5786  STORE_FAST               'en_month'

 L.1017      5788  LOAD_DEREF               'datestr'
             5790  LOAD_METHOD              replace
             5792  LOAD_FAST                'months'
             5794  LOAD_FAST                'idx'
             5796  BINARY_SUBSCR    
             5798  LOAD_FAST                'en_month'
             5800  CALL_METHOD_2         2  '2 positional arguments'
             5802  STORE_DEREF              'datestr'
         5804_5806  JUMP_BACK          5780  'to 5780'
             5808  POP_BLOCK        
           5810_0  COME_FROM_LOOP     5770  '5770'

 L.1018      5810  SETUP_LOOP         5850  'to 5850'
             5812  LOAD_GLOBAL              enumerate
             5814  LOAD_FAST                'en_monthsShort'
             5816  CALL_FUNCTION_1       1  '1 positional argument'
             5818  GET_ITER         
             5820  FOR_ITER           5848  'to 5848'
             5822  UNPACK_SEQUENCE_2     2 
             5824  STORE_FAST               'idx'
             5826  STORE_FAST               'en_month'

 L.1019      5828  LOAD_DEREF               'datestr'
             5830  LOAD_METHOD              replace
             5832  LOAD_FAST                'monthsShort'
             5834  LOAD_FAST                'idx'
             5836  BINARY_SUBSCR    
             5838  LOAD_FAST                'en_month'
             5840  CALL_METHOD_2         2  '2 positional arguments'
             5842  STORE_DEREF              'datestr'
         5844_5846  JUMP_BACK          5820  'to 5820'
             5848  POP_BLOCK        
           5850_0  COME_FROM_LOOP     5810  '5810'

 L.1021      5850  LOAD_GLOBAL              datetime
             5852  LOAD_METHOD              strptime
             5854  LOAD_DEREF               'datestr'
             5856  LOAD_STR                 '%B %d'
             5858  CALL_METHOD_2         2  '2 positional arguments'
             5860  STORE_FAST               'temp'

 L.1022      5862  LOAD_FAST                'temp'
             5864  LOAD_ATTR                replace
             5866  LOAD_CONST               None
             5868  LOAD_CONST               ('tzinfo',)
             5870  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5872  STORE_FAST               'temp'

 L.1023      5874  LOAD_FAST                'hasYear'
         5876_5878  POP_JUMP_IF_TRUE   6026  'to 6026'

 L.1024      5880  LOAD_FAST                'temp'
             5882  LOAD_ATTR                replace
             5884  LOAD_FAST                'extractedDate'
             5886  LOAD_ATTR                year
             5888  LOAD_CONST               ('year',)
             5890  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5892  STORE_FAST               'temp'

 L.1025      5894  LOAD_GLOBAL              print
             5896  LOAD_GLOBAL              gettz
             5898  LOAD_FAST                'temp'
             5900  LOAD_METHOD              tzname
             5902  CALL_METHOD_0         0  '0 positional arguments'
             5904  CALL_FUNCTION_1       1  '1 positional argument'
             5906  CALL_FUNCTION_1       1  '1 positional argument'
             5908  POP_TOP          

 L.1026      5910  LOAD_GLOBAL              print
             5912  LOAD_FAST                'extractedDate'
             5914  LOAD_METHOD              tzname
             5916  CALL_METHOD_0         0  '0 positional arguments'
             5918  LOAD_FAST                'temp'
             5920  LOAD_METHOD              tzname
             5922  CALL_METHOD_0         0  '0 positional arguments'
             5924  CALL_FUNCTION_2       2  '2 positional arguments'
             5926  POP_TOP          

 L.1027      5928  LOAD_FAST                'extractedDate'
             5930  LOAD_FAST                'temp'
             5932  COMPARE_OP               <
         5934_5936  POP_JUMP_IF_FALSE  5980  'to 5980'

 L.1028      5938  LOAD_FAST                'extractedDate'
             5940  LOAD_ATTR                replace
             5942  LOAD_GLOBAL              int
             5944  LOAD_FAST                'currentYear'
             5946  CALL_FUNCTION_1       1  '1 positional argument'

 L.1029      5948  LOAD_GLOBAL              int

 L.1030      5950  LOAD_FAST                'temp'
             5952  LOAD_METHOD              strftime

 L.1031      5954  LOAD_STR                 '%m'
             5956  CALL_METHOD_1         1  '1 positional argument'
             5958  CALL_FUNCTION_1       1  '1 positional argument'

 L.1032      5960  LOAD_GLOBAL              int
             5962  LOAD_FAST                'temp'
             5964  LOAD_METHOD              strftime

 L.1033      5966  LOAD_STR                 '%d'
             5968  CALL_METHOD_1         1  '1 positional argument'
             5970  CALL_FUNCTION_1       1  '1 positional argument'
             5972  LOAD_CONST               ('year', 'month', 'day')
             5974  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5976  STORE_FAST               'extractedDate'
             5978  JUMP_FORWARD       6024  'to 6024'
           5980_0  COME_FROM          5934  '5934'

 L.1035      5980  LOAD_FAST                'extractedDate'
             5982  LOAD_ATTR                replace

 L.1036      5984  LOAD_GLOBAL              int
             5986  LOAD_FAST                'currentYear'
             5988  CALL_FUNCTION_1       1  '1 positional argument'
             5990  LOAD_CONST               1
             5992  BINARY_ADD       

 L.1037      5994  LOAD_GLOBAL              int
             5996  LOAD_FAST                'temp'
             5998  LOAD_METHOD              strftime
             6000  LOAD_STR                 '%m'
             6002  CALL_METHOD_1         1  '1 positional argument'
             6004  CALL_FUNCTION_1       1  '1 positional argument'

 L.1038      6006  LOAD_GLOBAL              int
             6008  LOAD_FAST                'temp'
             6010  LOAD_METHOD              strftime
             6012  LOAD_STR                 '%d'
             6014  CALL_METHOD_1         1  '1 positional argument'
             6016  CALL_FUNCTION_1       1  '1 positional argument'
             6018  LOAD_CONST               ('year', 'month', 'day')
             6020  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6022  STORE_FAST               'extractedDate'
           6024_0  COME_FROM          5978  '5978'
             6024  JUMP_FORWARD       6072  'to 6072'
           6026_0  COME_FROM          5876  '5876'

 L.1040      6026  LOAD_FAST                'extractedDate'
             6028  LOAD_ATTR                replace

 L.1041      6030  LOAD_GLOBAL              int
             6032  LOAD_FAST                'temp'
             6034  LOAD_METHOD              strftime
             6036  LOAD_STR                 '%Y'
             6038  CALL_METHOD_1         1  '1 positional argument'
             6040  CALL_FUNCTION_1       1  '1 positional argument'

 L.1042      6042  LOAD_GLOBAL              int
             6044  LOAD_FAST                'temp'
             6046  LOAD_METHOD              strftime
             6048  LOAD_STR                 '%m'
             6050  CALL_METHOD_1         1  '1 positional argument'
             6052  CALL_FUNCTION_1       1  '1 positional argument'

 L.1043      6054  LOAD_GLOBAL              int
             6056  LOAD_FAST                'temp'
             6058  LOAD_METHOD              strftime
             6060  LOAD_STR                 '%d'
             6062  CALL_METHOD_1         1  '1 positional argument'
             6064  CALL_FUNCTION_1       1  '1 positional argument'
             6066  LOAD_CONST               ('year', 'month', 'day')
             6068  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6070  STORE_FAST               'extractedDate'
           6072_0  COME_FROM          6024  '6024'
           6072_1  COME_FROM          5710  '5710'

 L.1045      6072  LOAD_DEREF               'yearOffset'
             6074  LOAD_CONST               0
             6076  COMPARE_OP               !=
         6078_6080  POP_JUMP_IF_FALSE  6096  'to 6096'

 L.1046      6082  LOAD_FAST                'extractedDate'
             6084  LOAD_GLOBAL              relativedelta
             6086  LOAD_DEREF               'yearOffset'
             6088  LOAD_CONST               ('years',)
             6090  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6092  BINARY_ADD       
             6094  STORE_FAST               'extractedDate'
           6096_0  COME_FROM          6078  '6078'

 L.1047      6096  LOAD_DEREF               'monthOffset'
             6098  LOAD_CONST               0
             6100  COMPARE_OP               !=
         6102_6104  POP_JUMP_IF_FALSE  6120  'to 6120'

 L.1048      6106  LOAD_FAST                'extractedDate'
             6108  LOAD_GLOBAL              relativedelta
             6110  LOAD_DEREF               'monthOffset'
             6112  LOAD_CONST               ('months',)
             6114  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6116  BINARY_ADD       
             6118  STORE_FAST               'extractedDate'
           6120_0  COME_FROM          6102  '6102'

 L.1049      6120  LOAD_DEREF               'dayOffset'
             6122  LOAD_CONST               0
             6124  COMPARE_OP               !=
         6126_6128  POP_JUMP_IF_FALSE  6144  'to 6144'

 L.1050      6130  LOAD_FAST                'extractedDate'
             6132  LOAD_GLOBAL              relativedelta
             6134  LOAD_DEREF               'dayOffset'
             6136  LOAD_CONST               ('days',)
             6138  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6140  BINARY_ADD       
             6142  STORE_FAST               'extractedDate'
           6144_0  COME_FROM          6126  '6126'

 L.1052      6144  LOAD_DEREF               'hrAbs'
             6146  LOAD_CONST               None
             6148  COMPARE_OP               is
         6150_6152  POP_JUMP_IF_FALSE  6182  'to 6182'
             6154  LOAD_DEREF               'minAbs'
             6156  LOAD_CONST               None
             6158  COMPARE_OP               is
         6160_6162  POP_JUMP_IF_FALSE  6182  'to 6182'
             6164  LOAD_FAST                'default_time'
         6166_6168  POP_JUMP_IF_FALSE  6182  'to 6182'

 L.1053      6170  LOAD_FAST                'default_time'
             6172  LOAD_ATTR                hour
             6174  STORE_DEREF              'hrAbs'

 L.1054      6176  LOAD_FAST                'default_time'
             6178  LOAD_ATTR                minute
             6180  STORE_DEREF              'minAbs'
           6182_0  COME_FROM          6166  '6166'
           6182_1  COME_FROM          6160  '6160'
           6182_2  COME_FROM          6150  '6150'

 L.1056      6182  LOAD_DEREF               'hrAbs'
             6184  LOAD_CONST               -1
             6186  COMPARE_OP               !=
         6188_6190  POP_JUMP_IF_FALSE  6282  'to 6282'
             6192  LOAD_DEREF               'minAbs'
             6194  LOAD_CONST               -1
             6196  COMPARE_OP               !=
         6198_6200  POP_JUMP_IF_FALSE  6282  'to 6282'

 L.1057      6202  LOAD_FAST                'extractedDate'
             6204  LOAD_GLOBAL              relativedelta
             6206  LOAD_DEREF               'hrAbs'
         6208_6210  JUMP_IF_TRUE_OR_POP  6214  'to 6214'
             6212  LOAD_CONST               0
           6214_0  COME_FROM          6208  '6208'

 L.1058      6214  LOAD_DEREF               'minAbs'
         6216_6218  JUMP_IF_TRUE_OR_POP  6222  'to 6222'
             6220  LOAD_CONST               0
           6222_0  COME_FROM          6216  '6216'
             6222  LOAD_CONST               ('hours', 'minutes')
             6224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6226  BINARY_ADD       
             6228  STORE_FAST               'extractedDate'

 L.1059      6230  LOAD_DEREF               'hrAbs'
         6232_6234  POP_JUMP_IF_TRUE   6242  'to 6242'
             6236  LOAD_DEREF               'minAbs'
         6238_6240  POP_JUMP_IF_FALSE  6282  'to 6282'
           6242_0  COME_FROM          6232  '6232'
             6242  LOAD_DEREF               'datestr'
             6244  LOAD_STR                 ''
             6246  COMPARE_OP               ==
         6248_6250  POP_JUMP_IF_FALSE  6282  'to 6282'

 L.1060      6252  LOAD_FAST                'daySpecified'
         6254_6256  POP_JUMP_IF_TRUE   6282  'to 6282'
             6258  LOAD_FAST                'dateNow'
             6260  LOAD_FAST                'extractedDate'
             6262  COMPARE_OP               >
         6264_6266  POP_JUMP_IF_FALSE  6282  'to 6282'

 L.1061      6268  LOAD_FAST                'extractedDate'
             6270  LOAD_GLOBAL              relativedelta
             6272  LOAD_CONST               1
             6274  LOAD_CONST               ('days',)
             6276  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6278  BINARY_ADD       
             6280  STORE_FAST               'extractedDate'
           6282_0  COME_FROM          6264  '6264'
           6282_1  COME_FROM          6254  '6254'
           6282_2  COME_FROM          6248  '6248'
           6282_3  COME_FROM          6238  '6238'
           6282_4  COME_FROM          6198  '6198'
           6282_5  COME_FROM          6188  '6188'

 L.1062      6282  LOAD_DEREF               'hrOffset'
             6284  LOAD_CONST               0
             6286  COMPARE_OP               !=
         6288_6290  POP_JUMP_IF_FALSE  6306  'to 6306'

 L.1063      6292  LOAD_FAST                'extractedDate'
             6294  LOAD_GLOBAL              relativedelta
             6296  LOAD_DEREF               'hrOffset'
             6298  LOAD_CONST               ('hours',)
             6300  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6302  BINARY_ADD       
             6304  STORE_FAST               'extractedDate'
           6306_0  COME_FROM          6288  '6288'

 L.1064      6306  LOAD_DEREF               'minOffset'
             6308  LOAD_CONST               0
             6310  COMPARE_OP               !=
         6312_6314  POP_JUMP_IF_FALSE  6330  'to 6330'

 L.1065      6316  LOAD_FAST                'extractedDate'
             6318  LOAD_GLOBAL              relativedelta
             6320  LOAD_DEREF               'minOffset'
             6322  LOAD_CONST               ('minutes',)
             6324  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6326  BINARY_ADD       
             6328  STORE_FAST               'extractedDate'
           6330_0  COME_FROM          6312  '6312'

 L.1066      6330  LOAD_DEREF               'secOffset'
             6332  LOAD_CONST               0
             6334  COMPARE_OP               !=
         6336_6338  POP_JUMP_IF_FALSE  6354  'to 6354'

 L.1067      6340  LOAD_FAST                'extractedDate'
             6342  LOAD_GLOBAL              relativedelta
             6344  LOAD_DEREF               'secOffset'
             6346  LOAD_CONST               ('seconds',)
             6348  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6350  BINARY_ADD       
             6352  STORE_FAST               'extractedDate'
           6354_0  COME_FROM          6336  '6336'

 L.1069      6354  LOAD_STR                 ' '
             6356  LOAD_METHOD              join
             6358  LOAD_FAST                'words'
             6360  CALL_METHOD_1         1  '1 positional argument'
             6362  STORE_FAST               'resultStr'

 L.1070      6364  LOAD_STR                 ' '
             6366  LOAD_METHOD              join
             6368  LOAD_FAST                'resultStr'
             6370  LOAD_METHOD              split
             6372  CALL_METHOD_0         0  '0 positional arguments'
             6374  CALL_METHOD_1         1  '1 positional argument'
             6376  STORE_FAST               'resultStr'

 L.1072      6378  LOAD_FAST                'extractedDate'
             6380  LOAD_FAST                'resultStr'
             6382  BUILD_LIST_2          2 
             6384  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_METHOD_0' instruction at offset 2344


def get_gender_es(word, raw_string=''):
    word = word.rstrip('s')
    gender = False
    words = raw_string.split(' ')
    for idx, w in enumerate(words):
        if w == word and idx != 0:
            previous = words[(idx - 1)]
            gender = get_gender_es(previous)
            break

    if not gender:
        if word[(-1)] == 'a':
            gender = 'f'
        if word[(-1)] == 'o' or word[(-1)] == 'e':
            gender = 'm'
    return gender