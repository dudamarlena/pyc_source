# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_rec2dict.py
# Compiled at: 2012-02-03 05:34:20
"""Tests for :mod:`cgp.utils.rec2dict`."""
from ..utils import rec2dict

def test_dict2rec_unicode():
    """Test with unicode keys."""
    rec2dict.dict2rec({'a': 'b'})