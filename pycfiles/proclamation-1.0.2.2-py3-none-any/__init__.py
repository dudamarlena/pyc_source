# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kracekumar/Dropbox/codes/python/python/procinfo/tests/__init__.py
# Compiled at: 2012-08-08 08:58:51
import os, sys
from nose.tools import assert_dict_equal
sys.path.insert(0, os.path.abspath('..'))
import procinfo

def test_return_human_readable():
    assert_dict_equal(procinfo.return_human_readable(3035918336), {'value': 2.83, 'str': '2.83 GB'})