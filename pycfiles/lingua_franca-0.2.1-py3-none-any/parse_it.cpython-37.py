# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_it.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 46121 bytes
"""
    Parse functions for Italian (IT-IT)

"""
import collections
from datetime import datetime
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions, extract_numbers_generic
from lingua_franca.lang.format_it import LONG_SCALE_IT, SHORT_SCALE_IT, pronounce_number_it
SHORT_ORDINAL_STRING_IT = {1:'primo', 
 2:'secondo', 
 3:'terzo', 
 4:'quarto', 
 5:'quinto', 
 6:'sesto', 
 7:'settimo', 
 8:'ottavo', 
 9:'nono', 
 10:'decimo', 
 11:'undicesimo', 
 12:'dodicesimo', 
 13:'tredicesimo', 
 14:'quattordicesimo', 
 15:'quindicesimo', 
 16:'sedicesimo', 
 17:'diciassettesimo', 
 18:'diciottesimo', 
 19:'diciannovesimo', 
 20:'ventesimo', 
 30:'trentesimo', 
 40:'quarantesimo', 
 50:'cinquantesimo', 
 60:'sessantesimo', 
 70:'settantesimo', 
 80:'ottantesimo', 
 90:'novantesimo', 
 100.0:'centesimo', 
 1000.0:'millesimo', 
 1000000.0:'milionesimo', 
 1000000000.0:'miliardesimo', 
 1000000000000.0:'trilionesimo', 
 1000000000000000.0:'quadrilionesimo', 
 1e+18:'quintilionesim', 
 1e+21:'sestilionesimo', 
 1e+24:'settilionesimo', 
 1e+27:'ottilionesimo', 
 1e+30:'nonilionesimo', 
 1e+33:'decilionesimo'}
LONG_ORDINAL_STRING_IT = {1:'primo', 
 2:'secondo', 
 3:'terzo', 
 4:'quarto', 
 5:'quinto', 
 6:'sesto', 
 7:'settimo', 
 8:'ottavo', 
 9:'nono', 
 10:'decimo', 
 11:'undicesimo', 
 12:'dodicesimo', 
 13:'tredicesimo', 
 14:'quattordicesimo', 
 15:'quindicesimo', 
 16:'sedicesimo', 
 17:'diciassettesimo', 
 18:'diciottesimo', 
 19:'diciannovesimo', 
 20:'ventesimo', 
 30:'trentesimo', 
 40:'quarantesimo', 
 50:'cinquantesimo', 
 60:'sessantesimo', 
 70:'settantesimo', 
 80:'ottantesimo', 
 90:'novantesimo', 
 100.0:'centesimo', 
 1000.0:'millesimo', 
 1000000.0:'milionesimo', 
 1000000000000.0:'bilionesimo', 
 1e+18:'trilionesimo', 
 1e+24:'quadrilionesimo', 
 1e+30:'quintilionesimo', 
 1e+36:'sestilionesimo', 
 1e+42:'settilionesimo', 
 1e+48:'ottilionesimo', 
 1e+54:'nonilionesimo', 
 1e+60:'decilionesimo'}
ARTICLES_IT = [
 'il', 'lo', 'la', 'i', 'gli', 'le']
STRING_NUM_ITA = {'zero':0, 
 'un':1, 
 'uno':1, 
 'una':1, 
 "un'":1, 
 'due':2, 
 'tre':3, 
 'quattro':4, 
 'cinque':5, 
 'sei':6, 
 'sette':7, 
 'otto':8, 
 'nove':9, 
 'dieci':10, 
 'undici':11, 
 'dodici':12, 
 'tredici':13, 
 'quattordici':14, 
 'quindici':15, 
 'sedici':16, 
 'diciassette':17, 
 'diciotto':18, 
 'diciannove':19, 
 'venti':20, 
 'vent':20, 
 'trenta':30, 
 'trent':30, 
 'quaranta':40, 
 'quarant':40, 
 'cinquanta':50, 
 'cinquant':50, 
 'sessanta':60, 
 'sessant':60, 
 'settanta':70, 
 'settant':70, 
 'ottanta':80, 
 'ottant':80, 
 'novanta':90, 
 'novant':90, 
 'cento':100, 
 'duecento':200, 
 'trecento':300, 
 'quattrocento':400, 
 'cinquecento':500, 
 'seicento':600, 
 'settecento':700, 
 'ottocento':800, 
 'novecento':900, 
 'mille':1000, 
 'mila':1000, 
 'centomila':100000, 
 'milione':1000000, 
 'miliardo':1000000000, 
 'primo':1, 
 'secondo':2, 
 'mezzo':0.5, 
 'mezza':0.5, 
 'paio':2, 
 'decina':10, 
 'decine':10, 
 'dozzina':12, 
 'dozzine':12, 
 'centinaio':100, 
 'centinaia':100, 
 'migliaio':1000, 
 'migliaia':1000}

