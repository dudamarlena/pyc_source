# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/cancellable.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 414 bytes


class Cancellable(object):
    __doc__ = '\n        Object which has a (threaded) action that can be cancelled by the user.\n    '
    _stop = None

    def _user_cancelled(self):
        return bool(self._stop is not None and self._stop.is_set())