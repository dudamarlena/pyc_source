# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\strings.py
# Compiled at: 2020-04-06 12:55:33
# Size of source mod 2**32: 388 bytes
"""String"""
import pprint

def nicely_print(dictionary, print=True):
    """Prints the nicely formatted dictionary - shaonutil.strings.nicely_print(object)"""
    if print:
        pprint.pprint(dictionary)
    return pprint.pformat(dictionary)


def change_dic_key(dic, old_key, new_key):
    """Change dictionary key with new key"""
    dic[new_key] = dic.pop(old_key)
    return dic