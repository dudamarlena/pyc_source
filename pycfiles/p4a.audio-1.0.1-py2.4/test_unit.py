# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/audio/tests/test_unit.py
# Compiled at: 2007-11-27 10:11:31
import unittest
from zope import component
from zope.component import testing
from zope.testing import doctestunit

def test_suite():
    return unittest.TestSuite((doctestunit.DocTestSuite('p4a.audio.audioanno'), doctestunit.DocTestSuite('p4a.audio.genre'), doctestunit.DocTestSuite('p4a.audio.migration'), doctestunit.DocTestSuite('p4a.audio.utils'), doctestunit.DocTestSuite('p4a.audio.browser.audio'), doctestunit.DocTestSuite('p4a.audio.browser.media'), doctestunit.DocTestSuite('p4a.audio.browser.support'), doctestunit.DocTestSuite('p4a.audio.browser.widget'), doctestunit.DocFileSuite('p4a-audio.txt', package='p4a.audio')))