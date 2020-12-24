# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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