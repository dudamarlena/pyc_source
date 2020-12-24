# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_field.py
# Compiled at: 2018-01-31 21:14:38
# Size of source mod 2**32: 1271 bytes
from .is_field import is_field
from .tools import get_field_name
from .tools import space_fill

def collect_field(lines, index, interspace):
    output = []
    words = lines[index].strip().split(' ')
    field_name, words = get_field_name(words)
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    first_line = leading_space + field_name + interspace + ' '.join(words).strip()
    output.append(first_line)
    lspace = leading_space + space_fill(len(field_name), ' ') + interspace
    index += 1
    new_lined = False
    while index < len(lines):
        if not is_field(lines, index):
            if not lines[index] == '' and lines[index].startswith(lspace):
                new_lined or output.append(lines[index].lstrip() + ' ')
            else:
                output.append(lspace + lines[index].lstrip() + ' ')
                new_lined = False
            index += 1
        elif not is_field(lines, index) and index < len(lines) - 1 and lines[(index + 1)].startswith(leading_space + ' '):
            output.append('\n')
            output.append(lines[index].lstrip())
            new_lined = True
            index += 1
        else:
            return (
             ' '.join(output), index)

    return (
     ''.join(output), index)