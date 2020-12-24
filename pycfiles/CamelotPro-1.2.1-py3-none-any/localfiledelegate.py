# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/localfiledelegate.py
# Compiled at: 2013-04-11 17:47:52
import logging
logger = logging.getLogger('camelot.view.controls.delegates.localfiledelegate')
from PyQt4.QtCore import Qt
from customdelegate import CustomDelegate
from customdelegate import DocumentationMetaclass
from camelot.core.utils import variant_to_pyobject
from camelot.view.controls import editors
from camelot.view.proxy import ValueLoading

class LocalFileDelegate(CustomDelegate):
    """Delegate for displaying a path on the local file system.  This path can
    either point to a file or a directory
    """
    __metaclass__ = DocumentationMetaclass
    editor = editors.LocalFileEditor

    def __init__(self, parent=None, **kw):
        CustomDelegate.__init__(self, parent, **kw)

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if value not in (None, ValueLoading):
            value_str = unicode(value)
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return