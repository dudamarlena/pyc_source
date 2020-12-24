# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_simple_table.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 460 bytes
from .tools import simple2data
from .tools import data2simplerst

def collect_simple_table(lines, index):
    output = []
    top_line = lines[index]
    while index < len(lines) and not lines[index] == '':
        output.append(lines[index])
        index += 1

    text = '\n'.join(output)
    table, spans, use_headers, headers_row = simple2data(text)
    simple_table = data2simplerst(table, spans, use_headers, headers_row)
    return (
     simple_table, index)