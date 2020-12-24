# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\configuration.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1326 bytes
import os
__hypothesis_home_directory_default = os.path.join(os.getcwd(), '.hypothesis')
__hypothesis_home_directory = None

def set_hypothesis_home_dir(directory):
    global __hypothesis_home_directory
    __hypothesis_home_directory = directory


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def storage_directory(*names):
    global __hypothesis_home_directory
    if not __hypothesis_home_directory:
        __hypothesis_home_directory = os.getenv('HYPOTHESIS_STORAGE_DIRECTORY')
    if not __hypothesis_home_directory:
        __hypothesis_home_directory = __hypothesis_home_directory_default
    return (os.path.join)(__hypothesis_home_directory, *names)