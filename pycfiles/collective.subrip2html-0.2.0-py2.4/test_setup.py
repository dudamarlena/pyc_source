# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/subrip2html/tests/test_setup.py
# Compiled at: 2010-12-28 12:03:03
import os, unittest
from Testing import ZopeTestCase as ztc
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite(products=['collective.subrip2html'])
import collective.subrip2html
from pysrt import SubRipFile, SubRipTime

class TestCase(ptc.PloneTestCase):
    __module__ = __name__

    class layer(PloneSite):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(collective.subrip2html)
            fiveconfigure.debug_mode = False
            p = ('/').join(os.path.realpath(__file__).split(os.path.sep)[:-2])
            p = '%s/tests/test.srt' % p
            cls.test_srt_file = p

        @classmethod
        def tearDown(cls):
            pass


class TestSrt(TestCase):
    __module__ = __name__

    def test_registered(self):
        pt = self.portal.portal_transforms
        self.assertTrue(bool(pt.srt_to_html))

    def test_pysrt(self):
        test_srt = SubRipFile.open(self.layer.test_srt_file)
        self.assertEquals(test_srt[0].text, 'Eagle, say again.\nRepeat, please, Eagle.\n')
        self.assertEquals(test_srt[0].start, SubRipTime(0, 0, 13, 800))

    def test_transform(self):
        pt = self.portal.portal_transforms
        text = open(self.layer.test_srt_file).read()
        data = pt.convert('srt_to_html', text)
        html = data.getData()
        self.assertEquals(html, '<dl class="subripSection">\n<dt>00:00:13,800 &rarr; 00:00:16,700</dt>\n<dd>Eagle, say again.\nRepeat, please, Eagle.\n</dd>\n<dt>00:00:18,600 &rarr; 00:00:20,800</dt>\n<dd>Zero One Zero, can you confirm deployment?\n</dd>\n<dt>00:00:20,900 &rarr; 00:00:22,800</dt>\n<dd>Roger that, Eagle. Stand by.\n</dd>\n</dl>\n')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSrt))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')