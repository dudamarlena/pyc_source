# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/setuptools/setuptools/errors.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 524 bytes
"""setuptools.errors

Provides exceptions used by setuptools modules.
"""
from distutils.errors import DistutilsError

class RemovedCommandError(DistutilsError, RuntimeError):
    __doc__ = 'Error used for commands that have been removed in setuptools.\n\n    Since ``setuptools`` is built on ``distutils``, simply removing a command\n    from ``setuptools`` will make the behavior fall back to ``distutils``; this\n    error is raised if a command exists in ``distutils`` but has been actively\n    removed in ``setuptools``.\n    '