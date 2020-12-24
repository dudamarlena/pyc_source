# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_en.py
# Compiled at: 2020-03-20 12:49:10
# Size of source mod 2**32: 58717 bytes
from datetime import datetime, timedelta
import dateutil.relativedelta as relativedelta
from lingua_franca.lang.parse_common import is_numeric, look_for_fractions, invert_dict, ReplaceableNumber, partition_list, tokenize, Token, Normalizer
from lingua_franca.lang.common_data_en import _ARTICLES_EN, _NUM_STRING_EN, _LONG_ORDINAL_EN, _LONG_SCALE_EN, _SHORT_SCALE_EN, _SHORT_ORDINAL_EN
import re, json
from lingua_franca import resolve_resource_file
from lingua_franca.time import now_local

def generate_plurals_en(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    if isinstance(originals, dict):
        return {key + 's':value for key, value in originals.items()}
    return {value + 's' for value in originals}


_NEGATIVES = {
 'negative', 'minus'}
_SUMS = {
 'twenty', '20', 'thirty', '30', 'forty', '40', 'fifty', '50',
 'sixty', '60', 'seventy', '70', 'eighty', '80', 'ninety', '90'}
_MULTIPLIES_LONG_SCALE_EN = set(_LONG_SCALE_EN.values()) | generate_plurals_en(_LONG_SCALE_EN.values())
_MULTIPLIES_SHORT_SCALE_EN = set(_SHORT_SCALE_EN.values()) | generate_plurals_en(_SHORT_SCALE_EN.values())
_FRACTION_MARKER = {
 'and'}
_DECIMAL_MARKER = {
 'point', 'dot'}
_STRING_NUM_EN = invert_dict(_NUM_STRING_EN)
_STRING_NUM_EN.update(generate_plurals_en(_STRING_NUM_EN))
_STRING_NUM_EN.update({'half':0.5, 
 'halves':0.5, 
 'couple':2})
_STRING_SHORT_ORDINAL_EN = invert_dict(_SHORT_ORDINAL_EN)
_STRING_LONG_ORDINAL_EN = invert_dict(_LONG_ORDINAL_EN)

def _convert_words_to_numbers_en(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: True if short scale numbers should be used.
        ordinals boolean: True if ordinals (e.g. first, second, third) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.

    """
    text = text.lower()
    tokens = tokenize(text)
    numbers_to_replace = _extract_numbers_with_text_en(tokens, short_scale, ordinals)
    numbers_to_replace.sort(key=(lambda number: number.start_index))
    results = []
    for token in tokens:
        if numbers_to_replace:
            if token.index < numbers_to_replace[0].start_index:
                results.append(token.word)
        elif numbers_to_replace and token.index == numbers_to_replace[0].start_index:
            results.append(str(numbers_to_replace[0].value))
        if numbers_to_replace and token.index == numbers_to_replace[0].end_index:
            numbers_to_replace.pop(0)

    return ' '.join(results)


def _extract_numbers_with_text_en(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (first, second, third, etc) should
                       be parsed.
        fractional_numbers bool: True if we should look for fractions and
                                 decimals.

    Returns:
        [ReplaceableNumber]: A list of tuples, each containing a number and a
                         string.

    """
    placeholder = '<placeholder>'
    results = []
    while True:
        to_replace = _extract_number_with_text_en(tokens, short_scale, ordinals, fractional_numbers)
        if not to_replace:
            break
        results.append(to_replace)
        tokens = [t if (to_replace.start_index <= t.index <= to_replace.end_index) else (Token(placeholder, t.index)) for t in tokens]

    results.sort(key=(lambda n: n.start_index))
    return results


def _extract_number_with_text_en(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = _extract_number_with_text_en_helper(tokens, short_scale, ordinals, fractional_numbers)
    while tokens and tokens[0].word in _ARTICLES_EN:
        tokens.pop(0)

    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_en_helper(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """
    Helper for _extract_number_with_text_en.

    This contains the real logic for parsing, but produces
    a result that needs a little cleaning (specific, it may
    contain leading articles that can be trimmed off).

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:

    Returns:
        int or float, [Tokens]

    """
    if fractional_numbers:
        fraction, fraction_text = _extract_fraction_with_text_en(tokens, short_scale, ordinals)
        if fraction:
            return (
             fraction, fraction_text)
        decimal, decimal_text = _extract_decimal_with_text_en(tokens, short_scale, ordinals)
        if decimal:
            return (
             decimal, decimal_text)
    return _extract_whole_number_with_text_en(tokens, short_scale, ordinals)


def _extract_fraction_with_text_en(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string.

    This function handles text such as '2 and 3/4'. Note that "one half" or
    similar will be parsed by the whole number function.

    Args:
        tokens [Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.

    """
    for c in _FRACTION_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)
        if len(partitions) == 3:
            numbers1 = _extract_numbers_with_text_en((partitions[0]), short_scale, ordinals,
              fractional_numbers=False)
            numbers2 = _extract_numbers_with_text_en((partitions[2]), short_scale, ordinals,
              fractional_numbers=True)
            return numbers1 and numbers2 or (None, None)
            num1 = numbers1[(-1)]
            num2 = numbers2[0]
            if num1.value >= 1:
                if 0 < num2.value < 1:
                    return (
                     num1.value + num2.value,
                     num1.tokens + partitions[1] + num2.tokens)

    return (None, None)


def _extract_decimal_with_text_en(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extractnumber_en, it also depends on
        extractnumber_en, to parse out the components of the decimal.

        This does not currently handle things like:
            number dot number number number

    Args:
        tokens [Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.

    """
    for c in _DECIMAL_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)
        if len(partitions) == 3:
            numbers1 = _extract_numbers_with_text_en((partitions[0]), short_scale, ordinals,
              fractional_numbers=False)
            numbers2 = _extract_numbers_with_text_en((partitions[2]), short_scale, ordinals,
              fractional_numbers=False)
            return numbers1 and numbers2 or (None, None)
            number = numbers1[(-1)]
            decimal = numbers2[0]
            if '.' not in str(decimal.text):
                return (
                 number.value + float('0.' + str(decimal.value)),
                 number.tokens + partitions[1] + decimal.tokens)

    return (None, None)


def _extract_whole_number_with_text_en(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions. This is
    generally whole numbers. Note that phrases such as "one half" will be
    handled by this function, while "one and a half" are handled by the
    fraction function.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    multiplies, string_num_ordinal, string_num_scale = _initialize_number_data(short_scale)
    number_words = []
    val = False
    prev_val = None
    next_val = None
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue
        word = token.word
        if word in _ARTICLES_EN or word in _NEGATIVES:
            number_words.append(token)
            continue
        prev_word = tokens[(idx - 1)].word if idx > 0 else ''
        next_word = tokens[(idx + 1)].word if idx + 1 < len(tokens) else ''
        if not is_numeric(word[:-2]) or word.endswith('st') or word.endswith('nd') or word.endswith('rd') or word.endswith('th'):
            word = word[:-2]
            if next_word == 'one':
                tokens[idx + 1] = Token('', idx)
                next_word = ''
            if word not in string_num_scale and word not in _STRING_NUM_EN and word not in _SUMS and word not in multiplies:
                if ordinals and not word in string_num_ordinal or is_numeric(word) or isFractional_en(word, short_scale=short_scale) or look_for_fractions(word.split('/')):
                    words_only = [token.word for token in number_words]
                    if number_words:
                        if not all([w in _ARTICLES_EN | _NEGATIVES for w in words_only]):
                            break
                        else:
                            number_words = []
                            continue
                    else:
                        if not (word not in multiplies and prev_word not in multiplies and prev_word not in _SUMS):
                            if prev_word not in _NEGATIVES and prev_word not in _ARTICLES_EN:
                                number_words = [
                                 token]
                            else:
                                if prev_word in _SUMS and word in _SUMS:
                                    number_words = [
                                     token]
                                else:
                                    number_words.append(token)
                        if is_numeric(word):
                            if word.isdigit():
                                val = int(word)
                            else:
                                val = float(word)
                            current_val = val
                    if word in _STRING_NUM_EN:
                        val = _STRING_NUM_EN.get(word)
                        current_val = val
                    else:
                        if word in string_num_scale:
                            val = string_num_scale.get(word)
                            current_val = val
                        else:
                            if ordinals:
                                if word in string_num_ordinal:
                                    val = string_num_ordinal[word]
                                    current_val = val
                                if ordinals:
                                    if prev_word in string_num_ordinal:
                                        if val is 1:
                                            val = prev_val
                                if not (prev_word in _SUMS and val and val < 10):
                                    if all([
                                     prev_word in multiplies,
                                     val < prev_val if prev_val else False]):
                                        val = prev_val + val
                                    if word in multiplies:
                                        if not prev_val:
                                            prev_val = 1
                                        val = prev_val * val
                                if val is False:
                                    val = isFractional_en(word, short_scale=short_scale)
                                    current_val = val
                                if not ordinals:
                                    next_val = isFractional_en(next_word, short_scale=short_scale)
                                    if next_val:
                                        if not val:
                                            val = 1
                                        val = val * next_val
                                        number_words.append(tokens[(idx + 1)])
                            elif val:
                                if prev_word and prev_word in _NEGATIVES:
                                    val = 0 - val
                    if not val:
                        aPieces = word.split('/')
                        if look_for_fractions(aPieces):
                            val = float(aPieces[0]) / float(aPieces[1])
                            current_val = val
        else:
            if all([
             prev_word in _SUMS,
             word not in _SUMS,
             word not in multiplies,
             current_val >= 10]):
                number_words.pop()
                val = prev_val
                break
            prev_val = val
        if word in multiplies:
            if next_word not in multiplies:
                time_to_sum = True
                for other_token in tokens[idx + 1:]:
                    if other_token.word in multiplies:
                        if string_num_scale[other_token.word] >= current_val:
                            time_to_sum = False
                        else:
                            continue
                    if not time_to_sum:
                        break

                if time_to_sum:
                    to_sum.append(val)
                    val = 0
                    prev_val = 0

    if val is not None:
        if to_sum:
            val += sum(to_sum)
    return (
     val, number_words)


def _initialize_number_data(short_scale):
    """
    Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    multiplies = _MULTIPLIES_SHORT_SCALE_EN if short_scale else _MULTIPLIES_LONG_SCALE_EN
    string_num_ordinal_en = _STRING_SHORT_ORDINAL_EN if short_scale else _STRING_LONG_ORDINAL_EN
    string_num_scale_en = _SHORT_SCALE_EN if short_scale else _LONG_SCALE_EN
    string_num_scale_en = invert_dict(string_num_scale_en)
    string_num_scale_en.update(generate_plurals_en(string_num_scale_en))
    return (multiplies, string_num_ordinal_en, string_num_scale_en)


def extractnumber_en(text, short_scale=True, ordinals=False):
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
    return _extract_number_with_text_en(tokenize(text.lower()), short_scale, ordinals).value


def extract_duration_en(text):
    """
    Convert an english phrase into a number of seconds

    Convert things like:
        "10 minute"
        "2 and a half hours"
        "3 days 8 hours 10 minutes and 49 seconds"
    into an int, representing the total number of seconds.

    The words used in the duration will be consumed, and
    the remainder returned.

    As an example, "set a timer for 5 minutes" would return
    (300, "set a timer for").

    Args:
        text (str): string containing a duration

    Returns:
        (timedelta, str):
                    A tuple containing the duration and the remaining text
                    not consumed in the parsing. The first value will
                    be None if no duration is found. The text returned
                    will have whitespace stripped from the ends.
    """
    if not text:
        return
    time_units = {'microseconds':None,  'milliseconds':None, 
     'seconds':None, 
     'minutes':None, 
     'hours':None, 
     'days':None, 
     'weeks':None}
    pattern = '(?P<value>\\d+(?:\\.?\\d+)?)(?:\\s+|\\-){unit}s?'
    text = _convert_words_to_numbers_en(text)
    for unit in time_units:
        unit_pattern = pattern.format(unit=(unit[:-1]))
        matches = re.findall(unit_pattern, text)
        value = sum(map(float, matches))
        time_units[unit] = value
        text = re.sub(unit_pattern, '', text)

    text = text.strip()
    duration = timedelta(**time_units) if any(time_units.values()) else None
    return (
     duration, text)


def month_to_int_en(month):
    if isinstance(month, int) or isinstance(month, float):
        return int(month)
    if isinstance(month, str):
        month = month.lower()
        if month.startswith('jan'):
            return 1
        if month.startswith('feb'):
            return 2
        if month.startswith('mar'):
            return 3
        if month.startswith('apr'):
            return 4
        if month.startswith('may'):
            return 5
        if month.startswith('jun'):
            return 6
        if month.startswith('jul'):
            return 7
        if month.startswith('aug'):
            return 8
        if month.startswith('sep'):
            return 9
        if month.startswith('oct'):
            return 10
        if month.startswith('nov'):
            return 11
        if month.startswith('dec'):
            return 12


def extract_datetime_en--- This code section failed: ---

 L. 705         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_en.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 729         8  LOAD_CLOSURE             'datestr'
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
               32  LOAD_STR                 'extract_datetime_en.<locals>.date_found'
               34  MAKE_FUNCTION_8          'closure'
               36  STORE_FAST               'date_found'

 L. 739        38  LOAD_FAST                'string'
               40  LOAD_STR                 ''
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  LOAD_FAST                'dateNow'
               48  POP_JUMP_IF_TRUE     54  'to 54'
             50_0  COME_FROM            44  '44'

 L. 740        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 742        54  LOAD_CONST               False
               56  STORE_DEREF              'found'

 L. 743        58  LOAD_CONST               False
               60  STORE_FAST               'daySpecified'

 L. 744        62  LOAD_CONST               False
               64  STORE_DEREF              'dayOffset'

 L. 745        66  LOAD_CONST               0
               68  STORE_DEREF              'monthOffset'

 L. 746        70  LOAD_CONST               0
               72  STORE_DEREF              'yearOffset'

 L. 747        74  LOAD_FAST                'dateNow'
               76  LOAD_METHOD              strftime
               78  LOAD_STR                 '%w'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  STORE_FAST               'today'

 L. 748        84  LOAD_FAST                'dateNow'
               86  LOAD_METHOD              strftime
               88  LOAD_STR                 '%Y'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               'currentYear'

 L. 749        94  LOAD_CONST               False
               96  STORE_FAST               'fromFlag'

 L. 750        98  LOAD_STR                 ''
              100  STORE_DEREF              'datestr'

 L. 751       102  LOAD_CONST               False
              104  STORE_FAST               'hasYear'

 L. 752       106  LOAD_STR                 ''
              108  STORE_FAST               'timeQualifier'

 L. 754       110  LOAD_STR                 'morning'
              112  BUILD_LIST_1          1 
              114  STORE_FAST               'timeQualifiersAM'

 L. 755       116  LOAD_STR                 'afternoon'
              118  LOAD_STR                 'evening'
              120  LOAD_STR                 'night'
              122  LOAD_STR                 'tonight'
              124  BUILD_LIST_4          4 
              126  STORE_FAST               'timeQualifiersPM'

 L. 756       128  LOAD_GLOBAL              set
              130  LOAD_FAST                'timeQualifiersAM'
              132  LOAD_FAST                'timeQualifiersPM'
              134  BINARY_ADD       
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  STORE_FAST               'timeQualifiersList'

 L. 757       140  LOAD_STR                 'at'
              142  LOAD_STR                 'in'
              144  LOAD_STR                 'on'
              146  LOAD_STR                 'by'
              148  LOAD_STR                 'this'
              150  LOAD_STR                 'around'
              152  LOAD_STR                 'for'
              154  LOAD_STR                 'of'
              156  LOAD_STR                 'within'
              158  BUILD_LIST_9          9 
              160  STORE_FAST               'markers'

 L. 758       162  LOAD_STR                 'monday'
              164  LOAD_STR                 'tuesday'
              166  LOAD_STR                 'wednesday'

 L. 759       168  LOAD_STR                 'thursday'
              170  LOAD_STR                 'friday'
              172  LOAD_STR                 'saturday'
              174  LOAD_STR                 'sunday'
              176  BUILD_LIST_7          7 
              178  STORE_FAST               'days'

 L. 760       180  LOAD_STR                 'january'
              182  LOAD_STR                 'february'
              184  LOAD_STR                 'march'
              186  LOAD_STR                 'april'
              188  LOAD_STR                 'may'
              190  LOAD_STR                 'june'

 L. 761       192  LOAD_STR                 'july'
              194  LOAD_STR                 'august'
              196  LOAD_STR                 'september'
              198  LOAD_STR                 'october'
              200  LOAD_STR                 'november'

 L. 762       202  LOAD_STR                 'december'
              204  BUILD_LIST_12        12 
              206  STORE_FAST               'months'

 L. 763       208  LOAD_FAST                'days'
              210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'extract_datetime_en.<locals>.<listcomp>'
              214  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              216  LOAD_FAST                'days'
              218  GET_ITER         
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  BINARY_ADD       
              224  LOAD_STR                 'weekend'
              226  LOAD_STR                 'weekday'

 L. 764       228  LOAD_STR                 'weekends'
              230  LOAD_STR                 'weekdays'
              232  BUILD_LIST_4          4 
              234  BINARY_ADD       
              236  STORE_FAST               'recur_markers'

 L. 765       238  LOAD_STR                 'jan'
              240  LOAD_STR                 'feb'
              242  LOAD_STR                 'mar'
              244  LOAD_STR                 'apr'
              246  LOAD_STR                 'may'
              248  LOAD_STR                 'june'
              250  LOAD_STR                 'july'
              252  LOAD_STR                 'aug'

 L. 766       254  LOAD_STR                 'sept'
              256  LOAD_STR                 'oct'
              258  LOAD_STR                 'nov'
              260  LOAD_STR                 'dec'
              262  BUILD_LIST_12        12 
              264  STORE_FAST               'monthsShort'

 L. 767       266  LOAD_STR                 'decade'
              268  LOAD_STR                 'century'
              270  LOAD_STR                 'millennium'
              272  BUILD_LIST_3          3 
              274  STORE_FAST               'year_multiples'

 L. 768       276  LOAD_STR                 'weeks'
              278  LOAD_STR                 'months'
              280  LOAD_STR                 'years'
              282  BUILD_LIST_3          3 
              284  STORE_FAST               'day_multiples'

 L. 770       286  LOAD_FAST                'clean_string'
              288  LOAD_FAST                'string'
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  STORE_FAST               'words'

 L. 772   294_296  SETUP_LOOP         2664  'to 2664'
              298  LOAD_GLOBAL              enumerate
              300  LOAD_FAST                'words'
              302  CALL_FUNCTION_1       1  '1 positional argument'
              304  GET_ITER         
            306_0  COME_FROM          2520  '2520'
          306_308  FOR_ITER           2662  'to 2662'
              310  UNPACK_SEQUENCE_2     2 
              312  STORE_FAST               'idx'
              314  STORE_FAST               'word'

 L. 773       316  LOAD_FAST                'word'
              318  LOAD_STR                 ''
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   330  'to 330'

 L. 774   326_328  CONTINUE            306  'to 306'
            330_0  COME_FROM           322  '322'

 L. 775       330  LOAD_FAST                'idx'
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

 L. 776       356  LOAD_FAST                'idx'
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

 L. 777       382  LOAD_FAST                'idx'
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

 L. 778       416  LOAD_FAST                'idx'
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

 L. 781       450  LOAD_FAST                'word'
              452  LOAD_METHOD              rstrip
              454  LOAD_STR                 's'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  STORE_FAST               'word'

 L. 782       460  LOAD_FAST                'idx'
              462  STORE_FAST               'start'

 L. 783       464  LOAD_CONST               0
              466  STORE_FAST               'used'

 L. 785       468  LOAD_FAST                'word'
              470  LOAD_STR                 'ago'
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   498  'to 498'
              478  LOAD_DEREF               'dayOffset'
          480_482  POP_JUMP_IF_FALSE   498  'to 498'

 L. 786       484  LOAD_DEREF               'dayOffset'
              486  UNARY_NEGATIVE   
              488  STORE_DEREF              'dayOffset'

 L. 787       490  LOAD_FAST                'used'
              492  LOAD_CONST               1
              494  INPLACE_ADD      
              496  STORE_FAST               'used'
            498_0  COME_FROM           480  '480'
            498_1  COME_FROM           474  '474'

 L. 788       498  LOAD_FAST                'word'
              500  LOAD_STR                 'now'
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   570  'to 570'
              508  LOAD_DEREF               'datestr'
          510_512  POP_JUMP_IF_TRUE    570  'to 570'

 L. 789       514  LOAD_STR                 ' '
              516  LOAD_METHOD              join
              518  LOAD_FAST                'words'
              520  LOAD_FAST                'idx'
              522  LOAD_CONST               1
              524  BINARY_ADD       
              526  LOAD_CONST               None
              528  BUILD_SLICE_2         2 
              530  BINARY_SUBSCR    
              532  CALL_METHOD_1         1  '1 positional argument'
              534  STORE_FAST               'resultStr'

 L. 790       536  LOAD_STR                 ' '
              538  LOAD_METHOD              join
              540  LOAD_FAST                'resultStr'
              542  LOAD_METHOD              split
              544  CALL_METHOD_0         0  '0 positional arguments'
              546  CALL_METHOD_1         1  '1 positional argument'
              548  STORE_FAST               'resultStr'

 L. 791       550  LOAD_FAST                'dateNow'
              552  LOAD_ATTR                replace
              554  LOAD_CONST               0
              556  LOAD_CONST               ('microsecond',)
              558  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              560  STORE_FAST               'extractedDate'

 L. 792       562  LOAD_FAST                'extractedDate'
              564  LOAD_FAST                'resultStr'
              566  BUILD_LIST_2          2 
              568  RETURN_VALUE     
            570_0  COME_FROM           510  '510'
            570_1  COME_FROM           504  '504'

 L. 793       570  LOAD_FAST                'wordNext'
              572  LOAD_FAST                'year_multiples'
              574  COMPARE_OP               in
          576_578  POP_JUMP_IF_FALSE   690  'to 690'

 L. 794       580  LOAD_CONST               None
              582  STORE_FAST               'multiplier'

 L. 795       584  LOAD_GLOBAL              is_numeric
              586  LOAD_FAST                'word'
              588  CALL_FUNCTION_1       1  '1 positional argument'
          590_592  POP_JUMP_IF_FALSE   602  'to 602'

 L. 796       594  LOAD_GLOBAL              extractnumber_en
              596  LOAD_FAST                'word'
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  STORE_FAST               'multiplier'
            602_0  COME_FROM           590  '590'

 L. 797       602  LOAD_FAST                'multiplier'
          604_606  JUMP_IF_TRUE_OR_POP   610  'to 610'
              608  LOAD_CONST               1
            610_0  COME_FROM           604  '604'
              610  STORE_FAST               'multiplier'

 L. 798       612  LOAD_GLOBAL              int
              614  LOAD_FAST                'multiplier'
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  STORE_FAST               'multiplier'

 L. 799       620  LOAD_FAST                'used'
              622  LOAD_CONST               2
              624  INPLACE_ADD      
              626  STORE_FAST               'used'

 L. 800       628  LOAD_FAST                'wordNext'
              630  LOAD_STR                 'decade'
              632  COMPARE_OP               ==
          634_636  POP_JUMP_IF_FALSE   648  'to 648'

 L. 801       638  LOAD_FAST                'multiplier'
              640  LOAD_CONST               10
              642  BINARY_MULTIPLY  
              644  STORE_DEREF              'yearOffset'
              646  JUMP_FORWARD       2152  'to 2152'
            648_0  COME_FROM           634  '634'

 L. 802       648  LOAD_FAST                'wordNext'
              650  LOAD_STR                 'century'
              652  COMPARE_OP               ==
          654_656  POP_JUMP_IF_FALSE   668  'to 668'

 L. 803       658  LOAD_FAST                'multiplier'
              660  LOAD_CONST               100
              662  BINARY_MULTIPLY  
              664  STORE_DEREF              'yearOffset'
              666  JUMP_FORWARD       2152  'to 2152'
            668_0  COME_FROM           654  '654'

 L. 804       668  LOAD_FAST                'wordNext'
              670  LOAD_STR                 'millennium'
              672  COMPARE_OP               ==
          674_676  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 805       678  LOAD_FAST                'multiplier'
              680  LOAD_CONST               1000
              682  BINARY_MULTIPLY  
              684  STORE_DEREF              'yearOffset'
          686_688  JUMP_FORWARD       2152  'to 2152'
            690_0  COME_FROM           576  '576'

 L. 807       690  LOAD_FAST                'word'
              692  LOAD_STR                 '2'
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   794  'to 794'
              700  LOAD_FAST                'wordNext'
              702  LOAD_STR                 'of'
              704  COMPARE_OP               ==
          706_708  POP_JUMP_IF_FALSE   794  'to 794'

 L. 808       710  LOAD_FAST                'wordNextNext'
              712  LOAD_FAST                'year_multiples'
              714  COMPARE_OP               in
          716_718  POP_JUMP_IF_FALSE   794  'to 794'

 L. 809       720  LOAD_CONST               2
              722  STORE_FAST               'multiplier'

 L. 810       724  LOAD_FAST                'used'
              726  LOAD_CONST               3
              728  INPLACE_ADD      
              730  STORE_FAST               'used'

 L. 811       732  LOAD_FAST                'wordNextNext'
              734  LOAD_STR                 'decade'
              736  COMPARE_OP               ==
          738_740  POP_JUMP_IF_FALSE   752  'to 752'

 L. 812       742  LOAD_FAST                'multiplier'
              744  LOAD_CONST               10
              746  BINARY_MULTIPLY  
              748  STORE_DEREF              'yearOffset'
              750  JUMP_FORWARD       2152  'to 2152'
            752_0  COME_FROM           738  '738'

 L. 813       752  LOAD_FAST                'wordNextNext'
              754  LOAD_STR                 'century'
              756  COMPARE_OP               ==
          758_760  POP_JUMP_IF_FALSE   772  'to 772'

 L. 814       762  LOAD_FAST                'multiplier'
              764  LOAD_CONST               100
              766  BINARY_MULTIPLY  
              768  STORE_DEREF              'yearOffset'
              770  JUMP_FORWARD       2152  'to 2152'
            772_0  COME_FROM           758  '758'

 L. 815       772  LOAD_FAST                'wordNextNext'
              774  LOAD_STR                 'millennium'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 816       782  LOAD_FAST                'multiplier'
              784  LOAD_CONST               1000
              786  BINARY_MULTIPLY  
              788  STORE_DEREF              'yearOffset'
          790_792  JUMP_FORWARD       2152  'to 2152'
            794_0  COME_FROM           716  '716'
            794_1  COME_FROM           706  '706'
            794_2  COME_FROM           696  '696'

 L. 817       794  LOAD_FAST                'word'
              796  LOAD_STR                 '2'
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   890  'to 890'
              804  LOAD_FAST                'wordNext'
              806  LOAD_STR                 'of'
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   890  'to 890'

 L. 818       814  LOAD_FAST                'wordNextNext'
              816  LOAD_FAST                'day_multiples'
              818  COMPARE_OP               in
          820_822  POP_JUMP_IF_FALSE   890  'to 890'

 L. 819       824  LOAD_CONST               2
              826  STORE_FAST               'multiplier'

 L. 820       828  LOAD_FAST                'used'
              830  LOAD_CONST               3
              832  INPLACE_ADD      
              834  STORE_FAST               'used'

 L. 821       836  LOAD_FAST                'wordNextNext'
              838  LOAD_STR                 'years'
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE   852  'to 852'

 L. 822       846  LOAD_FAST                'multiplier'
              848  STORE_DEREF              'yearOffset'
              850  JUMP_FORWARD       2152  'to 2152'
            852_0  COME_FROM           842  '842'

 L. 823       852  LOAD_FAST                'wordNextNext'
              854  LOAD_STR                 'months'
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   868  'to 868'

 L. 824       862  LOAD_FAST                'multiplier'
              864  STORE_DEREF              'monthOffset'
              866  JUMP_FORWARD       2152  'to 2152'
            868_0  COME_FROM           858  '858'

 L. 825       868  LOAD_FAST                'wordNextNext'
              870  LOAD_STR                 'weeks'
              872  COMPARE_OP               ==
          874_876  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 826       878  LOAD_FAST                'multiplier'
              880  LOAD_CONST               7
              882  BINARY_MULTIPLY  
              884  STORE_DEREF              'dayOffset'
          886_888  JUMP_FORWARD       2152  'to 2152'
            890_0  COME_FROM           820  '820'
            890_1  COME_FROM           810  '810'
            890_2  COME_FROM           800  '800'

 L. 827       890  LOAD_FAST                'word'
              892  LOAD_FAST                'timeQualifiersList'
              894  COMPARE_OP               in
          896_898  POP_JUMP_IF_FALSE   908  'to 908'

 L. 828       900  LOAD_FAST                'word'
              902  STORE_FAST               'timeQualifier'
          904_906  JUMP_FORWARD       2152  'to 2152'
            908_0  COME_FROM           896  '896'

 L. 830       908  LOAD_FAST                'word'
              910  LOAD_STR                 'today'
              912  COMPARE_OP               ==
          914_916  POP_JUMP_IF_FALSE   940  'to 940'
              918  LOAD_FAST                'fromFlag'
          920_922  POP_JUMP_IF_TRUE    940  'to 940'

 L. 831       924  LOAD_CONST               0
              926  STORE_DEREF              'dayOffset'

 L. 832       928  LOAD_FAST                'used'
              930  LOAD_CONST               1
              932  INPLACE_ADD      
              934  STORE_FAST               'used'
          936_938  JUMP_FORWARD       2152  'to 2152'
            940_0  COME_FROM           920  '920'
            940_1  COME_FROM           914  '914'

 L. 833       940  LOAD_FAST                'word'
              942  LOAD_STR                 'tomorrow'
              944  COMPARE_OP               ==
          946_948  POP_JUMP_IF_FALSE   972  'to 972'
              950  LOAD_FAST                'fromFlag'
          952_954  POP_JUMP_IF_TRUE    972  'to 972'

 L. 834       956  LOAD_CONST               1
              958  STORE_DEREF              'dayOffset'

 L. 835       960  LOAD_FAST                'used'
              962  LOAD_CONST               1
              964  INPLACE_ADD      
              966  STORE_FAST               'used'
          968_970  JUMP_FORWARD       2152  'to 2152'
            972_0  COME_FROM           952  '952'
            972_1  COME_FROM           946  '946'

 L. 836       972  LOAD_FAST                'word'
              974  LOAD_STR                 'day'
              976  COMPARE_OP               ==
          978_980  POP_JUMP_IF_FALSE  1024  'to 1024'
              982  LOAD_FAST                'wordNext'
              984  LOAD_STR                 'before'
              986  COMPARE_OP               ==
          988_990  POP_JUMP_IF_FALSE  1024  'to 1024'
              992  LOAD_FAST                'wordNextNext'
              994  LOAD_STR                 'yesterday'
              996  COMPARE_OP               ==
         998_1000  POP_JUMP_IF_FALSE  1024  'to 1024'
             1002  LOAD_FAST                'fromFlag'
         1004_1006  POP_JUMP_IF_TRUE   1024  'to 1024'

 L. 837      1008  LOAD_CONST               -2
             1010  STORE_DEREF              'dayOffset'

 L. 838      1012  LOAD_FAST                'used'
             1014  LOAD_CONST               3
             1016  INPLACE_ADD      
             1018  STORE_FAST               'used'
         1020_1022  JUMP_FORWARD       2152  'to 2152'
           1024_0  COME_FROM          1004  '1004'
           1024_1  COME_FROM           998  '998'
           1024_2  COME_FROM           988  '988'
           1024_3  COME_FROM           978  '978'

 L. 839      1024  LOAD_FAST                'word'
             1026  LOAD_STR                 'before'
             1028  COMPARE_OP               ==
         1030_1032  POP_JUMP_IF_FALSE  1066  'to 1066'
             1034  LOAD_FAST                'wordNext'
             1036  LOAD_STR                 'yesterday'
             1038  COMPARE_OP               ==
         1040_1042  POP_JUMP_IF_FALSE  1066  'to 1066'
             1044  LOAD_FAST                'fromFlag'
         1046_1048  POP_JUMP_IF_TRUE   1066  'to 1066'

 L. 840      1050  LOAD_CONST               -2
             1052  STORE_DEREF              'dayOffset'

 L. 841      1054  LOAD_FAST                'used'
             1056  LOAD_CONST               2
             1058  INPLACE_ADD      
             1060  STORE_FAST               'used'
         1062_1064  JUMP_FORWARD       2152  'to 2152'
           1066_0  COME_FROM          1046  '1046'
           1066_1  COME_FROM          1040  '1040'
           1066_2  COME_FROM          1030  '1030'

 L. 842      1066  LOAD_FAST                'word'
             1068  LOAD_STR                 'yesterday'
             1070  COMPARE_OP               ==
         1072_1074  POP_JUMP_IF_FALSE  1098  'to 1098'
             1076  LOAD_FAST                'fromFlag'
         1078_1080  POP_JUMP_IF_TRUE   1098  'to 1098'

 L. 843      1082  LOAD_CONST               -1
             1084  STORE_DEREF              'dayOffset'

 L. 844      1086  LOAD_FAST                'used'
             1088  LOAD_CONST               1
             1090  INPLACE_ADD      
             1092  STORE_FAST               'used'
         1094_1096  JUMP_FORWARD       2152  'to 2152'
           1098_0  COME_FROM          1078  '1078'
           1098_1  COME_FROM          1072  '1072'

 L. 845      1098  LOAD_FAST                'word'
             1100  LOAD_STR                 'day'
             1102  COMPARE_OP               ==
         1104_1106  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 846      1108  LOAD_FAST                'wordNext'
             1110  LOAD_STR                 'after'
             1112  COMPARE_OP               ==
         1114_1116  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 847      1118  LOAD_FAST                'wordNextNext'
             1120  LOAD_STR                 'tomorrow'
             1122  COMPARE_OP               ==
         1124_1126  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 848      1128  LOAD_FAST                'fromFlag'
         1130_1132  POP_JUMP_IF_TRUE   1192  'to 1192'

 L. 849      1134  LOAD_FAST                'wordPrev'
         1136_1138  POP_JUMP_IF_FALSE  1154  'to 1154'
             1140  LOAD_FAST                'wordPrev'
             1142  LOAD_CONST               0
             1144  BINARY_SUBSCR    
             1146  LOAD_METHOD              isdigit
             1148  CALL_METHOD_0         0  '0 positional arguments'
         1150_1152  POP_JUMP_IF_TRUE   1192  'to 1192'
           1154_0  COME_FROM          1136  '1136'

 L. 850      1154  LOAD_CONST               2
             1156  STORE_DEREF              'dayOffset'

 L. 851      1158  LOAD_CONST               3
             1160  STORE_FAST               'used'

 L. 852      1162  LOAD_FAST                'wordPrev'
             1164  LOAD_STR                 'the'
             1166  COMPARE_OP               ==
         1168_1170  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 853      1172  LOAD_FAST                'start'
             1174  LOAD_CONST               1
             1176  INPLACE_SUBTRACT 
             1178  STORE_FAST               'start'

 L. 854      1180  LOAD_FAST                'used'
             1182  LOAD_CONST               1
             1184  INPLACE_ADD      
             1186  STORE_FAST               'used'
         1188_1190  JUMP_FORWARD       2152  'to 2152'
           1192_0  COME_FROM          1150  '1150'
           1192_1  COME_FROM          1130  '1130'
           1192_2  COME_FROM          1124  '1124'
           1192_3  COME_FROM          1114  '1114'
           1192_4  COME_FROM          1104  '1104'

 L. 856      1192  LOAD_FAST                'word'
             1194  LOAD_STR                 'day'
             1196  COMPARE_OP               ==
         1198_1200  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 857      1202  LOAD_FAST                'wordPrev'
         1204_1206  POP_JUMP_IF_FALSE  2152  'to 2152'
             1208  LOAD_FAST                'wordPrev'
             1210  LOAD_CONST               0
             1212  BINARY_SUBSCR    
             1214  LOAD_METHOD              isdigit
             1216  CALL_METHOD_0         0  '0 positional arguments'
         1218_1220  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 858      1222  LOAD_DEREF               'dayOffset'
             1224  LOAD_GLOBAL              int
             1226  LOAD_FAST                'wordPrev'
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  INPLACE_ADD      
             1232  STORE_DEREF              'dayOffset'

 L. 859      1234  LOAD_FAST                'start'
             1236  LOAD_CONST               1
             1238  INPLACE_SUBTRACT 
             1240  STORE_FAST               'start'

 L. 860      1242  LOAD_CONST               2
             1244  STORE_FAST               'used'
         1246_1248  JUMP_FORWARD       2152  'to 2152'
           1250_0  COME_FROM          1198  '1198'

 L. 861      1250  LOAD_FAST                'word'
             1252  LOAD_STR                 'week'
             1254  COMPARE_OP               ==
         1256_1258  POP_JUMP_IF_FALSE  1374  'to 1374'
             1260  LOAD_FAST                'fromFlag'
         1262_1264  POP_JUMP_IF_TRUE   1374  'to 1374'
             1266  LOAD_FAST                'wordPrev'
         1268_1270  POP_JUMP_IF_FALSE  1374  'to 1374'

 L. 862      1272  LOAD_FAST                'wordPrev'
             1274  LOAD_CONST               0
             1276  BINARY_SUBSCR    
             1278  LOAD_METHOD              isdigit
             1280  CALL_METHOD_0         0  '0 positional arguments'
         1282_1284  POP_JUMP_IF_FALSE  1316  'to 1316'

 L. 863      1286  LOAD_DEREF               'dayOffset'
             1288  LOAD_GLOBAL              int
             1290  LOAD_FAST                'wordPrev'
             1292  CALL_FUNCTION_1       1  '1 positional argument'
             1294  LOAD_CONST               7
             1296  BINARY_MULTIPLY  
             1298  INPLACE_ADD      
             1300  STORE_DEREF              'dayOffset'

 L. 864      1302  LOAD_FAST                'start'
             1304  LOAD_CONST               1
             1306  INPLACE_SUBTRACT 
             1308  STORE_FAST               'start'

 L. 865      1310  LOAD_CONST               2
             1312  STORE_FAST               'used'
             1314  JUMP_FORWARD       2152  'to 2152'
           1316_0  COME_FROM          1282  '1282'

 L. 866      1316  LOAD_FAST                'wordPrev'
             1318  LOAD_STR                 'next'
             1320  COMPARE_OP               ==
         1322_1324  POP_JUMP_IF_FALSE  1344  'to 1344'

 L. 867      1326  LOAD_CONST               7
             1328  STORE_DEREF              'dayOffset'

 L. 868      1330  LOAD_FAST                'start'
             1332  LOAD_CONST               1
             1334  INPLACE_SUBTRACT 
             1336  STORE_FAST               'start'

 L. 869      1338  LOAD_CONST               2
             1340  STORE_FAST               'used'
             1342  JUMP_FORWARD       2152  'to 2152'
           1344_0  COME_FROM          1322  '1322'

 L. 870      1344  LOAD_FAST                'wordPrev'
             1346  LOAD_STR                 'last'
             1348  COMPARE_OP               ==
         1350_1352  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 871      1354  LOAD_CONST               -7
             1356  STORE_DEREF              'dayOffset'

 L. 872      1358  LOAD_FAST                'start'
             1360  LOAD_CONST               1
             1362  INPLACE_SUBTRACT 
             1364  STORE_FAST               'start'

 L. 873      1366  LOAD_CONST               2
             1368  STORE_FAST               'used'
         1370_1372  JUMP_FORWARD       2152  'to 2152'
           1374_0  COME_FROM          1268  '1268'
           1374_1  COME_FROM          1262  '1262'
           1374_2  COME_FROM          1256  '1256'

 L. 875      1374  LOAD_FAST                'word'
             1376  LOAD_STR                 'month'
             1378  COMPARE_OP               ==
         1380_1382  POP_JUMP_IF_FALSE  1490  'to 1490'
             1384  LOAD_FAST                'fromFlag'
         1386_1388  POP_JUMP_IF_TRUE   1490  'to 1490'
             1390  LOAD_FAST                'wordPrev'
         1392_1394  POP_JUMP_IF_FALSE  1490  'to 1490'

 L. 876      1396  LOAD_FAST                'wordPrev'
             1398  LOAD_CONST               0
             1400  BINARY_SUBSCR    
             1402  LOAD_METHOD              isdigit
             1404  CALL_METHOD_0         0  '0 positional arguments'
         1406_1408  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 877      1410  LOAD_GLOBAL              int
             1412  LOAD_FAST                'wordPrev'
             1414  CALL_FUNCTION_1       1  '1 positional argument'
             1416  STORE_DEREF              'monthOffset'

 L. 878      1418  LOAD_FAST                'start'
             1420  LOAD_CONST               1
             1422  INPLACE_SUBTRACT 
             1424  STORE_FAST               'start'

 L. 879      1426  LOAD_CONST               2
             1428  STORE_FAST               'used'
             1430  JUMP_FORWARD       2152  'to 2152'
           1432_0  COME_FROM          1406  '1406'

 L. 880      1432  LOAD_FAST                'wordPrev'
             1434  LOAD_STR                 'next'
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1460  'to 1460'

 L. 881      1442  LOAD_CONST               1
             1444  STORE_DEREF              'monthOffset'

 L. 882      1446  LOAD_FAST                'start'
             1448  LOAD_CONST               1
             1450  INPLACE_SUBTRACT 
             1452  STORE_FAST               'start'

 L. 883      1454  LOAD_CONST               2
             1456  STORE_FAST               'used'
             1458  JUMP_FORWARD       2152  'to 2152'
           1460_0  COME_FROM          1438  '1438'

 L. 884      1460  LOAD_FAST                'wordPrev'
             1462  LOAD_STR                 'last'
             1464  COMPARE_OP               ==
         1466_1468  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 885      1470  LOAD_CONST               -1
             1472  STORE_DEREF              'monthOffset'

 L. 886      1474  LOAD_FAST                'start'
             1476  LOAD_CONST               1
             1478  INPLACE_SUBTRACT 
             1480  STORE_FAST               'start'

 L. 887      1482  LOAD_CONST               2
             1484  STORE_FAST               'used'
         1486_1488  JUMP_FORWARD       2152  'to 2152'
           1490_0  COME_FROM          1392  '1392'
           1490_1  COME_FROM          1386  '1386'
           1490_2  COME_FROM          1380  '1380'

 L. 889      1490  LOAD_FAST                'word'
             1492  LOAD_STR                 'year'
             1494  COMPARE_OP               ==
         1496_1498  POP_JUMP_IF_FALSE  1606  'to 1606'
             1500  LOAD_FAST                'fromFlag'
         1502_1504  POP_JUMP_IF_TRUE   1606  'to 1606'
             1506  LOAD_FAST                'wordPrev'
         1508_1510  POP_JUMP_IF_FALSE  1606  'to 1606'

 L. 890      1512  LOAD_FAST                'wordPrev'
             1514  LOAD_CONST               0
             1516  BINARY_SUBSCR    
             1518  LOAD_METHOD              isdigit
             1520  CALL_METHOD_0         0  '0 positional arguments'
         1522_1524  POP_JUMP_IF_FALSE  1548  'to 1548'

 L. 891      1526  LOAD_GLOBAL              int
             1528  LOAD_FAST                'wordPrev'
             1530  CALL_FUNCTION_1       1  '1 positional argument'
             1532  STORE_DEREF              'yearOffset'

 L. 892      1534  LOAD_FAST                'start'
             1536  LOAD_CONST               1
             1538  INPLACE_SUBTRACT 
             1540  STORE_FAST               'start'

 L. 893      1542  LOAD_CONST               2
             1544  STORE_FAST               'used'
             1546  JUMP_FORWARD       2152  'to 2152'
           1548_0  COME_FROM          1522  '1522'

 L. 894      1548  LOAD_FAST                'wordPrev'
             1550  LOAD_STR                 'next'
             1552  COMPARE_OP               ==
         1554_1556  POP_JUMP_IF_FALSE  1576  'to 1576'

 L. 895      1558  LOAD_CONST               1
             1560  STORE_DEREF              'yearOffset'

 L. 896      1562  LOAD_FAST                'start'
             1564  LOAD_CONST               1
             1566  INPLACE_SUBTRACT 
             1568  STORE_FAST               'start'

 L. 897      1570  LOAD_CONST               2
             1572  STORE_FAST               'used'
             1574  JUMP_FORWARD       2152  'to 2152'
           1576_0  COME_FROM          1554  '1554'

 L. 898      1576  LOAD_FAST                'wordPrev'
             1578  LOAD_STR                 'last'
             1580  COMPARE_OP               ==
         1582_1584  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 899      1586  LOAD_CONST               -1
             1588  STORE_DEREF              'yearOffset'

 L. 900      1590  LOAD_FAST                'start'
             1592  LOAD_CONST               1
             1594  INPLACE_SUBTRACT 
             1596  STORE_FAST               'start'

 L. 901      1598  LOAD_CONST               2
             1600  STORE_FAST               'used'
         1602_1604  JUMP_FORWARD       2152  'to 2152'
           1606_0  COME_FROM          1508  '1508'
           1606_1  COME_FROM          1502  '1502'
           1606_2  COME_FROM          1496  '1496'

 L. 904      1606  LOAD_FAST                'word'
             1608  LOAD_FAST                'days'
             1610  COMPARE_OP               in
         1612_1614  POP_JUMP_IF_FALSE  1754  'to 1754'
             1616  LOAD_FAST                'fromFlag'
         1618_1620  POP_JUMP_IF_TRUE   1754  'to 1754'

 L. 905      1622  LOAD_FAST                'days'
             1624  LOAD_METHOD              index
             1626  LOAD_FAST                'word'
             1628  CALL_METHOD_1         1  '1 positional argument'
             1630  STORE_FAST               'd'

 L. 906      1632  LOAD_FAST                'd'
             1634  LOAD_CONST               1
             1636  BINARY_ADD       
             1638  LOAD_GLOBAL              int
             1640  LOAD_FAST                'today'
             1642  CALL_FUNCTION_1       1  '1 positional argument'
             1644  BINARY_SUBTRACT  
             1646  STORE_DEREF              'dayOffset'

 L. 907      1648  LOAD_CONST               1
             1650  STORE_FAST               'used'

 L. 908      1652  LOAD_DEREF               'dayOffset'
             1654  LOAD_CONST               0
             1656  COMPARE_OP               <
         1658_1660  POP_JUMP_IF_FALSE  1670  'to 1670'

 L. 909      1662  LOAD_DEREF               'dayOffset'
             1664  LOAD_CONST               7
             1666  INPLACE_ADD      
             1668  STORE_DEREF              'dayOffset'
           1670_0  COME_FROM          1658  '1658'

 L. 910      1670  LOAD_FAST                'wordPrev'
             1672  LOAD_STR                 'next'
             1674  COMPARE_OP               ==
         1676_1678  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 911      1680  LOAD_DEREF               'dayOffset'
             1682  LOAD_CONST               2
             1684  COMPARE_OP               <=
         1686_1688  POP_JUMP_IF_FALSE  1698  'to 1698'

 L. 912      1690  LOAD_DEREF               'dayOffset'
             1692  LOAD_CONST               7
             1694  INPLACE_ADD      
             1696  STORE_DEREF              'dayOffset'
           1698_0  COME_FROM          1686  '1686'

 L. 913      1698  LOAD_FAST                'used'
             1700  LOAD_CONST               1
             1702  INPLACE_ADD      
             1704  STORE_FAST               'used'

 L. 914      1706  LOAD_FAST                'start'
             1708  LOAD_CONST               1
             1710  INPLACE_SUBTRACT 
             1712  STORE_FAST               'start'
             1714  JUMP_FORWARD       2152  'to 2152'
           1716_0  COME_FROM          1676  '1676'

 L. 915      1716  LOAD_FAST                'wordPrev'
             1718  LOAD_STR                 'last'
             1720  COMPARE_OP               ==
         1722_1724  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 916      1726  LOAD_DEREF               'dayOffset'
             1728  LOAD_CONST               7
             1730  INPLACE_SUBTRACT 
             1732  STORE_DEREF              'dayOffset'

 L. 917      1734  LOAD_FAST                'used'
             1736  LOAD_CONST               1
             1738  INPLACE_ADD      
             1740  STORE_FAST               'used'

 L. 918      1742  LOAD_FAST                'start'
             1744  LOAD_CONST               1
             1746  INPLACE_SUBTRACT 
             1748  STORE_FAST               'start'
         1750_1752  JUMP_FORWARD       2152  'to 2152'
           1754_0  COME_FROM          1618  '1618'
           1754_1  COME_FROM          1612  '1612'

 L. 920      1754  LOAD_FAST                'word'
             1756  LOAD_FAST                'months'
             1758  COMPARE_OP               in
         1760_1762  POP_JUMP_IF_TRUE   1780  'to 1780'
             1764  LOAD_FAST                'word'
             1766  LOAD_FAST                'monthsShort'
             1768  COMPARE_OP               in
         1770_1772  POP_JUMP_IF_FALSE  2152  'to 2152'
             1774  LOAD_FAST                'fromFlag'
         1776_1778  POP_JUMP_IF_TRUE   2152  'to 2152'
           1780_0  COME_FROM          1760  '1760'

 L. 921      1780  LOAD_GLOBAL              month_to_int_en
             1782  LOAD_FAST                'word'
             1784  CALL_FUNCTION_1       1  '1 positional argument'
             1786  STORE_FAST               'm'

 L. 923      1788  LOAD_FAST                'wordPrev'
             1790  LOAD_CONST               ('next', 'this', 'last', 'past', 'previous')
             1792  COMPARE_OP               in
         1794_1796  POP_JUMP_IF_FALSE  1826  'to 1826'

 L. 924      1798  LOAD_DEREF               'datestr'
             1800  LOAD_FAST                'wordPrev'
             1802  LOAD_STR                 ' '
             1804  BINARY_ADD       
             1806  INPLACE_ADD      
             1808  STORE_DEREF              'datestr'

 L. 925      1810  LOAD_FAST                'start'
             1812  LOAD_CONST               1
             1814  INPLACE_SUBTRACT 
             1816  STORE_FAST               'start'

 L. 926      1818  LOAD_FAST                'used'
             1820  LOAD_CONST               1
             1822  INPLACE_ADD      
             1824  STORE_FAST               'used'
           1826_0  COME_FROM          1794  '1794'

 L. 927      1826  LOAD_DEREF               'datestr'
             1828  LOAD_FAST                'months'
             1830  LOAD_FAST                'm'
             1832  LOAD_CONST               1
             1834  BINARY_SUBTRACT  
             1836  BINARY_SUBSCR    
             1838  INPLACE_ADD      
             1840  STORE_DEREF              'datestr'

 L. 928      1842  LOAD_FAST                'used'
             1844  LOAD_CONST               1
             1846  INPLACE_ADD      
             1848  STORE_FAST               'used'

 L. 929      1850  LOAD_FAST                'wordPrev'
         1852_1854  POP_JUMP_IF_FALSE  2036  'to 2036'
             1856  LOAD_FAST                'wordPrev'
             1858  LOAD_CONST               0
             1860  BINARY_SUBSCR    
             1862  LOAD_METHOD              isdigit
             1864  CALL_METHOD_0         0  '0 positional arguments'
         1866_1868  POP_JUMP_IF_TRUE   1894  'to 1894'

 L. 930      1870  LOAD_FAST                'wordPrev'
             1872  LOAD_STR                 'of'
             1874  COMPARE_OP               ==
         1876_1878  POP_JUMP_IF_FALSE  2036  'to 2036'
             1880  LOAD_FAST                'wordPrevPrev'
             1882  LOAD_CONST               0
             1884  BINARY_SUBSCR    
             1886  LOAD_METHOD              isdigit
             1888  CALL_METHOD_0         0  '0 positional arguments'
         1890_1892  POP_JUMP_IF_FALSE  2036  'to 2036'
           1894_0  COME_FROM          1866  '1866'

 L. 931      1894  LOAD_FAST                'wordPrev'
             1896  LOAD_STR                 'of'
             1898  COMPARE_OP               ==
         1900_1902  POP_JUMP_IF_FALSE  1956  'to 1956'
             1904  LOAD_FAST                'wordPrevPrev'
             1906  LOAD_CONST               0
             1908  BINARY_SUBSCR    
             1910  LOAD_METHOD              isdigit
             1912  CALL_METHOD_0         0  '0 positional arguments'
         1914_1916  POP_JUMP_IF_FALSE  1956  'to 1956'

 L. 932      1918  LOAD_DEREF               'datestr'
             1920  LOAD_STR                 ' '
             1922  LOAD_FAST                'words'
             1924  LOAD_FAST                'idx'
             1926  LOAD_CONST               2
             1928  BINARY_SUBTRACT  
             1930  BINARY_SUBSCR    
             1932  BINARY_ADD       
             1934  INPLACE_ADD      
             1936  STORE_DEREF              'datestr'

 L. 933      1938  LOAD_FAST                'used'
             1940  LOAD_CONST               1
             1942  INPLACE_ADD      
             1944  STORE_FAST               'used'

 L. 934      1946  LOAD_FAST                'start'
             1948  LOAD_CONST               1
             1950  INPLACE_SUBTRACT 
             1952  STORE_FAST               'start'
             1954  JUMP_FORWARD       1968  'to 1968'
           1956_0  COME_FROM          1914  '1914'
           1956_1  COME_FROM          1900  '1900'

 L. 936      1956  LOAD_DEREF               'datestr'
             1958  LOAD_STR                 ' '
             1960  LOAD_FAST                'wordPrev'
             1962  BINARY_ADD       
             1964  INPLACE_ADD      
             1966  STORE_DEREF              'datestr'
           1968_0  COME_FROM          1954  '1954'

 L. 937      1968  LOAD_FAST                'start'
             1970  LOAD_CONST               1
             1972  INPLACE_SUBTRACT 
             1974  STORE_FAST               'start'

 L. 938      1976  LOAD_FAST                'used'
             1978  LOAD_CONST               1
             1980  INPLACE_ADD      
             1982  STORE_FAST               'used'

 L. 939      1984  LOAD_FAST                'wordNext'
         1986_1988  POP_JUMP_IF_FALSE  2030  'to 2030'
             1990  LOAD_FAST                'wordNext'
             1992  LOAD_CONST               0
             1994  BINARY_SUBSCR    
             1996  LOAD_METHOD              isdigit
             1998  CALL_METHOD_0         0  '0 positional arguments'
         2000_2002  POP_JUMP_IF_FALSE  2030  'to 2030'

 L. 940      2004  LOAD_DEREF               'datestr'
             2006  LOAD_STR                 ' '
             2008  LOAD_FAST                'wordNext'
             2010  BINARY_ADD       
             2012  INPLACE_ADD      
             2014  STORE_DEREF              'datestr'

 L. 941      2016  LOAD_FAST                'used'
             2018  LOAD_CONST               1
             2020  INPLACE_ADD      
             2022  STORE_FAST               'used'

 L. 942      2024  LOAD_CONST               True
             2026  STORE_FAST               'hasYear'
             2028  JUMP_FORWARD       2034  'to 2034'
           2030_0  COME_FROM          2000  '2000'
           2030_1  COME_FROM          1986  '1986'

 L. 944      2030  LOAD_CONST               False
             2032  STORE_FAST               'hasYear'
           2034_0  COME_FROM          2028  '2028'
             2034  JUMP_FORWARD       2152  'to 2152'
           2036_0  COME_FROM          1890  '1890'
           2036_1  COME_FROM          1876  '1876'
           2036_2  COME_FROM          1852  '1852'

 L. 946      2036  LOAD_FAST                'wordNext'
         2038_2040  POP_JUMP_IF_FALSE  2128  'to 2128'
             2042  LOAD_FAST                'wordNext'
             2044  LOAD_CONST               0
             2046  BINARY_SUBSCR    
             2048  LOAD_METHOD              isdigit
             2050  CALL_METHOD_0         0  '0 positional arguments'
         2052_2054  POP_JUMP_IF_FALSE  2128  'to 2128'

 L. 947      2056  LOAD_DEREF               'datestr'
             2058  LOAD_STR                 ' '
             2060  LOAD_FAST                'wordNext'
             2062  BINARY_ADD       
             2064  INPLACE_ADD      
             2066  STORE_DEREF              'datestr'

 L. 948      2068  LOAD_FAST                'used'
             2070  LOAD_CONST               1
             2072  INPLACE_ADD      
             2074  STORE_FAST               'used'

 L. 949      2076  LOAD_FAST                'wordNextNext'
         2078_2080  POP_JUMP_IF_FALSE  2122  'to 2122'
             2082  LOAD_FAST                'wordNextNext'
             2084  LOAD_CONST               0
             2086  BINARY_SUBSCR    
             2088  LOAD_METHOD              isdigit
             2090  CALL_METHOD_0         0  '0 positional arguments'
         2092_2094  POP_JUMP_IF_FALSE  2122  'to 2122'

 L. 950      2096  LOAD_DEREF               'datestr'
             2098  LOAD_STR                 ' '
             2100  LOAD_FAST                'wordNextNext'
             2102  BINARY_ADD       
             2104  INPLACE_ADD      
             2106  STORE_DEREF              'datestr'

 L. 951      2108  LOAD_FAST                'used'
           2110_0  COME_FROM           750  '750'
           2110_1  COME_FROM           646  '646'
             2110  LOAD_CONST               1
             2112  INPLACE_ADD      
           2114_0  COME_FROM          1714  '1714'
           2114_1  COME_FROM           850  '850'
             2114  STORE_FAST               'used'

 L. 952      2116  LOAD_CONST               True
             2118  STORE_FAST               'hasYear'
             2120  JUMP_FORWARD       2126  'to 2126'
           2122_0  COME_FROM          2092  '2092'
           2122_1  COME_FROM          2078  '2078'
           2122_2  COME_FROM          1574  '1574'
           2122_3  COME_FROM          1458  '1458'
           2122_4  COME_FROM          1342  '1342'

 L. 954      2122  LOAD_CONST               False
             2124  STORE_FAST               'hasYear'
           2126_0  COME_FROM          2120  '2120'
             2126  JUMP_FORWARD       2152  'to 2152'
           2128_0  COME_FROM          2052  '2052'
           2128_1  COME_FROM          2038  '2038'

 L. 959      2128  LOAD_FAST                'word'
           2130_0  COME_FROM           866  '866'
           2130_1  COME_FROM           770  '770'
           2130_2  COME_FROM           666  '666'
             2130  LOAD_STR                 'may'
             2132  COMPARE_OP               ==
         2134_2136  POP_JUMP_IF_FALSE  2152  'to 2152'
             2138  LOAD_FAST                'wordNext'
             2140  LOAD_CONST               ('i', 'we', 'be')
             2142  COMPARE_OP               in
         2144_2146  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 960      2148  LOAD_STR                 ''
             2150  STORE_DEREF              'datestr'
           2152_0  COME_FROM          2144  '2144'
           2152_1  COME_FROM          2134  '2134'
           2152_2  COME_FROM          2126  '2126'
           2152_3  COME_FROM          2034  '2034'
           2152_4  COME_FROM          1776  '1776'
           2152_5  COME_FROM          1770  '1770'
           2152_6  COME_FROM          1750  '1750'
           2152_7  COME_FROM          1722  '1722'
           2152_8  COME_FROM          1602  '1602'
           2152_9  COME_FROM          1582  '1582'
          2152_10  COME_FROM          1486  '1486'
          2152_11  COME_FROM          1466  '1466'
          2152_12  COME_FROM          1370  '1370'
          2152_13  COME_FROM          1350  '1350'
          2152_14  COME_FROM          1246  '1246'
          2152_15  COME_FROM          1218  '1218'
          2152_16  COME_FROM          1204  '1204'
          2152_17  COME_FROM          1188  '1188'
          2152_18  COME_FROM          1168  '1168'
          2152_19  COME_FROM          1094  '1094'
          2152_20  COME_FROM          1062  '1062'
          2152_21  COME_FROM          1020  '1020'
          2152_22  COME_FROM           968  '968'
          2152_23  COME_FROM           936  '936'
          2152_24  COME_FROM           904  '904'
          2152_25  COME_FROM           886  '886'
          2152_26  COME_FROM           874  '874'
          2152_27  COME_FROM           790  '790'
          2152_28  COME_FROM           778  '778'
          2152_29  COME_FROM           686  '686'
          2152_30  COME_FROM           674  '674'

 L. 964      2152  LOAD_FAST                'days'
             2154  LOAD_FAST                'months'
             2156  BINARY_ADD       
             2158  LOAD_FAST                'monthsShort'
             2160  BINARY_ADD       
             2162  STORE_FAST               'validFollowups'

 L. 965      2164  LOAD_FAST                'validFollowups'
             2166  LOAD_METHOD              append
             2168  LOAD_STR                 'today'
             2170  CALL_METHOD_1         1  '1 positional argument'
             2172  POP_TOP          

 L. 966      2174  LOAD_FAST                'validFollowups'
             2176  LOAD_METHOD              append
             2178  LOAD_STR                 'tomorrow'
             2180  CALL_METHOD_1         1  '1 positional argument'
             2182  POP_TOP          

 L. 967      2184  LOAD_FAST                'validFollowups'
             2186  LOAD_METHOD              append
             2188  LOAD_STR                 'yesterday'
             2190  CALL_METHOD_1         1  '1 positional argument'
             2192  POP_TOP          

 L. 968      2194  LOAD_FAST                'validFollowups'
             2196  LOAD_METHOD              append
             2198  LOAD_STR                 'next'
             2200  CALL_METHOD_1         1  '1 positional argument'
             2202  POP_TOP          

 L. 969      2204  LOAD_FAST                'validFollowups'
             2206  LOAD_METHOD              append
             2208  LOAD_STR                 'last'
             2210  CALL_METHOD_1         1  '1 positional argument'
             2212  POP_TOP          

 L. 970      2214  LOAD_FAST                'validFollowups'
             2216  LOAD_METHOD              append
             2218  LOAD_STR                 'now'
             2220  CALL_METHOD_1         1  '1 positional argument'
             2222  POP_TOP          

 L. 971      2224  LOAD_FAST                'validFollowups'
             2226  LOAD_METHOD              append
             2228  LOAD_STR                 'this'
             2230  CALL_METHOD_1         1  '1 positional argument'
             2232  POP_TOP          

 L. 972      2234  LOAD_FAST                'word'
             2236  LOAD_STR                 'from'
             2238  COMPARE_OP               ==
         2240_2242  POP_JUMP_IF_TRUE   2254  'to 2254'
             2244  LOAD_FAST                'word'
             2246  LOAD_STR                 'after'
             2248  COMPARE_OP               ==
         2250_2252  POP_JUMP_IF_FALSE  2514  'to 2514'
           2254_0  COME_FROM          2240  '2240'
             2254  LOAD_FAST                'wordNext'
             2256  LOAD_FAST                'validFollowups'
             2258  COMPARE_OP               in
         2260_2262  POP_JUMP_IF_FALSE  2514  'to 2514'

 L. 973      2264  LOAD_CONST               2
             2266  STORE_FAST               'used'

 L. 974      2268  LOAD_CONST               True
             2270  STORE_FAST               'fromFlag'

 L. 975      2272  LOAD_FAST                'wordNext'
             2274  LOAD_STR                 'tomorrow'
             2276  COMPARE_OP               ==
         2278_2280  POP_JUMP_IF_FALSE  2292  'to 2292'

 L. 976      2282  LOAD_DEREF               'dayOffset'
             2284  LOAD_CONST               1
             2286  INPLACE_ADD      
             2288  STORE_DEREF              'dayOffset'
             2290  JUMP_FORWARD       2514  'to 2514'
           2292_0  COME_FROM          2278  '2278'

 L. 977      2292  LOAD_FAST                'wordNext'
             2294  LOAD_STR                 'yesterday'
             2296  COMPARE_OP               ==
         2298_2300  POP_JUMP_IF_FALSE  2312  'to 2312'

 L. 978      2302  LOAD_DEREF               'dayOffset'
             2304  LOAD_CONST               1
             2306  INPLACE_SUBTRACT 
             2308  STORE_DEREF              'dayOffset'
             2310  JUMP_FORWARD       2514  'to 2514'
           2312_0  COME_FROM          2298  '2298'

 L. 979      2312  LOAD_FAST                'wordNext'
             2314  LOAD_FAST                'days'
             2316  COMPARE_OP               in
         2318_2320  POP_JUMP_IF_FALSE  2380  'to 2380'

 L. 980      2322  LOAD_FAST                'days'
             2324  LOAD_METHOD              index
             2326  LOAD_FAST                'wordNext'
             2328  CALL_METHOD_1         1  '1 positional argument'
             2330  STORE_FAST               'd'

 L. 981      2332  LOAD_FAST                'd'
             2334  LOAD_CONST               1
             2336  BINARY_ADD       
             2338  LOAD_GLOBAL              int
             2340  LOAD_FAST                'today'
             2342  CALL_FUNCTION_1       1  '1 positional argument'
             2344  BINARY_SUBTRACT  
             2346  STORE_FAST               'tmpOffset'

 L. 982      2348  LOAD_CONST               2
             2350  STORE_FAST               'used'

 L. 983      2352  LOAD_FAST                'tmpOffset'
             2354  LOAD_CONST               0
             2356  COMPARE_OP               <
         2358_2360  POP_JUMP_IF_FALSE  2370  'to 2370'

 L. 984      2362  LOAD_FAST                'tmpOffset'
             2364  LOAD_CONST               7
             2366  INPLACE_ADD      
             2368  STORE_FAST               'tmpOffset'
           2370_0  COME_FROM          2358  '2358'

 L. 985      2370  LOAD_DEREF               'dayOffset'
             2372  LOAD_FAST                'tmpOffset'
             2374  INPLACE_ADD      
             2376  STORE_DEREF              'dayOffset'
             2378  JUMP_FORWARD       2514  'to 2514'
           2380_0  COME_FROM          2318  '2318'

 L. 986      2380  LOAD_FAST                'wordNextNext'
         2382_2384  POP_JUMP_IF_FALSE  2514  'to 2514'
             2386  LOAD_FAST                'wordNextNext'
             2388  LOAD_FAST                'days'
             2390  COMPARE_OP               in
         2392_2394  POP_JUMP_IF_FALSE  2514  'to 2514'

 L. 987      2396  LOAD_FAST                'days'
             2398  LOAD_METHOD              index
             2400  LOAD_FAST                'wordNextNext'
             2402  CALL_METHOD_1         1  '1 positional argument'
             2404  STORE_FAST               'd'

 L. 988      2406  LOAD_FAST                'd'
             2408  LOAD_CONST               1
             2410  BINARY_ADD       
             2412  LOAD_GLOBAL              int
             2414  LOAD_FAST                'today'
             2416  CALL_FUNCTION_1       1  '1 positional argument'
             2418  BINARY_SUBTRACT  
             2420  STORE_FAST               'tmpOffset'

 L. 989      2422  LOAD_CONST               3
             2424  STORE_FAST               'used'

 L. 990      2426  LOAD_FAST                'wordNext'
             2428  LOAD_STR                 'next'
             2430  COMPARE_OP               ==
         2432_2434  POP_JUMP_IF_FALSE  2472  'to 2472'

 L. 991      2436  LOAD_DEREF               'dayOffset'
             2438  LOAD_CONST               2
             2440  COMPARE_OP               <=
         2442_2444  POP_JUMP_IF_FALSE  2454  'to 2454'

 L. 992      2446  LOAD_FAST                'tmpOffset'
             2448  LOAD_CONST               7
             2450  INPLACE_ADD      
             2452  STORE_FAST               'tmpOffset'
           2454_0  COME_FROM          2442  '2442'

 L. 993      2454  LOAD_FAST                'used'
             2456  LOAD_CONST               1
             2458  INPLACE_ADD      
             2460  STORE_FAST               'used'

 L. 994      2462  LOAD_FAST                'start'
             2464  LOAD_CONST               1
             2466  INPLACE_SUBTRACT 
             2468  STORE_FAST               'start'
             2470  JUMP_FORWARD       2506  'to 2506'
           2472_0  COME_FROM          2432  '2432'

 L. 995      2472  LOAD_FAST                'wordNext'
             2474  LOAD_STR                 'last'
             2476  COMPARE_OP               ==
         2478_2480  POP_JUMP_IF_FALSE  2506  'to 2506'

 L. 996      2482  LOAD_FAST                'tmpOffset'
             2484  LOAD_CONST               7
             2486  INPLACE_SUBTRACT 
             2488  STORE_FAST               'tmpOffset'

 L. 997      2490  LOAD_FAST                'used'
             2492  LOAD_CONST               1
             2494  INPLACE_ADD      
             2496  STORE_FAST               'used'

 L. 998      2498  LOAD_FAST                'start'
             2500  LOAD_CONST               1
             2502  INPLACE_SUBTRACT 
             2504  STORE_FAST               'start'
           2506_0  COME_FROM          2478  '2478'
           2506_1  COME_FROM          2470  '2470'

 L. 999      2506  LOAD_DEREF               'dayOffset'
             2508  LOAD_FAST                'tmpOffset'
             2510  INPLACE_ADD      
             2512  STORE_DEREF              'dayOffset'
           2514_0  COME_FROM          2392  '2392'
           2514_1  COME_FROM          2382  '2382'
           2514_2  COME_FROM          2378  '2378'
           2514_3  COME_FROM          2310  '2310'
           2514_4  COME_FROM          2290  '2290'
           2514_5  COME_FROM          2260  '2260'
           2514_6  COME_FROM          2250  '2250'

 L.1000      2514  LOAD_FAST                'used'
             2516  LOAD_CONST               0
             2518  COMPARE_OP               >
         2520_2522  POP_JUMP_IF_FALSE   306  'to 306'

 L.1001      2524  LOAD_FAST                'start'
             2526  LOAD_CONST               1
             2528  BINARY_SUBTRACT  
             2530  LOAD_CONST               0
             2532  COMPARE_OP               >
         2534_2536  POP_JUMP_IF_FALSE  2572  'to 2572'
             2538  LOAD_FAST                'words'
             2540  LOAD_FAST                'start'
             2542  LOAD_CONST               1
             2544  BINARY_SUBTRACT  
             2546  BINARY_SUBSCR    
             2548  LOAD_STR                 'this'
             2550  COMPARE_OP               ==
         2552_2554  POP_JUMP_IF_FALSE  2572  'to 2572'

 L.1002      2556  LOAD_FAST                'start'
             2558  LOAD_CONST               1
             2560  INPLACE_SUBTRACT 
             2562  STORE_FAST               'start'

 L.1003      2564  LOAD_FAST                'used'
             2566  LOAD_CONST               1
             2568  INPLACE_ADD      
             2570  STORE_FAST               'used'
           2572_0  COME_FROM          2552  '2552'
           2572_1  COME_FROM          2534  '2534'

 L.1005      2572  SETUP_LOOP         2606  'to 2606'
             2574  LOAD_GLOBAL              range
             2576  LOAD_CONST               0
             2578  LOAD_FAST                'used'
             2580  CALL_FUNCTION_2       2  '2 positional arguments'
             2582  GET_ITER         
             2584  FOR_ITER           2604  'to 2604'
             2586  STORE_FAST               'i'

 L.1006      2588  LOAD_STR                 ''
             2590  LOAD_FAST                'words'
             2592  LOAD_FAST                'i'
             2594  LOAD_FAST                'start'
             2596  BINARY_ADD       
             2598  STORE_SUBSCR     
         2600_2602  JUMP_BACK          2584  'to 2584'
             2604  POP_BLOCK        
           2606_0  COME_FROM_LOOP     2572  '2572'

 L.1008      2606  LOAD_FAST                'start'
             2608  LOAD_CONST               1
             2610  BINARY_SUBTRACT  
             2612  LOAD_CONST               0
             2614  COMPARE_OP               >=
         2616_2618  POP_JUMP_IF_FALSE  2650  'to 2650'
             2620  LOAD_FAST                'words'
             2622  LOAD_FAST                'start'
             2624  LOAD_CONST               1
             2626  BINARY_SUBTRACT  
             2628  BINARY_SUBSCR    
             2630  LOAD_FAST                'markers'
             2632  COMPARE_OP               in
         2634_2636  POP_JUMP_IF_FALSE  2650  'to 2650'

 L.1009      2638  LOAD_STR                 ''
             2640  LOAD_FAST                'words'
             2642  LOAD_FAST                'start'
             2644  LOAD_CONST               1
             2646  BINARY_SUBTRACT  
             2648  STORE_SUBSCR     
           2650_0  COME_FROM          2634  '2634'
           2650_1  COME_FROM          2616  '2616'

 L.1010      2650  LOAD_CONST               True
             2652  STORE_DEREF              'found'

 L.1011      2654  LOAD_CONST               True
             2656  STORE_FAST               'daySpecified'
         2658_2660  JUMP_BACK           306  'to 306'
             2662  POP_BLOCK        
           2664_0  COME_FROM_LOOP      294  '294'

 L.1014      2664  LOAD_CONST               0
             2666  STORE_DEREF              'hrOffset'

 L.1015      2668  LOAD_CONST               0
             2670  STORE_DEREF              'minOffset'

 L.1016      2672  LOAD_CONST               0
             2674  STORE_DEREF              'secOffset'

 L.1017      2676  LOAD_CONST               None
             2678  STORE_DEREF              'hrAbs'

 L.1018      2680  LOAD_CONST               None
             2682  STORE_DEREF              'minAbs'

 L.1019      2684  LOAD_CONST               False
             2686  STORE_FAST               'military'

 L.1021  2688_2690  SETUP_LOOP         6118  'to 6118'
             2692  LOAD_GLOBAL              enumerate
             2694  LOAD_FAST                'words'
             2696  CALL_FUNCTION_1       1  '1 positional argument'
             2698  GET_ITER         
           2700_0  COME_FROM          5844  '5844'
         2700_2702  FOR_ITER           6116  'to 6116'
             2704  UNPACK_SEQUENCE_2     2 
             2706  STORE_FAST               'idx'
             2708  STORE_FAST               'word'

 L.1022      2710  LOAD_FAST                'word'
             2712  LOAD_STR                 ''
             2714  COMPARE_OP               ==
         2716_2718  POP_JUMP_IF_FALSE  2724  'to 2724'

 L.1023  2720_2722  CONTINUE           2700  'to 2700'
           2724_0  COME_FROM          2716  '2716'

 L.1025      2724  LOAD_FAST                'idx'
             2726  LOAD_CONST               1
             2728  COMPARE_OP               >
         2730_2732  POP_JUMP_IF_FALSE  2746  'to 2746'
             2734  LOAD_FAST                'words'
             2736  LOAD_FAST                'idx'
             2738  LOAD_CONST               2
             2740  BINARY_SUBTRACT  
             2742  BINARY_SUBSCR    
             2744  JUMP_FORWARD       2748  'to 2748'
           2746_0  COME_FROM          2730  '2730'
             2746  LOAD_STR                 ''
           2748_0  COME_FROM          2744  '2744'
             2748  STORE_FAST               'wordPrevPrev'

 L.1026      2750  LOAD_FAST                'idx'
             2752  LOAD_CONST               0
             2754  COMPARE_OP               >
         2756_2758  POP_JUMP_IF_FALSE  2772  'to 2772'
             2760  LOAD_FAST                'words'
             2762  LOAD_FAST                'idx'
             2764  LOAD_CONST               1
             2766  BINARY_SUBTRACT  
             2768  BINARY_SUBSCR    
             2770  JUMP_FORWARD       2774  'to 2774'
           2772_0  COME_FROM          2756  '2756'
             2772  LOAD_STR                 ''
           2774_0  COME_FROM          2770  '2770'
             2774  STORE_FAST               'wordPrev'

 L.1027      2776  LOAD_FAST                'idx'
             2778  LOAD_CONST               1
             2780  BINARY_ADD       
             2782  LOAD_GLOBAL              len
             2784  LOAD_FAST                'words'
             2786  CALL_FUNCTION_1       1  '1 positional argument'
             2788  COMPARE_OP               <
         2790_2792  POP_JUMP_IF_FALSE  2806  'to 2806'
             2794  LOAD_FAST                'words'
             2796  LOAD_FAST                'idx'
             2798  LOAD_CONST               1
             2800  BINARY_ADD       
             2802  BINARY_SUBSCR    
             2804  JUMP_FORWARD       2808  'to 2808'
           2806_0  COME_FROM          2790  '2790'
             2806  LOAD_STR                 ''
           2808_0  COME_FROM          2804  '2804'
             2808  STORE_FAST               'wordNext'

 L.1028      2810  LOAD_FAST                'idx'
             2812  LOAD_CONST               2
             2814  BINARY_ADD       
             2816  LOAD_GLOBAL              len
             2818  LOAD_FAST                'words'
             2820  CALL_FUNCTION_1       1  '1 positional argument'
             2822  COMPARE_OP               <
         2824_2826  POP_JUMP_IF_FALSE  2840  'to 2840'
             2828  LOAD_FAST                'words'
             2830  LOAD_FAST                'idx'
             2832  LOAD_CONST               2
             2834  BINARY_ADD       
             2836  BINARY_SUBSCR    
             2838  JUMP_FORWARD       2842  'to 2842'
           2840_0  COME_FROM          2824  '2824'
             2840  LOAD_STR                 ''
           2842_0  COME_FROM          2838  '2838'
             2842  STORE_FAST               'wordNextNext'

 L.1030      2844  LOAD_CONST               0
             2846  STORE_FAST               'used'

 L.1031      2848  LOAD_FAST                'word'
             2850  LOAD_STR                 'noon'
             2852  COMPARE_OP               ==
         2854_2856  POP_JUMP_IF_FALSE  2874  'to 2874'

 L.1032      2858  LOAD_CONST               12
             2860  STORE_DEREF              'hrAbs'

 L.1033      2862  LOAD_FAST                'used'
             2864  LOAD_CONST               1
             2866  INPLACE_ADD      
             2868  STORE_FAST               'used'
         2870_2872  JUMP_FORWARD       5838  'to 5838'
           2874_0  COME_FROM          2854  '2854'

 L.1034      2874  LOAD_FAST                'word'
             2876  LOAD_STR                 'midnight'
             2878  COMPARE_OP               ==
         2880_2882  POP_JUMP_IF_FALSE  2900  'to 2900'

 L.1035      2884  LOAD_CONST               0
             2886  STORE_DEREF              'hrAbs'

 L.1036      2888  LOAD_FAST                'used'
             2890  LOAD_CONST               1
             2892  INPLACE_ADD      
             2894  STORE_FAST               'used'
         2896_2898  JUMP_FORWARD       5838  'to 5838'
           2900_0  COME_FROM          2880  '2880'

 L.1037      2900  LOAD_FAST                'word'
             2902  LOAD_STR                 'morning'
             2904  COMPARE_OP               ==
         2906_2908  POP_JUMP_IF_FALSE  2936  'to 2936'

 L.1038      2910  LOAD_DEREF               'hrAbs'
             2912  LOAD_CONST               None
             2914  COMPARE_OP               is
         2916_2918  POP_JUMP_IF_FALSE  2924  'to 2924'

 L.1039      2920  LOAD_CONST               8
             2922  STORE_DEREF              'hrAbs'
           2924_0  COME_FROM          2916  '2916'

 L.1040      2924  LOAD_FAST                'used'
             2926  LOAD_CONST               1
             2928  INPLACE_ADD      
             2930  STORE_FAST               'used'
         2932_2934  JUMP_FORWARD       5838  'to 5838'
           2936_0  COME_FROM          2906  '2906'

 L.1041      2936  LOAD_FAST                'word'
             2938  LOAD_STR                 'afternoon'
             2940  COMPARE_OP               ==
         2942_2944  POP_JUMP_IF_FALSE  2972  'to 2972'

 L.1042      2946  LOAD_DEREF               'hrAbs'
             2948  LOAD_CONST               None
             2950  COMPARE_OP               is
         2952_2954  POP_JUMP_IF_FALSE  2960  'to 2960'

 L.1043      2956  LOAD_CONST               15
             2958  STORE_DEREF              'hrAbs'
           2960_0  COME_FROM          2952  '2952'

 L.1044      2960  LOAD_FAST                'used'
             2962  LOAD_CONST               1
             2964  INPLACE_ADD      
             2966  STORE_FAST               'used'
         2968_2970  JUMP_FORWARD       5838  'to 5838'
           2972_0  COME_FROM          2942  '2942'

 L.1045      2972  LOAD_FAST                'word'
             2974  LOAD_STR                 'evening'
             2976  COMPARE_OP               ==
         2978_2980  POP_JUMP_IF_FALSE  3008  'to 3008'

 L.1046      2982  LOAD_DEREF               'hrAbs'
             2984  LOAD_CONST               None
             2986  COMPARE_OP               is
         2988_2990  POP_JUMP_IF_FALSE  2996  'to 2996'

 L.1047      2992  LOAD_CONST               19
             2994  STORE_DEREF              'hrAbs'
           2996_0  COME_FROM          2988  '2988'

 L.1048      2996  LOAD_FAST                'used'
             2998  LOAD_CONST               1
             3000  INPLACE_ADD      
             3002  STORE_FAST               'used'
         3004_3006  JUMP_FORWARD       5838  'to 5838'
           3008_0  COME_FROM          2978  '2978'

 L.1049      3008  LOAD_FAST                'word'
             3010  LOAD_STR                 'tonight'
             3012  COMPARE_OP               ==
         3014_3016  POP_JUMP_IF_TRUE   3028  'to 3028'
             3018  LOAD_FAST                'word'
             3020  LOAD_STR                 'night'
             3022  COMPARE_OP               ==
         3024_3026  POP_JUMP_IF_FALSE  3046  'to 3046'
           3028_0  COME_FROM          3014  '3014'

 L.1050      3028  LOAD_DEREF               'hrAbs'
             3030  LOAD_CONST               None
             3032  COMPARE_OP               is
         3034_3036  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1051      3038  LOAD_CONST               22
             3040  STORE_DEREF              'hrAbs'
         3042_3044  JUMP_FORWARD       5838  'to 5838'
           3046_0  COME_FROM          3024  '3024'

 L.1055      3046  LOAD_FAST                'word'
             3048  LOAD_STR                 '2'
             3050  COMPARE_OP               ==
         3052_3054  POP_JUMP_IF_FALSE  3134  'to 3134'
             3056  LOAD_FAST                'wordNext'
             3058  LOAD_STR                 'of'
             3060  COMPARE_OP               ==
         3062_3064  POP_JUMP_IF_FALSE  3134  'to 3134'

 L.1056      3066  LOAD_FAST                'wordNextNext'
             3068  LOAD_CONST               ('hours', 'minutes', 'seconds')
             3070  COMPARE_OP               in
         3072_3074  POP_JUMP_IF_FALSE  3134  'to 3134'

 L.1057      3076  LOAD_FAST                'used'
             3078  LOAD_CONST               3
             3080  INPLACE_ADD      
             3082  STORE_FAST               'used'

 L.1058      3084  LOAD_FAST                'wordNextNext'
             3086  LOAD_STR                 'hours'
             3088  COMPARE_OP               ==
         3090_3092  POP_JUMP_IF_FALSE  3100  'to 3100'

 L.1059      3094  LOAD_CONST               2
             3096  STORE_DEREF              'hrOffset'
             3098  JUMP_FORWARD       5838  'to 5838'
           3100_0  COME_FROM          3090  '3090'

 L.1060      3100  LOAD_FAST                'wordNextNext'
             3102  LOAD_STR                 'minutes'
             3104  COMPARE_OP               ==
         3106_3108  POP_JUMP_IF_FALSE  3116  'to 3116'

 L.1061      3110  LOAD_CONST               2
             3112  STORE_DEREF              'minOffset'
             3114  JUMP_FORWARD       5838  'to 5838'
           3116_0  COME_FROM          3106  '3106'

 L.1062      3116  LOAD_FAST                'wordNextNext'
             3118  LOAD_STR                 'seconds'
             3120  COMPARE_OP               ==
         3122_3124  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1063      3126  LOAD_CONST               2
             3128  STORE_DEREF              'secOffset'
         3130_3132  JUMP_FORWARD       5838  'to 5838'
           3134_0  COME_FROM          3072  '3072'
           3134_1  COME_FROM          3062  '3062'
           3134_2  COME_FROM          3052  '3052'

 L.1065      3134  LOAD_FAST                'word'
             3136  LOAD_STR                 'hour'
             3138  COMPARE_OP               ==
         3140_3142  POP_JUMP_IF_FALSE  3352  'to 3352'

 L.1066      3144  LOAD_FAST                'wordPrev'
             3146  LOAD_FAST                'markers'
             3148  COMPARE_OP               in
         3150_3152  POP_JUMP_IF_TRUE   3164  'to 3164'
             3154  LOAD_FAST                'wordPrevPrev'
             3156  LOAD_FAST                'markers'
             3158  COMPARE_OP               in
         3160_3162  POP_JUMP_IF_FALSE  3352  'to 3352'
           3164_0  COME_FROM          3150  '3150'

 L.1067      3164  LOAD_FAST                'wordPrev'
             3166  LOAD_STR                 'half'
             3168  COMPARE_OP               ==
         3170_3172  POP_JUMP_IF_FALSE  3180  'to 3180'

 L.1068      3174  LOAD_CONST               30
             3176  STORE_DEREF              'minOffset'
             3178  JUMP_FORWARD       3284  'to 3284'
           3180_0  COME_FROM          3170  '3170'

 L.1069      3180  LOAD_FAST                'wordPrev'
             3182  LOAD_STR                 'quarter'
             3184  COMPARE_OP               ==
         3186_3188  POP_JUMP_IF_FALSE  3196  'to 3196'

 L.1070      3190  LOAD_CONST               15
             3192  STORE_DEREF              'minOffset'
             3194  JUMP_FORWARD       3284  'to 3284'
           3196_0  COME_FROM          3186  '3186'

 L.1071      3196  LOAD_FAST                'wordPrevPrev'
             3198  LOAD_STR                 'quarter'
             3200  COMPARE_OP               ==
         3202_3204  POP_JUMP_IF_FALSE  3264  'to 3264'

 L.1072      3206  LOAD_CONST               15
             3208  STORE_DEREF              'minOffset'

 L.1073      3210  LOAD_FAST                'idx'
             3212  LOAD_CONST               2
             3214  COMPARE_OP               >
         3216_3218  POP_JUMP_IF_FALSE  3250  'to 3250'
             3220  LOAD_FAST                'words'
             3222  LOAD_FAST                'idx'
             3224  LOAD_CONST               3
             3226  BINARY_SUBTRACT  
             3228  BINARY_SUBSCR    
             3230  LOAD_FAST                'markers'
             3232  COMPARE_OP               in
         3234_3236  POP_JUMP_IF_FALSE  3250  'to 3250'

 L.1074      3238  LOAD_STR                 ''
             3240  LOAD_FAST                'words'
             3242  LOAD_FAST                'idx'
             3244  LOAD_CONST               3
             3246  BINARY_SUBTRACT  
             3248  STORE_SUBSCR     
           3250_0  COME_FROM          3234  '3234'
           3250_1  COME_FROM          3216  '3216'

 L.1075      3250  LOAD_STR                 ''
             3252  LOAD_FAST                'words'
             3254  LOAD_FAST                'idx'
             3256  LOAD_CONST               2
             3258  BINARY_SUBTRACT  
             3260  STORE_SUBSCR     
             3262  JUMP_FORWARD       3284  'to 3284'
           3264_0  COME_FROM          3202  '3202'

 L.1076      3264  LOAD_FAST                'wordPrev'
             3266  LOAD_STR                 'within'
             3268  COMPARE_OP               ==
         3270_3272  POP_JUMP_IF_FALSE  3280  'to 3280'

 L.1077      3274  LOAD_CONST               1
             3276  STORE_DEREF              'hrOffset'
             3278  JUMP_FORWARD       3284  'to 3284'
           3280_0  COME_FROM          3270  '3270'

 L.1079      3280  LOAD_CONST               1
             3282  STORE_DEREF              'hrOffset'
           3284_0  COME_FROM          3278  '3278'
           3284_1  COME_FROM          3262  '3262'
           3284_2  COME_FROM          3194  '3194'
           3284_3  COME_FROM          3178  '3178'

 L.1080      3284  LOAD_FAST                'wordPrevPrev'
             3286  LOAD_FAST                'markers'
             3288  COMPARE_OP               in
         3290_3292  POP_JUMP_IF_FALSE  3320  'to 3320'

 L.1081      3294  LOAD_STR                 ''
             3296  LOAD_FAST                'words'
             3298  LOAD_FAST                'idx'
             3300  LOAD_CONST               2
             3302  BINARY_SUBTRACT  
             3304  STORE_SUBSCR     

 L.1082      3306  LOAD_FAST                'wordPrevPrev'
             3308  LOAD_STR                 'this'
             3310  COMPARE_OP               ==
         3312_3314  POP_JUMP_IF_FALSE  3320  'to 3320'

 L.1083      3316  LOAD_CONST               True
             3318  STORE_FAST               'daySpecified'
           3320_0  COME_FROM          3312  '3312'
           3320_1  COME_FROM          3290  '3290'

 L.1084      3320  LOAD_STR                 ''
             3322  LOAD_FAST                'words'
             3324  LOAD_FAST                'idx'
             3326  LOAD_CONST               1
             3328  BINARY_SUBTRACT  
             3330  STORE_SUBSCR     

 L.1085      3332  LOAD_FAST                'used'
             3334  LOAD_CONST               1
             3336  INPLACE_ADD      
             3338  STORE_FAST               'used'

 L.1086      3340  LOAD_CONST               -1
             3342  STORE_DEREF              'hrAbs'

 L.1087      3344  LOAD_CONST               -1
             3346  STORE_DEREF              'minAbs'
         3348_3350  JUMP_FORWARD       5838  'to 5838'
           3352_0  COME_FROM          3160  '3160'
           3352_1  COME_FROM          3140  '3140'

 L.1090      3352  LOAD_FAST                'word'
             3354  LOAD_STR                 'minute'
             3356  COMPARE_OP               ==
         3358_3360  POP_JUMP_IF_FALSE  3400  'to 3400'
             3362  LOAD_FAST                'wordPrev'
             3364  LOAD_STR                 'in'
             3366  COMPARE_OP               ==
         3368_3370  POP_JUMP_IF_FALSE  3400  'to 3400'

 L.1091      3372  LOAD_CONST               1
             3374  STORE_DEREF              'minOffset'

 L.1092      3376  LOAD_STR                 ''
             3378  LOAD_FAST                'words'
             3380  LOAD_FAST                'idx'
             3382  LOAD_CONST               1
             3384  BINARY_SUBTRACT  
             3386  STORE_SUBSCR     

 L.1093      3388  LOAD_FAST                'used'
             3390  LOAD_CONST               1
             3392  INPLACE_ADD      
             3394  STORE_FAST               'used'
         3396_3398  JUMP_FORWARD       5838  'to 5838'
           3400_0  COME_FROM          3368  '3368'
           3400_1  COME_FROM          3358  '3358'

 L.1095      3400  LOAD_FAST                'word'
             3402  LOAD_STR                 'second'
             3404  COMPARE_OP               ==
         3406_3408  POP_JUMP_IF_FALSE  3448  'to 3448'
             3410  LOAD_FAST                'wordPrev'
             3412  LOAD_STR                 'in'
             3414  COMPARE_OP               ==
         3416_3418  POP_JUMP_IF_FALSE  3448  'to 3448'

 L.1096      3420  LOAD_CONST               1
             3422  STORE_DEREF              'secOffset'

 L.1097      3424  LOAD_STR                 ''
             3426  LOAD_FAST                'words'
             3428  LOAD_FAST                'idx'
             3430  LOAD_CONST               1
             3432  BINARY_SUBTRACT  
             3434  STORE_SUBSCR     

 L.1098      3436  LOAD_FAST                'used'
             3438  LOAD_CONST               1
             3440  INPLACE_ADD      
             3442  STORE_FAST               'used'
         3444_3446  JUMP_FORWARD       5838  'to 5838'
           3448_0  COME_FROM          3416  '3416'
           3448_1  COME_FROM          3406  '3406'

 L.1099      3448  LOAD_FAST                'word'
             3450  LOAD_CONST               0
             3452  BINARY_SUBSCR    
             3454  LOAD_METHOD              isdigit
             3456  CALL_METHOD_0         0  '0 positional arguments'
         3458_3460  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1100      3462  LOAD_CONST               True
             3464  STORE_FAST               'isTime'

 L.1101      3466  LOAD_STR                 ''
             3468  STORE_FAST               'strHH'

 L.1102      3470  LOAD_STR                 ''
             3472  STORE_FAST               'strMM'

 L.1103      3474  LOAD_STR                 ''
             3476  STORE_FAST               'remainder'

 L.1105      3478  LOAD_FAST                'idx'
             3480  LOAD_CONST               3
             3482  BINARY_ADD       
             3484  LOAD_GLOBAL              len
             3486  LOAD_FAST                'words'
             3488  CALL_FUNCTION_1       1  '1 positional argument'
             3490  COMPARE_OP               <
         3492_3494  POP_JUMP_IF_FALSE  3508  'to 3508'
             3496  LOAD_FAST                'words'
             3498  LOAD_FAST                'idx'
             3500  LOAD_CONST               3
             3502  BINARY_ADD       
             3504  BINARY_SUBSCR    
             3506  JUMP_FORWARD       3510  'to 3510'
           3508_0  COME_FROM          3492  '3492'
             3508  LOAD_STR                 ''
           3510_0  COME_FROM          3506  '3506'
             3510  STORE_FAST               'wordNextNextNext'

 L.1106      3512  LOAD_FAST                'wordNext'
             3514  LOAD_STR                 'tonight'
             3516  COMPARE_OP               ==
         3518_3520  POP_JUMP_IF_TRUE   3562  'to 3562'
             3522  LOAD_FAST                'wordNextNext'
             3524  LOAD_STR                 'tonight'
             3526  COMPARE_OP               ==
         3528_3530  POP_JUMP_IF_TRUE   3562  'to 3562'

 L.1107      3532  LOAD_FAST                'wordPrev'
             3534  LOAD_STR                 'tonight'
             3536  COMPARE_OP               ==
         3538_3540  POP_JUMP_IF_TRUE   3562  'to 3562'
             3542  LOAD_FAST                'wordPrevPrev'
             3544  LOAD_STR                 'tonight'
             3546  COMPARE_OP               ==
         3548_3550  POP_JUMP_IF_TRUE   3562  'to 3562'

 L.1108      3552  LOAD_FAST                'wordNextNextNext'
             3554  LOAD_STR                 'tonight'
             3556  COMPARE_OP               ==
         3558_3560  POP_JUMP_IF_FALSE  3654  'to 3654'
           3562_0  COME_FROM          3548  '3548'
           3562_1  COME_FROM          3538  '3538'
           3562_2  COME_FROM          3528  '3528'
           3562_3  COME_FROM          3518  '3518'

 L.1109      3562  LOAD_STR                 'pm'
             3564  STORE_FAST               'remainder'

 L.1110      3566  LOAD_FAST                'used'
             3568  LOAD_CONST               1
             3570  INPLACE_ADD      
             3572  STORE_FAST               'used'

 L.1111      3574  LOAD_FAST                'wordPrev'
             3576  LOAD_STR                 'tonight'
             3578  COMPARE_OP               ==
         3580_3582  POP_JUMP_IF_FALSE  3596  'to 3596'

 L.1112      3584  LOAD_STR                 ''
             3586  LOAD_FAST                'words'
             3588  LOAD_FAST                'idx'
             3590  LOAD_CONST               1
             3592  BINARY_SUBTRACT  
             3594  STORE_SUBSCR     
           3596_0  COME_FROM          3580  '3580'

 L.1113      3596  LOAD_FAST                'wordPrevPrev'
             3598  LOAD_STR                 'tonight'
             3600  COMPARE_OP               ==
         3602_3604  POP_JUMP_IF_FALSE  3618  'to 3618'

 L.1114      3606  LOAD_STR                 ''
             3608  LOAD_FAST                'words'
             3610  LOAD_FAST                'idx'
             3612  LOAD_CONST               2
             3614  BINARY_SUBTRACT  
             3616  STORE_SUBSCR     
           3618_0  COME_FROM          3602  '3602'

 L.1115      3618  LOAD_FAST                'wordNextNext'
             3620  LOAD_STR                 'tonight'
             3622  COMPARE_OP               ==
         3624_3626  POP_JUMP_IF_FALSE  3636  'to 3636'

 L.1116      3628  LOAD_FAST                'used'
             3630  LOAD_CONST               1
             3632  INPLACE_ADD      
             3634  STORE_FAST               'used'
           3636_0  COME_FROM          3624  '3624'

 L.1117      3636  LOAD_FAST                'wordNextNextNext'
             3638  LOAD_STR                 'tonight'
             3640  COMPARE_OP               ==
         3642_3644  POP_JUMP_IF_FALSE  3654  'to 3654'

 L.1118      3646  LOAD_FAST                'used'
             3648  LOAD_CONST               1
             3650  INPLACE_ADD      
             3652  STORE_FAST               'used'
           3654_0  COME_FROM          3642  '3642'
           3654_1  COME_FROM          3558  '3558'

 L.1120      3654  LOAD_STR                 ':'
             3656  LOAD_FAST                'word'
             3658  COMPARE_OP               in
         3660_3662  POP_JUMP_IF_FALSE  4408  'to 4408'

 L.1123      3664  LOAD_CONST               0
             3666  STORE_FAST               'stage'

 L.1124      3668  LOAD_GLOBAL              len
             3670  LOAD_FAST                'word'
             3672  CALL_FUNCTION_1       1  '1 positional argument'
             3674  STORE_FAST               'length'

 L.1125      3676  SETUP_LOOP         3852  'to 3852'
             3678  LOAD_GLOBAL              range
             3680  LOAD_FAST                'length'
             3682  CALL_FUNCTION_1       1  '1 positional argument'
             3684  GET_ITER         
           3686_0  COME_FROM          3820  '3820'
             3686  FOR_ITER           3850  'to 3850'
             3688  STORE_FAST               'i'

 L.1126      3690  LOAD_FAST                'stage'
             3692  LOAD_CONST               0
             3694  COMPARE_OP               ==
         3696_3698  POP_JUMP_IF_FALSE  3762  'to 3762'

 L.1127      3700  LOAD_FAST                'word'
             3702  LOAD_FAST                'i'
             3704  BINARY_SUBSCR    
             3706  LOAD_METHOD              isdigit
             3708  CALL_METHOD_0         0  '0 positional arguments'
         3710_3712  POP_JUMP_IF_FALSE  3728  'to 3728'

 L.1128      3714  LOAD_FAST                'strHH'
             3716  LOAD_FAST                'word'
             3718  LOAD_FAST                'i'
             3720  BINARY_SUBSCR    
             3722  INPLACE_ADD      
             3724  STORE_FAST               'strHH'
             3726  JUMP_FORWARD       3760  'to 3760'
           3728_0  COME_FROM          3710  '3710'

 L.1129      3728  LOAD_FAST                'word'
             3730  LOAD_FAST                'i'
             3732  BINARY_SUBSCR    
             3734  LOAD_STR                 ':'
             3736  COMPARE_OP               ==
         3738_3740  POP_JUMP_IF_FALSE  3748  'to 3748'

 L.1130      3742  LOAD_CONST               1
             3744  STORE_FAST               'stage'
             3746  JUMP_FORWARD       3760  'to 3760'
           3748_0  COME_FROM          3738  '3738'

 L.1132      3748  LOAD_CONST               2
             3750  STORE_FAST               'stage'

 L.1133      3752  LOAD_FAST                'i'
             3754  LOAD_CONST               1
             3756  INPLACE_SUBTRACT 
             3758  STORE_FAST               'i'
           3760_0  COME_FROM          3746  '3746'
           3760_1  COME_FROM          3726  '3726'
             3760  JUMP_BACK          3686  'to 3686'
           3762_0  COME_FROM          3696  '3696'

 L.1134      3762  LOAD_FAST                'stage'
             3764  LOAD_CONST               1
             3766  COMPARE_OP               ==
         3768_3770  POP_JUMP_IF_FALSE  3814  'to 3814'

 L.1135      3772  LOAD_FAST                'word'
             3774  LOAD_FAST                'i'
             3776  BINARY_SUBSCR    
             3778  LOAD_METHOD              isdigit
             3780  CALL_METHOD_0         0  '0 positional arguments'
         3782_3784  POP_JUMP_IF_FALSE  3800  'to 3800'

 L.1136      3786  LOAD_FAST                'strMM'
             3788  LOAD_FAST                'word'
             3790  LOAD_FAST                'i'
             3792  BINARY_SUBSCR    
             3794  INPLACE_ADD      
             3796  STORE_FAST               'strMM'
             3798  JUMP_FORWARD       3812  'to 3812'
           3800_0  COME_FROM          3782  '3782'

 L.1138      3800  LOAD_CONST               2
             3802  STORE_FAST               'stage'

 L.1139      3804  LOAD_FAST                'i'
             3806  LOAD_CONST               1
             3808  INPLACE_SUBTRACT 
             3810  STORE_FAST               'i'
           3812_0  COME_FROM          3798  '3798'
             3812  JUMP_BACK          3686  'to 3686'
           3814_0  COME_FROM          3768  '3768'

 L.1140      3814  LOAD_FAST                'stage'
             3816  LOAD_CONST               2
             3818  COMPARE_OP               ==
         3820_3822  POP_JUMP_IF_FALSE  3686  'to 3686'

 L.1141      3824  LOAD_FAST                'word'
             3826  LOAD_FAST                'i'
             3828  LOAD_CONST               None
             3830  BUILD_SLICE_2         2 
             3832  BINARY_SUBSCR    
             3834  LOAD_METHOD              replace
             3836  LOAD_STR                 '.'
             3838  LOAD_STR                 ''
             3840  CALL_METHOD_2         2  '2 positional arguments'
             3842  STORE_FAST               'remainder'

 L.1142      3844  BREAK_LOOP       
         3846_3848  JUMP_BACK          3686  'to 3686'
             3850  POP_BLOCK        
           3852_0  COME_FROM_LOOP     3676  '3676'

 L.1143      3852  LOAD_FAST                'remainder'
             3854  LOAD_STR                 ''
             3856  COMPARE_OP               ==
         3858_3860  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1144      3862  LOAD_FAST                'wordNext'
             3864  LOAD_METHOD              replace
             3866  LOAD_STR                 '.'
             3868  LOAD_STR                 ''
             3870  CALL_METHOD_2         2  '2 positional arguments'
             3872  STORE_FAST               'nextWord'

 L.1145      3874  LOAD_FAST                'nextWord'
             3876  LOAD_STR                 'am'
             3878  COMPARE_OP               ==
         3880_3882  POP_JUMP_IF_TRUE   3894  'to 3894'
             3884  LOAD_FAST                'nextWord'
             3886  LOAD_STR                 'pm'
             3888  COMPARE_OP               ==
         3890_3892  POP_JUMP_IF_FALSE  3910  'to 3910'
           3894_0  COME_FROM          3880  '3880'

 L.1146      3894  LOAD_FAST                'nextWord'
             3896  STORE_FAST               'remainder'

 L.1147      3898  LOAD_FAST                'used'
             3900  LOAD_CONST               1
             3902  INPLACE_ADD      
             3904  STORE_FAST               'used'
         3906_3908  JUMP_ABSOLUTE      5538  'to 5538'
           3910_0  COME_FROM          3890  '3890'

 L.1149      3910  LOAD_FAST                'wordNext'
             3912  LOAD_STR                 'in'
             3914  COMPARE_OP               ==
         3916_3918  POP_JUMP_IF_FALSE  3964  'to 3964'
             3920  LOAD_FAST                'wordNextNext'
             3922  LOAD_STR                 'the'
             3924  COMPARE_OP               ==
         3926_3928  POP_JUMP_IF_FALSE  3964  'to 3964'

 L.1150      3930  LOAD_FAST                'words'
             3932  LOAD_FAST                'idx'
             3934  LOAD_CONST               3
             3936  BINARY_ADD       
             3938  BINARY_SUBSCR    
             3940  LOAD_STR                 'morning'
             3942  COMPARE_OP               ==
         3944_3946  POP_JUMP_IF_FALSE  3964  'to 3964'

 L.1151      3948  LOAD_STR                 'am'
             3950  STORE_FAST               'remainder'

 L.1152      3952  LOAD_FAST                'used'
             3954  LOAD_CONST               3
             3956  INPLACE_ADD      
             3958  STORE_FAST               'used'
         3960_3962  JUMP_ABSOLUTE      5538  'to 5538'
           3964_0  COME_FROM          3944  '3944'
           3964_1  COME_FROM          3926  '3926'
           3964_2  COME_FROM          3916  '3916'

 L.1153      3964  LOAD_FAST                'wordNext'
             3966  LOAD_STR                 'in'
             3968  COMPARE_OP               ==
         3970_3972  POP_JUMP_IF_FALSE  4018  'to 4018'
             3974  LOAD_FAST                'wordNextNext'
             3976  LOAD_STR                 'the'
             3978  COMPARE_OP               ==
         3980_3982  POP_JUMP_IF_FALSE  4018  'to 4018'

 L.1154      3984  LOAD_FAST                'words'
             3986  LOAD_FAST                'idx'
             3988  LOAD_CONST               3
             3990  BINARY_ADD       
             3992  BINARY_SUBSCR    
             3994  LOAD_STR                 'afternoon'
             3996  COMPARE_OP               ==
         3998_4000  POP_JUMP_IF_FALSE  4018  'to 4018'

 L.1155      4002  LOAD_STR                 'pm'
             4004  STORE_FAST               'remainder'

 L.1156      4006  LOAD_FAST                'used'
             4008  LOAD_CONST               3
             4010  INPLACE_ADD      
             4012  STORE_FAST               'used'
         4014_4016  JUMP_ABSOLUTE      5538  'to 5538'
           4018_0  COME_FROM          3998  '3998'
           4018_1  COME_FROM          3980  '3980'
           4018_2  COME_FROM          3970  '3970'

 L.1157      4018  LOAD_FAST                'wordNext'
             4020  LOAD_STR                 'in'
             4022  COMPARE_OP               ==
         4024_4026  POP_JUMP_IF_FALSE  4072  'to 4072'
             4028  LOAD_FAST                'wordNextNext'
             4030  LOAD_STR                 'the'
             4032  COMPARE_OP               ==
         4034_4036  POP_JUMP_IF_FALSE  4072  'to 4072'

 L.1158      4038  LOAD_FAST                'words'
             4040  LOAD_FAST                'idx'
             4042  LOAD_CONST               3
             4044  BINARY_ADD       
             4046  BINARY_SUBSCR    
             4048  LOAD_STR                 'evening'
             4050  COMPARE_OP               ==
         4052_4054  POP_JUMP_IF_FALSE  4072  'to 4072'

 L.1159      4056  LOAD_STR                 'pm'
             4058  STORE_FAST               'remainder'

 L.1160      4060  LOAD_FAST                'used'
             4062  LOAD_CONST               3
             4064  INPLACE_ADD      
             4066  STORE_FAST               'used'
         4068_4070  JUMP_ABSOLUTE      5538  'to 5538'
           4072_0  COME_FROM          4052  '4052'
           4072_1  COME_FROM          4034  '4034'
           4072_2  COME_FROM          4024  '4024'

 L.1161      4072  LOAD_FAST                'wordNext'
             4074  LOAD_STR                 'in'
             4076  COMPARE_OP               ==
         4078_4080  POP_JUMP_IF_FALSE  4108  'to 4108'
             4082  LOAD_FAST                'wordNextNext'
             4084  LOAD_STR                 'morning'
             4086  COMPARE_OP               ==
         4088_4090  POP_JUMP_IF_FALSE  4108  'to 4108'

 L.1162      4092  LOAD_STR                 'am'
             4094  STORE_FAST               'remainder'

 L.1163      4096  LOAD_FAST                'used'
             4098  LOAD_CONST               2
             4100  INPLACE_ADD      
             4102  STORE_FAST               'used'
         4104_4106  JUMP_ABSOLUTE      5538  'to 5538'
           4108_0  COME_FROM          4088  '4088'
           4108_1  COME_FROM          4078  '4078'

 L.1164      4108  LOAD_FAST                'wordNext'
             4110  LOAD_STR                 'in'
             4112  COMPARE_OP               ==
         4114_4116  POP_JUMP_IF_FALSE  4144  'to 4144'
             4118  LOAD_FAST                'wordNextNext'
             4120  LOAD_STR                 'afternoon'
             4122  COMPARE_OP               ==
         4124_4126  POP_JUMP_IF_FALSE  4144  'to 4144'

 L.1165      4128  LOAD_STR                 'pm'
             4130  STORE_FAST               'remainder'

 L.1166      4132  LOAD_FAST                'used'
             4134  LOAD_CONST               2
             4136  INPLACE_ADD      
             4138  STORE_FAST               'used'
         4140_4142  JUMP_ABSOLUTE      5538  'to 5538'
           4144_0  COME_FROM          4124  '4124'
           4144_1  COME_FROM          4114  '4114'

 L.1167      4144  LOAD_FAST                'wordNext'
             4146  LOAD_STR                 'in'
             4148  COMPARE_OP               ==
         4150_4152  POP_JUMP_IF_FALSE  4178  'to 4178'
             4154  LOAD_FAST                'wordNextNext'
             4156  LOAD_STR                 'evening'
             4158  COMPARE_OP               ==
         4160_4162  POP_JUMP_IF_FALSE  4178  'to 4178'

 L.1168      4164  LOAD_STR                 'pm'
             4166  STORE_FAST               'remainder'

 L.1169      4168  LOAD_FAST                'used'
             4170  LOAD_CONST               2
             4172  INPLACE_ADD      
             4174  STORE_FAST               'used'
             4176  JUMP_FORWARD       5538  'to 5538'
           4178_0  COME_FROM          4160  '4160'
           4178_1  COME_FROM          4150  '4150'

 L.1170      4178  LOAD_FAST                'wordNext'
             4180  LOAD_STR                 'this'
             4182  COMPARE_OP               ==
         4184_4186  POP_JUMP_IF_FALSE  4212  'to 4212'
             4188  LOAD_FAST                'wordNextNext'
             4190  LOAD_STR                 'morning'
             4192  COMPARE_OP               ==
         4194_4196  POP_JUMP_IF_FALSE  4212  'to 4212'

 L.1171      4198  LOAD_STR                 'am'
             4200  STORE_FAST               'remainder'

 L.1172      4202  LOAD_CONST               2
             4204  STORE_FAST               'used'

 L.1173      4206  LOAD_CONST               True
             4208  STORE_FAST               'daySpecified'
             4210  JUMP_FORWARD       5538  'to 5538'
           4212_0  COME_FROM          4194  '4194'
           4212_1  COME_FROM          4184  '4184'

 L.1174      4212  LOAD_FAST                'wordNext'
             4214  LOAD_STR                 'this'
             4216  COMPARE_OP               ==
         4218_4220  POP_JUMP_IF_FALSE  4246  'to 4246'
             4222  LOAD_FAST                'wordNextNext'
             4224  LOAD_STR                 'afternoon'
             4226  COMPARE_OP               ==
         4228_4230  POP_JUMP_IF_FALSE  4246  'to 4246'

 L.1175      4232  LOAD_STR                 'pm'
             4234  STORE_FAST               'remainder'

 L.1176      4236  LOAD_CONST               2
             4238  STORE_FAST               'used'

 L.1177      4240  LOAD_CONST               True
             4242  STORE_FAST               'daySpecified'
             4244  JUMP_FORWARD       5538  'to 5538'
           4246_0  COME_FROM          4228  '4228'
           4246_1  COME_FROM          4218  '4218'

 L.1178      4246  LOAD_FAST                'wordNext'
             4248  LOAD_STR                 'this'
             4250  COMPARE_OP               ==
         4252_4254  POP_JUMP_IF_FALSE  4280  'to 4280'
             4256  LOAD_FAST                'wordNextNext'
             4258  LOAD_STR                 'evening'
             4260  COMPARE_OP               ==
         4262_4264  POP_JUMP_IF_FALSE  4280  'to 4280'

 L.1179      4266  LOAD_STR                 'pm'
             4268  STORE_FAST               'remainder'

 L.1180      4270  LOAD_CONST               2
             4272  STORE_FAST               'used'

 L.1181      4274  LOAD_CONST               True
             4276  STORE_FAST               'daySpecified'
             4278  JUMP_FORWARD       5538  'to 5538'
           4280_0  COME_FROM          4262  '4262'
           4280_1  COME_FROM          4252  '4252'

 L.1182      4280  LOAD_FAST                'wordNext'
             4282  LOAD_STR                 'at'
             4284  COMPARE_OP               ==
         4286_4288  POP_JUMP_IF_FALSE  4340  'to 4340'
             4290  LOAD_FAST                'wordNextNext'
             4292  LOAD_STR                 'night'
             4294  COMPARE_OP               ==
         4296_4298  POP_JUMP_IF_FALSE  4340  'to 4340'

 L.1183      4300  LOAD_FAST                'strHH'
         4302_4304  POP_JUMP_IF_FALSE  4326  'to 4326'
             4306  LOAD_GLOBAL              int
             4308  LOAD_FAST                'strHH'
             4310  CALL_FUNCTION_1       1  '1 positional argument'
             4312  LOAD_CONST               5
             4314  COMPARE_OP               >
         4316_4318  POP_JUMP_IF_FALSE  4326  'to 4326'

 L.1184      4320  LOAD_STR                 'pm'
             4322  STORE_FAST               'remainder'
             4324  JUMP_FORWARD       4330  'to 4330'
           4326_0  COME_FROM          4316  '4316'
           4326_1  COME_FROM          4302  '4302'

 L.1186      4326  LOAD_STR                 'am'
             4328  STORE_FAST               'remainder'
           4330_0  COME_FROM          4324  '4324'

 L.1187      4330  LOAD_FAST                'used'
             4332  LOAD_CONST               2
             4334  INPLACE_ADD      
             4336  STORE_FAST               'used'
             4338  JUMP_FORWARD       5538  'to 5538'
           4340_0  COME_FROM          4296  '4296'
           4340_1  COME_FROM          4286  '4286'

 L.1190      4340  LOAD_FAST                'timeQualifier'
             4342  LOAD_STR                 ''
             4344  COMPARE_OP               !=
         4346_4348  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1191      4350  LOAD_CONST               True
             4352  STORE_FAST               'military'

 L.1192      4354  LOAD_FAST                'strHH'
         4356_4358  POP_JUMP_IF_FALSE  5538  'to 5538'
             4360  LOAD_GLOBAL              int
             4362  LOAD_FAST                'strHH'
             4364  CALL_FUNCTION_1       1  '1 positional argument'
             4366  LOAD_CONST               12
             4368  COMPARE_OP               <=
         4370_4372  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1193      4374  LOAD_FAST                'timeQualifier'
             4376  LOAD_FAST                'timeQualifiersPM'
             4378  COMPARE_OP               in
         4380_4382  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1194      4384  LOAD_FAST                'strHH'
             4386  LOAD_GLOBAL              str
             4388  LOAD_GLOBAL              int
             4390  LOAD_FAST                'strHH'
             4392  CALL_FUNCTION_1       1  '1 positional argument'
             4394  LOAD_CONST               12
             4396  BINARY_ADD       
             4398  CALL_FUNCTION_1       1  '1 positional argument'
             4400  INPLACE_ADD      
             4402  STORE_FAST               'strHH'
         4404_4406  JUMP_FORWARD       5538  'to 5538'
           4408_0  COME_FROM          3660  '3660'

 L.1199      4408  LOAD_GLOBAL              len
             4410  LOAD_FAST                'word'
             4412  CALL_FUNCTION_1       1  '1 positional argument'
             4414  STORE_FAST               'length'

 L.1200      4416  LOAD_STR                 ''
             4418  STORE_FAST               'strNum'

 L.1201      4420  LOAD_STR                 ''
             4422  STORE_FAST               'remainder'

 L.1202      4424  SETUP_LOOP         4484  'to 4484'
             4426  LOAD_GLOBAL              range
             4428  LOAD_FAST                'length'
             4430  CALL_FUNCTION_1       1  '1 positional argument'
             4432  GET_ITER         
             4434  FOR_ITER           4482  'to 4482'
             4436  STORE_FAST               'i'

 L.1203      4438  LOAD_FAST                'word'
             4440  LOAD_FAST                'i'
             4442  BINARY_SUBSCR    
             4444  LOAD_METHOD              isdigit
             4446  CALL_METHOD_0         0  '0 positional arguments'
         4448_4450  POP_JUMP_IF_FALSE  4466  'to 4466'

 L.1204      4452  LOAD_FAST                'strNum'
             4454  LOAD_FAST                'word'
             4456  LOAD_FAST                'i'
             4458  BINARY_SUBSCR    
             4460  INPLACE_ADD      
             4462  STORE_FAST               'strNum'
             4464  JUMP_BACK          4434  'to 4434'
           4466_0  COME_FROM          4448  '4448'

 L.1206      4466  LOAD_FAST                'remainder'
             4468  LOAD_FAST                'word'
             4470  LOAD_FAST                'i'
             4472  BINARY_SUBSCR    
             4474  INPLACE_ADD      
             4476  STORE_FAST               'remainder'
         4478_4480  JUMP_BACK          4434  'to 4434'
             4482  POP_BLOCK        
           4484_0  COME_FROM_LOOP     4424  '4424'

 L.1208      4484  LOAD_FAST                'remainder'
             4486  LOAD_STR                 ''
             4488  COMPARE_OP               ==
         4490_4492  POP_JUMP_IF_FALSE  4514  'to 4514'

 L.1209      4494  LOAD_FAST                'wordNext'
             4496  LOAD_METHOD              replace
             4498  LOAD_STR                 '.'
             4500  LOAD_STR                 ''
             4502  CALL_METHOD_2         2  '2 positional arguments'
             4504  LOAD_METHOD              lstrip
             4506  CALL_METHOD_0         0  '0 positional arguments'
             4508  LOAD_METHOD              rstrip
             4510  CALL_METHOD_0         0  '0 positional arguments'
             4512  STORE_FAST               'remainder'
           4514_0  COME_FROM          4490  '4490'

 L.1211      4514  LOAD_FAST                'remainder'
             4516  LOAD_STR                 'pm'
             4518  COMPARE_OP               ==
         4520_4522  POP_JUMP_IF_TRUE   4554  'to 4554'

 L.1212      4524  LOAD_FAST                'wordNext'
             4526  LOAD_STR                 'pm'
             4528  COMPARE_OP               ==
         4530_4532  POP_JUMP_IF_TRUE   4554  'to 4554'

 L.1213      4534  LOAD_FAST                'remainder'
             4536  LOAD_STR                 'p.m.'
             4538  COMPARE_OP               ==
         4540_4542  POP_JUMP_IF_TRUE   4554  'to 4554'

 L.1214      4544  LOAD_FAST                'wordNext'
             4546  LOAD_STR                 'p.m.'
             4548  COMPARE_OP               ==
         4550_4552  POP_JUMP_IF_FALSE  4570  'to 4570'
           4554_0  COME_FROM          4540  '4540'
           4554_1  COME_FROM          4530  '4530'
           4554_2  COME_FROM          4520  '4520'

 L.1215      4554  LOAD_FAST                'strNum'
             4556  STORE_FAST               'strHH'

 L.1216      4558  LOAD_STR                 'pm'
             4560  STORE_FAST               'remainder'

 L.1217      4562  LOAD_CONST               1
             4564  STORE_FAST               'used'
         4566_4568  JUMP_FORWARD       5538  'to 5538'
           4570_0  COME_FROM          4550  '4550'

 L.1219      4570  LOAD_FAST                'remainder'
             4572  LOAD_STR                 'am'
             4574  COMPARE_OP               ==
         4576_4578  POP_JUMP_IF_TRUE   4610  'to 4610'

 L.1220      4580  LOAD_FAST                'wordNext'
             4582  LOAD_STR                 'am'
             4584  COMPARE_OP               ==
         4586_4588  POP_JUMP_IF_TRUE   4610  'to 4610'

 L.1221      4590  LOAD_FAST                'remainder'
             4592  LOAD_STR                 'a.m.'
             4594  COMPARE_OP               ==
         4596_4598  POP_JUMP_IF_TRUE   4610  'to 4610'

 L.1222      4600  LOAD_FAST                'wordNext'
             4602  LOAD_STR                 'a.m.'
             4604  COMPARE_OP               ==
         4606_4608  POP_JUMP_IF_FALSE  4626  'to 4626'
           4610_0  COME_FROM          4596  '4596'
           4610_1  COME_FROM          4586  '4586'
           4610_2  COME_FROM          4576  '4576'

 L.1223      4610  LOAD_FAST                'strNum'
             4612  STORE_FAST               'strHH'

 L.1224      4614  LOAD_STR                 'am'
             4616  STORE_FAST               'remainder'

 L.1225      4618  LOAD_CONST               1
             4620  STORE_FAST               'used'
         4622_4624  JUMP_FORWARD       5538  'to 5538'
           4626_0  COME_FROM          4606  '4606'

 L.1227      4626  LOAD_FAST                'remainder'
             4628  LOAD_FAST                'recur_markers'
             4630  COMPARE_OP               in
         4632_4634  POP_JUMP_IF_TRUE   4656  'to 4656'

 L.1228      4636  LOAD_FAST                'wordNext'
             4638  LOAD_FAST                'recur_markers'
             4640  COMPARE_OP               in
         4642_4644  POP_JUMP_IF_TRUE   4656  'to 4656'

 L.1229      4646  LOAD_FAST                'wordNextNext'
             4648  LOAD_FAST                'recur_markers'
             4650  COMPARE_OP               in
         4652_4654  POP_JUMP_IF_FALSE  4668  'to 4668'
           4656_0  COME_FROM          4642  '4642'
           4656_1  COME_FROM          4632  '4632'

 L.1233      4656  LOAD_FAST                'strNum'
             4658  STORE_FAST               'strHH'

 L.1234      4660  LOAD_CONST               1
             4662  STORE_FAST               'used'
         4664_4666  JUMP_FORWARD       5538  'to 5538'
           4668_0  COME_FROM          4652  '4652'

 L.1237      4668  LOAD_GLOBAL              int
             4670  LOAD_FAST                'strNum'
             4672  CALL_FUNCTION_1       1  '1 positional argument'
             4674  LOAD_CONST               100
             4676  COMPARE_OP               >
         4678_4680  POP_JUMP_IF_FALSE  4760  'to 4760'

 L.1239      4682  LOAD_FAST                'wordPrev'
             4684  LOAD_STR                 'o'
             4686  COMPARE_OP               ==
         4688_4690  POP_JUMP_IF_TRUE   4702  'to 4702'

 L.1240      4692  LOAD_FAST                'wordPrev'
             4694  LOAD_STR                 'oh'
             4696  COMPARE_OP               ==
         4698_4700  POP_JUMP_IF_FALSE  4760  'to 4760'
           4702_0  COME_FROM          4688  '4688'

 L.1243      4702  LOAD_GLOBAL              str
             4704  LOAD_GLOBAL              int
             4706  LOAD_FAST                'strNum'
             4708  CALL_FUNCTION_1       1  '1 positional argument'
             4710  LOAD_CONST               100
             4712  BINARY_FLOOR_DIVIDE
             4714  CALL_FUNCTION_1       1  '1 positional argument'
             4716  STORE_FAST               'strHH'

 L.1244      4718  LOAD_GLOBAL              str
             4720  LOAD_GLOBAL              int
             4722  LOAD_FAST                'strNum'
             4724  CALL_FUNCTION_1       1  '1 positional argument'
             4726  LOAD_CONST               100
             4728  BINARY_MODULO    
             4730  CALL_FUNCTION_1       1  '1 positional argument'
             4732  STORE_FAST               'strMM'

 L.1245      4734  LOAD_CONST               True
             4736  STORE_FAST               'military'

 L.1246      4738  LOAD_FAST                'wordNext'
             4740  LOAD_STR                 'hours'
             4742  COMPARE_OP               ==
         4744_4746  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1247      4748  LOAD_FAST                'used'
             4750  LOAD_CONST               1
             4752  INPLACE_ADD      
             4754  STORE_FAST               'used'
         4756_4758  JUMP_FORWARD       5538  'to 5538'
           4760_0  COME_FROM          4698  '4698'
           4760_1  COME_FROM          4678  '4678'

 L.1249      4760  LOAD_FAST                'wordNext'
             4762  LOAD_STR                 'hours'
             4764  COMPARE_OP               ==
         4766_4768  POP_JUMP_IF_TRUE   4800  'to 4800'
             4770  LOAD_FAST                'wordNext'
             4772  LOAD_STR                 'hour'
             4774  COMPARE_OP               ==
         4776_4778  POP_JUMP_IF_TRUE   4800  'to 4800'

 L.1250      4780  LOAD_FAST                'remainder'
             4782  LOAD_STR                 'hours'
             4784  COMPARE_OP               ==
         4786_4788  POP_JUMP_IF_TRUE   4800  'to 4800'
             4790  LOAD_FAST                'remainder'
             4792  LOAD_STR                 'hour'
             4794  COMPARE_OP               ==
         4796_4798  POP_JUMP_IF_FALSE  4870  'to 4870'
           4800_0  COME_FROM          4786  '4786'
           4800_1  COME_FROM          4776  '4776'
           4800_2  COME_FROM          4766  '4766'

 L.1251      4800  LOAD_FAST                'word'
             4802  LOAD_CONST               0
             4804  BINARY_SUBSCR    
             4806  LOAD_STR                 '0'
             4808  COMPARE_OP               !=
         4810_4812  POP_JUMP_IF_FALSE  4870  'to 4870'

 L.1253      4814  LOAD_GLOBAL              int
             4816  LOAD_FAST                'strNum'
             4818  CALL_FUNCTION_1       1  '1 positional argument'
             4820  LOAD_CONST               100
             4822  COMPARE_OP               <
         4824_4826  POP_JUMP_IF_TRUE   4842  'to 4842'

 L.1254      4828  LOAD_GLOBAL              int
             4830  LOAD_FAST                'strNum'
             4832  CALL_FUNCTION_1       1  '1 positional argument'
             4834  LOAD_CONST               2400
             4836  COMPARE_OP               >
         4838_4840  POP_JUMP_IF_FALSE  4870  'to 4870'
           4842_0  COME_FROM          4824  '4824'

 L.1258      4842  LOAD_GLOBAL              int
             4844  LOAD_FAST                'strNum'
             4846  CALL_FUNCTION_1       1  '1 positional argument'
             4848  STORE_DEREF              'hrOffset'

 L.1259      4850  LOAD_CONST               2
             4852  STORE_FAST               'used'

 L.1260      4854  LOAD_CONST               False
             4856  STORE_FAST               'isTime'

 L.1261      4858  LOAD_CONST               -1
             4860  STORE_DEREF              'hrAbs'

 L.1262      4862  LOAD_CONST               -1
             4864  STORE_DEREF              'minAbs'
         4866_4868  JUMP_FORWARD       5538  'to 5538'
           4870_0  COME_FROM          4838  '4838'
           4870_1  COME_FROM          4810  '4810'
           4870_2  COME_FROM          4796  '4796'

 L.1264      4870  LOAD_FAST                'wordNext'
             4872  LOAD_STR                 'minutes'
             4874  COMPARE_OP               ==
         4876_4878  POP_JUMP_IF_TRUE   4910  'to 4910'
             4880  LOAD_FAST                'wordNext'
             4882  LOAD_STR                 'minute'
             4884  COMPARE_OP               ==
         4886_4888  POP_JUMP_IF_TRUE   4910  'to 4910'

 L.1265      4890  LOAD_FAST                'remainder'
             4892  LOAD_STR                 'minutes'
             4894  COMPARE_OP               ==
         4896_4898  POP_JUMP_IF_TRUE   4910  'to 4910'
             4900  LOAD_FAST                'remainder'
             4902  LOAD_STR                 'minute'
             4904  COMPARE_OP               ==
         4906_4908  POP_JUMP_IF_FALSE  4938  'to 4938'
           4910_0  COME_FROM          4896  '4896'
           4910_1  COME_FROM          4886  '4886'
           4910_2  COME_FROM          4876  '4876'

 L.1267      4910  LOAD_GLOBAL              int
             4912  LOAD_FAST                'strNum'
             4914  CALL_FUNCTION_1       1  '1 positional argument'
             4916  STORE_DEREF              'minOffset'

 L.1268      4918  LOAD_CONST               2
             4920  STORE_FAST               'used'

 L.1269      4922  LOAD_CONST               False
             4924  STORE_FAST               'isTime'

 L.1270      4926  LOAD_CONST               -1
             4928  STORE_DEREF              'hrAbs'

 L.1271      4930  LOAD_CONST               -1
             4932  STORE_DEREF              'minAbs'
         4934_4936  JUMP_FORWARD       5538  'to 5538'
           4938_0  COME_FROM          4906  '4906'

 L.1272      4938  LOAD_FAST                'wordNext'
             4940  LOAD_STR                 'seconds'
             4942  COMPARE_OP               ==
         4944_4946  POP_JUMP_IF_TRUE   4978  'to 4978'
             4948  LOAD_FAST                'wordNext'
             4950  LOAD_STR                 'second'
             4952  COMPARE_OP               ==
         4954_4956  POP_JUMP_IF_TRUE   4978  'to 4978'

 L.1273      4958  LOAD_FAST                'remainder'
             4960  LOAD_STR                 'seconds'
             4962  COMPARE_OP               ==
         4964_4966  POP_JUMP_IF_TRUE   4978  'to 4978'
             4968  LOAD_FAST                'remainder'
             4970  LOAD_STR                 'second'
             4972  COMPARE_OP               ==
         4974_4976  POP_JUMP_IF_FALSE  5006  'to 5006'
           4978_0  COME_FROM          4964  '4964'
           4978_1  COME_FROM          4954  '4954'
           4978_2  COME_FROM          4944  '4944'

 L.1275      4978  LOAD_GLOBAL              int
             4980  LOAD_FAST                'strNum'
             4982  CALL_FUNCTION_1       1  '1 positional argument'
             4984  STORE_DEREF              'secOffset'

 L.1276      4986  LOAD_CONST               2
             4988  STORE_FAST               'used'

 L.1277      4990  LOAD_CONST               False
             4992  STORE_FAST               'isTime'

 L.1278      4994  LOAD_CONST               -1
             4996  STORE_DEREF              'hrAbs'

 L.1279      4998  LOAD_CONST               -1
             5000  STORE_DEREF              'minAbs'
         5002_5004  JUMP_FORWARD       5538  'to 5538'
           5006_0  COME_FROM          4974  '4974'

 L.1280      5006  LOAD_GLOBAL              int
             5008  LOAD_FAST                'strNum'
             5010  CALL_FUNCTION_1       1  '1 positional argument'
             5012  LOAD_CONST               100
             5014  COMPARE_OP               >
         5016_5018  POP_JUMP_IF_FALSE  5108  'to 5108'

 L.1282      5020  LOAD_GLOBAL              str
             5022  LOAD_GLOBAL              int
             5024  LOAD_FAST                'strNum'
             5026  CALL_FUNCTION_1       1  '1 positional argument'
             5028  LOAD_CONST               100
             5030  BINARY_FLOOR_DIVIDE
             5032  CALL_FUNCTION_1       1  '1 positional argument'
             5034  STORE_FAST               'strHH'

 L.1283      5036  LOAD_GLOBAL              str
             5038  LOAD_GLOBAL              int
             5040  LOAD_FAST                'strNum'
             5042  CALL_FUNCTION_1       1  '1 positional argument'
             5044  LOAD_CONST               100
             5046  BINARY_MODULO    
             5048  CALL_FUNCTION_1       1  '1 positional argument'
             5050  STORE_FAST               'strMM'

 L.1284      5052  LOAD_CONST               True
             5054  STORE_FAST               'military'

 L.1285      5056  LOAD_FAST                'wordNext'
             5058  LOAD_STR                 'hours'
             5060  COMPARE_OP               ==
         5062_5064  POP_JUMP_IF_TRUE   5096  'to 5096'
             5066  LOAD_FAST                'wordNext'
             5068  LOAD_STR                 'hour'
             5070  COMPARE_OP               ==
         5072_5074  POP_JUMP_IF_TRUE   5096  'to 5096'

 L.1286      5076  LOAD_FAST                'remainder'
             5078  LOAD_STR                 'hours'
             5080  COMPARE_OP               ==
         5082_5084  POP_JUMP_IF_TRUE   5096  'to 5096'
             5086  LOAD_FAST                'remainder'
             5088  LOAD_STR                 'hour'
             5090  COMPARE_OP               ==
         5092_5094  POP_JUMP_IF_FALSE  5538  'to 5538'
           5096_0  COME_FROM          5082  '5082'
           5096_1  COME_FROM          5072  '5072'
           5096_2  COME_FROM          5062  '5062'

 L.1287      5096  LOAD_FAST                'used'
             5098  LOAD_CONST               1
             5100  INPLACE_ADD      
             5102  STORE_FAST               'used'
         5104_5106  JUMP_FORWARD       5538  'to 5538'
           5108_0  COME_FROM          5016  '5016'

 L.1288      5108  LOAD_FAST                'wordNext'
         5110_5112  POP_JUMP_IF_FALSE  5200  'to 5200'
             5114  LOAD_FAST                'wordNext'
             5116  LOAD_CONST               0
             5118  BINARY_SUBSCR    
             5120  LOAD_METHOD              isdigit
             5122  CALL_METHOD_0         0  '0 positional arguments'
         5124_5126  POP_JUMP_IF_FALSE  5200  'to 5200'

 L.1290      5128  LOAD_FAST                'strNum'
             5130  STORE_FAST               'strHH'

 L.1291      5132  LOAD_FAST                'wordNext'
             5134  STORE_FAST               'strMM'

 L.1292      5136  LOAD_CONST               True
             5138  STORE_FAST               'military'

 L.1293      5140  LOAD_FAST                'used'
             5142  LOAD_CONST               1
             5144  INPLACE_ADD      
             5146  STORE_FAST               'used'

 L.1294      5148  LOAD_FAST                'wordNextNext'
             5150  LOAD_STR                 'hours'
             5152  COMPARE_OP               ==
         5154_5156  POP_JUMP_IF_TRUE   5188  'to 5188'

 L.1295      5158  LOAD_FAST                'wordNextNext'
             5160  LOAD_STR                 'hour'
             5162  COMPARE_OP               ==
         5164_5166  POP_JUMP_IF_TRUE   5188  'to 5188'

 L.1296      5168  LOAD_FAST                'remainder'
             5170  LOAD_STR                 'hours'
             5172  COMPARE_OP               ==
         5174_5176  POP_JUMP_IF_TRUE   5188  'to 5188'
             5178  LOAD_FAST                'remainder'
             5180  LOAD_STR                 'hour'
             5182  COMPARE_OP               ==
         5184_5186  POP_JUMP_IF_FALSE  5538  'to 5538'
           5188_0  COME_FROM          5174  '5174'
           5188_1  COME_FROM          5164  '5164'
           5188_2  COME_FROM          5154  '5154'

 L.1297      5188  LOAD_FAST                'used'
             5190  LOAD_CONST               1
             5192  INPLACE_ADD      
             5194  STORE_FAST               'used'
         5196_5198  JUMP_FORWARD       5538  'to 5538'
           5200_0  COME_FROM          5124  '5124'
           5200_1  COME_FROM          5110  '5110'

 L.1299      5200  LOAD_FAST                'wordNext'
             5202  LOAD_STR                 ''
             5204  COMPARE_OP               ==
         5206_5208  POP_JUMP_IF_TRUE   5270  'to 5270'
             5210  LOAD_FAST                'wordNext'
             5212  LOAD_STR                 "o'clock"
             5214  COMPARE_OP               ==
         5216_5218  POP_JUMP_IF_TRUE   5270  'to 5270'

 L.1301      5220  LOAD_FAST                'wordNext'
             5222  LOAD_STR                 'in'
             5224  COMPARE_OP               ==
         5226_5228  POP_JUMP_IF_FALSE  5250  'to 5250'

 L.1303      5230  LOAD_FAST                'wordNextNext'
             5232  LOAD_STR                 'the'
             5234  COMPARE_OP               ==
         5236_5238  POP_JUMP_IF_TRUE   5270  'to 5270'

 L.1304      5240  LOAD_FAST                'wordNextNext'
             5242  LOAD_FAST                'timeQualifier'
             5244  COMPARE_OP               ==
         5246_5248  POP_JUMP_IF_TRUE   5270  'to 5270'
           5250_0  COME_FROM          5226  '5226'

 L.1306      5250  LOAD_FAST                'wordNext'
             5252  LOAD_STR                 'tonight'
             5254  COMPARE_OP               ==
         5256_5258  POP_JUMP_IF_TRUE   5270  'to 5270'

 L.1307      5260  LOAD_FAST                'wordNextNext'
             5262  LOAD_STR                 'tonight'
             5264  COMPARE_OP               ==
         5266_5268  POP_JUMP_IF_FALSE  5534  'to 5534'
           5270_0  COME_FROM          5256  '5256'
           5270_1  COME_FROM          5246  '5246'
           5270_2  COME_FROM          5236  '5236'
           5270_3  COME_FROM          5216  '5216'
           5270_4  COME_FROM          5206  '5206'

 L.1309      5270  LOAD_FAST                'strNum'
             5272  STORE_FAST               'strHH'

 L.1310      5274  LOAD_STR                 '00'
             5276  STORE_FAST               'strMM'

 L.1311      5278  LOAD_FAST                'wordNext'
             5280  LOAD_STR                 "o'clock"
             5282  COMPARE_OP               ==
         5284_5286  POP_JUMP_IF_FALSE  5296  'to 5296'

 L.1312      5288  LOAD_FAST                'used'
             5290  LOAD_CONST               1
             5292  INPLACE_ADD      
             5294  STORE_FAST               'used'
           5296_0  COME_FROM          5284  '5284'

 L.1314      5296  LOAD_FAST                'wordNext'
             5298  LOAD_STR                 'in'
             5300  COMPARE_OP               ==
         5302_5304  POP_JUMP_IF_TRUE   5316  'to 5316'
             5306  LOAD_FAST                'wordNextNext'
           5308_0  COME_FROM          4176  '4176'
             5308  LOAD_STR                 'in'
             5310  COMPARE_OP               ==
         5312_5314  POP_JUMP_IF_FALSE  5462  'to 5462'
           5316_0  COME_FROM          5302  '5302'

 L.1315      5316  LOAD_FAST                'used'
             5318  LOAD_FAST                'wordNext'
             5320  LOAD_STR                 'in'
             5322  COMPARE_OP               ==
         5324_5326  POP_JUMP_IF_FALSE  5332  'to 5332'
             5328  LOAD_CONST               1
             5330  JUMP_FORWARD       5334  'to 5334'
           5332_0  COME_FROM          5324  '5324'
             5332  LOAD_CONST               2
           5334_0  COME_FROM          5330  '5330'
             5334  INPLACE_ADD      
             5336  STORE_FAST               'used'

 L.1317      5338  LOAD_FAST                'idx'
             5340  LOAD_CONST               3
           5342_0  COME_FROM          4210  '4210'
             5342  BINARY_ADD       
             5344  LOAD_GLOBAL              len
             5346  LOAD_FAST                'words'
             5348  CALL_FUNCTION_1       1  '1 positional argument'
             5350  COMPARE_OP               <
         5352_5354  POP_JUMP_IF_FALSE  5368  'to 5368'
             5356  LOAD_FAST                'words'
             5358  LOAD_FAST                'idx'
             5360  LOAD_CONST               3
             5362  BINARY_ADD       
             5364  BINARY_SUBSCR    
             5366  JUMP_FORWARD       5370  'to 5370'
           5368_0  COME_FROM          5352  '5352'
             5368  LOAD_STR                 ''
           5370_0  COME_FROM          5366  '5366'
             5370  STORE_FAST               'wordNextNextNext'

 L.1319      5372  LOAD_FAST                'wordNextNext'
         5374_5376  POP_JUMP_IF_FALSE  5462  'to 5462'

 L.1320      5378  LOAD_FAST                'wordNextNext'
             5380  LOAD_FAST                'timeQualifier'
             5382  COMPARE_OP               in
         5384_5386  POP_JUMP_IF_TRUE   5398  'to 5398'

 L.1321      5388  LOAD_FAST                'wordNextNextNext'
             5390  LOAD_FAST                'timeQualifier'
             5392  COMPARE_OP               in
         5394_5396  POP_JUMP_IF_FALSE  5462  'to 5462'
           5398_0  COME_FROM          5384  '5384'

 L.1322      5398  LOAD_FAST                'wordNextNext'
             5400  LOAD_FAST                'timeQualifiersPM'
             5402  COMPARE_OP               in
         5404_5406  POP_JUMP_IF_TRUE   5418  'to 5418'

 L.1323      5408  LOAD_FAST                'wordNextNextNext'
           5410_0  COME_FROM          4278  '4278'
             5410  LOAD_FAST                'timeQualifiersPM'
             5412  COMPARE_OP               in
         5414_5416  POP_JUMP_IF_FALSE  5430  'to 5430'
           5418_0  COME_FROM          5404  '5404'

 L.1324      5418  LOAD_STR                 'pm'
             5420  STORE_FAST               'remainder'

 L.1325      5422  LOAD_FAST                'used'
             5424  LOAD_CONST               1
             5426  INPLACE_ADD      
             5428  STORE_FAST               'used'
           5430_0  COME_FROM          5414  '5414'

 L.1326      5430  LOAD_FAST                'wordNextNext'
             5432  LOAD_FAST                'timeQualifiersAM'
             5434  COMPARE_OP               in
         5436_5438  POP_JUMP_IF_TRUE   5450  'to 5450'

 L.1327      5440  LOAD_FAST                'wordNextNextNext'
             5442  LOAD_FAST                'timeQualifiersAM'
             5444  COMPARE_OP               in
         5446_5448  POP_JUMP_IF_FALSE  5462  'to 5462'
           5450_0  COME_FROM          5436  '5436'

 L.1328      5450  LOAD_STR                 'am'
             5452  STORE_FAST               'remainder'

 L.1329      5454  LOAD_FAST                'used'
             5456  LOAD_CONST               1
             5458  INPLACE_ADD      
             5460  STORE_FAST               'used'
           5462_0  COME_FROM          5446  '5446'
           5462_1  COME_FROM          5394  '5394'
           5462_2  COME_FROM          5374  '5374'
           5462_3  COME_FROM          5312  '5312'

 L.1331      5462  LOAD_FAST                'timeQualifier'
             5464  LOAD_STR                 ''
             5466  COMPARE_OP               !=
         5468_5470  POP_JUMP_IF_FALSE  5538  'to 5538'

 L.1332      5472  LOAD_FAST                'timeQualifier'
             5474  LOAD_FAST                'timeQualifiersPM'
             5476  COMPARE_OP               in
         5478_5480  POP_JUMP_IF_FALSE  5496  'to 5496'

 L.1333      5482  LOAD_STR                 'pm'
             5484  STORE_FAST               'remainder'

 L.1334      5486  LOAD_FAST                'used'
             5488  LOAD_CONST               1
             5490  INPLACE_ADD      
             5492  STORE_FAST               'used'
             5494  JUMP_FORWARD       5532  'to 5532'
           5496_0  COME_FROM          5478  '5478'

 L.1336      5496  LOAD_FAST                'timeQualifier'
             5498  LOAD_FAST                'timeQualifiersAM'
             5500  COMPARE_OP               in
         5502_5504  POP_JUMP_IF_FALSE  5520  'to 5520'

 L.1337      5506  LOAD_STR                 'am'
             5508  STORE_FAST               'remainder'

 L.1338      5510  LOAD_FAST                'used'
             5512  LOAD_CONST               1
             5514  INPLACE_ADD      
             5516  STORE_FAST               'used'
             5518  JUMP_FORWARD       5532  'to 5532'
           5520_0  COME_FROM          5502  '5502'

 L.1341      5520  LOAD_FAST                'used'
             5522  LOAD_CONST               1
             5524  INPLACE_ADD      
             5526  STORE_FAST               'used'

 L.1342      5528  LOAD_CONST               True
             5530  STORE_FAST               'military'
           5532_0  COME_FROM          5518  '5518'
           5532_1  COME_FROM          5494  '5494'
             5532  JUMP_FORWARD       5538  'to 5538'
           5534_0  COME_FROM          5266  '5266'

 L.1344      5534  LOAD_CONST               False
             5536  STORE_FAST               'isTime'
           5538_0  COME_FROM          5532  '5532'
           5538_1  COME_FROM          5468  '5468'
           5538_2  COME_FROM          5196  '5196'
           5538_3  COME_FROM          5184  '5184'
           5538_4  COME_FROM          5104  '5104'
           5538_5  COME_FROM          5092  '5092'
           5538_6  COME_FROM          5002  '5002'
           5538_7  COME_FROM          4934  '4934'
           5538_8  COME_FROM          4866  '4866'
           5538_9  COME_FROM          4756  '4756'
          5538_10  COME_FROM          4744  '4744'
          5538_11  COME_FROM          4664  '4664'
          5538_12  COME_FROM          4622  '4622'
          5538_13  COME_FROM          4566  '4566'
          5538_14  COME_FROM          4404  '4404'
          5538_15  COME_FROM          4380  '4380'
          5538_16  COME_FROM          4370  '4370'
          5538_17  COME_FROM          4356  '4356'
          5538_18  COME_FROM          4346  '4346'
          5538_19  COME_FROM          3858  '3858'

 L.1345      5538  LOAD_FAST                'strHH'
         5540_5542  POP_JUMP_IF_FALSE  5552  'to 5552'
             5544  LOAD_GLOBAL              int
             5546  LOAD_FAST                'strHH'
             5548  CALL_FUNCTION_1       1  '1 positional argument'
             5550  JUMP_FORWARD       5554  'to 5554'
           5552_0  COME_FROM          5540  '5540'
             5552  LOAD_CONST               0
           5554_0  COME_FROM          5550  '5550'
             5554  STORE_FAST               'HH'

 L.1346      5556  LOAD_FAST                'strMM'
         5558_5560  POP_JUMP_IF_FALSE  5570  'to 5570'
             5562  LOAD_GLOBAL              int
             5564  LOAD_FAST                'strMM'
             5566  CALL_FUNCTION_1       1  '1 positional argument'
             5568  JUMP_FORWARD       5572  'to 5572'
           5570_0  COME_FROM          5558  '5558'
             5570  LOAD_CONST               0
           5572_0  COME_FROM          5568  '5568'
             5572  STORE_FAST               'MM'

 L.1347      5574  LOAD_FAST                'remainder'
             5576  LOAD_STR                 'pm'
             5578  COMPARE_OP               ==
         5580_5582  POP_JUMP_IF_FALSE  5602  'to 5602'
             5584  LOAD_FAST                'HH'
             5586  LOAD_CONST               12
             5588  COMPARE_OP               <
         5590_5592  POP_JUMP_IF_FALSE  5602  'to 5602'
             5594  LOAD_FAST                'HH'
             5596  LOAD_CONST               12
             5598  BINARY_ADD       
             5600  JUMP_FORWARD       5604  'to 5604'
           5602_0  COME_FROM          5590  '5590'
           5602_1  COME_FROM          5580  '5580'
             5602  LOAD_FAST                'HH'
           5604_0  COME_FROM          5600  '5600'
             5604  STORE_FAST               'HH'

 L.1348      5606  LOAD_FAST                'remainder'
             5608  LOAD_STR                 'am'
             5610  COMPARE_OP               ==
         5612_5614  POP_JUMP_IF_FALSE  5634  'to 5634'
             5616  LOAD_FAST                'HH'
             5618  LOAD_CONST               12
             5620  COMPARE_OP               >=
         5622_5624  POP_JUMP_IF_FALSE  5634  'to 5634'
             5626  LOAD_FAST                'HH'
             5628  LOAD_CONST               12
             5630  BINARY_SUBTRACT  
             5632  JUMP_FORWARD       5636  'to 5636'
           5634_0  COME_FROM          5622  '5622'
           5634_1  COME_FROM          5612  '5612'
             5634  LOAD_FAST                'HH'
           5636_0  COME_FROM          5632  '5632'
             5636  STORE_FAST               'HH'

 L.1350      5638  LOAD_FAST                'military'
         5640_5642  POP_JUMP_IF_TRUE   5760  'to 5760'

 L.1351      5644  LOAD_FAST                'remainder'
             5646  LOAD_CONST               ('am', 'pm', 'hours', 'minutes', 'second', 'seconds', 'hour', 'minute')
             5648  COMPARE_OP               not-in
         5650_5652  POP_JUMP_IF_FALSE  5760  'to 5760'

 L.1354      5654  LOAD_FAST                'daySpecified'
         5656_5658  POP_JUMP_IF_FALSE  5688  'to 5688'
             5660  LOAD_CONST               0
             5662  LOAD_DEREF               'dayOffset'
             5664  DUP_TOP          
             5666  ROT_THREE        
             5668  COMPARE_OP               <=
         5670_5672  POP_JUMP_IF_FALSE  5684  'to 5684'
             5674  LOAD_CONST               1
             5676  COMPARE_OP               <
         5678_5680  POP_JUMP_IF_FALSE  5760  'to 5760'
             5682  JUMP_FORWARD       5688  'to 5688'
           5684_0  COME_FROM          5670  '5670'
             5684  POP_TOP          
             5686  JUMP_FORWARD       5760  'to 5760'
           5688_0  COME_FROM          5682  '5682'
           5688_1  COME_FROM          5656  '5656'

 L.1358      5688  LOAD_FAST                'dateNow'
             5690  LOAD_ATTR                hour
             5692  LOAD_FAST                'HH'
             5694  COMPARE_OP               <
         5696_5698  POP_JUMP_IF_TRUE   5760  'to 5760'
             5700  LOAD_FAST                'dateNow'
             5702  LOAD_ATTR                hour
             5704  LOAD_FAST                'HH'
             5706  COMPARE_OP               ==
         5708_5710  POP_JUMP_IF_FALSE  5726  'to 5726'

 L.1359      5712  LOAD_FAST                'dateNow'
             5714  LOAD_ATTR                minute
             5716  LOAD_FAST                'MM'
             5718  COMPARE_OP               <
         5720_5722  POP_JUMP_IF_FALSE  5726  'to 5726'

 L.1360      5724  JUMP_FORWARD       5760  'to 5760'
           5726_0  COME_FROM          5720  '5720'
           5726_1  COME_FROM          5708  '5708'

 L.1361      5726  LOAD_FAST                'dateNow'
             5728  LOAD_ATTR                hour
             5730  LOAD_FAST                'HH'
             5732  LOAD_CONST               12
             5734  BINARY_ADD       
             5736  COMPARE_OP               <
         5738_5740  POP_JUMP_IF_FALSE  5752  'to 5752'

 L.1362      5742  LOAD_FAST                'HH'
             5744  LOAD_CONST               12
             5746  INPLACE_ADD      
             5748  STORE_FAST               'HH'
             5750  JUMP_FORWARD       5760  'to 5760'
           5752_0  COME_FROM          5738  '5738'

 L.1365      5752  LOAD_DEREF               'dayOffset'
             5754  LOAD_CONST               1
             5756  INPLACE_ADD      
             5758  STORE_DEREF              'dayOffset'
           5760_0  COME_FROM          5750  '5750'
           5760_1  COME_FROM          5724  '5724'
           5760_2  COME_FROM          5696  '5696'
           5760_3  COME_FROM          5686  '5686'
           5760_4  COME_FROM          5678  '5678'
           5760_5  COME_FROM          5650  '5650'
           5760_6  COME_FROM          5640  '5640'

 L.1367      5760  LOAD_FAST                'timeQualifier'
             5762  LOAD_FAST                'timeQualifiersPM'
             5764  COMPARE_OP               in
         5766_5768  POP_JUMP_IF_FALSE  5788  'to 5788'
             5770  LOAD_FAST                'HH'
             5772  LOAD_CONST               12
             5774  COMPARE_OP               <
         5776_5778  POP_JUMP_IF_FALSE  5788  'to 5788'

 L.1368      5780  LOAD_FAST                'HH'
             5782  LOAD_CONST               12
             5784  INPLACE_ADD      
             5786  STORE_FAST               'HH'
           5788_0  COME_FROM          5776  '5776'
           5788_1  COME_FROM          5766  '5766'

 L.1370      5788  LOAD_FAST                'HH'
             5790  LOAD_CONST               24
             5792  COMPARE_OP               >
         5794_5796  POP_JUMP_IF_TRUE   5808  'to 5808'
             5798  LOAD_FAST                'MM'
             5800  LOAD_CONST               59
             5802  COMPARE_OP               >
           5804_0  COME_FROM          3098  '3098'
         5804_5806  POP_JUMP_IF_FALSE  5816  'to 5816'
           5808_0  COME_FROM          5794  '5794'

 L.1371      5808  LOAD_CONST               False
             5810  STORE_FAST               'isTime'

 L.1372      5812  LOAD_CONST               0
             5814  STORE_FAST               'used'
           5816_0  COME_FROM          5804  '5804'

 L.1373      5816  LOAD_FAST                'isTime'
         5818_5820  POP_JUMP_IF_FALSE  5838  'to 5838'

 L.1374      5822  LOAD_FAST                'HH'
             5824  STORE_DEREF              'hrAbs'

 L.1375      5826  LOAD_FAST                'MM'
             5828  STORE_DEREF              'minAbs'

 L.1376      5830  LOAD_FAST                'used'
             5832  LOAD_CONST               1
             5834  INPLACE_ADD      
             5836  STORE_FAST               'used'
           5838_0  COME_FROM          5818  '5818'
           5838_1  COME_FROM          3458  '3458'
           5838_2  COME_FROM          3444  '3444'
           5838_3  COME_FROM          3396  '3396'
           5838_4  COME_FROM          3348  '3348'
           5838_5  COME_FROM          3130  '3130'
           5838_6  COME_FROM          3122  '3122'
           5838_7  COME_FROM          3042  '3042'
           5838_8  COME_FROM          3034  '3034'
           5838_9  COME_FROM          3004  '3004'
          5838_10  COME_FROM          2968  '2968'
          5838_11  COME_FROM          2932  '2932'
          5838_12  COME_FROM          2896  '2896'
          5838_13  COME_FROM          2870  '2870'

 L.1378      5838  LOAD_FAST                'used'
             5840  LOAD_CONST               0
             5842  COMPARE_OP               >
         5844_5846  POP_JUMP_IF_FALSE  2700  'to 2700'

 L.1380      5848  SETUP_LOOP         5900  'to 5900'
             5850  LOAD_GLOBAL              range
             5852  LOAD_FAST                'used'
             5854  CALL_FUNCTION_1       1  '1 positional argument'
             5856  GET_ITER         
             5858  FOR_ITER           5898  'to 5898'
             5860  STORE_FAST               'i'

 L.1381      5862  LOAD_FAST                'idx'
             5864  LOAD_FAST                'i'
             5866  BINARY_ADD       
             5868  LOAD_GLOBAL              len
             5870  LOAD_FAST                'words'
             5872  CALL_FUNCTION_1       1  '1 positional argument'
             5874  COMPARE_OP               >=
         5876_5878  POP_JUMP_IF_FALSE  5882  'to 5882'

 L.1382      5880  BREAK_LOOP       
           5882_0  COME_FROM          5876  '5876'

 L.1383      5882  LOAD_STR                 ''
             5884  LOAD_FAST                'words'
             5886  LOAD_FAST                'idx'
             5888  LOAD_FAST                'i'
             5890  BINARY_ADD       
             5892  STORE_SUBSCR     
         5894_5896  JUMP_BACK          5858  'to 5858'
             5898  POP_BLOCK        
           5900_0  COME_FROM_LOOP     5848  '5848'

 L.1385      5900  LOAD_FAST                'wordPrev'
             5902  LOAD_STR                 'o'
             5904  COMPARE_OP               ==
         5906_5908  POP_JUMP_IF_TRUE   5920  'to 5920'
             5910  LOAD_FAST                'wordPrev'
             5912  LOAD_STR                 'oh'
             5914  COMPARE_OP               ==
         5916_5918  POP_JUMP_IF_FALSE  5934  'to 5934'
           5920_0  COME_FROM          5906  '5906'

 L.1386      5920  LOAD_STR                 ''
             5922  LOAD_FAST                'words'
             5924  LOAD_FAST                'words'
             5926  LOAD_METHOD              index
             5928  LOAD_FAST                'wordPrev'
             5930  CALL_METHOD_1         1  '1 positional argument'
             5932  STORE_SUBSCR     
           5934_0  COME_FROM          5916  '5916'

 L.1388      5934  LOAD_FAST                'wordPrev'
             5936  LOAD_STR                 'early'
             5938  COMPARE_OP               ==
         5940_5942  POP_JUMP_IF_FALSE  5970  'to 5970'

 L.1389      5944  LOAD_CONST               -1
             5946  STORE_DEREF              'hrOffset'

 L.1390      5948  LOAD_STR                 ''
             5950  LOAD_FAST                'words'
             5952  LOAD_FAST                'idx'
             5954  LOAD_CONST               1
             5956  BINARY_SUBTRACT  
             5958  STORE_SUBSCR     

 L.1391      5960  LOAD_FAST                'idx'
             5962  LOAD_CONST               1
             5964  INPLACE_SUBTRACT 
             5966  STORE_FAST               'idx'
             5968  JUMP_FORWARD       6004  'to 6004'
           5970_0  COME_FROM          5940  '5940'

 L.1392      5970  LOAD_FAST                'wordPrev'
             5972  LOAD_STR                 'late'
             5974  COMPARE_OP               ==
         5976_5978  POP_JUMP_IF_FALSE  6004  'to 6004'

 L.1393      5980  LOAD_CONST               1
             5982  STORE_DEREF              'hrOffset'

 L.1394      5984  LOAD_STR                 ''
             5986  LOAD_FAST                'words'
             5988  LOAD_FAST                'idx'
             5990  LOAD_CONST               1
             5992  BINARY_SUBTRACT  
             5994  STORE_SUBSCR     

 L.1395      5996  LOAD_FAST                'idx'
             5998  LOAD_CONST               1
             6000  INPLACE_SUBTRACT 
             6002  STORE_FAST               'idx'
           6004_0  COME_FROM          5976  '5976'
           6004_1  COME_FROM          5968  '5968'

 L.1396      6004  LOAD_FAST                'idx'
             6006  LOAD_CONST               0
             6008  COMPARE_OP               >
         6010_6012  POP_JUMP_IF_FALSE  6050  'to 6050'
             6014  LOAD_FAST                'wordPrev'
             6016  LOAD_FAST                'markers'
             6018  COMPARE_OP               in
         6020_6022  POP_JUMP_IF_FALSE  6050  'to 6050'

 L.1397      6024  LOAD_STR                 ''
             6026  LOAD_FAST                'words'
             6028  LOAD_FAST                'idx'
             6030  LOAD_CONST               1
             6032  BINARY_SUBTRACT  
             6034  STORE_SUBSCR     

 L.1398      6036  LOAD_FAST                'wordPrev'
             6038  LOAD_STR                 'this'
             6040  COMPARE_OP               ==
         6042_6044  POP_JUMP_IF_FALSE  6050  'to 6050'

 L.1399      6046  LOAD_CONST               True
             6048  STORE_FAST               'daySpecified'
           6050_0  COME_FROM          6042  '6042'
           6050_1  COME_FROM          6020  '6020'
           6050_2  COME_FROM          6010  '6010'

 L.1400      6050  LOAD_FAST                'idx'
             6052  LOAD_CONST               1
             6054  COMPARE_OP               >
         6056_6058  POP_JUMP_IF_FALSE  6096  'to 6096'
             6060  LOAD_FAST                'wordPrevPrev'
             6062  LOAD_FAST                'markers'
             6064  COMPARE_OP               in
         6066_6068  POP_JUMP_IF_FALSE  6096  'to 6096'

 L.1401      6070  LOAD_STR                 ''
             6072  LOAD_FAST                'words'
             6074  LOAD_FAST                'idx'
             6076  LOAD_CONST               2
             6078  BINARY_SUBTRACT  
             6080  STORE_SUBSCR     

 L.1402      6082  LOAD_FAST                'wordPrevPrev'
             6084  LOAD_STR                 'this'
             6086  COMPARE_OP               ==
         6088_6090  POP_JUMP_IF_FALSE  6096  'to 6096'

 L.1403      6092  LOAD_CONST               True
             6094  STORE_FAST               'daySpecified'
           6096_0  COME_FROM          6088  '6088'
           6096_1  COME_FROM          6066  '6066'
           6096_2  COME_FROM          6056  '6056'

 L.1405      6096  LOAD_FAST                'idx'
             6098  LOAD_FAST                'used'
             6100  LOAD_CONST               1
             6102  BINARY_SUBTRACT  
             6104  INPLACE_ADD      
             6106  STORE_FAST               'idx'

 L.1406      6108  LOAD_CONST               True
             6110  STORE_DEREF              'found'
         6112_6114  JUMP_BACK          2700  'to 2700'
             6116  POP_BLOCK        
           6118_0  COME_FROM_LOOP     2688  '2688'

 L.1408      6118  LOAD_FAST                'date_found'
             6120  CALL_FUNCTION_0       0  '0 positional arguments'
         6122_6124  POP_JUMP_IF_TRUE   6130  'to 6130'

 L.1409      6126  LOAD_CONST               None
             6128  RETURN_VALUE     
           6130_0  COME_FROM          6122  '6122'

 L.1411      6130  LOAD_DEREF               'dayOffset'
             6132  LOAD_CONST               False
             6134  COMPARE_OP               is
         6136_6138  POP_JUMP_IF_FALSE  6144  'to 6144'

 L.1412      6140  LOAD_CONST               0
             6142  STORE_DEREF              'dayOffset'
           6144_0  COME_FROM          6136  '6136'

 L.1416      6144  LOAD_FAST                'dateNow'
             6146  LOAD_ATTR                replace
             6148  LOAD_CONST               0
             6150  LOAD_CONST               ('microsecond',)
             6152  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6154  STORE_FAST               'extractedDate'

 L.1418      6156  LOAD_DEREF               'datestr'
             6158  LOAD_STR                 ''
             6160  COMPARE_OP               !=
         6162_6164  POP_JUMP_IF_FALSE  6606  'to 6606'

 L.1420      6166  SETUP_EXCEPT       6184  'to 6184'

 L.1421      6168  LOAD_GLOBAL              datetime
             6170  LOAD_METHOD              strptime
             6172  LOAD_DEREF               'datestr'
             6174  LOAD_STR                 '%B %d'
             6176  CALL_METHOD_2         2  '2 positional arguments'
             6178  STORE_FAST               'temp'
             6180  POP_BLOCK        
             6182  JUMP_FORWARD       6240  'to 6240'
           6184_0  COME_FROM_EXCEPT   6166  '6166'

 L.1422      6184  DUP_TOP          
             6186  LOAD_GLOBAL              ValueError
             6188  COMPARE_OP               exception-match
         6190_6192  POP_JUMP_IF_FALSE  6238  'to 6238'
             6194  POP_TOP          
             6196  POP_TOP          
             6198  POP_TOP          

 L.1424      6200  SETUP_EXCEPT       6218  'to 6218'

 L.1425      6202  LOAD_GLOBAL              datetime
             6204  LOAD_METHOD              strptime
             6206  LOAD_DEREF               'datestr'
             6208  LOAD_STR                 '%B %d %Y'
             6210  CALL_METHOD_2         2  '2 positional arguments'
             6212  STORE_FAST               'temp'
             6214  POP_BLOCK        
             6216  JUMP_FORWARD       6234  'to 6234'
           6218_0  COME_FROM_EXCEPT   6200  '6200'

 L.1426      6218  POP_TOP          
             6220  POP_TOP          
             6222  POP_TOP          

 L.1427      6224  LOAD_CONST               None
             6226  STORE_FAST               'temp'
             6228  POP_EXCEPT       
             6230  JUMP_FORWARD       6234  'to 6234'
             6232  END_FINALLY      
           6234_0  COME_FROM          6230  '6230'
           6234_1  COME_FROM          6216  '6216'
             6234  POP_EXCEPT       
             6236  JUMP_FORWARD       6240  'to 6240'
           6238_0  COME_FROM          6190  '6190'
             6238  END_FINALLY      
           6240_0  COME_FROM          6236  '6236'
           6240_1  COME_FROM          6182  '6182'

 L.1428      6240  LOAD_FAST                'temp'
             6242  LOAD_CONST               None
             6244  COMPARE_OP               is
         6246_6248  POP_JUMP_IF_FALSE  6408  'to 6408'

 L.1430      6250  SETUP_LOOP         6406  'to 6406'
             6252  LOAD_FAST                'months'
             6254  LOAD_FAST                'monthsShort'
             6256  BINARY_ADD       
             6258  GET_ITER         
           6260_0  COME_FROM          6270  '6270'
             6260  FOR_ITER           6404  'to 6404'
             6262  STORE_FAST               'm'

 L.1431      6264  LOAD_FAST                'm'
             6266  LOAD_DEREF               'datestr'
             6268  COMPARE_OP               in
         6270_6272  POP_JUMP_IF_FALSE  6260  'to 6260'

 L.1432      6274  LOAD_GLOBAL              month_to_int_en
             6276  LOAD_FAST                'm'
             6278  CALL_FUNCTION_1       1  '1 positional argument'
             6280  STORE_FAST               'int_month'

 L.1433      6282  LOAD_FAST                'extractedDate'
             6284  LOAD_ATTR                year
             6286  STORE_FAST               'year'

 L.1434      6288  LOAD_FAST                'int_month'
             6290  LOAD_FAST                'extractedDate'
             6292  LOAD_ATTR                month
             6294  COMPARE_OP               <
         6296_6298  POP_JUMP_IF_FALSE  6340  'to 6340'

 L.1435      6300  LOAD_STR                 'last'
             6302  LOAD_DEREF               'datestr'
             6304  COMPARE_OP               not-in
         6306_6308  POP_JUMP_IF_FALSE  6378  'to 6378'

 L.1436      6310  LOAD_STR                 'past'
             6312  LOAD_DEREF               'datestr'
             6314  COMPARE_OP               not-in
         6316_6318  POP_JUMP_IF_FALSE  6378  'to 6378'

 L.1437      6320  LOAD_STR                 'prev'
             6322  LOAD_DEREF               'datestr'
             6324  COMPARE_OP               not-in
         6326_6328  POP_JUMP_IF_FALSE  6378  'to 6378'

 L.1438      6330  LOAD_FAST                'year'
             6332  LOAD_CONST               1
             6334  INPLACE_ADD      
             6336  STORE_FAST               'year'
             6338  JUMP_FORWARD       6378  'to 6378'
           6340_0  COME_FROM          6296  '6296'

 L.1439      6340  LOAD_STR                 'last'
             6342  LOAD_DEREF               'datestr'
             6344  COMPARE_OP               in
         6346_6348  POP_JUMP_IF_TRUE   6370  'to 6370'
             6350  LOAD_STR                 'past'
             6352  LOAD_DEREF               'datestr'
             6354  COMPARE_OP               in
         6356_6358  POP_JUMP_IF_TRUE   6370  'to 6370'

 L.1440      6360  LOAD_STR                 'prev'
             6362  LOAD_DEREF               'datestr'
             6364  COMPARE_OP               in
         6366_6368  POP_JUMP_IF_FALSE  6378  'to 6378'
           6370_0  COME_FROM          6356  '6356'
           6370_1  COME_FROM          6346  '6346'

 L.1441      6370  LOAD_FAST                'year'
             6372  LOAD_CONST               1
             6374  INPLACE_SUBTRACT 
             6376  STORE_FAST               'year'
           6378_0  COME_FROM          6366  '6366'
           6378_1  COME_FROM          6338  '6338'
           6378_2  COME_FROM          6326  '6326'
           6378_3  COME_FROM          6316  '6316'
           6378_4  COME_FROM          6306  '6306'

 L.1442      6378  LOAD_FAST                'extractedDate'
             6380  LOAD_ATTR                replace
             6382  LOAD_FAST                'year'

 L.1443      6384  LOAD_FAST                'int_month'

 L.1444      6386  LOAD_CONST               1

 L.1445      6388  LOAD_CONST               0

 L.1446      6390  LOAD_CONST               0
             6392  LOAD_CONST               ('year', 'month', 'day', 'hour', 'minute')
             6394  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             6396  STORE_FAST               'extractedDate'

 L.1447      6398  BREAK_LOOP       
         6400_6402  JUMP_BACK          6260  'to 6260'
             6404  POP_BLOCK        
           6406_0  COME_FROM_LOOP     6250  '6250'
             6406  JUMP_FORWARD       6604  'to 6604'
           6408_0  COME_FROM          6246  '6246'

 L.1449      6408  LOAD_FAST                'extractedDate'
             6410  LOAD_ATTR                replace
             6412  LOAD_CONST               0
             6414  LOAD_CONST               0
             6416  LOAD_CONST               0
             6418  LOAD_CONST               ('hour', 'minute', 'second')
             6420  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6422  STORE_FAST               'extractedDate'

 L.1450      6424  LOAD_FAST                'hasYear'
         6426_6428  POP_JUMP_IF_TRUE   6554  'to 6554'

 L.1451      6430  LOAD_FAST                'temp'
             6432  LOAD_ATTR                replace
             6434  LOAD_FAST                'extractedDate'
             6436  LOAD_ATTR                year

 L.1452      6438  LOAD_FAST                'extractedDate'
             6440  LOAD_ATTR                tzinfo
             6442  LOAD_CONST               ('year', 'tzinfo')
             6444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6446  STORE_FAST               'temp'

 L.1453      6448  LOAD_FAST                'extractedDate'
             6450  LOAD_FAST                'temp'
             6452  COMPARE_OP               <
         6454_6456  POP_JUMP_IF_FALSE  6504  'to 6504'

 L.1454      6458  LOAD_FAST                'extractedDate'
             6460  LOAD_ATTR                replace

 L.1455      6462  LOAD_GLOBAL              int
             6464  LOAD_FAST                'currentYear'
             6466  CALL_FUNCTION_1       1  '1 positional argument'

 L.1456      6468  LOAD_GLOBAL              int
             6470  LOAD_FAST                'temp'
             6472  LOAD_METHOD              strftime
             6474  LOAD_STR                 '%m'
             6476  CALL_METHOD_1         1  '1 positional argument'
             6478  CALL_FUNCTION_1       1  '1 positional argument'

 L.1457      6480  LOAD_GLOBAL              int
             6482  LOAD_FAST                'temp'
             6484  LOAD_METHOD              strftime
             6486  LOAD_STR                 '%d'
             6488  CALL_METHOD_1         1  '1 positional argument'
             6490  CALL_FUNCTION_1       1  '1 positional argument'

 L.1458      6492  LOAD_FAST                'extractedDate'
             6494  LOAD_ATTR                tzinfo
             6496  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             6498  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6500  STORE_FAST               'extractedDate'
             6502  JUMP_FORWARD       6552  'to 6552'
           6504_0  COME_FROM          6454  '6454'

 L.1460      6504  LOAD_FAST                'extractedDate'
             6506  LOAD_ATTR                replace

 L.1461      6508  LOAD_GLOBAL              int
             6510  LOAD_FAST                'currentYear'
             6512  CALL_FUNCTION_1       1  '1 positional argument'
             6514  LOAD_CONST               1
             6516  BINARY_ADD       

 L.1462      6518  LOAD_GLOBAL              int
             6520  LOAD_FAST                'temp'
             6522  LOAD_METHOD              strftime
             6524  LOAD_STR                 '%m'
             6526  CALL_METHOD_1         1  '1 positional argument'
             6528  CALL_FUNCTION_1       1  '1 positional argument'

 L.1463      6530  LOAD_GLOBAL              int
             6532  LOAD_FAST                'temp'
             6534  LOAD_METHOD              strftime
             6536  LOAD_STR                 '%d'
             6538  CALL_METHOD_1         1  '1 positional argument'
             6540  CALL_FUNCTION_1       1  '1 positional argument'

 L.1464      6542  LOAD_FAST                'extractedDate'
             6544  LOAD_ATTR                tzinfo
             6546  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             6548  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6550  STORE_FAST               'extractedDate'
           6552_0  COME_FROM          6502  '6502'
             6552  JUMP_FORWARD       6604  'to 6604'
           6554_0  COME_FROM          6426  '6426'

 L.1466      6554  LOAD_FAST                'extractedDate'
             6556  LOAD_ATTR                replace

 L.1467      6558  LOAD_GLOBAL              int
             6560  LOAD_FAST                'temp'
             6562  LOAD_METHOD              strftime
             6564  LOAD_STR                 '%Y'
             6566  CALL_METHOD_1         1  '1 positional argument'
             6568  CALL_FUNCTION_1       1  '1 positional argument'

 L.1468      6570  LOAD_GLOBAL              int
             6572  LOAD_FAST                'temp'
             6574  LOAD_METHOD              strftime
             6576  LOAD_STR                 '%m'
             6578  CALL_METHOD_1         1  '1 positional argument'
             6580  CALL_FUNCTION_1       1  '1 positional argument'

 L.1469      6582  LOAD_GLOBAL              int
             6584  LOAD_FAST                'temp'
             6586  LOAD_METHOD              strftime
             6588  LOAD_STR                 '%d'
             6590  CALL_METHOD_1         1  '1 positional argument'
             6592  CALL_FUNCTION_1       1  '1 positional argument'

 L.1470      6594  LOAD_FAST                'extractedDate'
             6596  LOAD_ATTR                tzinfo
             6598  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             6600  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6602  STORE_FAST               'extractedDate'
           6604_0  COME_FROM          6552  '6552'
           6604_1  COME_FROM          6406  '6406'
             6604  JUMP_FORWARD       6652  'to 6652'
           6606_0  COME_FROM          6162  '6162'

 L.1473      6606  LOAD_DEREF               'hrOffset'
             6608  LOAD_CONST               0
             6610  COMPARE_OP               ==
         6612_6614  POP_JUMP_IF_FALSE  6652  'to 6652'
             6616  LOAD_DEREF               'minOffset'
             6618  LOAD_CONST               0
             6620  COMPARE_OP               ==
         6622_6624  POP_JUMP_IF_FALSE  6652  'to 6652'
             6626  LOAD_DEREF               'secOffset'
             6628  LOAD_CONST               0
             6630  COMPARE_OP               ==
         6632_6634  POP_JUMP_IF_FALSE  6652  'to 6652'

 L.1474      6636  LOAD_FAST                'extractedDate'
             6638  LOAD_ATTR                replace
             6640  LOAD_CONST               0
             6642  LOAD_CONST               0
             6644  LOAD_CONST               0
             6646  LOAD_CONST               ('hour', 'minute', 'second')
             6648  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6650  STORE_FAST               'extractedDate'
           6652_0  COME_FROM          6632  '6632'
           6652_1  COME_FROM          6622  '6622'
           6652_2  COME_FROM          6612  '6612'
           6652_3  COME_FROM          6604  '6604'

 L.1476      6652  LOAD_DEREF               'yearOffset'
             6654  LOAD_CONST               0
             6656  COMPARE_OP               !=
         6658_6660  POP_JUMP_IF_FALSE  6676  'to 6676'

 L.1477      6662  LOAD_FAST                'extractedDate'
             6664  LOAD_GLOBAL              relativedelta
             6666  LOAD_DEREF               'yearOffset'
             6668  LOAD_CONST               ('years',)
             6670  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6672  BINARY_ADD       
             6674  STORE_FAST               'extractedDate'
           6676_0  COME_FROM          6658  '6658'

 L.1478      6676  LOAD_DEREF               'monthOffset'
             6678  LOAD_CONST               0
             6680  COMPARE_OP               !=
         6682_6684  POP_JUMP_IF_FALSE  6700  'to 6700'

 L.1479      6686  LOAD_FAST                'extractedDate'
             6688  LOAD_GLOBAL              relativedelta
             6690  LOAD_DEREF               'monthOffset'
             6692  LOAD_CONST               ('months',)
             6694  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6696  BINARY_ADD       
             6698  STORE_FAST               'extractedDate'
           6700_0  COME_FROM          6682  '6682'

 L.1480      6700  LOAD_DEREF               'dayOffset'
             6702  LOAD_CONST               0
             6704  COMPARE_OP               !=
         6706_6708  POP_JUMP_IF_FALSE  6724  'to 6724'

 L.1481      6710  LOAD_FAST                'extractedDate'
             6712  LOAD_GLOBAL              relativedelta
             6714  LOAD_DEREF               'dayOffset'
             6716  LOAD_CONST               ('days',)
             6718  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6720  BINARY_ADD       
             6722  STORE_FAST               'extractedDate'
           6724_0  COME_FROM          6706  '6706'

 L.1482      6724  LOAD_DEREF               'hrAbs'
             6726  LOAD_CONST               -1
             6728  COMPARE_OP               !=
         6730_6732  POP_JUMP_IF_FALSE  6886  'to 6886'
             6734  LOAD_DEREF               'minAbs'
             6736  LOAD_CONST               -1
             6738  COMPARE_OP               !=
         6740_6742  POP_JUMP_IF_FALSE  6886  'to 6886'

 L.1485      6744  LOAD_DEREF               'hrAbs'
             6746  LOAD_CONST               None
             6748  COMPARE_OP               is
         6750_6752  POP_JUMP_IF_FALSE  6790  'to 6790'
             6754  LOAD_DEREF               'minAbs'
             6756  LOAD_CONST               None
             6758  COMPARE_OP               is
         6760_6762  POP_JUMP_IF_FALSE  6790  'to 6790'
             6764  LOAD_FAST                'default_time'
             6766  LOAD_CONST               None
             6768  COMPARE_OP               is-not
         6770_6772  POP_JUMP_IF_FALSE  6790  'to 6790'

 L.1486      6774  LOAD_FAST                'default_time'
             6776  LOAD_ATTR                hour
             6778  LOAD_FAST                'default_time'
             6780  LOAD_ATTR                minute
             6782  ROT_TWO          
             6784  STORE_DEREF              'hrAbs'
             6786  STORE_DEREF              'minAbs'
             6788  JUMP_FORWARD       6810  'to 6810'
           6790_0  COME_FROM          6770  '6770'
           6790_1  COME_FROM          6760  '6760'
           6790_2  COME_FROM          6750  '6750'

 L.1488      6790  LOAD_DEREF               'hrAbs'
         6792_6794  JUMP_IF_TRUE_OR_POP  6798  'to 6798'
             6796  LOAD_CONST               0
           6798_0  COME_FROM          6792  '6792'
             6798  STORE_DEREF              'hrAbs'

 L.1489      6800  LOAD_DEREF               'minAbs'
         6802_6804  JUMP_IF_TRUE_OR_POP  6808  'to 6808'
             6806  LOAD_CONST               0
           6808_0  COME_FROM          6802  '6802'
             6808  STORE_DEREF              'minAbs'
           6810_0  COME_FROM          6788  '6788'

 L.1491      6810  LOAD_FAST                'extractedDate'
             6812  LOAD_GLOBAL              relativedelta
             6814  LOAD_DEREF               'hrAbs'

 L.1492      6816  LOAD_DEREF               'minAbs'
             6818  LOAD_CONST               ('hours', 'minutes')
             6820  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6822  BINARY_ADD       
             6824  STORE_FAST               'extractedDate'

 L.1493      6826  LOAD_DEREF               'hrAbs'
             6828  LOAD_CONST               0
             6830  COMPARE_OP               !=
         6832_6834  POP_JUMP_IF_TRUE   6846  'to 6846'
             6836  LOAD_DEREF               'minAbs'
             6838  LOAD_CONST               0
             6840  COMPARE_OP               !=
         6842_6844  POP_JUMP_IF_FALSE  6886  'to 6886'
           6846_0  COME_FROM          6832  '6832'
             6846  LOAD_DEREF               'datestr'
             6848  LOAD_STR                 ''
             6850  COMPARE_OP               ==
         6852_6854  POP_JUMP_IF_FALSE  6886  'to 6886'

 L.1494      6856  LOAD_FAST                'daySpecified'
         6858_6860  POP_JUMP_IF_TRUE   6886  'to 6886'
             6862  LOAD_FAST                'dateNow'
             6864  LOAD_FAST                'extractedDate'
             6866  COMPARE_OP               >
         6868_6870  POP_JUMP_IF_FALSE  6886  'to 6886'

 L.1495      6872  LOAD_FAST                'extractedDate'
             6874  LOAD_GLOBAL              relativedelta
             6876  LOAD_CONST               1
             6878  LOAD_CONST               ('days',)
             6880  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6882  BINARY_ADD       
             6884  STORE_FAST               'extractedDate'
           6886_0  COME_FROM          6868  '6868'
           6886_1  COME_FROM          6858  '6858'
           6886_2  COME_FROM          6852  '6852'
           6886_3  COME_FROM          6842  '6842'
           6886_4  COME_FROM          6740  '6740'
           6886_5  COME_FROM          6730  '6730'

 L.1496      6886  LOAD_DEREF               'hrOffset'
             6888  LOAD_CONST               0
             6890  COMPARE_OP               !=
         6892_6894  POP_JUMP_IF_FALSE  6910  'to 6910'

 L.1497      6896  LOAD_FAST                'extractedDate'
             6898  LOAD_GLOBAL              relativedelta
             6900  LOAD_DEREF               'hrOffset'
             6902  LOAD_CONST               ('hours',)
             6904  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6906  BINARY_ADD       
             6908  STORE_FAST               'extractedDate'
           6910_0  COME_FROM          6892  '6892'

 L.1498      6910  LOAD_DEREF               'minOffset'
             6912  LOAD_CONST               0
             6914  COMPARE_OP               !=
         6916_6918  POP_JUMP_IF_FALSE  6934  'to 6934'

 L.1499      6920  LOAD_FAST                'extractedDate'
             6922  LOAD_GLOBAL              relativedelta
             6924  LOAD_DEREF               'minOffset'
             6926  LOAD_CONST               ('minutes',)
             6928  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6930  BINARY_ADD       
             6932  STORE_FAST               'extractedDate'
           6934_0  COME_FROM          6916  '6916'

 L.1500      6934  LOAD_DEREF               'secOffset'
             6936  LOAD_CONST               0
             6938  COMPARE_OP               !=
         6940_6942  POP_JUMP_IF_FALSE  6958  'to 6958'

 L.1501      6944  LOAD_FAST                'extractedDate'
             6946  LOAD_GLOBAL              relativedelta
             6948  LOAD_DEREF               'secOffset'
             6950  LOAD_CONST               ('seconds',)
             6952  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6954  BINARY_ADD       
             6956  STORE_FAST               'extractedDate'
           6958_0  COME_FROM          6940  '6940'

 L.1502      6958  SETUP_LOOP         7040  'to 7040'
             6960  LOAD_GLOBAL              enumerate
             6962  LOAD_FAST                'words'
             6964  CALL_FUNCTION_1       1  '1 positional argument'
             6966  GET_ITER         
           6968_0  COME_FROM          7022  '7022'
           6968_1  COME_FROM          7004  '7004'
           6968_2  COME_FROM          6986  '6986'
             6968  FOR_ITER           7038  'to 7038'
             6970  UNPACK_SEQUENCE_2     2 
             6972  STORE_FAST               'idx'
             6974  STORE_FAST               'word'

 L.1503      6976  LOAD_FAST                'words'
             6978  LOAD_FAST                'idx'
             6980  BINARY_SUBSCR    
             6982  LOAD_STR                 'and'
             6984  COMPARE_OP               ==
         6986_6988  POP_JUMP_IF_FALSE  6968  'to 6968'

 L.1504      6990  LOAD_FAST                'words'
             6992  LOAD_FAST                'idx'
             6994  LOAD_CONST               1
             6996  BINARY_SUBTRACT  
             6998  BINARY_SUBSCR    
             7000  LOAD_STR                 ''
             7002  COMPARE_OP               ==
         7004_7006  POP_JUMP_IF_FALSE  6968  'to 6968'
             7008  LOAD_FAST                'words'
             7010  LOAD_FAST                'idx'
             7012  LOAD_CONST               1
             7014  BINARY_ADD       
             7016  BINARY_SUBSCR    
             7018  LOAD_STR                 ''
             7020  COMPARE_OP               ==
         7022_7024  POP_JUMP_IF_FALSE  6968  'to 6968'

 L.1505      7026  LOAD_STR                 ''
             7028  LOAD_FAST                'words'
             7030  LOAD_FAST                'idx'
             7032  STORE_SUBSCR     
         7034_7036  JUMP_BACK          6968  'to 6968'
             7038  POP_BLOCK        
           7040_0  COME_FROM_LOOP     6958  '6958'

 L.1507      7040  LOAD_STR                 ' '
             7042  LOAD_METHOD              join
             7044  LOAD_FAST                'words'
             7046  CALL_METHOD_1         1  '1 positional argument'
             7048  STORE_FAST               'resultStr'

 L.1508      7050  LOAD_STR                 ' '
             7052  LOAD_METHOD              join
             7054  LOAD_FAST                'resultStr'
             7056  LOAD_METHOD              split
             7058  CALL_METHOD_0         0  '0 positional arguments'
             7060  CALL_METHOD_1         1  '1 positional argument'
             7062  STORE_FAST               'resultStr'

 L.1509      7064  LOAD_FAST                'extractedDate'
             7066  LOAD_FAST                'resultStr'
             7068  BUILD_LIST_2          2 
             7070  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 2110


def isFractional_en(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]
    fracts = {'whole':1,  'half':2,  'halve':2,  'quarter':4}
    if short_scale:
        for num in _SHORT_ORDINAL_EN:
            if num > 2:
                fracts[_SHORT_ORDINAL_EN[num]] = num

    else:
        for num in _LONG_ORDINAL_EN:
            if num > 2:
                fracts[_LONG_ORDINAL_EN[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False


def extract_numbers_en(text, short_scale=True, ordinals=False):
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
    results = _extract_numbers_with_text_en(tokenize(text), short_scale, ordinals)
    return [float(result.value) for result in results]


class EnglishNormalizer(Normalizer):
    with open(resolve_resource_file('text/en-us/normalize.json')) as (f):
        _default_config = json.load(f)


def normalize_en(text, remove_articles):
    """ English string normalization """
    return EnglishNormalizer.normalize(text, remove_articles)