# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/unix/weisburd/code/igv_utils/igv_plotter/tests/test_igv_plotter_script.py
# Compiled at: 2016-09-21 16:10:43
import unittest, os, sys, subprocess

class TestBasicUseCases(unittest.TestCase):

    def setUp(self):
        self.python_path = '/usr/local/bin/python'
        self.igv_plotter_path = os.path.dirname(__file__) + '/../bin/igv_plotter'

    def test_igv_plotter_exit_code(self):
        """Integration test for igv_plotter script"""
        exit_code = os.system((' ').join([self.python_path, self.igv_plotter_path, '1:12345']))
        self.assertEqual(exit_code, 0)