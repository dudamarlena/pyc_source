# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/higlass/__init__.py
# Compiled at: 2020-01-26 00:21:31
# Size of source mod 2**32: 406 bytes
from ._version import __version__
from .viewer import display
from .tilesets import Tileset
from .server import Server
from .client import Track, CombinedTrack, View, ViewConf

def _jupyter_nbextension_paths():
    return [
     {'section':'notebook', 
      'src':'static', 
      'dest':'higlass-jupyter', 
      'require':'higlass-jupyter/extension'}]