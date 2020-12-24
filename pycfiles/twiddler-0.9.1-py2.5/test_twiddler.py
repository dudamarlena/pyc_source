# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/tests/test_twiddler.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from searchable import SearchableTests
from zope.interface.verify import verifyObject

class TwiddlerTests(unittest.TestCase, SearchableTests):

    def setUp(self):
        from twiddler import Twiddler
        self.s = self.t = Twiddler('<moo/>')

    def test_interface(self):
        from twiddler.interfaces import ITwiddler
        verifyObject(ITwiddler, self.t)

    def test_replaced_quoting_already_quoted(self):
        self.t.setSource('<input name="test" type="text" value="" />')
        self.t['test'].replace(value='&lt;something&gt;', filters=False)
        self.assertEqual(self.t.render(), '<input name="test" type="text" value="&lt;something&gt;" />')

    def test_replaced_quotable_characters(self):
        self.t.setSource('<input name="test" type="text" value="" />')
        self.t['test'].replace(value='<something>', filters=False)
        self.assertEqual(self.t.render(), '<input name="test" type="text" value="<something>" />')

    def test_cdata_quoting(self):
        xml = '<tag><![CDATA[ <some> <more> <tags> ]]></tag>'
        self.t.setSource(xml)
        self.assertEqual(self.t.render(), xml)


def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(TwiddlerTests),))