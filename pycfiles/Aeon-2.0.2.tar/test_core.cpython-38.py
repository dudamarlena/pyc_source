# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/tests/test_core.py
# Compiled at: 2019-11-21 05:24:28
# Size of source mod 2**32: 551 bytes
__doc__ = 'Test the core submodule.'
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