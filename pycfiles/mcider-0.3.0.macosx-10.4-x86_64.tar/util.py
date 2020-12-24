# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ogom/.pyenv/versions/2.7.6/lib/python2.7/site-packages/mcider/util.py
# Compiled at: 2014-12-15 07:23:29
""" mcider - util
Copyright(c) 2012-2014 ogom

"""
import codecs, sys
py2k = sys.version_info < (3, 0)

def fs_reader(path):
    return codecs.open(path, mode='r', encoding='utf8').read()


def fs_writer(path, raw):
    codecs.open(path, mode='w', encoding='utf8').write(raw)