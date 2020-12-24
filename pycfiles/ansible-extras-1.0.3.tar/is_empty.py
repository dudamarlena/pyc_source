# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/is_empty.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import os.path

def is_empty(arg):
    if arg is None or str(arg).strip() is '':
        return True
    return False


class FilterModule(object):
    """Returns true if the argument is null or an empty string"""

    def filters(self):
        return {'is_empty': is_empty}