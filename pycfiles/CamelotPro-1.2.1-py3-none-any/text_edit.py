# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/text_edit.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtCore, QtGui
from camelot.admin.action import ActionStep
from camelot.core.utils import ugettext_lazy as _
from camelot.view.action_runner import hide_progress_dialog
from camelot.view.controls.standalone_wizard_page import StandaloneWizardPage
from camelot.view.controls.editors import RichTextEditor
from camelot.view.utils import resize_widget_to_screen

class EditTextDocument(ActionStep):
    """
    Display a rich text editor to edit a text document.
    
    :param document: a :class:`QtGui.QTextDocument` object.
    
    When this action step is constructed, the thread affinity of
    the document is changed to be the gui thread.  when the editing
    of the document is finished, the affinity is returned to the
    current thread.  There is no :guilabel:`Cancel` button on the
    dialog because the document is changed when the user is editing
    it, and this cannot be undone.
    
    This action step can be customised using these attributes :    
        
    .. attribute:: window_title
    
        the window title of the dialog shown
        
    .. attribute:: title
    
        the title of the dialog shown
        
    .. attribute:: subtitle
    
        the subtitle of the dialog shown
        
    .. image:: /_static/actionsteps/text_document.png
        
    """

    def __init__(self, document):
        self.document = document
        self.thread = QtCore.QThread.currentThread()
        self.document.moveToThread(QtGui.QApplication.instance().thread())
        self.window_title = _('Edit text')
        self.title = _('Edit text')
        self.subtitle = _('Press OK when finished')

    def render(self):
        """create the text edit dialog. this method is used to unit test
        the action step."""
        dialog = StandaloneWizardPage(self.window_title)
        dialog.set_default_buttons(reject=None)
        dialog.set_banner_title(self.title)
        dialog.set_banner_subtitle(self.subtitle)
        main_widget = dialog.main_widget()
        layout = QtGui.QHBoxLayout()
        editor = RichTextEditor()
        editor.set_document(self.document)
        editor.set_toolbar_hidden(False)
        layout.addWidget(editor)
        main_widget.setLayout(layout)
        resize_widget_to_screen(dialog)
        return dialog

    def gui_run(self, gui_context):
        try:
            dialog = self.render()
            with hide_progress_dialog(gui_context):
                dialog.exec_()
        finally:
            self.document.moveToThread(self.thread)