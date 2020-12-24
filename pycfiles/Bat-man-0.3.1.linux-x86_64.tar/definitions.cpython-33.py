# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.3/site-packages/batman/definitions.py
# Compiled at: 2014-02-04 17:41:10
# Size of source mod 2**32: 844 bytes
import sys, os, logging
logging.basicConfig(level=logging.INFO)
VERSION = '0.3'
if getattr(sys, 'frozen', False):
    CURRENT_PATH = os.path.join(os.path.dirname(os.path.realpath(sys.executable)), 'batman')
else:
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
WINDOWS = sys.platform.startswith('win')

def path_with(*args):
    return os.path.join(CURRENT_PATH, *args)


try:
    os.mkdir(os.path.expanduser('~/.batman'))
except OSError:
    pass

def get_user_data_folder():
    if not WINDOWS:
        return os.path.expanduser('~/.batman')


def get_user_data_folder_with(*args):
    return os.path.join(get_user_data_folder(), *args)