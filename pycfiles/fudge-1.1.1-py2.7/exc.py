# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fudge/exc.py
# Compiled at: 2015-06-08 14:33:15
"""Exceptions used by the fudge module.

See :ref:`using-fudge` for common scenarios.
"""
__all__ = [
 'FakeDeclarationError']

class FakeDeclarationError(Exception):
    """Exception in how this :class:`fudge.Fake` was declared."""
    pass