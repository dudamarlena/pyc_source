# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/pytest.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 498 bytes
"""
pytest: unit and functional testing with Python.
"""
__all__ = [
 'main']
if __name__ == '__main__':
    import pytest
    raise SystemExit(pytest.main())
from _pytest.config import main, UsageError, _preloadplugins, cmdline
from _pytest import __version__
_preloadplugins()