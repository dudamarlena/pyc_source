# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/testfiles.py
# Compiled at: 2013-04-17 04:25:02
import os
__base_dir = os.path.dirname(os.path.abspath(__file__))
__testfiles_dir = os.path.realpath(__base_dir + '/../testdata')
testfiles = {}
for file in os.listdir(__testfiles_dir):
    testfiles[file] = '%s/%s' % (__testfiles_dir, file)