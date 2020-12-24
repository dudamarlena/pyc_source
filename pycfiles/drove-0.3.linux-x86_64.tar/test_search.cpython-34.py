# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/command/test_search.py
# Compiled at: 2015-02-18 05:15:49
# Size of source mod 2**32: 1232 bytes
import unittest
from six import b, BytesIO
from drove.config import Config
from drove.command import search
from drove.command import CommandError
from drove.util.log import getLogger
_test_result_msg = '{\n   "results": [{"name": "none.none",\n                "url": "http://none",\n                "description": "none"}]\n}\n'
_test_result_malformed = '{}'
_test_result_empty = '{\n    "results": []\n}\n'

class TestSearchCommand(unittest.TestCase):
    index_url = 'http://localhost'

    def test_search(self, result=_test_result_msg):
        self.plugin = 'none.none'
        config = Config()
        config['plugin_dir'] = ['none']
        _urlopen = search.urllib.request.urlopen
        search.urllib.request.urlopen = lambda *a**a: BytesIO(b(result))
        try:
            search.SearchCommand(config, self, getLogger()).execute()
        finally:
            search.urllib.request.urlopen = _urlopen

    def test_search_error(self):
        with self.assertRaises(CommandError):
            self.test_search(_test_result_malformed)

    def test_search_error_empty(self):
        self.test_search(_test_result_empty)