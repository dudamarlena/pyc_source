# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmiedema/.pyenv/versions/3.6.0/lib/python3.6/site-packages/holdmybeer/operations.py
# Compiled at: 2017-03-28 16:38:34
# Size of source mod 2**32: 273 bytes


def flow(contenttype, source, destination, amount):
    splitoff = source.take(contenttype, amount)
    try:
        destination.give(contenttype, amount, splitoff.value)
    except:
        source.give(contenttype, amount, splitoff.value)
        raise