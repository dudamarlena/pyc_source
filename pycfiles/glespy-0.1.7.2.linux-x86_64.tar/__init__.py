# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/__init__.py
# Compiled at: 2013-11-25 14:03:24
__author__ = 'yarnaid'
import properties
from ext.angles import Zone, Angle
from pixelmap import gPixelMap as PixelMap
from pointsource import PointSource
from tools import convertion as convert
from tools import colorer
from tools.logger import logger
import tools.tools, os
from cl import Cl
mappat_path = os.path.join(tools.tools.glesp_exec, tools.tools.glesp['mappat'])
if not os.path.exists(mappat_path):
    raise ImportError(('Cannot import module {}. No mappat binary found in {}').format(__name__, tools.tools.glesp_exec))