# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_bullet_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 270 bytes


def is_bullet_list_item(lines, index):
    """check if it's a bullet list item"""
    bullets = [
     '*', '-', '+', '•', '‣', '⁃']
    first_char = lines[index].lstrip().split(' ')[0]
    if first_char in bullets:
        return True
    else:
        return False