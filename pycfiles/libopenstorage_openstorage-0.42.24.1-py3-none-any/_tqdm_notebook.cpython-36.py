# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/tqdm/tqdm/_tqdm_notebook.py
# Compiled at: 2020-01-10 16:25:33
# Size of source mod 2**32: 305 bytes
from .notebook import *
from .notebook import __all__
from .std import TqdmDeprecationWarning
from warnings import warn
warn('This function will be removed in tqdm==5.0.0\nPlease use `tqdm.notebook.*` instead of `tqdm._tqdm_notebook.*`', TqdmDeprecationWarning,
  stacklevel=2)