# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/one2manydelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from camelot.view.controls import editors
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.core.utils import variant_to_pyobject
import logging
logger = logging.getLogger('camelot.view.controls.delegates.one2manydelegate')

class One2ManyDelegate(CustomDelegate):
    """Custom delegate for many 2 one relations
  
  .. image:: /_static/onetomany.png
  """
    __metaclass__ = DocumentationMetaclass

    def __init__(self, parent=None, **kwargs):
        super(One2ManyDelegate, self).__init__(parent=parent, **kwargs)
        logger.debug('create one2manycolumn delegate')
        self.kwargs = kwargs

    def createEditor(self, parent, option, index):
        logger.debug('create a one2many editor')
        editor = editors.One2ManyEditor(parent=parent, **self.kwargs)
        self.setEditorData(editor, index)
        editor.editingFinished.connect(self.commitAndCloseEditor)
        return editor

    def setEditorData(self, editor, index):
        logger.debug('set one2many editor data')
        model = variant_to_pyobject(index.data(Qt.EditRole))
        editor.set_value(model)
        field_attributes = variant_to_pyobject(index.data(Qt.UserRole))
        editor.set_field_attributes(**field_attributes)

    def setModelData(self, editor, model, index):
        pass