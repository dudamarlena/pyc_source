# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_general.py
# Compiled at: 2020-04-17 19:10:58
# Size of source mod 2**32: 240 bytes
__doc__ = '\nModule that contains general tests for plottwist-libs-pyblish\n'
import pytest
from plottwist.libs.pyblish import __version__

def test_version():
    assert __version__.get_version()