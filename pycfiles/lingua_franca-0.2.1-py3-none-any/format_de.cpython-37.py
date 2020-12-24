# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_de.py
# Compiled at: 2020-01-13 02:46:59
# Size of source mod 2**32: 12732 bytes
from lingua_franca.lang.format_common import convert_to_mixed_fraction
from math import floor
months = [
 'januar', 'februar', 'märz', 'april', 'mai', 'juni',
 'juli', 'august', 'september', 'oktober', 'november',
 'dezember']
NUM_STRING_DE = {0:'null', 
 1:'ein', 
 2:'zwei', 
 3:'drei', 
 4:'vier', 
 5:'fünf', 
 6:'sechs', 
 7:'sieben', 
 8:'acht', 
 9:'neun', 
 10:'zehn', 
 11:'elf', 
 12:'zwölf', 
 13:'dreizehn', 
 14:'vierzehn', 
 15:'fünfzehn', 
 16:'sechzehn', 
 17:'siebzehn', 
 18:'achtzehn', 
 19:'neunzehn', 
 20:'zwanzig', 
 30:'dreißig', 
 40:'vierzig', 
 50:'fünfzig', 
 60:'sechzig', 
 70:'siebzig', 
 80:'achtzig', 
 90:'neunzig', 
 100:'hundert'}
NUM_POWERS_OF_TEN = [
 '', 'tausend', 'Million', 'Milliarde', 'Billion', 'Billiarde', 'Trillion',
 'Trilliarde']
FRACTION_STRING_DE = {2:'halb', 
 3:'drittel', 
 4:'viertel', 
 5:'fünftel', 
 6:'sechstel', 
 7:'siebtel', 
 8:'achtel', 
 9:'neuntel', 
 10:'zehntel', 
 11:'elftel', 
 12:'zwölftel', 
 13:'dreizehntel', 
 14:'vierzehntel', 
 15:'fünfzehntel', 
 16:'sechzehntel', 
 17:'siebzehntel', 
 18:'achtzehntel', 
 19:'neunzehntel', 
 20:'zwanzigstel'}
EXTRA_SPACE = ''

