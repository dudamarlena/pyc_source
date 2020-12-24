# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_footnote.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 475 bytes


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_footnote(lines, index):
    if not lines[index].lstrip().startswith('.. ['):
        return False
    else:
        footnote_symbols = [
         '*', '†', '‡', '§', '¶', '#', '♠', '♥', '♦', '♣']
        if lines[index].lstrip()[4] not in footnote_symbols:
            if not is_int(lines[index].lstrip()[4]):
                return False
        return True