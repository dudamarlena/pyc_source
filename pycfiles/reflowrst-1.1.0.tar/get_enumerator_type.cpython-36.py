# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/get_enumerator_type.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 1386 bytes


def get_enumerator_type(enumerator):
    """
    Define the type of enumerator

    An enumerator may be hashtag, arabic, alpha, or roman
    upper or lower
    period, full_parenthesis, or right_parenthesis

    For example: "II)" is an  ["roman", "upper", "right_parenthesis"]
    """
    output = []
    if enumerator.endswith('.'):
        output.append('period')
        enumerator = enumerator[0:-1]
    else:
        if enumerator.startswith('('):
            output.append('full_parenthesis')
            enumerator = enumerator[1:-1]
        else:
            output.append('right_parenthesis')
            enumerator = enumerator[0:-1]
    try:
        int(enumerator)
        output.append('arabic')
    except ValueError:
        if enumerator == '#':
            output.append('hashtag')
        else:
            if enumerator.lower() == 'i':
                output.append('roman')
                if enumerator.isupper():
                    output.append('upper')
                else:
                    output.append('lower')
            else:
                if len(enumerator) == 1:
                    output.append('alpha')
                    if enumerator.isupper():
                        output.append('upper')
                    else:
                        output.append('lower')
                else:
                    output.append('roman')
                    if enumerator.isupper():
                        output.append('upper')
                    else:
                        output.append('lower')

    return output