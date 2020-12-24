# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/select_object.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtCore, QtGui
from camelot.admin.action import ActionStep
from camelot.core.exception import CancelRequest
from camelot.core.utils import ugettext as _
from camelot.view.action_runner import hide_progress_dialog

class SelectDialog(QtGui.QDialog):

    def __init__(self, admin, query, parent=None):
        super(SelectDialog, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setWindowTitle(_('Select %s') % admin.get_verbose_name())
        select = admin.create_select_view(query, parent=self, search_text='')
        layout.addWidget(select)
        self.setLayout(layout)
        self.object_getter = None
        select.entity_selected_signal.connect(self.object_selected)
        return

    @QtCore.pyqtSlot(object)
    def object_selected(self, object_getter):
        self.object_getter = object_getter
        self.accept()


class SelectObject(ActionStep):
    """Select an object from a list
    
    :param admin: a :class:`camelot.admin.object_admin.ObjectAdmin` object
    """

    def __init__(self, admin):
        self.admin = admin
        self.query = admin.get_query()

    def gui_run(self, gui_context):
        select_dialog = SelectDialog(self.admin, self.query)
        with hide_progress_dialog(gui_context):
            select_dialog.exec_()
            if select_dialog.object_getter:
                return select_dialog.object_getter
            raise CancelRequest()