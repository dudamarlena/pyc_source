# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/subform.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3022 bytes
"""PyAMS_form.subform module

This module provides subforms management.
"""
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
    __doc__ = 'Base inner subform'

    def __init__(self, context, request, parent_form):
        super(BaseInnerForm, self).__init__(context, request)
        self.parent_form = self.__parent__ = parent_form


class InnerAddForm(BaseInnerForm):
    __doc__ = 'Inner subform into an add form'
    ignore_context = True


class InnerEditForm(BaseInnerForm):
    __doc__ = 'Inner edit subform into a main edit form'


class InnerDisplayForm(BaseInnerForm):
    __doc__ = 'Inner display form'
    _mode = DISPLAY_MODE


@implementer(ISubForm, IHandlerForm)
class EditSubForm(BaseForm):
    __doc__ = 'Edit sub-form'
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