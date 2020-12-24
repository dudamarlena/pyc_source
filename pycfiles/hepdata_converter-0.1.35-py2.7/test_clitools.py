# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_clitools.py
# Compiled at: 2020-03-05 14:33:22
import os, hepdata_converter
from hepdata_converter.testsuite import insert_data_as_str, insert_path
from hepdata_converter.testsuite.test_writer import WriterTestSuite

class CLIToolsTestSuite(WriterTestSuite):

    def test_wrong_call(self):
        self.assertRaises(SystemExit, hepdata_converter.main, [])

    @insert_path('yaml_full')
    @insert_data_as_str('csv/table_1.csv')
    def test_convert_yaml2csv(self, submission_file, table_csv):
        output_path = os.path.join(self.current_tmp, 'output.csv')
        code, message = hepdata_converter._main(['--input-format', 'yaml',
         '--output-format', 'csv',
         '--table', 'Table 1',
         '--validator-schema-version', '0.1.0',
         '--pack', submission_file, output_path])
        self.assertEqual(code, 0, message)
        self.assertTrue(os.path.exists(output_path))
        with open(output_path) as (f):
            self.assertMultiLineAlmostEqual(table_csv, f.read())

    def test_convert_yaml2yoda(self):
        hepdata_converter._main(['--input-format', 'yaml', '--output-format', 'csv',
         '--table', 'Table 1',
         self.current_tmp, os.path.join(self.current_tmp, 'output.csv')])

    def test_help(self):
        self.assertRaises(SystemExit, hepdata_converter.main, ['--help'])

    def test_version(self):
        r, message = hepdata_converter._main(['--version'])
        self.assertEqual(r, 0)
        self.assertTrue(message.endswith(hepdata_converter.version.__version__))