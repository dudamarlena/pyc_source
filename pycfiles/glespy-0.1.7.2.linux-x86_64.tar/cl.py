# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/cl.py
# Compiled at: 2013-11-25 13:47:29
__author__ = 'yarnaid'
import properties, tools.convertion as conv, alm, pixelmap, os

class Cl(properties.Printable):
    r"""C(\ell)"""
    name = None
    temp = True
    data = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.name:
            if os.path.exists(self.name) and self.name.count('tmp') < 1:
                self.temp = False

    def to_alm(self, alm_name=None, **kwargs):
        attrs = {}
        alm_name = conv.tools.get_out_name(alm_name, suffix='rand_alm_from_cl')
        alm_res = conv.cl_to_alm(self.name, alm_name=alm_name, **kwargs)
        attrs.update(alm_res)
        return alm.Alm(**attrs)

    def to_map(self, map_name=None, **kwargs):
        attrs = {}
        map_name = conv.tools.get_out_name(map_name, suffix='rand_map_from_cl')
        map_res = conv.cl_to_map(self.name, map_name=map_name, **kwargs)
        attrs.update(map_res)
        return pixelmap.gPixelMap(**attrs)