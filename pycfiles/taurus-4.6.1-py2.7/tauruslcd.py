# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/tauruslcd.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides a Taurus widget based on QLCDNumber"""
from __future__ import absolute_import
from builtins import str
from builtins import object
import collections
from taurus.core.taurusbasetypes import TaurusElementType, TaurusEventType, AttrQuality, TaurusDevState
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.qt.qtgui.base import TaurusBaseController
from taurus.qt.qtgui.base import TaurusScalarAttributeControllerHelper
from taurus.qt.qtgui.base import TaurusConfigurationControllerHelper
from taurus.qt.qtgui.base import updateLabelBackground
__all__ = [
 'TaurusLCD']
__docformat__ = 'restructuredtext'
_QT_PLUGIN_INFO = {'module': 'taurus.qt.qtgui.display', 
   'group': 'Taurus Display', 
   'icon': 'designer:lcdnumber.png'}
TaurusModelType = TaurusElementType
EventType = TaurusEventType

class TaurusLCDController(TaurusBaseController):

    def _setStyle(self):
        TaurusBaseController._setStyle(self)
        lcd = self.lcd()
        if self.usePalette():
            lcd.setFrameShape(Qt.QFrame.Box)
            lcd.setFrameShadow(Qt.QFrame.Raised)
            lcd.setLineWidth(1)

    def lcd(self):
        """Helper method that returns the LCDNumber widget"""
        return self.widget()

    def _updateForeground(self, lcd):
        value = None
        if lcd.fgRole == 'value':
            value = self.getDisplayValue()
        elif lcd.fgRole == 'w_value':
            value = self.getDisplayValue(True)
        elif lcd.fgRole in ('', 'none'):
            value = ''
        if value is None:
            value = 'udef'
        lcd.setNumDigits(len(value))
        lcd.display(value)
        return

    def _needsStateConnection(self):
        lcd = self.lcd()
        return 'state' in (lcd.fgRole, lcd.bgRole)

    _updateBackground = updateLabelBackground


class TaurusLCDControllerAttribute(TaurusScalarAttributeControllerHelper, TaurusLCDController):

    def __init__(self, lcd):
        TaurusScalarAttributeControllerHelper.__init__(self)
        TaurusLCDController.__init__(self, lcd)

    def _getDisplayValue(self, widget, valueObj, idx, write):
        try:
            if write:
                value = valueObj.wvalue.magnitude
            else:
                value = valueObj.rvalue.magnitude
            if idx is not None and len(idx):
                for i in idx:
                    value = value[i]

            return widget.displayValue(value)
        except Exception as e:
            return widget.getNoneValue()

        return


class TaurusLCDControllerConfiguration(TaurusConfigurationControllerHelper, TaurusLCDController):

    def __init__(self, lcd):
        TaurusConfigurationControllerHelper.__init__(self)
        TaurusLCDController.__init__(self, lcd)


class TaurusLCDControllerDesignMode(object):

    def _updateLength(self, lcd):
        lcd.setNumDigits(6)

    def getDisplayValue(self, write=False):
        v = self.w_value()
        if not write:
            v = self.value()
        return '%6.2f' % v

    def value(self):
        return 99.99

    def w_value(self):
        return 0.0

    def quality(self):
        return AttrQuality.ATTR_VALID

    def state(self):
        return TaurusDevState.ON

    def _updateToolTip(self, lcd):
        lcd.setToolTip('Some random value for design purposes only')


class TaurusLCDControllerAttributeDesignMode(TaurusLCDControllerDesignMode, TaurusLCDControllerAttribute):

    def __init__(self, label):
        TaurusLCDControllerDesignMode.__init__(self)
        TaurusLCDControllerAttribute.__init__(self, label)


class TaurusLCDControllerConfigurationDesignMode(TaurusLCDControllerDesignMode, TaurusLCDControllerConfiguration):

    def __init__(self, label):
        TaurusLCDControllerDesignMode.__init__(self)
        TaurusLCDControllerConfiguration.__init__(self, label)

    def getDisplayValue(self, write=False):
        return '-99.99'

    def _updateToolTip(self, lcd):
        lcd.setToolTip('Some random configuration value for design purposes only')


_CONTROLLER_MAP = {None: TaurusLCDController, 
   TaurusModelType.Unknown: TaurusLCDController, 
   TaurusModelType.Attribute: TaurusLCDControllerAttribute, 
   TaurusModelType.Configuration: TaurusLCDControllerConfiguration}
_DESIGNER_CONTROLLER_MAP = {None: TaurusLCDControllerAttributeDesignMode, 
   TaurusModelType.Unknown: TaurusLCDControllerAttributeDesignMode, 
   TaurusModelType.Attribute: TaurusLCDControllerAttributeDesignMode, 
   TaurusModelType.Configuration: TaurusLCDControllerConfigurationDesignMode}

