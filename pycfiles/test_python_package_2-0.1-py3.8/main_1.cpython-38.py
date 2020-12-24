# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/package_example_2/subpackage_example_2/main_1.py
# Compiled at: 2020-04-12 13:52:11
# Size of source mod 2**32: 231 bytes


def echo_indented_list(item, level=0):
    for x in item:
        if isinstance(x, list):
            echo_indented_list(x, level + 1)
        else:
            print(('\t' * level + str(level) + ': -> '), end='')
            print(x)