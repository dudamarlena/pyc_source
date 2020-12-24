# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subdicts/utils.py
# Compiled at: 2014-07-11 04:57:23
import re

def parse(dictionary):
    subd = {}
    for key, value in dictionary.items():
        keys = re.split('(\\[|\\])', key)
        keys = [ x for x in keys if x not in ('[', ']', '') ]
        subd = __insert(subd, keys, value)

    return subd


def __insert(dictionary, keys, value):
    if len(keys) == 1:
        dictionary[keys[0]] = value
    elif keys[0] in dictionary:
        dictionary[keys[0]] = __insert(dictionary[keys[0]], keys[1:], value)
    else:
        dictionary[keys[0]] = __insert({}, keys[1:], value)
    return dictionary