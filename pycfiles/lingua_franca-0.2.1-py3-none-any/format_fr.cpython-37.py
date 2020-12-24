# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_fr.py
# Compiled at: 2020-03-04 07:40:03
# Size of source mod 2**32: 8918 bytes
""" Format functions for french (fr)

"""
from lingua_franca.lang.format_common import convert_to_mixed_fraction
NUM_STRING_FR = {0:'zéro', 
 1:'un', 
 2:'deux', 
 3:'trois', 
 4:'quatre', 
 5:'cinq', 
 6:'six', 
 7:'sept', 
 8:'huit', 
 9:'neuf', 
 10:'dix', 
 11:'onze', 
 12:'douze', 
 13:'treize', 
 14:'quatorze', 
 15:'quinze', 
 16:'seize', 
 20:'vingt', 
 30:'trente', 
 40:'quarante', 
 50:'cinquante', 
 60:'soixante', 
 70:'soixante-dix', 
 80:'quatre-vingt', 
 90:'quatre-vingt-dix'}
FRACTION_STRING_FR = {2:'demi', 
 3:'tiers', 
 4:'quart', 
 5:'cinquième', 
 6:'sixième', 
 7:'septième', 
 8:'huitième', 
 9:'neuvième', 
 10:'dixième', 
 11:'onzième', 
 12:'douzième', 
 13:'treizième', 
 14:'quatorzième', 
 15:'quinzième', 
 16:'seizième', 
 17:'dix-septième', 
 18:'dix-huitième', 
 19:'dix-neuvième', 
 20:'vingtième'}

def nice_number_fr(number, speech, denominators=range(1, 21)):
    """ French helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 et demi" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ''
    whole = 0
    num = 0
    den = 0
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        whole = round(number, 3)
    else:
        whole, num, den = result
    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(',', '\xa0')
            strNumber = strNumber.replace('.', ',')
            return strNumber
        return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            strNumber = str(whole)
            strNumber = strNumber.replace('.', ',')
            return strNumber
        den_str = FRACTION_STRING_FR[den]
        if whole == 0:
            if num == 1:
                strNumber = 'un {}'.format(den_str)
            else:
                strNumber = '{} {}'.format(num, den_str)
        else:
            if num == 1:
                if den == 2:
                    strNumber = '{} et {}'.format(whole, den_str)
                else:
                    strNumber = '{} et 1 {}'.format(whole, den_str)
            else:
                strNumber = '{} et {} {}'.format(whole, num, den_str)
        if num > 1:
            if den != 3:
                strNumber += 's'
        return strNumber


def pronounce_number_fr(num, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinq virgule deux'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(num) >= 100:
        return str(num)
    else:
        result = ''
        if num < 0:
            result = 'moins '
        else:
            num = abs(num)
            if num > 16:
                tens = int(num - int(num) % 10)
                ones = int(num - tens)
                if ones != 0:
                    if tens > 10:
                        if tens <= 60:
                            if int(num - tens) == 1:
                                result += NUM_STRING_FR[tens] + '-et-' + NUM_STRING_FR[ones]
                            else:
                                if num == 71:
                                    result += 'soixante-et-onze'
                                else:
                                    if tens == 70:
                                        result += NUM_STRING_FR[60] + '-'
                                        if ones < 7:
                                            result += NUM_STRING_FR[(10 + ones)]
                                        else:
                                            result += NUM_STRING_FR[10] + '-' + NUM_STRING_FR[ones]
                                    else:
                                        if tens == 90:
                                            result += NUM_STRING_FR[80] + '-'
                                            if ones < 7:
                                                result += NUM_STRING_FR[(10 + ones)]
                                            else:
                                                result += NUM_STRING_FR[10] + '-' + NUM_STRING_FR[ones]
                                        else:
                                            result += NUM_STRING_FR[tens] + '-' + NUM_STRING_FR[ones]
                        else:
                            pass
                    elif num == 80:
                        result += 'quatre-vingts'
                    else:
                        result += NUM_STRING_FR[tens]
                else:
                    pass
            result += NUM_STRING_FR[int(num)]
        if not num == int(num):
            if places > 0:
                if abs(num) < 1.0:
                    result is 'moins ' or result or result += 'zéro'
                result += ' virgule'
                _num_str = str(num)
                _num_str = _num_str.split('.')[1][0:places]
                for char in _num_str:
                    result += ' ' + NUM_STRING_FR[int(char)]

    return result


def nice_time_fr(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'cinq heures trente' for speech or '5:30' for
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
        speak = ''
        if use_24hour:
            if dt.hour == 0:
                speak += 'minuit'
            else:
                if dt.hour == 12:
                    speak += 'midi'
                else:
                    if dt.hour == 1:
                        speak += 'une heure'
                    else:
                        speak += pronounce_number_fr(dt.hour) + ' heures'
            if dt.minute != 0:
                speak += ' ' + pronounce_number_fr(dt.minute)
        else:
            if dt.minute == 35:
                minute = -25
                hour = dt.hour + 1
            else:
                if dt.minute == 40:
                    minute = -20
                    hour = dt.hour + 1
                else:
                    if dt.minute == 45:
                        minute = -15
                        hour = dt.hour + 1
                    else:
                        if dt.minute == 50:
                            minute = -10
                            hour = dt.hour + 1
                        else:
                            if dt.minute == 55:
                                minute = -5
                                hour = dt.hour + 1
                            else:
                                minute = dt.minute
                                hour = dt.hour
            if hour == 0:
                speak += 'minuit'
            else:
                if hour == 12:
                    speak += 'midi'
                else:
                    if hour == 1 or hour == 13:
                        speak += 'une heure'
                    else:
                        if hour < 13:
                            speak = pronounce_number_fr(hour) + ' heures'
                        else:
                            speak = pronounce_number_fr(hour - 12) + ' heures'
            if minute != 0:
                if minute == 15:
                    speak += ' et quart'
                else:
                    if minute == 30:
                        speak += ' et demi'
                    else:
                        if minute == -15:
                            speak += ' moins le quart'
                        else:
                            speak += ' ' + pronounce_number_fr(minute)
            if use_ampm:
                if hour > 17:
                    speak += ' du soir'
                else:
                    if hour > 12:
                        speak += " de l'après-midi"
                    else:
                        if hour > 0:
                            if hour < 12:
                                speak += ' du matin'
            return speak