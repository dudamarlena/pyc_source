# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/pointsource.py
# Compiled at: 2013-09-16 16:07:19
__author__ = 'yarnaid'
try:
    import glespy.properties as properties, glespy.pixelmap as pixelmap, glespy.tools.convertion as conv
except:
    import properties

class PointSource(object):
    """
    Class for storing file with point sources and
    converting it
    """
    name = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_pixelmap(self, map_name=None, tp='fp', **kwargs):
        map_name = conv.asci_to_map(self.name, tp, map_name=map_name, **kwargs)
        attrs = kwargs.copy()
        attrs['name'] = map_name
        pixmap = pixelmap.gPixelMap(**attrs)
        return pixmap

    def show(self, **kwargs):
        self.to_pixelmap(**kwargs).show(**kwargs)