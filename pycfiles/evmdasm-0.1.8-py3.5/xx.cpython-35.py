# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\xx.py
# Compiled at: 2018-10-20 08:33:04
# Size of source mod 2**32: 161 bytes


class lala(list):

    def __iter__(self):
        print('ITER')
        return super().__iter__()


x = lala([1, 2, 3, 4, 5])
for i in x:
    print(x)