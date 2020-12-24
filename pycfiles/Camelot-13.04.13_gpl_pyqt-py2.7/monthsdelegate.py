# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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