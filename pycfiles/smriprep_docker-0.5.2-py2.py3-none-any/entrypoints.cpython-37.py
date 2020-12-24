# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/utils/entrypoints.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 1152 bytes
import sys
import pip._internal.cli.main as main
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, List

def _wrapper(args=None):
    """Central wrapper for all old entrypoints.

    Historically pip has had several entrypoints defined. Because of issues
    arising from PATH, sys.path, multiple Pythons, their interactions, and most
    of them having a pip installed, users suffer every time an entrypoint gets
    moved.

    To alleviate this pain, and provide a mechanism for warning users and
    directing them to an appropriate place for help, we now define all of
    our old entrypoints as wrappers for the current one.
    """
    sys.stderr.write("WARNING: pip is being invoked by an old script wrapper. This will fail in a future version of pip.\nPlease see https://github.com/pypa/pip/issues/5599 for advice on fixing the underlying issue.\nTo avoid this problem you can invoke Python with '-m pip' instead of running pip directly.\n")
    return main(args)