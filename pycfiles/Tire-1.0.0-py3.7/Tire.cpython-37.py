# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Tire.py
# Compiled at: 2019-03-16 09:43:24
# Size of source mod 2**32: 247 bytes


def Tire():
    s = input()
    s1 = sorted(s)
    s2 = list(set(s1))
    s2 = sorted(s2)
    dict2 = {s2[i]:s1.count(s2[i]) for i in range(len(s2))}
    dict1 = sorted(dict2, key=(dict2.get), reverse=True)[0:3]
    print(dict1)


print(Tire())