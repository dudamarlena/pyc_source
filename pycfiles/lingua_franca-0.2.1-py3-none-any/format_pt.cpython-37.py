# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_pt.py
# Compiled at: 2019-12-23 02:55:06
# Size of source mod 2**32: 6870 bytes
from lingua_franca.lang.format_common import convert_to_mixed_fraction
from lingua_franca.lang.common_data_pt import _FRACTION_STRING_PT, _NUM_STRING_PT

def nice_number_pt(number, speech, denominators=range(1, 21)):
    """ Portuguese helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e meio" for speech and "4 1/2" for text

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
                den_str = _FRACTION_STRING_PT[den]
                if whole == 0:
                    if num == 1:
                        return_string = 'um {}'.format(den_str)
            else:
                return_string = '{} {}'.format(num, den_str)
        elif num == 1:
            return_string = '{} e {}'.format(whole, den_str)
        else:
            return_string = '{} e {} {}'.format(whole, num, den_str)
    if num > 1:
        return_string += 's'
    return return_string


def pronounce_number_pt(num, places=2):
    """
    Convert a number to it's spoken equivalent
     For example, '5.2' would return 'cinco virgula dois'
     Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(num) >= 100:
        return str(num)
        result = ''
        if num < 0:
            result = 'menos '
        num = abs(num)
        if num >= 20:
            tens = int(num - int(num) % 10)
            ones = int(num - tens)
            result += _NUM_STRING_PT[tens]
            if ones > 0:
                result += ' e ' + _NUM_STRING_PT[ones]
    else:
        result += _NUM_STRING_PT[int(num)]
    if not num == int(num):
        if places > 0:
            result += ' vírgula'
            place = 10
            while int(num * place) % 10 > 0 and places > 0:
                result += ' ' + _NUM_STRING_PT[(int(num * place) % 10)]
                place *= 10
                places -= 1

    return result


def nice_time_pt(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format
     For example, generate 'cinco treinta' for speech or '5:30' for
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
            if dt.hour == 1:
                speak += 'uma'
            else:
                speak += pronounce_number_pt(dt.hour)
            if dt.minute > 0:
                speak += ' e ' + pronounce_number_pt(dt.minute)
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
                speak += 'meia noite'
            else:
                if hour == 12:
                    speak += 'meio dia'
                else:
                    if hour == 1 or hour == 13:
                        speak += 'uma'
                    else:
                        if hour == 2 or hour == 14:
                            speak += 'duas'
                        else:
                            if hour < 13:
                                speak = pronounce_number_pt(hour)
                            else:
                                speak = pronounce_number_pt(hour - 12)
            if minute != 0:
                if minute == 15:
                    speak += ' e um quarto'
                else:
                    if minute == 30:
                        speak += ' e meia'
                    else:
                        if minute == -15:
                            speak += ' menos um quarto'
                        else:
                            if minute > 0:
                                speak += ' e ' + pronounce_number_pt(minute)
                            else:
                                speak += ' ' + pronounce_number_pt(minute)
            if minute == 0:
                if not use_ampm:
                    speak += ' em ponto'
                if use_ampm:
                    if hour > 0 and hour < 6:
                        speak += ' da madrugada'
            elif hour >= 6 and hour < 12:
                speak += ' da manhã'
            else:
                if hour >= 13 and hour < 21:
                    speak += ' da tarde'
                else:
                    if hour != 0:
                        if hour != 12:
                            speak += ' da noite'
            return speak