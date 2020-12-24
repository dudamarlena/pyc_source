# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/test/tools_test.py
# Compiled at: 2015-09-04 08:27:04
import unittest
from avroknife.test.tools import Tools

class ToolsTestCase(unittest.TestCase):

    @staticmethod
    def replace_according_to_map(key):
        my_map = {'simple': '/some/path/to/simple/file', 'path_with_space': '/some/path with/space', 
           'name/with/slashes': '/some/other/path'}
        return my_map[key]

    def test_replace_prefix(self):
        text = 'interesting simple path:@in:simple and some other path that follows it @in:path_with_space and some other path: @in:name/with/slashes'
        expected = 'interesting simple path:/some/path/to/simple/file and some other path that follows it /some/path with/space and some other path: /some/other/path'
        actual = Tools.replace(text, '@in:', self.replace_according_to_map)
        self.assertEqual(expected, actual)