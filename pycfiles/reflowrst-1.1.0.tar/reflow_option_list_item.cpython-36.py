# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/reflow_option_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 765 bytes
from .reflow_paragraph import reflow_paragraph
from .tools import space_fill

def reflow_option_list_item(text, space):
    leading_space = text.replace(text.lstrip(), '')
    option = text.lstrip().split('  ')[0]
    rest_of_text = text.lstrip()[len(option):]
    interspace = rest_of_text.replace(rest_of_text.lstrip(), '')
    lspace = leading_space + space_fill(len(option), ' ') + interspace
    blocks = rest_of_text.split('\n')
    for b in range(len(blocks)):
        blocks[b] = reflow_paragraph(blocks[b].lstrip(), space, lspace).lstrip()

    for b in range(len(blocks)):
        if b == 0:
            blocks[b] = leading_space + option + interspace + blocks[b]
        else:
            blocks[b] = lspace + blocks[b]

    return '\n'.join(blocks)