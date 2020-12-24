# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/tests/auto_inherit_config.py
# Compiled at: 2019-10-06 19:10:59
# Size of source mod 2**32: 381 bytes
import attr
from lbdrabbit.lbd_func_config.base import BaseConfig, REQUIRED, NOTHING

@attr.s
class LbdFuncConfig(BaseConfig):
    memory = attr.ib(default=REQUIRED)
    timeout = attr.ib(default=REQUIRED)
    alias = attr.ib(default=NOTHING)
    description = attr.ib(default=NOTHING)
    _default = {'memory':128, 
     'timeout':3}