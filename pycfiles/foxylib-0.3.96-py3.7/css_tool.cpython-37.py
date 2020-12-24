# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/html/css_tool.py
# Compiled at: 2019-12-31 02:29:14
# Size of source mod 2**32: 1410 bytes
from foxylib.tools.collections.collections_tool import DictTool, lchain

class CSSTool:

    class VWrite:

        @classmethod
        def attr2is_appendable(cls, attr):
            l = {'class', 'style', 'onChange', 'onchange'}
            return attr in l

        @classmethod
        def is_attr_appendable2vwrite(cls, f_attr2is_appendable, vwrite_in):

            def vwrite_out(h, k, v_in):
                if f_attr2is_appendable(k):
                    v_new = ' '.join(lchain(h.get(k, '').split(), v_in.split()))
                    return DictTool.VWrite.overwrite(h, k, v_new)
                return vwrite_in(h, k, v_in)

            return vwrite_out

    class Merge:

        @classmethod
        def merge2dict(cls, h_to, h_from, vwrite=None):
            if vwrite is None:
                vwrite = DictTool.VWrite.overwrite
            vwrite_out = CSSTool.VWrite.is_attr_appendable2vwrite(CSSTool.VWrite.attr2is_appendable, vwrite)
            return DictTool.Merge.merge2dict(h_to, h_from, vwrite=vwrite_out)

        merge_dicts = DictTool.f_binary2f_iter(merge2dict, default={})

    merge_dicts = Merge.merge_dicts