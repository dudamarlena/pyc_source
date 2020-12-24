# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hjb/test/test_hjbmessages.py
# Compiled at: 2006-05-29 12:24:26
"""
Test Cases for various classes in hjbmessages.py
"""
import unittest
from unittest import makeSuite as make_suite
from hjb.hjbmessages import MessageReader

class Struct(object):
    __module__ = __name__

    def __init__(self, **kw):
        self.__dict__.update(kw)


class MessageReaderTest(unittest.TestCase):
    __module__ = __name__

    def test_a_single_messages_is_read_ok(self):
        response = Struct(dataread='\n        test.header=test.value\n        %\n        hello world\n        ')
        test_reader = MessageReader(response)
        messages = list(test_reader.messages())
        self.assertEquals('hello world', messages[0].payload.strip())
        self.assert_('test.header' in messages[0].headers)
        self.assertEquals('test.value', messages[0].headers['test.header'])
        self.assertEquals(1, len(messages))
        self.assertEquals(0, len(list(test_reader.messages())))

    def test_multiple_message_are_read_ok(self):
        response = Struct(dataread="test.header=test.value\n%\nhello world\n%%\ntest.header2=test.value2\n%\nhow's it goin!")
        test_reader = MessageReader(response)
        messages = list(test_reader.messages())
        self.assertEquals('hello world', messages[0].payload.strip())
        self.assert_('test.header' in messages[0].headers)
        self.assertEquals('test.value', messages[0].headers['test.header'])
        self.assertEquals("how's it goin!", messages[1].payload.strip())
        self.assert_('test.header2' in messages[1].headers)
        self.assertEquals('test.value2', messages[1].headers['test.header2'])
        self.assertEquals(2, len(messages))
        self.assertEquals(0, len(list(test_reader.messages())))


def test_suite():
    return unittest.TestSuite(tuple([ make_suite(s) for s in [MessageReaderTest] ]))


def main():
    unittest.TextTestRunner(verbosity=2).run(test_suite())


if __name__ == '__main__':
    main()