# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/split.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re

def split_string(string, separator=' '):
    return string.split(separator)


def split_regex(string, separator_pattern='\\s+'):
    return re.split(separator_pattern, string)


class FilterModule(object):
    """ A filter to split a string into a list. """

    def filters(self):
        return {'split': split_string, 
           'split_regex': split_regex}