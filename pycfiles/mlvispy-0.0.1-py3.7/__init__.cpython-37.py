# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/jupyter_vis/__init__.py
# Compiled at: 2019-07-22 13:45:32
# Size of source mod 2**32: 212 bytes
from .class_builder import *

def _jupyter_nbextension_paths():
    return [
     {'section':'notebook', 
      'src':'static', 
      'dest':'jupyter_vis', 
      'require':'jupyter_vis/index'}]