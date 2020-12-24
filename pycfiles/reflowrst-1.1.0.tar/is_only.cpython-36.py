# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/is_only.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 297 bytes


def is_only(text, char_list):
    """
    return true if the text is made up of only the characters in char
    list
    """
    text = text.strip()
    if text == '':
        return False
    else:
        for i in range(len(text)):
            if text[i] not in char_list:
                return False

        return True