def isFractional_it(input_str, short_scale=False):
    """
    This function takes the given text and checks if it is a fraction.
    Updated to italian from en version 18.8.9

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    if input_str.endswith('i', -1):
        if len(input_str) > 2:
            input_str = input_str[:-1] + 'o'
    fracts_it = {'intero':1, 
     'mezza':2,  'mezzo':2}
    if short_scale:
        for num in SHORT_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[SHORT_ORDINAL_STRING_IT[num]] = num

    else:
        for num in LONG_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[LONG_ORDINAL_STRING_IT[num]] = num

    if input_str in fracts_it:
        return 1.0 / fracts_it[input_str]
    return False


def extractnumber_long_it(word):
    """
     This function converts a long textual number like
     milleventisette -> 1027 diecimila -> 10041 in
     integer value, covers from  0 to 999999999999999
     for now limited to 999_e21 but ready for 999_e63
     example:
        milleventisette -> 1027
        diecimilaquarantuno-> 10041
        centottomiladuecentotredici -> 108213
    Args:
         word (str): the word to convert in number
    Returns:
         (bool) or (int): The extracted number or False if no number
                                   was found
    """
    units = {'zero':0, 
     'uno':1,  'due':2,  'tre':3,  'quattro':4,  'cinque':5, 
     'sei':6,  'sette':7,  'otto':8,  'nove':9}
    tens = {'dieci':10, 
     'venti':20,  'trenta':30,  'quaranta':40,  'cinquanta':50, 
     'sessanta':60,  'settanta':70,  'ottanta':80,  'novanta':90}
    tens_short = {'vent':20, 
     'trent':30,  'quarant':40,  'cinquant':50,  'sessant':60, 
     'settant':70,  'ottant':80,  'novant':90}
    nums_long = {'undici':11, 
     'dodici':12,  'tredici':13,  'quattordici':14,  'quindici':15, 
     'sedici':16,  'diciassette':17,  'diciotto':18, 
     'diciannove':19}
    multipli_it = collections.OrderedDict([
     (1e+21, 'triliardi'),
     (1e+18, 'trilioni'),
     (1000000000000000.0, 'biliardi'),
     (1000000000000.0, 'bilioni'),
     (1000000000.0, 'miliardi'),
     (1000000.0, 'milioni')])
    multiplier = {}
    un_multiplier = {}
    for num in multipli_it:
        if num > 1000 and num <= 1e+21:
            multiplier[multipli_it[num]] = int(num)
            if multipli_it[num][-5:-1] == 'iard':
                un_multiplier['un' + multipli_it[num][:-1] + 'o'] = int(num)
            else:
                un_multiplier['un' + multipli_it[num][:-1] + 'e'] = int(num)

    value = False
    if word[-5:-1] == 'esim':
        base = word[:-5]
        normalize_ita3 = {'tre':'',  'ttr':'o',  'sei':'',  'ott':'o'}
        normalize_ita2 = {'un':'o',  'du':'e',  'qu':'e',  'tt':'e',  'ov':'e'}
        if base[-3:] in normalize_ita3:
            base += normalize_ita3[base[-3:]]
        else:
            if base[-2:] in normalize_ita2:
                base += normalize_ita2[base[-2:]]
        word = base
    else:
        for item in un_multiplier:
            components = word.split(item, 1)
            if len(components) == 2:
                if not (components[0] or components[1]):
                    word = str(int(un_multiplier[item]))
                else:
                    word = str(int(un_multiplier[item]) + extractnumber_long_it(components[1]))

        for item in multiplier:
            components = word.split(item, 1)
            if len(components) == 2:
                if not components[0]:
                    word = str(int(multiplier[item]) + extractnumber_long_it(components[1]))
                elif not components[1]:
                    word = str(extractnumber_long_it(components[0])) + '*' + str(int(multiplier[item]))
                else:
                    word = str(extractnumber_long_it(components[0])) + '*' + str(int(multiplier[item])) + '+' + str(extractnumber_long_it(components[1]))

        for item in tens:
            word = word.replace(item, '+' + str(tens[item]))

        for item in tens_short:
            word = word.replace(item, '+' + str(tens_short[item]))

        for item in nums_long:
            word = word.replace(item, '+' + str(nums_long[item]))

        word = word.replace('cento', '+1xx')
        word = word.replace('cent', '+1xx')
        word = word.replace('mille', '+1000')
        word = word.replace('mila', '*1000')
        for item in units:
            word = word.replace(item, '+' + str(units[item]))

        occorrenze = word.count('+1xx')
        for _ in range(0, occorrenze):
            components = word.rsplit('+1xx', 1)
            if len(components[0]) > 1 and components[0].endswith('0'):
                word = components[0] + '+100' + components[1]
            else:
                word = components[0] + '*100' + components[1]

        components = word.rsplit('*1000', 1)
        if len(components) == 2:
            if components[0].startswith('*'):
                components[0] = components[0][1:]
            word = str(extractnumber_long_it(components[0])) + '*1000' + str(components[1])
        if not word.startswith('*'):
            if word.startswith('+'):
                word = word[1:]
            addends = word.split('+')
            for c, _ in enumerate(addends):
                if '*' in addends[c]:
                    factors = addends[c].split('*')
                    result = int(factors[0]) * int(factors[1])
                    if len(factors) == 3:
                        result *= int(factors[2])
                    addends[c] = str(result)

            if all([s.isdecimal() for s in addends]):
                value = sum([int(s) for s in addends])
        else:
            value = False
    return value


def extractnumber_it(text, short_scale=False, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    text = text.lower()
    string_num_ordinal_it = {}
    if ordinals:
        if short_scale:
            for num in SHORT_ORDINAL_STRING_IT:
                num_string = SHORT_ORDINAL_STRING_IT[num]
                string_num_ordinal_it[num_string] = num
                STRING_NUM_ITA[num_string] = num

        else:
            for num in LONG_ORDINAL_STRING_IT:
                num_string = LONG_ORDINAL_STRING_IT[num]
                string_num_ordinal_it[num_string] = num
                STRING_NUM_ITA[num_string] = num

    negatives = [
     'meno']
    multiplies = [
     'decina', 'decine', 'dozzina', 'dozzine',
     'centinaia', 'centinaio', 'migliaia', 'migliaio', 'mila']
    fraction_marker = [
     ' e ']
    decimal_marker = [
     ' punto ', ' virgola ']
    if short_scale:
        for num in SHORT_SCALE_IT:
            num_string = SHORT_SCALE_IT[num]
            STRING_NUM_ITA[num_string] = num
            multiplies.append(num_string)

    else:
        for num in LONG_SCALE_IT:
            num_string = LONG_SCALE_IT[num]
            STRING_NUM_ITA[num_string] = num
            multiplies.append(num_string)

    for separator in fraction_marker:
        components = text.split(separator)
        zeros = 0
        if len(components) == 2:
            sub_components = components[1].split(' ')
            for element in sub_components:
                if element == 'zero' or element == '0':
                    zeros += 1
                else:
                    break

            num1 = extractnumber_it(components[0])
            num2 = extractnumber_it(components[1])
        if num1 is not None and num2 is not None and num1 >= 1:
            if 0 < num2 < 1:
                return num1 + num2
            if num1 is not None and num2 is not None and num1 >= 1 and num2 > 1:
                return num1 + num2 / pow(10, len(str(num2)) + zeros)

    for separator in decimal_marker:
        zeros = 0
        components = text.split(separator)
        if len(components) == 2:
            sub_components = components[1].split(' ')
            for element in sub_components:
                if element == 'zero' or element == '0':
                    zeros += 1
                else:
                    break

            number = int(extractnumber_it(components[0]))
            decimal = int(extractnumber_it(components[1]))
            if number is not None and decimal is not None and '.' not in str(decimal):
                return number + decimal / pow(10, len(str(decimal)) + zeros)

    all_words = text.split()
    val = False
    prev_val = None
    to_sum = []
    for idx, word in enumerate(all_words):
        if not word:
            continue
        else:
            prev_word = all_words[(idx - 1)] if idx > 0 else ''
            next_word = all_words[(idx + 1)] if idx + 1 < len(all_words) else ''
            if is_numeric(word):
                val = float(word)
            if word in STRING_NUM_ITA:
                val = STRING_NUM_ITA[word]
            if isFractional_it(word):
                if prev_val:
                    if word[:-1] == 'second':
                        val = ordinals or prev_val * 2
                    else:
                        val = prev_val
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val
        if val is False:
            val = isFractional_it(word, short_scale=short_scale)
        if not ordinals:
            next_value = isFractional_it(next_word, short_scale=short_scale)
            if next_value:
                if not val:
                    val = 1
                val = val * next_value
            if val:
                if prev_word:
                    if prev_word in negatives:
                        val = 0 - val
                if not val:
                    val = extractnumber_long_it(word)
                if not val:
                    all_pieces = word.split('/')
                    if look_for_fractions(all_pieces):
                        val = float(all_pieces[0]) / float(all_pieces[1])
            else:
                prev_val = val
                if word in multiplies:
                    if next_word not in multiplies:
                        to_sum.append(val)
                        val = 0
                        prev_val = 0
                if extractnumber_long_it(word) > 100:
                    if extractnumber_long_it(next_word) and next_word not in multiplies:
                        to_sum.append(val)
                        val = 0
                        prev_val = 0

    if val is not None:
        for addend in to_sum:
            val = val + addend

    return val


def normalize_it(text, remove_articles):
    """ IT string normalization """
    text = text.replace('un paio', 'due')
    words = text.split()
    normalized = ''
    i = 0
    while i < len(words):
        word = words[i]
        if remove_articles:
            if word in ARTICLES_IT:
                i += 1
                continue
        if word in STRING_NUM_ITA:
            word = str(STRING_NUM_ITA[word])
        val = int(extractnumber_it(word))
        if val:
            word = str(val)
        normalized += ' ' + word
        i += 1

    return normalized[1:]


def extract_datetime_it--- This code section failed: ---

 L. 601         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_it.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 648         8  LOAD_CLOSURE             'datestr'
               10  LOAD_CLOSURE             'day_offset'
               12  LOAD_CLOSURE             'found'
               14  LOAD_CLOSURE             'hr_abs'
               16  LOAD_CLOSURE             'hr_offset'
               18  LOAD_CLOSURE             'min_abs'
               20  LOAD_CLOSURE             'min_offset'
               22  LOAD_CLOSURE             'month_offset'
               24  LOAD_CLOSURE             'sec_offset'
               26  LOAD_CLOSURE             'time_str'
               28  LOAD_CLOSURE             'year_offset'
               30  BUILD_TUPLE_11       11 
               32  LOAD_CODE                <code_object date_found>
               34  LOAD_STR                 'extract_datetime_it.<locals>.date_found'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'date_found'

 L. 654        40  LOAD_FAST                'string'
               42  LOAD_STR                 ''
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     52  'to 52'
               48  LOAD_FAST                'dateNow'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            46  '46'

 L. 655        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 657        56  LOAD_CONST               False
               58  STORE_DEREF              'found'

 L. 658        60  LOAD_CONST               False
               62  STORE_FAST               'day_specified'

 L. 659        64  LOAD_CONST               False
               66  STORE_DEREF              'day_offset'

 L. 660        68  LOAD_CONST               0
               70  STORE_DEREF              'month_offset'

 L. 661        72  LOAD_CONST               0
               74  STORE_DEREF              'year_offset'

 L. 662        76  LOAD_FAST                'dateNow'
               78  LOAD_METHOD              strftime
               80  LOAD_STR                 '%w'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'today'

 L. 663        86  LOAD_FAST                'dateNow'
               88  LOAD_METHOD              strftime
               90  LOAD_STR                 '%Y'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  STORE_FAST               'current_year'

 L. 664        96  LOAD_CONST               False
               98  STORE_FAST               'from_flag'

 L. 665       100  LOAD_STR                 ''
              102  STORE_DEREF              'datestr'

 L. 666       104  LOAD_CONST               False
              106  STORE_FAST               'has_year'

 L. 667       108  LOAD_STR                 ''
              110  STORE_FAST               'time_qualifier'

 L. 668       112  LOAD_STR                 'mattina'
              114  LOAD_STR                 'stamani'
              116  LOAD_STR                 'stamane'
              118  BUILD_LIST_3          3 
              120  STORE_FAST               'time_qualifiers_am'

 L. 669       122  LOAD_STR                 'pomeriggio'
              124  LOAD_STR                 'sera'
              126  LOAD_STR                 'stasera'
              128  LOAD_STR                 'stanotte'
              130  BUILD_LIST_4          4 
              132  STORE_FAST               'time_qualifiers_pm'

 L. 670       134  LOAD_GLOBAL              set
              136  LOAD_FAST                'time_qualifiers_am'
              138  LOAD_FAST                'time_qualifiers_pm'
              140  BINARY_ADD       
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  STORE_FAST               'time_qualifiers_list'

 L. 671       146  LOAD_STR                 'alle'
              148  LOAD_STR                 'in'
              150  LOAD_STR                 'questo'
              152  LOAD_STR                 'per'
              154  LOAD_STR                 'di'
              156  LOAD_STR                 'tra'
              158  LOAD_STR                 'fra'
              160  LOAD_STR                 'entro'
              162  BUILD_LIST_8          8 
              164  STORE_FAST               'markers'

 L. 672       166  LOAD_STR                 'lunedi'
              168  LOAD_STR                 'martedi'
              170  LOAD_STR                 'mercoledi'

 L. 673       172  LOAD_STR                 'giovedi'
              174  LOAD_STR                 'venerdi'
              176  LOAD_STR                 'sabato'
              178  LOAD_STR                 'domenica'
              180  BUILD_LIST_7          7 
              182  STORE_FAST               'days'

 L. 674       184  LOAD_STR                 'gennaio'
              186  LOAD_STR                 'febbraio'
              188  LOAD_STR                 'marzo'
              190  LOAD_STR                 'aprile'
              192  LOAD_STR                 'maggio'
              194  LOAD_STR                 'giugno'

 L. 675       196  LOAD_STR                 'luglio'
              198  LOAD_STR                 'agosto'
              200  LOAD_STR                 'settembre'
              202  LOAD_STR                 'ottobre'
              204  LOAD_STR                 'novembre'

 L. 676       206  LOAD_STR                 'dicembre'
              208  BUILD_LIST_12        12 
              210  STORE_FAST               'months'

 L. 677       212  LOAD_STR                 'gen'
              214  LOAD_STR                 'feb'
              216  LOAD_STR                 'mar'
              218  LOAD_STR                 'apr'
              220  LOAD_STR                 'mag'
              222  LOAD_STR                 'giu'
              224  LOAD_STR                 'lug'
              226  LOAD_STR                 'ago'

 L. 678       228  LOAD_STR                 'set'
              230  LOAD_STR                 'ott'
              232  LOAD_STR                 'nov'
              234  LOAD_STR                 'dic'
              236  BUILD_LIST_12        12 
              238  STORE_FAST               'months_short'

 L. 679       240  LOAD_STR                 'decenni'
              242  LOAD_STR                 'secolo'
              244  LOAD_STR                 'millenni'
              246  BUILD_LIST_3          3 
              248  STORE_FAST               'year_multiples'

 L. 680       250  LOAD_STR                 'ora'
              252  LOAD_STR                 'minuto'
              254  LOAD_STR                 'secondo'
              256  BUILD_LIST_3          3 
              258  STORE_FAST               'time_multiples'

 L. 681       260  LOAD_STR                 'settimana'
              262  LOAD_STR                 'mese'
              264  LOAD_STR                 'anno'
              266  BUILD_LIST_3          3 
              268  STORE_FAST               'day_multiples'

 L. 682       270  LOAD_STR                 'tra'
              272  LOAD_STR                 'di'
              274  LOAD_STR                 'per'
              276  LOAD_STR                 'fra'
              278  LOAD_STR                 'un '
              280  LOAD_STR                 'uno'
              282  LOAD_STR                 'lo'
              284  LOAD_STR                 'del'

 L. 683       286  LOAD_STR                 'l'
              288  LOAD_STR                 'in_punto'
              290  LOAD_STR                 ' '
              292  LOAD_STR                 'nella'
              294  LOAD_STR                 'dell'
              296  BUILD_LIST_13        13 
              298  STORE_DEREF              'noise_words_2'

 L. 685       300  LOAD_FAST                'clean_string'
              302  LOAD_FAST                'string'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  STORE_FAST               'words'

 L. 687   308_310  SETUP_LOOP         2586  'to 2586'
              312  LOAD_GLOBAL              enumerate
              314  LOAD_FAST                'words'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  GET_ITER         
            320_0  COME_FROM          2442  '2442'
          320_322  FOR_ITER           2584  'to 2584'
              324  UNPACK_SEQUENCE_2     2 
              326  STORE_FAST               'idx'
              328  STORE_FAST               'word'

 L. 688       330  LOAD_FAST                'word'
              332  LOAD_STR                 ''
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   344  'to 344'

 L. 689   340_342  CONTINUE            320  'to 320'
            344_0  COME_FROM           336  '336'

 L. 690       344  LOAD_FAST                'idx'
              346  LOAD_CONST               1
              348  COMPARE_OP               >
          350_352  POP_JUMP_IF_FALSE   366  'to 366'
              354  LOAD_FAST                'words'
              356  LOAD_FAST                'idx'
              358  LOAD_CONST               2
              360  BINARY_SUBTRACT  
              362  BINARY_SUBSCR    
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           350  '350'
              366  LOAD_STR                 ''
            368_0  COME_FROM           364  '364'
              368  STORE_FAST               'word_prev_prev'

 L. 691       370  LOAD_FAST                'idx'
              372  LOAD_CONST               0
              374  COMPARE_OP               >
          376_378  POP_JUMP_IF_FALSE   392  'to 392'
              380  LOAD_FAST                'words'
              382  LOAD_FAST                'idx'
              384  LOAD_CONST               1
              386  BINARY_SUBTRACT  
              388  BINARY_SUBSCR    
              390  JUMP_FORWARD        394  'to 394'
            392_0  COME_FROM           376  '376'
              392  LOAD_STR                 ''
            394_0  COME_FROM           390  '390'
              394  STORE_FAST               'word_prev'

 L. 692       396  LOAD_FAST                'idx'
              398  LOAD_CONST               1
              400  BINARY_ADD       
              402  LOAD_GLOBAL              len
              404  LOAD_FAST                'words'
              406  CALL_FUNCTION_1       1  '1 positional argument'
              408  COMPARE_OP               <
          410_412  POP_JUMP_IF_FALSE   426  'to 426'
              414  LOAD_FAST                'words'
              416  LOAD_FAST                'idx'
              418  LOAD_CONST               1
              420  BINARY_ADD       
              422  BINARY_SUBSCR    
              424  JUMP_FORWARD        428  'to 428'
            426_0  COME_FROM           410  '410'
              426  LOAD_STR                 ''
            428_0  COME_FROM           424  '424'
              428  STORE_FAST               'word_next'

 L. 693       430  LOAD_FAST                'idx'
              432  LOAD_CONST               2
              434  BINARY_ADD       
              436  LOAD_GLOBAL              len
              438  LOAD_FAST                'words'
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  COMPARE_OP               <
          444_446  POP_JUMP_IF_FALSE   460  'to 460'
              448  LOAD_FAST                'words'
              450  LOAD_FAST                'idx'
              452  LOAD_CONST               2
              454  BINARY_ADD       
              456  BINARY_SUBSCR    
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           444  '444'
              460  LOAD_STR                 ''
            462_0  COME_FROM           458  '458'
              462  STORE_FAST               'word_next_next'

 L. 694       464  LOAD_FAST                'idx'
              466  STORE_FAST               'start'

 L. 695       468  LOAD_CONST               0
              470  STORE_FAST               'used'

 L. 697       472  LOAD_FAST                'word'
              474  LOAD_STR                 'adesso'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   546  'to 546'
              482  LOAD_DEREF               'datestr'
          484_486  POP_JUMP_IF_TRUE    546  'to 546'

 L. 699       488  LOAD_LISTCOMP            '<code_object <listcomp>>'
              490  LOAD_STR                 'extract_datetime_it.<locals>.<listcomp>'
              492  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              494  LOAD_FAST                'words'
              496  GET_ITER         
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  STORE_FAST               'words'

 L. 700       502  LOAD_LISTCOMP            '<code_object <listcomp>>'
              504  LOAD_STR                 'extract_datetime_it.<locals>.<listcomp>'
              506  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              508  LOAD_FAST                'words'
              510  GET_ITER         
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  STORE_FAST               'words'

 L. 701       516  LOAD_STR                 ' '
              518  LOAD_METHOD              join
              520  LOAD_FAST                'words'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  STORE_FAST               'result_str'

 L. 702       526  LOAD_FAST                'dateNow'
              528  LOAD_ATTR                replace
              530  LOAD_CONST               0
              532  LOAD_CONST               ('microsecond',)
              534  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              536  STORE_FAST               'extracted_date'

 L. 703       538  LOAD_FAST                'extracted_date'
              540  LOAD_FAST                'result_str'
              542  BUILD_LIST_2          2 
              544  RETURN_VALUE     
            546_0  COME_FROM           484  '484'
            546_1  COME_FROM           478  '478'

 L. 706       546  LOAD_GLOBAL              extractnumber_it
              548  LOAD_FAST                'word'
              550  CALL_FUNCTION_1       1  '1 positional argument'
          552_554  POP_JUMP_IF_FALSE   710  'to 710'
              556  LOAD_FAST                'word_next'
              558  LOAD_FAST                'year_multiples'
              560  COMPARE_OP               in
          562_564  POP_JUMP_IF_TRUE    576  'to 576'

 L. 707       566  LOAD_FAST                'word_next'
              568  LOAD_FAST                'day_multiples'
              570  COMPARE_OP               in
          572_574  POP_JUMP_IF_FALSE   710  'to 710'
            576_0  COME_FROM           562  '562'

 L. 708       576  LOAD_GLOBAL              int
              578  LOAD_GLOBAL              extractnumber_it
              580  LOAD_FAST                'word'
              582  CALL_FUNCTION_1       1  '1 positional argument'
              584  CALL_FUNCTION_1       1  '1 positional argument'
              586  STORE_FAST               'multiplier'

 L. 709       588  LOAD_FAST                'used'
              590  LOAD_CONST               2
              592  INPLACE_ADD      
              594  STORE_FAST               'used'

 L. 710       596  LOAD_FAST                'word_next'
              598  LOAD_STR                 'decenni'
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   616  'to 616'

 L. 711       606  LOAD_FAST                'multiplier'
              608  LOAD_CONST               10
              610  BINARY_MULTIPLY  
              612  STORE_DEREF              'year_offset'
              614  JUMP_FORWARD       2058  'to 2058'
            616_0  COME_FROM           602  '602'

 L. 712       616  LOAD_FAST                'word_next'
              618  LOAD_STR                 'secolo'
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   636  'to 636'

 L. 713       626  LOAD_FAST                'multiplier'
              628  LOAD_CONST               100
              630  BINARY_MULTIPLY  
              632  STORE_DEREF              'year_offset'
              634  JUMP_FORWARD       2058  'to 2058'
            636_0  COME_FROM           622  '622'

 L. 714       636  LOAD_FAST                'word_next'
              638  LOAD_STR                 'millenni'
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE   656  'to 656'

 L. 715       646  LOAD_FAST                'multiplier'
              648  LOAD_CONST               1000
              650  BINARY_MULTIPLY  
              652  STORE_DEREF              'year_offset'
              654  JUMP_FORWARD       2058  'to 2058'
            656_0  COME_FROM           642  '642'

 L. 716       656  LOAD_FAST                'word_next'
              658  LOAD_STR                 'anno'
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE   672  'to 672'

 L. 717       666  LOAD_FAST                'multiplier'
              668  STORE_DEREF              'year_offset'
              670  JUMP_FORWARD       2058  'to 2058'
            672_0  COME_FROM           662  '662'

 L. 718       672  LOAD_FAST                'word_next'
              674  LOAD_STR                 'mese'
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   688  'to 688'

 L. 719       682  LOAD_FAST                'multiplier'
              684  STORE_DEREF              'month_offset'
              686  JUMP_FORWARD       2058  'to 2058'
            688_0  COME_FROM           678  '678'

 L. 720       688  LOAD_FAST                'word_next'
              690  LOAD_STR                 'settimana'
              692  COMPARE_OP               ==
          694_696  POP_JUMP_IF_FALSE  2058  'to 2058'

 L. 721       698  LOAD_FAST                'multiplier'
              700  LOAD_CONST               7
              702  BINARY_MULTIPLY  
              704  STORE_DEREF              'day_offset'
          706_708  JUMP_FORWARD       2058  'to 2058'
            710_0  COME_FROM           572  '572'
            710_1  COME_FROM           552  '552'

 L. 722       710  LOAD_FAST                'word'
              712  LOAD_FAST                'time_qualifiers_list'
              714  COMPARE_OP               in
          716_718  POP_JUMP_IF_FALSE   728  'to 728'

 L. 723       720  LOAD_FAST                'word'
              722  STORE_FAST               'time_qualifier'
          724_726  JUMP_FORWARD       2058  'to 2058'
            728_0  COME_FROM           716  '716'

 L. 725       728  LOAD_FAST                'word'
              730  LOAD_STR                 'oggi'
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   760  'to 760'
              738  LOAD_FAST                'from_flag'
          740_742  POP_JUMP_IF_TRUE    760  'to 760'

 L. 726       744  LOAD_CONST               0
              746  STORE_DEREF              'day_offset'

 L. 727       748  LOAD_FAST                'used'
              750  LOAD_CONST               1
              752  INPLACE_ADD      
              754  STORE_FAST               'used'
          756_758  JUMP_FORWARD       2058  'to 2058'
            760_0  COME_FROM           740  '740'
            760_1  COME_FROM           734  '734'

 L. 728       760  LOAD_FAST                'word'
              762  LOAD_STR                 'domani'
              764  COMPARE_OP               ==
          766_768  POP_JUMP_IF_FALSE   792  'to 792'
              770  LOAD_FAST                'from_flag'
          772_774  POP_JUMP_IF_TRUE    792  'to 792'

 L. 729       776  LOAD_CONST               1
              778  STORE_DEREF              'day_offset'

 L. 730       780  LOAD_FAST                'used'
              782  LOAD_CONST               1
              784  INPLACE_ADD      
              786  STORE_FAST               'used'
          788_790  JUMP_FORWARD       2058  'to 2058'
            792_0  COME_FROM           772  '772'
            792_1  COME_FROM           766  '766'

 L. 731       792  LOAD_FAST                'word'
              794  LOAD_STR                 'ieri'
              796  COMPARE_OP               ==
          798_800  POP_JUMP_IF_FALSE   828  'to 828'
              802  LOAD_FAST                'from_flag'
          804_806  POP_JUMP_IF_TRUE    828  'to 828'

 L. 732       808  LOAD_DEREF               'day_offset'
              810  LOAD_CONST               1
              812  INPLACE_SUBTRACT 
              814  STORE_DEREF              'day_offset'

 L. 733       816  LOAD_FAST                'used'
              818  LOAD_CONST               1
              820  INPLACE_ADD      
              822  STORE_FAST               'used'
          824_826  JUMP_FORWARD       2058  'to 2058'
            828_0  COME_FROM           804  '804'
            828_1  COME_FROM           798  '798'

 L. 734       828  LOAD_FAST                'word'
              830  LOAD_STR                 'dopodomani'
              832  COMPARE_OP               ==
          834_836  POP_JUMP_IF_FALSE   864  'to 864'
              838  LOAD_FAST                'from_flag'
          840_842  POP_JUMP_IF_TRUE    864  'to 864'

 L. 735       844  LOAD_DEREF               'day_offset'
              846  LOAD_CONST               2
              848  INPLACE_ADD      
              850  STORE_DEREF              'day_offset'

 L. 736       852  LOAD_FAST                'used'
              854  LOAD_CONST               1
              856  INPLACE_ADD      
              858  STORE_FAST               'used'
          860_862  JUMP_FORWARD       2058  'to 2058'
            864_0  COME_FROM           840  '840'
            864_1  COME_FROM           834  '834'

 L. 737       864  LOAD_FAST                'word'
              866  LOAD_STR                 'dopo'
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   910  'to 910'
              874  LOAD_FAST                'word_next'
              876  LOAD_STR                 'domani'
              878  COMPARE_OP               ==
          880_882  POP_JUMP_IF_FALSE   910  'to 910'
              884  LOAD_FAST                'from_flag'
          886_888  POP_JUMP_IF_TRUE    910  'to 910'

 L. 738       890  LOAD_DEREF               'day_offset'
              892  LOAD_CONST               1
              894  INPLACE_ADD      
              896  STORE_DEREF              'day_offset'

 L. 739       898  LOAD_FAST                'used'
              900  LOAD_CONST               2
              902  INPLACE_ADD      
              904  STORE_FAST               'used'
          906_908  JUMP_FORWARD       2058  'to 2058'
            910_0  COME_FROM           886  '886'
            910_1  COME_FROM           880  '880'
            910_2  COME_FROM           870  '870'

 L. 740       910  LOAD_FAST                'word'
              912  LOAD_STR                 'giorno'
              914  COMPARE_OP               ==
          916_918  POP_JUMP_IF_FALSE   998  'to 998'

 L. 741       920  LOAD_FAST                'word_prev'
              922  LOAD_CONST               0
              924  BINARY_SUBSCR    
              926  LOAD_METHOD              isdigit
              928  CALL_METHOD_0         0  '0 positional arguments'
          930_932  POP_JUMP_IF_FALSE  2058  'to 2058'

 L. 742       934  LOAD_DEREF               'day_offset'
              936  LOAD_GLOBAL              int
              938  LOAD_FAST                'word_prev'
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  INPLACE_ADD      
              944  STORE_DEREF              'day_offset'

 L. 743       946  LOAD_FAST                'start'
              948  LOAD_CONST               1
              950  INPLACE_SUBTRACT 
              952  STORE_FAST               'start'

 L. 744       954  LOAD_CONST               2
              956  STORE_FAST               'used'

 L. 745       958  LOAD_FAST                'word_next'
              960  LOAD_STR                 'dopo'
              962  COMPARE_OP               ==
          964_966  POP_JUMP_IF_FALSE  2058  'to 2058'
              968  LOAD_FAST                'word_next_next'
              970  LOAD_STR                 'domani'
              972  COMPARE_OP               ==
          974_976  POP_JUMP_IF_FALSE  2058  'to 2058'

 L. 746       978  LOAD_DEREF               'day_offset'
              980  LOAD_CONST               1
              982  INPLACE_ADD      
              984  STORE_DEREF              'day_offset'

 L. 747       986  LOAD_FAST                'used'
              988  LOAD_CONST               2
              990  INPLACE_ADD      
              992  STORE_FAST               'used'
          994_996  JUMP_FORWARD       2058  'to 2058'
            998_0  COME_FROM           916  '916'

 L. 748       998  LOAD_FAST                'word'
             1000  LOAD_STR                 'settimana'
             1002  COMPARE_OP               ==
         1004_1006  POP_JUMP_IF_FALSE  1140  'to 1140'
             1008  LOAD_FAST                'from_flag'
         1010_1012  POP_JUMP_IF_TRUE   1140  'to 1140'

 L. 749      1014  LOAD_FAST                'word_prev'
             1016  LOAD_STR                 'prossimo'
             1018  COMPARE_OP               ==
         1020_1022  POP_JUMP_IF_FALSE  1042  'to 1042'

 L. 750      1024  LOAD_CONST               7
             1026  STORE_DEREF              'day_offset'

 L. 751      1028  LOAD_FAST                'start'
             1030  LOAD_CONST               1
             1032  INPLACE_SUBTRACT 
             1034  STORE_FAST               'start'

 L. 752      1036  LOAD_CONST               2
             1038  STORE_FAST               'used'
             1040  JUMP_FORWARD       2058  'to 2058'
           1042_0  COME_FROM          1020  '1020'

 L. 753      1042  LOAD_FAST                'word_prev'
             1044  LOAD_STR                 'passato'
             1046  COMPARE_OP               ==
         1048_1050  POP_JUMP_IF_TRUE   1062  'to 1062'
             1052  LOAD_FAST                'word_prev'
             1054  LOAD_STR                 'scorso'
             1056  COMPARE_OP               ==
         1058_1060  POP_JUMP_IF_FALSE  1080  'to 1080'
           1062_0  COME_FROM          1048  '1048'

 L. 754      1062  LOAD_CONST               -7
             1064  STORE_DEREF              'day_offset'

 L. 755      1066  LOAD_FAST                'start'
             1068  LOAD_CONST               1
             1070  INPLACE_SUBTRACT 
             1072  STORE_FAST               'start'

 L. 756      1074  LOAD_CONST               2
             1076  STORE_FAST               'used'
             1078  JUMP_FORWARD       2058  'to 2058'
           1080_0  COME_FROM          1058  '1058'

 L. 757      1080  LOAD_FAST                'word_next'
             1082  LOAD_STR                 'prossimo'
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1104  'to 1104'

 L. 758      1090  LOAD_CONST               7
             1092  STORE_DEREF              'day_offset'

 L. 759      1094  LOAD_FAST                'used'
             1096  LOAD_CONST               2
             1098  INPLACE_ADD      
             1100  STORE_FAST               'used'
             1102  JUMP_FORWARD       2058  'to 2058'
           1104_0  COME_FROM          1086  '1086'

 L. 760      1104  LOAD_FAST                'word_next'
             1106  LOAD_STR                 'passato'
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_TRUE   1124  'to 1124'
             1114  LOAD_FAST                'word_next'
             1116  LOAD_STR                 'scorso'
             1118  COMPARE_OP               ==
         1120_1122  POP_JUMP_IF_FALSE  2058  'to 2058'
           1124_0  COME_FROM          1110  '1110'

 L. 761      1124  LOAD_CONST               -7
             1126  STORE_DEREF              'day_offset'

 L. 762      1128  LOAD_FAST                'used'
             1130  LOAD_CONST               2
             1132  INPLACE_ADD      
             1134  STORE_FAST               'used'
         1136_1138  JUMP_FORWARD       2058  'to 2058'
           1140_0  COME_FROM          1010  '1010'
           1140_1  COME_FROM          1004  '1004'

 L. 764      1140  LOAD_FAST                'word'
             1142  LOAD_STR                 'mese'
             1144  COMPARE_OP               ==
         1146_1148  POP_JUMP_IF_FALSE  1282  'to 1282'
             1150  LOAD_FAST                'from_flag'
         1152_1154  POP_JUMP_IF_TRUE   1282  'to 1282'

 L. 765      1156  LOAD_FAST                'word_prev'
             1158  LOAD_STR                 'prossimo'
             1160  COMPARE_OP               ==
         1162_1164  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 766      1166  LOAD_CONST               1
             1168  STORE_DEREF              'month_offset'

 L. 767      1170  LOAD_FAST                'start'
             1172  LOAD_CONST               1
             1174  INPLACE_SUBTRACT 
             1176  STORE_FAST               'start'

 L. 768      1178  LOAD_CONST               2
             1180  STORE_FAST               'used'
             1182  JUMP_FORWARD       2058  'to 2058'
           1184_0  COME_FROM          1162  '1162'

 L. 769      1184  LOAD_FAST                'word_prev'
             1186  LOAD_STR                 'passato'
             1188  COMPARE_OP               ==
         1190_1192  POP_JUMP_IF_TRUE   1204  'to 1204'
             1194  LOAD_FAST                'word_prev'
             1196  LOAD_STR                 'scorso'
             1198  COMPARE_OP               ==
         1200_1202  POP_JUMP_IF_FALSE  1222  'to 1222'
           1204_0  COME_FROM          1190  '1190'

 L. 770      1204  LOAD_CONST               -1
             1206  STORE_DEREF              'month_offset'

 L. 771      1208  LOAD_FAST                'start'
             1210  LOAD_CONST               1
             1212  INPLACE_SUBTRACT 
             1214  STORE_FAST               'start'

 L. 772      1216  LOAD_CONST               2
             1218  STORE_FAST               'used'
             1220  JUMP_FORWARD       2058  'to 2058'
           1222_0  COME_FROM          1200  '1200'

 L. 773      1222  LOAD_FAST                'word_next'
             1224  LOAD_STR                 'prossimo'
             1226  COMPARE_OP               ==
         1228_1230  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 774      1232  LOAD_CONST               1
             1234  STORE_DEREF              'month_offset'

 L. 775      1236  LOAD_FAST                'used'
             1238  LOAD_CONST               2
             1240  INPLACE_ADD      
             1242  STORE_FAST               'used'
             1244  JUMP_FORWARD       2058  'to 2058'
           1246_0  COME_FROM          1228  '1228'

 L. 776      1246  LOAD_FAST                'word_next'
             1248  LOAD_STR                 'passato'
             1250  COMPARE_OP               ==
         1252_1254  POP_JUMP_IF_TRUE   1266  'to 1266'
             1256  LOAD_FAST                'word_next'
             1258  LOAD_STR                 'scorso'
             1260  COMPARE_OP               ==
         1262_1264  POP_JUMP_IF_FALSE  2058  'to 2058'
           1266_0  COME_FROM          1252  '1252'

 L. 777      1266  LOAD_CONST               -1
             1268  STORE_DEREF              'month_offset'

 L. 778      1270  LOAD_FAST                'used'
             1272  LOAD_CONST               2
             1274  INPLACE_ADD      
             1276  STORE_FAST               'used'
         1278_1280  JUMP_FORWARD       2058  'to 2058'
           1282_0  COME_FROM          1152  '1152'
           1282_1  COME_FROM          1146  '1146'

 L. 780      1282  LOAD_FAST                'word'
             1284  LOAD_STR                 'anno'
             1286  COMPARE_OP               ==
         1288_1290  POP_JUMP_IF_FALSE  1416  'to 1416'
             1292  LOAD_FAST                'from_flag'
         1294_1296  POP_JUMP_IF_TRUE   1416  'to 1416'

 L. 781      1298  LOAD_FAST                'word_prev'
             1300  LOAD_STR                 'prossimo'
             1302  COMPARE_OP               ==
         1304_1306  POP_JUMP_IF_FALSE  1326  'to 1326'

 L. 782      1308  LOAD_CONST               1
             1310  STORE_DEREF              'year_offset'

 L. 783      1312  LOAD_FAST                'start'
             1314  LOAD_CONST               1
             1316  INPLACE_SUBTRACT 
             1318  STORE_FAST               'start'

 L. 784      1320  LOAD_CONST               2
             1322  STORE_FAST               'used'
             1324  JUMP_FORWARD       2058  'to 2058'
           1326_0  COME_FROM          1304  '1304'

 L. 785      1326  LOAD_FAST                'word_next'
             1328  LOAD_STR                 'prossimo'
             1330  COMPARE_OP               ==
         1332_1334  POP_JUMP_IF_FALSE  1346  'to 1346'

 L. 786      1336  LOAD_CONST               1
             1338  STORE_DEREF              'year_offset'

 L. 787      1340  LOAD_CONST               2
             1342  STORE_FAST               'used'
             1344  JUMP_FORWARD       2058  'to 2058'
           1346_0  COME_FROM          1332  '1332'

 L. 788      1346  LOAD_FAST                'word_prev'
             1348  LOAD_STR                 'passato'
             1350  COMPARE_OP               ==
         1352_1354  POP_JUMP_IF_TRUE   1366  'to 1366'
             1356  LOAD_FAST                'word_prev'
             1358  LOAD_STR                 'scorso'
             1360  COMPARE_OP               ==
         1362_1364  POP_JUMP_IF_FALSE  1384  'to 1384'
           1366_0  COME_FROM          1352  '1352'

 L. 789      1366  LOAD_CONST               -1
             1368  STORE_DEREF              'year_offset'

 L. 790      1370  LOAD_FAST                'start'
             1372  LOAD_CONST               1
             1374  INPLACE_SUBTRACT 
             1376  STORE_FAST               'start'

 L. 791      1378  LOAD_CONST               2
             1380  STORE_FAST               'used'
             1382  JUMP_FORWARD       2058  'to 2058'
           1384_0  COME_FROM          1362  '1362'

 L. 792      1384  LOAD_FAST                'word_next'
             1386  LOAD_STR                 'passato'
             1388  COMPARE_OP               ==
         1390_1392  POP_JUMP_IF_TRUE   1404  'to 1404'
             1394  LOAD_FAST                'word_next'
             1396  LOAD_STR                 'scorso'
             1398  COMPARE_OP               ==
         1400_1402  POP_JUMP_IF_FALSE  2058  'to 2058'
           1404_0  COME_FROM          1390  '1390'

 L. 793      1404  LOAD_CONST               -1
             1406  STORE_DEREF              'year_offset'

 L. 794      1408  LOAD_CONST               2
             1410  STORE_FAST               'used'
         1412_1414  JUMP_FORWARD       2058  'to 2058'
           1416_0  COME_FROM          1294  '1294'
           1416_1  COME_FROM          1288  '1288'

 L. 795      1416  LOAD_FAST                'word'
             1418  LOAD_STR                 'decenni'
             1420  COMPARE_OP               ==
         1422_1424  POP_JUMP_IF_FALSE  1550  'to 1550'
             1426  LOAD_FAST                'from_flag'
         1428_1430  POP_JUMP_IF_TRUE   1550  'to 1550'

 L. 796      1432  LOAD_FAST                'word_prev'
             1434  LOAD_STR                 'prossimo'
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1460  'to 1460'

 L. 797      1442  LOAD_CONST               10
             1444  STORE_DEREF              'year_offset'

 L. 798      1446  LOAD_FAST                'start'
             1448  LOAD_CONST               1
             1450  INPLACE_SUBTRACT 
             1452  STORE_FAST               'start'

 L. 799      1454  LOAD_CONST               2
             1456  STORE_FAST               'used'
             1458  JUMP_FORWARD       2058  'to 2058'
           1460_0  COME_FROM          1438  '1438'

 L. 800      1460  LOAD_FAST                'word_next'
             1462  LOAD_STR                 'prossimo'
             1464  COMPARE_OP               ==
         1466_1468  POP_JUMP_IF_FALSE  1480  'to 1480'

 L. 801      1470  LOAD_CONST               10
             1472  STORE_DEREF              'year_offset'

 L. 802      1474  LOAD_CONST               2
             1476  STORE_FAST               'used'
             1478  JUMP_FORWARD       2058  'to 2058'
           1480_0  COME_FROM          1466  '1466'

 L. 803      1480  LOAD_FAST                'word_prev'
             1482  LOAD_STR                 'passato'
             1484  COMPARE_OP               ==
         1486_1488  POP_JUMP_IF_TRUE   1500  'to 1500'
             1490  LOAD_FAST                'word_prev'
             1492  LOAD_STR                 'scorso'
             1494  COMPARE_OP               ==
         1496_1498  POP_JUMP_IF_FALSE  1518  'to 1518'
           1500_0  COME_FROM          1486  '1486'

 L. 804      1500  LOAD_CONST               -10
             1502  STORE_DEREF              'year_offset'

 L. 805      1504  LOAD_FAST                'start'
             1506  LOAD_CONST               1
             1508  INPLACE_SUBTRACT 
             1510  STORE_FAST               'start'

 L. 806      1512  LOAD_CONST               2
             1514  STORE_FAST               'used'
             1516  JUMP_FORWARD       2058  'to 2058'
           1518_0  COME_FROM          1496  '1496'

 L. 807      1518  LOAD_FAST                'word_next'
             1520  LOAD_STR                 'passato'
             1522  COMPARE_OP               ==
         1524_1526  POP_JUMP_IF_TRUE   1538  'to 1538'
             1528  LOAD_FAST                'word_next'
             1530  LOAD_STR                 'scorso'
             1532  COMPARE_OP               ==
         1534_1536  POP_JUMP_IF_FALSE  2058  'to 2058'
           1538_0  COME_FROM          1524  '1524'

 L. 808      1538  LOAD_CONST               -10
             1540  STORE_DEREF              'year_offset'

 L. 809      1542  LOAD_CONST               2
             1544  STORE_FAST               'used'
         1546_1548  JUMP_FORWARD       2058  'to 2058'
           1550_0  COME_FROM          1428  '1428'
           1550_1  COME_FROM          1422  '1422'

 L. 812      1550  LOAD_FAST                'word'
             1552  LOAD_FAST                'days'
             1554  COMPARE_OP               in
         1556_1558  POP_JUMP_IF_FALSE  1762  'to 1762'
             1560  LOAD_FAST                'from_flag'
         1562_1564  POP_JUMP_IF_TRUE   1762  'to 1762'

 L. 813      1566  LOAD_FAST                'days'
             1568  LOAD_METHOD              index
             1570  LOAD_FAST                'word'
             1572  CALL_METHOD_1         1  '1 positional argument'
             1574  STORE_FAST               'ddd'

 L. 814      1576  LOAD_FAST                'ddd'
             1578  LOAD_CONST               1
             1580  BINARY_ADD       
             1582  LOAD_GLOBAL              int
             1584  LOAD_FAST                'today'
             1586  CALL_FUNCTION_1       1  '1 positional argument'
             1588  BINARY_SUBTRACT  
             1590  STORE_DEREF              'day_offset'

 L. 815      1592  LOAD_CONST               1
             1594  STORE_FAST               'used'

 L. 816      1596  LOAD_DEREF               'day_offset'
             1598  LOAD_CONST               0
             1600  COMPARE_OP               <
         1602_1604  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 817      1606  LOAD_DEREF               'day_offset'
             1608  LOAD_CONST               7
             1610  INPLACE_ADD      
             1612  STORE_DEREF              'day_offset'
           1614_0  COME_FROM          1602  '1602'

 L. 818      1614  LOAD_FAST                'word_prev'
             1616  LOAD_STR                 'prossimo'
             1618  COMPARE_OP               ==
         1620_1622  POP_JUMP_IF_FALSE  1650  'to 1650'

 L. 819      1624  LOAD_DEREF               'day_offset'
             1626  LOAD_CONST               7
             1628  INPLACE_ADD      
             1630  STORE_DEREF              'day_offset'

 L. 820      1632  LOAD_FAST                'start'
             1634  LOAD_CONST               1
             1636  INPLACE_SUBTRACT 
             1638  STORE_FAST               'start'

 L. 821      1640  LOAD_FAST                'used'
             1642  LOAD_CONST               1
             1644  INPLACE_ADD      
             1646  STORE_FAST               'used'
             1648  JUMP_FORWARD       1694  'to 1694'
           1650_0  COME_FROM          1620  '1620'

 L. 822      1650  LOAD_FAST                'word_prev'
             1652  LOAD_STR                 'passato'
             1654  COMPARE_OP               ==
         1656_1658  POP_JUMP_IF_TRUE   1670  'to 1670'
             1660  LOAD_FAST                'word_prev'
             1662  LOAD_STR                 'scorso'
             1664  COMPARE_OP               ==
         1666_1668  POP_JUMP_IF_FALSE  1694  'to 1694'
           1670_0  COME_FROM          1656  '1656'

 L. 823      1670  LOAD_DEREF               'day_offset'
             1672  LOAD_CONST               7
             1674  INPLACE_SUBTRACT 
             1676  STORE_DEREF              'day_offset'

 L. 824      1678  LOAD_FAST                'start'
             1680  LOAD_CONST               1
             1682  INPLACE_SUBTRACT 
             1684  STORE_FAST               'start'

 L. 825      1686  LOAD_FAST                'used'
             1688  LOAD_CONST               1
             1690  INPLACE_ADD      
             1692  STORE_FAST               'used'
           1694_0  COME_FROM          1666  '1666'
           1694_1  COME_FROM          1648  '1648'

 L. 826      1694  LOAD_FAST                'word_next'
             1696  LOAD_STR                 'prossimo'
             1698  COMPARE_OP               ==
         1700_1702  POP_JUMP_IF_FALSE  1722  'to 1722'

 L. 827      1704  LOAD_DEREF               'day_offset'
             1706  LOAD_CONST               7
             1708  INPLACE_ADD      
             1710  STORE_DEREF              'day_offset'

 L. 828      1712  LOAD_FAST                'used'
             1714  LOAD_CONST               1
             1716  INPLACE_ADD      
             1718  STORE_FAST               'used'
             1720  JUMP_FORWARD       2058  'to 2058'
           1722_0  COME_FROM          1700  '1700'

 L. 829      1722  LOAD_FAST                'word_next'
             1724  LOAD_STR                 'passato'
             1726  COMPARE_OP               ==
         1728_1730  POP_JUMP_IF_TRUE   1742  'to 1742'
             1732  LOAD_FAST                'word_next'
             1734  LOAD_STR                 'scorso'
             1736  COMPARE_OP               ==
         1738_1740  POP_JUMP_IF_FALSE  2058  'to 2058'
           1742_0  COME_FROM          1728  '1728'

 L. 830      1742  LOAD_DEREF               'day_offset'
             1744  LOAD_CONST               7
             1746  INPLACE_SUBTRACT 
             1748  STORE_DEREF              'day_offset'

 L. 831      1750  LOAD_FAST                'used'
             1752  LOAD_CONST               1
             1754  INPLACE_ADD      
             1756  STORE_FAST               'used'
         1758_1760  JUMP_FORWARD       2058  'to 2058'
           1762_0  COME_FROM          1562  '1562'
           1762_1  COME_FROM          1556  '1556'

 L. 833      1762  LOAD_FAST                'word'
             1764  LOAD_FAST                'months'
             1766  COMPARE_OP               in
         1768_1770  POP_JUMP_IF_TRUE   1788  'to 1788'
             1772  LOAD_FAST                'word'
             1774  LOAD_FAST                'months_short'
             1776  COMPARE_OP               in
         1778_1780  POP_JUMP_IF_FALSE  2058  'to 2058'
             1782  LOAD_FAST                'from_flag'
         1784_1786  POP_JUMP_IF_TRUE   2058  'to 2058'
           1788_0  COME_FROM          1768  '1768'

 L. 834      1788  SETUP_EXCEPT       1804  'to 1804'

 L. 835      1790  LOAD_FAST                'months'
             1792  LOAD_METHOD              index
             1794  LOAD_FAST                'word'
             1796  CALL_METHOD_1         1  '1 positional argument'
             1798  STORE_FAST               'mmm'
             1800  POP_BLOCK        
             1802  JUMP_FORWARD       1836  'to 1836'
           1804_0  COME_FROM_EXCEPT   1788  '1788'

 L. 836      1804  DUP_TOP          
             1806  LOAD_GLOBAL              ValueError
             1808  COMPARE_OP               exception-match
         1810_1812  POP_JUMP_IF_FALSE  1834  'to 1834'
             1814  POP_TOP          
             1816  POP_TOP          
             1818  POP_TOP          

 L. 837      1820  LOAD_FAST                'months_short'
             1822  LOAD_METHOD              index
             1824  LOAD_FAST                'word'
             1826  CALL_METHOD_1         1  '1 positional argument'
             1828  STORE_FAST               'mmm'
             1830  POP_EXCEPT       
             1832  JUMP_FORWARD       1836  'to 1836'
           1834_0  COME_FROM          1810  '1810'
             1834  END_FINALLY      
           1836_0  COME_FROM          1832  '1832'
           1836_1  COME_FROM          1802  '1802'

 L. 838      1836  LOAD_FAST                'used'
             1838  LOAD_CONST               1
             1840  INPLACE_ADD      
             1842  STORE_FAST               'used'

 L. 839      1844  LOAD_FAST                'months'
             1846  LOAD_FAST                'mmm'
             1848  BINARY_SUBSCR    
             1850  STORE_DEREF              'datestr'

 L. 840      1852  LOAD_FAST                'word_prev'
         1854_1856  POP_JUMP_IF_FALSE  1968  'to 1968'
             1858  LOAD_GLOBAL              extractnumber_it
             1860  LOAD_FAST                'word_prev'
             1862  CALL_FUNCTION_1       1  '1 positional argument'
         1864_1866  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 841      1868  LOAD_DEREF               'datestr'
             1870  LOAD_STR                 ' '
             1872  LOAD_GLOBAL              str
             1874  LOAD_GLOBAL              int
             1876  LOAD_GLOBAL              extractnumber_it
             1878  LOAD_FAST                'word_prev'
             1880  CALL_FUNCTION_1       1  '1 positional argument'
             1882  CALL_FUNCTION_1       1  '1 positional argument'
             1884  CALL_FUNCTION_1       1  '1 positional argument'
             1886  BINARY_ADD       
             1888  INPLACE_ADD      
             1890  STORE_DEREF              'datestr'

 L. 842      1892  LOAD_FAST                'start'
             1894  LOAD_CONST               1
             1896  INPLACE_SUBTRACT 
             1898  STORE_FAST               'start'

 L. 843      1900  LOAD_FAST                'used'
             1902  LOAD_CONST               1
             1904  INPLACE_ADD      
             1906  STORE_FAST               'used'

 L. 844      1908  LOAD_FAST                'word_next'
         1910_1912  POP_JUMP_IF_FALSE  1962  'to 1962'
             1914  LOAD_GLOBAL              extractnumber_it
             1916  LOAD_FAST                'word_next'
             1918  CALL_FUNCTION_1       1  '1 positional argument'
         1920_1922  POP_JUMP_IF_FALSE  1962  'to 1962'

 L. 845      1924  LOAD_DEREF               'datestr'
             1926  LOAD_STR                 ' '
             1928  LOAD_GLOBAL              str
             1930  LOAD_GLOBAL              int
             1932  LOAD_GLOBAL              extractnumber_it
             1934  LOAD_FAST                'word_next'
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  CALL_FUNCTION_1       1  '1 positional argument'
             1940  CALL_FUNCTION_1       1  '1 positional argument'
             1942  BINARY_ADD       
             1944  INPLACE_ADD      
             1946  STORE_DEREF              'datestr'

 L. 846      1948  LOAD_FAST                'used'
             1950  LOAD_CONST               1
             1952  INPLACE_ADD      
             1954  STORE_FAST               'used'

 L. 847      1956  LOAD_CONST               True
             1958  STORE_FAST               'has_year'
           1960_0  COME_FROM          1182  '1182'
           1960_1  COME_FROM          1040  '1040'
             1960  JUMP_FORWARD       1966  'to 1966'
           1962_0  COME_FROM          1920  '1920'
           1962_1  COME_FROM          1910  '1910'

 L. 849      1962  LOAD_CONST               False
           1964_0  COME_FROM           614  '614'
             1964  STORE_FAST               'has_year'
           1966_0  COME_FROM          1960  '1960'
             1966  JUMP_FORWARD       2058  'to 2058'
           1968_0  COME_FROM          1864  '1864'
           1968_1  COME_FROM          1854  '1854'
           1968_2  COME_FROM          1458  '1458'
           1968_3  COME_FROM          1324  '1324'

 L. 850      1968  LOAD_FAST                'word_next'
         1970_1972  POP_JUMP_IF_FALSE  2058  'to 2058'
             1974  LOAD_FAST                'word_next'
             1976  LOAD_CONST               0
             1978  BINARY_SUBSCR    
             1980  LOAD_METHOD              isdigit
             1982  CALL_METHOD_0         0  '0 positional arguments'
           1984_0  COME_FROM           634  '634'
         1984_1986  POP_JUMP_IF_FALSE  2058  'to 2058'
           1988_0  COME_FROM          1478  '1478'
           1988_1  COME_FROM          1344  '1344'

 L. 851      1988  LOAD_DEREF               'datestr'
             1990  LOAD_STR                 ' '
             1992  LOAD_FAST                'word_next'
             1994  BINARY_ADD       
             1996  INPLACE_ADD      
           1998_0  COME_FROM          1220  '1220'
           1998_1  COME_FROM          1078  '1078'
             1998  STORE_DEREF              'datestr'

 L. 852      2000  LOAD_FAST                'used'
             2002  LOAD_CONST               1
           2004_0  COME_FROM           654  '654'
             2004  INPLACE_ADD      
             2006  STORE_FAST               'used'

 L. 853      2008  LOAD_FAST                'word_next_next'
         2010_2012  POP_JUMP_IF_FALSE  2054  'to 2054'
             2014  LOAD_FAST                'word_next_next'
             2016  LOAD_CONST               0
           2018_0  COME_FROM          1720  '1720'
             2018  BINARY_SUBSCR    
           2020_0  COME_FROM           670  '670'
             2020  LOAD_METHOD              isdigit
           2022_0  COME_FROM          1244  '1244'
           2022_1  COME_FROM          1102  '1102'
             2022  CALL_METHOD_0         0  '0 positional arguments'
         2024_2026  POP_JUMP_IF_FALSE  2054  'to 2054'

 L. 854      2028  LOAD_DEREF               'datestr'
             2030  LOAD_STR                 ' '
             2032  LOAD_FAST                'word_next_next'
             2034  BINARY_ADD       
           2036_0  COME_FROM           686  '686'
             2036  INPLACE_ADD      
             2038  STORE_DEREF              'datestr'

 L. 855      2040  LOAD_FAST                'used'
             2042  LOAD_CONST               1
             2044  INPLACE_ADD      
             2046  STORE_FAST               'used'

 L. 856      2048  LOAD_CONST               True
             2050  STORE_FAST               'has_year'
             2052  JUMP_FORWARD       2058  'to 2058'
           2054_0  COME_FROM          2024  '2024'
           2054_1  COME_FROM          2010  '2010'

 L. 858      2054  LOAD_CONST               False
             2056  STORE_FAST               'has_year'
           2058_0  COME_FROM          2052  '2052'
           2058_1  COME_FROM          1984  '1984'
           2058_2  COME_FROM          1970  '1970'
           2058_3  COME_FROM          1966  '1966'
           2058_4  COME_FROM          1784  '1784'
           2058_5  COME_FROM          1778  '1778'
           2058_6  COME_FROM          1758  '1758'
           2058_7  COME_FROM          1738  '1738'
           2058_8  COME_FROM          1546  '1546'
           2058_9  COME_FROM          1534  '1534'
          2058_10  COME_FROM          1412  '1412'
          2058_11  COME_FROM          1400  '1400'
          2058_12  COME_FROM          1278  '1278'
          2058_13  COME_FROM          1262  '1262'
          2058_14  COME_FROM          1136  '1136'
          2058_15  COME_FROM          1120  '1120'
          2058_16  COME_FROM           994  '994'
          2058_17  COME_FROM           974  '974'
          2058_18  COME_FROM           964  '964'
          2058_19  COME_FROM           930  '930'
          2058_20  COME_FROM           906  '906'
          2058_21  COME_FROM           860  '860'
          2058_22  COME_FROM           824  '824'
          2058_23  COME_FROM           788  '788'
          2058_24  COME_FROM           756  '756'
          2058_25  COME_FROM           724  '724'
          2058_26  COME_FROM           706  '706'
          2058_27  COME_FROM           694  '694'

 L. 861      2058  LOAD_FAST                'days'
             2060  LOAD_FAST                'months'
             2062  BINARY_ADD       
             2064  LOAD_FAST                'months_short'
             2066  BINARY_ADD       
             2068  STORE_FAST               'validFollowups'

 L. 862      2070  LOAD_FAST                'validFollowups'
             2072  LOAD_METHOD              append
             2074  LOAD_STR                 'oggi'
             2076  CALL_METHOD_1         1  '1 positional argument'
             2078  POP_TOP          

 L. 863      2080  LOAD_FAST                'validFollowups'
             2082  LOAD_METHOD              append
             2084  LOAD_STR                 'domani'
             2086  CALL_METHOD_1         1  '1 positional argument'
             2088  POP_TOP          

 L. 864      2090  LOAD_FAST                'validFollowups'
             2092  LOAD_METHOD              append
             2094  LOAD_STR                 'prossimo'
             2096  CALL_METHOD_1         1  '1 positional argument'
             2098  POP_TOP          

 L. 865      2100  LOAD_FAST                'validFollowups'
             2102  LOAD_METHOD              append
             2104  LOAD_STR                 'passato'
             2106  CALL_METHOD_1         1  '1 positional argument'
             2108  POP_TOP          

 L. 866      2110  LOAD_FAST                'validFollowups'
             2112  LOAD_METHOD              append
             2114  LOAD_STR                 'adesso'
             2116  CALL_METHOD_1         1  '1 positional argument'
             2118  POP_TOP          

 L. 868      2120  LOAD_FAST                'word'
             2122  LOAD_STR                 'da'
             2124  COMPARE_OP               ==
         2126_2128  POP_JUMP_IF_TRUE   2140  'to 2140'
             2130  LOAD_FAST                'word'
             2132  LOAD_STR                 'dopo'
             2134  COMPARE_OP               ==
         2136_2138  POP_JUMP_IF_FALSE  2436  'to 2436'
           2140_0  COME_FROM          2126  '2126'
             2140  LOAD_FAST                'word_next'
             2142  LOAD_FAST                'validFollowups'
             2144  COMPARE_OP               in
         2146_2148  POP_JUMP_IF_FALSE  2436  'to 2436'

 L. 869      2150  LOAD_CONST               0
             2152  STORE_FAST               'used'

 L. 870      2154  LOAD_CONST               True
             2156  STORE_FAST               'from_flag'

 L. 871      2158  LOAD_FAST                'word_next'
             2160  LOAD_STR                 'domani'
             2162  COMPARE_OP               ==
         2164_2166  POP_JUMP_IF_FALSE  2186  'to 2186'

 L. 872      2168  LOAD_DEREF               'day_offset'
             2170  LOAD_CONST               1
             2172  INPLACE_ADD      
             2174  STORE_DEREF              'day_offset'

 L. 873      2176  LOAD_FAST                'used'
             2178  LOAD_CONST               2
             2180  INPLACE_ADD      
             2182  STORE_FAST               'used'
             2184  JUMP_FORWARD       2436  'to 2436'
           2186_0  COME_FROM          2164  '2164'

 L. 874      2186  LOAD_FAST                'word_next'
             2188  LOAD_STR                 'oggi'
             2190  COMPARE_OP               ==
         2192_2194  POP_JUMP_IF_TRUE   2206  'to 2206'
             2196  LOAD_FAST                'word_next'
             2198  LOAD_STR                 'adesso'
             2200  COMPARE_OP               ==
         2202_2204  POP_JUMP_IF_FALSE  2216  'to 2216'
           2206_0  COME_FROM          2192  '2192'

 L. 875      2206  LOAD_FAST                'used'
             2208  LOAD_CONST               2
             2210  INPLACE_ADD      
             2212  STORE_FAST               'used'
             2214  JUMP_FORWARD       2436  'to 2436'
           2216_0  COME_FROM          2202  '2202'

 L. 876      2216  LOAD_FAST                'word_next'
             2218  LOAD_FAST                'days'
             2220  COMPARE_OP               in
         2222_2224  POP_JUMP_IF_FALSE  2360  'to 2360'

 L. 877      2226  LOAD_FAST                'days'
             2228  LOAD_METHOD              index
             2230  LOAD_FAST                'word_next'
             2232  CALL_METHOD_1         1  '1 positional argument'
             2234  STORE_FAST               'ddd'

 L. 878      2236  LOAD_FAST                'ddd'
             2238  LOAD_CONST               1
             2240  BINARY_ADD       
             2242  LOAD_GLOBAL              int
             2244  LOAD_FAST                'today'
             2246  CALL_FUNCTION_1       1  '1 positional argument'
             2248  BINARY_SUBTRACT  
             2250  STORE_FAST               'tmp_offset'

 L. 879      2252  LOAD_FAST                'used'
             2254  LOAD_CONST               2
             2256  INPLACE_ADD      
             2258  STORE_FAST               'used'

 L. 880      2260  LOAD_FAST                'tmp_offset'
             2262  LOAD_CONST               0
             2264  COMPARE_OP               <
         2266_2268  POP_JUMP_IF_FALSE  2278  'to 2278'

 L. 881      2270  LOAD_FAST                'tmp_offset'
             2272  LOAD_CONST               7
             2274  INPLACE_ADD      
             2276  STORE_FAST               'tmp_offset'
           2278_0  COME_FROM          2266  '2266'

 L. 882      2278  LOAD_FAST                'word_next_next'
             2280  LOAD_STR                 'prossimo'
             2282  COMPARE_OP               ==
         2284_2286  POP_JUMP_IF_FALSE  2306  'to 2306'

 L. 883      2288  LOAD_FAST                'tmp_offset'
             2290  LOAD_CONST               7
             2292  INPLACE_ADD      
             2294  STORE_FAST               'tmp_offset'

 L. 884      2296  LOAD_FAST                'used'
             2298  LOAD_CONST               1
             2300  INPLACE_ADD      
             2302  STORE_FAST               'used'
             2304  JUMP_FORWARD       2350  'to 2350'
           2306_0  COME_FROM          2284  '2284'

 L. 885      2306  LOAD_FAST                'word_next_next'
             2308  LOAD_STR                 'passato'
             2310  COMPARE_OP               ==
         2312_2314  POP_JUMP_IF_TRUE   2326  'to 2326'
             2316  LOAD_FAST                'word_next_next'
             2318  LOAD_STR                 'scorso'
             2320  COMPARE_OP               ==
         2322_2324  POP_JUMP_IF_FALSE  2350  'to 2350'
           2326_0  COME_FROM          2312  '2312'

 L. 886      2326  LOAD_FAST                'ddd'
             2328  LOAD_CONST               1
             2330  BINARY_ADD       
             2332  LOAD_GLOBAL              int
             2334  LOAD_FAST                'today'
             2336  CALL_FUNCTION_1       1  '1 positional argument'
             2338  BINARY_SUBTRACT  
             2340  STORE_FAST               'tmp_offset'

 L. 887      2342  LOAD_FAST                'used'
             2344  LOAD_CONST               1
             2346  INPLACE_ADD      
             2348  STORE_FAST               'used'
           2350_0  COME_FROM          2322  '2322'
           2350_1  COME_FROM          2304  '2304'

 L. 888      2350  LOAD_DEREF               'day_offset'
             2352  LOAD_FAST                'tmp_offset'
             2354  INPLACE_ADD      
             2356  STORE_DEREF              'day_offset'
             2358  JUMP_FORWARD       2436  'to 2436'
           2360_0  COME_FROM          2222  '2222'

 L. 889      2360  LOAD_FAST                'word_next_next'
         2362_2364  POP_JUMP_IF_FALSE  2436  'to 2436'
             2366  LOAD_FAST                'word_next_next'
             2368  LOAD_FAST                'days'
             2370  COMPARE_OP               in
         2372_2374  POP_JUMP_IF_FALSE  2436  'to 2436'

 L. 890      2376  LOAD_FAST                'days'
             2378  LOAD_METHOD              index
             2380  LOAD_FAST                'word_next_next'
             2382  CALL_METHOD_1         1  '1 positional argument'
             2384  STORE_FAST               'ddd'

 L. 891      2386  LOAD_FAST                'ddd'
             2388  LOAD_CONST               1
             2390  BINARY_ADD       
             2392  LOAD_GLOBAL              int
             2394  LOAD_FAST                'today'
             2396  CALL_FUNCTION_1       1  '1 positional argument'
             2398  BINARY_SUBTRACT  
             2400  STORE_FAST               'tmp_offset'

 L. 892      2402  LOAD_FAST                'word_next'
             2404  LOAD_STR                 'prossimo'
             2406  COMPARE_OP               ==
         2408_2410  POP_JUMP_IF_FALSE  2420  'to 2420'

 L. 893      2412  LOAD_FAST                'tmp_offset'
             2414  LOAD_CONST               7
             2416  INPLACE_ADD      
             2418  STORE_FAST               'tmp_offset'
           2420_0  COME_FROM          2408  '2408'

 L. 896      2420  LOAD_DEREF               'day_offset'
             2422  LOAD_FAST                'tmp_offset'
             2424  INPLACE_ADD      
             2426  STORE_DEREF              'day_offset'

 L. 897      2428  LOAD_FAST                'used'
             2430  LOAD_CONST               3
             2432  INPLACE_ADD      
             2434  STORE_FAST               'used'
           2436_0  COME_FROM          2372  '2372'
           2436_1  COME_FROM          2362  '2362'
           2436_2  COME_FROM          2358  '2358'
           2436_3  COME_FROM          2214  '2214'
           2436_4  COME_FROM          2184  '2184'
           2436_5  COME_FROM          2146  '2146'
           2436_6  COME_FROM          2136  '2136'

 L. 899      2436  LOAD_FAST                'used'
             2438  LOAD_CONST               0
             2440  COMPARE_OP               >
         2442_2444  POP_JUMP_IF_FALSE   320  'to 320'

 L. 900      2446  LOAD_FAST                'start'
             2448  LOAD_CONST               1
             2450  BINARY_SUBTRACT  
             2452  LOAD_CONST               0
             2454  COMPARE_OP               >
         2456_2458  POP_JUMP_IF_FALSE  2494  'to 2494'
             2460  LOAD_FAST                'words'
             2462  LOAD_FAST                'start'
             2464  LOAD_CONST               1
             2466  BINARY_SUBTRACT  
             2468  BINARY_SUBSCR    
             2470  LOAD_STR                 'questo'
             2472  COMPARE_OP               ==
         2474_2476  POP_JUMP_IF_FALSE  2494  'to 2494'

 L. 901      2478  LOAD_FAST                'start'
             2480  LOAD_CONST               1
             2482  INPLACE_SUBTRACT 
             2484  STORE_FAST               'start'

 L. 902      2486  LOAD_FAST                'used'
             2488  LOAD_CONST               1
             2490  INPLACE_ADD      
             2492  STORE_FAST               'used'
           2494_0  COME_FROM          2474  '2474'
           2494_1  COME_FROM          2456  '2456'

 L. 904      2494  SETUP_LOOP         2528  'to 2528'
             2496  LOAD_GLOBAL              range
             2498  LOAD_CONST               0
             2500  LOAD_FAST                'used'
             2502  CALL_FUNCTION_2       2  '2 positional arguments'
             2504  GET_ITER         
             2506  FOR_ITER           2526  'to 2526'
             2508  STORE_FAST               'i'

 L. 905      2510  LOAD_STR                 ''
             2512  LOAD_FAST                'words'
             2514  LOAD_FAST                'i'
             2516  LOAD_FAST                'start'
             2518  BINARY_ADD       
             2520  STORE_SUBSCR     
         2522_2524  JUMP_BACK          2506  'to 2506'
             2526  POP_BLOCK        
           2528_0  COME_FROM_LOOP     2494  '2494'

 L. 907      2528  LOAD_FAST                'start'
             2530  LOAD_CONST               1
             2532  BINARY_SUBTRACT  
             2534  LOAD_CONST               0
             2536  COMPARE_OP               >=
         2538_2540  POP_JUMP_IF_FALSE  2572  'to 2572'
             2542  LOAD_FAST                'words'
             2544  LOAD_FAST                'start'
             2546  LOAD_CONST               1
             2548  BINARY_SUBTRACT  
             2550  BINARY_SUBSCR    
             2552  LOAD_FAST                'markers'
             2554  COMPARE_OP               in
         2556_2558  POP_JUMP_IF_FALSE  2572  'to 2572'

 L. 908      2560  LOAD_STR                 ''
             2562  LOAD_FAST                'words'
             2564  LOAD_FAST                'start'
             2566  LOAD_CONST               1
             2568  BINARY_SUBTRACT  
             2570  STORE_SUBSCR     
           2572_0  COME_FROM          2556  '2556'
           2572_1  COME_FROM          2538  '2538'

 L. 909      2572  LOAD_CONST               True
             2574  STORE_DEREF              'found'

 L. 910      2576  LOAD_CONST               True
             2578  STORE_FAST               'day_specified'
         2580_2582  JUMP_BACK           320  'to 320'
             2584  POP_BLOCK        
           2586_0  COME_FROM_LOOP      308  '308'

 L. 913      2586  LOAD_STR                 ''
             2588  STORE_DEREF              'time_str'

 L. 914      2590  LOAD_CONST               0
             2592  STORE_DEREF              'hr_offset'

 L. 915      2594  LOAD_CONST               0
             2596  STORE_DEREF              'min_offset'

 L. 916      2598  LOAD_CONST               0
             2600  STORE_DEREF              'sec_offset'

 L. 917      2602  LOAD_CONST               None
             2604  STORE_DEREF              'hr_abs'

 L. 918      2606  LOAD_CONST               None
             2608  STORE_DEREF              'min_abs'

 L. 919      2610  LOAD_CONST               False
             2612  STORE_FAST               'military'

 L. 921  2614_2616  SETUP_LOOP         5022  'to 5022'
             2618  LOAD_GLOBAL              enumerate
             2620  LOAD_FAST                'words'
             2622  CALL_FUNCTION_1       1  '1 positional argument'
             2624  GET_ITER         
           2626_0  COME_FROM          4866  '4866'
         2626_2628  FOR_ITER           5020  'to 5020'
             2630  UNPACK_SEQUENCE_2     2 
             2632  STORE_FAST               'idx'
             2634  STORE_FAST               'word'

 L. 922      2636  LOAD_FAST                'word'
             2638  LOAD_STR                 ''
             2640  COMPARE_OP               ==
         2642_2644  POP_JUMP_IF_FALSE  2650  'to 2650'

 L. 923  2646_2648  CONTINUE           2626  'to 2626'
           2650_0  COME_FROM          2642  '2642'

 L. 924      2650  LOAD_FAST                'idx'
             2652  LOAD_CONST               1
             2654  COMPARE_OP               >
         2656_2658  POP_JUMP_IF_FALSE  2672  'to 2672'
             2660  LOAD_FAST                'words'
             2662  LOAD_FAST                'idx'
             2664  LOAD_CONST               2
             2666  BINARY_SUBTRACT  
             2668  BINARY_SUBSCR    
             2670  JUMP_FORWARD       2674  'to 2674'
           2672_0  COME_FROM          2656  '2656'
             2672  LOAD_STR                 ''
           2674_0  COME_FROM          2670  '2670'
             2674  STORE_FAST               'word_prev_prev'

 L. 925      2676  LOAD_FAST                'idx'
             2678  LOAD_CONST               0
             2680  COMPARE_OP               >
         2682_2684  POP_JUMP_IF_FALSE  2698  'to 2698'
             2686  LOAD_FAST                'words'
             2688  LOAD_FAST                'idx'
             2690  LOAD_CONST               1
             2692  BINARY_SUBTRACT  
             2694  BINARY_SUBSCR    
             2696  JUMP_FORWARD       2700  'to 2700'
           2698_0  COME_FROM          2682  '2682'
             2698  LOAD_STR                 ''
           2700_0  COME_FROM          2696  '2696'
             2700  STORE_FAST               'word_prev'

 L. 926      2702  LOAD_FAST                'idx'
             2704  LOAD_CONST               1
             2706  BINARY_ADD       
             2708  LOAD_GLOBAL              len
             2710  LOAD_FAST                'words'
             2712  CALL_FUNCTION_1       1  '1 positional argument'
             2714  COMPARE_OP               <
         2716_2718  POP_JUMP_IF_FALSE  2732  'to 2732'
             2720  LOAD_FAST                'words'
             2722  LOAD_FAST                'idx'
             2724  LOAD_CONST               1
             2726  BINARY_ADD       
             2728  BINARY_SUBSCR    
             2730  JUMP_FORWARD       2734  'to 2734'
           2732_0  COME_FROM          2716  '2716'
             2732  LOAD_STR                 ''
           2734_0  COME_FROM          2730  '2730'
             2734  STORE_FAST               'word_next'

 L. 927      2736  LOAD_FAST                'idx'
             2738  LOAD_CONST               2
             2740  BINARY_ADD       
             2742  LOAD_GLOBAL              len
             2744  LOAD_FAST                'words'
             2746  CALL_FUNCTION_1       1  '1 positional argument'
             2748  COMPARE_OP               <
         2750_2752  POP_JUMP_IF_FALSE  2766  'to 2766'
             2754  LOAD_FAST                'words'
             2756  LOAD_FAST                'idx'
             2758  LOAD_CONST               2
             2760  BINARY_ADD       
             2762  BINARY_SUBSCR    
             2764  JUMP_FORWARD       2768  'to 2768'
           2766_0  COME_FROM          2750  '2750'
             2766  LOAD_STR                 ''
           2768_0  COME_FROM          2764  '2764'
             2768  STORE_FAST               'word_next_next'

 L. 929      2770  LOAD_CONST               0
             2772  STORE_FAST               'used'

 L. 930      2774  LOAD_FAST                'word'
             2776  LOAD_STR                 'mezzogiorno'
             2778  COMPARE_OP               ==
         2780_2782  POP_JUMP_IF_FALSE  2798  'to 2798'

 L. 931      2784  LOAD_CONST               12
             2786  STORE_DEREF              'hr_abs'

 L. 932      2788  LOAD_FAST                'used'
             2790  LOAD_CONST               1
             2792  INPLACE_ADD      
             2794  STORE_FAST               'used'
             2796  JUMP_FORWARD       2820  'to 2820'
           2798_0  COME_FROM          2780  '2780'

 L. 933      2798  LOAD_FAST                'word'
             2800  LOAD_STR                 'mezzanotte'
             2802  COMPARE_OP               ==
         2804_2806  POP_JUMP_IF_FALSE  2820  'to 2820'

 L. 934      2808  LOAD_CONST               24
             2810  STORE_DEREF              'hr_abs'

 L. 935      2812  LOAD_FAST                'used'
             2814  LOAD_CONST               1
             2816  INPLACE_ADD      
             2818  STORE_FAST               'used'
           2820_0  COME_FROM          2804  '2804'
           2820_1  COME_FROM          2796  '2796'

 L. 936      2820  LOAD_FAST                'word'
             2822  LOAD_STR                 'mezzo'
             2824  COMPARE_OP               ==
         2826_2828  POP_JUMP_IF_FALSE  2856  'to 2856'
             2830  LOAD_FAST                'word_next'
             2832  LOAD_STR                 'giorno'
             2834  COMPARE_OP               ==
         2836_2838  POP_JUMP_IF_FALSE  2856  'to 2856'

 L. 937      2840  LOAD_CONST               12
             2842  STORE_DEREF              'hr_abs'

 L. 938      2844  LOAD_FAST                'used'
             2846  LOAD_CONST               2
             2848  INPLACE_ADD      
             2850  STORE_FAST               'used'
         2852_2854  JUMP_FORWARD       4860  'to 4860'
           2856_0  COME_FROM          2836  '2836'
           2856_1  COME_FROM          2826  '2826'

 L. 939      2856  LOAD_FAST                'word'
             2858  LOAD_STR                 'mezza'
             2860  COMPARE_OP               ==
         2862_2864  POP_JUMP_IF_FALSE  2892  'to 2892'
             2866  LOAD_FAST                'word_next'
             2868  LOAD_STR                 'notte'
             2870  COMPARE_OP               ==
         2872_2874  POP_JUMP_IF_FALSE  2892  'to 2892'

 L. 940      2876  LOAD_CONST               24
             2878  STORE_DEREF              'hr_abs'

 L. 941      2880  LOAD_FAST                'used'
             2882  LOAD_CONST               2
             2884  INPLACE_ADD      
             2886  STORE_FAST               'used'
         2888_2890  JUMP_FORWARD       4860  'to 4860'
           2892_0  COME_FROM          2872  '2872'
           2892_1  COME_FROM          2862  '2862'

 L. 942      2892  LOAD_FAST                'word'
             2894  LOAD_STR                 'mattina'
             2896  COMPARE_OP               ==
         2898_2900  POP_JUMP_IF_FALSE  2960  'to 2960'

 L. 943      2902  LOAD_DEREF               'hr_abs'
         2904_2906  POP_JUMP_IF_TRUE   2912  'to 2912'

 L. 944      2908  LOAD_CONST               8
             2910  STORE_DEREF              'hr_abs'
           2912_0  COME_FROM          2904  '2904'

 L. 945      2912  LOAD_FAST                'used'
             2914  LOAD_CONST               1
             2916  INPLACE_ADD      
             2918  STORE_FAST               'used'

 L. 946      2920  LOAD_FAST                'word_next'
         2922_2924  POP_JUMP_IF_FALSE  4860  'to 4860'
             2926  LOAD_FAST                'word_next'
             2928  LOAD_CONST               0
             2930  BINARY_SUBSCR    
             2932  LOAD_METHOD              isdigit
             2934  CALL_METHOD_0         0  '0 positional arguments'
         2936_2938  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 947      2940  LOAD_GLOBAL              int
             2942  LOAD_FAST                'word_next'
             2944  CALL_FUNCTION_1       1  '1 positional argument'
             2946  STORE_DEREF              'hr_abs'

 L. 948      2948  LOAD_FAST                'used'
             2950  LOAD_CONST               1
             2952  INPLACE_ADD      
             2954  STORE_FAST               'used'
         2956_2958  JUMP_FORWARD       4860  'to 4860'
           2960_0  COME_FROM          2898  '2898'

 L. 949      2960  LOAD_FAST                'word'
             2962  LOAD_STR                 'pomeriggio'
             2964  COMPARE_OP               ==
         2966_2968  POP_JUMP_IF_FALSE  3058  'to 3058'

 L. 950      2970  LOAD_DEREF               'hr_abs'
         2972_2974  POP_JUMP_IF_TRUE   2980  'to 2980'

 L. 951      2976  LOAD_CONST               15
             2978  STORE_DEREF              'hr_abs'
           2980_0  COME_FROM          2972  '2972'

 L. 952      2980  LOAD_FAST                'used'
             2982  LOAD_CONST               1
             2984  INPLACE_ADD      
             2986  STORE_FAST               'used'

 L. 953      2988  LOAD_FAST                'word_next'
         2990_2992  POP_JUMP_IF_FALSE  4860  'to 4860'
             2994  LOAD_FAST                'word_next'
             2996  LOAD_CONST               0
             2998  BINARY_SUBSCR    
             3000  LOAD_METHOD              isdigit
             3002  CALL_METHOD_0         0  '0 positional arguments'
         3004_3006  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 954      3008  LOAD_GLOBAL              int
             3010  LOAD_FAST                'word_next'
             3012  CALL_FUNCTION_1       1  '1 positional argument'
             3014  STORE_DEREF              'hr_abs'

 L. 955      3016  LOAD_FAST                'used'
             3018  LOAD_CONST               1
             3020  INPLACE_ADD      
             3022  STORE_FAST               'used'

 L. 956      3024  LOAD_DEREF               'hr_abs'
         3026_3028  JUMP_IF_TRUE_OR_POP  3032  'to 3032'
             3030  LOAD_CONST               0
           3032_0  COME_FROM          3026  '3026'
             3032  LOAD_CONST               12
             3034  COMPARE_OP               <
         3036_3038  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 957      3040  LOAD_DEREF               'hr_abs'
         3042_3044  JUMP_IF_TRUE_OR_POP  3048  'to 3048'
             3046  LOAD_CONST               0
           3048_0  COME_FROM          3042  '3042'
             3048  LOAD_CONST               12
             3050  BINARY_ADD       
             3052  STORE_DEREF              'hr_abs'
         3054_3056  JUMP_FORWARD       4860  'to 4860'
           3058_0  COME_FROM          2966  '2966'

 L. 958      3058  LOAD_FAST                'word'
             3060  LOAD_STR                 'sera'
             3062  COMPARE_OP               ==
         3064_3066  POP_JUMP_IF_FALSE  3166  'to 3166'

 L. 959      3068  LOAD_DEREF               'hr_abs'
         3070_3072  POP_JUMP_IF_TRUE   3078  'to 3078'

 L. 960      3074  LOAD_CONST               19
             3076  STORE_DEREF              'hr_abs'
           3078_0  COME_FROM          3070  '3070'

 L. 961      3078  LOAD_FAST                'used'
             3080  LOAD_CONST               1
             3082  INPLACE_ADD      
             3084  STORE_FAST               'used'

 L. 962      3086  LOAD_FAST                'word_next'
         3088_3090  POP_JUMP_IF_FALSE  4860  'to 4860'
             3092  LOAD_FAST                'word_next'
             3094  LOAD_CONST               0
             3096  BINARY_SUBSCR    
             3098  LOAD_METHOD              isdigit
             3100  CALL_METHOD_0         0  '0 positional arguments'
         3102_3104  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 963      3106  LOAD_STR                 ':'
             3108  LOAD_FAST                'word_next'
             3110  COMPARE_OP               not-in
         3112_3114  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 964      3116  LOAD_GLOBAL              int
             3118  LOAD_FAST                'word_next'
             3120  CALL_FUNCTION_1       1  '1 positional argument'
             3122  STORE_DEREF              'hr_abs'

 L. 965      3124  LOAD_FAST                'used'
             3126  LOAD_CONST               1
             3128  INPLACE_ADD      
             3130  STORE_FAST               'used'

 L. 966      3132  LOAD_DEREF               'hr_abs'
         3134_3136  JUMP_IF_TRUE_OR_POP  3140  'to 3140'
             3138  LOAD_CONST               0
           3140_0  COME_FROM          3134  '3134'
             3140  LOAD_CONST               12
             3142  COMPARE_OP               <
         3144_3146  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 967      3148  LOAD_DEREF               'hr_abs'
         3150_3152  JUMP_IF_TRUE_OR_POP  3156  'to 3156'
             3154  LOAD_CONST               0
           3156_0  COME_FROM          3150  '3150'
             3156  LOAD_CONST               12
             3158  BINARY_ADD       
             3160  STORE_DEREF              'hr_abs'
         3162_3164  JUMP_FORWARD       4860  'to 4860'
           3166_0  COME_FROM          3064  '3064'

 L. 969      3166  LOAD_FAST                'word'
             3168  LOAD_STR                 'presto'
             3170  COMPARE_OP               ==
         3172_3174  POP_JUMP_IF_FALSE  3196  'to 3196'

 L. 970      3176  LOAD_DEREF               'hr_abs'
             3178  LOAD_CONST               1
             3180  INPLACE_SUBTRACT 
             3182  STORE_DEREF              'hr_abs'

 L. 971      3184  LOAD_FAST                'used'
             3186  LOAD_CONST               1
             3188  INPLACE_ADD      
             3190  STORE_FAST               'used'
         3192_3194  JUMP_FORWARD       4860  'to 4860'
           3196_0  COME_FROM          3172  '3172'

 L. 972      3196  LOAD_FAST                'word'
             3198  LOAD_STR                 'tardi'
             3200  COMPARE_OP               ==
         3202_3204  POP_JUMP_IF_FALSE  3226  'to 3226'

 L. 973      3206  LOAD_DEREF               'hr_abs'
             3208  LOAD_CONST               1
             3210  INPLACE_ADD      
             3212  STORE_DEREF              'hr_abs'

 L. 974      3214  LOAD_FAST                'used'
             3216  LOAD_CONST               1
             3218  INPLACE_ADD      
             3220  STORE_FAST               'used'
         3222_3224  JUMP_FORWARD       4860  'to 4860'
           3226_0  COME_FROM          3202  '3202'

 L. 976      3226  LOAD_GLOBAL              extractnumber_it
             3228  LOAD_FAST                'word'
             3230  CALL_FUNCTION_1       1  '1 positional argument'
         3232_3234  POP_JUMP_IF_FALSE  3352  'to 3352'
             3236  LOAD_FAST                'word_next'
             3238  LOAD_FAST                'time_multiples'
             3240  COMPARE_OP               in
         3242_3244  POP_JUMP_IF_FALSE  3352  'to 3352'

 L. 977      3246  LOAD_GLOBAL              int
             3248  LOAD_GLOBAL              extractnumber_it
             3250  LOAD_FAST                'word'
             3252  CALL_FUNCTION_1       1  '1 positional argument'
             3254  CALL_FUNCTION_1       1  '1 positional argument'
             3256  STORE_FAST               'd_time'

 L. 978      3258  LOAD_FAST                'used'
             3260  LOAD_CONST               2
             3262  INPLACE_ADD      
             3264  STORE_FAST               'used'

 L. 979      3266  LOAD_FAST                'word_next'
             3268  LOAD_STR                 'ora'
             3270  COMPARE_OP               ==
         3272_3274  POP_JUMP_IF_FALSE  3294  'to 3294'

 L. 980      3276  LOAD_FAST                'd_time'
             3278  STORE_DEREF              'hr_offset'

 L. 981      3280  LOAD_CONST               False
             3282  STORE_FAST               'isTime'

 L. 982      3284  LOAD_CONST               -1
             3286  STORE_DEREF              'hr_abs'

 L. 983      3288  LOAD_CONST               -1
             3290  STORE_DEREF              'min_abs'
             3292  JUMP_FORWARD       4860  'to 4860'
           3294_0  COME_FROM          3272  '3272'

 L. 984      3294  LOAD_FAST                'word_next'
             3296  LOAD_STR                 'minuto'
             3298  COMPARE_OP               ==
         3300_3302  POP_JUMP_IF_FALSE  3322  'to 3322'

 L. 985      3304  LOAD_FAST                'd_time'
             3306  STORE_DEREF              'min_offset'

 L. 986      3308  LOAD_CONST               False
             3310  STORE_FAST               'isTime'

 L. 987      3312  LOAD_CONST               -1
             3314  STORE_DEREF              'hr_abs'

 L. 988      3316  LOAD_CONST               -1
             3318  STORE_DEREF              'min_abs'
             3320  JUMP_FORWARD       4860  'to 4860'
           3322_0  COME_FROM          3300  '3300'

 L. 989      3322  LOAD_FAST                'word_next'
             3324  LOAD_STR                 'secondo'
             3326  COMPARE_OP               ==
         3328_3330  POP_JUMP_IF_FALSE  4860  'to 4860'

 L. 990      3332  LOAD_FAST                'd_time'
             3334  STORE_DEREF              'sec_offset'

 L. 991      3336  LOAD_CONST               False
             3338  STORE_FAST               'isTime'

 L. 992      3340  LOAD_CONST               -1
             3342  STORE_DEREF              'hr_abs'

 L. 993      3344  LOAD_CONST               -1
             3346  STORE_DEREF              'min_abs'
         3348_3350  JUMP_FORWARD       4860  'to 4860'
           3352_0  COME_FROM          3242  '3242'
           3352_1  COME_FROM          3232  '3232'

 L. 994      3352  LOAD_FAST                'word'
             3354  LOAD_STR                 'mezzora'
             3356  COMPARE_OP               ==
         3358_3360  POP_JUMP_IF_FALSE  3386  'to 3386'

 L. 995      3362  LOAD_CONST               30
             3364  STORE_DEREF              'min_offset'

 L. 996      3366  LOAD_CONST               1
             3368  STORE_FAST               'used'

 L. 997      3370  LOAD_CONST               False
             3372  STORE_FAST               'isTime'

 L. 998      3374  LOAD_CONST               -1
             3376  STORE_DEREF              'hr_abs'

 L. 999      3378  LOAD_CONST               -1
             3380  STORE_DEREF              'min_abs'
         3382_3384  JUMP_FORWARD       4860  'to 4860'
           3386_0  COME_FROM          3358  '3358'

 L.1003      3386  LOAD_GLOBAL              extractnumber_it
             3388  LOAD_FAST                'word'
             3390  CALL_FUNCTION_1       1  '1 positional argument'
         3392_3394  POP_JUMP_IF_FALSE  3508  'to 3508'
             3396  LOAD_FAST                'word_next'
         3398_3400  POP_JUMP_IF_FALSE  3508  'to 3508'

 L.1004      3402  LOAD_FAST                'word_next'
             3404  LOAD_STR                 'quarto'
             3406  COMPARE_OP               ==
         3408_3410  POP_JUMP_IF_FALSE  3508  'to 3508'
             3412  LOAD_FAST                'word_next_next'
             3414  LOAD_STR                 'ora'
             3416  COMPARE_OP               ==
         3418_3420  POP_JUMP_IF_FALSE  3508  'to 3508'

 L.1005      3422  LOAD_GLOBAL              int
             3424  LOAD_GLOBAL              extractnumber_it
             3426  LOAD_FAST                'word'
             3428  CALL_FUNCTION_1       1  '1 positional argument'
             3430  CALL_FUNCTION_1       1  '1 positional argument'
             3432  LOAD_CONST               1
             3434  COMPARE_OP               ==
         3436_3438  POP_JUMP_IF_TRUE   3458  'to 3458'

 L.1006      3440  LOAD_GLOBAL              int
             3442  LOAD_GLOBAL              extractnumber_it
             3444  LOAD_FAST                'word'
             3446  CALL_FUNCTION_1       1  '1 positional argument'
             3448  CALL_FUNCTION_1       1  '1 positional argument'
             3450  LOAD_CONST               3
             3452  COMPARE_OP               ==
         3454_3456  POP_JUMP_IF_FALSE  3476  'to 3476'
           3458_0  COME_FROM          3436  '3436'

 L.1007      3458  LOAD_CONST               15
             3460  LOAD_GLOBAL              int
             3462  LOAD_GLOBAL              extractnumber_it
             3464  LOAD_FAST                'word'
             3466  CALL_FUNCTION_1       1  '1 positional argument'
             3468  CALL_FUNCTION_1       1  '1 positional argument'
             3470  BINARY_MULTIPLY  
             3472  STORE_DEREF              'min_offset'
             3474  JUMP_FORWARD       3480  'to 3480'
           3476_0  COME_FROM          3454  '3454'

 L.1009      3476  LOAD_CONST               15
             3478  STORE_DEREF              'min_offset'
           3480_0  COME_FROM          3474  '3474'

 L.1010      3480  LOAD_CONST               3
             3482  STORE_FAST               'used'

 L.1011      3484  LOAD_FAST                'start'
             3486  LOAD_CONST               1
             3488  INPLACE_SUBTRACT 
             3490  STORE_FAST               'start'

 L.1012      3492  LOAD_CONST               False
             3494  STORE_FAST               'isTime'

 L.1013      3496  LOAD_CONST               -1
             3498  STORE_DEREF              'hr_abs'

 L.1014      3500  LOAD_CONST               -1
             3502  STORE_DEREF              'min_abs'
         3504_3506  JUMP_FORWARD       4860  'to 4860'
           3508_0  COME_FROM          3418  '3418'
           3508_1  COME_FROM          3408  '3408'
           3508_2  COME_FROM          3398  '3398'
           3508_3  COME_FROM          3392  '3392'

 L.1015      3508  LOAD_FAST                'word'
             3510  LOAD_CONST               0
             3512  BINARY_SUBSCR    
             3514  LOAD_METHOD              isdigit
             3516  CALL_METHOD_0         0  '0 positional arguments'
         3518_3520  POP_JUMP_IF_FALSE  4860  'to 4860'

 L.1016      3522  LOAD_CONST               True
             3524  STORE_FAST               'isTime'

 L.1017      3526  LOAD_STR                 ''
             3528  STORE_FAST               'str_hh'

 L.1018      3530  LOAD_STR                 ''
             3532  STORE_FAST               'str_mm'

 L.1019      3534  LOAD_STR                 ''
             3536  STORE_FAST               'remainder'

 L.1020      3538  LOAD_STR                 ':'
             3540  LOAD_FAST                'word'
             3542  COMPARE_OP               in
         3544_3546  POP_JUMP_IF_FALSE  3698  'to 3698'

 L.1023      3548  LOAD_FAST                'word'
             3550  LOAD_METHOD              split
             3552  LOAD_STR                 ':'
             3554  CALL_METHOD_1         1  '1 positional argument'
             3556  STORE_FAST               'components'

 L.1024      3558  LOAD_GLOBAL              len
             3560  LOAD_FAST                'components'
             3562  CALL_FUNCTION_1       1  '1 positional argument'
             3564  LOAD_CONST               2
             3566  COMPARE_OP               ==
         3568_3570  POP_JUMP_IF_FALSE  3830  'to 3830'

 L.1025      3572  LOAD_GLOBAL              int
             3574  LOAD_GLOBAL              extractnumber_it
             3576  LOAD_FAST                'components'
             3578  LOAD_CONST               0
             3580  BINARY_SUBSCR    
             3582  CALL_FUNCTION_1       1  '1 positional argument'
             3584  CALL_FUNCTION_1       1  '1 positional argument'
             3586  STORE_FAST               'num0'

 L.1026      3588  LOAD_GLOBAL              int
             3590  LOAD_GLOBAL              extractnumber_it
             3592  LOAD_FAST                'components'
             3594  LOAD_CONST               1
             3596  BINARY_SUBSCR    
             3598  CALL_FUNCTION_1       1  '1 positional argument'
             3600  CALL_FUNCTION_1       1  '1 positional argument'
             3602  STORE_FAST               'num1'

 L.1027      3604  LOAD_FAST                'num0'
             3606  LOAD_CONST               False
             3608  COMPARE_OP               is-not
         3610_3612  POP_JUMP_IF_FALSE  3830  'to 3830'
             3614  LOAD_FAST                'num1'
             3616  LOAD_CONST               False
             3618  COMPARE_OP               is-not
         3620_3622  POP_JUMP_IF_FALSE  3830  'to 3830'

 L.1028      3624  LOAD_CONST               0
             3626  LOAD_FAST                'num0'
             3628  DUP_TOP          
             3630  ROT_THREE        
             3632  COMPARE_OP               <=
         3634_3636  POP_JUMP_IF_FALSE  3648  'to 3648'
             3638  LOAD_CONST               23
             3640  COMPARE_OP               <=
         3642_3644  POP_JUMP_IF_FALSE  3830  'to 3830'
             3646  JUMP_FORWARD       3652  'to 3652'
           3648_0  COME_FROM          3634  '3634'
             3648  POP_TOP          
             3650  JUMP_FORWARD       3696  'to 3696'
           3652_0  COME_FROM          3646  '3646'
             3652  LOAD_CONST               0
             3654  LOAD_FAST                'num1'
             3656  DUP_TOP          
             3658  ROT_THREE        
             3660  COMPARE_OP               <=
         3662_3664  POP_JUMP_IF_FALSE  3676  'to 3676'
             3666  LOAD_CONST               59
             3668  COMPARE_OP               <=
         3670_3672  POP_JUMP_IF_FALSE  3830  'to 3830'
             3674  JUMP_FORWARD       3680  'to 3680'
           3676_0  COME_FROM          3662  '3662'
             3676  POP_TOP          
             3678  JUMP_FORWARD       3696  'to 3696'
           3680_0  COME_FROM          3674  '3674'

 L.1029      3680  LOAD_GLOBAL              str
             3682  LOAD_FAST                'num0'
             3684  CALL_FUNCTION_1       1  '1 positional argument'
             3686  STORE_FAST               'str_hh'

 L.1030      3688  LOAD_GLOBAL              str
             3690  LOAD_FAST                'num1'
             3692  CALL_FUNCTION_1       1  '1 positional argument'
             3694  STORE_FAST               'str_mm'
           3696_0  COME_FROM          3678  '3678'
           3696_1  COME_FROM          3650  '3650'
             3696  JUMP_FORWARD       3830  'to 3830'
           3698_0  COME_FROM          3544  '3544'

 L.1031      3698  LOAD_CONST               0
             3700  LOAD_GLOBAL              int
             3702  LOAD_GLOBAL              extractnumber_it
             3704  LOAD_FAST                'word'
             3706  CALL_FUNCTION_1       1  '1 positional argument'
             3708  CALL_FUNCTION_1       1  '1 positional argument'
             3710  DUP_TOP          
             3712  ROT_THREE        
             3714  COMPARE_OP               <
         3716_3718  POP_JUMP_IF_FALSE  3730  'to 3730'
             3720  LOAD_CONST               24
             3722  COMPARE_OP               <
         3724_3726  POP_JUMP_IF_FALSE  3762  'to 3762'
             3728  JUMP_FORWARD       3734  'to 3734'
           3730_0  COME_FROM          3716  '3716'
             3730  POP_TOP          
             3732  JUMP_FORWARD       3762  'to 3762'
           3734_0  COME_FROM          3728  '3728'

 L.1032      3734  LOAD_FAST                'word_next'
             3736  LOAD_STR                 'quarto'
             3738  COMPARE_OP               !=
         3740_3742  POP_JUMP_IF_FALSE  3762  'to 3762'

 L.1033      3744  LOAD_GLOBAL              str
             3746  LOAD_GLOBAL              int
             3748  LOAD_FAST                'word'
             3750  CALL_FUNCTION_1       1  '1 positional argument'
             3752  CALL_FUNCTION_1       1  '1 positional argument'
             3754  STORE_FAST               'str_hh'

 L.1034      3756  LOAD_STR                 '00'
             3758  STORE_FAST               'str_mm'
             3760  JUMP_FORWARD       3830  'to 3830'
           3762_0  COME_FROM          3740  '3740'
           3762_1  COME_FROM          3732  '3732'
           3762_2  COME_FROM          3724  '3724'

 L.1035      3762  LOAD_CONST               100
             3764  LOAD_GLOBAL              int
             3766  LOAD_FAST                'word'
             3768  CALL_FUNCTION_1       1  '1 positional argument'
             3770  DUP_TOP          
             3772  ROT_THREE        
             3774  COMPARE_OP               <=
         3776_3778  POP_JUMP_IF_FALSE  3790  'to 3790'
             3780  LOAD_CONST               2400
             3782  COMPARE_OP               <=
         3784_3786  POP_JUMP_IF_FALSE  3830  'to 3830'
             3788  JUMP_FORWARD       3794  'to 3794'
           3790_0  COME_FROM          3776  '3776'
             3790  POP_TOP          
             3792  JUMP_FORWARD       3830  'to 3830'
           3794_0  COME_FROM          3788  '3788'

 L.1036      3794  LOAD_GLOBAL              int
             3796  LOAD_FAST                'word'
             3798  CALL_FUNCTION_1       1  '1 positional argument'
             3800  LOAD_CONST               100
             3802  BINARY_TRUE_DIVIDE
             3804  STORE_FAST               'str_hh'

 L.1037      3806  LOAD_GLOBAL              int
             3808  LOAD_FAST                'word'
             3810  CALL_FUNCTION_1       1  '1 positional argument'
             3812  LOAD_FAST                'str_hh'
             3814  LOAD_CONST               100
             3816  BINARY_MULTIPLY  
             3818  BINARY_SUBTRACT  
             3820  STORE_FAST               'str_mm'

 L.1038      3822  LOAD_CONST               True
             3824  STORE_FAST               'military'

 L.1039      3826  LOAD_CONST               False
             3828  STORE_FAST               'isTime'
           3830_0  COME_FROM          3792  '3792'
           3830_1  COME_FROM          3784  '3784'
           3830_2  COME_FROM          3760  '3760'
           3830_3  COME_FROM          3696  '3696'
           3830_4  COME_FROM          3670  '3670'
           3830_5  COME_FROM          3642  '3642'
           3830_6  COME_FROM          3620  '3620'
           3830_7  COME_FROM          3610  '3610'
           3830_8  COME_FROM          3568  '3568'

 L.1040      3830  LOAD_GLOBAL              extractnumber_it
             3832  LOAD_FAST                'word'
             3834  CALL_FUNCTION_1       1  '1 positional argument'
         3836_3838  POP_JUMP_IF_FALSE  3956  'to 3956'
             3840  LOAD_FAST                'word_next'
         3842_3844  POP_JUMP_IF_FALSE  3956  'to 3956'

 L.1041      3846  LOAD_FAST                'word_next'
             3848  LOAD_STR                 'quarto'
             3850  COMPARE_OP               ==
         3852_3854  POP_JUMP_IF_FALSE  3956  'to 3956'
             3856  LOAD_FAST                'word_next_next'
             3858  LOAD_STR                 'ora'
             3860  COMPARE_OP               !=
         3862_3864  POP_JUMP_IF_FALSE  3956  'to 3956'

 L.1042      3866  LOAD_GLOBAL              int
             3868  LOAD_GLOBAL              extractnumber_it
             3870  LOAD_FAST                'word'
             3872  CALL_FUNCTION_1       1  '1 positional argument'
             3874  CALL_FUNCTION_1       1  '1 positional argument'
             3876  LOAD_CONST               1
             3878  COMPARE_OP               ==
         3880_3882  POP_JUMP_IF_TRUE   3902  'to 3902'

 L.1043      3884  LOAD_GLOBAL              int
             3886  LOAD_GLOBAL              extractnumber_it
             3888  LOAD_FAST                'word'
             3890  CALL_FUNCTION_1       1  '1 positional argument'
             3892  CALL_FUNCTION_1       1  '1 positional argument'
             3894  LOAD_CONST               3
             3896  COMPARE_OP               ==
         3898_3900  POP_JUMP_IF_FALSE  3924  'to 3924'
           3902_0  COME_FROM          3880  '3880'

 L.1044      3902  LOAD_GLOBAL              str
             3904  LOAD_CONST               15
             3906  LOAD_GLOBAL              int
             3908  LOAD_GLOBAL              extractnumber_it
             3910  LOAD_FAST                'word'
             3912  CALL_FUNCTION_1       1  '1 positional argument'
             3914  CALL_FUNCTION_1       1  '1 positional argument'
             3916  BINARY_MULTIPLY  
             3918  CALL_FUNCTION_1       1  '1 positional argument'
             3920  STORE_FAST               'str_mm'
             3922  JUMP_FORWARD       3928  'to 3928'
           3924_0  COME_FROM          3898  '3898'

 L.1046      3924  LOAD_STR                 '0'
             3926  STORE_FAST               'str_mm'
           3928_0  COME_FROM          3922  '3922'

 L.1047      3928  LOAD_GLOBAL              str
             3930  LOAD_DEREF               'hr_abs'
             3932  CALL_FUNCTION_1       1  '1 positional argument'
             3934  STORE_FAST               'str_hh'

 L.1048      3936  LOAD_CONST               2
             3938  STORE_FAST               'used'

 L.1049      3940  LOAD_STR                 ''
             3942  LOAD_FAST                'words'
             3944  LOAD_FAST                'idx'
             3946  LOAD_CONST               1
             3948  BINARY_ADD       
             3950  STORE_SUBSCR     

 L.1050      3952  LOAD_CONST               False
             3954  STORE_FAST               'isTime'
           3956_0  COME_FROM          3862  '3862'
           3956_1  COME_FROM          3852  '3852'
           3956_2  COME_FROM          3842  '3842'
           3956_3  COME_FROM          3836  '3836'

 L.1051      3956  LOAD_GLOBAL              extractnumber_it
             3958  LOAD_FAST                'word'
             3960  CALL_FUNCTION_1       1  '1 positional argument'
         3962_3964  POP_JUMP_IF_FALSE  4002  'to 4002'
             3966  LOAD_FAST                'word_next'
         3968_3970  POP_JUMP_IF_FALSE  4002  'to 4002'

 L.1052      3972  LOAD_FAST                'word_next'
             3974  LOAD_STR                 'in_punto'
             3976  COMPARE_OP               ==
         3978_3980  POP_JUMP_IF_FALSE  4002  'to 4002'

 L.1053      3982  LOAD_GLOBAL              str
             3984  LOAD_GLOBAL              int
             3986  LOAD_GLOBAL              extractnumber_it
             3988  LOAD_FAST                'word'
             3990  CALL_FUNCTION_1       1  '1 positional argument'
             3992  CALL_FUNCTION_1       1  '1 positional argument'
             3994  CALL_FUNCTION_1       1  '1 positional argument'
             3996  STORE_FAST               'str_hh'

 L.1054      3998  LOAD_CONST               2
             4000  STORE_FAST               'used'
           4002_0  COME_FROM          3978  '3978'
           4002_1  COME_FROM          3968  '3968'
           4002_2  COME_FROM          3962  '3962'

 L.1055      4002  LOAD_FAST                'word_next'
             4004  LOAD_STR                 'pm'
             4006  COMPARE_OP               ==
         4008_4010  POP_JUMP_IF_FALSE  4058  'to 4058'

 L.1056      4012  LOAD_STR                 'pm'
             4014  STORE_FAST               'remainder'

 L.1057      4016  LOAD_GLOBAL              int
             4018  LOAD_FAST                'str_hh'
             4020  CALL_FUNCTION_1       1  '1 positional argument'
             4022  STORE_DEREF              'hr_abs'

 L.1058      4024  LOAD_GLOBAL              int
             4026  LOAD_FAST                'str_mm'
             4028  CALL_FUNCTION_1       1  '1 positional argument'
             4030  STORE_DEREF              'min_abs'

 L.1059      4032  LOAD_DEREF               'hr_abs'
             4034  LOAD_CONST               12
             4036  COMPARE_OP               <=
         4038_4040  POP_JUMP_IF_FALSE  4050  'to 4050'

 L.1060      4042  LOAD_DEREF               'hr_abs'
             4044  LOAD_CONST               12
             4046  BINARY_ADD       
             4048  STORE_DEREF              'hr_abs'
           4050_0  COME_FROM          4038  '4038'

 L.1061      4050  LOAD_CONST               2
             4052  STORE_FAST               'used'
         4054_4056  JUMP_FORWARD       4474  'to 4474'
           4058_0  COME_FROM          4008  '4008'

 L.1062      4058  LOAD_FAST                'word_next'
             4060  LOAD_STR                 'am'
             4062  COMPARE_OP               ==
         4064_4066  POP_JUMP_IF_FALSE  4096  'to 4096'

 L.1063      4068  LOAD_STR                 'am'
             4070  STORE_FAST               'remainder'

 L.1064      4072  LOAD_GLOBAL              int
             4074  LOAD_FAST                'str_hh'
             4076  CALL_FUNCTION_1       1  '1 positional argument'
             4078  STORE_DEREF              'hr_abs'

 L.1065      4080  LOAD_GLOBAL              int
             4082  LOAD_FAST                'str_mm'
             4084  CALL_FUNCTION_1       1  '1 positional argument'
             4086  STORE_DEREF              'min_abs'

 L.1066      4088  LOAD_CONST               2
             4090  STORE_FAST               'used'
         4092_4094  JUMP_FORWARD       4474  'to 4474'
           4096_0  COME_FROM          4064  '4064'

 L.1067      4096  LOAD_FAST                'word_next'
             4098  LOAD_STR                 'mattina'
             4100  COMPARE_OP               ==
         4102_4104  POP_JUMP_IF_FALSE  4146  'to 4146'

 L.1069      4106  LOAD_GLOBAL              int
             4108  LOAD_FAST                'str_hh'
             4110  CALL_FUNCTION_1       1  '1 positional argument'
             4112  STORE_FAST               'hh'

 L.1070      4114  LOAD_GLOBAL              int
             4116  LOAD_FAST                'str_mm'
             4118  CALL_FUNCTION_1       1  '1 positional argument'
             4120  STORE_FAST               'mm'

 L.1071      4122  LOAD_CONST               2
             4124  STORE_FAST               'used'

 L.1072      4126  LOAD_STR                 'am'
             4128  STORE_FAST               'remainder'

 L.1073      4130  LOAD_CONST               False
             4132  STORE_FAST               'isTime'

 L.1074      4134  LOAD_FAST                'hh'
             4136  STORE_DEREF              'hr_abs'

 L.1075      4138  LOAD_FAST                'mm'
             4140  STORE_DEREF              'min_abs'
         4142_4144  JUMP_FORWARD       4474  'to 4474'
           4146_0  COME_FROM          4102  '4102'

 L.1076      4146  LOAD_FAST                'word_next'
             4148  LOAD_STR                 'pomeriggio'
             4150  COMPARE_OP               ==
         4152_4154  POP_JUMP_IF_FALSE  4214  'to 4214'

 L.1078      4156  LOAD_GLOBAL              int
             4158  LOAD_FAST                'str_hh'
             4160  CALL_FUNCTION_1       1  '1 positional argument'
             4162  STORE_FAST               'hh'

 L.1079      4164  LOAD_GLOBAL              int
             4166  LOAD_FAST                'str_mm'
             4168  CALL_FUNCTION_1       1  '1 positional argument'
             4170  STORE_FAST               'mm'

 L.1080      4172  LOAD_FAST                'hh'
             4174  LOAD_CONST               12
             4176  COMPARE_OP               <
         4178_4180  POP_JUMP_IF_FALSE  4190  'to 4190'

 L.1081      4182  LOAD_FAST                'hh'
             4184  LOAD_CONST               12
             4186  INPLACE_ADD      
             4188  STORE_FAST               'hh'
           4190_0  COME_FROM          4178  '4178'

 L.1082      4190  LOAD_CONST               2
             4192  STORE_FAST               'used'

 L.1083      4194  LOAD_STR                 'pm'
             4196  STORE_FAST               'remainder'

 L.1084      4198  LOAD_CONST               False
             4200  STORE_FAST               'isTime'

 L.1085      4202  LOAD_FAST                'hh'
             4204  STORE_DEREF              'hr_abs'

 L.1086      4206  LOAD_FAST                'mm'
             4208  STORE_DEREF              'min_abs'
         4210_4212  JUMP_FORWARD       4474  'to 4474'
           4214_0  COME_FROM          4152  '4152'

 L.1087      4214  LOAD_FAST                'word_next'
             4216  LOAD_STR                 'sera'
             4218  COMPARE_OP               ==
         4220_4222  POP_JUMP_IF_FALSE  4280  'to 4280'

 L.1089      4224  LOAD_GLOBAL              int
             4226  LOAD_FAST                'str_hh'
             4228  CALL_FUNCTION_1       1  '1 positional argument'
             4230  STORE_FAST               'hh'

 L.1090      4232  LOAD_GLOBAL              int
             4234  LOAD_FAST                'str_mm'
             4236  CALL_FUNCTION_1       1  '1 positional argument'
             4238  STORE_FAST               'mm'

 L.1091      4240  LOAD_FAST                'hh'
             4242  LOAD_CONST               12
             4244  COMPARE_OP               <
         4246_4248  POP_JUMP_IF_FALSE  4258  'to 4258'

 L.1092      4250  LOAD_FAST                'hh'
             4252  LOAD_CONST               12
             4254  INPLACE_ADD      
             4256  STORE_FAST               'hh'
           4258_0  COME_FROM          4246  '4246'

 L.1093      4258  LOAD_CONST               2
             4260  STORE_FAST               'used'

 L.1094      4262  LOAD_STR                 'pm'
             4264  STORE_FAST               'remainder'

 L.1095      4266  LOAD_CONST               False
             4268  STORE_FAST               'isTime'

 L.1096      4270  LOAD_FAST                'hh'
             4272  STORE_DEREF              'hr_abs'

 L.1097      4274  LOAD_FAST                'mm'
             4276  STORE_DEREF              'min_abs'
             4278  JUMP_FORWARD       4474  'to 4474'
           4280_0  COME_FROM          4220  '4220'

 L.1098      4280  LOAD_FAST                'word_next'
             4282  LOAD_STR                 'notte'
             4284  COMPARE_OP               ==
         4286_4288  POP_JUMP_IF_FALSE  4344  'to 4344'

 L.1099      4290  LOAD_GLOBAL              int
             4292  LOAD_FAST                'str_hh'
             4294  CALL_FUNCTION_1       1  '1 positional argument'
             4296  STORE_FAST               'hh'

 L.1100      4298  LOAD_GLOBAL              int
             4300  LOAD_FAST                'str_mm'
             4302  CALL_FUNCTION_1       1  '1 positional argument'
             4304  STORE_FAST               'mm'

 L.1101      4306  LOAD_FAST                'hh'
             4308  LOAD_CONST               5
             4310  COMPARE_OP               >
         4312_4314  POP_JUMP_IF_FALSE  4322  'to 4322'

 L.1102      4316  LOAD_STR                 'pm'
             4318  STORE_FAST               'remainder'
             4320  JUMP_FORWARD       4326  'to 4326'
           4322_0  COME_FROM          4312  '4312'

 L.1104      4322  LOAD_STR                 'am'
             4324  STORE_FAST               'remainder'
           4326_0  COME_FROM          4320  '4320'

 L.1105      4326  LOAD_CONST               2
             4328  STORE_FAST               'used'

 L.1106      4330  LOAD_CONST               False
             4332  STORE_FAST               'isTime'

 L.1107      4334  LOAD_FAST                'hh'
             4336  STORE_DEREF              'hr_abs'

 L.1108      4338  LOAD_FAST                'mm'
             4340  STORE_DEREF              'min_abs'
             4342  JUMP_FORWARD       4474  'to 4474'
           4344_0  COME_FROM          4286  '4286'

 L.1110      4344  LOAD_FAST                'word_next'
         4346_4348  POP_JUMP_IF_FALSE  4382  'to 4382'
             4350  LOAD_FAST                'word_next'
             4352  LOAD_STR                 'mezza'
             4354  COMPARE_OP               ==
         4356_4358  POP_JUMP_IF_FALSE  4382  'to 4382'

 L.1111      4360  LOAD_GLOBAL              int
             4362  LOAD_FAST                'str_hh'
             4364  CALL_FUNCTION_1       1  '1 positional argument'
             4366  STORE_DEREF              'hr_abs'

 L.1112      4368  LOAD_CONST               30
             4370  STORE_DEREF              'min_abs'

 L.1113      4372  LOAD_CONST               2
             4374  STORE_FAST               'used'

 L.1114      4376  LOAD_CONST               False
             4378  STORE_FAST               'isTime'
             4380  JUMP_FORWARD       4474  'to 4474'
           4382_0  COME_FROM          4356  '4356'
           4382_1  COME_FROM          4346  '4346'

 L.1115      4382  LOAD_FAST                'word_next'
         4384_4386  POP_JUMP_IF_FALSE  4424  'to 4424'
             4388  LOAD_FAST                'word_next'
             4390  LOAD_STR                 'in_punto'
             4392  COMPARE_OP               ==
         4394_4396  POP_JUMP_IF_FALSE  4424  'to 4424'

 L.1116      4398  LOAD_GLOBAL              int
             4400  LOAD_FAST                'str_hh'
             4402  CALL_FUNCTION_1       1  '1 positional argument'
             4404  STORE_DEREF              'hr_abs'

 L.1117      4406  LOAD_CONST               0
             4408  STORE_DEREF              'min_abs'

 L.1118      4410  LOAD_STR                 '0'
             4412  STORE_FAST               'str_mm'

 L.1119      4414  LOAD_CONST               2
             4416  STORE_FAST               'used'

 L.1120      4418  LOAD_CONST               False
             4420  STORE_FAST               'isTime'
             4422  JUMP_FORWARD       4474  'to 4474'
           4424_0  COME_FROM          4394  '4394'
           4424_1  COME_FROM          4384  '4384'

 L.1123      4424  LOAD_STR                 ''
             4426  STORE_FAST               'remainder'

 L.1124      4428  LOAD_GLOBAL              int
             4430  LOAD_FAST                'str_hh'
             4432  CALL_FUNCTION_1       1  '1 positional argument'
             4434  STORE_DEREF              'hr_abs'

 L.1125      4436  LOAD_GLOBAL              int
             4438  LOAD_FAST                'str_mm'
             4440  CALL_FUNCTION_1       1  '1 positional argument'
             4442  STORE_DEREF              'min_abs'

 L.1126      4444  LOAD_CONST               1
             4446  STORE_FAST               'used'

 L.1127      4448  LOAD_CONST               False
             4450  STORE_FAST               'isTime'

 L.1128      4452  LOAD_FAST                'word_prev'
             4454  LOAD_STR                 'ora'
             4456  COMPARE_OP               ==
         4458_4460  POP_JUMP_IF_FALSE  4474  'to 4474'

 L.1129      4462  LOAD_STR                 ''
             4464  LOAD_FAST                'words'
             4466  LOAD_FAST                'idx'
             4468  LOAD_CONST               1
             4470  BINARY_SUBTRACT  
             4472  STORE_SUBSCR     
           4474_0  COME_FROM          4458  '4458'
           4474_1  COME_FROM          4422  '4422'
           4474_2  COME_FROM          4380  '4380'
           4474_3  COME_FROM          4342  '4342'
           4474_4  COME_FROM          4278  '4278'
           4474_5  COME_FROM          4210  '4210'
           4474_6  COME_FROM          4142  '4142'
           4474_7  COME_FROM          4092  '4092'
           4474_8  COME_FROM          4054  '4054'

 L.1131      4474  LOAD_FAST                'time_qualifier'
             4476  LOAD_STR                 ''
             4478  COMPARE_OP               !=
         4480_4482  POP_JUMP_IF_FALSE  4532  'to 4532'

 L.1133      4484  LOAD_FAST                'str_hh'
         4486_4488  POP_JUMP_IF_FALSE  4536  'to 4536'
             4490  LOAD_GLOBAL              int
             4492  LOAD_FAST                'str_hh'
             4494  CALL_FUNCTION_1       1  '1 positional argument'
             4496  LOAD_CONST               12
             4498  COMPARE_OP               <=
         4500_4502  POP_JUMP_IF_FALSE  4536  'to 4536'

 L.1134      4504  LOAD_FAST                'time_qualifier'
             4506  LOAD_FAST                'time_qualifiers_pm'
             4508  COMPARE_OP               in
         4510_4512  POP_JUMP_IF_FALSE  4536  'to 4536'

 L.1135      4514  LOAD_GLOBAL              str
             4516  LOAD_GLOBAL              int
             4518  LOAD_FAST                'str_hh'
             4520  CALL_FUNCTION_1       1  '1 positional argument'
             4522  LOAD_CONST               12
             4524  BINARY_ADD       
             4526  CALL_FUNCTION_1       1  '1 positional argument'
             4528  STORE_FAST               'str_hh'
             4530  JUMP_FORWARD       4536  'to 4536'
           4532_0  COME_FROM          4480  '4480'

 L.1137      4532  LOAD_CONST               False
             4534  STORE_FAST               'isTime'
           4536_0  COME_FROM          4530  '4530'
           4536_1  COME_FROM          4510  '4510'
           4536_2  COME_FROM          4500  '4500'
           4536_3  COME_FROM          4486  '4486'

 L.1139      4536  LOAD_FAST                'str_hh'
         4538_4540  POP_JUMP_IF_FALSE  4550  'to 4550'
             4542  LOAD_GLOBAL              int
             4544  LOAD_FAST                'str_hh'
             4546  CALL_FUNCTION_1       1  '1 positional argument'
             4548  JUMP_FORWARD       4552  'to 4552'
           4550_0  COME_FROM          4538  '4538'
             4550  LOAD_CONST               0
           4552_0  COME_FROM          4548  '4548'
             4552  STORE_FAST               'str_hh'

 L.1140      4554  LOAD_FAST                'str_mm'
         4556_4558  POP_JUMP_IF_FALSE  4568  'to 4568'
             4560  LOAD_GLOBAL              int
             4562  LOAD_FAST                'str_mm'
             4564  CALL_FUNCTION_1       1  '1 positional argument'
             4566  JUMP_FORWARD       4570  'to 4570'
           4568_0  COME_FROM          4556  '4556'
             4568  LOAD_CONST               0
           4570_0  COME_FROM          4566  '4566'
             4570  STORE_FAST               'str_mm'

 L.1142      4572  LOAD_FAST                'remainder'
             4574  LOAD_STR                 'pm'
             4576  COMPARE_OP               ==
         4578_4580  POP_JUMP_IF_FALSE  4600  'to 4600'

 L.1143      4582  LOAD_FAST                'str_hh'
             4584  LOAD_CONST               12
             4586  COMPARE_OP               <
         4588_4590  POP_JUMP_IF_FALSE  4600  'to 4600'
             4592  LOAD_FAST                'str_hh'
             4594  LOAD_CONST               12
             4596  BINARY_ADD       
             4598  JUMP_FORWARD       4602  'to 4602'
           4600_0  COME_FROM          4588  '4588'
           4600_1  COME_FROM          4578  '4578'
             4600  LOAD_FAST                'str_hh'
           4602_0  COME_FROM          4598  '4598'
             4602  STORE_FAST               'str_hh'

 L.1144      4604  LOAD_FAST                'remainder'
             4606  LOAD_STR                 'am'
             4608  COMPARE_OP               ==
         4610_4612  POP_JUMP_IF_FALSE  4632  'to 4632'

 L.1145      4614  LOAD_FAST                'str_hh'
             4616  LOAD_CONST               12
             4618  COMPARE_OP               >=
         4620_4622  POP_JUMP_IF_FALSE  4632  'to 4632'
             4624  LOAD_FAST                'str_hh'
             4626  LOAD_CONST               12
             4628  BINARY_SUBTRACT  
             4630  JUMP_FORWARD       4634  'to 4634'
           4632_0  COME_FROM          4620  '4620'
           4632_1  COME_FROM          4610  '4610'
             4632  LOAD_FAST                'str_hh'
           4634_0  COME_FROM          4630  '4630'
             4634  STORE_FAST               'str_hh'

 L.1147      4636  LOAD_FAST                'military'
         4638_4640  POP_JUMP_IF_TRUE   4724  'to 4724'

 L.1148      4642  LOAD_FAST                'remainder'
             4644  LOAD_CONST               ('am', 'pm')
             4646  COMPARE_OP               not-in
         4648_4650  POP_JUMP_IF_FALSE  4724  'to 4724'

 L.1149      4652  LOAD_FAST                'day_specified'
         4654_4656  POP_JUMP_IF_FALSE  4668  'to 4668'
             4658  LOAD_DEREF               'day_offset'
             4660  LOAD_CONST               1
             4662  COMPARE_OP               <
         4664_4666  POP_JUMP_IF_FALSE  4724  'to 4724'
           4668_0  COME_FROM          4654  '4654'

 L.1152      4668  LOAD_FAST                'str_hh'
             4670  STORE_DEREF              'hr_abs'

 L.1153      4672  LOAD_FAST                'dateNow'
             4674  LOAD_ATTR                hour
             4676  LOAD_FAST                'str_hh'
             4678  COMPARE_OP               <
         4680_4682  POP_JUMP_IF_FALSE  4686  'to 4686'

 L.1154      4684  JUMP_FORWARD       4724  'to 4724'
           4686_0  COME_FROM          4680  '4680'

 L.1155      4686  LOAD_FAST                'dateNow'
             4688  LOAD_ATTR                hour
             4690  LOAD_FAST                'str_hh'
             4692  LOAD_CONST               12
             4694  BINARY_ADD       
             4696  COMPARE_OP               <
         4698_4700  POP_JUMP_IF_FALSE  4716  'to 4716'

 L.1156      4702  LOAD_FAST                'str_hh'
             4704  LOAD_CONST               12
             4706  INPLACE_ADD      
             4708  STORE_FAST               'str_hh'

 L.1157      4710  LOAD_FAST                'str_hh'
             4712  STORE_DEREF              'hr_abs'
             4714  JUMP_FORWARD       4724  'to 4724'
           4716_0  COME_FROM          4698  '4698'

 L.1160      4716  LOAD_DEREF               'day_offset'
             4718  LOAD_CONST               1
             4720  INPLACE_ADD      
             4722  STORE_DEREF              'day_offset'
           4724_0  COME_FROM          4714  '4714'
           4724_1  COME_FROM          4684  '4684'
           4724_2  COME_FROM          4664  '4664'
           4724_3  COME_FROM          4648  '4648'
           4724_4  COME_FROM          4638  '4638'

 L.1162      4724  LOAD_FAST                'time_qualifier'
             4726  LOAD_FAST                'time_qualifiers_pm'
             4728  COMPARE_OP               in
         4730_4732  POP_JUMP_IF_FALSE  4752  'to 4752'
             4734  LOAD_FAST                'str_hh'
             4736  LOAD_CONST               12
             4738  COMPARE_OP               <
         4740_4742  POP_JUMP_IF_FALSE  4752  'to 4752'

 L.1163      4744  LOAD_FAST                'str_hh'
             4746  LOAD_CONST               12
             4748  INPLACE_ADD      
             4750  STORE_FAST               'str_hh'
           4752_0  COME_FROM          4740  '4740'
           4752_1  COME_FROM          4730  '4730'

 L.1165      4752  LOAD_FAST                'str_hh'
             4754  LOAD_CONST               24
             4756  COMPARE_OP               >
         4758_4760  POP_JUMP_IF_TRUE   4772  'to 4772'
             4762  LOAD_FAST                'str_mm'
             4764  LOAD_CONST               59
             4766  COMPARE_OP               >
         4768_4770  POP_JUMP_IF_FALSE  4780  'to 4780'
           4772_0  COME_FROM          4758  '4758'

 L.1166      4772  LOAD_CONST               False
             4774  STORE_FAST               'isTime'

 L.1167      4776  LOAD_CONST               0
             4778  STORE_FAST               'used'
           4780_0  COME_FROM          4768  '4768'

 L.1168      4780  LOAD_FAST                'isTime'
         4782_4784  POP_JUMP_IF_FALSE  4810  'to 4810'

 L.1169      4786  LOAD_FAST                'str_hh'
             4788  LOAD_CONST               1
             4790  BINARY_MULTIPLY  
             4792  STORE_DEREF              'hr_abs'

 L.1170      4794  LOAD_FAST                'str_mm'
             4796  LOAD_CONST               1
             4798  BINARY_MULTIPLY  
             4800  STORE_DEREF              'min_abs'
           4802_0  COME_FROM          3292  '3292'

 L.1171      4802  LOAD_FAST                'used'
             4804  LOAD_CONST               1
             4806  INPLACE_ADD      
             4808  STORE_FAST               'used'
           4810_0  COME_FROM          4782  '4782'

 L.1173      4810  LOAD_DEREF               'hr_abs'
         4812_4814  JUMP_IF_TRUE_OR_POP  4818  'to 4818'
             4816  LOAD_CONST               0
           4818_0  COME_FROM          4812  '4812'
             4818  LOAD_CONST               12
             4820  COMPARE_OP               <=
         4822_4824  POP_JUMP_IF_FALSE  4860  'to 4860'
             4826  LOAD_FAST                'time_qualifier'
             4828  LOAD_STR                 'sera'
           4830_0  COME_FROM          3320  '3320'
             4830  COMPARE_OP               ==
         4832_4834  POP_JUMP_IF_TRUE   4846  'to 4846'

 L.1174      4836  LOAD_FAST                'time_qualifier'
             4838  LOAD_STR                 'pomeriggio'
             4840  COMPARE_OP               ==
         4842_4844  POP_JUMP_IF_FALSE  4860  'to 4860'
           4846_0  COME_FROM          4832  '4832'

 L.1175      4846  LOAD_DEREF               'hr_abs'
         4848_4850  JUMP_IF_TRUE_OR_POP  4854  'to 4854'
             4852  LOAD_CONST               0
           4854_0  COME_FROM          4848  '4848'
             4854  LOAD_CONST               12
             4856  BINARY_ADD       
             4858  STORE_DEREF              'hr_abs'
           4860_0  COME_FROM          4842  '4842'
           4860_1  COME_FROM          4822  '4822'
           4860_2  COME_FROM          3518  '3518'
           4860_3  COME_FROM          3504  '3504'
           4860_4  COME_FROM          3382  '3382'
           4860_5  COME_FROM          3348  '3348'
           4860_6  COME_FROM          3328  '3328'
           4860_7  COME_FROM          3222  '3222'
           4860_8  COME_FROM          3192  '3192'
           4860_9  COME_FROM          3162  '3162'
          4860_10  COME_FROM          3144  '3144'
          4860_11  COME_FROM          3112  '3112'
          4860_12  COME_FROM          3102  '3102'
          4860_13  COME_FROM          3088  '3088'
          4860_14  COME_FROM          3054  '3054'
          4860_15  COME_FROM          3036  '3036'
          4860_16  COME_FROM          3004  '3004'
          4860_17  COME_FROM          2990  '2990'
          4860_18  COME_FROM          2956  '2956'
          4860_19  COME_FROM          2936  '2936'
          4860_20  COME_FROM          2922  '2922'
          4860_21  COME_FROM          2888  '2888'
          4860_22  COME_FROM          2852  '2852'

 L.1177      4860  LOAD_FAST                'used'
             4862  LOAD_CONST               0
             4864  COMPARE_OP               >
         4866_4868  POP_JUMP_IF_FALSE  2626  'to 2626'

 L.1179      4870  SETUP_LOOP         4902  'to 4902'
             4872  LOAD_GLOBAL              range
             4874  LOAD_FAST                'used'
             4876  CALL_FUNCTION_1       1  '1 positional argument'
             4878  GET_ITER         
             4880  FOR_ITER           4900  'to 4900'
             4882  STORE_FAST               'i'

 L.1180      4884  LOAD_STR                 ''
             4886  LOAD_FAST                'words'
             4888  LOAD_FAST                'idx'
             4890  LOAD_FAST                'i'
             4892  BINARY_ADD       
             4894  STORE_SUBSCR     
         4896_4898  JUMP_BACK          4880  'to 4880'
             4900  POP_BLOCK        
           4902_0  COME_FROM_LOOP     4870  '4870'

 L.1182      4902  LOAD_FAST                'word_prev'
             4904  LOAD_STR                 'o'
             4906  COMPARE_OP               ==
         4908_4910  POP_JUMP_IF_TRUE   4922  'to 4922'
             4912  LOAD_FAST                'word_prev'
             4914  LOAD_STR                 'oh'
             4916  COMPARE_OP               ==
         4918_4920  POP_JUMP_IF_FALSE  4936  'to 4936'
           4922_0  COME_FROM          4908  '4908'

 L.1183      4922  LOAD_STR                 ''
             4924  LOAD_FAST                'words'
             4926  LOAD_FAST                'words'
             4928  LOAD_METHOD              index
             4930  LOAD_FAST                'word_prev'
             4932  CALL_METHOD_1         1  '1 positional argument'
             4934  STORE_SUBSCR     
           4936_0  COME_FROM          4918  '4918'

 L.1185      4936  LOAD_FAST                'idx'
             4938  LOAD_CONST               0
             4940  COMPARE_OP               >
         4942_4944  POP_JUMP_IF_FALSE  4968  'to 4968'
             4946  LOAD_FAST                'word_prev'
             4948  LOAD_FAST                'markers'
             4950  COMPARE_OP               in
         4952_4954  POP_JUMP_IF_FALSE  4968  'to 4968'

 L.1186      4956  LOAD_STR                 ''
             4958  LOAD_FAST                'words'
             4960  LOAD_FAST                'idx'
             4962  LOAD_CONST               1
             4964  BINARY_SUBTRACT  
             4966  STORE_SUBSCR     
           4968_0  COME_FROM          4952  '4952'
           4968_1  COME_FROM          4942  '4942'

 L.1187      4968  LOAD_FAST                'idx'
             4970  LOAD_CONST               1
             4972  COMPARE_OP               >
         4974_4976  POP_JUMP_IF_FALSE  5000  'to 5000'
             4978  LOAD_FAST                'word_prev_prev'
             4980  LOAD_FAST                'markers'
             4982  COMPARE_OP               in
         4984_4986  POP_JUMP_IF_FALSE  5000  'to 5000'

 L.1188      4988  LOAD_STR                 ''
             4990  LOAD_FAST                'words'
             4992  LOAD_FAST                'idx'
             4994  LOAD_CONST               2
             4996  BINARY_SUBTRACT  
             4998  STORE_SUBSCR     
           5000_0  COME_FROM          4984  '4984'
           5000_1  COME_FROM          4974  '4974'

 L.1190      5000  LOAD_FAST                'idx'
             5002  LOAD_FAST                'used'
             5004  LOAD_CONST               1
             5006  BINARY_SUBTRACT  
             5008  INPLACE_ADD      
             5010  STORE_FAST               'idx'

 L.1191      5012  LOAD_CONST               True
             5014  STORE_DEREF              'found'
         5016_5018  JUMP_BACK          2626  'to 2626'
             5020  POP_BLOCK        
           5022_0  COME_FROM_LOOP     2614  '2614'

 L.1194      5022  LOAD_FAST                'date_found'
         5024_5026  POP_JUMP_IF_TRUE   5032  'to 5032'

 L.1195      5028  LOAD_CONST               None
             5030  RETURN_VALUE     
           5032_0  COME_FROM          5024  '5024'

 L.1197      5032  LOAD_DEREF               'day_offset'
             5034  LOAD_CONST               False
             5036  COMPARE_OP               is
         5038_5040  POP_JUMP_IF_FALSE  5046  'to 5046'

 L.1198      5042  LOAD_CONST               0
             5044  STORE_DEREF              'day_offset'
           5046_0  COME_FROM          5038  '5038'

 L.1202      5046  LOAD_FAST                'dateNow'
             5048  LOAD_ATTR                replace
             5050  LOAD_CONST               0
             5052  LOAD_CONST               ('microsecond',)
             5054  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5056  STORE_FAST               'extracted_date'

 L.1204      5058  LOAD_DEREF               'datestr'
             5060  LOAD_STR                 ''
             5062  COMPARE_OP               !=
         5064_5066  POP_JUMP_IF_FALSE  5454  'to 5454'

 L.1205      5068  LOAD_STR                 'january'
             5070  LOAD_STR                 'february'
             5072  LOAD_STR                 'march'
             5074  LOAD_STR                 'april'
             5076  LOAD_STR                 'may'
             5078  LOAD_STR                 'june'

 L.1206      5080  LOAD_STR                 'july'
             5082  LOAD_STR                 'august'
             5084  LOAD_STR                 'september'
             5086  LOAD_STR                 'october'
             5088  LOAD_STR                 'november'

 L.1207      5090  LOAD_STR                 'december'
             5092  BUILD_LIST_12        12 
             5094  STORE_FAST               'en_months'

 L.1208      5096  LOAD_STR                 'jan'
             5098  LOAD_STR                 'feb'
             5100  LOAD_STR                 'mar'
             5102  LOAD_STR                 'apr'
             5104  LOAD_STR                 'may'
             5106  LOAD_STR                 'june'
             5108  LOAD_STR                 'july'

 L.1209      5110  LOAD_STR                 'aug'
             5112  LOAD_STR                 'sept'
             5114  LOAD_STR                 'oct'
             5116  LOAD_STR                 'nov'
             5118  LOAD_STR                 'dec'
             5120  BUILD_LIST_12        12 
             5122  STORE_FAST               'en_months_short'

 L.1211      5124  SETUP_LOOP         5164  'to 5164'
             5126  LOAD_GLOBAL              enumerate
             5128  LOAD_FAST                'en_months'
             5130  CALL_FUNCTION_1       1  '1 positional argument'
             5132  GET_ITER         
             5134  FOR_ITER           5162  'to 5162'
             5136  UNPACK_SEQUENCE_2     2 
             5138  STORE_FAST               'idx'
             5140  STORE_FAST               'en_month'

 L.1212      5142  LOAD_DEREF               'datestr'
             5144  LOAD_METHOD              replace
             5146  LOAD_FAST                'months'
             5148  LOAD_FAST                'idx'
             5150  BINARY_SUBSCR    
             5152  LOAD_FAST                'en_month'
             5154  CALL_METHOD_2         2  '2 positional arguments'
             5156  STORE_DEREF              'datestr'
         5158_5160  JUMP_BACK          5134  'to 5134'
             5162  POP_BLOCK        
           5164_0  COME_FROM_LOOP     5124  '5124'

 L.1214      5164  SETUP_LOOP         5204  'to 5204'
             5166  LOAD_GLOBAL              enumerate
             5168  LOAD_FAST                'en_months_short'
             5170  CALL_FUNCTION_1       1  '1 positional argument'
             5172  GET_ITER         
             5174  FOR_ITER           5202  'to 5202'
             5176  UNPACK_SEQUENCE_2     2 
             5178  STORE_FAST               'idx'
             5180  STORE_FAST               'en_month'

 L.1215      5182  LOAD_DEREF               'datestr'
             5184  LOAD_METHOD              replace
             5186  LOAD_FAST                'months_short'
             5188  LOAD_FAST                'idx'
             5190  BINARY_SUBSCR    
             5192  LOAD_FAST                'en_month'
             5194  CALL_METHOD_2         2  '2 positional arguments'
             5196  STORE_DEREF              'datestr'
         5198_5200  JUMP_BACK          5174  'to 5174'
             5202  POP_BLOCK        
           5204_0  COME_FROM_LOOP     5164  '5164'

 L.1217      5204  SETUP_EXCEPT       5222  'to 5222'

 L.1218      5206  LOAD_GLOBAL              datetime
             5208  LOAD_METHOD              strptime
             5210  LOAD_DEREF               'datestr'
             5212  LOAD_STR                 '%B %d'
             5214  CALL_METHOD_2         2  '2 positional arguments'
             5216  STORE_FAST               'temp'
             5218  POP_BLOCK        
             5220  JUMP_FORWARD       5256  'to 5256'
           5222_0  COME_FROM_EXCEPT   5204  '5204'

 L.1219      5222  DUP_TOP          
             5224  LOAD_GLOBAL              ValueError
             5226  COMPARE_OP               exception-match
         5228_5230  POP_JUMP_IF_FALSE  5254  'to 5254'
             5232  POP_TOP          
             5234  POP_TOP          
             5236  POP_TOP          

 L.1221      5238  LOAD_GLOBAL              datetime
             5240  LOAD_METHOD              strptime
             5242  LOAD_DEREF               'datestr'
             5244  LOAD_STR                 '%B %d %Y'
             5246  CALL_METHOD_2         2  '2 positional arguments'
             5248  STORE_FAST               'temp'
             5250  POP_EXCEPT       
             5252  JUMP_FORWARD       5256  'to 5256'
           5254_0  COME_FROM          5228  '5228'
             5254  END_FINALLY      
           5256_0  COME_FROM          5252  '5252'
           5256_1  COME_FROM          5220  '5220'

 L.1222      5256  LOAD_FAST                'extracted_date'
             5258  LOAD_ATTR                replace
             5260  LOAD_CONST               0
             5262  LOAD_CONST               0
             5264  LOAD_CONST               0
             5266  LOAD_CONST               ('hour', 'minute', 'second')
             5268  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5270  STORE_FAST               'extracted_date'

 L.1223      5272  LOAD_FAST                'has_year'
         5274_5276  POP_JUMP_IF_TRUE   5402  'to 5402'

 L.1224      5278  LOAD_FAST                'temp'
             5280  LOAD_ATTR                replace
             5282  LOAD_FAST                'extracted_date'
             5284  LOAD_ATTR                year

 L.1225      5286  LOAD_FAST                'extracted_date'
             5288  LOAD_ATTR                tzinfo
             5290  LOAD_CONST               ('year', 'tzinfo')
             5292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5294  STORE_FAST               'temp'

 L.1226      5296  LOAD_FAST                'extracted_date'
             5298  LOAD_FAST                'temp'
             5300  COMPARE_OP               <
         5302_5304  POP_JUMP_IF_FALSE  5352  'to 5352'

 L.1227      5306  LOAD_FAST                'extracted_date'
             5308  LOAD_ATTR                replace

 L.1228      5310  LOAD_GLOBAL              int
             5312  LOAD_FAST                'current_year'
             5314  CALL_FUNCTION_1       1  '1 positional argument'

 L.1229      5316  LOAD_GLOBAL              int
             5318  LOAD_FAST                'temp'
             5320  LOAD_METHOD              strftime
             5322  LOAD_STR                 '%m'
             5324  CALL_METHOD_1         1  '1 positional argument'
             5326  CALL_FUNCTION_1       1  '1 positional argument'

 L.1230      5328  LOAD_GLOBAL              int
             5330  LOAD_FAST                'temp'
             5332  LOAD_METHOD              strftime
             5334  LOAD_STR                 '%d'
             5336  CALL_METHOD_1         1  '1 positional argument'
             5338  CALL_FUNCTION_1       1  '1 positional argument'

 L.1231      5340  LOAD_FAST                'extracted_date'
             5342  LOAD_ATTR                tzinfo
             5344  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5346  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5348  STORE_FAST               'extracted_date'
             5350  JUMP_FORWARD       5400  'to 5400'
           5352_0  COME_FROM          5302  '5302'

 L.1233      5352  LOAD_FAST                'extracted_date'
             5354  LOAD_ATTR                replace

 L.1234      5356  LOAD_GLOBAL              int
             5358  LOAD_FAST                'current_year'
             5360  CALL_FUNCTION_1       1  '1 positional argument'
             5362  LOAD_CONST               1
             5364  BINARY_ADD       

 L.1235      5366  LOAD_GLOBAL              int
             5368  LOAD_FAST                'temp'
             5370  LOAD_METHOD              strftime
             5372  LOAD_STR                 '%m'
             5374  CALL_METHOD_1         1  '1 positional argument'
             5376  CALL_FUNCTION_1       1  '1 positional argument'

 L.1236      5378  LOAD_GLOBAL              int
             5380  LOAD_FAST                'temp'
             5382  LOAD_METHOD              strftime
             5384  LOAD_STR                 '%d'
             5386  CALL_METHOD_1         1  '1 positional argument'
             5388  CALL_FUNCTION_1       1  '1 positional argument'

 L.1237      5390  LOAD_FAST                'extracted_date'
             5392  LOAD_ATTR                tzinfo
             5394  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5396  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5398  STORE_FAST               'extracted_date'
           5400_0  COME_FROM          5350  '5350'
             5400  JUMP_FORWARD       5452  'to 5452'
           5402_0  COME_FROM          5274  '5274'

 L.1239      5402  LOAD_FAST                'extracted_date'
             5404  LOAD_ATTR                replace

 L.1240      5406  LOAD_GLOBAL              int
             5408  LOAD_FAST                'temp'
             5410  LOAD_METHOD              strftime
             5412  LOAD_STR                 '%Y'
             5414  CALL_METHOD_1         1  '1 positional argument'
             5416  CALL_FUNCTION_1       1  '1 positional argument'

 L.1241      5418  LOAD_GLOBAL              int
             5420  LOAD_FAST                'temp'
             5422  LOAD_METHOD              strftime
             5424  LOAD_STR                 '%m'
             5426  CALL_METHOD_1         1  '1 positional argument'
             5428  CALL_FUNCTION_1       1  '1 positional argument'

 L.1242      5430  LOAD_GLOBAL              int
             5432  LOAD_FAST                'temp'
             5434  LOAD_METHOD              strftime
             5436  LOAD_STR                 '%d'
             5438  CALL_METHOD_1         1  '1 positional argument'
             5440  CALL_FUNCTION_1       1  '1 positional argument'

 L.1243      5442  LOAD_FAST                'extracted_date'
             5444  LOAD_ATTR                tzinfo
             5446  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5448  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5450  STORE_FAST               'extracted_date'
           5452_0  COME_FROM          5400  '5400'
             5452  JUMP_FORWARD       5500  'to 5500'
           5454_0  COME_FROM          5064  '5064'

 L.1246      5454  LOAD_DEREF               'hr_offset'
             5456  LOAD_CONST               0
             5458  COMPARE_OP               ==
         5460_5462  POP_JUMP_IF_FALSE  5500  'to 5500'
             5464  LOAD_DEREF               'min_offset'
             5466  LOAD_CONST               0
             5468  COMPARE_OP               ==
         5470_5472  POP_JUMP_IF_FALSE  5500  'to 5500'
             5474  LOAD_DEREF               'sec_offset'
             5476  LOAD_CONST               0
             5478  COMPARE_OP               ==
         5480_5482  POP_JUMP_IF_FALSE  5500  'to 5500'

 L.1247      5484  LOAD_FAST                'extracted_date'
             5486  LOAD_ATTR                replace
             5488  LOAD_CONST               0
             5490  LOAD_CONST               0
             5492  LOAD_CONST               0
             5494  LOAD_CONST               ('hour', 'minute', 'second')
             5496  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5498  STORE_FAST               'extracted_date'
           5500_0  COME_FROM          5480  '5480'
           5500_1  COME_FROM          5470  '5470'
           5500_2  COME_FROM          5460  '5460'
           5500_3  COME_FROM          5452  '5452'

 L.1249      5500  LOAD_DEREF               'year_offset'
             5502  LOAD_CONST               0
             5504  COMPARE_OP               !=
         5506_5508  POP_JUMP_IF_FALSE  5524  'to 5524'

 L.1250      5510  LOAD_FAST                'extracted_date'
             5512  LOAD_GLOBAL              relativedelta
             5514  LOAD_DEREF               'year_offset'
             5516  LOAD_CONST               ('years',)
             5518  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5520  BINARY_ADD       
             5522  STORE_FAST               'extracted_date'
           5524_0  COME_FROM          5506  '5506'

 L.1251      5524  LOAD_DEREF               'month_offset'
             5526  LOAD_CONST               0
             5528  COMPARE_OP               !=
         5530_5532  POP_JUMP_IF_FALSE  5548  'to 5548'

 L.1252      5534  LOAD_FAST                'extracted_date'
             5536  LOAD_GLOBAL              relativedelta
             5538  LOAD_DEREF               'month_offset'
             5540  LOAD_CONST               ('months',)
             5542  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5544  BINARY_ADD       
             5546  STORE_FAST               'extracted_date'
           5548_0  COME_FROM          5530  '5530'

 L.1253      5548  LOAD_DEREF               'day_offset'
             5550  LOAD_CONST               0
             5552  COMPARE_OP               !=
         5554_5556  POP_JUMP_IF_FALSE  5572  'to 5572'

 L.1254      5558  LOAD_FAST                'extracted_date'
             5560  LOAD_GLOBAL              relativedelta
             5562  LOAD_DEREF               'day_offset'
             5564  LOAD_CONST               ('days',)
             5566  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5568  BINARY_ADD       
             5570  STORE_FAST               'extracted_date'
           5572_0  COME_FROM          5554  '5554'

 L.1255      5572  LOAD_DEREF               'hr_abs'
             5574  LOAD_CONST               -1
             5576  COMPARE_OP               !=
         5578_5580  POP_JUMP_IF_FALSE  5734  'to 5734'
             5582  LOAD_DEREF               'min_abs'
             5584  LOAD_CONST               -1
             5586  COMPARE_OP               !=
         5588_5590  POP_JUMP_IF_FALSE  5734  'to 5734'

 L.1258      5592  LOAD_DEREF               'hr_abs'
             5594  LOAD_CONST               None
             5596  COMPARE_OP               is
         5598_5600  POP_JUMP_IF_FALSE  5638  'to 5638'
             5602  LOAD_DEREF               'min_abs'
             5604  LOAD_CONST               None
             5606  COMPARE_OP               is
         5608_5610  POP_JUMP_IF_FALSE  5638  'to 5638'
             5612  LOAD_FAST                'default_time'
             5614  LOAD_CONST               None
             5616  COMPARE_OP               is-not
         5618_5620  POP_JUMP_IF_FALSE  5638  'to 5638'

 L.1259      5622  LOAD_FAST                'default_time'
             5624  LOAD_ATTR                hour
             5626  LOAD_FAST                'default_time'
             5628  LOAD_ATTR                minute
             5630  ROT_TWO          
             5632  STORE_DEREF              'hr_abs'
             5634  STORE_DEREF              'min_abs'
             5636  JUMP_FORWARD       5658  'to 5658'
           5638_0  COME_FROM          5618  '5618'
           5638_1  COME_FROM          5608  '5608'
           5638_2  COME_FROM          5598  '5598'

 L.1261      5638  LOAD_DEREF               'hr_abs'
         5640_5642  JUMP_IF_TRUE_OR_POP  5646  'to 5646'
             5644  LOAD_CONST               0
           5646_0  COME_FROM          5640  '5640'
             5646  STORE_DEREF              'hr_abs'

 L.1262      5648  LOAD_DEREF               'min_abs'
         5650_5652  JUMP_IF_TRUE_OR_POP  5656  'to 5656'
             5654  LOAD_CONST               0
           5656_0  COME_FROM          5650  '5650'
             5656  STORE_DEREF              'min_abs'
           5658_0  COME_FROM          5636  '5636'

 L.1264      5658  LOAD_FAST                'extracted_date'
             5660  LOAD_GLOBAL              relativedelta
             5662  LOAD_DEREF               'hr_abs'

 L.1265      5664  LOAD_DEREF               'min_abs'
             5666  LOAD_CONST               ('hours', 'minutes')
             5668  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5670  BINARY_ADD       
             5672  STORE_FAST               'extracted_date'

 L.1266      5674  LOAD_DEREF               'hr_abs'
             5676  LOAD_CONST               0
             5678  COMPARE_OP               !=
         5680_5682  POP_JUMP_IF_TRUE   5694  'to 5694'
             5684  LOAD_DEREF               'min_abs'
             5686  LOAD_CONST               0
             5688  COMPARE_OP               !=
         5690_5692  POP_JUMP_IF_FALSE  5734  'to 5734'
           5694_0  COME_FROM          5680  '5680'
             5694  LOAD_DEREF               'datestr'
             5696  LOAD_STR                 ''
             5698  COMPARE_OP               ==
         5700_5702  POP_JUMP_IF_FALSE  5734  'to 5734'

 L.1267      5704  LOAD_FAST                'day_specified'
         5706_5708  POP_JUMP_IF_TRUE   5734  'to 5734'
             5710  LOAD_FAST                'dateNow'
             5712  LOAD_FAST                'extracted_date'
             5714  COMPARE_OP               >
         5716_5718  POP_JUMP_IF_FALSE  5734  'to 5734'

 L.1268      5720  LOAD_FAST                'extracted_date'
             5722  LOAD_GLOBAL              relativedelta
             5724  LOAD_CONST               1
             5726  LOAD_CONST               ('days',)
             5728  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5730  BINARY_ADD       
             5732  STORE_FAST               'extracted_date'
           5734_0  COME_FROM          5716  '5716'
           5734_1  COME_FROM          5706  '5706'
           5734_2  COME_FROM          5700  '5700'
           5734_3  COME_FROM          5690  '5690'
           5734_4  COME_FROM          5588  '5588'
           5734_5  COME_FROM          5578  '5578'

 L.1269      5734  LOAD_DEREF               'hr_offset'
             5736  LOAD_CONST               0
             5738  COMPARE_OP               !=
         5740_5742  POP_JUMP_IF_FALSE  5758  'to 5758'

 L.1270      5744  LOAD_FAST                'extracted_date'
             5746  LOAD_GLOBAL              relativedelta
             5748  LOAD_DEREF               'hr_offset'
             5750  LOAD_CONST               ('hours',)
             5752  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5754  BINARY_ADD       
             5756  STORE_FAST               'extracted_date'
           5758_0  COME_FROM          5740  '5740'

 L.1271      5758  LOAD_DEREF               'min_offset'
             5760  LOAD_CONST               0
             5762  COMPARE_OP               !=
         5764_5766  POP_JUMP_IF_FALSE  5782  'to 5782'

 L.1272      5768  LOAD_FAST                'extracted_date'
             5770  LOAD_GLOBAL              relativedelta
             5772  LOAD_DEREF               'min_offset'
             5774  LOAD_CONST               ('minutes',)
             5776  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5778  BINARY_ADD       
             5780  STORE_FAST               'extracted_date'
           5782_0  COME_FROM          5764  '5764'

 L.1273      5782  LOAD_DEREF               'sec_offset'
             5784  LOAD_CONST               0
             5786  COMPARE_OP               !=
         5788_5790  POP_JUMP_IF_FALSE  5806  'to 5806'

 L.1274      5792  LOAD_FAST                'extracted_date'
             5794  LOAD_GLOBAL              relativedelta
             5796  LOAD_DEREF               'sec_offset'
             5798  LOAD_CONST               ('seconds',)
             5800  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5802  BINARY_ADD       
             5804  STORE_FAST               'extracted_date'
           5806_0  COME_FROM          5788  '5788'

 L.1276      5806  LOAD_CLOSURE             'noise_words_2'
             5808  BUILD_TUPLE_1         1 
             5810  LOAD_LISTCOMP            '<code_object <listcomp>>'
             5812  LOAD_STR                 'extract_datetime_it.<locals>.<listcomp>'
             5814  MAKE_FUNCTION_8          'closure'
             5816  LOAD_FAST                'words'
             5818  GET_ITER         
             5820  CALL_FUNCTION_1       1  '1 positional argument'
             5822  STORE_FAST               'words'

 L.1277      5824  LOAD_LISTCOMP            '<code_object <listcomp>>'
             5826  LOAD_STR                 'extract_datetime_it.<locals>.<listcomp>'
             5828  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             5830  LOAD_FAST                'words'
             5832  GET_ITER         
             5834  CALL_FUNCTION_1       1  '1 positional argument'
             5836  STORE_FAST               'words'

 L.1278      5838  LOAD_STR                 ' '
             5840  LOAD_METHOD              join
             5842  LOAD_FAST                'words'
             5844  CALL_METHOD_1         1  '1 positional argument'
             5846  STORE_FAST               'result_str'

 L.1280      5848  LOAD_FAST                'extracted_date'
             5850  LOAD_FAST                'result_str'
             5852  BUILD_LIST_2          2 
             5854  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1962_1


def get_gender_it--- This code section failed: ---

 L.1292         0  LOAD_CONST               None
                2  STORE_FAST               'gender'

 L.1293         4  LOAD_FAST                'raw_string'
                6  LOAD_METHOD              split
                8  LOAD_STR                 ' '
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'words'

 L.1294        14  SETUP_LOOP           74  'to 74'
               16  LOAD_GLOBAL              enumerate
               18  LOAD_FAST                'words'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  GET_ITER         
             24_0  COME_FROM            46  '46'
             24_1  COME_FROM            38  '38'
               24  FOR_ITER             72  'to 72'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'idx'
               30  STORE_FAST               'w'

 L.1295        32  LOAD_FAST                'w'
               34  LOAD_FAST                'word'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    24  'to 24'
               40  LOAD_FAST                'idx'
               42  LOAD_CONST               0
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    24  'to 24'

 L.1296        48  LOAD_FAST                'words'
               50  LOAD_FAST                'idx'
               52  LOAD_CONST               1
               54  BINARY_SUBTRACT  
               56  BINARY_SUBSCR    
               58  STORE_FAST               'previous'

 L.1297        60  LOAD_GLOBAL              get_gender_it
               62  LOAD_FAST                'previous'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  STORE_FAST               'gender'

 L.1298        68  BREAK_LOOP       
               70  JUMP_BACK            24  'to 24'
               72  POP_BLOCK        
             74_0  COME_FROM_LOOP       14  '14'

 L.1300        74  LOAD_FAST                'gender'
               76  POP_JUMP_IF_TRUE    158  'to 158'

 L.1301        78  LOAD_FAST                'word'
               80  LOAD_CONST               -1
               82  BINARY_SUBSCR    
               84  LOAD_STR                 'a'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE    102  'to 102'
               90  LOAD_FAST                'word'
               92  LOAD_CONST               -1
               94  BINARY_SUBSCR    
               96  LOAD_STR                 'e'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   106  'to 106'
            102_0  COME_FROM            88  '88'

 L.1302       102  LOAD_STR                 'f'
              104  STORE_FAST               'gender'
            106_0  COME_FROM           100  '100'

 L.1303       106  LOAD_FAST                'word'
              108  LOAD_CONST               -1
              110  BINARY_SUBSCR    
              112  LOAD_STR                 'o'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    154  'to 154'
              118  LOAD_FAST                'word'
              120  LOAD_CONST               -1
              122  BINARY_SUBSCR    
              124  LOAD_STR                 'n'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_TRUE    154  'to 154'

 L.1304       130  LOAD_FAST                'word'
              132  LOAD_CONST               -1
              134  BINARY_SUBSCR    
              136  LOAD_STR                 'l'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_TRUE    154  'to 154'
              142  LOAD_FAST                'word'
              144  LOAD_CONST               -1
              146  BINARY_SUBSCR    
              148  LOAD_STR                 'i'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   158  'to 158'
            154_0  COME_FROM           140  '140'
            154_1  COME_FROM           128  '128'
            154_2  COME_FROM           116  '116'

 L.1305       154  LOAD_STR                 'm'
              156  STORE_FAST               'gender'
            158_0  COME_FROM           152  '152'
            158_1  COME_FROM            76  '76'

 L.1307       158  LOAD_FAST                'gender'
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 158_0


def extract_numbers_it(text, short_scale=False, ordinals=False):
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
    return extract_numbers_generic(text, pronounce_number_it, extractnumber_it, short_scale=short_scale,
      ordinals=ordinals)