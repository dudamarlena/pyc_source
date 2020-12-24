# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/blooser/anaconda3/lib/python3.7/site-packages/youtubedownloader/component_changer.py
# Compiled at: 2020-04-23 10:07:19
# Size of source mod 2**32: 1966 bytes
from PySide2.QtCore import QObject, QStateMachine, QState, QFinalState, Signal, Slot, Property
from PySide2.QtQml import QQmlParserStatus, QQmlComponent, QQmlListReference, ListProperty
from PySide2 import QtWidgets
from PySide2 import QtQuick

class Change(QObject):
    actived = Signal()
    whenChanged = Signal(bool)
    componentChanged = Signal(QQmlComponent)

    def __init__(self):
        super(Change, self).__init__(None)
        self._when = False
        self._component = None

    def readWhen(self):
        return self._when

    def setWhen(self, new_when):
        self._when = new_when
        self.whenChanged.emit(self._when)
        if self._when:
            self.actived.emit()

    def readComponent(self):
        return self._component

    def setComponent(self, new_component):
        self._component = new_component
        self.componentChanged.emit(self._component)

    when = Property('bool', readWhen, setWhen, whenChanged)
    component = Property(QQmlComponent, readComponent, setComponent, componentChanged)


class ComponentChanger(QObject, QQmlParserStatus):
    currentComponentChanged = Signal(QQmlComponent)

    def __init__(self):
        super(ComponentChanger, self).__init__(None)
        self._current_component = None
        self._changes = []

    @Property(QQmlComponent, notify=currentComponentChanged)
    def currentComponent(self):
        return self._current_component

    def setCurrentComponent(self, new_current_component):
        self._current_component = new_current_component
        self.currentComponentChanged.emit(self._current_component)

    def appendChange(self, change):
        change.actived.connect(lambda : self.setCurrentComponent(change.component))
        self._changes.append(change)

    def classBegin(self):
        pass

    def componentComplete(self):
        pass

    changes = ListProperty(Change, appendChange)