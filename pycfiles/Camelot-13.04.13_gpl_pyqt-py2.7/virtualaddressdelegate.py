# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/virtualaddressdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.view.controls import editors
from camelot.view.proxy import ValueLoading
from camelot.core.utils import variant_to_pyobject

class VirtualAddressDelegate(CustomDelegate):
    """
  """
    __metaclass__ = DocumentationMetaclass
    editor = editors.VirtualAddressEditor

    def __init__(self, parent=None, editable=True, address_type=None, **kwargs):
        super(VirtualAddressDelegate, self).__init__(parent=parent, editable=editable, address_type=address_type, **kwargs)
        self._address_type = address_type

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        virtual_address = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        if virtual_address and virtual_address != ValueLoading:
            if virtual_address[0]:
                if not self._address_type:
                    self.paint_text(painter, option, index, '%s : %s' % (virtual_address[0], virtual_address[1]), margin_left=0, margin_right=18)
                else:
                    self.paint_text(painter, option, index, '%s' % virtual_address[1], margin_left=0, margin_right=18)
        painter.restore()