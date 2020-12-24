# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/controller/base.py
# Compiled at: 2015-07-14 12:50:20
# Size of source mod 2**32: 220 bytes
from .mechanics import ControllerMechanics
from .utils import ControllerUtils
from .virtual import ControllerVirtuals

class Controller(ControllerMechanics, ControllerUtils, ControllerVirtuals):
    pass