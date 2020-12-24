# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/file_exists.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import os.path

def file_exists(file):
    return os.path.isfile(file)


def dir_exists(file):
    return os.path.isdir(file)


class FilterModule(object):
    """Returns true if the file exists"""

    def filters(self):
        return {'file_exists': file_exists, 
           'dir_exists': dir_exists}