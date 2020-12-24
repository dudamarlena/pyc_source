# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/__init__.py
# Compiled at: 2020-03-24 03:33:48
# Size of source mod 2**32: 356 bytes
import logging
from mapchete._core import open, Mapchete
from mapchete._processing import MapcheteProcess
from mapchete.tile import count_tiles
from mapchete._timer import Timer
__all__ = [
 'open', 'count_tiles', 'Mapchete', 'MapcheteProcess', 'Timer']
__version__ = '0.33'
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())