# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/input/tauruscombobox.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides a set of basic taurus widgets based on QCheckBox"""
__all__ = [
 'TaurusAttrListComboBox', 'TaurusValueComboBox']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.core import DataType, TaurusEventType
from taurus.core.taurusattribute import TaurusAttribute
from taurus.qt.qtgui.base import TaurusBaseWidget, TaurusBaseWritableWidget
from taurus.core.util import eventfilters

class TaurusValueComboBox(Qt.QComboBox, TaurusBaseWritableWidget):
    """This widget shows a combobox that offers a limited choice of values that
    can be set on an attribute."""

    def __init__(self, parent=None, designMode=False):
        self._previousModelName = None
        self._lastValueByUser = None
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QComboBox, parent)
        self.call__init__(TaurusBaseWritableWidget, name, designMode=designMode)
        return

    def _setCurrentIndex(self, index):
        bs = self.blockSignals(True)
        try:
            self.setCurrentIndex(index)
        finally:
            self.blockSignals(bs)

    def preAttach(self):
        """reimplemented from :class:`TaurusBaseWritableWidget`"""
        TaurusBaseWritableWidget.preAttach(self)
        self.currentIndexChanged.connect(self.writeIndexValue)

    def postDetach(self):
        """reimplemented from :class:`TaurusBaseWritableWidget`"""
        TaurusBaseWritableWidget.postDetach(self)
        try:
            self.currentIndexChanged.disconnect(self.writeIndexValue)
        except TypeError:
            pass

    def getValue(self):
        """
        Get the value that the widget is displaying now, not the value
        of the attribute.
        """
        model = self.getModelObj()
        if model is None:
            return
        else:
            dtype = model.type
            new_value = self.itemData(self.currentIndex())
            if new_value is None:
                return
            if dtype == DataType.Integer:
                func = int
            elif dtype == DataType.Float:
                func = float
            elif dtype == DataType.String:
                func = str
            elif dtype == DataType.Boolean:
                func = bool
            else:
                return
            return new_value

    def setValue(self, value):
        """
        Set the value for the widget to display, not the value of the
        attribute.
        """
        index = self.findData(value)
        self._setCurrentIndex(index)

    def updateStyle(self):
        """reimplemented from :class:`TaurusBaseWritableWidget`"""
        if self.hasPendingOperations():
            self.setStyleSheet('TaurusValueComboBox {color: blue; font-weight: bold;}')
        else:
            self.setStyleSheet('TaurusValueComboBox {}')
        super(TaurusValueComboBox, self).updateStyle()

    @Qt.pyqtSlot(int, name='currentIndexChanged')
    def writeIndexValue(self, index):
        """slot called to emit a valueChanged signal when the currentIndex is
        changed (and trigger a write if AutoApply is enabled)
        """
        self.emitValueChanged()
        if self.getAutoApply():
            self.writeValue()

    def keyPressEvent(self, event):
        """reimplemented to trigger a write when Enter (or Return) key is
        pressed
        """
        if event.key() in [Qt.Qt.Key_Return, Qt.Qt.Key_Enter]:
            self.writeValue()
            event.accept()
        else:
            return Qt.QComboBox.keyPressEvent(self, event)

    def setValueNames(self, names):
        """
        Sets the correspondence between the values to be applied and their
        associated text to show in the combobox.

        :param names: (sequence<tuple>) A sequence of (name,value) tuples,
                      where each attribute value gets a name for display
        """
        bs = self.blockSignals(True)
        self.clear()
        self.blockSignals(bs)
        self.addValueNames(names)

    def addValueNames(self, names):
        """
        Add new value-name associations to the combobox.

        ... seealso: :meth:`setValueNames`

        :param names: (sequence<tuple>) A sequence of (name,value) tuples,
                      where each attribute value gets a name for display
        """
        bs = self.blockSignals(True)
        try:
            for k, v in names:
                self.addItem(k, v)

            mv = self.getModelValueObj()
            if mv is not None:
                self.setValue(mv.wvalue)
        finally:
            self.blockSignals(bs)

        self.emitValueChanged()
        return

    def getValueString(self, value, default='UNKNOWN(%s)'):
        """Returns the corresponding name in the combobox out of a value
        (or a default value if not found).

        :param value: value to look up
        :param default: (str) value in case it is not found. It accepts
                        a '%s' placeholder which will be substituted with
                        str(value). It defaults to 'UNKNOWN(%s)'.
        """
        item = self.findData(value)
        if item < 0:
            if '%s' in default:
                return default % str(value)
            else:
                return default

        return str(self.itemText(item))

    def teachDisplayTranslationToWidget(self, widget, default='UNKNOWN(%s)'):
        """
        Makes a label object change the displayed text by the corresponding
        value of the combobox. This is implemented for the general case
        and may be not what you expect in some cases (as for example, it
        fires a fake periodic event which may be problematic if these
        are being filtered out).
        """
        widget.displayValue = lambda v: self.getValueString(v, default)
        model = widget.getModelObj()
        if model:
            widget.fireEvent(model, TaurusEventType.Periodic, model.getValueObj())

    def setQModel(self, *args, **kwargs):
        """access to :meth:`QCombobox.setModel`

        .. seealso: :meth:`setModel`
        """
        Qt.QComboBox.setModel(self, *args, **kwargs)

    def setModel(self, m):
        """Reimplemented from :meth:`TaurusBaseWritableWidget.setModel` """
        if isinstance(m, Qt.QAbstractItemModel):
            self.warning('Deprecation warning: use setQModel() if you want to set a Qt Item Model. The setModel() method is reserved for Taurus models')
            return Qt.QComboBox.setModel(self, m)
        ret = TaurusBaseWritableWidget.setModel(self, m)
        self.emitValueChanged()
        return ret

    @classmethod
    def getQtDesignerPluginInfo(cls):
        """reimplemented from :class:`TaurusBaseWritableWidget`"""
        ret = TaurusBaseWritableWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.input'
        ret['icon'] = 'designer:combobox.png'
        return ret

    model = Qt.pyqtProperty('QString', TaurusBaseWidget.getModel, TaurusBaseWidget.setModel, TaurusBaseWidget.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)
    autoApply = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getAutoApply, TaurusBaseWritableWidget.setAutoApply, TaurusBaseWritableWidget.resetAutoApply)
    forcedApply = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getForcedApply, TaurusBaseWritableWidget.setForcedApply, TaurusBaseWritableWidget.resetForcedApply)


