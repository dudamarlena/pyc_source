# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/type/guitype.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 4175 bytes
"""
Core :mod:`PySide2`-specific **type** (i.e., class) functionality.
"""
from PySide2.QtCore import QAbstractEventDispatcher, QThread, QThreadPool, QPoint, QSize, Slot
from PySide2.QtWidgets import QLabel, QProgressBar, QWidget, QTreeWidgetItem
from betse.util.type.types import NoneType, NoneTypes
from betsee.util.widget.stock.guiprogressbar import QBetseeProgressBar
QWidgetType = QWidget
QVariantTypes = (
 bool, int, float, str,
 QPoint, QSize)
QAbstractEventDispatcherOrNoneTypes = (
 QAbstractEventDispatcher, NoneType)
QTreeWidgetItemOrNoneTypes = (
 QTreeWidgetItem, NoneType)
QVariantOrNoneTypes = QVariantTypes + NoneTypes
SlotOrNoneTypes = (
 Slot, NoneType)
QThreadOrNoneTypes = (
 QThread, NoneType)
QThreadPoolOrNoneTypes = (
 QThreadPool, NoneType)
QLabelOrNoneTypes = (
 QLabel, NoneType)
QProgressBarOrNoneTypes = (
 QProgressBar, NoneType)
QWidgetOrNoneTypes = (
 QWidgetType, NoneType)
QBetseeProgressBarOrNoneTypes = (
 QBetseeProgressBar, NoneType)