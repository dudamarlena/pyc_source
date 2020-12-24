# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/dpi.py
# Compiled at: 2020-05-13 19:31:15
# Size of source mod 2**32: 1188 bytes
"""
Module that contains base class to handle DPI functionality
"""
from __future__ import print_function, division, absolute_import
from tpDcc.libs.qt.core import qtutils

class DPIScaling(object):
    __doc__ = '\n    Mixin class that can be used in any QWidget to add DPI scaling functionality to it\n    '

    def setFixedSize(self, size):
        return super(DPIScaling, self).setFixedSize(qtutils.dpi_scale(size))

    def setFixedHeight(self, height):
        return super(DPIScaling, self).setFixedHeight(qtutils.dpi_scale(height))

    def setFixedWidth(self, width):
        return super(DPIScaling, self).setFixedWidth(qtutils.dpiScale(width))

    def setMaximumWidth(self, width):
        return super(DPIScaling, self).setMaximumWidth(qtutils.dpi_scale(width))

    def setMinimumWidth(self, width):
        return super(DPIScaling, self).setMinimumWidth(qtutils.dpi_scale(width))

    def setMaximumHeight(self, height):
        return super(DPIScaling, self).setMaximumHeight(qtutils.dpi_scale(height))

    def setMinimumHeight(self, height):
        return super(DPIScaling, self).setMinimumHeight(qtutils.dpi_scale(height))