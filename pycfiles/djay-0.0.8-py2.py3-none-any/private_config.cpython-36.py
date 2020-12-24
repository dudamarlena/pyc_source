# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/redbaron/redbaron/private_config.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 315 bytes
from __future__ import absolute_import
import redbaron

def runned_from_ipython():
    if redbaron.force_ipython_behavior:
        return True
    if not redbaron.ipython_behavior:
        return False
    try:
        __IPYTHON__
        return True
    except NameError:
        return False