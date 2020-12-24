# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\test\run.py
# Compiled at: 2017-12-11 20:12:50
import unittest, os.path

def load_tests():
    start_dir = os.path.split(__file__)[0]
    top_level = os.path.normpath(os.path.join(start_dir, '../..'))
    l = unittest.TestLoader()
    t = l.discover(start_dir, top_level_dir=top_level)
    return t