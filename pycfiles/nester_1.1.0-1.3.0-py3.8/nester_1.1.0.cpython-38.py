# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\nester_1.1.0.py
# Compiled at: 2020-02-22 20:52:10
# Size of source mod 2**32: 737 bytes
"""This is the nester.py module, and it provides one function called
    print_list() which prints lists that may or may not include nested lists."""

def print_list(the_list, indent=False, level=0):
    """This function takes a positional argument called “the_list", which is any
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line."""
    for each_items in the_list:
        if isinstance(each_items, list):
            print_list(each_items, indent, level=1)
        elif indent:
            for tab_stop in range(level):
                print('\t', end='')
            else:
                print(each_items)