# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_directive.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 358 bytes


def collect_directive(lines, index):
    output = []
    output.append(lines[index])
    index += 1
    while index < len(lines):
        if not lines[index] == '':
            if not lines[index].startswith(' '):
                return (
                 '\n'.join(output), index)
        output.append(lines[index])
        index += 1

    return (
     '\n'.join(output), index)