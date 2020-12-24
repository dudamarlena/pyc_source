# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/utils/paths.py
# Compiled at: 2016-11-07 00:37:15
# Size of source mod 2**32: 325 bytes
import os

def get_running_test(test_file):
    if os.path.isfile(test_file):
        return os.path.pardir


def find_main_file(in_directory):
    """
    Find the main.json / main.yml file
    :param in_directory: the directory to search
    :return:
    """
    if os.path.isdir(in_directory):
        pass