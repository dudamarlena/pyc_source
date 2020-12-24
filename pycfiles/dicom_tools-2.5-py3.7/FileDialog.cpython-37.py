# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/FileDialog.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 478 bytes
from ..Qt import QtGui, QtCore
import sys
__all__ = ['FileDialog']

class FileDialog(QtGui.QFileDialog):

    def __init__(self, *args):
        (QtGui.QFileDialog.__init__)(self, *args)
        if sys.platform == 'darwin':
            self.setOption(QtGui.QFileDialog.DontUseNativeDialog)