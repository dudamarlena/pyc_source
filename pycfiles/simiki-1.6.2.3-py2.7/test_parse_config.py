# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tests/test_parse_config.py
# Compiled at: 2017-06-02 11:17:28
from __future__ import unicode_literals
import os.path, unittest, datetime
from simiki.config import parse_config, get_default_config
test_path = os.path.dirname(os.path.abspath(__file__))

class TestParseConfig(unittest.TestCase):

    def setUp(self):
        wiki_path = os.path.join(test_path, b'mywiki_for_others')
        self.expected_config = get_default_config()
        self.expected_config.update({b'author': b'Tanky Woo', 
           b'debug': True, 
           b'default_ext': b'markdown', 
           b'description': b"This is a simiki's config sample, 测试样例", 
           b'destination': b'destination', 
           b'keywords': b'wiki, simiki, python, 维基', 
           b'root': b'/wiki/', 
           b'source': b'source', 
           b'attach': b'attach', 
           b'theme': b'mytheme', 
           b'themes_dir': b'simiki_themes', 
           b'title': b'我的Wiki', 
           b'url': b'http://wiki.tankywoo.com'})
        self.config_file = os.path.join(wiki_path, b'config_sample.yml')

    def test_parse_config(self):
        config = parse_config(self.config_file)
        self.expected_config.pop(b'time')
        _date = config.pop(b'time')
        if hasattr(unittest.TestCase, b'assertIsInstance'):
            self.assertIsInstance(_date, datetime.datetime)
        else:
            assert isinstance(_date, datetime.datetime), b'%s is not an instance of %r' % (
             repr(_date), datetime.datetime)
        self.assertEqual(config, self.expected_config)

    def test_parse_config_not_exist(self):
        not_exist_config_file = os.path.join(self.config_file, b'not_exist')
        self.assertRaises(Exception, lambda : parse_config(not_exist_config_file))


if __name__ == b'__main__':
    unittest.main()