# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/io/test_io_utils.py
# Compiled at: 2019-12-16 17:25:58
# Size of source mod 2**32: 4569 bytes
"""
Created on Tue Nov  3 15:07:16 2017

@author: Suhas Somnath
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import unittest, sys
sys.path.append('../../pyUSID/')
from pyUSID.io import io_utils
from pyUSID.processing import comp_utils

class TestFormattedStrToNum(unittest.TestCase):

    def test_typical(self):
        self.assertEqual(io_utils.formatted_str_to_number('4.32 MHz', ['MHz', 'kHz'], [1000000.0, 1000.0]), 4320000.0)

    def test_wrong_types(self):
        with self.assertRaises(TypeError):
            _ = io_utils.formatted_str_to_number('4.32 MHz', ['MHz', 'kHz'], [
             1000000.0, 1000.0], separator=14)
        with self.assertRaises(TypeError):
            _ = io_utils.formatted_str_to_number({'dfdfd': 123}, ['MHz'], [1000000.0])
        with self.assertRaises(TypeError):
            _ = io_utils.formatted_str_to_number('dfdfdf', ['MHz'], 1000000.0)
        with self.assertRaises(TypeError):
            _ = io_utils.formatted_str_to_number('jkjk', ['MHz', 1234], [1000000.0, 10000.0])
        with self.assertRaises(TypeError):
            _ = io_utils.formatted_str_to_number('4.32 MHz', ['MHz', 'kHz'], [{'dfdfd': 13}, 1000.0])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('4.32 MHz', ['MHz'], [1000000.0, 1000.0])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('4.32 MHz', ['MHz', 'kHz'], [1000.0])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('4.32-MHz', ['MHz', 'kHz'], [1000000.0, 1000.0])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('haha MHz', ['MHz', 'kHz'], [1000000.0, 1000.0])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('1.2.3.4 MHz', ['MHz', 'kHz'], [1000000.0, 1000.0])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number('MHz', ['MHz', 'kHz'], [1000000.0, 1000.0])


class TestFormatQuantity(unittest.TestCase):

    def test_typical(self):
        qty_names = [
         'sec', 'mins', 'hours', 'days']
        qty_factors = [1, 60, 3600, 86400]
        ret_val = io_utils.format_quantity(315, qty_names, qty_factors)
        self.assertEqual(ret_val, '5.25 mins')
        ret_val = io_utils.format_quantity(6300, qty_names, qty_factors)
        self.assertEqual(ret_val, '1.75 hours')

    def test_unequal_lengths(self):
        with self.assertRaises(ValueError):
            _ = io_utils.format_quantity(315, ['sec', 'mins', 'hours'], [1, 60, 3600, 86400])
        with self.assertRaises(ValueError):
            _ = io_utils.format_quantity(315, ['sec', 'mins', 'hours'], [1, 60])

    def test_incorrect_element_types(self):
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity(315, ['sec', 14, 'hours'], [1, 60, 86400])

    def test_incorrect_number_to_format(self):
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity('hello', ['sec', 'mins', 'hours'], [1, 60, 3600])

    def test_not_iterable(self):
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity(315, 14, [1, 60, 3600])
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity(315, ['sec', 'mins', 'hours'], slice(None))


class TestTimeSizeFormatting(unittest.TestCase):

    def test_format_time(self):
        ret_val = io_utils.format_time(315)
        self.assertEqual(ret_val, '5.25 mins')
        ret_val = io_utils.format_time(6300)
        self.assertEqual(ret_val, '1.75 hours')

    def test_format_size(self):
        ret_val = io_utils.format_size(15.23)
        self.assertEqual(ret_val, '15.23 bytes')
        ret_val = io_utils.format_size(5830418104.32)
        self.assertEqual(ret_val, '5.43 GB')


class TestIOUtils(unittest.TestCase):

    def test_get_available_memory_rerouting(self):
        if sys.version_info.major == 3:
            with self.assertWarns(FutureWarning):
                _ = io_utils.get_available_memory()
        self.assertEqual(comp_utils.get_available_memory(), io_utils.get_available_memory())

    def test_recommend_cpu_cores_rerouting(self):
        if sys.version_info.major == 3:
            with self.assertWarns(FutureWarning):
                _ = io_utils.recommend_cpu_cores(140)
        self.assertEqual(comp_utils.recommend_cpu_cores(140), io_utils.recommend_cpu_cores(140))


if __name__ == '__main__':
    unittest.main()