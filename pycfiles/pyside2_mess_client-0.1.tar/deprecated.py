# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_build/py2.7-qt5.14.2-64bit-release/pyside2/PySide2/support/deprecated.py
# Compiled at: 2020-04-24 02:58:07
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