def Controller(lcd):
    ctrl_map = _CONTROLLER_MAP
    if lcd._designMode:
        ctrl_map = _DESIGNER_CONTROLLER_MAP
    model_type = lcd.getModelType()
    ctrl_klass = ctrl_map.get(model_type, TaurusLCDController)
    return ctrl_klass(lcd)


class TaurusLCD(Qt.QLCDNumber, TaurusBaseWidget):
    """ A Taurus-enabled :class:`Qt.QLCDNumber` widget. Its text can represent
    either the rvalue or wvalue *magnitude* (or nothing), and the background
    can colour-code the attribute quality or the device state (or nothing)"""
    DefaultBgRole = 'quality'
    DefaultFgRole = 'value'
    DefaultShowText = True
    DefaultModelIndex = None

    def __init__(self, parent=None, designMode=False):
        self._bgRole = self.DefaultBgRole
        self._fgRole = self.DefaultFgRole
        self._modelIndex = self.DefaultModelIndex
        self._modelIndexStr = ''
        self._controller = None
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QLCDNumber, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        if self._designMode:
            self.controller().update()
        return

    def _calculate_controller_class(self):
        ctrl_map = _CONTROLLER_MAP
        if self._designMode:
            ctrl_map = _DESIGNER_CONTROLLER_MAP
        model_type = self.getModelType()
        ctrl_klass = ctrl_map.get(model_type, TaurusLCDController)
        return ctrl_klass

    def controller(self):
        ctrl = self._controller
        if ctrl is not None and not ctrl.__class__ == TaurusLCDController:
            return ctrl
        else:
            ctrl_klass = self._calculate_controller_class()
            if ctrl is not None and ctrl.__class__ == ctrl_klass:
                return ctrl
            self._controller = ctrl = ctrl_klass(self)
            return ctrl

    def handleEvent(self, evt_src, evt_type, evt_value):
        self.controller().handleEvent(evt_src, evt_type, evt_value)

    def isReadOnly(self):
        return True

    def setModel(self, m):
        self._controller = None
        TaurusBaseWidget.setModel(self, m)
        return

    def getModelIndexValue(self):
        return self._modelIndex

    def getModelIndex(self):
        return self._modelIndexStr

    def setModelIndex(self, modelIndex):
        mi = str(modelIndex)
        if len(mi) == 0:
            self._modelIndex = None
        else:
            try:
                mi_value = eval(str(mi))
            except:
                return

            if type(mi_value) == int:
                mi_value = (
                 mi_value,)
            if not isinstance(mi_value, collections.Sequence):
                return
            self._modelIndex = mi_value
        self._modelIndexStr = mi
        self.controller().update()
        return

    def resetModelIndex(self):
        self.setModelIndex(self.DefaultModelIndex)

    def getBgRole(self):
        return self._bgRole

    def setBgRole(self, bgRole):
        self._bgRole = str(bgRole).lower()
        self.controller().update()

    def resetBgRole(self):
        self.setBgRole(self.DefaultBgRole)

    def getFgRole(self):
        return self._fgRole

    def setFgRole(self, fgRole):
        self._fgRole = str(fgRole).lower()
        self.controller().update()

    def resetFgRole(self):
        self.setFgRole(self.DefaultFgRole)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        d = TaurusBaseWidget.getQtDesignerPluginInfo()
        d.update(_QT_PLUGIN_INFO)
        return d

    model = Qt.pyqtProperty('QString', TaurusBaseWidget.getModel, setModel, TaurusBaseWidget.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)
    modelIndex = Qt.pyqtProperty('QString', getModelIndex, setModelIndex, resetModelIndex)
    fgRole = Qt.pyqtProperty('QString', getFgRole, setFgRole, resetFgRole, doc='foreground role')
    bgRole = Qt.pyqtProperty('QString', getBgRole, setBgRole, resetBgRole, doc='background role')


def demo():
    """LCD"""
    from .demo import tauruslcddemo
    return tauruslcddemo.main()


def main():
    import sys, taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    app = Application.instance()
    owns_app = app is None
    if owns_app:
        import taurus.core.util.argparse
        parser = taurus.core.util.argparse.get_taurus_parser()
        parser.usage = '%prog [options] <full_attribute_name(s)>'
        app = Application(sys.argv, cmd_line_parser=parser, app_name='Taurus LCD demo', app_version='1.0', org_domain='Taurus', org_name='Tango community')
    args = app.get_command_line_args()
    if len(args) == 0:
        w = demo()
    else:
        models = map(str.lower, args)
        w = Qt.QWidget()
        layout = Qt.QGridLayout()
        w.setLayout(layout)
        for model in models:
            label = TaurusLCD()
            label.model = model
            layout.addWidget(label)

    w.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w
    return


if __name__ == '__main__':
    main()