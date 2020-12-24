# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/random.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 1330 bytes
"""randomisation functions"""
from re import search
try:
    from os import urandom as getrandom
except ImportError:
    from random import random as urandom

    def getrandom():
        return urandom()


def random(limit=10, regex='[\\w -~]'):
    """random character by limit"""
    rets = []
    while 1:
        try:
            out = getrandom(1)
        except UnicodeDecodeError as err:
            continue

        try:
            out = out.decode('utf-8')
        except (AttributeError, UnicodeDecodeError) as err:
            continue

        try:
            if search(regex, out).group(0):
                rets.append(out.strip())
        except AttributeError:
            continue

        if len(''.join(rets)) >= int(limit):
            break

    return ''.join(r for r in rets)


def biggerrand(num):
    """greater random number"""
    while 1:
        try:
            g = int(random((int(len(str(num)) + 1)), regex='[0-9]*'))
        except ValueError:
            continue

        if g > int(num):
            break

    return g


def lowerrand(num):
    """lower random number"""
    while 1:
        try:
            g = int(random((int(len(str(num)))), regex='[0-9]*'))
        except ValueError:
            continue

        if g > 1:
            if g < int(num):
                break

    return g


def randin(top, low=0):
    """number in between low and top"""
    if low:
        low, top = top, low
    while 1:
        try:
            g = int(random((int(len(str(top)))), regex='[0-9]*'))
        except ValueError:
            continue

        if g > int(low):
            if g < int(top):
                break

    return g