# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/test_util.py
# Compiled at: 2017-12-04 07:19:32
import io, textwrap, six
from six.moves import configparser
import sys
from pbr.tests import base
from pbr import util

class TestExtrasRequireParsingScenarios(base.BaseTestCase):
    scenarios = [
     (
      'simple_extras',
      {'config_text': '\n                [extras]\n                first =\n                    foo\n                    bar==1.0\n                second =\n                    baz>=3.2\n                    foo\n                ', 
         'expected_extra_requires': {'first': ['foo', 'bar==1.0'], 'second': [
                                              'baz>=3.2', 'foo']}}),
     (
      'with_markers',
      {'config_text': "\n                [extras]\n                test =\n                    foo:python_version=='2.6'\n                    bar\n                    baz<1.6 :python_version=='2.6'\n                    zaz :python_version>'1.0'\n                ", 
         'expected_extra_requires': {"test:(python_version=='2.6')": [
                                                                    'foo', 'baz<1.6'], 
                                     'test': [
                                            'bar', 'zaz']}}),
     (
      'no_extras',
      {'config_text': '\n            [metadata]\n            long_description = foo\n            ', 
         'expected_extra_requires': {}})]

    def config_from_ini(self, ini):
        config = {}
        if sys.version_info >= (3, 2):
            parser = configparser.ConfigParser()
        else:
            parser = configparser.SafeConfigParser()
        ini = textwrap.dedent(six.u(ini))
        parser.readfp(io.StringIO(ini))
        for section in parser.sections():
            config[section] = dict(parser.items(section))

        return config

    def test_extras_parsing(self):
        config = self.config_from_ini(self.config_text)
        kwargs = util.setup_cfg_to_setup_kwargs(config)
        self.assertEqual(self.expected_extra_requires, kwargs['extras_require'])


class TestInvalidMarkers(base.BaseTestCase):

    def test_invalid_marker_raises_error(self):
        config = {'extras': {'test': "foo :bad_marker>'1.0'"}}
        self.assertRaises(SyntaxError, util.setup_cfg_to_setup_kwargs, config)