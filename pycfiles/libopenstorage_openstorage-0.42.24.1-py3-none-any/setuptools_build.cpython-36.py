# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/utils/setuptools_build.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 1631 bytes
import sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List, Sequence
_SETUPTOOLS_SHIM = "import sys, setuptools, tokenize; sys.argv[0] = {0!r}; __file__={0!r};f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\\r\\n', '\\n');f.close();exec(compile(code, __file__, 'exec'))"

def make_setuptools_shim_args(setup_py_path, global_options=None, no_user_config=False, unbuffered_output=False):
    """
    Get setuptools command arguments with shim wrapped setup file invocation.

    :param setup_py_path: The path to setup.py to be wrapped.
    :param global_options: Additional global options.
    :param no_user_config: If True, disables personal user configuration.
    :param unbuffered_output: If True, adds the unbuffered switch to the
     argument list.
    """
    args = [
     sys.executable]
    if unbuffered_output:
        args.append('-u')
    args.extend(['-c', _SETUPTOOLS_SHIM.format(setup_py_path)])
    if global_options:
        args.extend(global_options)
    if no_user_config:
        args.append('--no-user-cfg')
    return args