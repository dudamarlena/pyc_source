# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\pkg\superjson\util.py
# Compiled at: 2017-07-13 17:04:39
# Size of source mod 2**32: 242 bytes


def write(s, abspath):
    with open(abspath, 'wb') as (f):
        f.write(s.encode('utf-8'))


def read(abspath):
    with open(abspath, 'rb') as (f):
        f.read().decode('utf-8')