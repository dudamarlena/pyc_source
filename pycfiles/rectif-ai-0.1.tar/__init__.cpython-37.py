# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/__init__.py
# Compiled at: 2019-09-17 17:20:56
# Size of source mod 2**32: 162 bytes
import sys
if sys.version_info < (3, 6, 1):
    raise RuntimeError('Rectif.ai requires Python 3.6 or later')
import rectifai.version as __version__