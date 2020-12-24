# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/tqdm/tqdm/auto.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 231 bytes
import warnings
from .std import TqdmExperimentalWarning
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=TqdmExperimentalWarning)
    from .autonotebook import tqdm, trange
__all__ = [
 'tqdm', 'trange']