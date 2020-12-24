# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/basic/prints.py
# Compiled at: 2019-02-22 23:25:00
from __future__ import print_function

def print_2d_array(dm, msg):
    print(msg)
    print('real part')
    for row in dm:
        print(('').join('%9.4f' % x.real for x in row))

    print('imag part')
    for row in dm:
        print(('').join('%9.4f' % x.imag for x in row))