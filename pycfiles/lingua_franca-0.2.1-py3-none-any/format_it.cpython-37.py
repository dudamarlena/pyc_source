# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_it.py
# Compiled at: 2020-03-04 07:40:03
# Size of source mod 2**32: 14797 bytes
from lingua_franca.lang.format_common import convert_to_mixed_fraction
import collections
NUM_STRING_IT = {0:'zero', 
 1:'uno', 
 2:'due', 
 3:'tre', 
 4:'quattro', 
 5:'cinque', 
 6:'sei', 
 7:'sette', 
 8:'otto', 
 9:'nove', 
 10:'dieci', 
 11:'undici', 
 12:'dodici', 
 13:'tredici', 
 14:'quattordici', 
 15:'quindici', 
 16:'sedici', 
 17:'diciassette', 
 18:'diciotto', 
 19:'diciannove', 
 20:'venti', 
 30:'trenta', 
 40:'quaranta', 
 50:'cinquanta', 
 60:'sessanta', 
 70:'settanta', 
 80:'ottanta', 
 90:'novanta'}
FRACTION_STRING_IT = {2:'mezz', 
 3:'terz', 
 4:'quart', 
 5:'quint', 
 6:'sest', 
 7:'settim', 
 8:'ottav', 
 9:'non', 
 10:'decim', 
 11:'undicesim', 
 12:'dodicesim', 
 13:'tredicesim', 
 14:'quattordicesim', 
 15:'quindicesim', 
 16:'sedicesim', 
 17:'diciassettesim', 
 18:'diciottesim', 
 19:'diciannovesim', 
 20:'ventesim'}
LONG_SCALE_IT = collections.OrderedDict([
 (100, 'cento'),
 (1000, 'mila'),
 (1000000, 'milioni'),
 (1000000000.0, 'miliardi'),
 (1000000000000.0, 'bilioni'),
 (1e+18, 'trilioni'),
 (1e+24, 'quadrilioni'),
 (1e+30, 'quintilioni'),
 (1e+36, 'sestilioni'),
 (1e+42, 'settilioni'),
 (1e+48, 'ottillioni'),
 (1e+54, 'nonillioni'),
 (1e+60, 'decemillioni'),
 (1e+66, 'undicilione'),
 (1e+72, 'dodicilione'),
 (1e+78, 'tredicilione'),
 (1e+84, 'quattordicilione'),
 (1e+90, 'quindicilione'),
 (1e+96, 'sedicilione'),
 (1e+102, 'diciasettilione'),
 (1e+108, 'diciottilione'),
 (1e+114, 'dicianovilione'),
 (1e+120, 'vintilione'),
 (1e+306, 'unquinquagintilione'),
 (float('inf'), 'duoquinquagintilione'),
 (float('inf'), 'sesquinquagintilione'),
 (float('inf'), 'unsexagintilione')])
