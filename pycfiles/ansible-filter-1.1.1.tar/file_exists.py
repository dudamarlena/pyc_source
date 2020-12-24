# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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