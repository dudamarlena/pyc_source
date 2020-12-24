# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/goncalopp/private/mydocs/programacao/python/mexbtcapi/mexbtcapi/util/constant_generator.py
# Compiled at: 2012-09-28 22:09:50


def constant_generator(locals_dictionary, keys, values=None):
    """given the locals(), a string list ( keys - a list of names of 
    constants), and their values, this function assigns each constant 
    it's value (or an integer, if values=None) and registers them as 
    variables"""
    if values == None:
        values = range(len(keys))
    forward = dict(zip(keys, values))
    reverse = keys
    locals_dictionary['list'] = reverse
    locals_dictionary.update(forward)
    return