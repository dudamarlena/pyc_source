# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_en.py
# Compiled at: 2019-12-23 00:56:26
# Size of source mod 2**32: 13945 bytes
from lingua_franca.lang.format_common import convert_to_mixed_fraction
from lingua_franca.lang.common_data_en import _NUM_STRING_EN, _FRACTION_STRING_EN, _LONG_SCALE_EN, _SHORT_SCALE_EN, _SHORT_ORDINAL_EN, _LONG_ORDINAL_EN

def nice_number_en(number, speech, denominators=range(1, 21)):
    """ English helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 and a half" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3))
    else:
        whole, num, den = result
        if not speech:
            if num == 0:
                return str(whole)
                return '{} {}/{}'.format(whole, num, den)
                if num == 0:
                    return str(whole)
                den_str = _FRACTION_STRING_EN[den]
                if whole == 0:
                    if num == 1:
                        return_string = 'a {}'.format(den_str)
            else:
                return_string = '{} {}'.format(num, den_str)
        elif num == 1:
            return_string = '{} and a {}'.format(whole, den_str)
        else:
            return_string = '{} and {} {}'.format(whole, num, den_str)
    if num > 1:
        return_string += 's'
    return return_string


def pronounce_number_en(num, places=2, short_scale=True, scientific=False, ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    if num == float('inf'):
        return 'infinity'
        if num == float('-inf'):
            return 'negative infinity'
            if scientific:
                number = '%E' % num
                n, power = number.replace('+', '').split('E')
                power = int(power)
                if power != 0:
                    if ordinals:
                        return '{}{} times ten to the {}{} power'.format('negative ' if float(n) < 0 else '', pronounce_number_en((abs(float(n))), places, short_scale, False, ordinals=False), 'negative ' if power < 0 else '', pronounce_number_en((abs(power)), places, short_scale, False, ordinals=True))
                    return '{}{} times ten to the power of {}{}'.format('negative ' if float(n) < 0 else '', pronounce_number_en(abs(float(n)), places, short_scale, False), 'negative ' if power < 0 else '', pronounce_number_en(abs(power), places, short_scale, False))
        else:
            if short_scale:
                number_names = _NUM_STRING_EN.copy()
                number_names.update(_SHORT_SCALE_EN)
            else:
                number_names = _NUM_STRING_EN.copy()
                number_names.update(_LONG_SCALE_EN)
            digits = [number_names[n] for n in range(0, 20)]
            tens = [number_names[n] for n in range(10, 100, 10)]
            if short_scale:
                hundreds = [_SHORT_SCALE_EN[n] for n in _SHORT_SCALE_EN.keys()]
            else:
                hundreds = [_LONG_SCALE_EN[n] for n in _LONG_SCALE_EN.keys()]
        result = ''
        if num < 0:
            result = 'negative ' if scientific else 'minus '
        else:
            num = abs(num)
            if not ordinals:
                try:
                    if len(str(num)) == 4:
                        if isinstance(num, int):
                            _num = str(num)
                            if not _num[1:4] == '000':
                                if not _num[1:3] == '00':
                                    if int(_num[0:2]) >= 20:
                                        pass
                                    else:
                                        if _num[2:4] == '00':
                                            first = number_names[int(_num[0:2])]
                                            last = number_names[100]
                                            return first + ' ' + last
                                        first = number_names[int(_num[0:2])]
                                        if _num[3:4] == '0':
                                            last = number_names[int(_num[2:4])]
                                        else:
                                            second = number_names[(int(_num[2:3]) * 10)]
                                            last = second + ' ' + number_names[int(_num[3:4])]
                                        return first + ' ' + last
                except Exception as e:
                    try:
                        print('ERROR: Exception in pronounce_number_en: {}' + repr(e))
                    finally:
                        e = None
                        del e

            if num in number_names and not ordinals:
                if num > 90:
                    result += 'one '
                result += number_names[num]
            else:

                def _sub_thousand(n, ordinals=False):
                    assert 0 <= n <= 999
                    if n in _SHORT_ORDINAL_EN:
                        if ordinals:
                            return _SHORT_ORDINAL_EN[n]
                    if n <= 19:
                        return digits[n]
                    if n <= 99:
                        q, r = divmod(n, 10)
                        return tens[(q - 1)] + (' ' + _sub_thousand(r, ordinals) if r else '')
                    q, r = divmod(n, 100)
                    return digits[q] + ' hundred' + (' and ' + _sub_thousand(r, ordinals) if r else '')

                def _short_scale(n):
                    if n >= max(_SHORT_SCALE_EN.keys()):
                        return 'infinity'
                    ordi = ordinals
                    if int(n) != n:
                        ordi = False
                    n = int(n)
                    assert 0 <= n
                    res = []
                    for i, z in enumerate(_split_by(n, 1000)):
                        if not z:
                            continue
                        number = _sub_thousand(z, not i and ordi)
                        if i:
                            if i >= len(hundreds):
                                return ''
                            number += ' '
                            if ordi:
                                if i * 1000 in _SHORT_ORDINAL_EN:
                                    if z == 1:
                                        number = _SHORT_ORDINAL_EN[(i * 1000)]
                                    else:
                                        number += _SHORT_ORDINAL_EN[(i * 1000)]
                                else:
                                    if n not in _SHORT_SCALE_EN:
                                        num = int('1' + '0' * (len(str(n)) - 2))
                                        number += _SHORT_SCALE_EN[num] + 'th'
                                    else:
                                        number = _SHORT_SCALE_EN[n] + 'th'
                            else:
                                number += hundreds[i]
                        res.append(number)
                        ordi = False

                    return ', '.join(reversed(res))

                def _split_by(n, split=1000):
                    assert 0 <= n
                    res = []
                    while n:
                        n, r = divmod(n, split)
                        res.append(r)

                    return res

                def _long_scale(n):
                    if n >= max(_LONG_SCALE_EN.keys()):
                        return 'infinity'
                    ordi = ordinals
                    if int(n) != n:
                        ordi = False
                    n = int(n)
                    assert 0 <= n
                    res = []
                    for i, z in enumerate(_split_by(n, 1000000)):
                        if not z:
                            continue
                        number = pronounce_number_en(z, places, True, scientific, ordinals=(ordi and not i))
                        if i:
                            if i >= len(hundreds):
                                return ''
                            number = number.replace(',', '')
                            if ordi:
                                if i * 1000000 in _LONG_ORDINAL_EN:
                                    if z == 1:
                                        number = _LONG_ORDINAL_EN[((i + 1) * 1000000)]
                                    else:
                                        number += _LONG_ORDINAL_EN[((i + 1) * 1000000)]
                                else:
                                    if n not in _LONG_SCALE_EN:
                                        num = int('1' + '0' * (len(str(n)) - 2))
                                        number += ' ' + _LONG_SCALE_EN[num] + 'th'
                                    else:
                                        number = ' ' + _LONG_SCALE_EN[n] + 'th'
                            else:
                                number += ' ' + hundreds[(i + 1)]
                        res.append(number)

                    return ', '.join(reversed(res))

                if short_scale:
                    result += _short_scale(num)
                else:
                    result += _long_scale(num)
    else:
        if not result:
            if 'e' in str(num):
                return pronounce_number_en(num, places, short_scale, scientific=True)
        if not num == int(num):
            if places > 0:
                result += ' point'
                place = 10
                while int(num * place) % 10 > 0 and places > 0:
                    result += ' ' + number_names[(int(num * place) % 10)]
                    place *= 10
                    places -= 1

    return result


def nice_time_en(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format
    For example, generate 'five thirty' for speech or '5:30' for
    text display.
    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        string = dt.strftime('%H:%M')
    else:
        if use_ampm:
            string = dt.strftime('%I:%M %p')
        else:
            string = dt.strftime('%I:%M')
        if string[0] == '0':
            string = string[1:]
        else:
            return speech or string
        if use_24hour:
            speak = ''
            if string[0] == '0':
                speak += pronounce_number_en(int(string[0])) + ' '
                speak += pronounce_number_en(int(string[1]))
            else:
                speak = pronounce_number_en(int(string[0:2]))
            speak += ' '
            if string[3:5] == '00':
                speak += 'hundred'
            else:
                if string[3] == '0':
                    speak += pronounce_number_en(0) + ' '
                    speak += pronounce_number_en(int(string[4]))
                else:
                    speak += pronounce_number_en(int(string[3:5]))
            return speak
        if dt.hour == 0:
            if dt.minute == 0:
                return 'midnight'
        if dt.hour == 12:
            if dt.minute == 0:
                return 'noon'
        hour = dt.hour % 12 or 12
        if dt.minute == 15:
            speak = 'quarter past ' + pronounce_number_en(hour)
        else:
            if dt.minute == 30:
                speak = 'half past ' + pronounce_number_en(hour)
            else:
                if dt.minute == 45:
                    next_hour = (dt.hour + 1) % 12 or 12
                    speak = 'quarter to ' + pronounce_number_en(next_hour)
                else:
                    speak = pronounce_number_en(hour)
                    if dt.minute == 0:
                        if not use_ampm:
                            return speak + " o'clock"
                        else:
                            if dt.minute < 10:
                                speak += ' oh'
                            speak += ' ' + pronounce_number_en(dt.minute)
                    elif use_ampm:
                        if dt.hour > 11:
                            speak += ' p.m.'
                        else:
                            speak += ' a.m.'
                    return speak