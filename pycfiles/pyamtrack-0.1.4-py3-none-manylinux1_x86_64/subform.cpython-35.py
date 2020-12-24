# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/subform.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3022 bytes
__doc__ = 'PyAMS_form.subform module\n\nThis module provides subforms management.\n'
from zope.interface import implementer
from zope.lifecycleevent import ObjectModifiedEvent
from pyams_form.button import handler
from pyams_form.form import BaseForm, EditForm, apply_changes
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.button import IActionHandler
from pyams_form.interfaces.form import IHandlerForm, IInnerForm, ISubForm
__docformat__ = 'restructuredtext'
from pyams_form import _

@implementer(ISubForm, IInnerForm)
class BaseInnerForm(BaseForm):
    """BaseInnerForm"""

    def __init__(self, context, request, parent_form):
        super(BaseInnerForm, self).__init__(context, request)
        self.parent_form = self.__parent__ = parent_form


class InnerAddForm(BaseInnerForm):
    """InnerAddForm"""
    ignore_context = True


class InnerEditForm(BaseInnerForm):
    """InnerEditForm"""
    pass


class InnerDisplayForm(BaseInnerForm):
    """InnerDisplayForm"""
    _mode = DISPLAY_MODE


@implementer(ISubForm, IHandlerForm)
class EditSubForm(BaseForm):
    """EditSubForm"""
    form_errors_message = _('There were some errors.')
    success_message = _('Data successfully updated.')
    no_changes_message = _('No changes were applied.')

    def __init__(self, context, request, parent_form):
        super(EditSubForm, self).__init__(context, request)
        self.parent_form = self.__parent__ = parent_form

    @handler(EditForm.buttons['apply'])
    def handle_apply(self, action):
        """Handler for apply button"""
        data, errors = self.widgets.extract()
        if errors:
            self.status = self.form_errors_message
            return
        content = self.get_content()
        changed = apply_changes(self, content, data)
        if changed:
            registry = self.request.registry
            registry.notify(ObjectModifiedEvent(content))
            self.status = self.success_message
        else:
            self.status = self.no_changes_message

    def update(self):
        super(EditSubForm, self).update()
        registry = self.request.registry
        for action in self.parent_form.actions.executed_actions:
            adapter = registry.queryMultiAdapter((self, self.request, self.get_content(), action), IActionHandler)
            if adapter:
                adapter()