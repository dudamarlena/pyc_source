# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/autonotebook.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 657 bytes
import os
try:
    from IPython import get_ipython
    if 'IPKernelApp' not in get_ipython().config:
        raise ImportError('console')
    if 'VSCODE_PID' in os.environ:
        raise ImportError('vscode')
except:
    from .std import tqdm, trange
else:
    from .notebook import tqdm, trange
    from .std import TqdmExperimentalWarning
    from warnings import warn
    warn('Using `tqdm.autonotebook.tqdm` in notebook mode. Use `tqdm.tqdm` instead to force console mode (e.g. in jupyter console)', TqdmExperimentalWarning,
      stacklevel=2)
__all__ = [
 'tqdm', 'trange']