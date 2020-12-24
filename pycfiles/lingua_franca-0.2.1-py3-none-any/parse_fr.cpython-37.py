# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_fr.py
# Compiled at: 2020-03-04 07:40:03
# Size of source mod 2**32: 38318 bytes
""" Parse functions for french (fr)

    Todo:
        * extractnumber_fr: ordinal numbers ("cinquième")
        * extractnumber_fr: numbers greater than 999 999 ("cinq millions")
        * extract_datetime_fr: "quatrième lundi de janvier"
        * get_gender_fr
"""
from datetime import datetime
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions, extract_numbers_generic
from lingua_franca.lang.format_fr import pronounce_number_fr
articles_fr = [
 'le', 'la', 'du', 'de', 'les', 'des']
numbers_fr = {'zéro':0, 
 'un':1, 
 'une':1, 
 'deux':2, 
 'trois':3, 
 'quatre':4, 
 'cinq':5, 
 'six':6, 
 'sept':7, 
 'huit':8, 
 'neuf':9, 
 'dix':10, 
 'onze':11, 
 'douze':12, 
 'treize':13, 
 'quatorze':14, 
 'quinze':15, 
 'seize':16, 
 'vingt':20, 
 'trente':30, 
 'quarante':40, 
 'cinquante':50, 
 'soixante':60, 
 'soixante-dix':70, 
 'septante':70, 
 'quatre-vingt':80, 
 'quatre-vingts':80, 
 'octante':80, 
 'huitante':80, 
 'quatre-vingt-dix':90, 
 'nonante':90, 
 'cent':100, 
 'cents':100, 
 'mille':1000, 
 'mil':1000, 
 'millier':1000, 
 'milliers':1000, 
 'million':1000000, 
 'millions':1000000, 
 'milliard':1000000000, 
 'milliards':1000000000}
ordinals_fr = ('er', 're', 'ère', 'nd', 'ndeième', 'ème', 'e')

def number_parse_fr(words, i):
    """ Parses a list of words to find a number
    Takes in a list of words (strings without whitespace) and
    extracts a number that starts at the given index.
    Args:
        words (array): the list to extract a number from
        i (int): the index in words where to look for the number
    Returns:
        tuple with number, index of next word after the number.

        Returns None if no number was found.
    """

    def cte_fr(i, s):
        if i < len(words):
            if s == words[i]:
                return (
                 s, i + 1)

    def number_word_fr(i, mi, ma):
        if i < len(words):
            val = numbers_fr.get(words[i])
            if val is not None:
                if val >= mi:
                    if val <= ma:
                        return (
                         val, i + 1)
                return
            splitWord = words[i].split('-')
            if len(splitWord) > 1:
                val1 = numbers_fr.get(splitWord[0])
                if val1:
                    i1 = 0
                    val2 = 0
                    val3 = 0
                    if val1 < 10:
                        if splitWord[1] == 'cents':
                            val1 = val1 * 100
                            i1 = 2
                    if len(splitWord) > i1:
                        if splitWord[0] == 'quatre':
                            if splitWord[1] == 'vingt':
                                val1 = 80
                                i1 += 2
                    if i1 == 0:
                        i1 = 1
                    if len(splitWord) > i1:
                        if len(splitWord) > i1 + 1 and splitWord[i1] == 'et':
                            val2 = numbers_fr.get(splitWord[(i1 + 1)])
                            if val2 is not None:
                                i1 += 2
        else:
            if splitWord[i1] == 'dix' and len(splitWord) > i1 + 1:
                val2 = numbers_fr.get(splitWord[(i1 + 1)])
                if val2 is not None:
                    val2 += 10
                    i1 += 2
            else:
                val2 = numbers_fr.get(splitWord[i1])
            if val2 is not None:
                i1 += 1
                if len(splitWord) > i1:
                    val3 = numbers_fr.get(splitWord[i1])
                    if val3 is not None:
                        i1 += 1
                if val2:
                    if val3:
                        val = val1 + val2 + val3
                    else:
                        val = val1 + val2
                else:
                    return
            elif i1 == len(splitWord):
                if val:
                    if ma >= val >= mi:
                        return (
                         val, i + 1)

    def number_1_99_fr(i):
        result1 = number_word_fr(i, 1, 16)
        if result1:
            return result1
        result1 = number_word_fr(i, 10, 99)
        if result1:
            val1, i1 = result1
            result2 = cte_fr(i1, 'et')
            if result2:
                i2 = result2[1]
                result3 = number_word_fr(i2, 1, 11)
                if result3:
                    val3, i3 = result3
                    return (val1 + val3, i3)
            return result1

    def number_1_999_fr(i):
        result = number_word_fr(i, 100, 100)
        if not result:
            resultH1 = number_word_fr(i, 2, 9)
            if resultH1:
                valH1, iH1 = resultH1
                resultH2 = number_word_fr(iH1, 100, 100)
                if resultH2:
                    iH2 = resultH2[1]
                    result = (valH1 * 100, iH2)
        if result:
            val1, i1 = result
            result2 = number_1_99_fr(i1)
            if result2:
                val2, i2 = result2
                return (val1 + val2, i2)
            return result
        result = number_word_fr(i, 101, 999)
        if result:
            return result
        result = number_1_99_fr(i)
        if result:
            return result

    def number_1_999999_fr(i):
        result1 = number_word_fr(i, 0, 0)
        if result1:
            return result1
        result1 = number_1_999_fr(i)
        if result1:
            val1, i1 = result1
        else:
            val1 = 1
            i1 = i
        result2 = number_word_fr(i1, 1000, 1000)
        if result2:
            i2 = result2[1]
            result3 = number_1_999_fr(i2)
            if result3:
                val3, i3 = result3
                return (val1 * 1000 + val3, i3)
            return (val1 * 1000, i2)
        else:
            if result1:
                return result1

    return number_1_999999_fr(i)


def getOrdinal_fr(word):
    """ Get the ordinal number
    Takes in a word (string without whitespace) and
    extracts the ordinal number.
    Args:
        word (string): the word to extract the number from
    Returns:
        number (int)

        Returns None if no ordinal number was found.
    """
    if word:
        for ordinal in ordinals_fr:
            if word[0].isdigit() and ordinal in word:
                result = word.replace(ordinal, '')
                if result.isdigit():
                    return int(result)


def number_ordinal_fr(words, i):
    """ Find an ordinal number in a list of words
    Takes in a list of words (strings without whitespace) and
    extracts an ordinal number that starts at the given index.
    Args:
        words (array): the list to extract a number from
        i (int): the index in words where to look for the ordinal number
    Returns:
        tuple with ordinal number (str),
        index of next word after the number (int).

        Returns None if no ordinal number was found.
    """
    val1 = None
    strOrd = ''
    val1 = getOrdinal_fr(words[i])
    if val1 is not None:
        if val1 == 1:
            strOrd = '1er'
        else:
            strOrd = str(val1) + 'e'
        return (
         strOrd, i + 1)
        result = number_parse_fr(words, i)
        if result:
            val1, i = result
        else:
            val1 = 0
        if i < len(words):
            word = words[i]
            if word in ('premier', 'première'):
                strOrd = '1er'
        elif word == 'second':
            strOrd = '2e'
        else:
            if word.endswith('ième'):
                val2 = None
                word = word[:-4]
                if word == 'cent':
                    if val1:
                        strOrd = str(val1 * 100) + 'e'
            else:
                strOrd = '100e'
    else:
        pass
    if word == 'mill':
        if val1:
            strOrd = str(val1 * 1000) + 'e'
        else:
            strOrd = '1000e'
    else:
        if word.endswith('cinqu'):
            word = word[:-1]
        else:
            if word.endswith('neuv'):
                word = word[:-1] + 'f'
            result = number_parse_fr([word], 0)
            if not result:
                word = word + 'e'
                result = number_parse_fr([word], 0)
            if result:
                val2, i = result
            if val2 is not None:
                strOrd = str(val1 + val2) + 'e'
            if strOrd:
                return (
                 strOrd, i + 1)


def extractnumber_fr(text, short_scale=True, ordinals=False):
    """Takes in a string and extracts a number.
    Args:
        text (str): the string to extract a number from
    Returns:
        (str): The number extracted or the original text.
    """
    text = normalize_fr(text, False)
    aWords = text.split()
    count = 0
    result = None
    add = False
    while count < len(aWords):
        val = None
        word = aWords[count]
        wordNext = ''
        wordPrev = ''
        if count < len(aWords) - 1:
            wordNext = aWords[(count + 1)]
        if count > 0:
            wordPrev = aWords[(count - 1)]
        if word in articles_fr:
            count += 1
            continue
        if word in ('et', 'plus', '+'):
            count += 1
            add = True
            continue
        if word.isdigit():
            val = int(word)
            count += 1
        else:
            if is_numeric(word):
                val = float(word)
                count += 1
            else:
                if wordPrev in articles_fr and getOrdinal_fr(word):
                    val = getOrdinal_fr(word)
                    count += 1
                else:
                    if isFractional_fr(word):
                        val = isFractional_fr(word)
                        count += 1
                    else:
                        if val:
                            if wordNext:
                                valNext = isFractional_fr(wordNext)
                                if valNext:
                                    val = float(val) * valNext
                                    count += 1
                        val or count += 1
                        aPieces = word.split('/')
                        if look_for_fractions(aPieces):
                            val = float(aPieces[0]) / float(aPieces[1])
                        if wordNext == 'virgule':
                            zeros = 0
                            newWords = aWords[count + 1:]
                            for word in newWords:
                                if word == 'zéro' or word == '0':
                                    zeros += 1
                                else:
                                    break

                            afterDotVal = None
                            if newWords[zeros].isdigit():
                                afterDotVal = newWords[zeros]
                                countDot = count + zeros + 2
                            if afterDotVal:
                                count = countDot
                                if not val:
                                    val = 0
                                afterDotString = zeros * '0' + afterDotVal
                                val = float(str(val) + '.' + afterDotString)
        if val:
            if add:
                result += val
                add = False
            else:
                result = val

    return result or False


