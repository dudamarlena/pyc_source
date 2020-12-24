# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_gridtable.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 296 bytes


def collect_gridtable(lines, index):
    output = []
    while index < len(lines) and (lines[index].lstrip().startswith('+') or lines[index].lstrip().startswith('|')):
        output.append(lines[index])
        index += 1

    return (
     '\n'.join(output), index)