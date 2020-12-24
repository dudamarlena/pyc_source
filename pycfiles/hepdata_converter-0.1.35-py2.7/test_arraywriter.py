# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_arraywriter.py
# Compiled at: 2020-03-05 14:33:22
import os
from hepdata_converter import convert
from hepdata_converter.testsuite import insert_path
from hepdata_converter.testsuite.test_writer import WriterTestSuite

class ArrayWriterTestSuite(WriterTestSuite):

    @insert_path('yaml_full')
    def test_select_table(self, submission_filepath):
        csv_content = convert(submission_filepath, options={'input_format': 'yaml', 'output_format': 'csv', 
           'validator_schema_version': '0.1.0', 
           'table': os.path.join(submission_filepath, 'data1.yaml')})
        csv_content = convert(submission_filepath, options={'input_format': 'yaml', 'output_format': 'csv', 
           'validator_schema_version': '0.1.0', 
           'table': 'Table 1'})
        csv_content = convert(submission_filepath, options={'input_format': 'yaml', 'output_format': 'csv', 
           'validator_schema_version': '0.1.0', 
           'table': 0})