# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/union_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1976 bytes
from arch.api.utils import log_utils
from federatedml.util import consts
from federatedml.param.base_param import BaseParam
LOGGER = log_utils.getLogger()

class UnionParam(BaseParam):
    __doc__ = '\n    Define the union method for combining multiple dTables and keep entries with the same id\n\n    Parameters\n    ----------\n    need_run: bool, default True\n        Indicate if this module needed to be run\n\n    allow_missing: bool, default False\n        Whether allow mismatch between feature length and header length in the result. Note that empty tables will always be skipped regardless of this param setting.\n\n    '

    def __init__(self, need_run=True, allow_missing=False):
        super().__init__()
        self.need_run = need_run
        self.allow_missing = allow_missing

    def check(self):
        descr = "union param's "
        if type(self.need_run).__name__ != 'bool':
            raise ValueError(descr + 'need_run {} not supported, should be bool'.format(self.need_run))
        if type(self.allow_missing).__name__ != 'bool':
            raise ValueError(descr + 'allow_missing {} not supported, should be bool'.format(self.allow_missing))
        LOGGER.info('Finish union parameter check!')
        return True