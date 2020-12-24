# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/tests/test_imagelayout.py
# Compiled at: 2019-11-05 17:19:10
# Size of source mod 2**32: 771 bytes
from opencontainers.image.v1 import ImageLayout
import os, pytest

def test_imagelayout(tmp_path):
    """test creation of a simple sink plugin
    """
    layout = ImageLayout()
    with pytest.raises(SystemExit):
        layout.load({'imageLayoutVersion': 1.0})
    with pytest.raises(SystemExit):
        layout.load({'imageLayoutVersion': '1.0'})
    layout.load({'imageLayoutVersion': '1.0.0'})