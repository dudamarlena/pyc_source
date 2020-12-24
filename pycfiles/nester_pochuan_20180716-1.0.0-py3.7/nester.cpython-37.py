# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nester.py
# Compiled at: 2018-07-15 21:32:01
# Size of source mod 2**32: 582 bytes
"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

def print_lol(a_list, indent=False, level=0):
    """Prints each item in a list, recursively descending
       into nested lists (if necessary)."""
    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for l in range(level):
                    print('\t', end='')

            print(each_item)