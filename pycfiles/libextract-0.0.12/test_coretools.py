# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\rodrigo\github\libextract\libextract\tests\test_coretools.py
# Compiled at: 2015-04-09 14:24:27
from unittest import TestCase
from libextract.coretools import pipeline, histogram, above_threshold, argmax

class TestCoretools(TestCase):
    data = (
     ('i', 5),
     ('h', 7),
     ('g', 20),
     ('i', 10))

    def test_pipeline(self):
        pipe = [
         lambda x: x + 2,
         lambda x: x + 1,
         lambda x: x / 2.0]
        assert pipeline(1, pipe) == 2
        assert pipeline(2, pipe) == 2.5

    def test_histogram(self):
        hist = histogram(self.data)
        assert hist['i'] == 15
        assert hist['g'] == 20

    def test_above_threshold(self):
        func = above_threshold(7)
        assert list(func(self.data)) == [
         ('h', 7),
         ('g', 20),
         ('i', 10)]

    def test_argmax(self):
        hist = histogram(self.data)
        assert argmax(hist) == ('g', 20)