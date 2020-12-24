# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ss/tensorspace-converter/src/file_utility.py
# Compiled at: 2018-12-17 01:36:10
# Size of source mod 2**32: 791 bytes
import os

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(file_path + ' does not exist.')


def valid_file(file_path):
    if not os.path.exists(file_path):
        print(file_path + ' does not exist.')
        return False
    else:
        if not os.path.isfile(file_path):
            print(file_path + ' is not a file.')
            return False
        return True


def valid_directory(dir_path):
    if not os.path.exists(dir_path):
        print(dir_path + ' does not exist.')
        return False
    else:
        if not os.path.isdir(dir_path):
            print(dir_path + ' is not a directory.')
            return False
        return True


def show_invalid_message(msg, invalid_parameter):
    print('Aboard converting... INVALID : ' + invalid_parameter)