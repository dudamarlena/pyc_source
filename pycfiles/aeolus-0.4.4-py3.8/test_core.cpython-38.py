# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/tests/test_core.py
# Compiled at: 2019-11-21 05:24:28
# Size of source mod 2**32: 551 bytes
"""Test the core submodule."""
from pathlib import Path
from aeolus.exceptions import LoadError
import pytest
TST_DATA = Path(__file__).parent / 'data'

def test_foo():
    """Test ..."""
    pass


def test_loaderror():
    """Test raising LoadError."""
    with pytest.raises(LoadError):
        raise LoadError