# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/test/test_codecs.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.util.codecs"""
__docformat__ = 'restructuredtext'
import copy, unittest
from taurus.test import insertTest
from taurus.core.util.codecs import CodecFactory
import numpy

@insertTest(helper_name='encDec', cname='json', data=[1, 2, 3])
@insertTest(helper_name='encDec', cname='zip', data='foobar')
@insertTest(helper_name='encDec', cname='zip_utf8_json', data=[1, 2, 3])
@insertTest(helper_name='encDec', cname='videoimage', data=numpy.ones((2, 2), dtype='uint8'))
@insertTest(helper_name='encDec', cname='zip_null_zip_videoimage', data=numpy.ones((2,
                                                                                    2), dtype='uint8'))
@insertTest(helper_name='dec', cname='videoimage', data='VDEO\x00\x01\x00\x07\x00\x00\x00\x00\x00\x00\x00' + '\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00 ' + '\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01' + '\x01\x01\x01\x01\x01\x01\x01\x01', expected=numpy.ones((2,
                                                                                                                                                                                                                                                                                 2,
                                                                                                                                                                                                                                                                                 3), dtype='uint8'))
class CodecTest(unittest.TestCase):
    """TestCase for checking codecs"""

    def encDec(self, cname=None, data=None, expected=None):
        """Check that data can be encoded-decoded properly"""
        if expected is None:
            expected = copy.deepcopy(data)
        _, enc = self.enc(cname=cname, data=data)
        self.dec(cname=cname, data=enc, expected=expected)
        return

    def enc(self, cname=None, data=None, expected=None):
        """Check that data can be encoded-decoded properly"""
        cf = CodecFactory()
        codec = cf.getCodec(cname)
        fmt, enc = codec.encode(('', data))
        if expected is not None:
            msg = ('Wrong data after encoding with %s:\n' + ' -expected:%s\n -obtained:%s') % (cname, expected, enc)
            if numpy.isscalar(expected):
                equal = enc == expected
            else:
                equal = numpy.all(enc == expected)
            self.assertTrue(equal, msg)
        return (
         fmt, enc)

    def dec(self, cname=None, data=None, expected=None):
        """Check that data can be encoded-decoded properly"""
        cf = CodecFactory()
        codec = cf.getCodec(cname)
        fmt, dec = codec.decode((cname, data))
        if expected is not None:
            msg = ('Wrong data after decoding with %s:\n' + ' -expected:%s\n -obtained:%s') % (cname, expected, dec)
            if numpy.isscalar(expected):
                equal = dec == expected
            else:
                equal = numpy.all(dec == expected)
            self.assertTrue(equal, msg)
        return (
         fmt, dec)


if __name__ == '__main__':
    pass