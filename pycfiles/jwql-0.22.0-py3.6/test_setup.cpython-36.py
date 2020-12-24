# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/tests/test_setup.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 528 bytes
"""Tests for the ``setup.py`` module.

Authors
-------

    - Bryan Hilbert

Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to ``stdout``):

    ::

        pytest -s test_setup_info.py
"""
import jwql

def test_version_number():
    """Test that the JWQL version number is retrieved from
    ``setup.py``
    """
    if not isinstance(jwql.__version__, str):
        raise AssertionError
    else:
        version_parts = jwql.__version__.split('.')
        assert len(version_parts) == 3