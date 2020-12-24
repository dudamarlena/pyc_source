# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/ogg/tests.py
# Compiled at: 2007-11-27 08:43:15
from zope.testing import doctestunit
import unittest

def test_suite():
    return unittest.TestSuite((doctestunit.DocTestSuite('p4a.audio.ogg._audiodata'), doctestunit.DocTestSuite('p4a.audio.ogg._player')))