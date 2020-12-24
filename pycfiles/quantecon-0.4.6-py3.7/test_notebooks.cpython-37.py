# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/util/tests/test_notebooks.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 1136 bytes
"""
Tests for Notebook Utilities

Functions
---------
fetch_nb_dependencies

"""
from quantecon.util import fetch_nb_dependencies
import unittest, os
FILES = [
 'test_file.md']
REPO = 'https://github.com/QuantEcon/QuantEcon.py'
RAW = 'raw'
BRANCH = 'master'
FOLDER = 'quantecon/util/tests/'

class TestNotebookUtils(unittest.TestCase):

    def test_fetch_nb_dependencies(self):
        """
        Run First and Test Download
        """
        status = fetch_nb_dependencies(files=FILES,
          repo=REPO,
          raw=RAW,
          branch=BRANCH,
          folder=FOLDER)
        self.assertFalse(False in status)

    def test_fetch_nb_dependencies_overwrite(self):
        """
        Run Second and Ensure file is skipped by checking a False is found in status
        """
        status = fetch_nb_dependencies(files=FILES,
          repo=REPO,
          raw=RAW,
          branch=BRANCH,
          folder=FOLDER)
        status = fetch_nb_dependencies(files=FILES,
          repo=REPO,
          raw=RAW,
          branch=BRANCH,
          folder=FOLDER)
        self.assertTrue(False in status)

    def tearDown(self):
        os.remove('test_file.md')