SHORT_SCALE_IT = collections.OrderedDict([
 (100, 'cento'),
 (1000, 'mila'),
 (1000000, 'milioni'),
 (1000000000.0, 'miliardi'),
 (1000000000000.0, 'bilioni'),
 (1000000000000000.0, 'biliardi'),
 (1e+18, 'trilioni'),
 (1e+21, 'triliardi'),
 (1e+24, 'quadrilioni'),
 (1e+27, 'quadriliardi'),
 (1e+30, 'quintilioni'),
 (1e+33, 'quintiliardi'),
 (1e+36, 'sestilioni'),
 (1e+39, 'sestiliardi'),
 (1e+42, 'settilioni'),
 (1e+45, 'settiliardi'),
 (1e+48, 'ottilioni'),
 (1e+51, 'ottiliardi'),
 (1e+54, 'nonilioni'),
 (1e+57, 'noniliardi'),
 (1e+60, 'decilioni'),
 (1e+63, 'deciliardi'),
 (1e+66, 'undicilioni'),
 (1e+69, 'undiciliardi'),
 (1e+72, 'dodicilioni'),
 (1e+75, 'dodiciliardi'),
 (1e+78, 'tredicilioni'),
 (1e+81, 'trediciliardi'),
 (1e+84, 'quattordicilioni'),
 (1e+87, 'quattordiciliardi'),
 (1e+90, 'quindicilioni'),
 (1e+93, 'quindiciliardi'),
 (1e+96, 'sedicilioni'),
 (1e+99, 'sediciliardi'),
 (1e+102, 'diciassettilioni'),
 (1e+105, 'diciassettiliardi'),
 (1e+108, 'diciottilioni'),
 (1e+111, 'diciottiliardi'),
 (1e+114, 'dicianovilioni'),
 (1e+117, 'dicianoviliardi'),
 (1e+120, 'vintilioni'),
 (1e+123, 'vintiliardi'),
 (1e+153, 'quinquagintillion'),
 (1e+183, 'sexagintillion'),
 (1e+213, 'septuagintillion'),
 (1e+243, 'ottogintilioni'),
 (1e+273, 'nonigintillioni'),
 (1e+303, 'centilioni'),
 (1e+306, 'uncentilioni'),
 (float('inf'), 'duocentilioni'),
 (float('inf'), 'trecentilioni'),
 (float('inf'), 'decicentilioni'),
 (float('inf'), 'undicicentilioni'),
 (float('inf'), 'viginticentilioni'),
 (float('inf'), 'unviginticentilioni'),
 (float('inf'), 'trigintacentilioni'),
 (float('inf'), 'quadragintacentillion'),
 (float('inf'), 'quinquagintacentillion'),
 (float('inf'), 'sexagintacentillion'),
 (float('inf'), 'septuagintacentillion'),
 (float('inf'), 'ctogintacentillion'),
 (float('inf'), 'nonagintacentillion'),
 (float('inf'), 'ducentillion'),
 (float('inf'), 'trecentillion'),
 (float('inf'), 'quadringentillion'),
 (float('inf'), 'quingentillion'),
 (float('inf'), 'sescentillion'),
 (float('inf'), 'septingentillion'),
 (float('inf'), 'octingentillion'),
 (float('inf'), 'nongentillion'),
 (float('inf'), 'millinillion')])

def nice_number_it(number, speech, denominators=range(1, 21)):
    """ Italian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e un mezz" for speech and "4 1/2" for text

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
            else:
                return '{} {}/{}'.format(whole, num, den)
                if num == 0:
                    return str(whole)
                    den_str = FRACTION_STRING_IT[den]
                    if whole == 0:
                        if num == 1:
                            return_string = 'un {}'.format(den_str)
                        else:
                            return_string = '{} {}'.format(num, den_str)
                elif num == 1:
                    return_string = '{} e un {}'.format(whole, den_str)
                else:
                    return_string = '{} e {} {}'.format(whole, num, den_str)
            if num > 1:
                return_string += 'i'
        else:
            return_string += 'o'
    return return_string


def pronounce_number_it(num, places=2, short_scale=False, scientific=False):
    """
    Convert a number to it's spoken equivalent
    adapted to italian fron en version

    For example, '5.2' would return 'cinque virgola due'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    if num == float('inf'):
        return 'infinito'
        if num == float('-inf'):
            return 'meno infinito'
        if scientific:
            number = '%E' % num
            n, power = number.replace('+', '').split('E')
            power = int(power)
            if power != 0:
                return '{}{} per dieci elevato alla {}{}'.format('meno ' if float(n) < 0 else '', pronounce_number_it(abs(float(n)), places, short_scale, False), 'meno ' if power < 0 else '', pronounce_number_it(abs(power), places, short_scale, False))
    else:
        if short_scale:
            number_names = NUM_STRING_IT.copy()
            number_names.update(SHORT_SCALE_IT)
        else:
            number_names = NUM_STRING_IT.copy()
            number_names.update(LONG_SCALE_IT)
        digits = [number_names[n] for n in range(0, 20)]
        tens = [number_names[n] for n in range(10, 100, 10)]
        if short_scale:
            hundreds = [SHORT_SCALE_IT[n] for n in SHORT_SCALE_IT.keys()]
        else:
            hundreds = [LONG_SCALE_IT[n] for n in LONG_SCALE_IT.keys()]
        result = ''
        if num < 0:
            result = 'meno '
        else:
            num = abs(num)
            if num in number_names:
                if num > 90:
                    result += ''
                result += number_names[num]
            else:

                def _sub_thousand(n):
                    if not 0 <= n <= 999:
                        raise AssertionError
                    elif n <= 19:
                        return digits[n]
                        if n <= 99:
                            q, r = divmod(n, 10)
                            _deci = tens[(q - 1)]
                            _unit = r
                            _partial = _deci
                            if _unit > 0:
                                if _unit == 1 or _unit == 8:
                                    _partial = _partial[:-1]
                                _partial += number_names[_unit]
                            return _partial
                        q, r = divmod(n, 100)
                        if q == 1:
                            _partial = 'cento'
                    else:
                        _partial = digits[q] + 'cento'
                    _partial += ' ' + _sub_thousand(r) if r else ''
                    return _partial

                def _short_scale(n):
                    if n >= max(SHORT_SCALE_IT.keys()):
                        return 'numero davvero enorme'
                    n = int(n)
                    assert 0 <= n
                    res = []
                    for i, z in enumerate(_split_by(n, 1000)):
                        if not z:
                            continue
                        number = _sub_thousand(z)
                        if i:
                            number += ''
                            number += hundreds[i]
                        res.append(number)

                    return ', '.join(reversed(res))

                def _split_by(n, split=1000):
                    assert 0 <= n
                    res = []
                    while n:
                        n, r = divmod(n, split)
                        res.append(r)

                    return res

                def _long_scale(n):
                    if n >= max(LONG_SCALE_IT.keys()):
                        return 'numero davvero enorme'
                    n = int(n)
                    assert 0 <= n
                    res = []
                    for i, z in enumerate(_split_by(n, 1000000)):
                        if not z:
                            continue
                        number = pronounce_number_it(z, places, True, scientific)
                        if i:
                            number = number.replace(',', '')
                            number += ' ' + hundreds[(i + 1)]
                        res.append(number)

                    return ', '.join(reversed(res))

                if short_scale:
                    result += _short_scale(num)
                else:
                    result += _long_scale(num)
        if result == 'mila':
            result = 'mille'
        if result == 'milioni':
            result = 'un milione'
        if result == 'miliardi':
            result = 'un miliardo'
        if result[0:7] == 'unomila':
            result = result.replace('unomila', 'mille', 1)
        if result[0:10] == 'unomilioni':
            result = result.replace('unomilioni', 'un milione', 1)
        if not num == int(num):
            if places > 0:
                if abs(num) < 1.0:
                    result is 'meno ' or result or result += 'zero'
                result += ' virgola'
                _num_str = str(num)
                _num_str = _num_str.split('.')[1][0:places]
                for char in _num_str:
                    result += ' ' + number_names[int(char)]

    return result