class TaurusAttrListComboBox(Qt.QComboBox, TaurusBaseWidget):
    """Combobox whose items reflect the items read from a 1D attribute of dtype
    str
    """

    def __init__(self, parent=None, designMode=False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QComboBox, parent)
        self.call__init__(TaurusBaseWidget, name)
        self.insertEventFilter(eventfilters.IGNORE_CONFIG)
        self.setSizeAdjustPolicy(Qt.QComboBox.AdjustToContents)
        self.defineStyle()
        self._lastAttrList = None
        return

    def defineStyle(self):
        """Defines the initial style for the widget """
        self.updateStyle()

    def getModelClass(self):
        """reimplemented from :class:`TaurusBaseWidget`"""
        return TaurusAttribute

    def handleEvent(self, evt_src, evt_type, evt_value):
        """reimplemented from :class:`TaurusBaseWidget`"""
        if evt_type == TaurusEventType.Error:
            attrList = []
        elif evt_src is None or evt_value is None:
            attrList = []
        else:
            attrList = list(evt_value.rvalue)
            attrList.sort()
        if attrList != self._lastAttrList:
            self._lastAttrList = attrList
            self.clear()
            self.addItems(attrList)
            self.updateStyle()
        return

    def updateStyle(self):
        """reimplemented from :class:`TaurusBaseWidget`"""
        self.update()

    def setQModel(self, *args, **kwargs):
        """access to :meth:`QAbstractItemView.setModel`

        .. seealso: :meth:`setModel`
        """
        return Qt.QAbstractItemView.setModel(self, *args, **kwargs)

    def setModel(self, m):
        """reimplemented from :class:`TaurusBaseWidget`"""
        if isinstance(m, Qt.QAbstractItemModel):
            self.warning('Deprecation warning: use setQModel() if you' + ' want to set a Qt Item Model. The setModel()' + ' method is reserved for Taurus models')
            return Qt.QAbstractItemView.setQModel(self, m)
        return TaurusBaseWidget.setModel(self, m)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        """reimplemented from :class:`TaurusBaseWidget`"""
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['group'] = 'Taurus Input'
        ret['module'] = 'taurus.qt.qtgui.input'
        ret['icon'] = 'designer:combobox.png'
        return ret

    model = Qt.pyqtProperty('QString', TaurusBaseWidget.getModel, TaurusBaseWidget.setModel, TaurusBaseWidget.resetModel)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseWidget.getUseParentModel, TaurusBaseWidget.setUseParentModel, TaurusBaseWidget.resetUseParentModel)


def _taurusAttrListTest():
    """tests taurusAttrList. Model: an attribute containing a list of strings"""
    from taurus.qt.qtgui.application import TaurusApplication
    a = TaurusApplication(cmd_line_parser=None)
    model = 'sys/tg_test/1/string_spectrum'
    w = TaurusAttrListComboBox()
    w.setModel(model)
    w.show()
    return a.exec_()


def _taurusValueComboboxTest():
    from taurus.qt.qtgui.application import TaurusApplication
    names = [
     ('name0', 0),
     ('name1', 1),
     ('name2', 2),
     ('name3', 3)]
    a = TaurusApplication(cmd_line_parser=None)
    w = Qt.QWidget()
    w.setLayout(Qt.QVBoxLayout())
    cs = []
    for model in ['sys/tg_test/1/short_scalar'] * 2:
        c = TaurusValueComboBox()
        c.setModel(model)
        c.addValueNames(names)
        w.layout().addWidget(c)
        cs.append(c)

    w.show()
    return a.exec_()


if __name__ == '__main__':
    import sys
    main = _taurusValueComboboxTest
    sys.exit(main())