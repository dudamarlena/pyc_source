# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/action/document_action.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = 'ModelContext, GuiContext and Actions that are used in the context of\nediting a document.\n'
from .base import Action
from .application_action import ApplicationActionGuiContext, ApplicationActionModelContext
from ...core.utils import ugettext_lazy as _
from ...view.art import Icon

class DocumentActionModelContext(ApplicationActionModelContext):

    def __init__(self):
        super(DocumentActionModelContext, self).__init__()
        self.document = None
        return


class DocumentActionGuiContext(ApplicationActionGuiContext):
    """The GUI context for an :class:`camelot.admin.action.ApplicationActionGuiContext`.
    On top of  the attributes of the 
    :class:`camelot.admin.action.base.ApplicationActionGuiContext`, this context 
    contains :
    
    .. attribute:: document
    
        the :class:`QtGui.QTextDocument` upon which this action is acting
        
    """
    model_context = DocumentActionModelContext

    def __init__(self):
        super(DocumentActionGuiContext, self).__init__()
        self.document = None
        return

    def copy(self, base_class=None):
        new_context = super(DocumentActionGuiContext, self).copy(base_class)
        new_context.document = self.document
        return new_context

    def create_model_context(self):
        context = super(DocumentActionGuiContext, self).create_model_context()
        context.document = self.document
        return context


class EditDocument(Action):
    verbose_name = _('Edit')
    icon = Icon('tango/16x16/apps/accessories-text-editor.png')
    tooltip = _('Edit this document')

    def model_run(self, model_context):
        from ...view import action_steps
        edit = action_steps.EditTextDocument(model_context.document)
        yield edit