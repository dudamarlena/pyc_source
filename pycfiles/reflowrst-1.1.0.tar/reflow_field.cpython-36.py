# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/reflow_field.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 904 bytes
from .tools import space_fill
from .reflow_paragraph import reflow_paragraph
from .tools import get_field_name

def reflow_field(text, space):
    output = []
    leading_space = text.replace(text.lstrip(), '')
    words = text.strip().split(' ')
    field_name, words = get_field_name(words)
    rest_of_text = text[len(leading_space + field_name):]
    interspace = rest_of_text.replace(rest_of_text.lstrip(), '')
    rest_of_text = rest_of_text.strip()
    lspace = leading_space + space_fill(len(field_name), ' ') + interspace
    blocks = rest_of_text.split('\n')
    for b in range(len(blocks)):
        blocks[b] = reflow_paragraph(blocks[b].lstrip(), space, lspace).lstrip()

    for b in range(len(blocks)):
        if b == 0:
            blocks[b] = leading_space + field_name + interspace + blocks[b]
        else:
            blocks[b] = lspace + blocks[b]

    return '\n'.join(blocks)