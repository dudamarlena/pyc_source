# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/collect_option_list_item.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 1048 bytes
from .is_option_list_item import is_option_list_item
from .tools import space_fill

def collect_option_list_item(lines, index, interspace):
    output = []
    leading_space = lines[index].replace(lines[index].lstrip(), '')
    option = lines[index].lstrip().split('  ')[0]
    lspace = leading_space + space_fill(len(option), ' ') + '  '
    rest_of_text = lines[index].lstrip()[len(option):].lstrip()
    output.append(leading_space + option + interspace + rest_of_text)
    index += 1
    while index < len(lines):
        if not is_option_list_item(lines, index):
            if not lines[index] == '':
                output.append(lines[index].lstrip())
                index += 1
            else:
                if index < len(lines) - 1 and lines[(index + 1)].startswith(lspace):
                    output.append('\n\n')
                    output.append(lspace + lines[index])
                    index += 1
                else:
                    return (
                     ' '.join(output), index)
        else:
            return (
             ' '.join(output), index)

    return (
     ' '.join(output), index)