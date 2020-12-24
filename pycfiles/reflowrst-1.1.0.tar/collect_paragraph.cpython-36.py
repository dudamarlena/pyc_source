# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_paragraph.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 419 bytes


def collect_paragraph(lines, index):
    output = [
     lines[index]]
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    index += 1
    while index < len(lines):
        if lines[index].startswith(leading_space) and not lines[index] == '':
            output.append(lines[index].strip())
            index += 1
        else:
            return (
             ' '.join(output), index)

    return (
     ' '.join(output), index)