def extract_datetime_fr--- This code section failed: ---

 L. 474         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_fr.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 489         8  LOAD_CLOSURE             'datestr'
               10  LOAD_CLOSURE             'dayOffset'
               12  LOAD_CLOSURE             'found'
               14  LOAD_CLOSURE             'hrAbs'
               16  LOAD_CLOSURE             'hrOffset'
               18  LOAD_CLOSURE             'isTime'
               20  LOAD_CLOSURE             'minAbs'
               22  LOAD_CLOSURE             'minOffset'
               24  LOAD_CLOSURE             'monthOffset'
               26  LOAD_CLOSURE             'secOffset'
               28  LOAD_CLOSURE             'yearOffset'
               30  BUILD_TUPLE_11       11 
               32  LOAD_CODE                <code_object date_found>
               34  LOAD_STR                 'extract_datetime_fr.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 498        40  LOAD_FAST                'string'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'currentDate'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 499        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 501        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 502        60  LOAD_CONST               False
               62  STORE_FAST               'daySpecified'

 L. 503        64  LOAD_CONST               False
               66  STORE_DEREF              'dayOffset'

 L. 504        68  LOAD_CONST               0
               70  STORE_DEREF              'monthOffset'

 L. 505        72  LOAD_CONST               0
               74  STORE_DEREF              'yearOffset'

 L. 506        76  LOAD_FAST                'currentDate'
               78  STORE_FAST               'dateNow'

 L. 507        80  LOAD_FAST                'dateNow'
               82  LOAD_METHOD              strftime
               84  LOAD_STR                 '%w'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'today'

 L. 508        90  LOAD_FAST                'dateNow'
               92  LOAD_METHOD              strftime
               94  LOAD_STR                 '%Y'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  STORE_FAST               'currentYear'

 L. 509       100  LOAD_CONST               False
              102  STORE_FAST               'fromFlag'

 L. 510       104  LOAD_STR                 ''
              106  STORE_DEREF              'datestr'

 L. 511       108  LOAD_CONST               False
              110  STORE_FAST               'hasYear'

 L. 512       112  LOAD_STR                 ''
              114  STORE_FAST               'timeQualifier'

 L. 514       116  LOAD_STR                 'matin'
              118  LOAD_STR                 'après-midi'
              120  LOAD_STR                 'soir'
              122  LOAD_STR                 'nuit'
              124  BUILD_LIST_4          4 
              126  STORE_FAST               'timeQualifiersList'

 L. 515       128  LOAD_STR                 'dans'
              130  LOAD_STR                 'après'
              132  BUILD_LIST_2          2 
              134  STORE_FAST               'words_in'

 L. 516       136  LOAD_STR                 'à'
              138  LOAD_STR                 'dès'
              140  LOAD_STR                 'autour'
              142  LOAD_STR                 'vers'
              144  LOAD_STR                 'environs'
              146  LOAD_STR                 'ce'

 L. 517       148  LOAD_STR                 'cette'
              150  BUILD_LIST_7          7 
              152  LOAD_FAST                'words_in'
              154  BINARY_ADD       
              156  STORE_FAST               'markers'

 L. 518       158  LOAD_STR                 'lundi'
              160  LOAD_STR                 'mardi'
              162  LOAD_STR                 'mercredi'

 L. 519       164  LOAD_STR                 'jeudi'
              166  LOAD_STR                 'vendredi'
              168  LOAD_STR                 'samedi'
              170  LOAD_STR                 'dimanche'
              172  BUILD_LIST_7          7 
              174  STORE_FAST               'days'

 L. 520       176  LOAD_STR                 'janvier'
              178  LOAD_STR                 'février'
              180  LOAD_STR                 'mars'
              182  LOAD_STR                 'avril'
              184  LOAD_STR                 'mai'
              186  LOAD_STR                 'juin'

 L. 521       188  LOAD_STR                 'juillet'
              190  LOAD_STR                 'août'
              192  LOAD_STR                 'septembre'
              194  LOAD_STR                 'octobre'
              196  LOAD_STR                 'novembre'

 L. 522       198  LOAD_STR                 'décembre'
              200  BUILD_LIST_12        12 
              202  STORE_FAST               'months'

 L. 523       204  LOAD_STR                 'jan'
              206  LOAD_STR                 'fév'
              208  LOAD_STR                 'mar'
              210  LOAD_STR                 'avr'
              212  LOAD_STR                 'mai'
              214  LOAD_STR                 'juin'
              216  LOAD_STR                 'juil'
              218  LOAD_STR                 'aoû'

 L. 524       220  LOAD_STR                 'sept'
              222  LOAD_STR                 'oct'
              224  LOAD_STR                 'nov'
              226  LOAD_STR                 'déc'
              228  BUILD_LIST_12        12 
              230  STORE_FAST               'monthsShort'

 L. 526       232  LOAD_STR                 'january'
              234  LOAD_STR                 'february'
              236  LOAD_STR                 'march'
              238  LOAD_STR                 'april'
              240  LOAD_STR                 'may'
              242  LOAD_STR                 'june'

 L. 527       244  LOAD_STR                 'july'
              246  LOAD_STR                 'august'
              248  LOAD_STR                 'september'
              250  LOAD_STR                 'october'
              252  LOAD_STR                 'november'

 L. 528       254  LOAD_STR                 'december'
              256  BUILD_LIST_12        12 
              258  STORE_FAST               'months_en'

 L. 530       260  LOAD_FAST                'clean_string'
              262  LOAD_FAST                'string'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  STORE_FAST               'words'

 L. 532   268_270  SETUP_LOOP         1740  'to 1740'
              272  LOAD_GLOBAL              enumerate
              274  LOAD_FAST                'words'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  GET_ITER         
            280_0  COME_FROM          1596  '1596'
          280_282  FOR_ITER           1738  'to 1738'
              284  UNPACK_SEQUENCE_2     2 
              286  STORE_FAST               'idx'
              288  STORE_FAST               'word'

 L. 533       290  LOAD_FAST                'word'
              292  LOAD_STR                 ''
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_FALSE   304  'to 304'

 L. 534   300_302  CONTINUE            280  'to 280'
            304_0  COME_FROM           296  '296'

 L. 535       304  LOAD_FAST                'idx'
              306  LOAD_CONST               2
              308  COMPARE_OP               >
          310_312  POP_JUMP_IF_FALSE   326  'to 326'
              314  LOAD_FAST                'words'
              316  LOAD_FAST                'idx'
              318  LOAD_CONST               3
              320  BINARY_SUBTRACT  
              322  BINARY_SUBSCR    
              324  JUMP_FORWARD        328  'to 328'
            326_0  COME_FROM           310  '310'
              326  LOAD_STR                 ''
            328_0  COME_FROM           324  '324'
              328  STORE_FAST               'wordPrevPrevPrev'

 L. 536       330  LOAD_FAST                'idx'
              332  LOAD_CONST               1
              334  COMPARE_OP               >
          336_338  POP_JUMP_IF_FALSE   352  'to 352'
              340  LOAD_FAST                'words'
              342  LOAD_FAST                'idx'
              344  LOAD_CONST               2
              346  BINARY_SUBTRACT  
              348  BINARY_SUBSCR    
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           336  '336'
              352  LOAD_STR                 ''
            354_0  COME_FROM           350  '350'
              354  STORE_FAST               'wordPrevPrev'

 L. 537       356  LOAD_FAST                'idx'
              358  LOAD_CONST               0
              360  COMPARE_OP               >
          362_364  POP_JUMP_IF_FALSE   378  'to 378'
              366  LOAD_FAST                'words'
              368  LOAD_FAST                'idx'
              370  LOAD_CONST               1
              372  BINARY_SUBTRACT  
              374  BINARY_SUBSCR    
              376  JUMP_FORWARD        380  'to 380'
            378_0  COME_FROM           362  '362'
              378  LOAD_STR                 ''
            380_0  COME_FROM           376  '376'
              380  STORE_FAST               'wordPrev'

 L. 538       382  LOAD_FAST                'idx'
              384  LOAD_CONST               1
              386  BINARY_ADD       
              388  LOAD_GLOBAL              len
              390  LOAD_FAST                'words'
              392  CALL_FUNCTION_1       1  '1 positional argument'
              394  COMPARE_OP               <
          396_398  POP_JUMP_IF_FALSE   412  'to 412'
              400  LOAD_FAST                'words'
              402  LOAD_FAST                'idx'
              404  LOAD_CONST               1
              406  BINARY_ADD       
              408  BINARY_SUBSCR    
              410  JUMP_FORWARD        414  'to 414'
            412_0  COME_FROM           396  '396'
              412  LOAD_STR                 ''
            414_0  COME_FROM           410  '410'
              414  STORE_FAST               'wordNext'

 L. 539       416  LOAD_FAST                'idx'
              418  LOAD_CONST               2
              420  BINARY_ADD       
              422  LOAD_GLOBAL              len
              424  LOAD_FAST                'words'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  COMPARE_OP               <
          430_432  POP_JUMP_IF_FALSE   446  'to 446'
              434  LOAD_FAST                'words'
              436  LOAD_FAST                'idx'
              438  LOAD_CONST               2
              440  BINARY_ADD       
              442  BINARY_SUBSCR    
              444  JUMP_FORWARD        448  'to 448'
            446_0  COME_FROM           430  '430'
              446  LOAD_STR                 ''
            448_0  COME_FROM           444  '444'
              448  STORE_FAST               'wordNextNext'

 L. 541       450  LOAD_FAST                'idx'
              452  STORE_FAST               'start'

 L. 542       454  LOAD_CONST               0
              456  STORE_FAST               'used'

 L. 544       458  LOAD_FAST                'word'
              460  LOAD_FAST                'timeQualifiersList'
              462  COMPARE_OP               in
          464_466  POP_JUMP_IF_FALSE   502  'to 502'

 L. 545       468  LOAD_FAST                'word'
              470  STORE_FAST               'timeQualifier'

 L. 546       472  LOAD_CONST               1
              474  STORE_FAST               'used'

 L. 547       476  LOAD_FAST                'wordPrev'
              478  LOAD_CONST               ('ce', 'cet', 'cette')
              480  COMPARE_OP               in
          482_484  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 548       486  LOAD_CONST               2
              488  STORE_FAST               'used'

 L. 549       490  LOAD_FAST                'start'
              492  LOAD_CONST               1
              494  INPLACE_SUBTRACT 
              496  STORE_FAST               'start'
          498_500  JUMP_FORWARD       1298  'to 1298'
            502_0  COME_FROM           464  '464'

 L. 551       502  LOAD_FAST                'word'
              504  LOAD_STR                 "aujourd'hui"
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   534  'to 534'
              512  LOAD_FAST                'fromFlag'
          514_516  POP_JUMP_IF_TRUE    534  'to 534'

 L. 552       518  LOAD_CONST               0
              520  STORE_DEREF              'dayOffset'

 L. 553       522  LOAD_FAST                'used'
              524  LOAD_CONST               1
              526  INPLACE_ADD      
              528  STORE_FAST               'used'
          530_532  JUMP_FORWARD       1298  'to 1298'
            534_0  COME_FROM           514  '514'
            534_1  COME_FROM           508  '508'

 L. 554       534  LOAD_FAST                'word'
              536  LOAD_STR                 'demain'
              538  COMPARE_OP               ==
          540_542  POP_JUMP_IF_FALSE   566  'to 566'
              544  LOAD_FAST                'fromFlag'
          546_548  POP_JUMP_IF_TRUE    566  'to 566'

 L. 555       550  LOAD_CONST               1
              552  STORE_DEREF              'dayOffset'

 L. 556       554  LOAD_FAST                'used'
              556  LOAD_CONST               1
              558  INPLACE_ADD      
              560  STORE_FAST               'used'
          562_564  JUMP_FORWARD       1298  'to 1298'
            566_0  COME_FROM           546  '546'
            566_1  COME_FROM           540  '540'

 L. 557       566  LOAD_FAST                'word'
              568  LOAD_STR                 'après-demain'
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE   598  'to 598'
              576  LOAD_FAST                'fromFlag'
          578_580  POP_JUMP_IF_TRUE    598  'to 598'

 L. 558       582  LOAD_CONST               2
              584  STORE_DEREF              'dayOffset'

 L. 559       586  LOAD_FAST                'used'
              588  LOAD_CONST               1
              590  INPLACE_ADD      
              592  STORE_FAST               'used'
          594_596  JUMP_FORWARD       1298  'to 1298'
            598_0  COME_FROM           578  '578'
            598_1  COME_FROM           572  '572'

 L. 561       598  LOAD_FAST                'word'
              600  LOAD_CONST               ('jour', 'jours')
              602  COMPARE_OP               in
          604_606  POP_JUMP_IF_FALSE   690  'to 690'

 L. 562       608  LOAD_FAST                'wordPrev'
              610  LOAD_METHOD              isdigit
              612  CALL_METHOD_0         0  '0 positional arguments'
          614_616  POP_JUMP_IF_FALSE   644  'to 644'

 L. 563       618  LOAD_DEREF               'dayOffset'
              620  LOAD_GLOBAL              int
              622  LOAD_FAST                'wordPrev'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  INPLACE_ADD      
              628  STORE_DEREF              'dayOffset'

 L. 564       630  LOAD_FAST                'start'
              632  LOAD_CONST               1
              634  INPLACE_SUBTRACT 
              636  STORE_FAST               'start'

 L. 565       638  LOAD_CONST               2
              640  STORE_FAST               'used'
              642  JUMP_FORWARD       1298  'to 1298'
            644_0  COME_FROM           614  '614'

 L. 567       644  LOAD_GLOBAL              getOrdinal_fr
              646  LOAD_FAST                'wordPrev'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  LOAD_CONST               None
              652  COMPARE_OP               is-not
          654_656  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 568       658  LOAD_DEREF               'dayOffset'
              660  LOAD_GLOBAL              getOrdinal_fr
              662  LOAD_FAST                'wordPrev'
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  LOAD_CONST               1
              668  BINARY_SUBTRACT  
              670  INPLACE_ADD      
              672  STORE_DEREF              'dayOffset'

 L. 569       674  LOAD_FAST                'start'
              676  LOAD_CONST               1
              678  INPLACE_SUBTRACT 
              680  STORE_FAST               'start'

 L. 570       682  LOAD_CONST               2
              684  STORE_FAST               'used'
          686_688  JUMP_FORWARD       1298  'to 1298'
            690_0  COME_FROM           604  '604'

 L. 571       690  LOAD_FAST                'word'
              692  LOAD_CONST               ('semaine', 'semaines')
              694  COMPARE_OP               in
          696_698  POP_JUMP_IF_FALSE   792  'to 792'
              700  LOAD_FAST                'fromFlag'
          702_704  POP_JUMP_IF_TRUE    792  'to 792'

 L. 572       706  LOAD_FAST                'wordPrev'
              708  LOAD_CONST               0
              710  BINARY_SUBSCR    
              712  LOAD_METHOD              isdigit
              714  CALL_METHOD_0         0  '0 positional arguments'
          716_718  POP_JUMP_IF_FALSE   750  'to 750'

 L. 573       720  LOAD_DEREF               'dayOffset'
              722  LOAD_GLOBAL              int
              724  LOAD_FAST                'wordPrev'
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  LOAD_CONST               7
              730  BINARY_MULTIPLY  
              732  INPLACE_ADD      
              734  STORE_DEREF              'dayOffset'

 L. 574       736  LOAD_FAST                'start'
              738  LOAD_CONST               1
              740  INPLACE_SUBTRACT 
              742  STORE_FAST               'start'

 L. 575       744  LOAD_CONST               2
              746  STORE_FAST               'used'
              748  JUMP_FORWARD       1298  'to 1298'
            750_0  COME_FROM           716  '716'

 L. 576       750  LOAD_FAST                'wordNext'
              752  LOAD_CONST               ('prochaine', 'suivante')
              754  COMPARE_OP               in
          756_758  POP_JUMP_IF_FALSE   770  'to 770'

 L. 577       760  LOAD_CONST               7
              762  STORE_DEREF              'dayOffset'

 L. 578       764  LOAD_CONST               2
              766  STORE_FAST               'used'
              768  JUMP_FORWARD       1298  'to 1298'
            770_0  COME_FROM           756  '756'

 L. 579       770  LOAD_FAST                'wordNext'
              772  LOAD_CONST               ('dernière', 'précédente')
              774  COMPARE_OP               in
          776_778  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 580       780  LOAD_CONST               -7
              782  STORE_DEREF              'dayOffset'

 L. 581       784  LOAD_CONST               2
              786  STORE_FAST               'used'
          788_790  JUMP_FORWARD       1298  'to 1298'
            792_0  COME_FROM           702  '702'
            792_1  COME_FROM           696  '696'

 L. 583       792  LOAD_FAST                'word'
              794  LOAD_STR                 'mois'
              796  COMPARE_OP               ==
          798_800  POP_JUMP_IF_FALSE   886  'to 886'
              802  LOAD_FAST                'fromFlag'
          804_806  POP_JUMP_IF_TRUE    886  'to 886'

 L. 584       808  LOAD_FAST                'wordPrev'
              810  LOAD_CONST               0
              812  BINARY_SUBSCR    
              814  LOAD_METHOD              isdigit
              816  CALL_METHOD_0         0  '0 positional arguments'
          818_820  POP_JUMP_IF_FALSE   844  'to 844'

 L. 585       822  LOAD_GLOBAL              int
              824  LOAD_FAST                'wordPrev'
              826  CALL_FUNCTION_1       1  '1 positional argument'
              828  STORE_DEREF              'monthOffset'

 L. 586       830  LOAD_FAST                'start'
              832  LOAD_CONST               1
              834  INPLACE_SUBTRACT 
              836  STORE_FAST               'start'

 L. 587       838  LOAD_CONST               2
              840  STORE_FAST               'used'
              842  JUMP_FORWARD       1298  'to 1298'
            844_0  COME_FROM           818  '818'

 L. 588       844  LOAD_FAST                'wordNext'
              846  LOAD_CONST               ('prochain', 'suivant')
              848  COMPARE_OP               in
          850_852  POP_JUMP_IF_FALSE   864  'to 864'

 L. 589       854  LOAD_CONST               1
              856  STORE_DEREF              'monthOffset'

 L. 590       858  LOAD_CONST               2
              860  STORE_FAST               'used'
              862  JUMP_FORWARD       1298  'to 1298'
            864_0  COME_FROM           850  '850'

 L. 591       864  LOAD_FAST                'wordNext'
              866  LOAD_CONST               ('dernier', 'précédent')
              868  COMPARE_OP               in
          870_872  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 592       874  LOAD_CONST               -1
              876  STORE_DEREF              'monthOffset'

 L. 593       878  LOAD_CONST               2
              880  STORE_FAST               'used'
          882_884  JUMP_FORWARD       1298  'to 1298'
            886_0  COME_FROM           804  '804'
            886_1  COME_FROM           798  '798'

 L. 595       886  LOAD_FAST                'word'
              888  LOAD_CONST               ('an', 'ans', 'année', 'années')
              890  COMPARE_OP               in
          892_894  POP_JUMP_IF_FALSE   980  'to 980'
              896  LOAD_FAST                'fromFlag'
          898_900  POP_JUMP_IF_TRUE    980  'to 980'

 L. 596       902  LOAD_FAST                'wordPrev'
              904  LOAD_CONST               0
              906  BINARY_SUBSCR    
              908  LOAD_METHOD              isdigit
              910  CALL_METHOD_0         0  '0 positional arguments'
          912_914  POP_JUMP_IF_FALSE   938  'to 938'

 L. 597       916  LOAD_GLOBAL              int
              918  LOAD_FAST                'wordPrev'
              920  CALL_FUNCTION_1       1  '1 positional argument'
              922  STORE_DEREF              'yearOffset'

 L. 598       924  LOAD_FAST                'start'
              926  LOAD_CONST               1
              928  INPLACE_SUBTRACT 
              930  STORE_FAST               'start'

 L. 599       932  LOAD_CONST               2
              934  STORE_FAST               'used'
              936  JUMP_FORWARD       1298  'to 1298'
            938_0  COME_FROM           912  '912'

 L. 600       938  LOAD_FAST                'wordNext'
              940  LOAD_CONST               ('prochain', 'prochaine', 'suivant', 'suivante')
              942  COMPARE_OP               in
          944_946  POP_JUMP_IF_FALSE   958  'to 958'

 L. 601       948  LOAD_CONST               1
              950  STORE_DEREF              'yearOffset'

 L. 602       952  LOAD_CONST               2
              954  STORE_FAST               'used'
              956  JUMP_FORWARD       1298  'to 1298'
            958_0  COME_FROM           944  '944'

 L. 603       958  LOAD_FAST                'wordNext'
              960  LOAD_CONST               ('dernier', 'dernière', 'précédent', 'précédente')
              962  COMPARE_OP               in
          964_966  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 605       968  LOAD_CONST               -1
              970  STORE_DEREF              'yearOffset'

 L. 606       972  LOAD_CONST               2
              974  STORE_FAST               'used'
          976_978  JUMP_FORWARD       1298  'to 1298'
            980_0  COME_FROM           898  '898'
            980_1  COME_FROM           892  '892'

 L. 608       980  LOAD_FAST                'word'
              982  LOAD_FAST                'days'
              984  COMPARE_OP               in
          986_988  POP_JUMP_IF_FALSE  1100  'to 1100'
              990  LOAD_FAST                'fromFlag'
          992_994  POP_JUMP_IF_TRUE   1100  'to 1100'

 L. 609       996  LOAD_FAST                'days'
              998  LOAD_METHOD              index
             1000  LOAD_FAST                'word'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  STORE_FAST               'd'

 L. 610      1006  LOAD_FAST                'd'
             1008  LOAD_CONST               1
             1010  BINARY_ADD       
             1012  LOAD_GLOBAL              int
             1014  LOAD_FAST                'today'
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  BINARY_SUBTRACT  
             1020  STORE_DEREF              'dayOffset'

 L. 611      1022  LOAD_CONST               1
             1024  STORE_FAST               'used'

 L. 612      1026  LOAD_DEREF               'dayOffset'
             1028  LOAD_CONST               0
             1030  COMPARE_OP               <
         1032_1034  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 613      1036  LOAD_DEREF               'dayOffset'
             1038  LOAD_CONST               7
             1040  INPLACE_ADD      
             1042  STORE_DEREF              'dayOffset'
           1044_0  COME_FROM          1032  '1032'

 L. 614      1044  LOAD_FAST                'wordNext'
             1046  LOAD_CONST               ('prochain', 'suivant')
             1048  COMPARE_OP               in
         1050_1052  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 615      1054  LOAD_DEREF               'dayOffset'
             1056  LOAD_CONST               7
             1058  INPLACE_ADD      
             1060  STORE_DEREF              'dayOffset'

 L. 616      1062  LOAD_FAST                'used'
             1064  LOAD_CONST               1
             1066  INPLACE_ADD      
             1068  STORE_FAST               'used'
             1070  JUMP_FORWARD       1098  'to 1098'
           1072_0  COME_FROM          1050  '1050'

 L. 617      1072  LOAD_FAST                'wordNext'
             1074  LOAD_CONST               ('dernier', 'précédent')
             1076  COMPARE_OP               in
         1078_1080  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 618      1082  LOAD_DEREF               'dayOffset'
             1084  LOAD_CONST               7
             1086  INPLACE_SUBTRACT 
             1088  STORE_DEREF              'dayOffset'

 L. 619      1090  LOAD_FAST                'used'
             1092  LOAD_CONST               1
             1094  INPLACE_ADD      
             1096  STORE_FAST               'used'
           1098_0  COME_FROM          1070  '1070'
             1098  JUMP_FORWARD       1298  'to 1298'
           1100_0  COME_FROM           992  '992'
           1100_1  COME_FROM           986  '986'

 L. 621      1100  LOAD_FAST                'word'
             1102  LOAD_FAST                'months'
             1104  COMPARE_OP               in
         1106_1108  POP_JUMP_IF_TRUE   1126  'to 1126'
             1110  LOAD_FAST                'word'
             1112  LOAD_FAST                'monthsShort'
             1114  COMPARE_OP               in
         1116_1118  POP_JUMP_IF_FALSE  1298  'to 1298'
             1120  LOAD_FAST                'fromFlag'
         1122_1124  POP_JUMP_IF_TRUE   1298  'to 1298'
           1126_0  COME_FROM          1106  '1106'

 L. 622      1126  SETUP_EXCEPT       1142  'to 1142'

 L. 623      1128  LOAD_FAST                'months'
             1130  LOAD_METHOD              index
             1132  LOAD_FAST                'word'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'm'
             1138  POP_BLOCK        
             1140  JUMP_FORWARD       1174  'to 1174'
           1142_0  COME_FROM_EXCEPT   1126  '1126'

 L. 624      1142  DUP_TOP          
             1144  LOAD_GLOBAL              ValueError
             1146  COMPARE_OP               exception-match
         1148_1150  POP_JUMP_IF_FALSE  1172  'to 1172'
             1152  POP_TOP          
             1154  POP_TOP          
             1156  POP_TOP          

 L. 625      1158  LOAD_FAST                'monthsShort'
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

 L. 626      1174  LOAD_FAST                'used'
             1176  LOAD_CONST               1
             1178  INPLACE_ADD      
             1180  STORE_FAST               'used'

 L. 627      1182  LOAD_FAST                'months_en'
             1184  LOAD_FAST                'm'
             1186  BINARY_SUBSCR    
             1188  STORE_DEREF              'datestr'

 L. 628      1190  LOAD_FAST                'wordPrev'
         1192_1194  POP_JUMP_IF_FALSE  1240  'to 1240'
             1196  LOAD_FAST                'wordPrev'
             1198  LOAD_CONST               0
             1200  BINARY_SUBSCR    
             1202  LOAD_METHOD              isdigit
             1204  CALL_METHOD_0         0  '0 positional arguments'
         1206_1208  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 629      1210  LOAD_DEREF               'datestr'
             1212  LOAD_STR                 ' '
             1214  LOAD_FAST                'wordPrev'
             1216  BINARY_ADD       
             1218  INPLACE_ADD      
             1220  STORE_DEREF              'datestr'

 L. 630      1222  LOAD_FAST                'start'
             1224  LOAD_CONST               1
             1226  INPLACE_SUBTRACT 
             1228  STORE_FAST               'start'

 L. 631      1230  LOAD_FAST                'used'
             1232  LOAD_CONST               1
             1234  INPLACE_ADD      
             1236  STORE_FAST               'used'
             1238  JUMP_FORWARD       1248  'to 1248'
           1240_0  COME_FROM          1206  '1206'
           1240_1  COME_FROM          1192  '1192'

 L. 633      1240  LOAD_DEREF               'datestr'
             1242  LOAD_STR                 ' 1'
             1244  INPLACE_ADD      
             1246  STORE_DEREF              'datestr'
           1248_0  COME_FROM          1238  '1238'

 L. 634      1248  LOAD_FAST                'wordNext'
         1250_1252  POP_JUMP_IF_FALSE  1294  'to 1294'
             1254  LOAD_FAST                'wordNext'
           1256_0  COME_FROM           936  '936'
           1256_1  COME_FROM           842  '842'
           1256_2  COME_FROM           748  '748'
             1256  LOAD_CONST               0
             1258  BINARY_SUBSCR    
             1260  LOAD_METHOD              isdigit
             1262  CALL_METHOD_0         0  '0 positional arguments'
         1264_1266  POP_JUMP_IF_FALSE  1294  'to 1294'

 L. 635      1268  LOAD_DEREF               'datestr'
             1270  LOAD_STR                 ' '
             1272  LOAD_FAST                'wordNext'
             1274  BINARY_ADD       
           1276_0  COME_FROM           956  '956'
           1276_1  COME_FROM           862  '862'
           1276_2  COME_FROM           768  '768'
             1276  INPLACE_ADD      
             1278  STORE_DEREF              'datestr'

 L. 636      1280  LOAD_FAST                'used'
             1282  LOAD_CONST               1
             1284  INPLACE_ADD      
             1286  STORE_FAST               'used'

 L. 637      1288  LOAD_CONST               True
             1290  STORE_FAST               'hasYear'
             1292  JUMP_FORWARD       1298  'to 1298'
           1294_0  COME_FROM          1264  '1264'
           1294_1  COME_FROM          1250  '1250'

 L. 639      1294  LOAD_CONST               False
             1296  STORE_FAST               'hasYear'
           1298_0  COME_FROM          1292  '1292'
           1298_1  COME_FROM          1122  '1122'
           1298_2  COME_FROM          1116  '1116'
           1298_3  COME_FROM          1098  '1098'
           1298_4  COME_FROM          1078  '1078'
           1298_5  COME_FROM           976  '976'
           1298_6  COME_FROM           964  '964'
           1298_7  COME_FROM           882  '882'
           1298_8  COME_FROM           870  '870'
           1298_9  COME_FROM           788  '788'
          1298_10  COME_FROM           776  '776'
          1298_11  COME_FROM           686  '686'
          1298_12  COME_FROM           654  '654'
          1298_13  COME_FROM           594  '594'
          1298_14  COME_FROM           562  '562'
          1298_15  COME_FROM           530  '530'
          1298_16  COME_FROM           498  '498'
          1298_17  COME_FROM           482  '482'

 L. 642      1298  LOAD_FAST                'days'
             1300  LOAD_FAST                'months'
             1302  BINARY_ADD       
             1304  LOAD_FAST                'monthsShort'
             1306  BINARY_ADD       
             1308  STORE_FAST               'validFollowups'

 L. 643      1310  LOAD_FAST                'validFollowups'
             1312  LOAD_METHOD              append
             1314  LOAD_STR                 "aujourd'hui"
             1316  CALL_METHOD_1         1  '1 positional argument'
             1318  POP_TOP          

 L. 644      1320  LOAD_FAST                'validFollowups'
             1322  LOAD_METHOD              append
             1324  LOAD_STR                 'demain'
             1326  CALL_METHOD_1         1  '1 positional argument'
             1328  POP_TOP          

 L. 645      1330  LOAD_FAST                'validFollowups'
             1332  LOAD_METHOD              append
             1334  LOAD_STR                 'prochain'
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  POP_TOP          

 L. 646      1340  LOAD_FAST                'validFollowups'
             1342  LOAD_METHOD              append
             1344  LOAD_STR                 'prochaine'
             1346  CALL_METHOD_1         1  '1 positional argument'
             1348  POP_TOP          

 L. 647      1350  LOAD_FAST                'validFollowups'
             1352  LOAD_METHOD              append
             1354  LOAD_STR                 'suivant'
             1356  CALL_METHOD_1         1  '1 positional argument'
             1358  POP_TOP          

 L. 648      1360  LOAD_FAST                'validFollowups'
             1362  LOAD_METHOD              append
             1364  LOAD_STR                 'suivante'
             1366  CALL_METHOD_1         1  '1 positional argument'
             1368  POP_TOP          

 L. 649      1370  LOAD_FAST                'validFollowups'
             1372  LOAD_METHOD              append
             1374  LOAD_STR                 'dernier'
             1376  CALL_METHOD_1         1  '1 positional argument'
             1378  POP_TOP          

 L. 650      1380  LOAD_FAST                'validFollowups'
             1382  LOAD_METHOD              append
             1384  LOAD_STR                 'dernière'
             1386  CALL_METHOD_1         1  '1 positional argument'
             1388  POP_TOP          

 L. 651      1390  LOAD_FAST                'validFollowups'
             1392  LOAD_METHOD              append
             1394  LOAD_STR                 'précédent'
             1396  CALL_METHOD_1         1  '1 positional argument'
             1398  POP_TOP          

 L. 652      1400  LOAD_FAST                'validFollowups'
             1402  LOAD_METHOD              append
             1404  LOAD_STR                 'précédente'
             1406  CALL_METHOD_1         1  '1 positional argument'
             1408  POP_TOP          

 L. 653      1410  LOAD_FAST                'validFollowups'
             1412  LOAD_METHOD              append
             1414  LOAD_STR                 'maintenant'
             1416  CALL_METHOD_1         1  '1 positional argument'
             1418  POP_TOP          

 L. 654      1420  LOAD_FAST                'word'
             1422  LOAD_CONST               ('après', 'depuis')
             1424  COMPARE_OP               in
         1426_1428  POP_JUMP_IF_FALSE  1590  'to 1590'
             1430  LOAD_FAST                'wordNext'
             1432  LOAD_FAST                'validFollowups'
             1434  COMPARE_OP               in
         1436_1438  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 655      1440  LOAD_CONST               2
             1442  STORE_FAST               'used'

 L. 656      1444  LOAD_CONST               True
             1446  STORE_FAST               'fromFlag'

 L. 657      1448  LOAD_FAST                'wordNext'
             1450  LOAD_STR                 'demain'
             1452  COMPARE_OP               ==
         1454_1456  POP_JUMP_IF_FALSE  1468  'to 1468'

 L. 658      1458  LOAD_DEREF               'dayOffset'
             1460  LOAD_CONST               1
             1462  INPLACE_ADD      
             1464  STORE_DEREF              'dayOffset'
             1466  JUMP_FORWARD       1590  'to 1590'
           1468_0  COME_FROM          1454  '1454'

 L. 659      1468  LOAD_FAST                'wordNext'
             1470  LOAD_FAST                'days'
             1472  COMPARE_OP               in
         1474_1476  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 660      1478  LOAD_FAST                'days'
             1480  LOAD_METHOD              index
             1482  LOAD_FAST                'wordNext'
             1484  CALL_METHOD_1         1  '1 positional argument'
             1486  STORE_FAST               'd'

 L. 661      1488  LOAD_FAST                'd'
             1490  LOAD_CONST               1
             1492  BINARY_ADD       
             1494  LOAD_GLOBAL              int
             1496  LOAD_FAST                'today'
             1498  CALL_FUNCTION_1       1  '1 positional argument'
             1500  BINARY_SUBTRACT  
             1502  STORE_FAST               'tmpOffset'

 L. 662      1504  LOAD_CONST               2
             1506  STORE_FAST               'used'

 L. 663      1508  LOAD_FAST                'wordNextNext'
             1510  LOAD_STR                 'prochain'
             1512  COMPARE_OP               ==
         1514_1516  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 664      1518  LOAD_FAST                'tmpOffset'
             1520  LOAD_CONST               7
             1522  INPLACE_ADD      
             1524  STORE_FAST               'tmpOffset'

 L. 665      1526  LOAD_FAST                'used'
             1528  LOAD_CONST               1
             1530  INPLACE_ADD      
             1532  STORE_FAST               'used'
             1534  JUMP_FORWARD       1582  'to 1582'
           1536_0  COME_FROM          1514  '1514'

 L. 666      1536  LOAD_FAST                'wordNextNext'
             1538  LOAD_STR                 'dernier'
             1540  COMPARE_OP               ==
         1542_1544  POP_JUMP_IF_FALSE  1564  'to 1564'

 L. 667      1546  LOAD_FAST                'tmpOffset'
             1548  LOAD_CONST               7
             1550  INPLACE_SUBTRACT 
             1552  STORE_FAST               'tmpOffset'

 L. 668      1554  LOAD_FAST                'used'
             1556  LOAD_CONST               1
             1558  INPLACE_ADD      
             1560  STORE_FAST               'used'
             1562  JUMP_FORWARD       1582  'to 1582'
           1564_0  COME_FROM          1542  '1542'

 L. 669      1564  LOAD_FAST                'tmpOffset'
             1566  LOAD_CONST               0
             1568  COMPARE_OP               <
         1570_1572  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 670      1574  LOAD_FAST                'tmpOffset'
             1576  LOAD_CONST               7
             1578  INPLACE_ADD      
             1580  STORE_FAST               'tmpOffset'
           1582_0  COME_FROM          1570  '1570'
           1582_1  COME_FROM          1562  '1562'
           1582_2  COME_FROM          1534  '1534'

 L. 671      1582  LOAD_DEREF               'dayOffset'
             1584  LOAD_FAST                'tmpOffset'
             1586  INPLACE_ADD      
             1588  STORE_DEREF              'dayOffset'
           1590_0  COME_FROM          1474  '1474'
           1590_1  COME_FROM          1466  '1466'
           1590_2  COME_FROM          1436  '1436'
           1590_3  COME_FROM          1426  '1426'

 L. 672      1590  LOAD_FAST                'used'
             1592  LOAD_CONST               0
             1594  COMPARE_OP               >
         1596_1598  POP_JUMP_IF_FALSE   280  'to 280'

 L. 673      1600  LOAD_FAST                'start'
             1602  LOAD_CONST               1
             1604  BINARY_SUBTRACT  
             1606  LOAD_CONST               0
             1608  COMPARE_OP               >
         1610_1612  POP_JUMP_IF_FALSE  1648  'to 1648'
             1614  LOAD_FAST                'words'
             1616  LOAD_FAST                'start'
             1618  LOAD_CONST               1
             1620  BINARY_SUBTRACT  
             1622  BINARY_SUBSCR    
             1624  LOAD_CONST               ('ce', 'cette')
             1626  COMPARE_OP               in
         1628_1630  POP_JUMP_IF_FALSE  1648  'to 1648'

 L. 674      1632  LOAD_FAST                'start'
             1634  LOAD_CONST               1
             1636  INPLACE_SUBTRACT 
             1638  STORE_FAST               'start'

 L. 675      1640  LOAD_FAST                'used'
             1642  LOAD_CONST               1
             1644  INPLACE_ADD      
             1646  STORE_FAST               'used'
           1648_0  COME_FROM          1628  '1628'
           1648_1  COME_FROM          1610  '1610'

 L. 677      1648  SETUP_LOOP         1682  'to 1682'
             1650  LOAD_GLOBAL              range
             1652  LOAD_CONST               0
             1654  LOAD_FAST                'used'
             1656  CALL_FUNCTION_2       2  '2 positional arguments'
             1658  GET_ITER         
             1660  FOR_ITER           1680  'to 1680'
             1662  STORE_FAST               'i'

 L. 678      1664  LOAD_STR                 ''
             1666  LOAD_FAST                'words'
             1668  LOAD_FAST                'i'
             1670  LOAD_FAST                'start'
             1672  BINARY_ADD       
             1674  STORE_SUBSCR     
         1676_1678  JUMP_BACK          1660  'to 1660'
             1680  POP_BLOCK        
           1682_0  COME_FROM_LOOP     1648  '1648'

 L. 680      1682  LOAD_FAST                'start'
             1684  LOAD_CONST               1
             1686  BINARY_SUBTRACT  
             1688  LOAD_CONST               0
             1690  COMPARE_OP               >=
         1692_1694  POP_JUMP_IF_FALSE  1726  'to 1726'
             1696  LOAD_FAST                'words'
             1698  LOAD_FAST                'start'
             1700  LOAD_CONST               1
             1702  BINARY_SUBTRACT  
             1704  BINARY_SUBSCR    
             1706  LOAD_FAST                'markers'
             1708  COMPARE_OP               in
         1710_1712  POP_JUMP_IF_FALSE  1726  'to 1726'

 L. 681      1714  LOAD_STR                 ''
             1716  LOAD_FAST                'words'
             1718  LOAD_FAST                'start'
             1720  LOAD_CONST               1
             1722  BINARY_SUBTRACT  
             1724  STORE_SUBSCR     
           1726_0  COME_FROM          1710  '1710'
           1726_1  COME_FROM          1692  '1692'

 L. 682      1726  LOAD_CONST               True
             1728  STORE_DEREF              'found'

 L. 683      1730  LOAD_CONST               True
             1732  STORE_FAST               'daySpecified'
         1734_1736  JUMP_BACK           280  'to 280'
             1738  POP_BLOCK        
           1740_0  COME_FROM_LOOP      268  '268'

 L. 686      1740  LOAD_CONST               0
             1742  STORE_DEREF              'hrOffset'

 L. 687      1744  LOAD_CONST               0
             1746  STORE_DEREF              'minOffset'

 L. 688      1748  LOAD_CONST               0
             1750  STORE_DEREF              'secOffset'

 L. 689      1752  LOAD_CONST               None
             1754  STORE_DEREF              'hrAbs'

 L. 690      1756  LOAD_CONST               None
             1758  STORE_DEREF              'minAbs'

 L. 691      1760  LOAD_STR                 ''
             1762  STORE_FAST               'ampm'

 L. 692      1764  LOAD_CONST               False
             1766  STORE_DEREF              'isTime'

 L. 694  1768_1770  SETUP_LOOP         3876  'to 3876'
             1772  LOAD_GLOBAL              enumerate
             1774  LOAD_FAST                'words'
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  GET_ITER         
           1780_0  COME_FROM          3772  '3772'
         1780_1782  FOR_ITER           3874  'to 3874'
             1784  UNPACK_SEQUENCE_2     2 
             1786  STORE_FAST               'idx'
             1788  STORE_FAST               'word'

 L. 695      1790  LOAD_FAST                'word'
             1792  LOAD_STR                 ''
             1794  COMPARE_OP               ==
         1796_1798  POP_JUMP_IF_FALSE  1804  'to 1804'

 L. 696  1800_1802  CONTINUE           1780  'to 1780'
           1804_0  COME_FROM          1796  '1796'

 L. 698      1804  LOAD_FAST                'idx'
             1806  LOAD_CONST               1
             1808  COMPARE_OP               >
         1810_1812  POP_JUMP_IF_FALSE  1826  'to 1826'
             1814  LOAD_FAST                'words'
             1816  LOAD_FAST                'idx'
             1818  LOAD_CONST               2
             1820  BINARY_SUBTRACT  
             1822  BINARY_SUBSCR    
             1824  JUMP_FORWARD       1828  'to 1828'
           1826_0  COME_FROM          1810  '1810'
             1826  LOAD_STR                 ''
           1828_0  COME_FROM          1824  '1824'
             1828  STORE_FAST               'wordPrevPrev'

 L. 699      1830  LOAD_FAST                'idx'
             1832  LOAD_CONST               0
             1834  COMPARE_OP               >
         1836_1838  POP_JUMP_IF_FALSE  1852  'to 1852'
             1840  LOAD_FAST                'words'
             1842  LOAD_FAST                'idx'
             1844  LOAD_CONST               1
             1846  BINARY_SUBTRACT  
             1848  BINARY_SUBSCR    
             1850  JUMP_FORWARD       1854  'to 1854'
           1852_0  COME_FROM          1836  '1836'
             1852  LOAD_STR                 ''
           1854_0  COME_FROM          1850  '1850'
             1854  STORE_FAST               'wordPrev'

 L. 700      1856  LOAD_FAST                'idx'
             1858  LOAD_CONST               1
             1860  BINARY_ADD       
             1862  LOAD_GLOBAL              len
             1864  LOAD_FAST                'words'
             1866  CALL_FUNCTION_1       1  '1 positional argument'
             1868  COMPARE_OP               <
         1870_1872  POP_JUMP_IF_FALSE  1886  'to 1886'
             1874  LOAD_FAST                'words'
             1876  LOAD_FAST                'idx'
             1878  LOAD_CONST               1
             1880  BINARY_ADD       
             1882  BINARY_SUBSCR    
             1884  JUMP_FORWARD       1888  'to 1888'
           1886_0  COME_FROM          1870  '1870'
             1886  LOAD_STR                 ''
           1888_0  COME_FROM          1884  '1884'
             1888  STORE_FAST               'wordNext'

 L. 701      1890  LOAD_FAST                'idx'
             1892  LOAD_CONST               2
             1894  BINARY_ADD       
             1896  LOAD_GLOBAL              len
             1898  LOAD_FAST                'words'
             1900  CALL_FUNCTION_1       1  '1 positional argument'
             1902  COMPARE_OP               <
         1904_1906  POP_JUMP_IF_FALSE  1920  'to 1920'
             1908  LOAD_FAST                'words'
             1910  LOAD_FAST                'idx'
             1912  LOAD_CONST               2
             1914  BINARY_ADD       
             1916  BINARY_SUBSCR    
             1918  JUMP_FORWARD       1922  'to 1922'
           1920_0  COME_FROM          1904  '1904'
             1920  LOAD_STR                 ''
           1922_0  COME_FROM          1918  '1918'
             1922  STORE_FAST               'wordNextNext'

 L. 702      1924  LOAD_CONST               0
             1926  STORE_FAST               'used'

 L. 703      1928  LOAD_FAST                'idx'
             1930  STORE_FAST               'start'

 L. 706      1932  LOAD_FAST                'word'
             1934  LOAD_CONST               ('midi', 'minuit')
             1936  COMPARE_OP               in
         1938_1940  POP_JUMP_IF_FALSE  2184  'to 2184'

 L. 707      1942  LOAD_CONST               True
             1944  STORE_DEREF              'isTime'

 L. 708      1946  LOAD_FAST                'word'
             1948  LOAD_STR                 'midi'
             1950  COMPARE_OP               ==
         1952_1954  POP_JUMP_IF_FALSE  1970  'to 1970'

 L. 709      1956  LOAD_CONST               12
             1958  STORE_DEREF              'hrAbs'

 L. 710      1960  LOAD_FAST                'used'
             1962  LOAD_CONST               1
             1964  INPLACE_ADD      
             1966  STORE_FAST               'used'
             1968  JUMP_FORWARD       1992  'to 1992'
           1970_0  COME_FROM          1952  '1952'

 L. 711      1970  LOAD_FAST                'word'
             1972  LOAD_STR                 'minuit'
             1974  COMPARE_OP               ==
         1976_1978  POP_JUMP_IF_FALSE  1992  'to 1992'

 L. 712      1980  LOAD_CONST               0
             1982  STORE_DEREF              'hrAbs'

 L. 713      1984  LOAD_FAST                'used'
             1986  LOAD_CONST               1
             1988  INPLACE_ADD      
             1990  STORE_FAST               'used'
           1992_0  COME_FROM          1976  '1976'
           1992_1  COME_FROM          1968  '1968'

 L. 714      1992  LOAD_FAST                'wordNext'
             1994  LOAD_METHOD              isdigit
             1996  CALL_METHOD_0         0  '0 positional arguments'
         1998_2000  POP_JUMP_IF_FALSE  2020  'to 2020'

 L. 715      2002  LOAD_GLOBAL              int
             2004  LOAD_FAST                'wordNext'
             2006  CALL_FUNCTION_1       1  '1 positional argument'
             2008  STORE_DEREF              'minAbs'

 L. 716      2010  LOAD_FAST                'used'
             2012  LOAD_CONST               1
             2014  INPLACE_ADD      
             2016  STORE_FAST               'used'
             2018  JUMP_FORWARD       3766  'to 3766'
           2020_0  COME_FROM          1998  '1998'

 L. 717      2020  LOAD_FAST                'wordNext'
             2022  LOAD_STR                 'et'
             2024  COMPARE_OP               ==
         2026_2028  POP_JUMP_IF_FALSE  2078  'to 2078'

 L. 718      2030  LOAD_FAST                'wordNextNext'
             2032  LOAD_STR                 'quart'
             2034  COMPARE_OP               ==
         2036_2038  POP_JUMP_IF_FALSE  2054  'to 2054'

 L. 719      2040  LOAD_CONST               15
             2042  STORE_DEREF              'minAbs'

 L. 720      2044  LOAD_FAST                'used'
             2046  LOAD_CONST               2
             2048  INPLACE_ADD      
             2050  STORE_FAST               'used'
             2052  JUMP_FORWARD       2076  'to 2076'
           2054_0  COME_FROM          2036  '2036'

 L. 721      2054  LOAD_FAST                'wordNextNext'
             2056  LOAD_STR                 'demi'
             2058  COMPARE_OP               ==
         2060_2062  POP_JUMP_IF_FALSE  2180  'to 2180'

 L. 722      2064  LOAD_CONST               30
             2066  STORE_DEREF              'minAbs'

 L. 723      2068  LOAD_FAST                'used'
             2070  LOAD_CONST               2
             2072  INPLACE_ADD      
             2074  STORE_FAST               'used'
           2076_0  COME_FROM          2052  '2052'
             2076  JUMP_FORWARD       3766  'to 3766'
           2078_0  COME_FROM          2026  '2026'

 L. 724      2078  LOAD_FAST                'wordNext'
             2080  LOAD_STR                 'moins'
             2082  COMPARE_OP               ==
         2084_2086  POP_JUMP_IF_FALSE  3766  'to 3766'

 L. 725      2088  LOAD_FAST                'wordNextNext'
             2090  LOAD_METHOD              isdigit
             2092  CALL_METHOD_0         0  '0 positional arguments'
         2094_2096  POP_JUMP_IF_FALSE  2138  'to 2138'

 L. 726      2098  LOAD_CONST               60
             2100  LOAD_GLOBAL              int
             2102  LOAD_FAST                'wordNextNext'
             2104  CALL_FUNCTION_1       1  '1 positional argument'
             2106  BINARY_SUBTRACT  
             2108  STORE_DEREF              'minAbs'

 L. 727      2110  LOAD_DEREF               'hrAbs'
         2112_2114  POP_JUMP_IF_TRUE   2122  'to 2122'

 L. 728      2116  LOAD_CONST               23
             2118  STORE_DEREF              'hrAbs'
             2120  JUMP_FORWARD       2130  'to 2130'
           2122_0  COME_FROM          2112  '2112'

 L. 730      2122  LOAD_DEREF               'hrAbs'
             2124  LOAD_CONST               1
             2126  INPLACE_SUBTRACT 
             2128  STORE_DEREF              'hrAbs'
           2130_0  COME_FROM          2120  '2120'

 L. 731      2130  LOAD_FAST                'used'
             2132  LOAD_CONST               2
             2134  INPLACE_ADD      
             2136  STORE_FAST               'used'
           2138_0  COME_FROM          2094  '2094'

 L. 732      2138  LOAD_FAST                'wordNextNext'
             2140  LOAD_STR                 'quart'
             2142  COMPARE_OP               ==
         2144_2146  POP_JUMP_IF_FALSE  3766  'to 3766'

 L. 733      2148  LOAD_CONST               45
             2150  STORE_DEREF              'minAbs'

 L. 734      2152  LOAD_DEREF               'hrAbs'
         2154_2156  POP_JUMP_IF_TRUE   2164  'to 2164'

 L. 735      2158  LOAD_CONST               23
             2160  STORE_DEREF              'hrAbs'
             2162  JUMP_FORWARD       2172  'to 2172'
           2164_0  COME_FROM          2154  '2154'

 L. 737      2164  LOAD_DEREF               'hrAbs'
             2166  LOAD_CONST               1
             2168  INPLACE_SUBTRACT 
             2170  STORE_DEREF              'hrAbs'
           2172_0  COME_FROM          2162  '2162'

 L. 738      2172  LOAD_FAST                'used'
             2174  LOAD_CONST               2
             2176  INPLACE_ADD      
             2178  STORE_FAST               'used'
           2180_0  COME_FROM          2060  '2060'
         2180_2182  JUMP_FORWARD       3766  'to 3766'
           2184_0  COME_FROM          1938  '1938'

 L. 740      2184  LOAD_FAST                'word'
             2186  LOAD_STR                 'demi-heure'
             2188  COMPARE_OP               ==
         2190_2192  POP_JUMP_IF_TRUE   2224  'to 2224'
             2194  LOAD_FAST                'word'
             2196  LOAD_STR                 'heure'
             2198  COMPARE_OP               ==
         2200_2202  POP_JUMP_IF_FALSE  2368  'to 2368'

 L. 741      2204  LOAD_FAST                'wordPrevPrev'
             2206  LOAD_FAST                'markers'
             2208  COMPARE_OP               in
         2210_2212  POP_JUMP_IF_TRUE   2224  'to 2224'
             2214  LOAD_FAST                'wordPrevPrevPrev'
             2216  LOAD_FAST                'markers'
             2218  COMPARE_OP               in
         2220_2222  POP_JUMP_IF_FALSE  2368  'to 2368'
           2224_0  COME_FROM          2210  '2210'
           2224_1  COME_FROM          2190  '2190'

 L. 742      2224  LOAD_CONST               1
             2226  STORE_FAST               'used'

 L. 743      2228  LOAD_CONST               True
             2230  STORE_DEREF              'isTime'

 L. 744      2232  LOAD_FAST                'word'
             2234  LOAD_STR                 'demi-heure'
             2236  COMPARE_OP               ==
         2238_2240  POP_JUMP_IF_FALSE  2248  'to 2248'

 L. 745      2242  LOAD_CONST               30
             2244  STORE_DEREF              'minOffset'
             2246  JUMP_FORWARD       2328  'to 2328'
           2248_0  COME_FROM          2238  '2238'

 L. 746      2248  LOAD_FAST                'wordPrev'
             2250  LOAD_STR                 'quart'
             2252  COMPARE_OP               ==
         2254_2256  POP_JUMP_IF_FALSE  2280  'to 2280'

 L. 747      2258  LOAD_CONST               15
             2260  STORE_DEREF              'minOffset'

 L. 748      2262  LOAD_FAST                'used'
             2264  LOAD_CONST               1
             2266  INPLACE_ADD      
             2268  STORE_FAST               'used'

 L. 749      2270  LOAD_FAST                'start'
             2272  LOAD_CONST               1
             2274  INPLACE_SUBTRACT 
             2276  STORE_FAST               'start'
             2278  JUMP_FORWARD       2328  'to 2328'
           2280_0  COME_FROM          2254  '2254'

 L. 750      2280  LOAD_FAST                'wordPrev'
             2282  LOAD_STR                 'quarts'
             2284  COMPARE_OP               ==
         2286_2288  POP_JUMP_IF_FALSE  2328  'to 2328'
             2290  LOAD_FAST                'wordPrevPrev'
             2292  LOAD_METHOD              isdigit
             2294  CALL_METHOD_0         0  '0 positional arguments'
         2296_2298  POP_JUMP_IF_FALSE  2328  'to 2328'

 L. 751      2300  LOAD_GLOBAL              int
             2302  LOAD_FAST                'wordPrevPrev'
             2304  CALL_FUNCTION_1       1  '1 positional argument'
             2306  LOAD_CONST               15
             2308  BINARY_MULTIPLY  
             2310  STORE_DEREF              'minOffset'

 L. 752      2312  LOAD_FAST                'used'
             2314  LOAD_CONST               1
             2316  INPLACE_ADD      
             2318  STORE_FAST               'used'

 L. 753      2320  LOAD_FAST                'start'
             2322  LOAD_CONST               1
             2324  INPLACE_SUBTRACT 
             2326  STORE_FAST               'start'
           2328_0  COME_FROM          2296  '2296'
           2328_1  COME_FROM          2286  '2286'
           2328_2  COME_FROM          2278  '2278'
           2328_3  COME_FROM          2246  '2246'

 L. 754      2328  LOAD_FAST                'wordPrev'
             2330  LOAD_METHOD              isdigit
             2332  CALL_METHOD_0         0  '0 positional arguments'
         2334_2336  POP_JUMP_IF_TRUE   2348  'to 2348'
             2338  LOAD_FAST                'wordPrevPrev'
             2340  LOAD_METHOD              isdigit
             2342  CALL_METHOD_0         0  '0 positional arguments'
         2344_2346  POP_JUMP_IF_FALSE  3766  'to 3766'
           2348_0  COME_FROM          2334  '2334'

 L. 755      2348  LOAD_FAST                'start'
             2350  LOAD_CONST               1
             2352  INPLACE_SUBTRACT 
             2354  STORE_FAST               'start'

 L. 756      2356  LOAD_FAST                'used'
             2358  LOAD_CONST               1
             2360  INPLACE_ADD      
             2362  STORE_FAST               'used'
         2364_2366  JUMP_FORWARD       3766  'to 3766'
           2368_0  COME_FROM          2220  '2220'
           2368_1  COME_FROM          2200  '2200'

 L. 758      2368  LOAD_FAST                'word'
             2370  LOAD_CONST               0
             2372  BINARY_SUBSCR    
             2374  LOAD_METHOD              isdigit
             2376  CALL_METHOD_0         0  '0 positional arguments'
         2378_2380  POP_JUMP_IF_FALSE  3688  'to 3688'
             2382  LOAD_GLOBAL              getOrdinal_fr
             2384  LOAD_FAST                'word'
             2386  CALL_FUNCTION_1       1  '1 positional argument'
             2388  LOAD_CONST               None
             2390  COMPARE_OP               is
         2392_2394  POP_JUMP_IF_FALSE  3688  'to 3688'

 L. 759      2396  LOAD_CONST               True
             2398  STORE_DEREF              'isTime'

 L. 760      2400  LOAD_STR                 ':'
             2402  LOAD_FAST                'word'
             2404  COMPARE_OP               in
         2406_2408  POP_JUMP_IF_TRUE   2430  'to 2430'
             2410  LOAD_STR                 'h'
             2412  LOAD_FAST                'word'
             2414  COMPARE_OP               in
         2416_2418  POP_JUMP_IF_TRUE   2430  'to 2430'
             2420  LOAD_STR                 'min'
             2422  LOAD_FAST                'word'
             2424  COMPARE_OP               in
         2426_2428  POP_JUMP_IF_FALSE  2724  'to 2724'
           2430_0  COME_FROM          2416  '2416'
           2430_1  COME_FROM          2406  '2406'

 L. 763      2430  LOAD_STR                 ''
             2432  STORE_FAST               'strHH'

 L. 764      2434  LOAD_STR                 ''
             2436  STORE_FAST               'strMM'

 L. 765      2438  LOAD_CONST               0
             2440  STORE_FAST               'stage'

 L. 766      2442  LOAD_GLOBAL              len
             2444  LOAD_FAST                'word'
             2446  CALL_FUNCTION_1       1  '1 positional argument'
             2448  STORE_FAST               'length'

 L. 767      2450  SETUP_LOOP         2636  'to 2636'
             2452  LOAD_GLOBAL              range
             2454  LOAD_FAST                'length'
             2456  CALL_FUNCTION_1       1  '1 positional argument'
             2458  GET_ITER         
           2460_0  COME_FROM          2624  '2624'
             2460  FOR_ITER           2634  'to 2634'
             2462  STORE_FAST               'i'

 L. 768      2464  LOAD_FAST                'stage'
             2466  LOAD_CONST               0
             2468  COMPARE_OP               ==
         2470_2472  POP_JUMP_IF_FALSE  2540  'to 2540'

 L. 769      2474  LOAD_FAST                'word'
             2476  LOAD_FAST                'i'
             2478  BINARY_SUBSCR    
             2480  LOAD_METHOD              isdigit
             2482  CALL_METHOD_0         0  '0 positional arguments'
         2484_2486  POP_JUMP_IF_FALSE  2506  'to 2506'

 L. 770      2488  LOAD_FAST                'strHH'
             2490  LOAD_FAST                'word'
             2492  LOAD_FAST                'i'
             2494  BINARY_SUBSCR    
             2496  INPLACE_ADD      
             2498  STORE_FAST               'strHH'

 L. 771      2500  LOAD_CONST               1
             2502  STORE_FAST               'used'
             2504  JUMP_FORWARD       2538  'to 2538'
           2506_0  COME_FROM          2484  '2484'

 L. 772      2506  LOAD_FAST                'word'
             2508  LOAD_FAST                'i'
             2510  BINARY_SUBSCR    
             2512  LOAD_CONST               (':', 'h', 'm')
             2514  COMPARE_OP               in
         2516_2518  POP_JUMP_IF_FALSE  2526  'to 2526'

 L. 773      2520  LOAD_CONST               1
             2522  STORE_FAST               'stage'
             2524  JUMP_FORWARD       2538  'to 2538'
           2526_0  COME_FROM          2516  '2516'

 L. 775      2526  LOAD_CONST               2
             2528  STORE_FAST               'stage'

 L. 776      2530  LOAD_FAST                'i'
             2532  LOAD_CONST               1
             2534  INPLACE_SUBTRACT 
             2536  STORE_FAST               'i'
           2538_0  COME_FROM          2524  '2524'
           2538_1  COME_FROM          2504  '2504'
             2538  JUMP_BACK          2460  'to 2460'
           2540_0  COME_FROM          2470  '2470'

 L. 777      2540  LOAD_FAST                'stage'
             2542  LOAD_CONST               1
             2544  COMPARE_OP               ==
         2546_2548  POP_JUMP_IF_FALSE  2618  'to 2618'

 L. 778      2550  LOAD_FAST                'word'
             2552  LOAD_FAST                'i'
             2554  BINARY_SUBSCR    
             2556  LOAD_METHOD              isdigit
             2558  CALL_METHOD_0         0  '0 positional arguments'
         2560_2562  POP_JUMP_IF_FALSE  2582  'to 2582'

 L. 779      2564  LOAD_FAST                'strMM'
             2566  LOAD_FAST                'word'
             2568  LOAD_FAST                'i'
             2570  BINARY_SUBSCR    
             2572  INPLACE_ADD      
             2574  STORE_FAST               'strMM'

 L. 780      2576  LOAD_CONST               1
             2578  STORE_FAST               'used'
             2580  JUMP_FORWARD       2616  'to 2616'
           2582_0  COME_FROM          2560  '2560'

 L. 782      2582  LOAD_CONST               2
             2584  STORE_FAST               'stage'

 L. 783      2586  LOAD_FAST                'word'
             2588  LOAD_FAST                'i'
             2590  LOAD_FAST                'i'
             2592  LOAD_CONST               3
             2594  BINARY_ADD       
             2596  BUILD_SLICE_2         2 
             2598  BINARY_SUBSCR    
             2600  LOAD_STR                 'min'
             2602  COMPARE_OP               ==
         2604_2606  POP_JUMP_IF_FALSE  2630  'to 2630'

 L. 784      2608  LOAD_FAST                'i'
             2610  LOAD_CONST               1
             2612  INPLACE_ADD      
             2614  STORE_FAST               'i'
           2616_0  COME_FROM          2580  '2580'
             2616  JUMP_BACK          2460  'to 2460'
           2618_0  COME_FROM          2546  '2546'

 L. 785      2618  LOAD_FAST                'stage'
             2620  LOAD_CONST               2
             2622  COMPARE_OP               ==
         2624_2626  POP_JUMP_IF_FALSE  2460  'to 2460'

 L. 786      2628  BREAK_LOOP       
           2630_0  COME_FROM          2604  '2604'
         2630_2632  JUMP_BACK          2460  'to 2460'
             2634  POP_BLOCK        
           2636_0  COME_FROM_LOOP     2450  '2450'

 L. 787      2636  LOAD_FAST                'wordPrev'
             2638  LOAD_FAST                'words_in'
             2640  COMPARE_OP               in
         2642_2644  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 788      2646  LOAD_FAST                'strHH'
         2648_2650  POP_JUMP_IF_FALSE  2660  'to 2660'
             2652  LOAD_GLOBAL              int
             2654  LOAD_FAST                'strHH'
             2656  CALL_FUNCTION_1       1  '1 positional argument'
             2658  JUMP_FORWARD       2662  'to 2662'
           2660_0  COME_FROM          2648  '2648'
             2660  LOAD_CONST               0
           2662_0  COME_FROM          2658  '2658'
             2662  STORE_DEREF              'hrOffset'

 L. 789      2664  LOAD_FAST                'strMM'
         2666_2668  POP_JUMP_IF_FALSE  2678  'to 2678'
             2670  LOAD_GLOBAL              int
             2672  LOAD_FAST                'strMM'
             2674  CALL_FUNCTION_1       1  '1 positional argument'
             2676  JUMP_FORWARD       2680  'to 2680'
           2678_0  COME_FROM          2666  '2666'
             2678  LOAD_CONST               0
           2680_0  COME_FROM          2676  '2676'
             2680  STORE_DEREF              'minOffset'
             2682  JUMP_FORWARD       3446  'to 3446'
           2684_0  COME_FROM          2642  '2642'

 L. 791      2684  LOAD_FAST                'strHH'
         2686_2688  POP_JUMP_IF_FALSE  2698  'to 2698'
             2690  LOAD_GLOBAL              int
             2692  LOAD_FAST                'strHH'
             2694  CALL_FUNCTION_1       1  '1 positional argument'
             2696  JUMP_FORWARD       2700  'to 2700'
           2698_0  COME_FROM          2686  '2686'
             2698  LOAD_CONST               0
           2700_0  COME_FROM          2696  '2696'
             2700  STORE_DEREF              'hrAbs'

 L. 792      2702  LOAD_FAST                'strMM'
         2704_2706  POP_JUMP_IF_FALSE  2716  'to 2716'
             2708  LOAD_GLOBAL              int
             2710  LOAD_FAST                'strMM'
             2712  CALL_FUNCTION_1       1  '1 positional argument'
             2714  JUMP_FORWARD       2718  'to 2718'
           2716_0  COME_FROM          2704  '2704'
             2716  LOAD_CONST               0
           2718_0  COME_FROM          2714  '2714'
             2718  STORE_DEREF              'minAbs'
         2720_2722  JUMP_FORWARD       3446  'to 3446'
           2724_0  COME_FROM          2426  '2426'

 L. 796      2724  LOAD_GLOBAL              len
             2726  LOAD_FAST                'word'
             2728  CALL_FUNCTION_1       1  '1 positional argument'
             2730  STORE_FAST               'length'

 L. 797      2732  LOAD_STR                 ''
             2734  STORE_FAST               'ampm'

 L. 799      2736  LOAD_FAST                'word'
             2738  LOAD_METHOD              isdigit
             2740  CALL_METHOD_0         0  '0 positional arguments'
         2742_2744  POP_JUMP_IF_FALSE  3314  'to 3314'

 L. 800      2746  LOAD_FAST                'wordNext'
             2748  LOAD_CONST               ('heures', 'heure')
             2750  COMPARE_OP               in
         2752_2754  POP_JUMP_IF_FALSE  3314  'to 3314'
             2756  LOAD_FAST                'word'
             2758  LOAD_STR                 '0'
             2760  COMPARE_OP               !=
         2762_2764  POP_JUMP_IF_FALSE  3314  'to 3314'

 L. 802      2766  LOAD_GLOBAL              int
             2768  LOAD_FAST                'word'
             2770  CALL_FUNCTION_1       1  '1 positional argument'
             2772  LOAD_CONST               100
             2774  COMPARE_OP               <
         2776_2778  POP_JUMP_IF_TRUE   2794  'to 2794'

 L. 803      2780  LOAD_GLOBAL              int
             2782  LOAD_FAST                'word'
             2784  CALL_FUNCTION_1       1  '1 positional argument'
             2786  LOAD_CONST               2400
             2788  COMPARE_OP               >
         2790_2792  POP_JUMP_IF_FALSE  3314  'to 3314'
           2794_0  COME_FROM          2776  '2776'

 L. 806      2794  LOAD_FAST                'wordPrev'
             2796  LOAD_FAST                'words_in'
             2798  COMPARE_OP               in
         2800_2802  POP_JUMP_IF_FALSE  2814  'to 2814'

 L. 807      2804  LOAD_GLOBAL              int
             2806  LOAD_FAST                'word'
             2808  CALL_FUNCTION_1       1  '1 positional argument'
             2810  STORE_DEREF              'hrOffset'
             2812  JUMP_FORWARD       2822  'to 2822'
           2814_0  COME_FROM          2800  '2800'

 L. 809      2814  LOAD_GLOBAL              int
             2816  LOAD_FAST                'word'
             2818  CALL_FUNCTION_1       1  '1 positional argument'
             2820  STORE_DEREF              'hrAbs'
           2822_0  COME_FROM          2812  '2812'

 L. 810      2822  LOAD_CONST               2
             2824  STORE_FAST               'used'

 L. 811      2826  LOAD_FAST                'idx'
             2828  LOAD_CONST               2
             2830  BINARY_ADD       
             2832  STORE_FAST               'idxHr'

 L. 813      2834  LOAD_FAST                'idxHr'
             2836  LOAD_GLOBAL              len
             2838  LOAD_FAST                'words'
             2840  CALL_FUNCTION_1       1  '1 positional argument'
             2842  COMPARE_OP               <
         2844_2846  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 815      2848  LOAD_FAST                'words'
             2850  LOAD_FAST                'idxHr'
             2852  BINARY_SUBSCR    
             2854  LOAD_METHOD              isdigit
             2856  CALL_METHOD_0         0  '0 positional arguments'
         2858_2860  POP_JUMP_IF_FALSE  2918  'to 2918'

 L. 816      2862  LOAD_FAST                'wordPrev'
             2864  LOAD_FAST                'words_in'
             2866  COMPARE_OP               in
         2868_2870  POP_JUMP_IF_FALSE  2886  'to 2886'

 L. 817      2872  LOAD_GLOBAL              int
             2874  LOAD_FAST                'words'
             2876  LOAD_FAST                'idxHr'
             2878  BINARY_SUBSCR    
             2880  CALL_FUNCTION_1       1  '1 positional argument'
             2882  STORE_DEREF              'minOffset'
             2884  JUMP_FORWARD       2898  'to 2898'
           2886_0  COME_FROM          2868  '2868'

 L. 819      2886  LOAD_GLOBAL              int
             2888  LOAD_FAST                'words'
             2890  LOAD_FAST                'idxHr'
             2892  BINARY_SUBSCR    
             2894  CALL_FUNCTION_1       1  '1 positional argument'
             2896  STORE_DEREF              'minAbs'
           2898_0  COME_FROM          2884  '2884'

 L. 820      2898  LOAD_FAST                'used'
             2900  LOAD_CONST               1
             2902  INPLACE_ADD      
             2904  STORE_FAST               'used'

 L. 821      2906  LOAD_FAST                'idxHr'
             2908  LOAD_CONST               1
             2910  INPLACE_ADD      
             2912  STORE_FAST               'idxHr'
         2914_2916  JUMP_FORWARD       3268  'to 3268'
           2918_0  COME_FROM          2858  '2858'

 L. 823      2918  LOAD_FAST                'words'
             2920  LOAD_FAST                'idxHr'
             2922  BINARY_SUBSCR    
             2924  LOAD_STR                 'et'
             2926  COMPARE_OP               ==
         2928_2930  POP_JUMP_IF_FALSE  3062  'to 3062'
             2932  LOAD_FAST                'idxHr'
             2934  LOAD_CONST               1
             2936  BINARY_ADD       
             2938  LOAD_GLOBAL              len
             2940  LOAD_FAST                'words'
             2942  CALL_FUNCTION_1       1  '1 positional argument'
             2944  COMPARE_OP               <
         2946_2948  POP_JUMP_IF_FALSE  3062  'to 3062'

 L. 824      2950  LOAD_FAST                'words'
             2952  LOAD_FAST                'idxHr'
             2954  LOAD_CONST               1
             2956  BINARY_ADD       
             2958  BINARY_SUBSCR    
             2960  LOAD_STR                 'quart'
             2962  COMPARE_OP               ==
         2964_2966  POP_JUMP_IF_FALSE  3006  'to 3006'

 L. 825      2968  LOAD_FAST                'wordPrev'
             2970  LOAD_FAST                'words_in'
             2972  COMPARE_OP               in
         2974_2976  POP_JUMP_IF_FALSE  2984  'to 2984'

 L. 826      2978  LOAD_CONST               15
             2980  STORE_DEREF              'minOffset'
             2982  JUMP_FORWARD       2988  'to 2988'
           2984_0  COME_FROM          2974  '2974'

 L. 828      2984  LOAD_CONST               15
             2986  STORE_DEREF              'minAbs'
           2988_0  COME_FROM          2982  '2982'

 L. 829      2988  LOAD_FAST                'used'
             2990  LOAD_CONST               2
             2992  INPLACE_ADD      
             2994  STORE_FAST               'used'

 L. 830      2996  LOAD_FAST                'idxHr'
             2998  LOAD_CONST               2
             3000  INPLACE_ADD      
             3002  STORE_FAST               'idxHr'
             3004  JUMP_FORWARD       3060  'to 3060'
           3006_0  COME_FROM          2964  '2964'

 L. 831      3006  LOAD_FAST                'words'
             3008  LOAD_FAST                'idxHr'
             3010  LOAD_CONST               1
             3012  BINARY_ADD       
             3014  BINARY_SUBSCR    
             3016  LOAD_STR                 'demi'
             3018  COMPARE_OP               ==
         3020_3022  POP_JUMP_IF_FALSE  3268  'to 3268'

 L. 832      3024  LOAD_FAST                'wordPrev'
             3026  LOAD_FAST                'words_in'
             3028  COMPARE_OP               in
         3030_3032  POP_JUMP_IF_FALSE  3040  'to 3040'

 L. 833      3034  LOAD_CONST               30
             3036  STORE_DEREF              'minOffset'
             3038  JUMP_FORWARD       3044  'to 3044'
           3040_0  COME_FROM          3030  '3030'

 L. 835      3040  LOAD_CONST               30
             3042  STORE_DEREF              'minAbs'
           3044_0  COME_FROM          3038  '3038'

 L. 836      3044  LOAD_FAST                'used'
             3046  LOAD_CONST               2
             3048  INPLACE_ADD      
             3050  STORE_FAST               'used'

 L. 837      3052  LOAD_FAST                'idxHr'
             3054  LOAD_CONST               2
             3056  INPLACE_ADD      
             3058  STORE_FAST               'idxHr'
           3060_0  COME_FROM          3004  '3004'
             3060  JUMP_FORWARD       3268  'to 3268'
           3062_0  COME_FROM          2946  '2946'
           3062_1  COME_FROM          2928  '2928'

 L. 839      3062  LOAD_FAST                'words'
             3064  LOAD_FAST                'idxHr'
             3066  BINARY_SUBSCR    
             3068  LOAD_STR                 'moins'
             3070  COMPARE_OP               ==
         3072_3074  POP_JUMP_IF_FALSE  3268  'to 3268'

 L. 840      3076  LOAD_FAST                'idxHr'
             3078  LOAD_CONST               1
             3080  BINARY_ADD       
             3082  LOAD_GLOBAL              len
             3084  LOAD_FAST                'words'
             3086  CALL_FUNCTION_1       1  '1 positional argument'
             3088  COMPARE_OP               <
         3090_3092  POP_JUMP_IF_FALSE  3268  'to 3268'

 L. 841      3094  LOAD_FAST                'words'
             3096  LOAD_FAST                'idxHr'
             3098  LOAD_CONST               1
             3100  BINARY_ADD       
             3102  BINARY_SUBSCR    
             3104  LOAD_METHOD              isdigit
             3106  CALL_METHOD_0         0  '0 positional arguments'
         3108_3110  POP_JUMP_IF_FALSE  3198  'to 3198'

 L. 842      3112  LOAD_FAST                'wordPrev'
             3114  LOAD_FAST                'words_in'
             3116  COMPARE_OP               in
         3118_3120  POP_JUMP_IF_FALSE  3152  'to 3152'

 L. 843      3122  LOAD_DEREF               'hrOffset'
             3124  LOAD_CONST               1
             3126  INPLACE_SUBTRACT 
             3128  STORE_DEREF              'hrOffset'

 L. 844      3130  LOAD_CONST               60
             3132  LOAD_GLOBAL              int
             3134  LOAD_FAST                'words'
             3136  LOAD_FAST                'idxHr'
             3138  LOAD_CONST               1
             3140  BINARY_ADD       
             3142  BINARY_SUBSCR    
             3144  CALL_FUNCTION_1       1  '1 positional argument'
             3146  BINARY_SUBTRACT  
             3148  STORE_DEREF              'minOffset'
             3150  JUMP_FORWARD       3180  'to 3180'
           3152_0  COME_FROM          3118  '3118'

 L. 846      3152  LOAD_DEREF               'hrAbs'
             3154  LOAD_CONST               1
             3156  BINARY_SUBTRACT  
             3158  STORE_DEREF              'hrAbs'

 L. 847      3160  LOAD_CONST               60
             3162  LOAD_GLOBAL              int
             3164  LOAD_FAST                'words'
             3166  LOAD_FAST                'idxHr'
             3168  LOAD_CONST               1
             3170  BINARY_ADD       
             3172  BINARY_SUBSCR    
             3174  CALL_FUNCTION_1       1  '1 positional argument'
             3176  BINARY_SUBTRACT  
             3178  STORE_DEREF              'minAbs'
           3180_0  COME_FROM          3150  '3150'

 L. 848      3180  LOAD_FAST                'used'
             3182  LOAD_CONST               2
             3184  INPLACE_ADD      
             3186  STORE_FAST               'used'

 L. 849      3188  LOAD_FAST                'idxHr'
             3190  LOAD_CONST               2
             3192  INPLACE_ADD      
             3194  STORE_FAST               'idxHr'
             3196  JUMP_FORWARD       3268  'to 3268'
           3198_0  COME_FROM          3108  '3108'

 L. 850      3198  LOAD_FAST                'words'
             3200  LOAD_FAST                'idxHr'
             3202  LOAD_CONST               1
             3204  BINARY_ADD       
             3206  BINARY_SUBSCR    
             3208  LOAD_STR                 'quart'
             3210  COMPARE_OP               ==
         3212_3214  POP_JUMP_IF_FALSE  3268  'to 3268'

 L. 851      3216  LOAD_FAST                'wordPrev'
             3218  LOAD_FAST                'words_in'
             3220  COMPARE_OP               in
         3222_3224  POP_JUMP_IF_FALSE  3240  'to 3240'

 L. 852      3226  LOAD_DEREF               'hrOffset'
             3228  LOAD_CONST               1
             3230  INPLACE_SUBTRACT 
             3232  STORE_DEREF              'hrOffset'

 L. 853      3234  LOAD_CONST               45
             3236  STORE_DEREF              'minOffset'
             3238  JUMP_FORWARD       3252  'to 3252'
           3240_0  COME_FROM          3222  '3222'

 L. 855      3240  LOAD_DEREF               'hrAbs'
             3242  LOAD_CONST               1
             3244  BINARY_SUBTRACT  
             3246  STORE_DEREF              'hrAbs'

 L. 856      3248  LOAD_CONST               45
             3250  STORE_DEREF              'minAbs'
           3252_0  COME_FROM          3238  '3238'

 L. 857      3252  LOAD_FAST                'used'
             3254  LOAD_CONST               2
             3256  INPLACE_ADD      
             3258  STORE_FAST               'used'

 L. 858      3260  LOAD_FAST                'idxHr'
             3262  LOAD_CONST               2
             3264  INPLACE_ADD      
             3266  STORE_FAST               'idxHr'
           3268_0  COME_FROM          3212  '3212'
           3268_1  COME_FROM          3196  '3196'
           3268_2  COME_FROM          3090  '3090'
           3268_3  COME_FROM          3072  '3072'
           3268_4  COME_FROM          3060  '3060'
           3268_5  COME_FROM          3020  '3020'
           3268_6  COME_FROM          2914  '2914'

 L. 860      3268  LOAD_FAST                'idxHr'
             3270  LOAD_GLOBAL              len
             3272  LOAD_FAST                'words'
             3274  CALL_FUNCTION_1       1  '1 positional argument'
             3276  COMPARE_OP               <
         3278_3280  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 861      3282  LOAD_FAST                'words'
             3284  LOAD_FAST                'idxHr'
             3286  BINARY_SUBSCR    
             3288  LOAD_CONST               ('minutes', 'minute')
             3290  COMPARE_OP               in
         3292_3294  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 862      3296  LOAD_FAST                'used'
             3298  LOAD_CONST               1
             3300  INPLACE_ADD      
             3302  STORE_FAST               'used'

 L. 863      3304  LOAD_FAST                'idxHr'
             3306  LOAD_CONST               1
             3308  INPLACE_ADD      
             3310  STORE_FAST               'idxHr'
             3312  JUMP_FORWARD       3446  'to 3446'
           3314_0  COME_FROM          2790  '2790'
           3314_1  COME_FROM          2762  '2762'
           3314_2  COME_FROM          2752  '2752'
           3314_3  COME_FROM          2742  '2742'

 L. 864      3314  LOAD_FAST                'wordNext'
             3316  LOAD_STR                 'minutes'
             3318  COMPARE_OP               ==
         3320_3322  POP_JUMP_IF_FALSE  3358  'to 3358'

 L. 866      3324  LOAD_FAST                'wordPrev'
             3326  LOAD_FAST                'words_in'
             3328  COMPARE_OP               in
         3330_3332  POP_JUMP_IF_FALSE  3344  'to 3344'

 L. 867      3334  LOAD_GLOBAL              int
             3336  LOAD_FAST                'word'
             3338  CALL_FUNCTION_1       1  '1 positional argument'
             3340  STORE_DEREF              'minOffset'
             3342  JUMP_FORWARD       3352  'to 3352'
           3344_0  COME_FROM          3330  '3330'

 L. 869      3344  LOAD_GLOBAL              int
             3346  LOAD_FAST                'word'
             3348  CALL_FUNCTION_1       1  '1 positional argument'
             3350  STORE_DEREF              'minAbs'
           3352_0  COME_FROM          3342  '3342'

 L. 870      3352  LOAD_CONST               2
             3354  STORE_FAST               'used'
             3356  JUMP_FORWARD       3446  'to 3446'
           3358_0  COME_FROM          3320  '3320'

 L. 871      3358  LOAD_FAST                'wordNext'
             3360  LOAD_STR                 'secondes'
             3362  COMPARE_OP               ==
         3364_3366  POP_JUMP_IF_FALSE  3382  'to 3382'

 L. 873      3368  LOAD_GLOBAL              int
             3370  LOAD_FAST                'word'
             3372  CALL_FUNCTION_1       1  '1 positional argument'
             3374  STORE_DEREF              'secOffset'

 L. 874      3376  LOAD_CONST               2
             3378  STORE_FAST               'used'
             3380  JUMP_FORWARD       3446  'to 3446'
           3382_0  COME_FROM          3364  '3364'

 L. 875      3382  LOAD_GLOBAL              int
             3384  LOAD_FAST                'word'
             3386  CALL_FUNCTION_1       1  '1 positional argument'
             3388  LOAD_CONST               100
             3390  COMPARE_OP               >
         3392_3394  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 877      3396  LOAD_GLOBAL              int
             3398  LOAD_FAST                'word'
             3400  CALL_FUNCTION_1       1  '1 positional argument'
             3402  LOAD_CONST               100
             3404  BINARY_TRUE_DIVIDE
           3406_0  COME_FROM          2682  '2682'
             3406  STORE_DEREF              'hrAbs'

 L. 878      3408  LOAD_GLOBAL              int
             3410  LOAD_FAST                'word'
             3412  CALL_FUNCTION_1       1  '1 positional argument'
             3414  LOAD_DEREF               'hrAbs'
             3416  LOAD_CONST               100
             3418  BINARY_MULTIPLY  
             3420  BINARY_SUBTRACT  
             3422  STORE_DEREF              'minAbs'

 L. 879      3424  LOAD_CONST               1
             3426  STORE_FAST               'used'

 L. 880      3428  LOAD_FAST                'wordNext'
             3430  LOAD_STR                 'heures'
             3432  COMPARE_OP               ==
         3434_3436  POP_JUMP_IF_FALSE  3446  'to 3446'

 L. 881      3438  LOAD_FAST                'used'
             3440  LOAD_CONST               1
             3442  INPLACE_ADD      
             3444  STORE_FAST               'used'
           3446_0  COME_FROM          3434  '3434'
           3446_1  COME_FROM          3392  '3392'
           3446_2  COME_FROM          3380  '3380'
           3446_3  COME_FROM          3356  '3356'
           3446_4  COME_FROM          3312  '3312'
           3446_5  COME_FROM          3292  '3292'
           3446_6  COME_FROM          3278  '3278'
           3446_7  COME_FROM          2844  '2844'
           3446_8  COME_FROM          2720  '2720'

 L. 884      3446  LOAD_FAST                'timeQualifier'
         3448_3450  POP_JUMP_IF_FALSE  3536  'to 3536'

 L. 885      3452  LOAD_FAST                'timeQualifier'
             3454  LOAD_STR                 'matin'
             3456  COMPARE_OP               ==
         3458_3460  POP_JUMP_IF_FALSE  3468  'to 3468'

 L. 886      3462  LOAD_STR                 'am'
             3464  STORE_FAST               'ampm'
             3466  JUMP_FORWARD       3536  'to 3536'
           3468_0  COME_FROM          3458  '3458'

 L. 887      3468  LOAD_FAST                'timeQualifier'
             3470  LOAD_STR                 'après-midi'
             3472  COMPARE_OP               ==
         3474_3476  POP_JUMP_IF_FALSE  3484  'to 3484'

 L. 888      3478  LOAD_STR                 'pm'
             3480  STORE_FAST               'ampm'
             3482  JUMP_FORWARD       3536  'to 3536'
           3484_0  COME_FROM          3474  '3474'

 L. 889      3484  LOAD_FAST                'timeQualifier'
             3486  LOAD_STR                 'soir'
             3488  COMPARE_OP               ==
         3490_3492  POP_JUMP_IF_FALSE  3500  'to 3500'

 L. 890      3494  LOAD_STR                 'pm'
             3496  STORE_FAST               'ampm'
             3498  JUMP_FORWARD       3536  'to 3536'
           3500_0  COME_FROM          3490  '3490'

 L. 891      3500  LOAD_FAST                'timeQualifier'
             3502  LOAD_STR                 'nuit'
             3504  COMPARE_OP               ==
         3506_3508  POP_JUMP_IF_FALSE  3536  'to 3536'

 L. 892      3510  LOAD_DEREF               'hrAbs'
         3512_3514  JUMP_IF_TRUE_OR_POP  3518  'to 3518'
             3516  LOAD_CONST               0
           3518_0  COME_FROM          3512  '3512'
             3518  LOAD_CONST               8
             3520  COMPARE_OP               >
         3522_3524  POP_JUMP_IF_FALSE  3532  'to 3532'

 L. 893      3526  LOAD_STR                 'pm'
             3528  STORE_FAST               'ampm'
             3530  JUMP_FORWARD       3536  'to 3536'
           3532_0  COME_FROM          3522  '3522'

 L. 895      3532  LOAD_STR                 'am'
             3534  STORE_FAST               'ampm'
           3536_0  COME_FROM          3530  '3530'
           3536_1  COME_FROM          3506  '3506'
           3536_2  COME_FROM          3498  '3498'
           3536_3  COME_FROM          3482  '3482'
           3536_4  COME_FROM          3466  '3466'
           3536_5  COME_FROM          3448  '3448'

 L. 896      3536  LOAD_FAST                'ampm'
             3538  LOAD_STR                 'pm'
             3540  COMPARE_OP               ==
         3542_3544  POP_JUMP_IF_FALSE  3576  'to 3576'
             3546  LOAD_DEREF               'hrAbs'
         3548_3550  JUMP_IF_TRUE_OR_POP  3554  'to 3554'
             3552  LOAD_CONST               0
           3554_0  COME_FROM          3548  '3548'
             3554  LOAD_CONST               12
             3556  COMPARE_OP               <
         3558_3560  POP_JUMP_IF_FALSE  3576  'to 3576'
             3562  LOAD_DEREF               'hrAbs'
         3564_3566  JUMP_IF_TRUE_OR_POP  3570  'to 3570'
             3568  LOAD_CONST               0
           3570_0  COME_FROM          3564  '3564'
             3570  LOAD_CONST               12
             3572  BINARY_ADD       
             3574  JUMP_FORWARD       3578  'to 3578'
           3576_0  COME_FROM          3558  '3558'
           3576_1  COME_FROM          3542  '3542'

 L. 897      3576  LOAD_DEREF               'hrAbs'
           3578_0  COME_FROM          3574  '3574'
             3578  STORE_DEREF              'hrAbs'

 L. 898      3580  LOAD_FAST                'ampm'
             3582  LOAD_STR                 'am'
             3584  COMPARE_OP               ==
         3586_3588  POP_JUMP_IF_FALSE  3620  'to 3620'
             3590  LOAD_DEREF               'hrAbs'
         3592_3594  JUMP_IF_TRUE_OR_POP  3598  'to 3598'
             3596  LOAD_CONST               0
           3598_0  COME_FROM          3592  '3592'
             3598  LOAD_CONST               12
             3600  COMPARE_OP               >=
           3602_0  COME_FROM          2018  '2018'
         3602_3604  POP_JUMP_IF_FALSE  3620  'to 3620'
             3606  LOAD_DEREF               'hrAbs'
         3608_3610  JUMP_IF_TRUE_OR_POP  3614  'to 3614'
             3612  LOAD_CONST               0
           3614_0  COME_FROM          3608  '3608'
             3614  LOAD_CONST               12
             3616  BINARY_SUBTRACT  
             3618  JUMP_FORWARD       3622  'to 3622'
           3620_0  COME_FROM          3602  '3602'
           3620_1  COME_FROM          3586  '3586'

 L. 899      3620  LOAD_DEREF               'hrAbs'
           3622_0  COME_FROM          3618  '3618'
             3622  STORE_DEREF              'hrAbs'

 L. 900      3624  LOAD_DEREF               'hrAbs'
         3626_3628  JUMP_IF_TRUE_OR_POP  3632  'to 3632'
             3630  LOAD_CONST               0
           3632_0  COME_FROM          3626  '3626'
             3632  LOAD_CONST               24
             3634  COMPARE_OP               >
         3636_3638  POP_JUMP_IF_TRUE   3656  'to 3656'
             3640  LOAD_DEREF               'minAbs'
         3642_3644  JUMP_IF_TRUE_OR_POP  3648  'to 3648'
             3646  LOAD_CONST               0
           3648_0  COME_FROM          3642  '3642'
             3648  LOAD_CONST               59
             3650  COMPARE_OP               >
         3652_3654  POP_JUMP_IF_FALSE  3666  'to 3666'
           3656_0  COME_FROM          3636  '3636'

 L. 901      3656  LOAD_CONST               False
             3658  STORE_DEREF              'isTime'
           3660_0  COME_FROM          2076  '2076'

 L. 902      3660  LOAD_CONST               0
             3662  STORE_FAST               'used'
             3664  JUMP_FORWARD       3686  'to 3686'
           3666_0  COME_FROM          3652  '3652'

 L. 903      3666  LOAD_FAST                'wordPrev'
             3668  LOAD_FAST                'words_in'
             3670  COMPARE_OP               in
         3672_3674  POP_JUMP_IF_FALSE  3682  'to 3682'

 L. 904      3676  LOAD_CONST               False
             3678  STORE_DEREF              'isTime'
             3680  JUMP_FORWARD       3686  'to 3686'
           3682_0  COME_FROM          3672  '3672'

 L. 906      3682  LOAD_CONST               True
             3684  STORE_DEREF              'isTime'
           3686_0  COME_FROM          3680  '3680'
           3686_1  COME_FROM          3664  '3664'
             3686  JUMP_FORWARD       3766  'to 3766'
           3688_0  COME_FROM          2392  '2392'
           3688_1  COME_FROM          2378  '2378'

 L. 908      3688  LOAD_DEREF               'hrAbs'
         3690_3692  POP_JUMP_IF_TRUE   3766  'to 3766'
             3694  LOAD_FAST                'timeQualifier'
         3696_3698  POP_JUMP_IF_FALSE  3766  'to 3766'

 L. 909      3700  LOAD_FAST                'timeQualifier'
             3702  LOAD_STR                 'matin'
             3704  COMPARE_OP               ==
         3706_3708  POP_JUMP_IF_FALSE  3716  'to 3716'

 L. 910      3710  LOAD_CONST               8
             3712  STORE_DEREF              'hrAbs'
             3714  JUMP_FORWARD       3762  'to 3762'
           3716_0  COME_FROM          3706  '3706'

 L. 911      3716  LOAD_FAST                'timeQualifier'
             3718  LOAD_STR                 'après-midi'
             3720  COMPARE_OP               ==
         3722_3724  POP_JUMP_IF_FALSE  3732  'to 3732'

 L. 912      3726  LOAD_CONST               15
             3728  STORE_DEREF              'hrAbs'
             3730  JUMP_FORWARD       3762  'to 3762'
           3732_0  COME_FROM          3722  '3722'

 L. 913      3732  LOAD_FAST                'timeQualifier'
             3734  LOAD_STR                 'soir'
             3736  COMPARE_OP               ==
         3738_3740  POP_JUMP_IF_FALSE  3748  'to 3748'

 L. 914      3742  LOAD_CONST               19
             3744  STORE_DEREF              'hrAbs'
             3746  JUMP_FORWARD       3762  'to 3762'
           3748_0  COME_FROM          3738  '3738'

 L. 915      3748  LOAD_FAST                'timeQualifier'
             3750  LOAD_STR                 'nuit'
             3752  COMPARE_OP               ==
         3754_3756  POP_JUMP_IF_FALSE  3762  'to 3762'

 L. 916      3758  LOAD_CONST               2
             3760  STORE_DEREF              'hrAbs'
           3762_0  COME_FROM          3754  '3754'
           3762_1  COME_FROM          3746  '3746'
           3762_2  COME_FROM          3730  '3730'
           3762_3  COME_FROM          3714  '3714'

 L. 917      3762  LOAD_CONST               True
             3764  STORE_DEREF              'isTime'
           3766_0  COME_FROM          3696  '3696'
           3766_1  COME_FROM          3690  '3690'
           3766_2  COME_FROM          3686  '3686'
           3766_3  COME_FROM          2364  '2364'
           3766_4  COME_FROM          2344  '2344'
           3766_5  COME_FROM          2180  '2180'
           3766_6  COME_FROM          2144  '2144'
           3766_7  COME_FROM          2084  '2084'

 L. 919      3766  LOAD_FAST                'used'
             3768  LOAD_CONST               0
             3770  COMPARE_OP               >
         3772_3774  POP_JUMP_IF_FALSE  1780  'to 1780'

 L. 921      3776  SETUP_LOOP         3810  'to 3810'
             3778  LOAD_GLOBAL              range
             3780  LOAD_CONST               0
             3782  LOAD_FAST                'used'
             3784  CALL_FUNCTION_2       2  '2 positional arguments'
             3786  GET_ITER         
             3788  FOR_ITER           3808  'to 3808'
             3790  STORE_FAST               'i'

 L. 922      3792  LOAD_STR                 ''
             3794  LOAD_FAST                'words'
             3796  LOAD_FAST                'i'
             3798  LOAD_FAST                'start'
             3800  BINARY_ADD       
             3802  STORE_SUBSCR     
         3804_3806  JUMP_BACK          3788  'to 3788'
             3808  POP_BLOCK        
           3810_0  COME_FROM_LOOP     3776  '3776'

 L. 924      3810  LOAD_FAST                'start'
             3812  LOAD_CONST               1
             3814  BINARY_SUBTRACT  
             3816  LOAD_CONST               0
             3818  COMPARE_OP               >=
         3820_3822  POP_JUMP_IF_FALSE  3854  'to 3854'
             3824  LOAD_FAST                'words'
             3826  LOAD_FAST                'start'
             3828  LOAD_CONST               1
             3830  BINARY_SUBTRACT  
             3832  BINARY_SUBSCR    
             3834  LOAD_FAST                'markers'
             3836  COMPARE_OP               in
         3838_3840  POP_JUMP_IF_FALSE  3854  'to 3854'

 L. 925      3842  LOAD_STR                 ''
             3844  LOAD_FAST                'words'
             3846  LOAD_FAST                'start'
             3848  LOAD_CONST               1
             3850  BINARY_SUBTRACT  
             3852  STORE_SUBSCR     
           3854_0  COME_FROM          3838  '3838'
           3854_1  COME_FROM          3820  '3820'

 L. 927      3854  LOAD_FAST                'idx'
             3856  LOAD_FAST                'used'
             3858  LOAD_CONST               1
             3860  BINARY_SUBTRACT  
             3862  INPLACE_ADD      
             3864  STORE_FAST               'idx'

 L. 928      3866  LOAD_CONST               True
             3868  STORE_DEREF              'found'
         3870_3872  JUMP_BACK          1780  'to 1780'
             3874  POP_BLOCK        
           3876_0  COME_FROM_LOOP     1768  '1768'

 L. 931      3876  LOAD_FAST                'date_found'
             3878  CALL_FUNCTION_0       0  '0 positional arguments'
         3880_3882  POP_JUMP_IF_TRUE   3888  'to 3888'

 L. 932      3884  LOAD_CONST               None
             3886  RETURN_VALUE     
           3888_0  COME_FROM          3880  '3880'

 L. 934      3888  LOAD_DEREF               'dayOffset'
             3890  LOAD_CONST               False
             3892  COMPARE_OP               is
         3894_3896  POP_JUMP_IF_FALSE  3902  'to 3902'

 L. 935      3898  LOAD_CONST               0
             3900  STORE_DEREF              'dayOffset'
           3902_0  COME_FROM          3894  '3894'

 L. 938      3902  LOAD_FAST                'dateNow'
             3904  STORE_FAST               'extractedDate'

 L. 939      3906  LOAD_FAST                'extractedDate'
             3908  LOAD_ATTR                replace
             3910  LOAD_CONST               0

 L. 940      3912  LOAD_CONST               0

 L. 941      3914  LOAD_CONST               0

 L. 942      3916  LOAD_CONST               0
             3918  LOAD_CONST               ('microsecond', 'second', 'minute', 'hour')
             3920  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             3922  STORE_FAST               'extractedDate'

 L. 943      3924  LOAD_DEREF               'datestr'
             3926  LOAD_STR                 ''
             3928  COMPARE_OP               !=
         3930_3932  POP_JUMP_IF_FALSE  4122  'to 4122'

 L. 944      3934  LOAD_FAST                'hasYear'
         3936_3938  POP_JUMP_IF_TRUE   4064  'to 4064'

 L. 945      3940  LOAD_GLOBAL              datetime
             3942  LOAD_METHOD              strptime
             3944  LOAD_DEREF               'datestr'
             3946  LOAD_STR                 '%B %d'
             3948  CALL_METHOD_2         2  '2 positional arguments'
             3950  STORE_FAST               'temp'

 L. 946      3952  LOAD_FAST                'temp'
             3954  LOAD_ATTR                replace
             3956  LOAD_FAST                'extractedDate'
             3958  LOAD_ATTR                year
             3960  LOAD_CONST               ('year',)
             3962  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3964  STORE_FAST               'temp'

 L. 947      3966  LOAD_FAST                'extractedDate'
             3968  LOAD_FAST                'temp'
             3970  COMPARE_OP               <
         3972_3974  POP_JUMP_IF_FALSE  4018  'to 4018'

 L. 948      3976  LOAD_FAST                'extractedDate'
             3978  LOAD_ATTR                replace
             3980  LOAD_GLOBAL              int
             3982  LOAD_FAST                'currentYear'
             3984  CALL_FUNCTION_1       1  '1 positional argument'

 L. 949      3986  LOAD_GLOBAL              int

 L. 950      3988  LOAD_FAST                'temp'
             3990  LOAD_METHOD              strftime

 L. 951      3992  LOAD_STR                 '%m'
             3994  CALL_METHOD_1         1  '1 positional argument'
             3996  CALL_FUNCTION_1       1  '1 positional argument'

 L. 952      3998  LOAD_GLOBAL              int
             4000  LOAD_FAST                'temp'
             4002  LOAD_METHOD              strftime

 L. 953      4004  LOAD_STR                 '%d'
             4006  CALL_METHOD_1         1  '1 positional argument'
             4008  CALL_FUNCTION_1       1  '1 positional argument'
             4010  LOAD_CONST               ('year', 'month', 'day')
             4012  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4014  STORE_FAST               'extractedDate'
             4016  JUMP_FORWARD       4062  'to 4062'
           4018_0  COME_FROM          3972  '3972'

 L. 955      4018  LOAD_FAST                'extractedDate'
             4020  LOAD_ATTR                replace

 L. 956      4022  LOAD_GLOBAL              int
             4024  LOAD_FAST                'currentYear'
             4026  CALL_FUNCTION_1       1  '1 positional argument'
             4028  LOAD_CONST               1
             4030  BINARY_ADD       

 L. 957      4032  LOAD_GLOBAL              int
             4034  LOAD_FAST                'temp'
             4036  LOAD_METHOD              strftime
             4038  LOAD_STR                 '%m'
             4040  CALL_METHOD_1         1  '1 positional argument'
             4042  CALL_FUNCTION_1       1  '1 positional argument'

 L. 958      4044  LOAD_GLOBAL              int
             4046  LOAD_FAST                'temp'
             4048  LOAD_METHOD              strftime
             4050  LOAD_STR                 '%d'
             4052  CALL_METHOD_1         1  '1 positional argument'
             4054  CALL_FUNCTION_1       1  '1 positional argument'
             4056  LOAD_CONST               ('year', 'month', 'day')
             4058  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4060  STORE_FAST               'extractedDate'
           4062_0  COME_FROM          4016  '4016'
             4062  JUMP_FORWARD       4122  'to 4122'
           4064_0  COME_FROM          3936  '3936'

 L. 960      4064  LOAD_GLOBAL              datetime
             4066  LOAD_METHOD              strptime
             4068  LOAD_DEREF               'datestr'
             4070  LOAD_STR                 '%B %d %Y'
             4072  CALL_METHOD_2         2  '2 positional arguments'
             4074  STORE_FAST               'temp'

 L. 961      4076  LOAD_FAST                'extractedDate'
             4078  LOAD_ATTR                replace

 L. 962      4080  LOAD_GLOBAL              int
             4082  LOAD_FAST                'temp'
             4084  LOAD_METHOD              strftime
             4086  LOAD_STR                 '%Y'
             4088  CALL_METHOD_1         1  '1 positional argument'
             4090  CALL_FUNCTION_1       1  '1 positional argument'

 L. 963      4092  LOAD_GLOBAL              int
             4094  LOAD_FAST                'temp'
             4096  LOAD_METHOD              strftime
             4098  LOAD_STR                 '%m'
             4100  CALL_METHOD_1         1  '1 positional argument'
             4102  CALL_FUNCTION_1       1  '1 positional argument'

 L. 964      4104  LOAD_GLOBAL              int
             4106  LOAD_FAST                'temp'
             4108  LOAD_METHOD              strftime
             4110  LOAD_STR                 '%d'
             4112  CALL_METHOD_1         1  '1 positional argument'
             4114  CALL_FUNCTION_1       1  '1 positional argument'
             4116  LOAD_CONST               ('year', 'month', 'day')
             4118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4120  STORE_FAST               'extractedDate'
           4122_0  COME_FROM          4062  '4062'
           4122_1  COME_FROM          3930  '3930'

 L. 966      4122  LOAD_DEREF               'yearOffset'
             4124  LOAD_CONST               0
             4126  COMPARE_OP               !=
         4128_4130  POP_JUMP_IF_FALSE  4146  'to 4146'

 L. 967      4132  LOAD_FAST                'extractedDate'
             4134  LOAD_GLOBAL              relativedelta
             4136  LOAD_DEREF               'yearOffset'
             4138  LOAD_CONST               ('years',)
             4140  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4142  BINARY_ADD       
             4144  STORE_FAST               'extractedDate'
           4146_0  COME_FROM          4128  '4128'

 L. 968      4146  LOAD_DEREF               'monthOffset'
             4148  LOAD_CONST               0
             4150  COMPARE_OP               !=
         4152_4154  POP_JUMP_IF_FALSE  4170  'to 4170'

 L. 969      4156  LOAD_FAST                'extractedDate'
             4158  LOAD_GLOBAL              relativedelta
             4160  LOAD_DEREF               'monthOffset'
             4162  LOAD_CONST               ('months',)
             4164  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4166  BINARY_ADD       
             4168  STORE_FAST               'extractedDate'
           4170_0  COME_FROM          4152  '4152'

 L. 970      4170  LOAD_DEREF               'dayOffset'
             4172  LOAD_CONST               0
             4174  COMPARE_OP               !=
         4176_4178  POP_JUMP_IF_FALSE  4194  'to 4194'

 L. 971      4180  LOAD_FAST                'extractedDate'
             4182  LOAD_GLOBAL              relativedelta
             4184  LOAD_DEREF               'dayOffset'
             4186  LOAD_CONST               ('days',)
             4188  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4190  BINARY_ADD       
             4192  STORE_FAST               'extractedDate'
           4194_0  COME_FROM          4176  '4176'

 L. 973      4194  LOAD_DEREF               'hrAbs'
             4196  LOAD_CONST               None
             4198  COMPARE_OP               is
         4200_4202  POP_JUMP_IF_FALSE  4232  'to 4232'
             4204  LOAD_DEREF               'minAbs'
             4206  LOAD_CONST               None
             4208  COMPARE_OP               is
         4210_4212  POP_JUMP_IF_FALSE  4232  'to 4232'
             4214  LOAD_FAST                'default_time'
         4216_4218  POP_JUMP_IF_FALSE  4232  'to 4232'

 L. 974      4220  LOAD_FAST                'default_time'
             4222  LOAD_ATTR                hour
             4224  STORE_DEREF              'hrAbs'

 L. 975      4226  LOAD_FAST                'default_time'
             4228  LOAD_ATTR                minute
             4230  STORE_DEREF              'minAbs'
           4232_0  COME_FROM          4216  '4216'
           4232_1  COME_FROM          4210  '4210'
           4232_2  COME_FROM          4200  '4200'

 L. 976      4232  LOAD_DEREF               'hrAbs'
             4234  LOAD_CONST               -1
             4236  COMPARE_OP               !=
         4238_4240  POP_JUMP_IF_FALSE  4332  'to 4332'
             4242  LOAD_DEREF               'minAbs'
             4244  LOAD_CONST               -1
             4246  COMPARE_OP               !=
         4248_4250  POP_JUMP_IF_FALSE  4332  'to 4332'

 L. 977      4252  LOAD_FAST                'extractedDate'
             4254  LOAD_GLOBAL              relativedelta
             4256  LOAD_DEREF               'hrAbs'
         4258_4260  JUMP_IF_TRUE_OR_POP  4264  'to 4264'
             4262  LOAD_CONST               0
           4264_0  COME_FROM          4258  '4258'

 L. 978      4264  LOAD_DEREF               'minAbs'
         4266_4268  JUMP_IF_TRUE_OR_POP  4272  'to 4272'
             4270  LOAD_CONST               0
           4272_0  COME_FROM          4266  '4266'
             4272  LOAD_CONST               ('hours', 'minutes')
             4274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             4276  BINARY_ADD       
             4278  STORE_FAST               'extractedDate'

 L. 979      4280  LOAD_DEREF               'hrAbs'
         4282_4284  POP_JUMP_IF_TRUE   4292  'to 4292'
             4286  LOAD_DEREF               'minAbs'
         4288_4290  POP_JUMP_IF_FALSE  4332  'to 4332'
           4292_0  COME_FROM          4282  '4282'
             4292  LOAD_DEREF               'datestr'
             4294  LOAD_STR                 ''
             4296  COMPARE_OP               ==
         4298_4300  POP_JUMP_IF_FALSE  4332  'to 4332'

 L. 980      4302  LOAD_FAST                'daySpecified'
         4304_4306  POP_JUMP_IF_TRUE   4332  'to 4332'
             4308  LOAD_FAST                'dateNow'
             4310  LOAD_FAST                'extractedDate'
             4312  COMPARE_OP               >
         4314_4316  POP_JUMP_IF_FALSE  4332  'to 4332'

 L. 981      4318  LOAD_FAST                'extractedDate'
             4320  LOAD_GLOBAL              relativedelta
             4322  LOAD_CONST               1
             4324  LOAD_CONST               ('days',)
             4326  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4328  BINARY_ADD       
             4330  STORE_FAST               'extractedDate'
           4332_0  COME_FROM          4314  '4314'
           4332_1  COME_FROM          4304  '4304'
           4332_2  COME_FROM          4298  '4298'
           4332_3  COME_FROM          4288  '4288'
           4332_4  COME_FROM          4248  '4248'
           4332_5  COME_FROM          4238  '4238'

 L. 982      4332  LOAD_DEREF               'hrOffset'
             4334  LOAD_CONST               0
             4336  COMPARE_OP               !=
         4338_4340  POP_JUMP_IF_FALSE  4356  'to 4356'

 L. 983      4342  LOAD_FAST                'extractedDate'
             4344  LOAD_GLOBAL              relativedelta
             4346  LOAD_DEREF               'hrOffset'
             4348  LOAD_CONST               ('hours',)
             4350  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4352  BINARY_ADD       
             4354  STORE_FAST               'extractedDate'
           4356_0  COME_FROM          4338  '4338'

 L. 984      4356  LOAD_DEREF               'minOffset'
             4358  LOAD_CONST               0
             4360  COMPARE_OP               !=
         4362_4364  POP_JUMP_IF_FALSE  4380  'to 4380'

 L. 985      4366  LOAD_FAST                'extractedDate'
             4368  LOAD_GLOBAL              relativedelta
             4370  LOAD_DEREF               'minOffset'
             4372  LOAD_CONST               ('minutes',)
             4374  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4376  BINARY_ADD       
             4378  STORE_FAST               'extractedDate'
           4380_0  COME_FROM          4362  '4362'

 L. 986      4380  LOAD_DEREF               'secOffset'
             4382  LOAD_CONST               0
             4384  COMPARE_OP               !=
         4386_4388  POP_JUMP_IF_FALSE  4404  'to 4404'

 L. 987      4390  LOAD_FAST                'extractedDate'
             4392  LOAD_GLOBAL              relativedelta
             4394  LOAD_DEREF               'secOffset'
             4396  LOAD_CONST               ('seconds',)
             4398  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             4400  BINARY_ADD       
             4402  STORE_FAST               'extractedDate'
           4404_0  COME_FROM          4386  '4386'

 L. 988      4404  SETUP_LOOP         4486  'to 4486'
             4406  LOAD_GLOBAL              enumerate
             4408  LOAD_FAST                'words'
             4410  CALL_FUNCTION_1       1  '1 positional argument'
             4412  GET_ITER         
           4414_0  COME_FROM          4468  '4468'
           4414_1  COME_FROM          4450  '4450'
           4414_2  COME_FROM          4432  '4432'
             4414  FOR_ITER           4484  'to 4484'
             4416  UNPACK_SEQUENCE_2     2 
             4418  STORE_FAST               'idx'
             4420  STORE_FAST               'word'

 L. 989      4422  LOAD_FAST                'words'
             4424  LOAD_FAST                'idx'
             4426  BINARY_SUBSCR    
             4428  LOAD_STR                 'et'
             4430  COMPARE_OP               ==
         4432_4434  POP_JUMP_IF_FALSE  4414  'to 4414'
             4436  LOAD_FAST                'words'
             4438  LOAD_FAST                'idx'
             4440  LOAD_CONST               1
             4442  BINARY_SUBTRACT  
             4444  BINARY_SUBSCR    
             4446  LOAD_STR                 ''
             4448  COMPARE_OP               ==
         4450_4452  POP_JUMP_IF_FALSE  4414  'to 4414'

 L. 990      4454  LOAD_FAST                'words'
             4456  LOAD_FAST                'idx'
             4458  LOAD_CONST               1
             4460  BINARY_ADD       
             4462  BINARY_SUBSCR    
             4464  LOAD_STR                 ''
             4466  COMPARE_OP               ==
         4468_4470  POP_JUMP_IF_FALSE  4414  'to 4414'

 L. 991      4472  LOAD_STR                 ''
             4474  LOAD_FAST                'words'
             4476  LOAD_FAST                'idx'
             4478  STORE_SUBSCR     
         4480_4482  JUMP_BACK          4414  'to 4414'
             4484  POP_BLOCK        
           4486_0  COME_FROM_LOOP     4404  '4404'

 L. 993      4486  LOAD_STR                 ' '
             4488  LOAD_METHOD              join
             4490  LOAD_FAST                'words'
             4492  CALL_METHOD_1         1  '1 positional argument'
             4494  STORE_FAST               'resultStr'

 L. 994      4496  LOAD_STR                 ' '
             4498  LOAD_METHOD              join
             4500  LOAD_FAST                'resultStr'
             4502  LOAD_METHOD              split
             4504  CALL_METHOD_0         0  '0 positional arguments'
             4506  CALL_METHOD_1         1  '1 positional argument'
             4508  STORE_FAST               'resultStr'

 L. 995      4510  LOAD_FAST                'extractedDate'
             4512  LOAD_FAST                'resultStr'
             4514  BUILD_LIST_2          2 
             4516  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 1256


