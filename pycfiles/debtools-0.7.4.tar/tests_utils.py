# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/DebTools/debtools/tests/tests_utils.py
# Compiled at: 2015-07-27 09:11:29
from __future__ import unicode_literals
from unittest import TestCase
import pkg_resources
from debtools.utils import get_control_data
__author__ = b'Matthieu Gallet'

class TestGetControlData(TestCase):

    @property
    def filename(self):
        return pkg_resources.resource_filename(b'debtools.tests', b'python-debtools_0.3-1_all.deb')

    def test_get_control_data(self):
        data = get_control_data(self.filename)
        self.assertEqual({b'Maintainer': b'Matthieu Gallet <gallet.matthieu@19pouces.net>', 
           b'Description': b'Utilities for creating mutliple Debian packages.\nDebTools\n========', 
           b'Package': b'python-debtools', 
           b'Section': b'python', 
           b'Depends': b'python (>= 2.7), python (<< 2.8), python-stdeb, python-backports.lzma', 
           b'Priority': b'optional', 
           b'Source': b'debtools', 
           b'Installed-Size': b'88', 
           b'Version': b'0.3-1', 
           b'Architecture': b'all'}, data)