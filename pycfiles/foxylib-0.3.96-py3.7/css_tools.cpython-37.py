# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/html/css_tools.py
# Compiled at: 2019-04-05 18:04:58
# Size of source mod 2**32: 1435 bytes
from foxylib.tools.collections.collections_tools import DictToolkit, lchain

class CSSToolkit:

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
                    return DictToolkit.VWrite.overwrite(h, k, v_new)
                return vwrite_in(h, k, v_in)

            return vwrite_out

    class Merge:

        @classmethod
        def merge2dict(cls, h_to, h_from, vwrite=None):
            if vwrite is None:
                vwrite = DictToolkit.VWrite.overwrite
            vwrite_out = CSSToolkit.VWrite.is_attr_appendable2vwrite(CSSToolkit.VWrite.attr2is_appendable, vwrite)
            return DictToolkit.Merge.merge2dict(h_to, h_from, vwrite=vwrite_out)

        merge_dicts = DictToolkit.f_binary2f_iter(merge2dict, default={})

    merge_dicts = Merge.merge_dicts