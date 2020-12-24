# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/_main.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 281 bytes
from .cli import *
from .cli import __all__
from .std import TqdmDeprecationWarning
from warnings import warn
warn('This function will be removed in tqdm==5.0.0\nPlease use `tqdm.cli.*` instead of `tqdm._main.*`', TqdmDeprecationWarning,
  stacklevel=2)