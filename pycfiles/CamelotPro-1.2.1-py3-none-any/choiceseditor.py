# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/choiceseditor.py
# Compiled at: 2013-04-11 17:47:52
import logging
from PyQt4 import QtGui
from PyQt4 import QtCore
from camelot.view.proxy import ValueLoading
from customeditor import AbstractCustomEditor
LOGGER = logging.getLogger('camelot.view.controls.editors.ChoicesEditor')

class ChoicesEditor(QtGui.QComboBox, AbstractCustomEditor):
    """A ComboBox aka Drop Down box that can be assigned a list of
    keys and values"""
    editingFinished = QtCore.pyqtSignal()
    valueChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None, nullable=True, field_name='choices', **kwargs):
        QtGui.QComboBox.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self.activated.connect(self._activated)
        self._nullable = nullable

    @QtCore.pyqtSlot(int)
    def _activated(self, _index):
        self.setProperty('value', QtCore.QVariant(self.get_value()))
        self.valueChanged.emit()
        self.editingFinished.emit()

    def set_choices(self, choices):
        """
    :param choices: a list of (value,name) tuples.  name will be displayed in the combobox,
    while value will be used within get_value and set_value.  This method changes the items
    in the combo box while preserving the current value, even if this value is not in the
    new list of choices.
        """
        current_index = self.currentIndex()
        if current_index >= 0:
            current_name = unicode(self.itemText(current_index))
        current_value = self.get_value()
        current_value_available = False
        for i in range(self.count(), 0, -1):
            self.removeItem(i - 1)

        for i, (value, name) in enumerate(choices):
            self.insertItem(i, unicode(name), QtCore.QVariant(value))
            if value == current_value:
                current_value_available = True

        if not current_value_available and current_index > 0:
            self.insertItem(i + 1, current_name, QtCore.QVariant(current_value))
        if current_value != ValueLoading:
            self.set_value(current_value)

    def set_field_attributes(self, editable=True, choices=None, **kwargs):
        if choices != None:
            self.set_choices(choices)
        self.setEnabled(editable != False)
        return

    def get_choices(self):
        """
    :rtype: a list of (value,name) tuples
    """
        from camelot.core.utils import variant_to_pyobject
        return [ (variant_to_pyobject(self.itemData(i)), unicode(self.itemText(i))) for i in range(self.count())
               ]

    def set_value(self, value):
        """Set the current value of the combobox where value, the name displayed
        is the one that matches the value in the list set with set_choices"""
        from camelot.core.utils import variant_to_pyobject
        value = AbstractCustomEditor.set_value(self, value)
        self.setProperty('value', QtCore.QVariant(value))
        self.valueChanged.emit()
        if not self._value_loading and value != NotImplemented:
            for i in range(self.count()):
                if value == variant_to_pyobject(self.itemData(i)):
                    self.setCurrentIndex(i)
                    return

            self.setCurrentIndex(-1)
            LOGGER.error('Could not set value %s in field %s because it is not in the list of choices' % (unicode(value),
             unicode(self.objectName())))

    def get_value(self):
        """Get the current value of the combobox"""
        from camelot.core.utils import variant_to_pyobject
        current_index = self.currentIndex()
        if current_index >= 0:
            value = variant_to_pyobject(self.itemData(self.currentIndex()))
        else:
            value = ValueLoading
        return AbstractCustomEditor.get_value(self) or value