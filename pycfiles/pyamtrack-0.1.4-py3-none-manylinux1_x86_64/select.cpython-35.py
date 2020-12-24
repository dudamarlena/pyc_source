# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/select.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 5199 bytes
__doc__ = 'PyAMS_form.browser.select module\n\nSelect widget implementation.\n'
from zope.interface import Interface, implementer_only
from zope.schema.interfaces import IChoice, ITitledTokenizedTerm, IUnorderedCollection
from pyams_form.browser.widget import HTMLSelectWidget, add_field_class
from pyams_form.interfaces.widget import IFieldWidget, ISelectWidget
from pyams_form.widget import FieldWidget, SequenceWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'reStructuredText'
from pyams_form import _

@implementer_only(ISelectWidget)
class SelectWidget(HTMLSelectWidget, SequenceWidget):
    """SelectWidget"""
    klass = 'select-widget'
    css = 'select'
    prompt = False
    no_value_message = _('No value')
    prompt_message = _('Select a value...')
    _adapter_value_attributes = SequenceWidget._adapter_value_attributes + ('no_value_message',
                                                                            'prompt_message',
                                                                            'prompt')

    def is_selected(self, term):
        """Check for term selection"""
        return term.token in self.value

    def update(self):
        """See pyams_form.interfaces.widget.IWidget."""
        super(SelectWidget, self).update()
        add_field_class(self)

    @property
    def items(self):
        """Items list getter"""
        if self.terms is None:
            return ()
        items = []
        if (not self.required or self.prompt) and self.multiple is None:
            if self.prompt:
                message = self.prompt_message
            else:
                message = self.no_value_message
            items.append({'id': self.id + '-novalue', 
             'value': self.no_value_token, 
             'content': message, 
             'selected': self.value in ((), [])})
        ignored = set(self.value)

        def add_item(idx, term, prefix=''):
            selected = self.is_selected(term)
            if selected and term.token in ignored:
                ignored.remove(term.token)
            item_id = '%s-%s%i' % (self.id, prefix, idx)
            content = term.token
            if ITitledTokenizedTerm.providedBy(term):
                content = self.request.localizer.translate(term.title)
            items.append({'id': item_id, 
             'value': term.token, 
             'content': content, 
             'selected': selected})

        for idx, term in enumerate(self.terms):
            add_item(idx, term)

        if ignored:
            for idx, token in enumerate(sorted(ignored)):
                try:
                    term = self.terms.getTermByToken(token)
                except LookupError:
                    continue

                add_item(idx, term, prefix='missing-')

        return items

    def json_data(self):
        data = super(SelectWidget, self).json_data()
        data['type'] = 'select'
        data['options'] = self.items
        return data


@adapter_config(required=(IChoice, IFormLayer), provided=IFieldWidget)
def ChoiceWidgetDispatcher(field, request):
    """Dispatch widget for IChoice based also on its source."""
    return request.registry.getMultiAdapter((field, field.vocabulary, request), IFieldWidget)


@adapter_config(required=(IChoice, Interface, IFormLayer), provided=IFieldWidget)
def SelectFieldWidget(field, source, request=None):
    """IFieldWidget factory for SelectWidget."""
    if request is None:
        real_request = source
    else:
        real_request = request
    return FieldWidget(field, SelectWidget(real_request))


@adapter_config(required=(IUnorderedCollection, IFormLayer), provided=IFieldWidget)
def CollectionSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    widget = request.registry.getMultiAdapter((field, field.value_type, request), IFieldWidget)
    widget.size = 5
    widget.multiple = 'multiple'
    return widget


@adapter_config(required=(IUnorderedCollection, IChoice, IFormLayer), provided=IFieldWidget)
def CollectionChoiceSelectFieldWidget(field, value_type, request):
    """IFieldWidget factory for SelectWidget."""
    return SelectFieldWidget(field, None, request)