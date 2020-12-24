# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/basic/prints.py
# Compiled at: 2019-02-26 10:11:51
# Size of source mod 2**32: 240 bytes


def print_2d_array(dm, msg):
    print(msg)
    print('real part')
    for row in dm:
        print(''.join(('%9.4f' % x.real for x in row)))

    print('imag part')
    for row in dm:
        print(''.join(('%9.4f' % x.imag for x in row)))