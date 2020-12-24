# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/multi.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3818 bytes
__doc__ = 'PyAMS_form.browser.multi module\n\nThis module provides multi-widgets implementation.\n'
from operator import attrgetter
from zope.interface import implementer
from zope.schema.interfaces import IDict, IField, IList, ITuple
from pyams_form.browser.widget import HTMLFormElement
from pyams_form.button import Buttons, button_and_handler
from pyams_form.interfaces.button import IActions
from pyams_form.interfaces.form import IButtonForm, IHandlerForm
from pyams_form.interfaces.widget import IFieldWidget, IMultiWidget
from pyams_form.widget import FieldWidget, MultiWidget as MultiWidgetBase
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'
from pyams_form import _

@implementer(IButtonForm, IHandlerForm)
class FormMixin:
    """FormMixin"""
    pass


@implementer(IMultiWidget)
class MultiWidget(HTMLFormElement, MultiWidgetBase, FormMixin):
    """MultiWidget"""
    buttons = Buttons()
    prefix = 'widget'
    klass = 'multi-widget'
    css = 'multi'
    items = ()
    actions = None
    show_label = True
    _adapter_value_attributes = MultiWidgetBase._adapter_value_attributes + ('show_label', )

    def update(self):
        """See pyams_form.interfaces.widget.IWidget."""
        super(MultiWidget, self).update()
        self.update_actions()
        self.actions.execute()
        self.update_actions()

    def update_actions(self):
        """Update widget actions"""
        self.update_allow_add_remove()
        if self.name is not None:
            self.prefix = self.name
        registry = self.request.registry
        self.actions = registry.getMultiAdapter((self, self.request, self), IActions)
        self.actions.update()

    @button_and_handler(_('Add'), name='add', condition=attrgetter('allow_adding'))
    def handle_add(self, action):
        """Add button handler"""
        self.append_adding_widget()

    @button_and_handler(_('Remove selected'), name='remove', condition=attrgetter('allow_removing'))
    def handle_remove(self, action):
        """Remove button handler"""
        self.remove_widgets([widget.name for widget in self.widgets if '{}.remove'.format(widget.name) in self.request.params])


@adapter_config(required=(IDict, IFormLayer), provided=IFieldWidget)
def MultiFieldWidgetFactory(field, request):
    """IFieldWidget factory for MultiWidget."""
    return FieldWidget(field, MultiWidget(request))


@adapter_config(required=(IDict, IField, IFormLayer), provided=IFieldWidget)
@adapter_config(required=(IList, IField, IFormLayer), provided=IFieldWidget)
@adapter_config(required=(ITuple, IField, IFormLayer), provided=IFieldWidget)
def MultiFieldWidget(field, value_type, request):
    """IFieldWidget factory for MultiWidget."""
    return MultiFieldWidgetFactory(field, request)