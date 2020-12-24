# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jsonstruct/compat.py
# Compiled at: 2013-08-09 10:47:32
try:
    set = set
except NameError:
    from sets import Set as set
    set = set

try:
    unicode = unicode
except NameError:
    unicode = str

try:
    long = long
except NameError:
    long = int