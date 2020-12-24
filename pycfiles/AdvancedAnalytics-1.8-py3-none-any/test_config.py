# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/tests/test_config.py
# Compiled at: 2015-07-22 05:24:08
import unittest, os
from advanced_ssh_config.config import Config
from advanced_ssh_config.exceptions import ConfigError
from . import set_config, prepare_config, write_config, PREFIX, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):

    def setUp(self):
        prepare_config()

    def test_initialize_config(self):
        config = Config([DEFAULT_CONFIG])
        self.assertIsInstance(config, Config)

    def test_include_existing_files(self):
        write_config('', name='include-1')
        write_config('', name='include-2')
        contents = '\n[default]\nIncludes = {0}/include-1 {0}/include-2\n'
        config = set_config(contents)
        self.assertEquals(config.loaded_files, [
         DEFAULT_CONFIG,
         ('{}/include-1').format(PREFIX),
         ('{}/include-2').format(PREFIX)])

    def test_include_glob(self):
        write_config('', name='include-1.conf')
        write_config('', name='include-2.conf')
        write_config('', name='include-3')
        write_config('', name='include-4.conf')
        contents = '\n[default]\nIncludes = {0}/*.conf\n'
        config = set_config(contents)
        self.assertEquals(sorted(config.loaded_files), sorted([
         DEFAULT_CONFIG,
         ('{}/include-1.conf').format(PREFIX),
         ('{}/include-2.conf').format(PREFIX),
         ('{}/include-4.conf').format(PREFIX)]))
        contents = '\n[default]\nIncludes = {0}/*\n'
        config = set_config(contents)
        self.assertEquals(sorted(config.loaded_files), [
         DEFAULT_CONFIG,
         ('{}/include-1.conf').format(PREFIX),
         ('{}/include-2.conf').format(PREFIX),
         ('{}/include-3').format(PREFIX),
         ('{}/include-4.conf').format(PREFIX)])

    def test_sections_simple(self):
        contents = '\n[hosta]\n[default]\n'
        config = set_config(contents)
        self.assertEquals(config.sections, ['default', 'hosta'])

    def test_sections_with_double(self):
        contents = '\n[hosta]\n[hosta]\n[default]\n'
        config = set_config(contents)
        self.assertEquals(config.sections, ['default', 'hosta'])

    def test_sections_with_case(self):
        contents = '\n[hosta]\n[hostA]\n[default]\n'
        config = set_config(contents)
        self.assertEquals(config.sections, ['default', 'hostA', 'hosta'])

    def test_sections_with_regex(self):
        contents = '\n[hosta]\n[host.*]\n[default]\n'
        config = set_config(contents)
        self.assertEquals(config.sections, ['default', 'host.*', 'hosta'])

    def test_get_simple(self):
        contents = '\n[hosta]\nhostname = 1.2.3.4\n'
        config = set_config(contents)
        self.assertEquals(config.get('Hostname', 'hosta'), '1.2.3.4')
        self.assertEquals(config.get('hostname', 'hosta'), '1.2.3.4')

    def test_get_key_not_found(self):
        contents = '\n[hosta]\n'
        config = set_config(contents)
        self.assertEquals(config.get('Hostname', 'hosta'), None)
        self.assertEquals(config.get('Hostname', 'hosta', 'localhost'), 'localhost')
        return

    def test_get_host_not_found(self):
        contents = '\n[default]\nport = 22\n'
        config = set_config(contents)
        self.assertEquals(config.get('Port', 'hosta'), '22')

    def test_get_host_and_key_not_found(self):
        config = set_config('')
        self.assertEquals(config.get('Port', 'hosta'), None)
        return

    def test_host_wildcard(self):
        contents = '\n[aaa.*]\nport = 25\n\n[.*bbb]\nport = 24\n\n[ccc.*ddd]\nport = 23\n\n[.*eee.*]\nport = 22\n\n[default]\nport = 21\n'
        config = set_config(contents)
        self.assertEquals(config.get('Port', 'aaa'), '25')
        self.assertEquals(config.get('Port', 'aaa42'), '25')
        self.assertEquals(config.get('Port', '42aaa'), '21')
        self.assertEquals(config.get('Port', 'bbb'), '24')
        self.assertEquals(config.get('Port', 'bbb42'), '24')
        self.assertEquals(config.get('Port', '42bbb'), '24')
        self.assertEquals(config.get('Port', 'cccddd'), '23')
        self.assertEquals(config.get('Port', 'ccc42ddd'), '23')
        self.assertEquals(config.get('Port', 'eee'), '22')
        self.assertEquals(config.get('Port', '42eee'), '22')
        self.assertEquals(config.get('Port', 'eee42'), '22')
        self.assertEquals(config.get('Port', '42eee42'), '22')

    def test_host_invalid_wildcard(self):
        contents = '\n[aaa.+]\nport = 25\n'
        set_config(contents, load=False)
        self.assertRaises(ConfigError, Config, [DEFAULT_CONFIG])

    def test_multiple_line(self):
        contents = '\n[test]\nlocalforward = 1 test 2 \n 2 test 3\n'
        config = set_config(contents)
        self.assertEquals(config.get('localforward', 'test'), ['1 test 2', '2 test 3'])

    def test_one_line_list(self):
        contents = '\n[test]\nlocalforward = 1 test 2\n'
        config = set_config(contents)
        self.assertEquals(config.get('localforward', 'test'), ['1 test 2'])