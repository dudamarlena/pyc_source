# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/many2onedelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.core.utils import variant_to_pyobject, create_constant_function
from camelot.view.proxy import ValueLoading
import logging
logger = logging.getLogger('camelot.view.controls.delegates.many2onedelegate')

class Many2OneDelegate(CustomDelegate):
    """Custom delegate for many 2 one relations

  .. image:: /_static/manytoone.png

  Once an item has been selected, it is represented by its unicode representation
  in the editor or the table.  So the related classes need an implementation of
  their __unicode__ method.
  """
    __metaclass__ = DocumentationMetaclass
    editor = editors.Many2OneEditor

    def __init__(self, parent=None, admin=None, editable=True, **kwargs):
        logger.debug('create many2onecolumn delegate')
        assert admin != None
        CustomDelegate.__init__(self, parent, editable, **kwargs)
        self.admin = admin
        self._kwargs = kwargs
        self._width = self._width * 2
        return

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = index.data(Qt.DisplayRole).toString()
        self.paint_text(painter, option, index, unicode(value))
        painter.restore()

    def createEditor(self, parent, option, index):
        editor = editors.Many2OneEditor(self.admin, parent, editable=self.editable, **self._kwargs)
        if option.version != 5:
            editor.setAutoFillBackground(True)
        editor.editingFinished.connect(self.commitAndCloseEditor)
        return editor

    def setEditorData(self, editor, index):
        value = variant_to_pyobject(index.data(Qt.EditRole))
        if value != ValueLoading:
            field_attributes = variant_to_pyobject(index.data(Qt.UserRole))
            editor.set_value(create_constant_function(value))
            editor.set_field_attributes(**field_attributes)
        else:
            editor.set_value(ValueLoading)

    def setModelData(self, editor, model, index):
        if editor.entity_instance_getter:
            model.setData(index, editor.entity_instance_getter)