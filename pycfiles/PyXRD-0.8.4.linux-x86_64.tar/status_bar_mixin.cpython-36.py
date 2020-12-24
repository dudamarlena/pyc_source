# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/controllers/status_bar_mixin.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1522 bytes
from functools import wraps

class StatusBarMixin(object):

    @property
    def statusbar(self):
        if self.parent is not None:
            return self.parent.statusbar
        else:
            if self.view is not None:
                return self.view['statusbar']
            return

    @property
    def status_cid(self):
        if self.statusbar is not None:
            return self.statusbar.get_context_id(self.__class__.__name__)
        else:
            return

    @staticmethod
    def status_message(message, cid=None):

        def decorator(func):

            @wraps(func)
            def wrapper(self, *args, **kwargs):
                self.push_status_msg(message, cid)
                res = func(self, *args, **kwargs)
                self.pop_status_msg(cid)
                return res

            return wrapper

        return decorator

    def push_status_msg(self, msg, cid=None):
        if cid is not None:
            cid = self.statusbar.get_context_id(cid)
        else:
            cid = self.status_cid
        if cid is not None:
            self.statusbar.push(cid, msg)

    def pop_status_msg(self, cid=None):
        if cid is not None:
            cid = self.statusbar.get_context_id(cid)
        else:
            cid = self.status_cid
        if cid is not None:
            self.statusbar.pop(cid)