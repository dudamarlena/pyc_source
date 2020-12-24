# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/reflow_paragraph.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 671 bytes


def reflow_paragraph(text, space, leading_space=''):
    """
    Reflow a flattened paragraph so it fits inside horizontal
    space
    """
    words = text.split(' ')
    growing_string = leading_space
    output_list = []
    while len(words) > 0:
        if growing_string == leading_space:
            growing_string += words[0]
            words.pop(0)
        elif len(growing_string + ' ' + words[0]) <= space:
            growing_string += ' ' + words[0]
            words.pop(0)
        else:
            output_list.append(growing_string + '\n')
            growing_string = leading_space

    output_list.append(growing_string)
    return ''.join(output_list)