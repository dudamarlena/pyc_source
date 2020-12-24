# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\cazipcode-project\cazipcode\pkg\superjson\util.py
# Compiled at: 2017-07-13 17:04:39
# Size of source mod 2**32: 242 bytes


def write(s, abspath):
    with open(abspath, 'wb') as (f):
        f.write(s.encode('utf-8'))


def read(abspath):
    with open(abspath, 'rb') as (f):
        f.read().decode('utf-8')