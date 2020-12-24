# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/orderedselect.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3767 bytes
__doc__ = 'PyAMS_form.browser.orderedselect module\n\nOrdered-selection widget implementation.\n'
from zope.interface import implementer_only
from zope.schema.interfaces import IChoice, IList, ISequence, ITitledTokenizedTerm, ITuple
from pyams_form.browser.widget import HTMLSelectWidget, add_field_class
from pyams_form.interfaces.widget import IFieldWidget, IOrderedSelectWidget
from pyams_form.widget import FieldWidget, SequenceWidget
__docformat__ = 'reStructuredText'
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config

@implementer_only(IOrderedSelectWidget)
class OrderedSelectWidget(HTMLSelectWidget, SequenceWidget):
    """OrderedSelectWidget"""
    size = 5
    multiple = 'multiple'
    items = ()
    selected_items = ()
    notselected_items = ()

    def get_item(self, term, count=0):
        """Get item matching given term"""
        item_id = '%s-%i' % (self.id, count)
        content = term.value
        if ITitledTokenizedTerm.providedBy(term):
            content = self.request.localizer.translate(term.title)
        return {'id': item_id, 
         'value': term.token, 
         'content': content}

    def update(self):
        """See pyams_form.interfaces.widget.IWidget."""
        super(OrderedSelectWidget, self).update()
        add_field_class(self)
        self.items = [self.get_item(term, count) for count, term in enumerate(self.terms)]
        self.selected_items = [self.get_item(self.terms.getTermByToken(token), count) for count, token in enumerate(self.value)]
        self.notselected_items = self.deselect()

    def deselect(self):
        """Get unselected items"""
        selected_items = []
        notselected_items = []
        for selected_item in self.selected_items:
            selected_items.append(selected_item['value'])

        for item in self.items:
            if item['value'] not in selected_items:
                notselected_items.append(item)

        return notselected_items

    def json_data(self):
        """Get widget data in JSON format"""
        data = super(OrderedSelectWidget, self).json_data()
        data['type'] = 'multi_select'
        data['options'] = self.items
        data['selected'] = self.selected_items
        data['not_selected'] = self.notselected_items
        return data


def OrderedSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, OrderedSelectWidget(request))


@adapter_config(required=(ISequence, IFormLayer), provided=IFieldWidget)
def SequenceSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return request.registry.getMultiAdapter((field, field.value_type, request), IFieldWidget)


@adapter_config(required=(IList, IChoice, IFormLayer), provided=IFieldWidget)
@adapter_config(required=(ITuple, IChoice, IFormLayer), provided=IFieldWidget)
def SequenceChoiceSelectFieldWidget(field, value_type, request):
    """IFieldWidget factory for SelectWidget."""
    return OrderedSelectFieldWidget(field, request)