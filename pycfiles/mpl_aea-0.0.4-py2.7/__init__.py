# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpl_aea/__init__.py
# Compiled at: 2017-04-14 21:04:55
from matplotlib.projections import register_projection
from .aea import AlbersEqualAreaAxes
from .geo import MollweideAxes
register_projection(AlbersEqualAreaAxes)
register_projection(MollweideAxes)
from .version import __version__
try:
    from matplotlib.transforms import TransformedPatchPath
except ImportError:
    from . import monkey