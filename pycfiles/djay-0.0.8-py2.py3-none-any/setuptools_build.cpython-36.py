# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/utils/setuptools_build.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 1239 bytes
import sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List
_SETUPTOOLS_SHIM = "import sys, setuptools, tokenize; sys.argv[0] = {0!r}; __file__={0!r};f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\\r\\n', '\\n');f.close();exec(compile(code, __file__, 'exec'))"

def make_setuptools_shim_args(setup_py_path, unbuffered_output=False):
    """
    Get setuptools command arguments with shim wrapped setup file invocation.

    :param setup_py_path: The path to setup.py to be wrapped.
    :param unbuffered_output: If True, adds the unbuffered switch to the
     argument list.
    """
    args = [
     sys.executable]
    if unbuffered_output:
        args.append('-u')
    args.extend(['-c', _SETUPTOOLS_SHIM.format(setup_py_path)])
    return args