# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/commands/test.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 1283 bytes
"""
Different implementations of the ``./setup.py test`` command depending on
what's locally available.

If Astropy v1.1.0.dev or later is available it should be possible to import
AstropyTest from ``astropy.tests.command``.  If ``astropy`` can be imported
but not ``astropy.tests.command`` (i.e. an older version of Astropy), we can
use the backwards-compat implementation of the command.

If Astropy can't be imported at all then there is a skeleton implementation
that allows users to at least discover the ``./setup.py test`` command and
learn that they need Astropy to run it.
"""
try:
    import astropy
    from astropy.tests.command import AstropyTest
except Exception:
    from ._dummy import _DummyCommand

    class AstropyTest(_DummyCommand):
        command_name = 'test'
        description = 'Run the tests for this package'
        error_msg = "The 'test' command requires the astropy package to be installed and importable."