# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_rec2dict.py
# Compiled at: 2012-02-03 05:34:20
__doc__ = 'Tests for :mod:`cgp.utils.rec2dict`.'
from ..utils import rec2dict

def test_dict2rec_unicode():
    """Test with unicode keys."""
    rec2dict.dict2rec({'a': 'b'})