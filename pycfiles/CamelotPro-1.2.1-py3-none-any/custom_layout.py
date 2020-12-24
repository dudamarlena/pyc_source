# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/form/custom_layout.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from camelot.view import forms
from camelot.admin.entity_admin import EntityAdmin

class CustomForm(forms.Form):

    def __init__(self):
        super(CustomForm, self).__init__(['first_name', 'last_name'])

    def render(self, editor_factory, parent=None, nomargins=False):
        widget = QtGui.QWidget(parent)
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel('Please fill in the complete name :', widget))
        for field_name in self.get_fields():
            field_editor = editor_factory.create_editor(field_name, widget)
            field_label = editor_factory.create_label(field_name, field_editor, widget)
            layout.addRow(field_label, field_editor)

        widget.setLayout(layout)
        widget.setBackgroundRole(QtGui.QPalette.ToolTipBase)
        widget.setAutoFillBackground(True)
        return widget


class Admin(EntityAdmin):
    list_display = [
     'first_name', 'last_name']
    form_display = CustomForm()
    form_size = (300, 100)