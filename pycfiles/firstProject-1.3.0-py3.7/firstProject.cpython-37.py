# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\firstProject.py
# Compiled at: 2019-01-09 00:42:57
# Size of source mod 2**32: 480 bytes


def printLol(the_list, indent=False, level_flag=0):
    for eachLol in the_list:
        if isinstance(eachLol, list):
            printLol(eachLol, indent, level_flag + 1)
        else:
            if indent:
                for tab_stop in range(level_flag):
                    print('\t', end='')

            print(eachLol)