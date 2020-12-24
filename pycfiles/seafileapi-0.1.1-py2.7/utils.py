# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/tests/utils.py
# Compiled at: 2014-11-09 11:12:37
import os, string, random

def randstring(length=12):
    return ('').join(random.choice(string.lowercase) for i in range(length))


def datafile(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)


def filesize(path):
    return os.stat(path).st_size