def nice_number_de(number, speech, denominators=range(1, 21)):
    """ German helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3)).replace('.', ',')
    else:
        whole, num, den = result
        if not speech:
            if num == 0:
                return str(whole)
                return '{} {}/{}'.format(whole, num, den)
                if num == 0:
                    return str(whole)
                den_str = FRACTION_STRING_DE[den]
                if whole == 0:
                    if num == 1:
                        return_string = 'ein {}'.format(den_str)
            else:
                return_string = '{} {}'.format(num, den_str)
        elif num == 1:
            return_string = '{} und ein {}'.format(whole, den_str)
        else:
            return_string = '{} und {} {}'.format(whole, num, den_str)
    return return_string


def pronounce_number_de(num, places=2):
    """
    Convert a number to its spoken equivalent
    For example, '5.2' would return 'five point two'
    Args:
        num(float or int): the number to pronounce (set limit below)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number

    """

    def pronounce_triplet_de(num):
        result = ''
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += NUM_STRING_DE[hundreds] + EXTRA_SPACE + 'hundert' + EXTRA_SPACE
                num -= hundreds * 100
        if num == 0:
            result += ''
        else:
            if num == 1:
                result += 'eins'
            else:
                if num <= 20:
                    result += NUM_STRING_DE[num]
                else:
                    if num > 20:
                        ones = num % 10
                        tens = num - ones
                        if ones > 0:
                            result += NUM_STRING_DE[ones] + EXTRA_SPACE
                            if tens > 0:
                                result += 'und' + EXTRA_SPACE
                        if tens > 0:
                            result += NUM_STRING_DE[tens] + EXTRA_SPACE
        return result

    def pronounce_fractional_de(num, places):
        result = ''
        place = 10
        while places > 0:
            result += ' ' + NUM_STRING_DE[(int(num * place) % 10)]
            if int(num * place) % 10 == 1:
                result += 's'
            place *= 10
            places -= 1

        return result

    def pronounce_whole_number_de(num, scale_level=0):
        if num == 0:
            return ''
        num = floor(num)
        result = ''
        last_triplet = num % 1000
        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += 'eins'
                else:
                    result += 'eins'
            elif scale_level == 1:
                result += 'ein' + EXTRA_SPACE + 'tausend' + EXTRA_SPACE
            else:
                result += 'eine ' + NUM_POWERS_OF_TEN[scale_level] + ' '
        elif last_triplet > 1:
            result += pronounce_triplet_de(last_triplet)
            if scale_level == 1:
                result += 'tausend' + EXTRA_SPACE
            if scale_level >= 2:
                result += ' ' + NUM_POWERS_OF_TEN[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    result += 'e'
                result += 'n '
        num = floor(num / 1000)
        scale_level += 1
        return pronounce_whole_number_de(num, scale_level) + result

    result = ''
    if abs(num) >= 1000000000000000000000000:
        return str(num)
    if num == 0:
        return str(NUM_STRING_DE[0])
    if num < 0:
        return 'minus ' + pronounce_number_de(abs(num), places)
    if num == int(num):
        return pronounce_whole_number_de(num)
    whole_number_part = floor(num)
    fractional_part = num - whole_number_part
    result += pronounce_whole_number_de(whole_number_part)
    if places > 0:
        result += ' Komma'
        result += pronounce_fractional_de(fractional_part, places)
    return result


def pronounce_ordinal_de(num):
    ordinals = [
     'nullte', 'erste', 'zweite', 'dritte', 'vierte', 'fünfte',
     'sechste', 'siebte', 'achte']
    if num < 0 or num != int(num):
        return num
    if num < 9:
        return ordinals[num]
    if num < 20:
        return pronounce_number_de(num) + 'te'
    return pronounce_number_de(num) + 'ste'


def nice_time_de(dt, speech=True, use_24hour=False, use_ampm=False):
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
    if not speech:
        if use_24hour:
            string = dt.strftime('%H:%M')
        else:
            if use_ampm:
                string = dt.strftime('%I:%M %p')
            else:
                string = dt.strftime('%I:%M')
            if string[0] == '0':
                string = string[1:]
        return string
        speak = ''
        if use_24hour:
            if dt.hour == 1:
                speak += 'ein'
            else:
                speak += pronounce_number_de(dt.hour)
            speak += ' Uhr'
            if not dt.minute == 0:
                speak += ' ' + pronounce_number_de(dt.minute)
            return speak
    else:
        if dt.hour == 0:
            if dt.minute == 0:
                return 'Mitternacht'
        if dt.hour == 12 and dt.minute == 0:
            return 'Mittag'
    if dt.minute == 15:
        next_hour = (dt.hour + 1) % 12 or 12
        speak = 'viertel ' + pronounce_number_de(next_hour)
    else:
        if dt.minute == 30:
            next_hour = (dt.hour + 1) % 12 or 12
            speak = 'halb ' + pronounce_number_de(next_hour)
        else:
            if dt.minute == 45:
                next_hour = (dt.hour + 1) % 12 or 12
                speak = 'dreiviertel ' + pronounce_number_de(next_hour)
            else:
                hour = dt.hour % 12 or 12
                if hour == 1:
                    speak += 'ein'
                else:
                    speak += pronounce_number_de(hour)
                speak += ' Uhr'
                if not dt.minute == 0:
                    speak += ' ' + pronounce_number_de(dt.minute)
                if use_ampm:
                    if 3 <= dt.hour < 12:
                        speak += ' morgens'
                    else:
                        if 12 <= dt.hour < 18:
                            speak += ' nachmittags'
                        else:
                            if 18 <= dt.hour < 22:
                                speak += ' abends'
                            else:
                                speak += ' nachts'
                return speak


def nice_response_de(text):
    words = text.split()
    for idx, word in enumerate(words):
        if word.lower() in months:
            text = nice_ordinal_de(text)
        if word == '^':
            wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
            if wordNext.isnumeric():
                words[idx] = 'hoch'
                text = ' '.join(words)

    return text


def nice_ordinal_de(text):
    normalized_text = text
    words = text.split()
    for idx, word in enumerate(words):
        wordNext = words[(idx + 1)] if idx + 1 < len(words) else ''
        wordPrev = words[(idx - 1)] if idx > 0 else ''
        if word[-1:] == '.':
            if word[:-1].isdecimal():
                if wordNext.lower() in months:
                    word = pronounce_ordinal_de(int(word[:-1]))
                    if wordPrev.lower() in ('am', 'dem', 'vom', 'zum', '(vom', '(am',
                                            'zum'):
                        word += 'n'
                    else:
                        if wordPrev.lower() not in ('der', 'die', 'das'):
                            word += 'r'
                    words[idx] = word
            normalized_text = ' '.join(words)

    return normalized_text