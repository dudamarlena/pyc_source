# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/reflow_footnote.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 296 bytes
from .reflow_paragraph import reflow_paragraph

def reflow_footnote(text, space):
    leading_space = text.replace(text.lstrip(), '')
    text = text.lstrip()[2:].lstrip()
    paragraph = reflow_paragraph(text, space, leading_space + '   ')
    return leading_space + '.. ' + paragraph.lstrip()