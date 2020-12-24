# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_parser.py
# Compiled at: 2020-03-05 14:33:22
import unittest, datetime
from hepdata_converter.parsers import Parser
from hepdata_converter.parsers.oldhepdata_parser import OldHEPData
from hepdata_converter.parsers.yaml_parser import YAML
from hepdata_converter.testsuite import insert_paths

class ParserTestSuite(unittest.TestCase):
    """Test suite for Parser factory class
    """

    def test_get_specific_parser_oldhepdata(self):
        self.assertEqual(Parser.get_concrete_class('oldhepdata').__class__, OldHEPData.__class__)

    def test_get_specific_parser_nonexist(self):
        self.assertRaises(ValueError, Parser.get_concrete_class, 'nonexisting_parser')

    @insert_paths('yaml/ins1283183', 'yaml/ins1397637', 'yaml/ins699647', 'yaml/ins1413748')
    def test_parse_speed(self, test_submissions):
        _yaml_parser = YAML()
        for idx, test_submission in enumerate(test_submissions):
            start_time = datetime.datetime.now()
            _yaml_parser.parse(test_submission)
            end_time = datetime.datetime.now()
            print ('Took {0}ms to parse {1}').format(end_time - start_time, test_submission)