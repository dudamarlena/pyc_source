# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nester_pasaribu.py
# Compiled at: 2020-04-12 01:46:10
# Size of source mod 2**32: 566 bytes
"""This is the "nester.py" module, and it provides on function called
print_lol() which prints lists that may or may nit include nested lists."""

def print_lol(the_list):
    """This function takes a positional argument called "the_list",
    which is any Python list (of, possibly, nested lists). Each data
    item in the provided list is (recursively) printed to the screen on
    its own line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)