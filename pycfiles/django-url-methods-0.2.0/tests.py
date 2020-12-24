# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Dropbox\vk\django-url-methods\urlmethods\tests.py
# Compiled at: 2014-04-29 03:32:50
import unittest, doctest, threadmethod, urlmethods

class Test(unittest.TestCase):

    def test_threadmethod(self):
        doctest.testmod(threadmethod)

    def test_urlmethods(self):
        doctest.testmod(urlmethods)