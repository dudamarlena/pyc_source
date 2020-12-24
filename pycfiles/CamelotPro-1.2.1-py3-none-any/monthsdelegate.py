# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/monthsdelegate.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from camelot.view.controls.editors import MonthsEditor
from camelot.view.controls.delegates.customdelegate import CustomDelegate, DocumentationMetaclass
from camelot.core.utils import variant_to_pyobject, ugettext
from camelot.view.proxy import ValueLoading

class MonthsDelegate(CustomDelegate):
    """MonthsDelegate

    custom delegate for showing and editing months and years
    """
    editor = MonthsEditor
    __metaclass__ = DocumentationMetaclass

    def __init__(self, parent=None, forever=2400, **kwargs):
        """
        :param forever: number of months that will be indicated as Forever, set
        to None if not appliceable
        """
        super(MonthsDelegate, self).__init__(parent=parent, **kwargs)
        self._forever = forever

    def sizeHint(self, option, index):
        q = MonthsEditor(None)
        return q.sizeHint()

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        value = variant_to_pyobject(index.model().data(index, Qt.EditRole))
        value_str = ''
        if self._forever != None and value == self._forever:
            value_str = ugettext('Forever')
        elif value not in (None, ValueLoading):
            years, months = divmod(value, 12)
            if years:
                value_str = value_str + ugettext('%i years ') % years
            if months:
                value_str = value_str + ugettext('%i months') % months
        self.paint_text(painter, option, index, value_str)
        painter.restore()
        return