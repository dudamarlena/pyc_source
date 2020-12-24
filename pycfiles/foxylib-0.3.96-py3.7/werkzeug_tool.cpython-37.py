# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/werkzeug/werkzeug_tool.py
# Compiled at: 2020-02-07 17:58:52
# Size of source mod 2**32: 934 bytes
from foxylib.tools.collections.collections_tool import l_singleton2obj

class WerkzeugTool:

    @classmethod
    def immutablemultidict2h(cls, imd, key_list_singleton=None):
        h_k2l = imd.to_dict(flat=False)
        if not key_list_singleton:
            return h_k2l
        h_k2v = {k:(l if k not in key_list_singleton else l_singleton2obj(l)) for k, l in h_k2l.items()}
        return h_k2v

    @classmethod
    def immutablemultidict_key2list(cls, imd, key):
        h = imd.to_dict(flat=False)
        l = h.get(key)
        return l

    @classmethod
    def immutablemultidict_key2v_singleton(cls, imd, key):
        l = cls.immutablemultidict_key2list(imd, key)
        if not l:
            return
        return l_singleton2obj(l)


imd2h = WerkzeugTool.immutablemultidict2h
imd_key2list = WerkzeugTool.immutablemultidict_key2list
imd_key2value = WerkzeugTool.immutablemultidict_key2v_singleton