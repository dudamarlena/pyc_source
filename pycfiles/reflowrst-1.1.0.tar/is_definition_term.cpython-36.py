# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_definition_term.py
# Compiled at: 2018-01-31 21:07:44
# Size of source mod 2**32: 288 bytes


def is_definition_term(lines, index):
    """Verify if the line is a definition term"""
    if index == len(lines) - 1:
        return False
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    if lines[(index + 1)].startswith(leading_space + '  '):
        return True