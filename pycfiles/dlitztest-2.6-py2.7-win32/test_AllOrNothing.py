# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Protocol\test_AllOrNothing.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
import unittest
from Crypto.Protocol import AllOrNothing
from Crypto.Util.py3compat import *
text = b("When in the Course of human events, it becomes necessary for one people to\ndissolve the political bands which have connected them with another, and to\nassume among the powers of the earth, the separate and equal station to which\nthe Laws of Nature and of Nature's God entitle them, a decent respect to the\nopinions of mankind requires that they should declare the causes which impel\nthem to the separation.\n\nWe hold these truths to be self-evident, that all men are created equal, that\nthey are endowed by their Creator with certain unalienable Rights, that among\nthese are Life, Liberty, and the pursuit of Happiness. That to secure these\nrights, Governments are instituted among Men, deriving their just powers from\nthe consent of the governed. That whenever any Form of Government becomes\ndestructive of these ends, it is the Right of the People to alter or to\nabolish it, and to institute new Government, laying its foundation on such\nprinciples and organizing its powers in such form, as to them shall seem most\nlikely to effect their Safety and Happiness.\n")

class AllOrNothingTest(unittest.TestCase):

    def runTest(self):
        """Simple test of AllOrNothing"""
        from Crypto.Cipher import AES
        import base64
        for i in range(50):
            x = AllOrNothing.AllOrNothing(AES)
            msgblocks = x.digest(text)
            y = AllOrNothing.AllOrNothing(AES)
            text2 = y.undigest(msgblocks)
            self.assertEqual(text, text2)


def get_tests(config={}):
    return [AllOrNothingTest()]


if __name__ == '__main__':
    unittest.main()