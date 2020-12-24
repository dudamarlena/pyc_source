# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alfredo/python/vguachi/guachi/guachi/tests/test_configurations.py
# Compiled at: 2010-09-22 19:52:06
import unittest
from os import remove, mkdir, path
from guachi.config import DictMatch, OptionConfigurationError

class MockDict(dict):
    pass


def setup():
    try:
        if path.exists('/tmp/guachi'):
            remove('/tmp/guachi')
        else:
            mkdir('/tmp/guachi')
    except Exception:
        pass

    txt = open('/tmp/guachi/conf.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.server_id = 2\nguachi.middleware.application = secondary\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\nguachi.db.port = 00000\n\n# Web Interface\nguachi.web.host = web.example.com\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s\n\n# Cache\nguachi.cache = 10\n    '
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_two.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.application = secondary\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\nguachi.db.port = 00000\n\n# Web Interface\nguachi.web.host = web.example.com\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    \n\n# Cache\nguachi.cache = 10\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_three.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.server_id = 2\nguachi.middleware.application = secondary\n\n# Database (Mongo)\nguachi.db.port = 00000\n\n# Web Interface\nguachi.web.host = web.example.com\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    \n\n# Cache\nguachi.cache = 10\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_four.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.server_id = 2\nguachi.middleware.application = secondary\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\n\n# Web Interface\nguachi.web.host = web.example.com\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    \n\n# Cache\nguachi.cache = 10\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_five.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.server_id = 2\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\nguachi.db.port = 00000\n\n# Web Interface\nguachi.web.host = web.example.com\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    \n\n# Cache\nguachi.cache = 10\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_six.ini', 'w')
    text = '\n[DEFAULT]\n# Middleware Configuration\nguachi.middleware.server_id = 2\nguachi.middleware.application = secondary\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\nguachi.db.port = 00000\n\n# Web Interface\nguachi.web.port = 80\n\n# Logging\nguachi.log.level = DEBUG\nguachi.log.datefmt = %H:%M:%S\nguachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    \n\n# Cache\nguachi.cache = 10\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_seven.ini', 'w')
    text = '\n[DEFAULT]\n\n# Database (Mongo)\nguachi.db.host = remote.example.com\nguachi.db.port = 0\n\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_eight.ini', 'w')
    text = '\n[DEFAULT]\n# Database (Mongo)\nguachi.db.host = example.com \nguachi.db.port = \n\n# Web Interface\nguachi.web.host = \nguachi.web.port = \n\n\n'
    txt.write(text)
    txt.close()
    txt = open('/tmp/guachi/conf_nine.ini', 'w')
    text = '\n[DEFAULT]\n# Database (Mongo)\nguachi.db.host = \nguachi.db.port = \n\n# Web Interface\nguachi.web.host = \nguachi.web.port = \n\n'
    txt.write(text)
    txt.close()


def teardown():
    try:
        remove('/tmp/guachi')
    except Exception:
        pass


class TestConfigOptions(unittest.TestCase):

    def setUp(self):
        self.mapped_options = {'guachi.db.host': 'db_host', 
           'guachi.db.port': 'db_port', 
           'guachi.web.host': 'web_host', 
           'guachi.web.port': 'web_port'}
        self.mapped_defaults = {'db_host': 'localhost', 
           'db_port': 27017, 
           'web_host': 'localhost', 
           'web_port': '8080'}

    def test_options_config_none_empty_defaults(self):
        """No config and no defaults should return an empty dict"""
        opts = DictMatch()
        actual = opts.options()
        expected = {}
        self.assertEqual(actual, expected)

    def test_options_config_invalid_empty_defaults(self):
        """Invalid config file and no defaults should return an empty dict"""
        opts = DictMatch(config='/path/to/invalid/file')
        actual = opts.options()
        expected = {}
        self.assertEqual(actual, expected)

    def test_options_config_dict_empty_defaults(self):
        """A dict config and no defaults should return an empty dict"""
        opts = DictMatch(config={})
        actual = opts.options()
        expected = {}
        self.assertEqual(actual, expected)

    def test_options_from_dict(self):
        """Pass a dict with no values and get defaults back"""
        opt = DictMatch(config={}, mapped_defaults=self.mapped_defaults)
        actual = opt.options()
        expected = self.mapped_defaults
        self.assertEqual(actual, expected)

    def test_options_dict_like_object(self):
        """Pass a dict-like object and make sure we get valid options back"""
        mock_dict = MockDict()
        opt = DictMatch(config=mock_dict, mapped_defaults=self.mapped_defaults)
        actual = opt.options()
        expected = self.mapped_defaults
        self.assertEqual(actual, expected)

    def test_options_from_file_empty_options(self):
        """A conf file with empty values should get values filled in"""
        opt = DictMatch('/tmp/guachi/conf_nine.ini', self.mapped_options, self.mapped_defaults)
        actual = opt.options()
        expected = self.mapped_defaults
        self.assertEqual(actual, expected)

    def test_options_from_file_one_option(self):
        """A conf file with one value should get values filled in"""
        opt = DictMatch('/tmp/guachi/conf_eight.ini', self.mapped_options, self.mapped_defaults)
        actual = opt.options()
        expected = {'db_host': 'example.com', 
           'db_port': 27017, 
           'web_host': 'localhost', 
           'web_port': '8080'}
        self.assertEqual(actual, expected)

    def test_options_from_file_empty_defaults(self):
        """Just one default should not overwrite other config values"""
        opt = DictMatch('/tmp/guachi/conf_eight.ini', self.mapped_options, {})
        actual = opt.options()
        expected = {'db_host': 'example.com', 
           'db_port': '', 
           'web_host': '', 
           'web_port': ''}
        self.assertEqual(actual, expected)

    def test_options_key_error_passes(self):
        """When options are missing options() passes on the KeyError"""
        opt = DictMatch('/tmp/guachi/conf_seven.ini', self.mapped_options, self.mapped_defaults)
        actual = opt.options()
        expected = {'db_host': 'remote.example.com', 
           'db_port': '0', 
           'web_host': 'localhost', 
           'web_port': '8080'}
        self.assertEqual(actual, expected)

    def test_options_from_file_raise_error(self):
        """Error out if we are passing a string in defaults"""
        opt = DictMatch('/tmp/guachi/conf_eight.ini', self.mapped_options, '')
        self.assertRaises(OptionConfigurationError, opt.options)

    def test_options_raise_error_mapped_options(self):
        """Error out if we are passing a None object in defaults"""
        opt = DictMatch('/tmp/guachi/conf_eight.ini', None, self.mapped_defaults)
        self.assertRaises(OptionConfigurationError, opt.options)
        return


if __name__ == '__main__':
    unittest.main()