# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/user/D/projects/github/pygetwallpapers/pygetwallpapers/pgw_tools/functions.py
# Compiled at: 2016-11-23 14:13:16
import sys, os, pprint, re

def ru(self, s='', e='utf-8'):
    try:
        s = s.encode(e)
    except:
        return s

    return s


def exit(self, code=0):
    sys.exit(code)


def chunks(array=[], chunk_size=5):
    for i in xrange(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


def print_(s='', mode=True):
    if mode == True:
        pprint.pprint(s)
    else:
        try:
            print s
        except:
            print s


def mkdirp(*args):
    directory = os.path.join(*args)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory