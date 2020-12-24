# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_general.py
# Compiled at: 2020-03-08 13:18:18
# Size of source mod 2**32: 250 bytes
"""
Module that contains general tests for solstice-tools-snowgenerator
"""
import pytest
from solstice.tools.snowgenerator import __version__

def test_version():
    assert __version__.__version__