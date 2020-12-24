# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/_tqdm.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 281 bytes
from .std import *
from .std import __all__
from .std import TqdmDeprecationWarning
from warnings import warn
warn('This function will be removed in tqdm==5.0.0\nPlease use `tqdm.std.*` instead of `tqdm._tqdm.*`', TqdmDeprecationWarning,
  stacklevel=2)