# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/parse_nl.py
# Compiled at: 2020-03-12 04:03:11
# Size of source mod 2**32: 52692 bytes
from collections import namedtuple
from datetime import datetime, timedelta
import dateutil.relativedelta as relativedelta
from .parse_common import is_numeric, look_for_fractions
from .common_data_nl import _ARTICLES, _NUM_STRING_NL, _LONG_ORDINAL_STRING_NL, _LONG_SCALE_NL, _SHORT_SCALE_NL, _SHORT_ORDINAL_STRING_NL
import re

def _invert_dict(original):
    """Produce a dictionary with the keys and values inverted based on input.

    Args:
        original dict: The dict like object to invert

    Returns:
        dict
    """
    return {value:key for key, value in original.items()}


_NEGATIVES = {
 'min', 'minus'}
_SUMS = {
 'twintig', '20', 'dertig', '30', 'veertig', '40', 'vijftig', '50',
 'zestig', '60', 'zeventig', '70', 'techtig', '80', 'negentig', '90'}
_MULTIPLIES_LONG_SCALE_NL = set(_LONG_SCALE_NL.values())
_MULTIPLIES_SHORT_SCALE_NL = set(_SHORT_SCALE_NL.values())
_FRACTION_MARKER = {
 'en'}
_DECIMAL_MARKER = {
 'komma', 'punt'}
_STRING_NUM_NL = _invert_dict(_NUM_STRING_NL)
_STRING_NUM_NL.update({'half':0.5, 
 'driekwart':0.75, 
 'anderhalf':1.5, 
 'paar':2})
_STRING_SHORT_ORDINAL_NL = _invert_dict(_SHORT_ORDINAL_STRING_NL)
_STRING_LONG_ORDINAL_NL = _invert_dict(_LONG_ORDINAL_STRING_NL)
_Token = namedtuple('_Token', 'word index')

class _ReplaceableNumber:
    __doc__ = "Similar to _Token, this class is used in number parsing.\n\n    Once we've found a number in a string, this class contains all\n    the info about the value, and where it came from in the original text.\n    In other words, it is the text, and the number that can replace it in\n    the string.\n    "

    def __init__(self, value, tokens: [
 _Token]):
        self.value = value
        self.tokens = tokens

    def __bool__(self):
        return bool(self.value is not None and self.value is not False)

    @property
    def start_index(self):
        return self.tokens[0].index

    @property
    def end_index(self):
        return self.tokens[(-1)].index

    @property
    def text(self):
        return ' '.join([t.word for t in self.tokens])

    def __setattr__(self, key, value):
        try:
            getattr(self, key)
        except AttributeError:
            super().__setattr__(key, value)
        else:
            raise Exception('Immutable!')

    def __str__(self):
        return '({v}, {t})'.format(v=(self.value), t=(self.tokens))

    def __repr__(self):
        return '{n}({v}, {t})'.format(n=(self.__class__.__name__), v=(self.value), t=(self.tokens))


def _tokenize(text):
    """Generate a list of token object, given a string.
    Args:
        text str: Text to tokenize.

    Returns:
        [_Token]
    """
    return [_Token(word, index) for index, word in enumerate(text.split())]


def _partition_list(items, split_on):
    """Partition a list of items.

    Works similarly to str.partition

    Args:
        items:
        split_on callable:
            Should return a boolean. Each item will be passed to
            this callable in succession, and partitions will be
            created any time it returns True.

    Returns:
        [[any]]
    """
    splits = []
    current_split = []
    for item in items:
        if split_on(item):
            splits.append(current_split)
            splits.append([item])
            current_split = []
        else:
            current_split.append(item)

    splits.append(current_split)
    return list(filter(lambda x: len(x) != 0, splits))