def nice_time_it(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format
    adapted to italian fron en version

    For example, generate 'cinque e trenta' for speech or '5:30' for
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
        elif not speech:
            return string
            if use_24hour:
                speak = ''
                if string[0:2] == '00':
                    speak += 'zerozero'
                else:
                    if string[0] == '0':
                        speak += pronounce_number_it(int(string[0])) + ' '
                        if int(string[1]) == 1:
                            speak = 'una'
                        else:
                            speak += pronounce_number_it(int(string[1]))
                    else:
                        speak = pronounce_number_it(int(string[0:2]))
                speak += ' e '
                if string[3:5] == '00':
                    speak += 'zerozero'
                else:
                    if string[3] == '0':
                        speak += pronounce_number_it(0) + ' '
                        speak += pronounce_number_it(int(string[4]))
                    else:
                        speak += pronounce_number_it(int(string[3:5]))
                return speak
            if dt.hour == 0:
                if dt.minute == 0:
                    return 'mezzanotte'
            if dt.hour == 12:
                if dt.minute == 0:
                    return 'mezzogiorno'
            if dt.hour == 0:
                speak = 'mezzanotte'
            else:
                if dt.hour == 1 or dt.hour == 13:
                    speak = 'una'
                else:
                    if dt.hour > 13:
                        speak = pronounce_number_it(dt.hour - 12)
                    else:
                        speak = pronounce_number_it(dt.hour)
            speak += ' e'
            if dt.minute == 0:
                speak = speak[:-2]
                if not use_ampm:
                    speak += ' in punto'
        elif dt.minute == 15:
            speak += ' un quarto'
        else:
            if dt.minute == 45:
                speak += ' tre quarti'
            else:
                if dt.minute < 10:
                    speak += ' zero'
                speak += ' ' + pronounce_number_it(dt.minute)
        if use_ampm:
            if dt.hour < 4:
                speak.strip()
            else:
                if dt.hour > 20:
                    speak += ' della notte'
                else:
                    if dt.hour > 17:
                        speak += ' della sera'
                    else:
                        if dt.hour > 12:
                            speak += ' del pomeriggio'
                        else:
                            speak += ' della mattina'
        return speak