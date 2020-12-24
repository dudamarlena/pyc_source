# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\tests\test_text.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.util.text import validate_id, getFirstSentence
import unittest

class TextUtilTest(unittest.TestCase):
    """
    """

    def test_validateId(self):
        """
        """
        good = 'aValidId_1'
        bad0 = ''
        self.assertEquals(validate_id(good), good)
        self.assertRaises(ValueError, validate_id, bad0)

    def test_getFirstSentence(self):
        """
        """
        original = ' muh. '
        expected = 'muh.'
        self.assertEquals(getFirstSentence(original), expected)
        original = '\n            muh maeh. blub\n        '
        expected = 'muh maeh.'
        self.assertEquals(getFirstSentence(original), expected)
        original = 'muh.maeh.blub.'
        expected = 'muh.'
        self.assertEquals(getFirstSentence(original), expected)
        original = 'm' * 600
        expected = 'm' * 255
        self.assertEquals(getFirstSentence(original), expected)
        original = 'm' * 600
        expected = 'mmmmm'
        self.assertEquals(getFirstSentence(original, 5), expected)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TextUtilTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')