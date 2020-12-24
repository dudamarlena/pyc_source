# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/base/utils/wrap.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 1248 bytes


class FederationWrapped(object):
    __doc__ = '\n    A wrapper, wraps _DTable as Table\n    '

    def __init__(self, session_id, dtable_cls, table_cls):
        self.dtable_cls = dtable_cls
        self.table_cls = table_cls
        self.session_id = session_id

    def unboxed(self, obj):
        if isinstance(obj, self.table_cls):
            return obj.dtable()
        return obj

    def boxed(self, obj):
        if isinstance(obj, self.dtable_cls):
            return self.table_cls.from_dtable(dtable=obj, session_id=(self.session_id))
        return obj