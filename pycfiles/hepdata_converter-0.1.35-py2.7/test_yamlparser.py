# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_yamlparser.py
# Compiled at: 2020-03-05 14:33:22
import hepdata_converter
from hepdata_converter.testsuite import insert_path, insert_data_as_str
from hepdata_converter.testsuite.test_writer import WriterTestSuite
__author__ = 'Michał Szostak'

class YAMLWriterTestSuite(WriterTestSuite):

    @insert_path('yaml_qual')
    @insert_data_as_str('csv/table_5_noqual.csv')
    def test_no_qal_parse(self, yaml_path, table_5_noqual):
        data = hepdata_converter.convert(yaml_path, options={'input_format': 'yaml', 'output_format': 'csv', 
           'single_file': True, 
           'validator_schema_version': '0.1.0'})
        self.assertEqual(data, table_5_noqual)