def isFractional_fr(input_str):
    """
    This function takes the given text and checks if it is a fraction.
    Args:
        input_str (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    input_str = input_str.lower()
    if input_str != 'tiers':
        if input_str.endswith('s', -1):
            input_str = input_str[:len(input_str) - 1]
    aFrac = [
     'entier', 'demi', 'tiers', 'quart', 'cinquième', 'sixième',
     'septième', 'huitième', 'neuvième', 'dixième', 'onzième',
     'douzième', 'treizième', 'quatorzième', 'quinzième', 'seizième',
     'dix-septième', 'dix-huitième', 'dix-neuvième', 'vingtième']
    if input_str in aFrac:
        return 1.0 / (aFrac.index(input_str) + 1)
    if getOrdinal_fr(input_str):
        return 1.0 / getOrdinal_fr(input_str)
    if input_str == 'trentième':
        return 0.03333333333333333
    if input_str == 'centième':
        return 0.01
    if input_str == 'millième':
        return 0.001
    return False


def normalize_fr(text, remove_articles):
    """ French string normalization """
    text = text.lower()
    words = text.split()
    normalized = ''
    i = 0
    while i < len(words):
        if remove_articles:
            if words[i] in articles_fr:
                i += 1
                continue
            elif remove_articles and words[i][:2] in ("l'", "d'"):
                words[i] = words[i][2:]
            if words[i] in ('?', '!', ';', '…'):
                i += 1
                continue
        elif i > 0:
            if words[(i - 1)] in articles_fr:
                result = number_ordinal_fr(words, i)
                if result is not None:
                    val, i = result
                    normalized += ' ' + str(val)
                    continue
        result = number_parse_fr(words, i)
        if result is not None:
            val, i = result
            normalized += ' ' + str(val)
            continue
        normalized += ' ' + words[i]
        i += 1

    return normalized[1:]


def extract_numbers_fr(text, short_scale=True, ordinals=False):
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
    return extract_numbers_generic(text, pronounce_number_fr, extractnumber_fr, short_scale=short_scale,
      ordinals=ordinals)