# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Data_Interaction/Signals.py
# Compiled at: 2020-04-29 15:54:12
# Size of source mod 2**32: 422 bytes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import numpy as np
from PySide2.QtCore import *

class MatrixSignal(QObject):

    def __init__(self):
        super().__init__()

    sig = Signal(np.matrix)


class StrSignal(QObject):

    def __init__(self):
        super().__init__()

    sig = Signal(str)


class BoolSignal(QObject):

    def __init__(self):
        super().__init__()

    sig = Signal(bool)