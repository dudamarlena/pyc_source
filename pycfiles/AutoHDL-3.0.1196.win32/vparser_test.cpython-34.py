# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\test\verilog\vparser_test.py
# Compiled at: 2015-05-12 15:42:38
# Size of source mod 2**32: 1648 bytes
import unittest
from autohdl.hdl_logger import *
logging.disable(logging.CRITICAL)
import sys
sys.path.insert(0, '../..')
from autohdl.verilog.vparser import *

class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cwd_was = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    @classmethod
    def tearDownClass(self):
        os.chdir(self.cwd_was)

    def test_parser(self):
        with open('in/parser/serial_neuron_core.v') as (f):
            actual = Parser({'file_path': 'fake_path',  'preprocessed': f.read()}).parsed
        expected = {'serial_neuron_core': {'path': 'fake_path',  'instances': {'serial_subs',
                                              'serial_mult',
                                              'serial_summ',
                                              'serial_summ_n'}}, 
         'second_in_one_file': {'instances': {'as'},  'path': 'fake_path'}}
        self.assertEqual(actual, expected)

    def test_parser2(self):
        with open('in/parser/dcs_packet_v2_TB.v') as (f):
            actual = Parser({'file_path': 'fake_path',  'preprocessed': f.read()}).parsed
        expected = {'dcs_packet_v2_tb': {'instances': {'dcs_packet_rx_v2', 'dcs_packet_tx_v2'},  'path': 'fake_path'}}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()