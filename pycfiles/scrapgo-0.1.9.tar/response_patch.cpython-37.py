# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\modules\request\response_patch.py
# Compiled at: 2019-03-30 13:15:09
# Size of source mod 2**32: 277 bytes


def _set_tracert(self, previous):
    if not hasattr(self, 'tracert'):
        self.tracert = []
    if previous:
        self.tracert.insert(0, previous)


def patch_response(Response):
    Response._set_tracert = _set_tracert