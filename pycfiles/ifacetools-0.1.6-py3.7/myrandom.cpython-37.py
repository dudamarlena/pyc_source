# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\myrandom.py
# Compiled at: 2019-08-04 22:14:48
# Size of source mod 2**32: 595 bytes
import random, uuid

def randomStr(num=1):
    ri = randomInt()
    s = ''
    for i in range(num):
        s = s + str(ri())

    return s


def randomInt():
    return lambda a=0, b=9: random.randint(a, b)


def uuidWithHyphen():
    return str(uuid.uuid4())


def uuidAfterReplace():
    s = uuidWithHyphen()
    return s.replace('-', '')