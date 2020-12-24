# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_literal_block.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 302 bytes


def collect_literal_block(lines, index):
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    output = []
    while index < len(lines) and (lines[index].startswith(' ') or lines[index] == ''):
        output.append(lines[index])
        index += 1

    return (
     '\n'.join(output), index)