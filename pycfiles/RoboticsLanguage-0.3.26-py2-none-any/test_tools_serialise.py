# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Tools/Tests/test_tools_serialise.py
# Compiled at: 2019-09-09 15:48:17
import unittest
from lxml import etree
from RoboticsLanguage.Tools import Serialise

class TestToolsSerialise(unittest.TestCase):

    def test_serialise(self):
        root = etree.fromstring('<root><xml name="hello"><string option="1">some text</string></xml></root>')
        xml = [ x for x in root.getchildren() ][0]
        keywords = {'xml': {'output': {'cpp': '// {{children|first}}'}}, 'string': {'output': {'cpp': '"{{text}}"'}}}
        parameters = {}
        language = 'cpp'
        Serialise.serialise(xml, parameters, keywords, language)
        self.assertEqual(Serialise.serialise(xml, parameters, keywords, language), '// "some text"')


if __name__ == '__main__':
    unittest.main()