def _convert_words_to_numbers(text, short_scale=True, ordinals=False):
    """Convert words in a string into their equivalent numbers.
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
    tokens = _tokenize(text)
    numbers_to_replace = _extract_numbers_with_text(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """Extract all numbers from a list of _Tokens, with the representing words.

    Args:
        [_Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (first, second, third, etc) should
                       be parsed.
        fractional_numbers bool: True if we should look for fractions and
                                 decimals.

    Returns:
        [_ReplaceableNumber]: A list of tuples, each containing a number and a
                         string.
    """
    placeholder = '<placeholder>'
    results = []
    while True:
        to_replace = _extract_number_with_text_nl(tokens, short_scale, ordinals, fractional_numbers)
        if not to_replace:
            break
        results.append(to_replace)
        tokens = [t if (to_replace.start_index <= t.index <= to_replace.end_index) else (_Token(placeholder, t.index)) for t in tokens]

    results.sort(key=(lambda n: n.start_index))
    return results


def _extract_number_with_text_nl(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """This function extracts a number from a list of _Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        _ReplaceableNumber
    """
    number, tokens = _extract_number_with_text_nl_helper(tokens, short_scale, ordinals, fractional_numbers)
    while tokens and tokens[0].word in _ARTICLES:
        tokens.pop(0)

    return _ReplaceableNumber(number, tokens)


def _extract_number_with_text_nl_helper(tokens, short_scale=True, ordinals=False, fractional_numbers=True):
    """Helper for _extract_number_with_text_nl.

    This contains the real logic for parsing, but produces
    a result that needs a little cleaning (specific, it may
    contain leading articles that can be trimmed off).

    Args:
        tokens [_Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:

    Returns:
        int or float, [_Tokens]
    """
    if fractional_numbers:
        fraction, fraction_text = _extract_fraction_with_text_nl(tokens, short_scale, ordinals)
        if fraction:
            return (
             fraction, fraction_text)
        decimal, decimal_text = _extract_decimal_with_text_nl(tokens, short_scale, ordinals)
        if decimal:
            return (
             decimal, decimal_text)
    return _extract_whole_number_with_text_nl(tokens, short_scale, ordinals)


def _extract_fraction_with_text_nl(tokens, short_scale, ordinals):
    """Extract fraction numbers from a string.

    This function handles text such as '2 and 3/4'. Note that "one half" or
    similar will be parsed by the whole number function.

    Args:
        tokens [_Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [_Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.
    """
    for c in _FRACTION_MARKER:
        partitions = _partition_list(tokens, lambda t: t.word == c)
        if len(partitions) == 3:
            numbers1 = _extract_numbers_with_text((partitions[0]), short_scale, ordinals,
              fractional_numbers=False)
            numbers2 = _extract_numbers_with_text((partitions[2]), short_scale, ordinals,
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


def _extract_decimal_with_text_nl(tokens, short_scale, ordinals):
    """Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extractnumber_nl, it also depends on
        extractnumber_nl, to parse out the components of the decimal.

        This does not currently handle things like:
            number dot number number number

    Args:
        tokens [_Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [_Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.
    """
    for c in _DECIMAL_MARKER:
        partitions = _partition_list(tokens, lambda t: t.word == c)
        if len(partitions) == 3:
            numbers1 = _extract_numbers_with_text((partitions[0]), short_scale, ordinals,
              fractional_numbers=False)
            numbers2 = _extract_numbers_with_text((partitions[2]), short_scale, ordinals,
              fractional_numbers=False)
            return numbers1 and numbers2 or (None, None)
            number = numbers1[(-1)]
            decimal = numbers2[0]
            if '.' not in str(decimal.text):
                return (
                 number.value + float('0.' + str(decimal.value)),
                 number.tokens + partitions[1] + decimal.tokens)

    return (None, None)


def _extract_whole_number_with_text_nl(tokens, short_scale, ordinals):
    """Handle numbers not handled by the decimal or fraction functions.

    This is generally whole numbers. Note that phrases such as "one half" will
    be handled by this function, while "one and a half" are handled by the
    fraction function.

    Args:
        tokens [_Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [_Tokens]
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
        if word in _ARTICLES or word in _NEGATIVES:
            number_words.append(token)
            continue
        prev_word = tokens[(idx - 1)].word if idx > 0 else ''
        next_word = tokens[(idx + 1)].word if idx + 1 < len(tokens) else ''
        if word not in string_num_scale and word not in _STRING_NUM_NL and word not in _SUMS and word not in multiplies and not ordinals and word in string_num_ordinal or is_numeric(word) or isFractional_nl(word, short_scale=short_scale) or look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words:
                if not all([w in _ARTICLES | _NEGATIVES for w in words_only]):
                    break
                else:
                    number_words = []
                    continue
            else:
                if not (word not in multiplies and prev_word not in multiplies and prev_word not in _SUMS):
                    if prev_word not in _NEGATIVES and prev_word not in _ARTICLES:
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
        if word in _STRING_NUM_NL:
            val = _STRING_NUM_NL.get(word)
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
                    if ordinals and prev_word in string_num_ordinal:
                        if val == 1:
                            val = prev_val
                else:
                    if prev_word in _SUMS:
                        if val:
                            if val < 10:
                                val = prev_val + val
                    if word in multiplies:
                        if not prev_val:
                            prev_val = 1
                        val = prev_val * val
                    if val is False:
                        val = isFractional_nl(word, short_scale=short_scale)
                        current_val = val
                    if not ordinals:
                        next_val = isFractional_nl(next_word, short_scale=short_scale)
                        if next_val:
                            if not val:
                                val = 1
                            val = val * next_val
                            number_words.append(tokens[(idx + 1)])
        if val and prev_word:
            if prev_word in _NEGATIVES:
                val = 0 - val
            if not val:
                aPieces = word.split('/')
                if look_for_fractions(aPieces):
                    val = float(aPieces[0]) / float(aPieces[1])
                    current_val = val
            else:
                if prev_word in _SUMS:
                    if word not in _SUMS:
                        if current_val >= 10:
                            number_words.pop()
                            val = prev_val
                            break
                prev_val = val
                if word in multiplies:
                    if next_word not in multiplies:
                        to_sum.append(val)
                        val = 0
                        prev_val = 0

    if val is not None:
        if to_sum:
            val += sum(to_sum)
    return (
     val, number_words)


def _initialize_number_data(short_scale):
    """Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale
    """
    multiplies = _MULTIPLIES_SHORT_SCALE_NL if short_scale else _MULTIPLIES_LONG_SCALE_NL
    string_num_ordinal_nl = _STRING_SHORT_ORDINAL_NL if short_scale else _STRING_LONG_ORDINAL_NL
    string_num_scale_nl = _SHORT_SCALE_NL if short_scale else _LONG_SCALE_NL
    string_num_scale_nl = _invert_dict(string_num_scale_nl)
    return (
     multiplies, string_num_ordinal_nl, string_num_scale_nl)


def extractnumber_nl(text, short_scale=True, ordinals=False):
    """Extract a number from a text string

    The function handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found
    """
    return _extract_number_with_text_nl(_tokenize(text.lower()), short_scale, ordinals).value


def extract_duration_nl(text):
    """Convert an english phrase into a number of seconds

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
    time_units = {'microseconden':None,  'milliseconden':None, 
     'seconden':None, 
     'minuten':None, 
     'uren':None, 
     'dagen':None, 
     'weken':None}
    pattern = '(?P<value>\\d+(?:\\.?\\d+)?)\\s+{unit}s?'
    text = _convert_words_to_numbers(text)
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


def extract_datetime_nl--- This code section failed: ---

 L. 650         0  LOAD_CODE                <code_object clean_string>
                2  LOAD_STR                 'extract_datetime_nl.<locals>.clean_string'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'clean_string'

 L. 670         8  LOAD_CLOSURE             'datestr'
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
               32  LOAD_STR                 'extract_datetime_nl.<locals>.date_found'
               34  MAKE_FUNCTION_8          'closure'
               36  STORE_FAST               'date_found'

 L. 680        38  LOAD_FAST                'string'
               40  LOAD_STR                 ''
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  LOAD_FAST                'dateNow'
               48  POP_JUMP_IF_TRUE     54  'to 54'
             50_0  COME_FROM            44  '44'

 L. 681        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 683        54  LOAD_CONST               False
               56  STORE_DEREF              'found'

 L. 684        58  LOAD_CONST               False
               60  STORE_FAST               'daySpecified'

 L. 685        62  LOAD_CONST               False
               64  STORE_DEREF              'dayOffset'

 L. 686        66  LOAD_CONST               0
               68  STORE_DEREF              'monthOffset'

 L. 687        70  LOAD_CONST               0
               72  STORE_DEREF              'yearOffset'

 L. 688        74  LOAD_FAST                'dateNow'
               76  LOAD_METHOD              strftime
               78  LOAD_STR                 '%w'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  STORE_FAST               'today'

 L. 689        84  LOAD_FAST                'dateNow'
               86  LOAD_METHOD              strftime
               88  LOAD_STR                 '%Y'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               'currentYear'

 L. 690        94  LOAD_CONST               False
               96  STORE_FAST               'fromFlag'

 L. 691        98  LOAD_STR                 ''
              100  STORE_DEREF              'datestr'

 L. 692       102  LOAD_CONST               False
              104  STORE_FAST               'hasYear'

 L. 693       106  LOAD_STR                 ''
              108  STORE_FAST               'timeQualifier'

 L. 695       110  LOAD_STR                 'ochtend'
              112  BUILD_LIST_1          1 
              114  STORE_FAST               'timeQualifiersAM'

 L. 696       116  LOAD_STR                 'middag'
              118  LOAD_STR                 'avond'
              120  LOAD_STR                 'nacht'
              122  BUILD_LIST_3          3 
              124  STORE_FAST               'timeQualifiersPM'

 L. 697       126  LOAD_FAST                'timeQualifiersAM'
              128  LOAD_FAST                'timeQualifiersPM'
              130  BINARY_ADD       
              132  STORE_DEREF              'timeQualifiersList'

 L. 698       134  LOAD_CONST               8
              136  LOAD_CONST               15
              138  LOAD_CONST               19
              140  LOAD_CONST               0
              142  BUILD_LIST_4          4 
              144  STORE_FAST               'timeQualifierOffsets'

 L. 699       146  LOAD_STR                 'op'
              148  LOAD_STR                 'in'
              150  LOAD_STR                 'om'
              152  LOAD_STR                 'tegen'
              154  LOAD_STR                 'over'

 L. 700       156  LOAD_STR                 'deze'
              158  LOAD_STR                 'rond'
              160  LOAD_STR                 'voor'
              162  LOAD_STR                 'van'
              164  LOAD_STR                 'binnen'
              166  BUILD_LIST_10        10 
              168  STORE_FAST               'markers'

 L. 701       170  LOAD_STR                 'maandag'
              172  LOAD_STR                 'dinsdag'
              174  LOAD_STR                 'woensdag'
              176  LOAD_STR                 'donderdag'
              178  LOAD_STR                 'vrijdag'

 L. 702       180  LOAD_STR                 'zaterdag'
              182  LOAD_STR                 'zondag'
              184  BUILD_LIST_7          7 
              186  STORE_FAST               'days'

 L. 703       188  LOAD_CLOSURE             'timeQualifiersList'
              190  BUILD_TUPLE_1         1 
              192  LOAD_LISTCOMP            '<code_object <listcomp>>'
              194  LOAD_STR                 'extract_datetime_nl.<locals>.<listcomp>'
              196  MAKE_FUNCTION_8          'closure'
              198  LOAD_FAST                'days'
              200  GET_ITER         
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  STORE_FAST               'day_parts'

 L. 704       206  LOAD_STR                 'januari'
              208  LOAD_STR                 'februari'
              210  LOAD_STR                 'maart'
              212  LOAD_STR                 'april'
              214  LOAD_STR                 'mei'
              216  LOAD_STR                 'juni'

 L. 705       218  LOAD_STR                 'juli'
              220  LOAD_STR                 'augustus'
              222  LOAD_STR                 'september'
              224  LOAD_STR                 'oktober'
              226  LOAD_STR                 'november'

 L. 706       228  LOAD_STR                 'december'
              230  BUILD_LIST_12        12 
              232  STORE_FAST               'months'

 L. 707       234  LOAD_FAST                'days'
              236  LOAD_LISTCOMP            '<code_object <listcomp>>'
              238  LOAD_STR                 'extract_datetime_nl.<locals>.<listcomp>'
              240  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              242  LOAD_FAST                'days'
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  BINARY_ADD       
              250  LOAD_STR                 'weekeinde'
              252  LOAD_STR                 'werkdag'

 L. 708       254  LOAD_STR                 'weekeinden'
              256  LOAD_STR                 'werkdagen'
              258  BUILD_LIST_4          4 
              260  BINARY_ADD       
              262  STORE_FAST               'recur_markers'

 L. 709       264  LOAD_STR                 'jan'
              266  LOAD_STR                 'feb'
              268  LOAD_STR                 'mar'
              270  LOAD_STR                 'apr'
              272  LOAD_STR                 'mei'
              274  LOAD_STR                 'jun'
              276  LOAD_STR                 'jul'
              278  LOAD_STR                 'aug'

 L. 710       280  LOAD_STR                 'sep'
              282  LOAD_STR                 'okt'
              284  LOAD_STR                 'nov'
              286  LOAD_STR                 'dec'
              288  BUILD_LIST_12        12 
              290  STORE_FAST               'months_short'

 L. 711       292  LOAD_STR                 'decennium'
              294  LOAD_STR                 'eeuw'
              296  LOAD_STR                 'millennium'
              298  BUILD_LIST_3          3 
              300  STORE_FAST               'year_multiples'

 L. 712       302  LOAD_STR                 'dagen'
              304  LOAD_STR                 'weken'
              306  LOAD_STR                 'maanden'
              308  LOAD_STR                 'jaren'
              310  BUILD_LIST_4          4 
              312  STORE_FAST               'day_multiples'

 L. 714       314  LOAD_FAST                'clean_string'
              316  LOAD_FAST                'string'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  STORE_FAST               'words'

 L. 716   322_324  SETUP_LOOP         2460  'to 2460'
              326  LOAD_GLOBAL              enumerate
              328  LOAD_FAST                'words'
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  GET_ITER         
            334_0  COME_FROM          2316  '2316'
          334_336  FOR_ITER           2458  'to 2458'
              338  UNPACK_SEQUENCE_2     2 
              340  STORE_FAST               'idx'
              342  STORE_FAST               'word'

 L. 717       344  LOAD_FAST                'word'
              346  LOAD_STR                 ''
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   358  'to 358'

 L. 718   354_356  CONTINUE            334  'to 334'
            358_0  COME_FROM           350  '350'

 L. 719       358  LOAD_FAST                'idx'
              360  LOAD_CONST               1
              362  COMPARE_OP               >
          364_366  POP_JUMP_IF_FALSE   380  'to 380'
              368  LOAD_FAST                'words'
              370  LOAD_FAST                'idx'
              372  LOAD_CONST               2
              374  BINARY_SUBTRACT  
              376  BINARY_SUBSCR    
              378  JUMP_FORWARD        382  'to 382'
            380_0  COME_FROM           364  '364'
              380  LOAD_STR                 ''
            382_0  COME_FROM           378  '378'
              382  STORE_FAST               'wordPrevPrev'

 L. 720       384  LOAD_FAST                'idx'
              386  LOAD_CONST               0
              388  COMPARE_OP               >
          390_392  POP_JUMP_IF_FALSE   406  'to 406'
              394  LOAD_FAST                'words'
              396  LOAD_FAST                'idx'
              398  LOAD_CONST               1
              400  BINARY_SUBTRACT  
              402  BINARY_SUBSCR    
              404  JUMP_FORWARD        408  'to 408'
            406_0  COME_FROM           390  '390'
              406  LOAD_STR                 ''
            408_0  COME_FROM           404  '404'
              408  STORE_FAST               'wordPrev'

 L. 721       410  LOAD_FAST                'idx'
              412  LOAD_CONST               1
              414  BINARY_ADD       
              416  LOAD_GLOBAL              len
              418  LOAD_FAST                'words'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  COMPARE_OP               <
          424_426  POP_JUMP_IF_FALSE   440  'to 440'
              428  LOAD_FAST                'words'
              430  LOAD_FAST                'idx'
              432  LOAD_CONST               1
              434  BINARY_ADD       
              436  BINARY_SUBSCR    
              438  JUMP_FORWARD        442  'to 442'
            440_0  COME_FROM           424  '424'
              440  LOAD_STR                 ''
            442_0  COME_FROM           438  '438'
              442  STORE_FAST               'wordNext'

 L. 722       444  LOAD_FAST                'idx'
              446  LOAD_CONST               2
              448  BINARY_ADD       
              450  LOAD_GLOBAL              len
              452  LOAD_FAST                'words'
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  COMPARE_OP               <
          458_460  POP_JUMP_IF_FALSE   474  'to 474'
              462  LOAD_FAST                'words'
              464  LOAD_FAST                'idx'
              466  LOAD_CONST               2
              468  BINARY_ADD       
              470  BINARY_SUBSCR    
              472  JUMP_FORWARD        476  'to 476'
            474_0  COME_FROM           458  '458'
              474  LOAD_STR                 ''
            476_0  COME_FROM           472  '472'
              476  STORE_FAST               'wordNextNext'

 L. 724       478  LOAD_FAST                'idx'
              480  STORE_FAST               'start'

 L. 725       482  LOAD_CONST               0
              484  STORE_FAST               'used'

 L. 728       486  LOAD_FAST                'word'
              488  LOAD_STR                 'nu'
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE   558  'to 558'
              496  LOAD_DEREF               'datestr'
          498_500  POP_JUMP_IF_TRUE    558  'to 558'

 L. 729       502  LOAD_STR                 ' '
              504  LOAD_METHOD              join
              506  LOAD_FAST                'words'
              508  LOAD_FAST                'idx'
              510  LOAD_CONST               1
              512  BINARY_ADD       
              514  LOAD_CONST               None
              516  BUILD_SLICE_2         2 
              518  BINARY_SUBSCR    
              520  CALL_METHOD_1         1  '1 positional argument'
              522  STORE_FAST               'resultStr'

 L. 730       524  LOAD_STR                 ' '
              526  LOAD_METHOD              join
              528  LOAD_FAST                'resultStr'
              530  LOAD_METHOD              split
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               'resultStr'

 L. 731       538  LOAD_FAST                'dateNow'
              540  LOAD_ATTR                replace
              542  LOAD_CONST               0
              544  LOAD_CONST               ('microsecond',)
              546  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              548  STORE_FAST               'extractedDate'

 L. 732       550  LOAD_FAST                'extractedDate'
              552  LOAD_FAST                'resultStr'
              554  BUILD_LIST_2          2 
              556  RETURN_VALUE     
            558_0  COME_FROM           498  '498'
            558_1  COME_FROM           492  '492'

 L. 733       558  LOAD_FAST                'wordNext'
              560  LOAD_FAST                'year_multiples'
              562  COMPARE_OP               in
          564_566  POP_JUMP_IF_FALSE   678  'to 678'

 L. 734       568  LOAD_CONST               None
              570  STORE_FAST               'multiplier'

 L. 735       572  LOAD_GLOBAL              is_numeric
              574  LOAD_FAST                'word'
              576  CALL_FUNCTION_1       1  '1 positional argument'
          578_580  POP_JUMP_IF_FALSE   590  'to 590'

 L. 736       582  LOAD_GLOBAL              extractnumber_nl
              584  LOAD_FAST                'word'
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  STORE_FAST               'multiplier'
            590_0  COME_FROM           578  '578'

 L. 737       590  LOAD_FAST                'multiplier'
          592_594  JUMP_IF_TRUE_OR_POP   598  'to 598'
              596  LOAD_CONST               1
            598_0  COME_FROM           592  '592'
              598  STORE_FAST               'multiplier'

 L. 738       600  LOAD_GLOBAL              int
              602  LOAD_FAST                'multiplier'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  STORE_FAST               'multiplier'

 L. 739       608  LOAD_FAST                'used'
              610  LOAD_CONST               2
              612  INPLACE_ADD      
              614  STORE_FAST               'used'

 L. 740       616  LOAD_FAST                'wordNext'
              618  LOAD_STR                 'decennium'
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   636  'to 636'

 L. 741       626  LOAD_FAST                'multiplier'
              628  LOAD_CONST               10
              630  BINARY_MULTIPLY  
              632  STORE_DEREF              'yearOffset'
              634  JUMP_FORWARD       1968  'to 1968'
            636_0  COME_FROM           622  '622'

 L. 742       636  LOAD_FAST                'wordNext'
              638  LOAD_STR                 'eeuw'
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE   656  'to 656'

 L. 743       646  LOAD_FAST                'multiplier'
              648  LOAD_CONST               100
              650  BINARY_MULTIPLY  
              652  STORE_DEREF              'yearOffset'
              654  JUMP_FORWARD       1968  'to 1968'
            656_0  COME_FROM           642  '642'

 L. 744       656  LOAD_FAST                'wordNext'
              658  LOAD_STR                 'millennium'
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 745       666  LOAD_FAST                'multiplier'
              668  LOAD_CONST               1000
              670  BINARY_MULTIPLY  
              672  STORE_DEREF              'yearOffset'
          674_676  JUMP_FORWARD       1968  'to 1968'
            678_0  COME_FROM           564  '564'

 L. 747       678  LOAD_FAST                'word'
              680  LOAD_STR                 '2'
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   772  'to 772'

 L. 748       688  LOAD_FAST                'wordNextNext'
              690  LOAD_FAST                'year_multiples'
              692  COMPARE_OP               in
          694_696  POP_JUMP_IF_FALSE   772  'to 772'

 L. 749       698  LOAD_CONST               2
              700  STORE_FAST               'multiplier'

 L. 750       702  LOAD_FAST                'used'
              704  LOAD_CONST               2
              706  INPLACE_ADD      
              708  STORE_FAST               'used'

 L. 751       710  LOAD_FAST                'wordNextNext'
              712  LOAD_STR                 'decennia'
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   730  'to 730'

 L. 752       720  LOAD_FAST                'multiplier'
              722  LOAD_CONST               10
              724  BINARY_MULTIPLY  
              726  STORE_DEREF              'yearOffset'
              728  JUMP_FORWARD       1968  'to 1968'
            730_0  COME_FROM           716  '716'

 L. 753       730  LOAD_FAST                'wordNextNext'
              732  LOAD_STR                 'eeuwen'
              734  COMPARE_OP               ==
          736_738  POP_JUMP_IF_FALSE   750  'to 750'

 L. 754       740  LOAD_FAST                'multiplier'
              742  LOAD_CONST               100
              744  BINARY_MULTIPLY  
              746  STORE_DEREF              'yearOffset'
              748  JUMP_FORWARD       1968  'to 1968'
            750_0  COME_FROM           736  '736'

 L. 755       750  LOAD_FAST                'wordNextNext'
              752  LOAD_STR                 'millennia'
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 756       760  LOAD_FAST                'multiplier'
              762  LOAD_CONST               1000
              764  BINARY_MULTIPLY  
              766  STORE_DEREF              'yearOffset'
          768_770  JUMP_FORWARD       1968  'to 1968'
            772_0  COME_FROM           694  '694'
            772_1  COME_FROM           684  '684'

 L. 757       772  LOAD_FAST                'word'
              774  LOAD_STR                 '2'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   858  'to 858'

 L. 758       782  LOAD_FAST                'wordNextNext'
              784  LOAD_FAST                'day_multiples'
              786  COMPARE_OP               in
          788_790  POP_JUMP_IF_FALSE   858  'to 858'

 L. 759       792  LOAD_CONST               2
              794  STORE_FAST               'multiplier'

 L. 760       796  LOAD_FAST                'used'
              798  LOAD_CONST               2
              800  INPLACE_ADD      
              802  STORE_FAST               'used'

 L. 761       804  LOAD_FAST                'wordNextNext'
              806  LOAD_STR                 'jaren'
              808  COMPARE_OP               ==
          810_812  POP_JUMP_IF_FALSE   820  'to 820'

 L. 762       814  LOAD_FAST                'multiplier'
              816  STORE_DEREF              'yearOffset'
              818  JUMP_FORWARD       1968  'to 1968'
            820_0  COME_FROM           810  '810'

 L. 763       820  LOAD_FAST                'wordNextNext'
              822  LOAD_STR                 'maanden'
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE   836  'to 836'

 L. 764       830  LOAD_FAST                'multiplier'
              832  STORE_DEREF              'monthOffset'
              834  JUMP_FORWARD       1968  'to 1968'
            836_0  COME_FROM           826  '826'

 L. 765       836  LOAD_FAST                'wordNextNext'
              838  LOAD_STR                 'weken'
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 766       846  LOAD_FAST                'multiplier'
              848  LOAD_CONST               7
              850  BINARY_MULTIPLY  
              852  STORE_DEREF              'dayOffset'
          854_856  JUMP_FORWARD       1968  'to 1968'
            858_0  COME_FROM           788  '788'
            858_1  COME_FROM           778  '778'

 L. 767       858  LOAD_FAST                'word'
              860  LOAD_DEREF               'timeQualifiersList'
              862  COMPARE_OP               in
          864_866  POP_JUMP_IF_FALSE   876  'to 876'

 L. 768       868  LOAD_FAST                'word'
              870  STORE_FAST               'timeQualifier'
          872_874  JUMP_FORWARD       1968  'to 1968'
            876_0  COME_FROM           864  '864'

 L. 770       876  LOAD_FAST                'word'
              878  LOAD_STR                 'vandaag'
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   908  'to 908'
              886  LOAD_FAST                'fromFlag'
          888_890  POP_JUMP_IF_TRUE    908  'to 908'

 L. 771       892  LOAD_CONST               0
              894  STORE_DEREF              'dayOffset'

 L. 772       896  LOAD_FAST                'used'
              898  LOAD_CONST               1
              900  INPLACE_ADD      
              902  STORE_FAST               'used'
          904_906  JUMP_FORWARD       1968  'to 1968'
            908_0  COME_FROM           888  '888'
            908_1  COME_FROM           882  '882'

 L. 773       908  LOAD_FAST                'word'
              910  LOAD_STR                 'morgen'
              912  COMPARE_OP               ==
          914_916  POP_JUMP_IF_FALSE   940  'to 940'
              918  LOAD_FAST                'fromFlag'
          920_922  POP_JUMP_IF_TRUE    940  'to 940'

 L. 774       924  LOAD_CONST               1
              926  STORE_DEREF              'dayOffset'

 L. 775       928  LOAD_FAST                'used'
              930  LOAD_CONST               1
              932  INPLACE_ADD      
              934  STORE_FAST               'used'
          936_938  JUMP_FORWARD       1968  'to 1968'
            940_0  COME_FROM           920  '920'
            940_1  COME_FROM           914  '914'

 L. 776       940  LOAD_FAST                'word'
              942  LOAD_STR                 'overmorgen'
              944  COMPARE_OP               ==
          946_948  POP_JUMP_IF_FALSE   972  'to 972'
              950  LOAD_FAST                'fromFlag'
          952_954  POP_JUMP_IF_TRUE    972  'to 972'

 L. 777       956  LOAD_CONST               2
              958  STORE_DEREF              'dayOffset'

 L. 778       960  LOAD_FAST                'used'
              962  LOAD_CONST               1
              964  INPLACE_ADD      
              966  STORE_FAST               'used'
          968_970  JUMP_FORWARD       1968  'to 1968'
            972_0  COME_FROM           952  '952'
            972_1  COME_FROM           946  '946'

 L. 780       972  LOAD_FAST                'word'
              974  LOAD_STR                 'dag'
              976  COMPARE_OP               ==
          978_980  POP_JUMP_IF_TRUE    992  'to 992'
              982  LOAD_FAST                'word'
              984  LOAD_STR                 'dagen'
              986  COMPARE_OP               ==
          988_990  POP_JUMP_IF_FALSE  1034  'to 1034'
            992_0  COME_FROM           978  '978'

 L. 781       992  LOAD_FAST                'wordPrev'
              994  LOAD_CONST               0
              996  BINARY_SUBSCR    
              998  LOAD_METHOD              isdigit
             1000  CALL_METHOD_0         0  '0 positional arguments'
         1002_1004  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 782      1006  LOAD_DEREF               'dayOffset'
             1008  LOAD_GLOBAL              int
             1010  LOAD_FAST                'wordPrev'
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  INPLACE_ADD      
             1016  STORE_DEREF              'dayOffset'

 L. 783      1018  LOAD_FAST                'start'
             1020  LOAD_CONST               1
             1022  INPLACE_SUBTRACT 
             1024  STORE_FAST               'start'

 L. 784      1026  LOAD_CONST               2
             1028  STORE_FAST               'used'
         1030_1032  JUMP_FORWARD       1968  'to 1968'
           1034_0  COME_FROM           988  '988'

 L. 785      1034  LOAD_FAST                'word'
             1036  LOAD_STR                 'week'
             1038  COMPARE_OP               ==
         1040_1042  POP_JUMP_IF_TRUE   1060  'to 1060'
             1044  LOAD_FAST                'word'
             1046  LOAD_STR                 'weken'
             1048  COMPARE_OP               ==
         1050_1052  POP_JUMP_IF_FALSE  1162  'to 1162'
             1054  LOAD_FAST                'fromFlag'
         1056_1058  POP_JUMP_IF_TRUE   1162  'to 1162'
           1060_0  COME_FROM          1040  '1040'

 L. 786      1060  LOAD_FAST                'wordPrev'
             1062  LOAD_CONST               0
             1064  BINARY_SUBSCR    
             1066  LOAD_METHOD              isdigit
             1068  CALL_METHOD_0         0  '0 positional arguments'
         1070_1072  POP_JUMP_IF_FALSE  1104  'to 1104'

 L. 787      1074  LOAD_DEREF               'dayOffset'
             1076  LOAD_GLOBAL              int
             1078  LOAD_FAST                'wordPrev'
             1080  CALL_FUNCTION_1       1  '1 positional argument'
             1082  LOAD_CONST               7
             1084  BINARY_MULTIPLY  
             1086  INPLACE_ADD      
             1088  STORE_DEREF              'dayOffset'

 L. 788      1090  LOAD_FAST                'start'
             1092  LOAD_CONST               1
             1094  INPLACE_SUBTRACT 
             1096  STORE_FAST               'start'

 L. 789      1098  LOAD_CONST               2
             1100  STORE_FAST               'used'
             1102  JUMP_FORWARD       1968  'to 1968'
           1104_0  COME_FROM          1070  '1070'

 L. 790      1104  LOAD_FAST                'wordPrev'
             1106  LOAD_STR                 'volgende'
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 791      1114  LOAD_CONST               7
             1116  STORE_DEREF              'dayOffset'

 L. 792      1118  LOAD_FAST                'start'
             1120  LOAD_CONST               1
             1122  INPLACE_SUBTRACT 
             1124  STORE_FAST               'start'

 L. 793      1126  LOAD_CONST               2
             1128  STORE_FAST               'used'
             1130  JUMP_FORWARD       1968  'to 1968'
           1132_0  COME_FROM          1110  '1110'

 L. 794      1132  LOAD_FAST                'wordPrev'
             1134  LOAD_STR                 'vorige'
             1136  COMPARE_OP               ==
         1138_1140  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 795      1142  LOAD_CONST               -7
             1144  STORE_DEREF              'dayOffset'

 L. 796      1146  LOAD_FAST                'start'
             1148  LOAD_CONST               1
             1150  INPLACE_SUBTRACT 
             1152  STORE_FAST               'start'

 L. 797      1154  LOAD_CONST               2
             1156  STORE_FAST               'used'
         1158_1160  JUMP_FORWARD       1968  'to 1968'
           1162_0  COME_FROM          1056  '1056'
           1162_1  COME_FROM          1050  '1050'

 L. 799      1162  LOAD_FAST                'word'
             1164  LOAD_STR                 'maand'
             1166  COMPARE_OP               ==
         1168_1170  POP_JUMP_IF_FALSE  1272  'to 1272'
             1172  LOAD_FAST                'fromFlag'
         1174_1176  POP_JUMP_IF_TRUE   1272  'to 1272'

 L. 800      1178  LOAD_FAST                'wordPrev'
             1180  LOAD_CONST               0
             1182  BINARY_SUBSCR    
             1184  LOAD_METHOD              isdigit
             1186  CALL_METHOD_0         0  '0 positional arguments'
         1188_1190  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 801      1192  LOAD_GLOBAL              int
             1194  LOAD_FAST                'wordPrev'
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  STORE_DEREF              'monthOffset'

 L. 802      1200  LOAD_FAST                'start'
             1202  LOAD_CONST               1
             1204  INPLACE_SUBTRACT 
             1206  STORE_FAST               'start'

 L. 803      1208  LOAD_CONST               2
             1210  STORE_FAST               'used'
             1212  JUMP_FORWARD       1968  'to 1968'
           1214_0  COME_FROM          1188  '1188'

 L. 804      1214  LOAD_FAST                'wordPrev'
             1216  LOAD_STR                 'volgende'
             1218  COMPARE_OP               ==
         1220_1222  POP_JUMP_IF_FALSE  1242  'to 1242'

 L. 805      1224  LOAD_CONST               1
             1226  STORE_DEREF              'monthOffset'

 L. 806      1228  LOAD_FAST                'start'
             1230  LOAD_CONST               1
             1232  INPLACE_SUBTRACT 
             1234  STORE_FAST               'start'

 L. 807      1236  LOAD_CONST               2
             1238  STORE_FAST               'used'
             1240  JUMP_FORWARD       1968  'to 1968'
           1242_0  COME_FROM          1220  '1220'

 L. 808      1242  LOAD_FAST                'wordPrev'
             1244  LOAD_STR                 'vorige'
             1246  COMPARE_OP               ==
         1248_1250  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 809      1252  LOAD_CONST               -1
             1254  STORE_DEREF              'monthOffset'

 L. 810      1256  LOAD_FAST                'start'
             1258  LOAD_CONST               1
             1260  INPLACE_SUBTRACT 
             1262  STORE_FAST               'start'

 L. 811      1264  LOAD_CONST               2
             1266  STORE_FAST               'used'
         1268_1270  JUMP_FORWARD       1968  'to 1968'
           1272_0  COME_FROM          1174  '1174'
           1272_1  COME_FROM          1168  '1168'

 L. 813      1272  LOAD_FAST                'word'
             1274  LOAD_STR                 'jaar'
             1276  COMPARE_OP               ==
         1278_1280  POP_JUMP_IF_FALSE  1382  'to 1382'
             1282  LOAD_FAST                'fromFlag'
         1284_1286  POP_JUMP_IF_TRUE   1382  'to 1382'

 L. 814      1288  LOAD_FAST                'wordPrev'
             1290  LOAD_CONST               0
             1292  BINARY_SUBSCR    
             1294  LOAD_METHOD              isdigit
             1296  CALL_METHOD_0         0  '0 positional arguments'
         1298_1300  POP_JUMP_IF_FALSE  1324  'to 1324'

 L. 815      1302  LOAD_GLOBAL              int
             1304  LOAD_FAST                'wordPrev'
             1306  CALL_FUNCTION_1       1  '1 positional argument'
             1308  STORE_DEREF              'yearOffset'

 L. 816      1310  LOAD_FAST                'start'
             1312  LOAD_CONST               1
             1314  INPLACE_SUBTRACT 
             1316  STORE_FAST               'start'

 L. 817      1318  LOAD_CONST               2
             1320  STORE_FAST               'used'
             1322  JUMP_FORWARD       1968  'to 1968'
           1324_0  COME_FROM          1298  '1298'

 L. 818      1324  LOAD_FAST                'wordPrev'
             1326  LOAD_STR                 'volgend'
             1328  COMPARE_OP               ==
         1330_1332  POP_JUMP_IF_FALSE  1352  'to 1352'

 L. 819      1334  LOAD_CONST               1
             1336  STORE_DEREF              'yearOffset'

 L. 820      1338  LOAD_FAST                'start'
             1340  LOAD_CONST               1
             1342  INPLACE_SUBTRACT 
             1344  STORE_FAST               'start'

 L. 821      1346  LOAD_CONST               2
             1348  STORE_FAST               'used'
             1350  JUMP_FORWARD       1968  'to 1968'
           1352_0  COME_FROM          1330  '1330'

 L. 822      1352  LOAD_FAST                'wordPrev'
             1354  LOAD_STR                 'vorig'
             1356  COMPARE_OP               ==
         1358_1360  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 823      1362  LOAD_CONST               -1
             1364  STORE_DEREF              'yearOffset'

 L. 824      1366  LOAD_FAST                'start'
             1368  LOAD_CONST               1
             1370  INPLACE_SUBTRACT 
             1372  STORE_FAST               'start'

 L. 825      1374  LOAD_CONST               2
             1376  STORE_FAST               'used'
         1378_1380  JUMP_FORWARD       1968  'to 1968'
           1382_0  COME_FROM          1284  '1284'
           1382_1  COME_FROM          1278  '1278'

 L. 828      1382  LOAD_FAST                'word'
             1384  LOAD_FAST                'days'
             1386  COMPARE_OP               in
         1388_1390  POP_JUMP_IF_FALSE  1530  'to 1530'
             1392  LOAD_FAST                'fromFlag'
         1394_1396  POP_JUMP_IF_TRUE   1530  'to 1530'

 L. 829      1398  LOAD_FAST                'days'
             1400  LOAD_METHOD              index
             1402  LOAD_FAST                'word'
             1404  CALL_METHOD_1         1  '1 positional argument'
             1406  STORE_FAST               'd'

 L. 830      1408  LOAD_FAST                'd'
             1410  LOAD_CONST               1
             1412  BINARY_ADD       
             1414  LOAD_GLOBAL              int
             1416  LOAD_FAST                'today'
             1418  CALL_FUNCTION_1       1  '1 positional argument'
             1420  BINARY_SUBTRACT  
             1422  STORE_DEREF              'dayOffset'

 L. 831      1424  LOAD_CONST               1
             1426  STORE_FAST               'used'

 L. 832      1428  LOAD_DEREF               'dayOffset'
             1430  LOAD_CONST               0
             1432  COMPARE_OP               <
         1434_1436  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 833      1438  LOAD_DEREF               'dayOffset'
             1440  LOAD_CONST               7
             1442  INPLACE_ADD      
             1444  STORE_DEREF              'dayOffset'
           1446_0  COME_FROM          1434  '1434'

 L. 834      1446  LOAD_FAST                'wordPrev'
             1448  LOAD_STR                 'volgende'
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1492  'to 1492'

 L. 835      1456  LOAD_DEREF               'dayOffset'
             1458  LOAD_CONST               2
             1460  COMPARE_OP               <=
         1462_1464  POP_JUMP_IF_FALSE  1474  'to 1474'

 L. 836      1466  LOAD_DEREF               'dayOffset'
             1468  LOAD_CONST               7
             1470  INPLACE_ADD      
             1472  STORE_DEREF              'dayOffset'
           1474_0  COME_FROM          1462  '1462'

 L. 837      1474  LOAD_FAST                'used'
             1476  LOAD_CONST               1
             1478  INPLACE_ADD      
             1480  STORE_FAST               'used'

 L. 838      1482  LOAD_FAST                'start'
             1484  LOAD_CONST               1
             1486  INPLACE_SUBTRACT 
             1488  STORE_FAST               'start'
             1490  JUMP_FORWARD       1968  'to 1968'
           1492_0  COME_FROM          1452  '1452'

 L. 839      1492  LOAD_FAST                'wordPrev'
             1494  LOAD_STR                 'vorige'
             1496  COMPARE_OP               ==
         1498_1500  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 840      1502  LOAD_DEREF               'dayOffset'
             1504  LOAD_CONST               7
             1506  INPLACE_SUBTRACT 
             1508  STORE_DEREF              'dayOffset'

 L. 841      1510  LOAD_FAST                'used'
             1512  LOAD_CONST               1
             1514  INPLACE_ADD      
             1516  STORE_FAST               'used'

 L. 842      1518  LOAD_FAST                'start'
             1520  LOAD_CONST               1
             1522  INPLACE_SUBTRACT 
             1524  STORE_FAST               'start'
         1526_1528  JUMP_FORWARD       1968  'to 1968'
           1530_0  COME_FROM          1394  '1394'
           1530_1  COME_FROM          1388  '1388'

 L. 843      1530  LOAD_FAST                'word'
             1532  LOAD_FAST                'day_parts'
             1534  COMPARE_OP               in
         1536_1538  POP_JUMP_IF_FALSE  1602  'to 1602'
             1540  LOAD_FAST                'fromFlag'
         1542_1544  POP_JUMP_IF_TRUE   1602  'to 1602'

 L. 844      1546  LOAD_FAST                'day_parts'
             1548  LOAD_METHOD              index
             1550  LOAD_FAST                'word'
             1552  CALL_METHOD_1         1  '1 positional argument'
             1554  LOAD_GLOBAL              len
             1556  LOAD_DEREF               'timeQualifiersList'
             1558  CALL_FUNCTION_1       1  '1 positional argument'
             1560  BINARY_TRUE_DIVIDE
             1562  STORE_FAST               'd'

 L. 845      1564  LOAD_FAST                'd'
             1566  LOAD_CONST               1
             1568  BINARY_ADD       
             1570  LOAD_GLOBAL              int
             1572  LOAD_FAST                'today'
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  BINARY_SUBTRACT  
             1578  STORE_DEREF              'dayOffset'

 L. 846      1580  LOAD_DEREF               'dayOffset'
             1582  LOAD_CONST               0
             1584  COMPARE_OP               <
         1586_1588  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 847      1590  LOAD_DEREF               'dayOffset'
             1592  LOAD_CONST               7
             1594  INPLACE_ADD      
             1596  STORE_DEREF              'dayOffset'
         1598_1600  JUMP_FORWARD       1968  'to 1968'
           1602_0  COME_FROM          1542  '1542'
           1602_1  COME_FROM          1536  '1536'

 L. 849      1602  LOAD_FAST                'word'
             1604  LOAD_FAST                'months'
             1606  COMPARE_OP               in
         1608_1610  POP_JUMP_IF_TRUE   1628  'to 1628'
             1612  LOAD_FAST                'word'
             1614  LOAD_FAST                'months_short'
             1616  COMPARE_OP               in
         1618_1620  POP_JUMP_IF_FALSE  1968  'to 1968'
             1622  LOAD_FAST                'fromFlag'
         1624_1626  POP_JUMP_IF_TRUE   1968  'to 1968'
           1628_0  COME_FROM          1608  '1608'

 L. 850      1628  SETUP_EXCEPT       1644  'to 1644'

 L. 851      1630  LOAD_FAST                'months'
             1632  LOAD_METHOD              index
             1634  LOAD_FAST                'word'
             1636  CALL_METHOD_1         1  '1 positional argument'
             1638  STORE_FAST               'm'
             1640  POP_BLOCK        
             1642  JUMP_FORWARD       1676  'to 1676'
           1644_0  COME_FROM_EXCEPT   1628  '1628'

 L. 852      1644  DUP_TOP          
             1646  LOAD_GLOBAL              ValueError
             1648  COMPARE_OP               exception-match
         1650_1652  POP_JUMP_IF_FALSE  1674  'to 1674'
             1654  POP_TOP          
             1656  POP_TOP          
             1658  POP_TOP          

 L. 853      1660  LOAD_FAST                'months_short'
             1662  LOAD_METHOD              index
             1664  LOAD_FAST                'word'
             1666  CALL_METHOD_1         1  '1 positional argument'
             1668  STORE_FAST               'm'
             1670  POP_EXCEPT       
             1672  JUMP_FORWARD       1676  'to 1676'
           1674_0  COME_FROM          1650  '1650'
             1674  END_FINALLY      
           1676_0  COME_FROM          1672  '1672'
           1676_1  COME_FROM          1642  '1642'

 L. 854      1676  LOAD_FAST                'used'
             1678  LOAD_CONST               1
             1680  INPLACE_ADD      
             1682  STORE_FAST               'used'

 L. 855      1684  LOAD_FAST                'months'
             1686  LOAD_FAST                'm'
             1688  BINARY_SUBSCR    
             1690  STORE_DEREF              'datestr'

 L. 856      1692  LOAD_FAST                'wordPrev'
         1694_1696  POP_JUMP_IF_FALSE  1878  'to 1878'

 L. 857      1698  LOAD_FAST                'wordPrev'
             1700  LOAD_CONST               0
             1702  BINARY_SUBSCR    
             1704  LOAD_METHOD              isdigit
             1706  CALL_METHOD_0         0  '0 positional arguments'
         1708_1710  POP_JUMP_IF_TRUE   1736  'to 1736'
             1712  LOAD_FAST                'wordPrev'
             1714  LOAD_STR                 'van'
             1716  COMPARE_OP               ==
         1718_1720  POP_JUMP_IF_FALSE  1878  'to 1878'

 L. 858      1722  LOAD_FAST                'wordPrevPrev'
             1724  LOAD_CONST               0
             1726  BINARY_SUBSCR    
             1728  LOAD_METHOD              isdigit
             1730  CALL_METHOD_0         0  '0 positional arguments'
         1732_1734  POP_JUMP_IF_FALSE  1878  'to 1878'
           1736_0  COME_FROM          1708  '1708'

 L. 859      1736  LOAD_FAST                'wordPrev'
             1738  LOAD_STR                 'van'
             1740  COMPARE_OP               ==
         1742_1744  POP_JUMP_IF_FALSE  1798  'to 1798'
             1746  LOAD_FAST                'wordPrevPrev'
             1748  LOAD_CONST               0
             1750  BINARY_SUBSCR    
             1752  LOAD_METHOD              isdigit
             1754  CALL_METHOD_0         0  '0 positional arguments'
         1756_1758  POP_JUMP_IF_FALSE  1798  'to 1798'

 L. 860      1760  LOAD_DEREF               'datestr'
             1762  LOAD_STR                 ' '
             1764  LOAD_FAST                'words'
             1766  LOAD_FAST                'idx'
             1768  LOAD_CONST               2
             1770  BINARY_SUBTRACT  
             1772  BINARY_SUBSCR    
             1774  BINARY_ADD       
             1776  INPLACE_ADD      
             1778  STORE_DEREF              'datestr'

 L. 861      1780  LOAD_FAST                'used'
             1782  LOAD_CONST               1
             1784  INPLACE_ADD      
             1786  STORE_FAST               'used'

 L. 862      1788  LOAD_FAST                'start'
             1790  LOAD_CONST               1
             1792  INPLACE_SUBTRACT 
             1794  STORE_FAST               'start'
             1796  JUMP_FORWARD       1810  'to 1810'
           1798_0  COME_FROM          1756  '1756'
           1798_1  COME_FROM          1742  '1742'

 L. 864      1798  LOAD_DEREF               'datestr'
             1800  LOAD_STR                 ' '
             1802  LOAD_FAST                'wordPrev'
             1804  BINARY_ADD       
             1806  INPLACE_ADD      
             1808  STORE_DEREF              'datestr'
           1810_0  COME_FROM          1796  '1796'

 L. 865      1810  LOAD_FAST                'start'
             1812  LOAD_CONST               1
             1814  INPLACE_SUBTRACT 
             1816  STORE_FAST               'start'

 L. 866      1818  LOAD_FAST                'used'
             1820  LOAD_CONST               1
             1822  INPLACE_ADD      
             1824  STORE_FAST               'used'

 L. 867      1826  LOAD_FAST                'wordNext'
         1828_1830  POP_JUMP_IF_FALSE  1872  'to 1872'
             1832  LOAD_FAST                'wordNext'
             1834  LOAD_CONST               0
             1836  BINARY_SUBSCR    
             1838  LOAD_METHOD              isdigit
             1840  CALL_METHOD_0         0  '0 positional arguments'
         1842_1844  POP_JUMP_IF_FALSE  1872  'to 1872'

 L. 868      1846  LOAD_DEREF               'datestr'
             1848  LOAD_STR                 ' '
             1850  LOAD_FAST                'wordNext'
             1852  BINARY_ADD       
             1854  INPLACE_ADD      
             1856  STORE_DEREF              'datestr'

 L. 869      1858  LOAD_FAST                'used'
             1860  LOAD_CONST               1
             1862  INPLACE_ADD      
             1864  STORE_FAST               'used'

 L. 870      1866  LOAD_CONST               True
             1868  STORE_FAST               'hasYear'
             1870  JUMP_FORWARD       1876  'to 1876'
           1872_0  COME_FROM          1842  '1842'
           1872_1  COME_FROM          1828  '1828'

 L. 872      1872  LOAD_CONST               False
             1874  STORE_FAST               'hasYear'
           1876_0  COME_FROM          1870  '1870'
             1876  JUMP_FORWARD       1968  'to 1968'
           1878_0  COME_FROM          1732  '1732'
           1878_1  COME_FROM          1718  '1718'
           1878_2  COME_FROM          1694  '1694'

 L. 874      1878  LOAD_FAST                'wordNext'
         1880_1882  POP_JUMP_IF_FALSE  1968  'to 1968'
             1884  LOAD_FAST                'wordNext'
             1886  LOAD_CONST               0
             1888  BINARY_SUBSCR    
             1890  LOAD_METHOD              isdigit
             1892  CALL_METHOD_0         0  '0 positional arguments'
         1894_1896  POP_JUMP_IF_FALSE  1968  'to 1968'

 L. 875      1898  LOAD_DEREF               'datestr'
             1900  LOAD_STR                 ' '
             1902  LOAD_FAST                'wordNext'
             1904  BINARY_ADD       
             1906  INPLACE_ADD      
             1908  STORE_DEREF              'datestr'
           1910_0  COME_FROM          1322  '1322'
           1910_1  COME_FROM          1212  '1212'
           1910_2  COME_FROM          1102  '1102'

 L. 876      1910  LOAD_FAST                'used'
             1912  LOAD_CONST               1
             1914  INPLACE_ADD      
             1916  STORE_FAST               'used'

 L. 877      1918  LOAD_FAST                'wordNextNext'
         1920_1922  POP_JUMP_IF_FALSE  1964  'to 1964'
             1924  LOAD_FAST                'wordNextNext'
           1926_0  COME_FROM           728  '728'
           1926_1  COME_FROM           634  '634'
             1926  LOAD_CONST               0
             1928  BINARY_SUBSCR    
           1930_0  COME_FROM          1490  '1490'
           1930_1  COME_FROM           818  '818'
             1930  LOAD_METHOD              isdigit
             1932  CALL_METHOD_0         0  '0 positional arguments'
         1934_1936  POP_JUMP_IF_FALSE  1964  'to 1964'
           1938_0  COME_FROM          1350  '1350'
           1938_1  COME_FROM          1240  '1240'
           1938_2  COME_FROM          1130  '1130'

 L. 878      1938  LOAD_DEREF               'datestr'
             1940  LOAD_STR                 ' '
             1942  LOAD_FAST                'wordNextNext'
             1944  BINARY_ADD       
           1946_0  COME_FROM           834  '834'
           1946_1  COME_FROM           748  '748'
           1946_2  COME_FROM           654  '654'
             1946  INPLACE_ADD      
             1948  STORE_DEREF              'datestr'

 L. 879      1950  LOAD_FAST                'used'
             1952  LOAD_CONST               1
             1954  INPLACE_ADD      
             1956  STORE_FAST               'used'

 L. 880      1958  LOAD_CONST               True
             1960  STORE_FAST               'hasYear'
             1962  JUMP_FORWARD       1968  'to 1968'
           1964_0  COME_FROM          1934  '1934'
           1964_1  COME_FROM          1920  '1920'

 L. 882      1964  LOAD_CONST               False
             1966  STORE_FAST               'hasYear'
           1968_0  COME_FROM          1962  '1962'
           1968_1  COME_FROM          1894  '1894'
           1968_2  COME_FROM          1880  '1880'
           1968_3  COME_FROM          1876  '1876'
           1968_4  COME_FROM          1624  '1624'
           1968_5  COME_FROM          1618  '1618'
           1968_6  COME_FROM          1598  '1598'
           1968_7  COME_FROM          1586  '1586'
           1968_8  COME_FROM          1526  '1526'
           1968_9  COME_FROM          1498  '1498'
          1968_10  COME_FROM          1378  '1378'
          1968_11  COME_FROM          1358  '1358'
          1968_12  COME_FROM          1268  '1268'
          1968_13  COME_FROM          1248  '1248'
          1968_14  COME_FROM          1158  '1158'
          1968_15  COME_FROM          1138  '1138'
          1968_16  COME_FROM          1030  '1030'
          1968_17  COME_FROM          1002  '1002'
          1968_18  COME_FROM           968  '968'
          1968_19  COME_FROM           936  '936'
          1968_20  COME_FROM           904  '904'
          1968_21  COME_FROM           872  '872'
          1968_22  COME_FROM           854  '854'
          1968_23  COME_FROM           842  '842'
          1968_24  COME_FROM           768  '768'
          1968_25  COME_FROM           756  '756'
          1968_26  COME_FROM           674  '674'
          1968_27  COME_FROM           662  '662'

 L. 886      1968  LOAD_FAST                'days'
             1970  LOAD_FAST                'months'
             1972  BINARY_ADD       
             1974  LOAD_FAST                'months_short'
             1976  BINARY_ADD       
             1978  STORE_FAST               'validFollowups'

 L. 887      1980  LOAD_FAST                'validFollowups'
             1982  LOAD_METHOD              append
             1984  LOAD_STR                 'vandaag'
             1986  CALL_METHOD_1         1  '1 positional argument'
             1988  POP_TOP          

 L. 888      1990  LOAD_FAST                'validFollowups'
             1992  LOAD_METHOD              append
             1994  LOAD_STR                 'morgen'
             1996  CALL_METHOD_1         1  '1 positional argument'
             1998  POP_TOP          

 L. 889      2000  LOAD_FAST                'validFollowups'
             2002  LOAD_METHOD              append
             2004  LOAD_STR                 'volgende'
             2006  CALL_METHOD_1         1  '1 positional argument'
             2008  POP_TOP          

 L. 890      2010  LOAD_FAST                'validFollowups'
             2012  LOAD_METHOD              append
             2014  LOAD_STR                 'vorige'
             2016  CALL_METHOD_1         1  '1 positional argument'
             2018  POP_TOP          

 L. 891      2020  LOAD_FAST                'validFollowups'
             2022  LOAD_METHOD              append
             2024  LOAD_STR                 'nu'
             2026  CALL_METHOD_1         1  '1 positional argument'
             2028  POP_TOP          

 L. 892      2030  LOAD_FAST                'word'
             2032  LOAD_STR                 'van'
             2034  COMPARE_OP               ==
         2036_2038  POP_JUMP_IF_TRUE   2050  'to 2050'
             2040  LOAD_FAST                'word'
             2042  LOAD_STR                 'na'
             2044  COMPARE_OP               ==
         2046_2048  POP_JUMP_IF_FALSE  2310  'to 2310'
           2050_0  COME_FROM          2036  '2036'
             2050  LOAD_FAST                'wordNext'
             2052  LOAD_FAST                'validFollowups'
             2054  COMPARE_OP               in
         2056_2058  POP_JUMP_IF_FALSE  2310  'to 2310'

 L. 893      2060  LOAD_CONST               2
             2062  STORE_FAST               'used'

 L. 894      2064  LOAD_CONST               True
             2066  STORE_FAST               'fromFlag'

 L. 895      2068  LOAD_FAST                'wordNext'
             2070  LOAD_STR                 'morgen'
             2072  COMPARE_OP               ==
         2074_2076  POP_JUMP_IF_FALSE  2088  'to 2088'

 L. 896      2078  LOAD_DEREF               'dayOffset'
             2080  LOAD_CONST               1
             2082  INPLACE_ADD      
             2084  STORE_DEREF              'dayOffset'
             2086  JUMP_FORWARD       2310  'to 2310'
           2088_0  COME_FROM          2074  '2074'

 L. 897      2088  LOAD_FAST                'wordNext'
             2090  LOAD_STR                 'overmorgen'
             2092  COMPARE_OP               ==
         2094_2096  POP_JUMP_IF_FALSE  2108  'to 2108'

 L. 898      2098  LOAD_DEREF               'dayOffset'
             2100  LOAD_CONST               2
             2102  INPLACE_ADD      
             2104  STORE_DEREF              'dayOffset'
             2106  JUMP_FORWARD       2310  'to 2310'
           2108_0  COME_FROM          2094  '2094'

 L. 899      2108  LOAD_FAST                'wordNext'
             2110  LOAD_FAST                'days'
             2112  COMPARE_OP               in
         2114_2116  POP_JUMP_IF_FALSE  2176  'to 2176'

 L. 900      2118  LOAD_FAST                'days'
             2120  LOAD_METHOD              index
             2122  LOAD_FAST                'wordNext'
             2124  CALL_METHOD_1         1  '1 positional argument'
             2126  STORE_FAST               'd'

 L. 901      2128  LOAD_FAST                'd'
             2130  LOAD_CONST               1
             2132  BINARY_ADD       
             2134  LOAD_GLOBAL              int
             2136  LOAD_FAST                'today'
             2138  CALL_FUNCTION_1       1  '1 positional argument'
             2140  BINARY_SUBTRACT  
             2142  STORE_FAST               'tmpOffset'

 L. 902      2144  LOAD_CONST               2
             2146  STORE_FAST               'used'

 L. 903      2148  LOAD_FAST                'tmpOffset'
             2150  LOAD_CONST               0
             2152  COMPARE_OP               <
         2154_2156  POP_JUMP_IF_FALSE  2166  'to 2166'

 L. 904      2158  LOAD_FAST                'tmpOffset'
             2160  LOAD_CONST               7
             2162  INPLACE_ADD      
             2164  STORE_FAST               'tmpOffset'
           2166_0  COME_FROM          2154  '2154'

 L. 905      2166  LOAD_DEREF               'dayOffset'
             2168  LOAD_FAST                'tmpOffset'
             2170  INPLACE_ADD      
             2172  STORE_DEREF              'dayOffset'
             2174  JUMP_FORWARD       2310  'to 2310'
           2176_0  COME_FROM          2114  '2114'

 L. 906      2176  LOAD_FAST                'wordNextNext'
         2178_2180  POP_JUMP_IF_FALSE  2310  'to 2310'
             2182  LOAD_FAST                'wordNextNext'
             2184  LOAD_FAST                'days'
             2186  COMPARE_OP               in
         2188_2190  POP_JUMP_IF_FALSE  2310  'to 2310'

 L. 907      2192  LOAD_FAST                'days'
             2194  LOAD_METHOD              index
             2196  LOAD_FAST                'wordNextNext'
             2198  CALL_METHOD_1         1  '1 positional argument'
             2200  STORE_FAST               'd'

 L. 908      2202  LOAD_FAST                'd'
             2204  LOAD_CONST               1
             2206  BINARY_ADD       
             2208  LOAD_GLOBAL              int
             2210  LOAD_FAST                'today'
             2212  CALL_FUNCTION_1       1  '1 positional argument'
             2214  BINARY_SUBTRACT  
             2216  STORE_FAST               'tmpOffset'

 L. 909      2218  LOAD_CONST               3
             2220  STORE_FAST               'used'

 L. 910      2222  LOAD_FAST                'wordNext'
             2224  LOAD_STR                 'volgende'
             2226  COMPARE_OP               ==
         2228_2230  POP_JUMP_IF_FALSE  2268  'to 2268'

 L. 911      2232  LOAD_DEREF               'dayOffset'
             2234  LOAD_CONST               2
             2236  COMPARE_OP               <=
         2238_2240  POP_JUMP_IF_FALSE  2250  'to 2250'

 L. 912      2242  LOAD_FAST                'tmpOffset'
             2244  LOAD_CONST               7
             2246  INPLACE_ADD      
             2248  STORE_FAST               'tmpOffset'
           2250_0  COME_FROM          2238  '2238'

 L. 913      2250  LOAD_FAST                'used'
             2252  LOAD_CONST               1
             2254  INPLACE_ADD      
             2256  STORE_FAST               'used'

 L. 914      2258  LOAD_FAST                'start'
             2260  LOAD_CONST               1
             2262  INPLACE_SUBTRACT 
             2264  STORE_FAST               'start'
             2266  JUMP_FORWARD       2302  'to 2302'
           2268_0  COME_FROM          2228  '2228'

 L. 915      2268  LOAD_FAST                'wordNext'
             2270  LOAD_STR                 'vorige'
             2272  COMPARE_OP               ==
         2274_2276  POP_JUMP_IF_FALSE  2302  'to 2302'

 L. 916      2278  LOAD_FAST                'tmpOffset'
             2280  LOAD_CONST               7
             2282  INPLACE_SUBTRACT 
             2284  STORE_FAST               'tmpOffset'

 L. 917      2286  LOAD_FAST                'used'
             2288  LOAD_CONST               1
             2290  INPLACE_ADD      
             2292  STORE_FAST               'used'

 L. 918      2294  LOAD_FAST                'start'
             2296  LOAD_CONST               1
             2298  INPLACE_SUBTRACT 
             2300  STORE_FAST               'start'
           2302_0  COME_FROM          2274  '2274'
           2302_1  COME_FROM          2266  '2266'

 L. 919      2302  LOAD_DEREF               'dayOffset'
             2304  LOAD_FAST                'tmpOffset'
             2306  INPLACE_ADD      
             2308  STORE_DEREF              'dayOffset'
           2310_0  COME_FROM          2188  '2188'
           2310_1  COME_FROM          2178  '2178'
           2310_2  COME_FROM          2174  '2174'
           2310_3  COME_FROM          2106  '2106'
           2310_4  COME_FROM          2086  '2086'
           2310_5  COME_FROM          2056  '2056'
           2310_6  COME_FROM          2046  '2046'

 L. 920      2310  LOAD_FAST                'used'
             2312  LOAD_CONST               0
             2314  COMPARE_OP               >
         2316_2318  POP_JUMP_IF_FALSE   334  'to 334'

 L. 921      2320  LOAD_FAST                'start'
             2322  LOAD_CONST               1
             2324  BINARY_SUBTRACT  
             2326  LOAD_CONST               0
             2328  COMPARE_OP               >
         2330_2332  POP_JUMP_IF_FALSE  2368  'to 2368'
             2334  LOAD_FAST                'words'
             2336  LOAD_FAST                'start'
             2338  LOAD_CONST               1
             2340  BINARY_SUBTRACT  
             2342  BINARY_SUBSCR    
             2344  LOAD_STR                 'deze'
             2346  COMPARE_OP               ==
         2348_2350  POP_JUMP_IF_FALSE  2368  'to 2368'

 L. 922      2352  LOAD_FAST                'start'
             2354  LOAD_CONST               1
             2356  INPLACE_SUBTRACT 
             2358  STORE_FAST               'start'

 L. 923      2360  LOAD_FAST                'used'
             2362  LOAD_CONST               1
             2364  INPLACE_ADD      
             2366  STORE_FAST               'used'
           2368_0  COME_FROM          2348  '2348'
           2368_1  COME_FROM          2330  '2330'

 L. 925      2368  SETUP_LOOP         2402  'to 2402'
             2370  LOAD_GLOBAL              range
             2372  LOAD_CONST               0
             2374  LOAD_FAST                'used'
             2376  CALL_FUNCTION_2       2  '2 positional arguments'
             2378  GET_ITER         
             2380  FOR_ITER           2400  'to 2400'
             2382  STORE_FAST               'i'

 L. 926      2384  LOAD_STR                 ''
             2386  LOAD_FAST                'words'
             2388  LOAD_FAST                'i'
             2390  LOAD_FAST                'start'
             2392  BINARY_ADD       
             2394  STORE_SUBSCR     
         2396_2398  JUMP_BACK          2380  'to 2380'
             2400  POP_BLOCK        
           2402_0  COME_FROM_LOOP     2368  '2368'

 L. 928      2402  LOAD_FAST                'start'
             2404  LOAD_CONST               1
             2406  BINARY_SUBTRACT  
             2408  LOAD_CONST               0
             2410  COMPARE_OP               >=
         2412_2414  POP_JUMP_IF_FALSE  2446  'to 2446'
             2416  LOAD_FAST                'words'
             2418  LOAD_FAST                'start'
             2420  LOAD_CONST               1
             2422  BINARY_SUBTRACT  
             2424  BINARY_SUBSCR    
             2426  LOAD_FAST                'markers'
             2428  COMPARE_OP               in
         2430_2432  POP_JUMP_IF_FALSE  2446  'to 2446'

 L. 929      2434  LOAD_STR                 ''
             2436  LOAD_FAST                'words'
             2438  LOAD_FAST                'start'
             2440  LOAD_CONST               1
             2442  BINARY_SUBTRACT  
             2444  STORE_SUBSCR     
           2446_0  COME_FROM          2430  '2430'
           2446_1  COME_FROM          2412  '2412'

 L. 930      2446  LOAD_CONST               True
             2448  STORE_DEREF              'found'

 L. 931      2450  LOAD_CONST               True
             2452  STORE_FAST               'daySpecified'
         2454_2456  JUMP_BACK           334  'to 334'
             2458  POP_BLOCK        
           2460_0  COME_FROM_LOOP      322  '322'

 L. 934      2460  LOAD_CONST               0
             2462  STORE_DEREF              'hrOffset'

 L. 935      2464  LOAD_CONST               0
             2466  STORE_DEREF              'minOffset'

 L. 936      2468  LOAD_CONST               0
             2470  STORE_DEREF              'secOffset'

 L. 937      2472  LOAD_CONST               None
             2474  STORE_DEREF              'hrAbs'

 L. 938      2476  LOAD_CONST               None
             2478  STORE_DEREF              'minAbs'

 L. 939      2480  LOAD_CONST               False
             2482  STORE_FAST               'military'

 L. 941  2484_2486  SETUP_LOOP         5676  'to 5676'
             2488  LOAD_GLOBAL              enumerate
             2490  LOAD_FAST                'words'
             2492  CALL_FUNCTION_1       1  '1 positional argument'
             2494  GET_ITER         
           2496_0  COME_FROM          5436  '5436'
         2496_2498  FOR_ITER           5674  'to 5674'
             2500  UNPACK_SEQUENCE_2     2 
             2502  STORE_FAST               'idx'
             2504  STORE_FAST               'word'

 L. 942      2506  LOAD_FAST                'word'
             2508  LOAD_STR                 ''
             2510  COMPARE_OP               ==
         2512_2514  POP_JUMP_IF_FALSE  2520  'to 2520'

 L. 943  2516_2518  CONTINUE           2496  'to 2496'
           2520_0  COME_FROM          2512  '2512'

 L. 945      2520  LOAD_FAST                'idx'
             2522  LOAD_CONST               1
             2524  COMPARE_OP               >
         2526_2528  POP_JUMP_IF_FALSE  2542  'to 2542'
             2530  LOAD_FAST                'words'
             2532  LOAD_FAST                'idx'
             2534  LOAD_CONST               2
             2536  BINARY_SUBTRACT  
             2538  BINARY_SUBSCR    
             2540  JUMP_FORWARD       2544  'to 2544'
           2542_0  COME_FROM          2526  '2526'
             2542  LOAD_STR                 ''
           2544_0  COME_FROM          2540  '2540'
             2544  STORE_FAST               'wordPrevPrev'

 L. 946      2546  LOAD_FAST                'idx'
             2548  LOAD_CONST               0
             2550  COMPARE_OP               >
         2552_2554  POP_JUMP_IF_FALSE  2568  'to 2568'
             2556  LOAD_FAST                'words'
             2558  LOAD_FAST                'idx'
             2560  LOAD_CONST               1
             2562  BINARY_SUBTRACT  
             2564  BINARY_SUBSCR    
             2566  JUMP_FORWARD       2570  'to 2570'
           2568_0  COME_FROM          2552  '2552'
             2568  LOAD_STR                 ''
           2570_0  COME_FROM          2566  '2566'
             2570  STORE_FAST               'wordPrev'

 L. 947      2572  LOAD_FAST                'idx'
             2574  LOAD_CONST               1
             2576  BINARY_ADD       
             2578  LOAD_GLOBAL              len
             2580  LOAD_FAST                'words'
             2582  CALL_FUNCTION_1       1  '1 positional argument'
             2584  COMPARE_OP               <
         2586_2588  POP_JUMP_IF_FALSE  2602  'to 2602'
             2590  LOAD_FAST                'words'
             2592  LOAD_FAST                'idx'
             2594  LOAD_CONST               1
             2596  BINARY_ADD       
             2598  BINARY_SUBSCR    
             2600  JUMP_FORWARD       2604  'to 2604'
           2602_0  COME_FROM          2586  '2586'
             2602  LOAD_STR                 ''
           2604_0  COME_FROM          2600  '2600'
             2604  STORE_FAST               'wordNext'

 L. 948      2606  LOAD_FAST                'idx'
             2608  LOAD_CONST               2
             2610  BINARY_ADD       
             2612  LOAD_GLOBAL              len
             2614  LOAD_FAST                'words'
             2616  CALL_FUNCTION_1       1  '1 positional argument'
             2618  COMPARE_OP               <
         2620_2622  POP_JUMP_IF_FALSE  2636  'to 2636'
             2624  LOAD_FAST                'words'
             2626  LOAD_FAST                'idx'
             2628  LOAD_CONST               2
             2630  BINARY_ADD       
             2632  BINARY_SUBSCR    
             2634  JUMP_FORWARD       2638  'to 2638'
           2636_0  COME_FROM          2620  '2620'
             2636  LOAD_STR                 ''
           2638_0  COME_FROM          2634  '2634'
             2638  STORE_FAST               'wordNextNext'

 L. 950      2640  LOAD_CONST               0
             2642  STORE_FAST               'used'

 L. 951      2644  LOAD_FAST                'word'
             2646  LOAD_METHOD              startswith
             2648  LOAD_STR                 'gister'
             2650  CALL_METHOD_1         1  '1 positional argument'
         2652_2654  POP_JUMP_IF_FALSE  2662  'to 2662'

 L. 952      2656  LOAD_CONST               -1
             2658  STORE_DEREF              'dayOffset'
             2660  JUMP_FORWARD       2678  'to 2678'
           2662_0  COME_FROM          2652  '2652'

 L. 953      2662  LOAD_FAST                'word'
             2664  LOAD_METHOD              startswith
             2666  LOAD_STR                 'morgen'
             2668  CALL_METHOD_1         1  '1 positional argument'
         2670_2672  POP_JUMP_IF_FALSE  2678  'to 2678'

 L. 954      2674  LOAD_CONST               1
             2676  STORE_DEREF              'dayOffset'
           2678_0  COME_FROM          2670  '2670'
           2678_1  COME_FROM          2660  '2660'

 L. 956      2678  LOAD_FAST                'word'
             2680  LOAD_METHOD              endswith
             2682  LOAD_STR                 'nacht'
             2684  CALL_METHOD_1         1  '1 positional argument'
         2686_2688  POP_JUMP_IF_FALSE  2716  'to 2716'

 L. 957      2690  LOAD_DEREF               'hrAbs'
             2692  LOAD_CONST               None
             2694  COMPARE_OP               is
         2696_2698  POP_JUMP_IF_FALSE  2704  'to 2704'

 L. 958      2700  LOAD_CONST               0
             2702  STORE_DEREF              'hrAbs'
           2704_0  COME_FROM          2696  '2696'

 L. 959      2704  LOAD_FAST                'used'
             2706  LOAD_CONST               1
             2708  INPLACE_ADD      
             2710  STORE_FAST               'used'
         2712_2714  JUMP_FORWARD       5430  'to 5430'
           2716_0  COME_FROM          2686  '2686'

 L. 960      2716  LOAD_FAST                'word'
             2718  LOAD_METHOD              endswith
             2720  LOAD_STR                 'ochtend'
             2722  CALL_METHOD_1         1  '1 positional argument'
         2724_2726  POP_JUMP_IF_FALSE  2754  'to 2754'

 L. 961      2728  LOAD_DEREF               'hrAbs'
             2730  LOAD_CONST               None
             2732  COMPARE_OP               is
         2734_2736  POP_JUMP_IF_FALSE  2742  'to 2742'

 L. 962      2738  LOAD_CONST               8
             2740  STORE_DEREF              'hrAbs'
           2742_0  COME_FROM          2734  '2734'

 L. 963      2742  LOAD_FAST                'used'
             2744  LOAD_CONST               1
             2746  INPLACE_ADD      
             2748  STORE_FAST               'used'
         2750_2752  JUMP_FORWARD       5430  'to 5430'
           2754_0  COME_FROM          2724  '2724'

 L. 964      2754  LOAD_FAST                'word'
             2756  LOAD_METHOD              endswith
             2758  LOAD_STR                 'middag'
             2760  CALL_METHOD_1         1  '1 positional argument'
         2762_2764  POP_JUMP_IF_FALSE  2792  'to 2792'

 L. 965      2766  LOAD_DEREF               'hrAbs'
             2768  LOAD_CONST               None
             2770  COMPARE_OP               is
         2772_2774  POP_JUMP_IF_FALSE  2780  'to 2780'

 L. 966      2776  LOAD_CONST               15
             2778  STORE_DEREF              'hrAbs'
           2780_0  COME_FROM          2772  '2772'

 L. 967      2780  LOAD_FAST                'used'
             2782  LOAD_CONST               1
             2784  INPLACE_ADD      
             2786  STORE_FAST               'used'
         2788_2790  JUMP_FORWARD       5430  'to 5430'
           2792_0  COME_FROM          2762  '2762'

 L. 968      2792  LOAD_FAST                'word'
             2794  LOAD_METHOD              endswith
             2796  LOAD_STR                 'avond'
             2798  CALL_METHOD_1         1  '1 positional argument'
         2800_2802  POP_JUMP_IF_FALSE  2830  'to 2830'

 L. 969      2804  LOAD_DEREF               'hrAbs'
             2806  LOAD_CONST               None
             2808  COMPARE_OP               is
         2810_2812  POP_JUMP_IF_FALSE  2818  'to 2818'

 L. 970      2814  LOAD_CONST               19
             2816  STORE_DEREF              'hrAbs'
           2818_0  COME_FROM          2810  '2810'

 L. 971      2818  LOAD_FAST                'used'
             2820  LOAD_CONST               1
             2822  INPLACE_ADD      
             2824  STORE_FAST               'used'
         2826_2828  JUMP_FORWARD       5430  'to 5430'
           2830_0  COME_FROM          2800  '2800'

 L. 974      2830  LOAD_FAST                'word'
             2832  LOAD_STR                 '2'
             2834  COMPARE_OP               ==
         2836_2838  POP_JUMP_IF_FALSE  2908  'to 2908'

 L. 975      2840  LOAD_FAST                'wordNextNext'
             2842  LOAD_CONST               ('uur', 'minuten', 'seconden')
             2844  COMPARE_OP               in
         2846_2848  POP_JUMP_IF_FALSE  2908  'to 2908'

 L. 976      2850  LOAD_FAST                'used'
             2852  LOAD_CONST               2
             2854  INPLACE_ADD      
             2856  STORE_FAST               'used'

 L. 977      2858  LOAD_FAST                'wordNextNext'
             2860  LOAD_STR                 'uur'
             2862  COMPARE_OP               ==
         2864_2866  POP_JUMP_IF_FALSE  2874  'to 2874'

 L. 978      2868  LOAD_CONST               2
             2870  STORE_DEREF              'hrOffset'
             2872  JUMP_FORWARD       5430  'to 5430'
           2874_0  COME_FROM          2864  '2864'

 L. 979      2874  LOAD_FAST                'wordNextNext'
             2876  LOAD_STR                 'minuten'
             2878  COMPARE_OP               ==
         2880_2882  POP_JUMP_IF_FALSE  2890  'to 2890'

 L. 980      2884  LOAD_CONST               2
             2886  STORE_DEREF              'minOffset'
             2888  JUMP_FORWARD       5430  'to 5430'
           2890_0  COME_FROM          2880  '2880'

 L. 981      2890  LOAD_FAST                'wordNextNext'
             2892  LOAD_STR                 'seconden'
             2894  COMPARE_OP               ==
         2896_2898  POP_JUMP_IF_FALSE  5430  'to 5430'

 L. 982      2900  LOAD_CONST               2
             2902  STORE_DEREF              'secOffset'
         2904_2906  JUMP_FORWARD       5430  'to 5430'
           2908_0  COME_FROM          2846  '2846'
           2908_1  COME_FROM          2836  '2836'

 L. 984      2908  LOAD_FAST                'word'
             2910  LOAD_STR                 'uur'
             2912  COMPARE_OP               ==
         2914_2916  POP_JUMP_IF_FALSE  3148  'to 3148'

 L. 985      2918  LOAD_FAST                'wordPrev'
             2920  LOAD_FAST                'markers'
             2922  COMPARE_OP               in
         2924_2926  POP_JUMP_IF_TRUE   2938  'to 2938'
             2928  LOAD_FAST                'wordPrevPrev'
             2930  LOAD_FAST                'markers'
             2932  COMPARE_OP               in
         2934_2936  POP_JUMP_IF_FALSE  3148  'to 3148'
           2938_0  COME_FROM          2924  '2924'

 L. 986      2938  LOAD_FAST                'wordPrev'
             2940  LOAD_STR                 'half'
             2942  COMPARE_OP               ==
         2944_2946  POP_JUMP_IF_FALSE  2954  'to 2954'

 L. 987      2948  LOAD_CONST               30
             2950  STORE_DEREF              'minOffset'
             2952  JUMP_FORWARD       3080  'to 3080'
           2954_0  COME_FROM          2944  '2944'

 L. 988      2954  LOAD_FAST                'wordPrev'
             2956  LOAD_STR                 'kwartier'
             2958  COMPARE_OP               ==
         2960_2962  POP_JUMP_IF_FALSE  2970  'to 2970'

 L. 989      2964  LOAD_CONST               15
             2966  STORE_DEREF              'minOffset'
             2968  JUMP_FORWARD       3080  'to 3080'
           2970_0  COME_FROM          2960  '2960'

 L. 990      2970  LOAD_FAST                'wordPrevPrev'
             2972  LOAD_STR                 'kwartier'
             2974  COMPARE_OP               ==
         2976_2978  POP_JUMP_IF_FALSE  3060  'to 3060'

 L. 991      2980  LOAD_CONST               15
             2982  STORE_DEREF              'minOffset'

 L. 992      2984  LOAD_FAST                'idx'
             2986  LOAD_CONST               2
             2988  COMPARE_OP               >
         2990_2992  POP_JUMP_IF_FALSE  3046  'to 3046'
             2994  LOAD_FAST                'words'
             2996  LOAD_FAST                'idx'
             2998  LOAD_CONST               3
             3000  BINARY_SUBTRACT  
             3002  BINARY_SUBSCR    
             3004  LOAD_FAST                'markers'
             3006  COMPARE_OP               in
         3008_3010  POP_JUMP_IF_FALSE  3046  'to 3046'

 L. 993      3012  LOAD_STR                 ''
             3014  LOAD_FAST                'words'
             3016  LOAD_FAST                'idx'
             3018  LOAD_CONST               3
             3020  BINARY_SUBTRACT  
             3022  STORE_SUBSCR     

 L. 994      3024  LOAD_FAST                'words'
             3026  LOAD_FAST                'idx'
             3028  LOAD_CONST               3
             3030  BINARY_SUBTRACT  
             3032  BINARY_SUBSCR    
             3034  LOAD_STR                 'deze'
             3036  COMPARE_OP               ==
         3038_3040  POP_JUMP_IF_FALSE  3046  'to 3046'

 L. 995      3042  LOAD_CONST               True
             3044  STORE_FAST               'daySpecified'
           3046_0  COME_FROM          3038  '3038'
           3046_1  COME_FROM          3008  '3008'
           3046_2  COME_FROM          2990  '2990'

 L. 996      3046  LOAD_STR                 ''
             3048  LOAD_FAST                'words'
             3050  LOAD_FAST                'idx'
             3052  LOAD_CONST               2
             3054  BINARY_SUBTRACT  
             3056  STORE_SUBSCR     
             3058  JUMP_FORWARD       3080  'to 3080'
           3060_0  COME_FROM          2976  '2976'

 L. 997      3060  LOAD_FAST                'wordPrev'
             3062  LOAD_STR                 'binnen'
             3064  COMPARE_OP               ==
         3066_3068  POP_JUMP_IF_FALSE  3076  'to 3076'

 L. 998      3070  LOAD_CONST               1
             3072  STORE_DEREF              'hrOffset'
             3074  JUMP_FORWARD       3080  'to 3080'
           3076_0  COME_FROM          3066  '3066'

 L.1000      3076  LOAD_CONST               1
             3078  STORE_DEREF              'hrOffset'
           3080_0  COME_FROM          3074  '3074'
           3080_1  COME_FROM          3058  '3058'
           3080_2  COME_FROM          2968  '2968'
           3080_3  COME_FROM          2952  '2952'

 L.1001      3080  LOAD_FAST                'wordPrevPrev'
             3082  LOAD_FAST                'markers'
             3084  COMPARE_OP               in
         3086_3088  POP_JUMP_IF_FALSE  3116  'to 3116'

 L.1002      3090  LOAD_STR                 ''
             3092  LOAD_FAST                'words'
             3094  LOAD_FAST                'idx'
             3096  LOAD_CONST               2
             3098  BINARY_SUBTRACT  
             3100  STORE_SUBSCR     

 L.1003      3102  LOAD_FAST                'wordPrevPrev'
             3104  LOAD_STR                 'deze'
             3106  COMPARE_OP               ==
         3108_3110  POP_JUMP_IF_FALSE  3116  'to 3116'

 L.1004      3112  LOAD_CONST               True
             3114  STORE_FAST               'daySpecified'
           3116_0  COME_FROM          3108  '3108'
           3116_1  COME_FROM          3086  '3086'

 L.1005      3116  LOAD_STR                 ''
             3118  LOAD_FAST                'words'
             3120  LOAD_FAST                'idx'
             3122  LOAD_CONST               1
             3124  BINARY_SUBTRACT  
             3126  STORE_SUBSCR     

 L.1006      3128  LOAD_FAST                'used'
             3130  LOAD_CONST               1
             3132  INPLACE_ADD      
             3134  STORE_FAST               'used'

 L.1007      3136  LOAD_CONST               -1
             3138  STORE_DEREF              'hrAbs'

 L.1008      3140  LOAD_CONST               -1
             3142  STORE_DEREF              'minAbs'
         3144_3146  JUMP_FORWARD       5430  'to 5430'
           3148_0  COME_FROM          2934  '2934'
           3148_1  COME_FROM          2914  '2914'

 L.1011      3148  LOAD_FAST                'word'
             3150  LOAD_STR                 'minuut'
             3152  COMPARE_OP               ==
         3154_3156  POP_JUMP_IF_FALSE  3196  'to 3196'
             3158  LOAD_FAST                'wordPrev'
             3160  LOAD_STR                 'over'
             3162  COMPARE_OP               ==
         3164_3166  POP_JUMP_IF_FALSE  3196  'to 3196'

 L.1012      3168  LOAD_CONST               1
             3170  STORE_DEREF              'minOffset'

 L.1013      3172  LOAD_STR                 ''
             3174  LOAD_FAST                'words'
             3176  LOAD_FAST                'idx'
             3178  LOAD_CONST               1
             3180  BINARY_SUBTRACT  
             3182  STORE_SUBSCR     

 L.1014      3184  LOAD_FAST                'used'
             3186  LOAD_CONST               1
             3188  INPLACE_ADD      
             3190  STORE_FAST               'used'
         3192_3194  JUMP_FORWARD       5430  'to 5430'
           3196_0  COME_FROM          3164  '3164'
           3196_1  COME_FROM          3154  '3154'

 L.1016      3196  LOAD_FAST                'word'
             3198  LOAD_STR                 'seconde'
             3200  COMPARE_OP               ==
         3202_3204  POP_JUMP_IF_FALSE  3244  'to 3244'
             3206  LOAD_FAST                'wordPrev'
             3208  LOAD_STR                 'over'
             3210  COMPARE_OP               ==
         3212_3214  POP_JUMP_IF_FALSE  3244  'to 3244'

 L.1017      3216  LOAD_CONST               1
             3218  STORE_DEREF              'secOffset'

 L.1018      3220  LOAD_STR                 ''
             3222  LOAD_FAST                'words'
             3224  LOAD_FAST                'idx'
             3226  LOAD_CONST               1
             3228  BINARY_SUBTRACT  
             3230  STORE_SUBSCR     

 L.1019      3232  LOAD_FAST                'used'
             3234  LOAD_CONST               1
             3236  INPLACE_ADD      
             3238  STORE_FAST               'used'
         3240_3242  JUMP_FORWARD       5430  'to 5430'
           3244_0  COME_FROM          3212  '3212'
           3244_1  COME_FROM          3202  '3202'

 L.1020      3244  LOAD_FAST                'word'
             3246  LOAD_CONST               0
             3248  BINARY_SUBSCR    
             3250  LOAD_METHOD              isdigit
             3252  CALL_METHOD_0         0  '0 positional arguments'
         3254_3256  POP_JUMP_IF_FALSE  5430  'to 5430'

 L.1021      3258  LOAD_CONST               True
             3260  STORE_FAST               'isTime'

 L.1022      3262  LOAD_STR                 ''
             3264  STORE_FAST               'strHH'

 L.1023      3266  LOAD_STR                 ''
             3268  STORE_FAST               'strMM'

 L.1024      3270  LOAD_STR                 ''
             3272  STORE_FAST               'remainder'

 L.1026      3274  LOAD_FAST                'idx'
             3276  LOAD_CONST               3
             3278  BINARY_ADD       
             3280  LOAD_GLOBAL              len
             3282  LOAD_FAST                'words'
             3284  CALL_FUNCTION_1       1  '1 positional argument'
             3286  COMPARE_OP               <
         3288_3290  POP_JUMP_IF_FALSE  3304  'to 3304'
             3292  LOAD_FAST                'words'
             3294  LOAD_FAST                'idx'
             3296  LOAD_CONST               3
             3298  BINARY_ADD       
             3300  BINARY_SUBSCR    
             3302  JUMP_FORWARD       3306  'to 3306'
           3304_0  COME_FROM          3288  '3288'
             3304  LOAD_STR                 ''
           3306_0  COME_FROM          3302  '3302'
             3306  STORE_FAST               'wordNextNextNext'

 L.1027      3308  LOAD_FAST                'wordNext'
             3310  LOAD_STR                 'vannacht'
             3312  COMPARE_OP               ==
         3314_3316  POP_JUMP_IF_TRUE   3358  'to 3358'
             3318  LOAD_FAST                'wordNextNext'
             3320  LOAD_STR                 'vannacht'
             3322  COMPARE_OP               ==
         3324_3326  POP_JUMP_IF_TRUE   3358  'to 3358'

 L.1028      3328  LOAD_FAST                'wordPrev'
             3330  LOAD_STR                 'vannacht'
             3332  COMPARE_OP               ==
         3334_3336  POP_JUMP_IF_TRUE   3358  'to 3358'
             3338  LOAD_FAST                'wordPrevPrev'
             3340  LOAD_STR                 'vannacht'
             3342  COMPARE_OP               ==
         3344_3346  POP_JUMP_IF_TRUE   3358  'to 3358'

 L.1029      3348  LOAD_FAST                'wordNextNextNext'
             3350  LOAD_STR                 'vannacht'
             3352  COMPARE_OP               ==
         3354_3356  POP_JUMP_IF_FALSE  3450  'to 3450'
           3358_0  COME_FROM          3344  '3344'
           3358_1  COME_FROM          3334  '3334'
           3358_2  COME_FROM          3324  '3324'
           3358_3  COME_FROM          3314  '3314'

 L.1030      3358  LOAD_STR                 'pm'
             3360  STORE_FAST               'remainder'

 L.1031      3362  LOAD_FAST                'used'
             3364  LOAD_CONST               1
             3366  INPLACE_ADD      
             3368  STORE_FAST               'used'

 L.1032      3370  LOAD_FAST                'wordPrev'
             3372  LOAD_STR                 'vannacht'
             3374  COMPARE_OP               ==
         3376_3378  POP_JUMP_IF_FALSE  3392  'to 3392'

 L.1033      3380  LOAD_STR                 ''
             3382  LOAD_FAST                'words'
             3384  LOAD_FAST                'idx'
             3386  LOAD_CONST               1
             3388  BINARY_SUBTRACT  
             3390  STORE_SUBSCR     
           3392_0  COME_FROM          3376  '3376'

 L.1034      3392  LOAD_FAST                'wordPrevPrev'
             3394  LOAD_STR                 'vannacht'
             3396  COMPARE_OP               ==
         3398_3400  POP_JUMP_IF_FALSE  3414  'to 3414'

 L.1035      3402  LOAD_STR                 ''
             3404  LOAD_FAST                'words'
             3406  LOAD_FAST                'idx'
             3408  LOAD_CONST               2
             3410  BINARY_SUBTRACT  
             3412  STORE_SUBSCR     
           3414_0  COME_FROM          3398  '3398'

 L.1036      3414  LOAD_FAST                'wordNextNext'
             3416  LOAD_STR                 'vannacht'
             3418  COMPARE_OP               ==
         3420_3422  POP_JUMP_IF_FALSE  3432  'to 3432'

 L.1037      3424  LOAD_FAST                'used'
             3426  LOAD_CONST               1
             3428  INPLACE_ADD      
             3430  STORE_FAST               'used'
           3432_0  COME_FROM          3420  '3420'

 L.1038      3432  LOAD_FAST                'wordNextNextNext'
             3434  LOAD_STR                 'vannacht'
             3436  COMPARE_OP               ==
         3438_3440  POP_JUMP_IF_FALSE  3450  'to 3450'

 L.1039      3442  LOAD_FAST                'used'
             3444  LOAD_CONST               1
             3446  INPLACE_ADD      
             3448  STORE_FAST               'used'
           3450_0  COME_FROM          3438  '3438'
           3450_1  COME_FROM          3354  '3354'

 L.1041      3450  LOAD_STR                 ':'
             3452  LOAD_FAST                'word'
             3454  COMPARE_OP               in
         3456_3458  POP_JUMP_IF_FALSE  4150  'to 4150'

 L.1044      3460  LOAD_CONST               0
             3462  STORE_FAST               'stage'

 L.1045      3464  LOAD_GLOBAL              len
             3466  LOAD_FAST                'word'
             3468  CALL_FUNCTION_1       1  '1 positional argument'
             3470  STORE_FAST               'length'

 L.1046      3472  SETUP_LOOP         3648  'to 3648'
             3474  LOAD_GLOBAL              range
             3476  LOAD_FAST                'length'
             3478  CALL_FUNCTION_1       1  '1 positional argument'
             3480  GET_ITER         
           3482_0  COME_FROM          3616  '3616'
             3482  FOR_ITER           3646  'to 3646'
             3484  STORE_FAST               'i'

 L.1047      3486  LOAD_FAST                'stage'
             3488  LOAD_CONST               0
             3490  COMPARE_OP               ==
         3492_3494  POP_JUMP_IF_FALSE  3558  'to 3558'

 L.1048      3496  LOAD_FAST                'word'
             3498  LOAD_FAST                'i'
             3500  BINARY_SUBSCR    
             3502  LOAD_METHOD              isdigit
             3504  CALL_METHOD_0         0  '0 positional arguments'
         3506_3508  POP_JUMP_IF_FALSE  3524  'to 3524'

 L.1049      3510  LOAD_FAST                'strHH'
             3512  LOAD_FAST                'word'
             3514  LOAD_FAST                'i'
             3516  BINARY_SUBSCR    
             3518  INPLACE_ADD      
             3520  STORE_FAST               'strHH'
             3522  JUMP_FORWARD       3556  'to 3556'
           3524_0  COME_FROM          3506  '3506'

 L.1050      3524  LOAD_FAST                'word'
             3526  LOAD_FAST                'i'
             3528  BINARY_SUBSCR    
             3530  LOAD_STR                 ':'
             3532  COMPARE_OP               ==
         3534_3536  POP_JUMP_IF_FALSE  3544  'to 3544'

 L.1051      3538  LOAD_CONST               1
             3540  STORE_FAST               'stage'
             3542  JUMP_FORWARD       3556  'to 3556'
           3544_0  COME_FROM          3534  '3534'

 L.1053      3544  LOAD_CONST               2
             3546  STORE_FAST               'stage'

 L.1054      3548  LOAD_FAST                'i'
             3550  LOAD_CONST               1
             3552  INPLACE_SUBTRACT 
             3554  STORE_FAST               'i'
           3556_0  COME_FROM          3542  '3542'
           3556_1  COME_FROM          3522  '3522'
             3556  JUMP_BACK          3482  'to 3482'
           3558_0  COME_FROM          3492  '3492'

 L.1055      3558  LOAD_FAST                'stage'
             3560  LOAD_CONST               1
             3562  COMPARE_OP               ==
         3564_3566  POP_JUMP_IF_FALSE  3610  'to 3610'

 L.1056      3568  LOAD_FAST                'word'
             3570  LOAD_FAST                'i'
             3572  BINARY_SUBSCR    
             3574  LOAD_METHOD              isdigit
             3576  CALL_METHOD_0         0  '0 positional arguments'
         3578_3580  POP_JUMP_IF_FALSE  3596  'to 3596'

 L.1057      3582  LOAD_FAST                'strMM'
             3584  LOAD_FAST                'word'
             3586  LOAD_FAST                'i'
             3588  BINARY_SUBSCR    
             3590  INPLACE_ADD      
             3592  STORE_FAST               'strMM'
             3594  JUMP_FORWARD       3608  'to 3608'
           3596_0  COME_FROM          3578  '3578'

 L.1059      3596  LOAD_CONST               2
             3598  STORE_FAST               'stage'

 L.1060      3600  LOAD_FAST                'i'
             3602  LOAD_CONST               1
             3604  INPLACE_SUBTRACT 
             3606  STORE_FAST               'i'
           3608_0  COME_FROM          3594  '3594'
             3608  JUMP_BACK          3482  'to 3482'
           3610_0  COME_FROM          3564  '3564'

 L.1061      3610  LOAD_FAST                'stage'
             3612  LOAD_CONST               2
             3614  COMPARE_OP               ==
         3616_3618  POP_JUMP_IF_FALSE  3482  'to 3482'

 L.1062      3620  LOAD_FAST                'word'
             3622  LOAD_FAST                'i'
             3624  LOAD_CONST               None
             3626  BUILD_SLICE_2         2 
             3628  BINARY_SUBSCR    
             3630  LOAD_METHOD              replace
             3632  LOAD_STR                 '.'
             3634  LOAD_STR                 ''
             3636  CALL_METHOD_2         2  '2 positional arguments'
             3638  STORE_FAST               'remainder'

 L.1063      3640  BREAK_LOOP       
         3642_3644  JUMP_BACK          3482  'to 3482'
             3646  POP_BLOCK        
           3648_0  COME_FROM_LOOP     3472  '3472'

 L.1064      3648  LOAD_FAST                'remainder'
             3650  LOAD_STR                 ''
             3652  COMPARE_OP               ==
         3654_3656  POP_JUMP_IF_FALSE  5148  'to 5148'

 L.1065      3658  LOAD_FAST                'wordNext'
             3660  LOAD_METHOD              replace
             3662  LOAD_STR                 '.'
             3664  LOAD_STR                 ''
             3666  CALL_METHOD_2         2  '2 positional arguments'
             3668  STORE_FAST               'nextWord'

 L.1066      3670  LOAD_FAST                'nextWord'
             3672  LOAD_STR                 'am'
             3674  COMPARE_OP               ==
         3676_3678  POP_JUMP_IF_TRUE   3690  'to 3690'
             3680  LOAD_FAST                'nextWord'
             3682  LOAD_STR                 'pm'
             3684  COMPARE_OP               ==
         3686_3688  POP_JUMP_IF_FALSE  3706  'to 3706'
           3690_0  COME_FROM          3676  '3676'

 L.1067      3690  LOAD_FAST                'nextWord'
             3692  STORE_FAST               'remainder'

 L.1068      3694  LOAD_FAST                'used'
             3696  LOAD_CONST               1
             3698  INPLACE_ADD      
             3700  STORE_FAST               'used'
         3702_3704  JUMP_ABSOLUTE      5148  'to 5148'
           3706_0  COME_FROM          3686  '3686'

 L.1070      3706  LOAD_FAST                'wordNext'
             3708  LOAD_STR                 'in'
             3710  COMPARE_OP               ==
         3712_3714  POP_JUMP_IF_FALSE  3742  'to 3742'
             3716  LOAD_FAST                'wordNextNext'
             3718  LOAD_STR                 'ochtend'
             3720  COMPARE_OP               ==
         3722_3724  POP_JUMP_IF_FALSE  3742  'to 3742'

 L.1071      3726  LOAD_STR                 'am'
             3728  STORE_FAST               'remainder'

 L.1072      3730  LOAD_FAST                'used'
             3732  LOAD_CONST               2
             3734  INPLACE_ADD      
             3736  STORE_FAST               'used'
         3738_3740  JUMP_ABSOLUTE      5148  'to 5148'
           3742_0  COME_FROM          3722  '3722'
           3742_1  COME_FROM          3712  '3712'

 L.1073      3742  LOAD_FAST                'wordNext'
             3744  LOAD_STR                 'in'
             3746  COMPARE_OP               ==
         3748_3750  POP_JUMP_IF_FALSE  3778  'to 3778'
             3752  LOAD_FAST                'wordNextNext'
             3754  LOAD_STR                 'middag'
             3756  COMPARE_OP               ==
         3758_3760  POP_JUMP_IF_FALSE  3778  'to 3778'

 L.1074      3762  LOAD_STR                 'pm'
             3764  STORE_FAST               'remainder'

 L.1075      3766  LOAD_FAST                'used'
             3768  LOAD_CONST               2
             3770  INPLACE_ADD      
             3772  STORE_FAST               'used'
         3774_3776  JUMP_ABSOLUTE      5148  'to 5148'
           3778_0  COME_FROM          3758  '3758'
           3778_1  COME_FROM          3748  '3748'

 L.1076      3778  LOAD_FAST                'wordNext'
             3780  LOAD_STR                 'in'
             3782  COMPARE_OP               ==
         3784_3786  POP_JUMP_IF_FALSE  3814  'to 3814'
             3788  LOAD_FAST                'wordNextNext'
             3790  LOAD_STR                 'avond'
             3792  COMPARE_OP               ==
         3794_3796  POP_JUMP_IF_FALSE  3814  'to 3814'

 L.1077      3798  LOAD_STR                 'pm'
             3800  STORE_FAST               'remainder'

 L.1078      3802  LOAD_FAST                'used'
             3804  LOAD_CONST               2
             3806  INPLACE_ADD      
             3808  STORE_FAST               'used'
         3810_3812  JUMP_ABSOLUTE      5148  'to 5148'
           3814_0  COME_FROM          3794  '3794'
           3814_1  COME_FROM          3784  '3784'

 L.1079      3814  LOAD_FAST                'wordNext'
             3816  LOAD_STR                 "'s"
             3818  COMPARE_OP               ==
         3820_3822  POP_JUMP_IF_FALSE  3850  'to 3850'
             3824  LOAD_FAST                'wordNextNext'
             3826  LOAD_STR                 'ochtends'
             3828  COMPARE_OP               ==
         3830_3832  POP_JUMP_IF_FALSE  3850  'to 3850'

 L.1080      3834  LOAD_STR                 'am'
             3836  STORE_FAST               'remainder'

 L.1081      3838  LOAD_FAST                'used'
             3840  LOAD_CONST               2
             3842  INPLACE_ADD      
             3844  STORE_FAST               'used'
         3846_3848  JUMP_ABSOLUTE      5148  'to 5148'
           3850_0  COME_FROM          3830  '3830'
           3850_1  COME_FROM          3820  '3820'

 L.1082      3850  LOAD_FAST                'wordNext'
             3852  LOAD_STR                 "'s"
             3854  COMPARE_OP               ==
         3856_3858  POP_JUMP_IF_FALSE  3886  'to 3886'
             3860  LOAD_FAST                'wordNextNext'
             3862  LOAD_STR                 'middags'
             3864  COMPARE_OP               ==
         3866_3868  POP_JUMP_IF_FALSE  3886  'to 3886'

 L.1083      3870  LOAD_STR                 'pm'
             3872  STORE_FAST               'remainder'

 L.1084      3874  LOAD_FAST                'used'
             3876  LOAD_CONST               2
             3878  INPLACE_ADD      
             3880  STORE_FAST               'used'
         3882_3884  JUMP_ABSOLUTE      5148  'to 5148'
           3886_0  COME_FROM          3866  '3866'
           3886_1  COME_FROM          3856  '3856'

 L.1085      3886  LOAD_FAST                'wordNext'
             3888  LOAD_STR                 "'s"
             3890  COMPARE_OP               ==
         3892_3894  POP_JUMP_IF_FALSE  3920  'to 3920'
             3896  LOAD_FAST                'wordNextNext'
             3898  LOAD_STR                 'avonds'
             3900  COMPARE_OP               ==
         3902_3904  POP_JUMP_IF_FALSE  3920  'to 3920'

 L.1086      3906  LOAD_STR                 'pm'
             3908  STORE_FAST               'remainder'

 L.1087      3910  LOAD_FAST                'used'
             3912  LOAD_CONST               2
             3914  INPLACE_ADD      
             3916  STORE_FAST               'used'
             3918  JUMP_FORWARD       5148  'to 5148'
           3920_0  COME_FROM          3902  '3902'
           3920_1  COME_FROM          3892  '3892'

 L.1088      3920  LOAD_FAST                'wordNext'
             3922  LOAD_STR                 'deze'
             3924  COMPARE_OP               ==
         3926_3928  POP_JUMP_IF_FALSE  3954  'to 3954'
             3930  LOAD_FAST                'wordNextNext'
             3932  LOAD_STR                 'ochtend'
             3934  COMPARE_OP               ==
         3936_3938  POP_JUMP_IF_FALSE  3954  'to 3954'

 L.1089      3940  LOAD_STR                 'am'
             3942  STORE_FAST               'remainder'

 L.1090      3944  LOAD_CONST               2
             3946  STORE_FAST               'used'

 L.1091      3948  LOAD_CONST               True
             3950  STORE_FAST               'daySpecified'
             3952  JUMP_FORWARD       5148  'to 5148'
           3954_0  COME_FROM          3936  '3936'
           3954_1  COME_FROM          3926  '3926'

 L.1092      3954  LOAD_FAST                'wordNext'
             3956  LOAD_STR                 'deze'
             3958  COMPARE_OP               ==
         3960_3962  POP_JUMP_IF_FALSE  3988  'to 3988'
             3964  LOAD_FAST                'wordNextNext'
             3966  LOAD_STR                 'middag'
             3968  COMPARE_OP               ==
         3970_3972  POP_JUMP_IF_FALSE  3988  'to 3988'

 L.1093      3974  LOAD_STR                 'pm'
             3976  STORE_FAST               'remainder'

 L.1094      3978  LOAD_CONST               2
             3980  STORE_FAST               'used'

 L.1095      3982  LOAD_CONST               True
             3984  STORE_FAST               'daySpecified'
             3986  JUMP_FORWARD       5148  'to 5148'
           3988_0  COME_FROM          3970  '3970'
           3988_1  COME_FROM          3960  '3960'

 L.1096      3988  LOAD_FAST                'wordNext'
             3990  LOAD_STR                 'deze'
             3992  COMPARE_OP               ==
         3994_3996  POP_JUMP_IF_FALSE  4022  'to 4022'
             3998  LOAD_FAST                'wordNextNext'
             4000  LOAD_STR                 'avond'
             4002  COMPARE_OP               ==
         4004_4006  POP_JUMP_IF_FALSE  4022  'to 4022'

 L.1097      4008  LOAD_STR                 'pm'
             4010  STORE_FAST               'remainder'

 L.1098      4012  LOAD_CONST               2
             4014  STORE_FAST               'used'

 L.1099      4016  LOAD_CONST               True
             4018  STORE_FAST               'daySpecified'
             4020  JUMP_FORWARD       5148  'to 5148'
           4022_0  COME_FROM          4004  '4004'
           4022_1  COME_FROM          3994  '3994'

 L.1100      4022  LOAD_FAST                'wordNext'
             4024  LOAD_STR                 "'s"
             4026  COMPARE_OP               ==
         4028_4030  POP_JUMP_IF_FALSE  4082  'to 4082'
             4032  LOAD_FAST                'wordNextNext'
             4034  LOAD_STR                 'nachts'
             4036  COMPARE_OP               ==
         4038_4040  POP_JUMP_IF_FALSE  4082  'to 4082'

 L.1101      4042  LOAD_FAST                'strHH'
         4044_4046  POP_JUMP_IF_FALSE  4068  'to 4068'
             4048  LOAD_GLOBAL              int
             4050  LOAD_FAST                'strHH'
             4052  CALL_FUNCTION_1       1  '1 positional argument'
             4054  LOAD_CONST               5
             4056  COMPARE_OP               >
         4058_4060  POP_JUMP_IF_FALSE  4068  'to 4068'

 L.1102      4062  LOAD_STR                 'pm'
             4064  STORE_FAST               'remainder'
             4066  JUMP_FORWARD       4072  'to 4072'
           4068_0  COME_FROM          4058  '4058'
           4068_1  COME_FROM          4044  '4044'

 L.1104      4068  LOAD_STR                 'am'
             4070  STORE_FAST               'remainder'
           4072_0  COME_FROM          4066  '4066'

 L.1105      4072  LOAD_FAST                'used'
             4074  LOAD_CONST               2
             4076  INPLACE_ADD      
             4078  STORE_FAST               'used'
             4080  JUMP_FORWARD       5148  'to 5148'
           4082_0  COME_FROM          4038  '4038'
           4082_1  COME_FROM          4028  '4028'

 L.1108      4082  LOAD_FAST                'timeQualifier'
             4084  LOAD_STR                 ''
             4086  COMPARE_OP               !=
         4088_4090  POP_JUMP_IF_FALSE  5148  'to 5148'

 L.1109      4092  LOAD_CONST               True
             4094  STORE_FAST               'military'

 L.1110      4096  LOAD_FAST                'strHH'
         4098_4100  POP_JUMP_IF_FALSE  5148  'to 5148'
             4102  LOAD_GLOBAL              int
             4104  LOAD_FAST                'strHH'
             4106  CALL_FUNCTION_1       1  '1 positional argument'
             4108  LOAD_CONST               12
             4110  COMPARE_OP               <=
         4112_4114  POP_JUMP_IF_FALSE  5148  'to 5148'

 L.1111      4116  LOAD_FAST                'timeQualifier'
             4118  LOAD_FAST                'timeQualifiersPM'
             4120  COMPARE_OP               in
         4122_4124  POP_JUMP_IF_FALSE  5148  'to 5148'

 L.1112      4126  LOAD_FAST                'strHH'
             4128  LOAD_GLOBAL              str
             4130  LOAD_GLOBAL              int
             4132  LOAD_FAST                'strHH'
             4134  CALL_FUNCTION_1       1  '1 positional argument'
             4136  LOAD_CONST               12
             4138  BINARY_ADD       
             4140  CALL_FUNCTION_1       1  '1 positional argument'
             4142  INPLACE_ADD      
             4144  STORE_FAST               'strHH'
         4146_4148  JUMP_FORWARD       5148  'to 5148'
           4150_0  COME_FROM          3456  '3456'

 L.1117      4150  LOAD_GLOBAL              len
             4152  LOAD_FAST                'word'
             4154  CALL_FUNCTION_1       1  '1 positional argument'
             4156  STORE_FAST               'length'

 L.1118      4158  LOAD_STR                 ''
             4160  STORE_FAST               'strNum'

 L.1119      4162  LOAD_STR                 ''
             4164  STORE_FAST               'remainder'

 L.1120      4166  SETUP_LOOP         4226  'to 4226'
             4168  LOAD_GLOBAL              range
             4170  LOAD_FAST                'length'
             4172  CALL_FUNCTION_1       1  '1 positional argument'
             4174  GET_ITER         
             4176  FOR_ITER           4224  'to 4224'
             4178  STORE_FAST               'i'

 L.1121      4180  LOAD_FAST                'word'
             4182  LOAD_FAST                'i'
             4184  BINARY_SUBSCR    
             4186  LOAD_METHOD              isdigit
             4188  CALL_METHOD_0         0  '0 positional arguments'
         4190_4192  POP_JUMP_IF_FALSE  4208  'to 4208'

 L.1122      4194  LOAD_FAST                'strNum'
             4196  LOAD_FAST                'word'
             4198  LOAD_FAST                'i'
             4200  BINARY_SUBSCR    
             4202  INPLACE_ADD      
             4204  STORE_FAST               'strNum'
             4206  JUMP_BACK          4176  'to 4176'
           4208_0  COME_FROM          4190  '4190'

 L.1124      4208  LOAD_FAST                'remainder'
             4210  LOAD_FAST                'word'
             4212  LOAD_FAST                'i'
             4214  BINARY_SUBSCR    
             4216  INPLACE_ADD      
             4218  STORE_FAST               'remainder'
         4220_4222  JUMP_BACK          4176  'to 4176'
             4224  POP_BLOCK        
           4226_0  COME_FROM_LOOP     4166  '4166'

 L.1126      4226  LOAD_FAST                'remainder'
             4228  LOAD_STR                 ''
             4230  COMPARE_OP               ==
         4232_4234  POP_JUMP_IF_FALSE  4256  'to 4256'

 L.1127      4236  LOAD_FAST                'wordNext'
             4238  LOAD_METHOD              replace
             4240  LOAD_STR                 '.'
             4242  LOAD_STR                 ''
             4244  CALL_METHOD_2         2  '2 positional arguments'
             4246  LOAD_METHOD              lstrip
             4248  CALL_METHOD_0         0  '0 positional arguments'
             4250  LOAD_METHOD              rstrip
             4252  CALL_METHOD_0         0  '0 positional arguments'
             4254  STORE_FAST               'remainder'
           4256_0  COME_FROM          4232  '4232'

 L.1129      4256  LOAD_FAST                'remainder'
             4258  LOAD_STR                 'pm'
             4260  COMPARE_OP               ==
         4262_4264  POP_JUMP_IF_TRUE   4296  'to 4296'

 L.1130      4266  LOAD_FAST                'wordNext'
             4268  LOAD_STR                 'pm'
             4270  COMPARE_OP               ==
         4272_4274  POP_JUMP_IF_TRUE   4296  'to 4296'

 L.1131      4276  LOAD_FAST                'remainder'
             4278  LOAD_STR                 'p.m.'
             4280  COMPARE_OP               ==
         4282_4284  POP_JUMP_IF_TRUE   4296  'to 4296'

 L.1132      4286  LOAD_FAST                'wordNext'
             4288  LOAD_STR                 'p.m.'
             4290  COMPARE_OP               ==
         4292_4294  POP_JUMP_IF_FALSE  4312  'to 4312'
           4296_0  COME_FROM          4282  '4282'
           4296_1  COME_FROM          4272  '4272'
           4296_2  COME_FROM          4262  '4262'

 L.1133      4296  LOAD_FAST                'strNum'
             4298  STORE_FAST               'strHH'

 L.1134      4300  LOAD_STR                 'pm'
             4302  STORE_FAST               'remainder'

 L.1135      4304  LOAD_CONST               1
             4306  STORE_FAST               'used'
         4308_4310  JUMP_FORWARD       5148  'to 5148'
           4312_0  COME_FROM          4292  '4292'

 L.1137      4312  LOAD_FAST                'remainder'
             4314  LOAD_STR                 'am'
             4316  COMPARE_OP               ==
         4318_4320  POP_JUMP_IF_TRUE   4352  'to 4352'

 L.1138      4322  LOAD_FAST                'wordNext'
             4324  LOAD_STR                 'am'
             4326  COMPARE_OP               ==
         4328_4330  POP_JUMP_IF_TRUE   4352  'to 4352'

 L.1139      4332  LOAD_FAST                'remainder'
             4334  LOAD_STR                 'a.m.'
             4336  COMPARE_OP               ==
         4338_4340  POP_JUMP_IF_TRUE   4352  'to 4352'

 L.1140      4342  LOAD_FAST                'wordNext'
             4344  LOAD_STR                 'a.m.'
             4346  COMPARE_OP               ==
         4348_4350  POP_JUMP_IF_FALSE  4368  'to 4368'
           4352_0  COME_FROM          4338  '4338'
           4352_1  COME_FROM          4328  '4328'
           4352_2  COME_FROM          4318  '4318'

 L.1141      4352  LOAD_FAST                'strNum'
             4354  STORE_FAST               'strHH'

 L.1142      4356  LOAD_STR                 'am'
             4358  STORE_FAST               'remainder'

 L.1143      4360  LOAD_CONST               1
             4362  STORE_FAST               'used'
         4364_4366  JUMP_FORWARD       5148  'to 5148'
           4368_0  COME_FROM          4348  '4348'

 L.1145      4368  LOAD_FAST                'remainder'
             4370  LOAD_FAST                'recur_markers'
             4372  COMPARE_OP               in
         4374_4376  POP_JUMP_IF_TRUE   4398  'to 4398'

 L.1146      4378  LOAD_FAST                'wordNext'
             4380  LOAD_FAST                'recur_markers'
             4382  COMPARE_OP               in
         4384_4386  POP_JUMP_IF_TRUE   4398  'to 4398'

 L.1147      4388  LOAD_FAST                'wordNextNext'
             4390  LOAD_FAST                'recur_markers'
             4392  COMPARE_OP               in
         4394_4396  POP_JUMP_IF_FALSE  4410  'to 4410'
           4398_0  COME_FROM          4384  '4384'
           4398_1  COME_FROM          4374  '4374'

 L.1151      4398  LOAD_FAST                'strNum'
             4400  STORE_FAST               'strHH'

 L.1152      4402  LOAD_CONST               1
             4404  STORE_FAST               'used'
         4406_4408  JUMP_FORWARD       5148  'to 5148'
           4410_0  COME_FROM          4394  '4394'

 L.1155      4410  LOAD_FAST                'wordNext'
             4412  LOAD_STR                 'uren'
             4414  COMPARE_OP               ==
         4416_4418  POP_JUMP_IF_TRUE   4450  'to 4450'
             4420  LOAD_FAST                'wordNext'
             4422  LOAD_STR                 'uur'
             4424  COMPARE_OP               ==
         4426_4428  POP_JUMP_IF_TRUE   4450  'to 4450'

 L.1156      4430  LOAD_FAST                'remainder'
             4432  LOAD_STR                 'uren'
             4434  COMPARE_OP               ==
         4436_4438  POP_JUMP_IF_TRUE   4450  'to 4450'
             4440  LOAD_FAST                'remainder'
             4442  LOAD_STR                 'uur'
             4444  COMPARE_OP               ==
         4446_4448  POP_JUMP_IF_FALSE  4520  'to 4520'
           4450_0  COME_FROM          4436  '4436'
           4450_1  COME_FROM          4426  '4426'
           4450_2  COME_FROM          4416  '4416'

 L.1157      4450  LOAD_FAST                'word'
             4452  LOAD_CONST               0
             4454  BINARY_SUBSCR    
             4456  LOAD_STR                 '0'
             4458  COMPARE_OP               !=
         4460_4462  POP_JUMP_IF_FALSE  4520  'to 4520'

 L.1159      4464  LOAD_GLOBAL              int
             4466  LOAD_FAST                'strNum'
             4468  CALL_FUNCTION_1       1  '1 positional argument'
             4470  LOAD_CONST               100
             4472  COMPARE_OP               <
         4474_4476  POP_JUMP_IF_TRUE   4492  'to 4492'

 L.1160      4478  LOAD_GLOBAL              int
             4480  LOAD_FAST                'strNum'
             4482  CALL_FUNCTION_1       1  '1 positional argument'
             4484  LOAD_CONST               2400
             4486  COMPARE_OP               >
         4488_4490  POP_JUMP_IF_FALSE  4520  'to 4520'
           4492_0  COME_FROM          4474  '4474'

 L.1164      4492  LOAD_GLOBAL              int
             4494  LOAD_FAST                'strNum'
             4496  CALL_FUNCTION_1       1  '1 positional argument'
             4498  STORE_DEREF              'hrOffset'

 L.1165      4500  LOAD_CONST               2
             4502  STORE_FAST               'used'

 L.1166      4504  LOAD_CONST               False
             4506  STORE_FAST               'isTime'

 L.1167      4508  LOAD_CONST               -1
             4510  STORE_DEREF              'hrAbs'

 L.1168      4512  LOAD_CONST               -1
             4514  STORE_DEREF              'minAbs'
         4516_4518  JUMP_FORWARD       5148  'to 5148'
           4520_0  COME_FROM          4488  '4488'
           4520_1  COME_FROM          4460  '4460'
           4520_2  COME_FROM          4446  '4446'

 L.1170      4520  LOAD_FAST                'wordNext'
             4522  LOAD_STR                 'minuten'
             4524  COMPARE_OP               ==
         4526_4528  POP_JUMP_IF_TRUE   4560  'to 4560'
             4530  LOAD_FAST                'wordNext'
             4532  LOAD_STR                 'minuut'
             4534  COMPARE_OP               ==
         4536_4538  POP_JUMP_IF_TRUE   4560  'to 4560'

 L.1171      4540  LOAD_FAST                'remainder'
             4542  LOAD_STR                 'minuten'
             4544  COMPARE_OP               ==
         4546_4548  POP_JUMP_IF_TRUE   4560  'to 4560'
             4550  LOAD_FAST                'remainder'
             4552  LOAD_STR                 'minuut'
             4554  COMPARE_OP               ==
         4556_4558  POP_JUMP_IF_FALSE  4588  'to 4588'
           4560_0  COME_FROM          4546  '4546'
           4560_1  COME_FROM          4536  '4536'
           4560_2  COME_FROM          4526  '4526'

 L.1173      4560  LOAD_GLOBAL              int
             4562  LOAD_FAST                'strNum'
             4564  CALL_FUNCTION_1       1  '1 positional argument'
             4566  STORE_DEREF              'minOffset'

 L.1174      4568  LOAD_CONST               2
             4570  STORE_FAST               'used'

 L.1175      4572  LOAD_CONST               False
             4574  STORE_FAST               'isTime'

 L.1176      4576  LOAD_CONST               -1
             4578  STORE_DEREF              'hrAbs'

 L.1177      4580  LOAD_CONST               -1
             4582  STORE_DEREF              'minAbs'
         4584_4586  JUMP_FORWARD       5148  'to 5148'
           4588_0  COME_FROM          4556  '4556'

 L.1178      4588  LOAD_FAST                'wordNext'
             4590  LOAD_STR                 'seconden'
             4592  COMPARE_OP               ==
         4594_4596  POP_JUMP_IF_TRUE   4628  'to 4628'
             4598  LOAD_FAST                'wordNext'
             4600  LOAD_STR                 'seconde'
             4602  COMPARE_OP               ==
         4604_4606  POP_JUMP_IF_TRUE   4628  'to 4628'

 L.1179      4608  LOAD_FAST                'remainder'
             4610  LOAD_STR                 'seconden'
             4612  COMPARE_OP               ==
         4614_4616  POP_JUMP_IF_TRUE   4628  'to 4628'

 L.1180      4618  LOAD_FAST                'remainder'
             4620  LOAD_STR                 'seconde'
             4622  COMPARE_OP               ==
         4624_4626  POP_JUMP_IF_FALSE  4656  'to 4656'
           4628_0  COME_FROM          4614  '4614'
           4628_1  COME_FROM          4604  '4604'
           4628_2  COME_FROM          4594  '4594'

 L.1182      4628  LOAD_GLOBAL              int
             4630  LOAD_FAST                'strNum'
             4632  CALL_FUNCTION_1       1  '1 positional argument'
             4634  STORE_DEREF              'secOffset'

 L.1183      4636  LOAD_CONST               2
             4638  STORE_FAST               'used'

 L.1184      4640  LOAD_CONST               False
             4642  STORE_FAST               'isTime'

 L.1185      4644  LOAD_CONST               -1
             4646  STORE_DEREF              'hrAbs'

 L.1186      4648  LOAD_CONST               -1
             4650  STORE_DEREF              'minAbs'
         4652_4654  JUMP_FORWARD       5148  'to 5148'
           4656_0  COME_FROM          4624  '4624'

 L.1187      4656  LOAD_GLOBAL              int
             4658  LOAD_FAST                'strNum'
             4660  CALL_FUNCTION_1       1  '1 positional argument'
             4662  LOAD_CONST               100
             4664  COMPARE_OP               >
         4666_4668  POP_JUMP_IF_FALSE  4738  'to 4738'

 L.1189      4670  LOAD_GLOBAL              str
             4672  LOAD_GLOBAL              int
             4674  LOAD_FAST                'strNum'
             4676  CALL_FUNCTION_1       1  '1 positional argument'
             4678  LOAD_CONST               100
             4680  BINARY_FLOOR_DIVIDE
             4682  CALL_FUNCTION_1       1  '1 positional argument'
             4684  STORE_FAST               'strHH'

 L.1190      4686  LOAD_GLOBAL              str
             4688  LOAD_GLOBAL              int
             4690  LOAD_FAST                'strNum'
             4692  CALL_FUNCTION_1       1  '1 positional argument'
             4694  LOAD_CONST               100
             4696  BINARY_MODULO    
             4698  CALL_FUNCTION_1       1  '1 positional argument'
             4700  STORE_FAST               'strMM'

 L.1191      4702  LOAD_CONST               True
             4704  STORE_FAST               'military'

 L.1192      4706  LOAD_FAST                'wordNext'
             4708  LOAD_STR                 'uur'
             4710  COMPARE_OP               ==
         4712_4714  POP_JUMP_IF_TRUE   4726  'to 4726'
             4716  LOAD_FAST                'remainder'
             4718  LOAD_STR                 'uur'
             4720  COMPARE_OP               ==
         4722_4724  POP_JUMP_IF_FALSE  5148  'to 5148'
           4726_0  COME_FROM          4712  '4712'

 L.1193      4726  LOAD_FAST                'used'
             4728  LOAD_CONST               1
             4730  INPLACE_ADD      
             4732  STORE_FAST               'used'
         4734_4736  JUMP_FORWARD       5148  'to 5148'
           4738_0  COME_FROM          4666  '4666'

 L.1194      4738  LOAD_FAST                'wordNext'
         4740_4742  POP_JUMP_IF_FALSE  4810  'to 4810'
             4744  LOAD_FAST                'wordNext'
             4746  LOAD_CONST               0
             4748  BINARY_SUBSCR    
             4750  LOAD_METHOD              isdigit
             4752  CALL_METHOD_0         0  '0 positional arguments'
         4754_4756  POP_JUMP_IF_FALSE  4810  'to 4810'

 L.1196      4758  LOAD_FAST                'strNum'
             4760  STORE_FAST               'strHH'

 L.1197      4762  LOAD_FAST                'wordNext'
             4764  STORE_FAST               'strMM'

 L.1198      4766  LOAD_CONST               True
             4768  STORE_FAST               'military'

 L.1199      4770  LOAD_FAST                'used'
             4772  LOAD_CONST               1
             4774  INPLACE_ADD      
             4776  STORE_FAST               'used'

 L.1200      4778  LOAD_FAST                'wordNextNext'
             4780  LOAD_STR                 'uur'
             4782  COMPARE_OP               ==
         4784_4786  POP_JUMP_IF_TRUE   4798  'to 4798'
             4788  LOAD_FAST                'remainder'
             4790  LOAD_STR                 'uur'
             4792  COMPARE_OP               ==
         4794_4796  POP_JUMP_IF_FALSE  5148  'to 5148'
           4798_0  COME_FROM          4784  '4784'

 L.1201      4798  LOAD_FAST                'used'
             4800  LOAD_CONST               1
             4802  INPLACE_ADD      
             4804  STORE_FAST               'used'
         4806_4808  JUMP_FORWARD       5148  'to 5148'
           4810_0  COME_FROM          4754  '4754'
           4810_1  COME_FROM          4740  '4740'

 L.1203      4810  LOAD_FAST                'wordNext'
             4812  LOAD_STR                 ''
             4814  COMPARE_OP               ==
         4816_4818  POP_JUMP_IF_TRUE   4880  'to 4880'
             4820  LOAD_FAST                'wordNext'
             4822  LOAD_STR                 'uur'
             4824  COMPARE_OP               ==
         4826_4828  POP_JUMP_IF_TRUE   4880  'to 4880'

 L.1205      4830  LOAD_FAST                'wordNext'
             4832  LOAD_STR                 'in'
             4834  COMPARE_OP               ==
         4836_4838  POP_JUMP_IF_FALSE  4860  'to 4860'

 L.1207      4840  LOAD_FAST                'wordNextNext'
             4842  LOAD_STR                 'de'
             4844  COMPARE_OP               ==
         4846_4848  POP_JUMP_IF_TRUE   4880  'to 4880'

 L.1208      4850  LOAD_FAST                'wordNextNext'
             4852  LOAD_FAST                'timeQualifier'
             4854  COMPARE_OP               ==
         4856_4858  POP_JUMP_IF_TRUE   4880  'to 4880'
           4860_0  COME_FROM          4836  '4836'

 L.1210      4860  LOAD_FAST                'wordNext'
             4862  LOAD_STR                 'vannacht'
             4864  COMPARE_OP               ==
         4866_4868  POP_JUMP_IF_TRUE   4880  'to 4880'

 L.1211      4870  LOAD_FAST                'wordNextNext'
             4872  LOAD_STR                 'vannacht'
             4874  COMPARE_OP               ==
         4876_4878  POP_JUMP_IF_FALSE  5144  'to 5144'
           4880_0  COME_FROM          4866  '4866'
           4880_1  COME_FROM          4856  '4856'
           4880_2  COME_FROM          4846  '4846'
           4880_3  COME_FROM          4826  '4826'
           4880_4  COME_FROM          4816  '4816'

 L.1213      4880  LOAD_FAST                'strNum'
             4882  STORE_FAST               'strHH'

 L.1214      4884  LOAD_STR                 '00'
             4886  STORE_FAST               'strMM'

 L.1215      4888  LOAD_FAST                'wordNext'
             4890  LOAD_STR                 'uur'
             4892  COMPARE_OP               ==
         4894_4896  POP_JUMP_IF_FALSE  4906  'to 4906'

 L.1216      4898  LOAD_FAST                'used'
             4900  LOAD_CONST               1
             4902  INPLACE_ADD      
             4904  STORE_FAST               'used'
           4906_0  COME_FROM          4894  '4894'

 L.1218      4906  LOAD_FAST                'wordNext'
             4908  LOAD_STR                 'in'
             4910  COMPARE_OP               ==
         4912_4914  POP_JUMP_IF_TRUE   4926  'to 4926'
             4916  LOAD_FAST                'wordNextNext'
           4918_0  COME_FROM          3918  '3918'
             4918  LOAD_STR                 'in'
             4920  COMPARE_OP               ==
         4922_4924  POP_JUMP_IF_FALSE  5072  'to 5072'
           4926_0  COME_FROM          4912  '4912'

 L.1219      4926  LOAD_FAST                'used'
             4928  LOAD_FAST                'wordNext'
             4930  LOAD_STR                 'in'
             4932  COMPARE_OP               ==
         4934_4936  POP_JUMP_IF_FALSE  4942  'to 4942'
             4938  LOAD_CONST               1
             4940  JUMP_FORWARD       4944  'to 4944'
           4942_0  COME_FROM          4934  '4934'
             4942  LOAD_CONST               2
           4944_0  COME_FROM          4940  '4940'
             4944  INPLACE_ADD      
             4946  STORE_FAST               'used'

 L.1221      4948  LOAD_FAST                'idx'
             4950  LOAD_CONST               3
           4952_0  COME_FROM          3952  '3952'
             4952  BINARY_ADD       
             4954  LOAD_GLOBAL              len
             4956  LOAD_FAST                'words'
             4958  CALL_FUNCTION_1       1  '1 positional argument'
             4960  COMPARE_OP               <
         4962_4964  POP_JUMP_IF_FALSE  4978  'to 4978'
             4966  LOAD_FAST                'words'
             4968  LOAD_FAST                'idx'
             4970  LOAD_CONST               3
             4972  BINARY_ADD       
             4974  BINARY_SUBSCR    
             4976  JUMP_FORWARD       4980  'to 4980'
           4978_0  COME_FROM          4962  '4962'
             4978  LOAD_STR                 ''
           4980_0  COME_FROM          4976  '4976'
             4980  STORE_FAST               'wordNextNextNext'

 L.1223      4982  LOAD_FAST                'wordNextNext'
         4984_4986  POP_JUMP_IF_FALSE  5072  'to 5072'

 L.1224      4988  LOAD_FAST                'wordNextNext'
             4990  LOAD_FAST                'timeQualifier'
             4992  COMPARE_OP               in
         4994_4996  POP_JUMP_IF_TRUE   5008  'to 5008'

 L.1225      4998  LOAD_FAST                'wordNextNextNext'
             5000  LOAD_FAST                'timeQualifier'
             5002  COMPARE_OP               in
         5004_5006  POP_JUMP_IF_FALSE  5072  'to 5072'
           5008_0  COME_FROM          4994  '4994'

 L.1226      5008  LOAD_FAST                'wordNextNext'
             5010  LOAD_FAST                'timeQualifiersPM'
             5012  COMPARE_OP               in
         5014_5016  POP_JUMP_IF_TRUE   5028  'to 5028'

 L.1227      5018  LOAD_FAST                'wordNextNextNext'
           5020_0  COME_FROM          4020  '4020'
             5020  LOAD_FAST                'timeQualifiersPM'
             5022  COMPARE_OP               in
         5024_5026  POP_JUMP_IF_FALSE  5040  'to 5040'
           5028_0  COME_FROM          5014  '5014'

 L.1228      5028  LOAD_STR                 'pm'
             5030  STORE_FAST               'remainder'

 L.1229      5032  LOAD_FAST                'used'
             5034  LOAD_CONST               1
             5036  INPLACE_ADD      
             5038  STORE_FAST               'used'
           5040_0  COME_FROM          5024  '5024'

 L.1230      5040  LOAD_FAST                'wordNextNext'
             5042  LOAD_FAST                'timeQualifiersAM'
             5044  COMPARE_OP               in
         5046_5048  POP_JUMP_IF_TRUE   5060  'to 5060'

 L.1231      5050  LOAD_FAST                'wordNextNextNext'
             5052  LOAD_FAST                'timeQualifiersAM'
             5054  COMPARE_OP               in
         5056_5058  POP_JUMP_IF_FALSE  5072  'to 5072'
           5060_0  COME_FROM          5046  '5046'

 L.1232      5060  LOAD_STR                 'am'
             5062  STORE_FAST               'remainder'

 L.1233      5064  LOAD_FAST                'used'
             5066  LOAD_CONST               1
             5068  INPLACE_ADD      
             5070  STORE_FAST               'used'
           5072_0  COME_FROM          5056  '5056'
           5072_1  COME_FROM          5004  '5004'
           5072_2  COME_FROM          4984  '4984'
           5072_3  COME_FROM          4922  '4922'

 L.1235      5072  LOAD_FAST                'timeQualifier'
             5074  LOAD_STR                 ''
             5076  COMPARE_OP               !=
         5078_5080  POP_JUMP_IF_FALSE  5148  'to 5148'

 L.1236      5082  LOAD_FAST                'timeQualifier'
             5084  LOAD_FAST                'timeQualifiersPM'
             5086  COMPARE_OP               in
         5088_5090  POP_JUMP_IF_FALSE  5106  'to 5106'

 L.1237      5092  LOAD_STR                 'pm'
             5094  STORE_FAST               'remainder'

 L.1238      5096  LOAD_FAST                'used'
             5098  LOAD_CONST               1
             5100  INPLACE_ADD      
             5102  STORE_FAST               'used'
             5104  JUMP_FORWARD       5142  'to 5142'
           5106_0  COME_FROM          5088  '5088'

 L.1240      5106  LOAD_FAST                'timeQualifier'
             5108  LOAD_FAST                'timeQualifiersAM'
             5110  COMPARE_OP               in
         5112_5114  POP_JUMP_IF_FALSE  5130  'to 5130'

 L.1241      5116  LOAD_STR                 'am'
             5118  STORE_FAST               'remainder'

 L.1242      5120  LOAD_FAST                'used'
             5122  LOAD_CONST               1
             5124  INPLACE_ADD      
             5126  STORE_FAST               'used'
             5128  JUMP_FORWARD       5142  'to 5142'
           5130_0  COME_FROM          5112  '5112'

 L.1245      5130  LOAD_FAST                'used'
             5132  LOAD_CONST               1
             5134  INPLACE_ADD      
             5136  STORE_FAST               'used'

 L.1246      5138  LOAD_CONST               True
             5140  STORE_FAST               'military'
           5142_0  COME_FROM          5128  '5128'
           5142_1  COME_FROM          5104  '5104'
             5142  JUMP_FORWARD       5148  'to 5148'
           5144_0  COME_FROM          4876  '4876'

 L.1248      5144  LOAD_CONST               False
             5146  STORE_FAST               'isTime'
           5148_0  COME_FROM          5142  '5142'
           5148_1  COME_FROM          5078  '5078'
           5148_2  COME_FROM          4806  '4806'
           5148_3  COME_FROM          4794  '4794'
           5148_4  COME_FROM          4734  '4734'
           5148_5  COME_FROM          4722  '4722'
           5148_6  COME_FROM          4652  '4652'
           5148_7  COME_FROM          4584  '4584'
           5148_8  COME_FROM          4516  '4516'
           5148_9  COME_FROM          4406  '4406'
          5148_10  COME_FROM          4364  '4364'
          5148_11  COME_FROM          4308  '4308'
          5148_12  COME_FROM          4146  '4146'
          5148_13  COME_FROM          4122  '4122'
          5148_14  COME_FROM          4112  '4112'
          5148_15  COME_FROM          4098  '4098'
          5148_16  COME_FROM          4088  '4088'
          5148_17  COME_FROM          3654  '3654'

 L.1249      5148  LOAD_FAST                'strHH'
         5150_5152  POP_JUMP_IF_FALSE  5162  'to 5162'
             5154  LOAD_GLOBAL              int
             5156  LOAD_FAST                'strHH'
             5158  CALL_FUNCTION_1       1  '1 positional argument'
             5160  JUMP_FORWARD       5164  'to 5164'
           5162_0  COME_FROM          5150  '5150'
             5162  LOAD_CONST               0
           5164_0  COME_FROM          5160  '5160'
             5164  STORE_FAST               'HH'

 L.1250      5166  LOAD_FAST                'strMM'
         5168_5170  POP_JUMP_IF_FALSE  5180  'to 5180'
             5172  LOAD_GLOBAL              int
             5174  LOAD_FAST                'strMM'
             5176  CALL_FUNCTION_1       1  '1 positional argument'
             5178  JUMP_FORWARD       5182  'to 5182'
           5180_0  COME_FROM          5168  '5168'
             5180  LOAD_CONST               0
           5182_0  COME_FROM          5178  '5178'
             5182  STORE_FAST               'MM'

 L.1251      5184  LOAD_FAST                'remainder'
             5186  LOAD_STR                 'pm'
             5188  COMPARE_OP               ==
         5190_5192  POP_JUMP_IF_FALSE  5212  'to 5212'
             5194  LOAD_FAST                'HH'
             5196  LOAD_CONST               12
             5198  COMPARE_OP               <
         5200_5202  POP_JUMP_IF_FALSE  5212  'to 5212'
             5204  LOAD_FAST                'HH'
             5206  LOAD_CONST               12
             5208  BINARY_ADD       
             5210  JUMP_FORWARD       5214  'to 5214'
           5212_0  COME_FROM          5200  '5200'
           5212_1  COME_FROM          5190  '5190'
             5212  LOAD_FAST                'HH'
           5214_0  COME_FROM          5210  '5210'
             5214  STORE_FAST               'HH'

 L.1252      5216  LOAD_FAST                'remainder'
             5218  LOAD_STR                 'am'
             5220  COMPARE_OP               ==
         5222_5224  POP_JUMP_IF_FALSE  5244  'to 5244'
             5226  LOAD_FAST                'HH'
             5228  LOAD_CONST               12
             5230  COMPARE_OP               >=
         5232_5234  POP_JUMP_IF_FALSE  5244  'to 5244'
             5236  LOAD_FAST                'HH'
             5238  LOAD_CONST               12
             5240  BINARY_SUBTRACT  
             5242  JUMP_FORWARD       5246  'to 5246'
           5244_0  COME_FROM          5232  '5232'
           5244_1  COME_FROM          5222  '5222'
             5244  LOAD_FAST                'HH'
           5246_0  COME_FROM          5242  '5242'
             5246  STORE_FAST               'HH'

 L.1254      5248  LOAD_FAST                'military'
         5250_5252  POP_JUMP_IF_TRUE   5352  'to 5352'

 L.1255      5254  LOAD_FAST                'remainder'
             5256  LOAD_CONST               ('am', 'pm', 'uren', 'minuten', 'seconde', 'seconden', 'uur', 'minuut')
             5258  COMPARE_OP               not-in
         5260_5262  POP_JUMP_IF_FALSE  5352  'to 5352'

 L.1258      5264  LOAD_FAST                'daySpecified'
         5266_5268  POP_JUMP_IF_FALSE  5280  'to 5280'
             5270  LOAD_DEREF               'dayOffset'
             5272  LOAD_CONST               1
             5274  COMPARE_OP               <
         5276_5278  POP_JUMP_IF_FALSE  5352  'to 5352'
           5280_0  COME_FROM          5266  '5266'

 L.1261      5280  LOAD_FAST                'dateNow'
             5282  LOAD_ATTR                hour
             5284  LOAD_FAST                'HH'
             5286  COMPARE_OP               <
         5288_5290  POP_JUMP_IF_TRUE   5352  'to 5352'
             5292  LOAD_FAST                'dateNow'
             5294  LOAD_ATTR                hour
             5296  LOAD_FAST                'HH'
             5298  COMPARE_OP               ==
         5300_5302  POP_JUMP_IF_FALSE  5318  'to 5318'

 L.1262      5304  LOAD_FAST                'dateNow'
             5306  LOAD_ATTR                minute
             5308  LOAD_FAST                'MM'
             5310  COMPARE_OP               <
         5312_5314  POP_JUMP_IF_FALSE  5318  'to 5318'

 L.1263      5316  JUMP_FORWARD       5352  'to 5352'
           5318_0  COME_FROM          5312  '5312'
           5318_1  COME_FROM          5300  '5300'

 L.1264      5318  LOAD_FAST                'dateNow'
             5320  LOAD_ATTR                hour
             5322  LOAD_FAST                'HH'
             5324  LOAD_CONST               12
             5326  BINARY_ADD       
             5328  COMPARE_OP               <
         5330_5332  POP_JUMP_IF_FALSE  5344  'to 5344'

 L.1265      5334  LOAD_FAST                'HH'
             5336  LOAD_CONST               12
             5338  INPLACE_ADD      
             5340  STORE_FAST               'HH'
             5342  JUMP_FORWARD       5352  'to 5352'
           5344_0  COME_FROM          5330  '5330'

 L.1268      5344  LOAD_DEREF               'dayOffset'
             5346  LOAD_CONST               1
             5348  INPLACE_ADD      
             5350  STORE_DEREF              'dayOffset'
           5352_0  COME_FROM          5342  '5342'
           5352_1  COME_FROM          5316  '5316'
           5352_2  COME_FROM          5288  '5288'
           5352_3  COME_FROM          5276  '5276'
           5352_4  COME_FROM          5260  '5260'
           5352_5  COME_FROM          5250  '5250'

 L.1270      5352  LOAD_FAST                'timeQualifier'
             5354  LOAD_FAST                'timeQualifiersPM'
             5356  COMPARE_OP               in
         5358_5360  POP_JUMP_IF_FALSE  5380  'to 5380'
             5362  LOAD_FAST                'HH'
             5364  LOAD_CONST               12
             5366  COMPARE_OP               <
         5368_5370  POP_JUMP_IF_FALSE  5380  'to 5380'

 L.1271      5372  LOAD_FAST                'HH'
             5374  LOAD_CONST               12
             5376  INPLACE_ADD      
             5378  STORE_FAST               'HH'
           5380_0  COME_FROM          5368  '5368'
           5380_1  COME_FROM          5358  '5358'

 L.1273      5380  LOAD_FAST                'HH'
             5382  LOAD_CONST               24
             5384  COMPARE_OP               >
         5386_5388  POP_JUMP_IF_TRUE   5400  'to 5400'
             5390  LOAD_FAST                'MM'
             5392  LOAD_CONST               59
             5394  COMPARE_OP               >
           5396_0  COME_FROM          2872  '2872'
         5396_5398  POP_JUMP_IF_FALSE  5408  'to 5408'
           5400_0  COME_FROM          5386  '5386'

 L.1274      5400  LOAD_CONST               False
             5402  STORE_FAST               'isTime'

 L.1275      5404  LOAD_CONST               0
             5406  STORE_FAST               'used'
           5408_0  COME_FROM          5396  '5396'

 L.1276      5408  LOAD_FAST                'isTime'
         5410_5412  POP_JUMP_IF_FALSE  5430  'to 5430'

 L.1277      5414  LOAD_FAST                'HH'
             5416  STORE_DEREF              'hrAbs'

 L.1278      5418  LOAD_FAST                'MM'
             5420  STORE_DEREF              'minAbs'

 L.1279      5422  LOAD_FAST                'used'
             5424  LOAD_CONST               1
             5426  INPLACE_ADD      
             5428  STORE_FAST               'used'
           5430_0  COME_FROM          5410  '5410'
           5430_1  COME_FROM          3254  '3254'
           5430_2  COME_FROM          3240  '3240'
           5430_3  COME_FROM          3192  '3192'
           5430_4  COME_FROM          3144  '3144'
           5430_5  COME_FROM          2904  '2904'
           5430_6  COME_FROM          2896  '2896'
           5430_7  COME_FROM          2826  '2826'
           5430_8  COME_FROM          2788  '2788'
           5430_9  COME_FROM          2750  '2750'
          5430_10  COME_FROM          2712  '2712'

 L.1281      5430  LOAD_FAST                'used'
             5432  LOAD_CONST               0
             5434  COMPARE_OP               >
         5436_5438  POP_JUMP_IF_FALSE  2496  'to 2496'

 L.1283      5440  SETUP_LOOP         5492  'to 5492'
             5442  LOAD_GLOBAL              range
             5444  LOAD_FAST                'used'
             5446  CALL_FUNCTION_1       1  '1 positional argument'
             5448  GET_ITER         
             5450  FOR_ITER           5490  'to 5490'
             5452  STORE_FAST               'i'

 L.1284      5454  LOAD_FAST                'idx'
             5456  LOAD_FAST                'i'
             5458  BINARY_ADD       
             5460  LOAD_GLOBAL              len
             5462  LOAD_FAST                'words'
             5464  CALL_FUNCTION_1       1  '1 positional argument'
             5466  COMPARE_OP               >=
         5468_5470  POP_JUMP_IF_FALSE  5474  'to 5474'

 L.1285      5472  BREAK_LOOP       
           5474_0  COME_FROM          5468  '5468'

 L.1286      5474  LOAD_STR                 ''
             5476  LOAD_FAST                'words'
             5478  LOAD_FAST                'idx'
             5480  LOAD_FAST                'i'
             5482  BINARY_ADD       
             5484  STORE_SUBSCR     
         5486_5488  JUMP_BACK          5450  'to 5450'
             5490  POP_BLOCK        
           5492_0  COME_FROM_LOOP     5440  '5440'

 L.1288      5492  LOAD_FAST                'wordPrev'
             5494  LOAD_STR                 'vroeg'
             5496  COMPARE_OP               ==
         5498_5500  POP_JUMP_IF_FALSE  5528  'to 5528'

 L.1289      5502  LOAD_CONST               -1
             5504  STORE_DEREF              'hrOffset'

 L.1290      5506  LOAD_STR                 ''
             5508  LOAD_FAST                'words'
             5510  LOAD_FAST                'idx'
             5512  LOAD_CONST               1
             5514  BINARY_SUBTRACT  
             5516  STORE_SUBSCR     

 L.1291      5518  LOAD_FAST                'idx'
             5520  LOAD_CONST               1
             5522  INPLACE_SUBTRACT 
             5524  STORE_FAST               'idx'
             5526  JUMP_FORWARD       5562  'to 5562'
           5528_0  COME_FROM          5498  '5498'

 L.1292      5528  LOAD_FAST                'wordPrev'
             5530  LOAD_STR                 'laat'
             5532  COMPARE_OP               ==
         5534_5536  POP_JUMP_IF_FALSE  5562  'to 5562'

 L.1293      5538  LOAD_CONST               1
             5540  STORE_DEREF              'hrOffset'

 L.1294      5542  LOAD_STR                 ''
             5544  LOAD_FAST                'words'
             5546  LOAD_FAST                'idx'
             5548  LOAD_CONST               1
             5550  BINARY_SUBTRACT  
             5552  STORE_SUBSCR     

 L.1295      5554  LOAD_FAST                'idx'
             5556  LOAD_CONST               1
             5558  INPLACE_SUBTRACT 
             5560  STORE_FAST               'idx'
           5562_0  COME_FROM          5534  '5534'
           5562_1  COME_FROM          5526  '5526'

 L.1296      5562  LOAD_FAST                'idx'
             5564  LOAD_CONST               0
             5566  COMPARE_OP               >
         5568_5570  POP_JUMP_IF_FALSE  5608  'to 5608'
             5572  LOAD_FAST                'wordPrev'
             5574  LOAD_FAST                'markers'
             5576  COMPARE_OP               in
         5578_5580  POP_JUMP_IF_FALSE  5608  'to 5608'

 L.1297      5582  LOAD_STR                 ''
             5584  LOAD_FAST                'words'
             5586  LOAD_FAST                'idx'
             5588  LOAD_CONST               1
             5590  BINARY_SUBTRACT  
             5592  STORE_SUBSCR     

 L.1298      5594  LOAD_FAST                'wordPrev'
             5596  LOAD_STR                 'deze'
             5598  COMPARE_OP               ==
         5600_5602  POP_JUMP_IF_FALSE  5608  'to 5608'

 L.1299      5604  LOAD_CONST               True
             5606  STORE_FAST               'daySpecified'
           5608_0  COME_FROM          5600  '5600'
           5608_1  COME_FROM          5578  '5578'
           5608_2  COME_FROM          5568  '5568'

 L.1300      5608  LOAD_FAST                'idx'
             5610  LOAD_CONST               1
             5612  COMPARE_OP               >
         5614_5616  POP_JUMP_IF_FALSE  5654  'to 5654'
             5618  LOAD_FAST                'wordPrevPrev'
             5620  LOAD_FAST                'markers'
             5622  COMPARE_OP               in
         5624_5626  POP_JUMP_IF_FALSE  5654  'to 5654'

 L.1301      5628  LOAD_STR                 ''
             5630  LOAD_FAST                'words'
             5632  LOAD_FAST                'idx'
             5634  LOAD_CONST               2
             5636  BINARY_SUBTRACT  
             5638  STORE_SUBSCR     

 L.1302      5640  LOAD_FAST                'wordPrevPrev'
             5642  LOAD_STR                 'deze'
             5644  COMPARE_OP               ==
         5646_5648  POP_JUMP_IF_FALSE  5654  'to 5654'

 L.1303      5650  LOAD_CONST               True
             5652  STORE_FAST               'daySpecified'
           5654_0  COME_FROM          5646  '5646'
           5654_1  COME_FROM          5624  '5624'
           5654_2  COME_FROM          5614  '5614'

 L.1305      5654  LOAD_FAST                'idx'
             5656  LOAD_FAST                'used'
             5658  LOAD_CONST               1
             5660  BINARY_SUBTRACT  
             5662  INPLACE_ADD      
             5664  STORE_FAST               'idx'

 L.1306      5666  LOAD_CONST               True
             5668  STORE_DEREF              'found'
         5670_5672  JUMP_BACK          2496  'to 2496'
             5674  POP_BLOCK        
           5676_0  COME_FROM_LOOP     2484  '2484'

 L.1308      5676  LOAD_FAST                'date_found'
         5678_5680  POP_JUMP_IF_TRUE   5686  'to 5686'

 L.1309      5682  LOAD_CONST               None
             5684  RETURN_VALUE     
           5686_0  COME_FROM          5678  '5678'

 L.1311      5686  LOAD_DEREF               'dayOffset'
             5688  LOAD_CONST               False
             5690  COMPARE_OP               is
         5692_5694  POP_JUMP_IF_FALSE  5700  'to 5700'

 L.1312      5696  LOAD_CONST               0
             5698  STORE_DEREF              'dayOffset'
           5700_0  COME_FROM          5692  '5692'

 L.1316      5700  LOAD_FAST                'dateNow'
             5702  LOAD_ATTR                replace
             5704  LOAD_CONST               0
             5706  LOAD_CONST               ('microsecond',)
             5708  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             5710  STORE_FAST               'extractedDate'

 L.1318      5712  LOAD_DEREF               'datestr'
             5714  LOAD_STR                 ''
             5716  COMPARE_OP               !=
         5718_5720  POP_JUMP_IF_FALSE  5972  'to 5972'

 L.1320      5722  SETUP_EXCEPT       5740  'to 5740'

 L.1321      5724  LOAD_GLOBAL              datetime
             5726  LOAD_METHOD              strptime
             5728  LOAD_DEREF               'datestr'
             5730  LOAD_STR                 '%B %d'
             5732  CALL_METHOD_2         2  '2 positional arguments'
             5734  STORE_FAST               'temp'
             5736  POP_BLOCK        
             5738  JUMP_FORWARD       5774  'to 5774'
           5740_0  COME_FROM_EXCEPT   5722  '5722'

 L.1322      5740  DUP_TOP          
             5742  LOAD_GLOBAL              ValueError
             5744  COMPARE_OP               exception-match
         5746_5748  POP_JUMP_IF_FALSE  5772  'to 5772'
             5750  POP_TOP          
             5752  POP_TOP          
             5754  POP_TOP          

 L.1324      5756  LOAD_GLOBAL              datetime
             5758  LOAD_METHOD              strptime
             5760  LOAD_DEREF               'datestr'
             5762  LOAD_STR                 '%B %d %Y'
             5764  CALL_METHOD_2         2  '2 positional arguments'
             5766  STORE_FAST               'temp'
             5768  POP_EXCEPT       
             5770  JUMP_FORWARD       5774  'to 5774'
           5772_0  COME_FROM          5746  '5746'
             5772  END_FINALLY      
           5774_0  COME_FROM          5770  '5770'
           5774_1  COME_FROM          5738  '5738'

 L.1325      5774  LOAD_FAST                'extractedDate'
             5776  LOAD_ATTR                replace
             5778  LOAD_CONST               0
             5780  LOAD_CONST               0
             5782  LOAD_CONST               0
             5784  LOAD_CONST               ('hour', 'minute', 'second')
             5786  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             5788  STORE_FAST               'extractedDate'

 L.1326      5790  LOAD_FAST                'hasYear'
         5792_5794  POP_JUMP_IF_TRUE   5920  'to 5920'

 L.1327      5796  LOAD_FAST                'temp'
             5798  LOAD_ATTR                replace
             5800  LOAD_FAST                'extractedDate'
             5802  LOAD_ATTR                year

 L.1328      5804  LOAD_FAST                'extractedDate'
             5806  LOAD_ATTR                tzinfo
             5808  LOAD_CONST               ('year', 'tzinfo')
             5810  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             5812  STORE_FAST               'temp'

 L.1329      5814  LOAD_FAST                'extractedDate'
             5816  LOAD_FAST                'temp'
             5818  COMPARE_OP               <
         5820_5822  POP_JUMP_IF_FALSE  5870  'to 5870'

 L.1330      5824  LOAD_FAST                'extractedDate'
             5826  LOAD_ATTR                replace

 L.1331      5828  LOAD_GLOBAL              int
             5830  LOAD_FAST                'currentYear'
             5832  CALL_FUNCTION_1       1  '1 positional argument'

 L.1332      5834  LOAD_GLOBAL              int
             5836  LOAD_FAST                'temp'
             5838  LOAD_METHOD              strftime
             5840  LOAD_STR                 '%m'
             5842  CALL_METHOD_1         1  '1 positional argument'
             5844  CALL_FUNCTION_1       1  '1 positional argument'

 L.1333      5846  LOAD_GLOBAL              int
             5848  LOAD_FAST                'temp'
             5850  LOAD_METHOD              strftime
             5852  LOAD_STR                 '%d'
             5854  CALL_METHOD_1         1  '1 positional argument'
             5856  CALL_FUNCTION_1       1  '1 positional argument'

 L.1334      5858  LOAD_FAST                'extractedDate'
             5860  LOAD_ATTR                tzinfo
             5862  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5864  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5866  STORE_FAST               'extractedDate'
             5868  JUMP_FORWARD       5918  'to 5918'
           5870_0  COME_FROM          5820  '5820'

 L.1336      5870  LOAD_FAST                'extractedDate'
             5872  LOAD_ATTR                replace

 L.1337      5874  LOAD_GLOBAL              int
             5876  LOAD_FAST                'currentYear'
             5878  CALL_FUNCTION_1       1  '1 positional argument'
             5880  LOAD_CONST               1
             5882  BINARY_ADD       

 L.1338      5884  LOAD_GLOBAL              int
             5886  LOAD_FAST                'temp'
             5888  LOAD_METHOD              strftime
             5890  LOAD_STR                 '%m'
             5892  CALL_METHOD_1         1  '1 positional argument'
             5894  CALL_FUNCTION_1       1  '1 positional argument'

 L.1339      5896  LOAD_GLOBAL              int
             5898  LOAD_FAST                'temp'
             5900  LOAD_METHOD              strftime
             5902  LOAD_STR                 '%d'
             5904  CALL_METHOD_1         1  '1 positional argument'
             5906  CALL_FUNCTION_1       1  '1 positional argument'

 L.1340      5908  LOAD_FAST                'extractedDate'
             5910  LOAD_ATTR                tzinfo
             5912  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5914  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5916  STORE_FAST               'extractedDate'
           5918_0  COME_FROM          5868  '5868'
             5918  JUMP_FORWARD       5970  'to 5970'
           5920_0  COME_FROM          5792  '5792'

 L.1342      5920  LOAD_FAST                'extractedDate'
             5922  LOAD_ATTR                replace

 L.1343      5924  LOAD_GLOBAL              int
             5926  LOAD_FAST                'temp'
             5928  LOAD_METHOD              strftime
             5930  LOAD_STR                 '%Y'
             5932  CALL_METHOD_1         1  '1 positional argument'
             5934  CALL_FUNCTION_1       1  '1 positional argument'

 L.1344      5936  LOAD_GLOBAL              int
             5938  LOAD_FAST                'temp'
             5940  LOAD_METHOD              strftime
             5942  LOAD_STR                 '%m'
             5944  CALL_METHOD_1         1  '1 positional argument'
             5946  CALL_FUNCTION_1       1  '1 positional argument'

 L.1345      5948  LOAD_GLOBAL              int
             5950  LOAD_FAST                'temp'
             5952  LOAD_METHOD              strftime
             5954  LOAD_STR                 '%d'
             5956  CALL_METHOD_1         1  '1 positional argument'
             5958  CALL_FUNCTION_1       1  '1 positional argument'

 L.1346      5960  LOAD_FAST                'extractedDate'
             5962  LOAD_ATTR                tzinfo
             5964  LOAD_CONST               ('year', 'month', 'day', 'tzinfo')
             5966  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             5968  STORE_FAST               'extractedDate'
           5970_0  COME_FROM          5918  '5918'
             5970  JUMP_FORWARD       6018  'to 6018'
           5972_0  COME_FROM          5718  '5718'

 L.1349      5972  LOAD_DEREF               'hrOffset'
             5974  LOAD_CONST               0
             5976  COMPARE_OP               ==
         5978_5980  POP_JUMP_IF_FALSE  6018  'to 6018'
             5982  LOAD_DEREF               'minOffset'
             5984  LOAD_CONST               0
             5986  COMPARE_OP               ==
         5988_5990  POP_JUMP_IF_FALSE  6018  'to 6018'
             5992  LOAD_DEREF               'secOffset'
             5994  LOAD_CONST               0
             5996  COMPARE_OP               ==
         5998_6000  POP_JUMP_IF_FALSE  6018  'to 6018'

 L.1350      6002  LOAD_FAST                'extractedDate'
             6004  LOAD_ATTR                replace
             6006  LOAD_CONST               0
             6008  LOAD_CONST               0
             6010  LOAD_CONST               0
             6012  LOAD_CONST               ('hour', 'minute', 'second')
             6014  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6016  STORE_FAST               'extractedDate'
           6018_0  COME_FROM          5998  '5998'
           6018_1  COME_FROM          5988  '5988'
           6018_2  COME_FROM          5978  '5978'
           6018_3  COME_FROM          5970  '5970'

 L.1352      6018  LOAD_DEREF               'yearOffset'
             6020  LOAD_CONST               0
             6022  COMPARE_OP               !=
         6024_6026  POP_JUMP_IF_FALSE  6042  'to 6042'

 L.1353      6028  LOAD_FAST                'extractedDate'
             6030  LOAD_GLOBAL              relativedelta
             6032  LOAD_DEREF               'yearOffset'
             6034  LOAD_CONST               ('years',)
             6036  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6038  BINARY_ADD       
             6040  STORE_FAST               'extractedDate'
           6042_0  COME_FROM          6024  '6024'

 L.1354      6042  LOAD_DEREF               'monthOffset'
             6044  LOAD_CONST               0
             6046  COMPARE_OP               !=
         6048_6050  POP_JUMP_IF_FALSE  6066  'to 6066'

 L.1355      6052  LOAD_FAST                'extractedDate'
             6054  LOAD_GLOBAL              relativedelta
             6056  LOAD_DEREF               'monthOffset'
             6058  LOAD_CONST               ('months',)
             6060  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6062  BINARY_ADD       
             6064  STORE_FAST               'extractedDate'
           6066_0  COME_FROM          6048  '6048'

 L.1356      6066  LOAD_DEREF               'dayOffset'
             6068  LOAD_CONST               0
             6070  COMPARE_OP               !=
         6072_6074  POP_JUMP_IF_FALSE  6090  'to 6090'

 L.1357      6076  LOAD_FAST                'extractedDate'
             6078  LOAD_GLOBAL              relativedelta
             6080  LOAD_DEREF               'dayOffset'
             6082  LOAD_CONST               ('days',)
             6084  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6086  BINARY_ADD       
             6088  STORE_FAST               'extractedDate'
           6090_0  COME_FROM          6072  '6072'

 L.1358      6090  LOAD_DEREF               'hrAbs'
             6092  LOAD_CONST               -1
             6094  COMPARE_OP               !=
         6096_6098  POP_JUMP_IF_FALSE  6250  'to 6250'
             6100  LOAD_DEREF               'minAbs'
             6102  LOAD_CONST               -1
             6104  COMPARE_OP               !=
         6106_6108  POP_JUMP_IF_FALSE  6250  'to 6250'

 L.1361      6110  LOAD_DEREF               'hrAbs'
             6112  LOAD_CONST               None
             6114  COMPARE_OP               is
         6116_6118  POP_JUMP_IF_FALSE  6156  'to 6156'
             6120  LOAD_DEREF               'minAbs'
             6122  LOAD_CONST               None
             6124  COMPARE_OP               is
         6126_6128  POP_JUMP_IF_FALSE  6156  'to 6156'
             6130  LOAD_FAST                'default_time'
             6132  LOAD_CONST               None
             6134  COMPARE_OP               is-not
         6136_6138  POP_JUMP_IF_FALSE  6156  'to 6156'

 L.1362      6140  LOAD_FAST                'default_time'
             6142  LOAD_ATTR                hour
             6144  LOAD_FAST                'default_time'
             6146  LOAD_ATTR                minute
             6148  ROT_TWO          
             6150  STORE_DEREF              'hrAbs'
             6152  STORE_DEREF              'minAbs'
             6154  JUMP_FORWARD       6176  'to 6176'
           6156_0  COME_FROM          6136  '6136'
           6156_1  COME_FROM          6126  '6126'
           6156_2  COME_FROM          6116  '6116'

 L.1364      6156  LOAD_DEREF               'hrAbs'
         6158_6160  JUMP_IF_TRUE_OR_POP  6164  'to 6164'
             6162  LOAD_CONST               0
           6164_0  COME_FROM          6158  '6158'
             6164  STORE_DEREF              'hrAbs'

 L.1365      6166  LOAD_DEREF               'minAbs'
         6168_6170  JUMP_IF_TRUE_OR_POP  6174  'to 6174'
             6172  LOAD_CONST               0
           6174_0  COME_FROM          6168  '6168'
             6174  STORE_DEREF              'minAbs'
           6176_0  COME_FROM          6154  '6154'

 L.1367      6176  LOAD_FAST                'extractedDate'
             6178  LOAD_ATTR                replace
             6180  LOAD_DEREF               'hrAbs'

 L.1368      6182  LOAD_DEREF               'minAbs'
             6184  LOAD_CONST               ('hour', 'minute')
             6186  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6188  STORE_FAST               'extractedDate'

 L.1369      6190  LOAD_DEREF               'hrAbs'
             6192  LOAD_CONST               0
             6194  COMPARE_OP               !=
         6196_6198  POP_JUMP_IF_TRUE   6210  'to 6210'
             6200  LOAD_DEREF               'minAbs'
             6202  LOAD_CONST               0
             6204  COMPARE_OP               !=
         6206_6208  POP_JUMP_IF_FALSE  6250  'to 6250'
           6210_0  COME_FROM          6196  '6196'
             6210  LOAD_DEREF               'datestr'
             6212  LOAD_STR                 ''
             6214  COMPARE_OP               ==
         6216_6218  POP_JUMP_IF_FALSE  6250  'to 6250'

 L.1370      6220  LOAD_FAST                'daySpecified'
         6222_6224  POP_JUMP_IF_TRUE   6250  'to 6250'
             6226  LOAD_FAST                'dateNow'
             6228  LOAD_FAST                'extractedDate'
             6230  COMPARE_OP               >
         6232_6234  POP_JUMP_IF_FALSE  6250  'to 6250'

 L.1371      6236  LOAD_FAST                'extractedDate'
             6238  LOAD_GLOBAL              relativedelta
             6240  LOAD_CONST               1
             6242  LOAD_CONST               ('days',)
             6244  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6246  BINARY_ADD       
             6248  STORE_FAST               'extractedDate'
           6250_0  COME_FROM          6232  '6232'
           6250_1  COME_FROM          6222  '6222'
           6250_2  COME_FROM          6216  '6216'
           6250_3  COME_FROM          6206  '6206'
           6250_4  COME_FROM          6106  '6106'
           6250_5  COME_FROM          6096  '6096'

 L.1372      6250  LOAD_DEREF               'hrOffset'
             6252  LOAD_CONST               0
             6254  COMPARE_OP               !=
         6256_6258  POP_JUMP_IF_FALSE  6274  'to 6274'

 L.1373      6260  LOAD_FAST                'extractedDate'
             6262  LOAD_GLOBAL              relativedelta
             6264  LOAD_DEREF               'hrOffset'
             6266  LOAD_CONST               ('hours',)
             6268  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6270  BINARY_ADD       
             6272  STORE_FAST               'extractedDate'
           6274_0  COME_FROM          6256  '6256'

 L.1374      6274  LOAD_DEREF               'minOffset'
             6276  LOAD_CONST               0
             6278  COMPARE_OP               !=
         6280_6282  POP_JUMP_IF_FALSE  6298  'to 6298'

 L.1375      6284  LOAD_FAST                'extractedDate'
             6286  LOAD_GLOBAL              relativedelta
             6288  LOAD_DEREF               'minOffset'
             6290  LOAD_CONST               ('minutes',)
             6292  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6294  BINARY_ADD       
             6296  STORE_FAST               'extractedDate'
           6298_0  COME_FROM          6280  '6280'

 L.1376      6298  LOAD_DEREF               'secOffset'
             6300  LOAD_CONST               0
             6302  COMPARE_OP               !=
         6304_6306  POP_JUMP_IF_FALSE  6322  'to 6322'

 L.1377      6308  LOAD_FAST                'extractedDate'
             6310  LOAD_GLOBAL              relativedelta
             6312  LOAD_DEREF               'secOffset'
             6314  LOAD_CONST               ('seconds',)
             6316  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             6318  BINARY_ADD       
             6320  STORE_FAST               'extractedDate'
           6322_0  COME_FROM          6304  '6304'

 L.1378      6322  SETUP_LOOP         6404  'to 6404'
             6324  LOAD_GLOBAL              enumerate
             6326  LOAD_FAST                'words'
             6328  CALL_FUNCTION_1       1  '1 positional argument'
             6330  GET_ITER         
           6332_0  COME_FROM          6386  '6386'
           6332_1  COME_FROM          6368  '6368'
           6332_2  COME_FROM          6350  '6350'
             6332  FOR_ITER           6402  'to 6402'
             6334  UNPACK_SEQUENCE_2     2 
             6336  STORE_FAST               'idx'
             6338  STORE_FAST               'word'

 L.1379      6340  LOAD_FAST                'words'
             6342  LOAD_FAST                'idx'
             6344  BINARY_SUBSCR    
             6346  LOAD_STR                 'en'
             6348  COMPARE_OP               ==
         6350_6352  POP_JUMP_IF_FALSE  6332  'to 6332'

 L.1380      6354  LOAD_FAST                'words'
             6356  LOAD_FAST                'idx'
             6358  LOAD_CONST               1
             6360  BINARY_SUBTRACT  
             6362  BINARY_SUBSCR    
             6364  LOAD_STR                 ''
             6366  COMPARE_OP               ==
         6368_6370  POP_JUMP_IF_FALSE  6332  'to 6332'
             6372  LOAD_FAST                'words'
             6374  LOAD_FAST                'idx'
             6376  LOAD_CONST               1
             6378  BINARY_ADD       
             6380  BINARY_SUBSCR    
             6382  LOAD_STR                 ''
             6384  COMPARE_OP               ==
         6386_6388  POP_JUMP_IF_FALSE  6332  'to 6332'

 L.1381      6390  LOAD_STR                 ''
             6392  LOAD_FAST                'words'
             6394  LOAD_FAST                'idx'
             6396  STORE_SUBSCR     
         6398_6400  JUMP_BACK          6332  'to 6332'
             6402  POP_BLOCK        
           6404_0  COME_FROM_LOOP     6322  '6322'

 L.1383      6404  LOAD_STR                 ' '
             6406  LOAD_METHOD              join
             6408  LOAD_FAST                'words'
             6410  CALL_METHOD_1         1  '1 positional argument'
             6412  STORE_FAST               'resultStr'

 L.1384      6414  LOAD_STR                 ' '
             6416  LOAD_METHOD              join
             6418  LOAD_FAST                'resultStr'
             6420  LOAD_METHOD              split
             6422  CALL_METHOD_0         0  '0 positional arguments'
             6424  CALL_METHOD_1         1  '1 positional argument'
             6426  STORE_FAST               'resultStr'

 L.1385      6428  LOAD_FAST                'extractedDate'
             6430  LOAD_FAST                'resultStr'
             6432  BUILD_LIST_2          2 
             6434  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 1926


def isFractional_nl(input_str, short_scale=True):
    """This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    fracts = {'heel':1, 
     'half':2,  'halve':2,  'kwart':4}
    if short_scale:
        for num in _SHORT_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_SHORT_ORDINAL_STRING_NL[num]] = num

    else:
        for num in _LONG_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_LONG_ORDINAL_STRING_NL[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False


def extract_numbers_nl(text, short_scale=True, ordinals=False):
    """Takes in a string and extracts a list of numbers.

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
    results = _extract_numbers_with_text(_tokenize(text), short_scale, ordinals)
    return [float(result.value) for result in results]


def normalize_nl(text, remove_articles):
    """Dutch string normalization."""
    words = text.split()
    normalized = ''
    for word in words:
        if remove_articles:
            if word in _ARTICLES:
                continue
        textNumbers = [
         'nul', 'een', 'twee', 'drie', 'vier', 'vijf', 'zes',
         'zeven', 'acht', 'negen', 'tien', 'elf', 'twaalf',
         'dertien', 'veertien', 'vijftien', 'zestien',
         'zeventien', 'achttien', 'negentien', 'twintig']
        if word in textNumbers:
            word = str(textNumbers.index(word))
        normalized += ' ' + word

    return normalized[1:]