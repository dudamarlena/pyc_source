# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/reflow_bullet_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 897 bytes


def reflow_bullet_list_item(text, space):
    """
    reflow a bullet list item
    """
    if space == 0:
        return text
    else:
        leading_space = text.replace(text.lstrip(), '')
        line = text.lstrip()
        words = line.split(' ')
        growing_string = leading_space
        output_list = []
        while len(words) > 0:
            if len(growing_string) == len(leading_space):
                growing_string += words[0]
                words.pop(0)
            elif len(growing_string) == len(leading_space) + 1:
                growing_string += ' ' + words[0]
                words.pop(0)
            elif len(growing_string + ' ' + words[0]) <= space:
                growing_string += ' ' + words[0]
                words.pop(0)
            else:
                output_list.append(growing_string + '\n')
                growing_string = leading_space + ' '

        output_list.append(growing_string + '\n')
        return ''.join(output_list).rstrip()