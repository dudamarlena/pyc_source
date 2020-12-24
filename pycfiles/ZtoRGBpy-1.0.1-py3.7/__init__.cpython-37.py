# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ZtoRGBpy\__init__.py
# Compiled at: 2019-05-19 01:57:06
# Size of source mod 2**32: 2217 bytes
"""
Reference
=========

Complex number to perceptually uniform RGB subset mapping library
Supports direct transformation of numpy arrays using remap, and
integration with matplotlib using imshow, colorbar and colorwheel.

.. moduleauthor:: Glen Fletcher <mail@glenfletcher.com>
"""
from ZtoRGBpy._core import remap, Scale, LinearScale, LogScale, RGBColorProfile, sRGB_HIGH, sRGB_LOW, sRGB
from ZtoRGBpy._info import __authors__, __copyright__, __license__, __contact__, __version__, __title__, __desc__
try:
    from ZtoRGBpy._mpl import colorbar, colorwheel, imshow
except ImportError:
    _mpl_requirement = 'Requires matplotlib>=1.3,<3'

    def colorbar():
        raise NotImplementedError(_mpl_requirement)


    def colorwheel():
        raise NotImplementedError(_mpl_requirement)


    def imshow():
        raise NotImplementedError(_mpl_requirement)


_real_module = {}
for name in list(locals().keys()):
    if name[0] != '_':
        _real_module[name] = locals()[name].__module__
        locals()[name].__module__ = 'ZtoRGBpy'