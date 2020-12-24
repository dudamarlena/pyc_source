# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/data/core/target.py
# Compiled at: 2019-09-14 05:43:36
# Size of source mod 2**32: 525 bytes
"""
target.py
Authors: rensike(rensike@baidu.com)
Date:    2019/9/14 下午5:42
"""

class Target(object):
    area = 0

    @property
    def is_small(self):
        return hasattr(self, 'area') and self.area < 322

    @property
    def is_middle(self):
        return hasattr(self, 'area') and 322 <= self.area < 962

    @property
    def is_large(self):
        return hasattr(self, 'area') and self.area >= 962