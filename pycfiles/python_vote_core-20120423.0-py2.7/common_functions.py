# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyvotecore/common_functions.py
# Compiled at: 2012-04-23 20:44:05


def matching_keys(dict, target_value):
    return set([ key for key, value in dict.iteritems() if value == target_value
               ])


def unique_permutations(xs):
    if len(xs) < 2:
        yield xs
    else:
        h = []
        for x in xs:
            h.append(x)
            if x in h[:-1]:
                continue
            ts = xs[:]
            ts.remove(x)
            for ps in unique_permutations(ts):
                yield [
                 x] + ps