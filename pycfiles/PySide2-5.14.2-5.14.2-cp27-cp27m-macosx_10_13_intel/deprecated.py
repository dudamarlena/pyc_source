# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_build/py2.7-qt5.14.2-64bit-release/pyside2/PySide2/support/deprecated.py
# Compiled at: 2020-03-30 06:44:48
from __future__ import print_function, absolute_import
import warnings
from textwrap import dedent

class PySideDeprecationWarningRemovedInQt6(Warning):
    pass


def constData(self):
    cls = self.__class__
    name = cls.__name__
    warnings.warn(dedent(('\n        {name}.constData is unpythonic and will be removed in Qt For Python 6.0 .\n        Please use {name}.data instead.').format(**locals())), PySideDeprecationWarningRemovedInQt6, stacklevel=2)
    return cls.data(self)


def fix_for_QtGui(QtGui):
    for name, cls in QtGui.__dict__.items():
        if name.startswith('QMatrix') and 'data' in cls.__dict__:
            cls.constData = constData