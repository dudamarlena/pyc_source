# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/tests/testPGP.py
# Compiled at: 2012-03-06 02:26:51
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from unittest import TestCase, TestSuite, makeSuite
from Testing import ZopeTestCase
from Products.BastionCrypto.BastionPGPKeyZopeRepository import manage_addBastionPGPKeyZopeRepository
fd = open(os.path.join(os.path.dirname(__file__), 'user1', 'key.export'))
KEY = fd.read()
fd.close()
from Products.BastionCrypto import BastionPGPKey

class TestPGPRecord(TestCase):

    def testParse(self):
        key = BastionPGPKey.BastionPGPKey(KEY)
        self.failUnless(key.isValid())

    def testKey(self):
        key = BastionPGPKey.BastionPGPKey(KEY)
        self.assertEqual(key.pgpKeyId(), '846B1B0423636051')

    def testNameCommentEmail(self):
        key = BastionPGPKey.BastionPGPKey(KEY)
        self.assertEqual(key.pgpNameCommentEmail(), ('Test Dummy1', 'Head Injuries',
                                                     'testdummy1@crash.com'))

    def testStripBoundary(self):
        raw = open(os.path.join(os.path.dirname(__file__), 'user1', 'msg.txt.asc')).read()
        cooked = open(os.path.join(os.path.dirname(__file__), 'user1', 'msg.txt')).read()
        self.assertEqual(BastionPGPKey.remove_pgp_clearsign_boundary(raw), cooked)

    def testSingleLevel(self):
        raw = open(os.path.join(os.path.dirname(__file__), 'user1', 'msg.txt.asc')).read()
        self.assertEqual(BastionPGPKey.parse_signatories(raw), [('846B1B0423636051', 'Thu Mar 24 06:54:08 EST 2005')])
        self.assertEqual(BastionPGPKey.pgp_headers(raw), ('\n').join(raw.split('\n')[0:3]))
        self.assertEqual(BastionPGPKey.pgp_trailers(raw), ('\n').join(raw.split('\n')[-8:]))

    def testTwoLevel(self):
        raw = open(os.path.join(os.path.dirname(__file__), 'user2', 'msg.txt.asc')).read()
        self.assertEqual(BastionPGPKey.parse_signatories(raw), [
         ('846B1B0423636051', 'Thu Mar 24 06:54:08 EST 2005'),
         ('83B539CF93462569', 'Sat Mar 26 05:52:08 EST 2005')])
        self.assertEqual(BastionPGPKey.pgp_headers(raw), ('\n').join(raw.split('\n')[0:6]))
        self.assertEqual(BastionPGPKey.pgp_trailers(raw), ('\n').join(raw.split('\n')[-15:]))

    def testThreeLevel(self):
        raw = open(os.path.join(os.path.dirname(__file__), 'user3', 'msg.txt.asc')).read()
        self.assertEqual(BastionPGPKey.parse_signatories(raw), [
         ('846B1B0423636051', 'Thu Mar 24 06:54:08 EST 2005'),
         ('83B539CF93462569', 'Sat Mar 26 05:52:08 EST 2005'),
         ('3CC2D55DCB330EF1', 'Sat Mar 26 06:15:59 EST 2005')])
        self.assertEqual(BastionPGPKey.pgp_headers(raw), ('\n').join(raw.split('\n')[0:9]))
        self.assertEqual(BastionPGPKey.pgp_trailers(raw), ('\n').join(raw.split('\n')[-22:]))

    def testNested(self):
        pass


class TestPGPRepository(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        manage_addBastionPGPKeyZopeRepository(self.app.test_folder_1_)
        self.pks = self.app.test_folder_1_.pks

    def testCreated(self):
        self.failUnless(hasattr(self.app.test_folder_1_, 'pks'))

    def testAddKey(self):
        self.pks.add(keytext=KEY)
        key = self.pks.lookup(keyid='846B1B0423636051')
        self.failUnless(key)
        self.assertEqual(key.getId(), '846B1B0423636051')


if __name__ == '__main__':
    framework()
else:

    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestPGPRecord))
        suite.addTest(makeSuite(TestPGPRepository))
        return suite