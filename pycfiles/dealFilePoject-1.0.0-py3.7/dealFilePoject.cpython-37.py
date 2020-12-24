# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dealFilePoject.py
# Compiled at: 2019-01-10 22:07:59
# Size of source mod 2**32: 2490 bytes
import sys

def printLol(the_list, indent=False, level_flag=0, file_dir=sys.stdout):
    for eachLol in the_list:
        if isinstance(eachLol, list):
            printLol(eachLol, indent, level_flag + 1, file_dir)
        else:
            if indent:
                for tab_stop in range(level_flag):
                    print('\t', end='', file=file_dir)

            print(eachLol, file=file_dir)


import os
os.chdir('E:\\WORK_SPACE\\workspace_for_python\\DataInfo\\firstFile')
man = []
other = []
try:
    data = open('sketch.txt')
    for each_line in data:
        try:
            person, spoken = each_line.split(':', 1)
            spoken = spoken.strip()
            if person == 'Man':
                man.append(spoken)
            else:
                if person == 'Other Man':
                    other.append(spoken)
        except ValueError:
            pass

    data.close()
except IOError as fileErr:
    try:
        print('Open file error: ' + str(fileErr))
    finally:
        fileErr = None
        del fileErr

try:
    with open('man_data.txt', 'w') as (man_out):
        with open('other_data.txt', 'w') as (other_out):
            printLol(man, True, 1, man_out)
            printLol(other, True, 1, other_out)
except IOError as err:
    try:
        print('Write file error: ' + str(err))
    finally:
        err = None
        del err