# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tooth/dicts.py
# Compiled at: 2015-04-29 21:26:33
__author__ = 'Tom James Holub'

def get_key(dictionary, for_value):
    if type(dictionary) is dict:
        for key, value in dictionary.items():
            if value == for_value:
                return key

    else:
        raise TypeError('can only subtract list-list')


def join(first, second):
    added = first.copy()
    for key in second:
        if key not in added:
            added[key] = second[key]

    return added


class Dict(dict):

    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.__dict__ = self