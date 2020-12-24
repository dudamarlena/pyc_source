# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/radio.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3779 bytes
__doc__ = 'PyAMS_form.browser.radio module\n\nThis module provides radio widgets.\n'
from zope.interface import implementer_only
from zope.schema.interfaces import IBool, ITitledTokenizedTerm
from zope.schema.vocabulary import SimpleTerm
from pyams_form.browser.widget import HTMLInputWidget, add_field_class
from pyams_form.interfaces.widget import IFieldWidget, IRadioWidget
from pyams_form.util import to_unicode
from pyams_form.widget import FieldWidget, SequenceWidget
from pyams_layer.interfaces import IFormLayer
from pyams_template.interfaces import IPageTemplate
__docformat__ = 'restructuredtext'
from pyams_utils.adapter import adapter_config

@implementer_only(IRadioWidget)
class RadioWidget(HTMLInputWidget, SequenceWidget):
    """RadioWidget"""
    klass = 'radio-widget'
    css = 'radio'

    def is_checked(self, term):
        """Check if given term is checked"""
        return term.token in self.value

    def render_for_value(self, value):
        """Render given value"""
        terms = list(self.terms)
        try:
            term = self.terms.getTermByToken(value)
        except LookupError:
            if value == SequenceWidget.no_value_token:
                term = SimpleTerm(value)
                terms.insert(0, term)
                item_id = '%s-novalue' % self.id
            else:
                raise
        else:
            item_id = '%s-%i' % (self.id, terms.index(term))
        checked = self.is_checked(term)
        item = {'id': item_id, 
         'name': self.name, 
         'value': term.token, 
         'checked': checked}
        template = self.request.registry.getMultiAdapter((
         self.context, self.request, self.form, self.field, self), IPageTemplate, name=self.mode + '-single')
        return template(**{'context': self.context, 
         'request': self.request, 
         'view': self, 
         'item': item})

    @property
    def items(self):
        """Items list getter"""
        if self.terms is None:
            return
        for count, term in enumerate(self.terms):
            checked = self.is_checked(term)
            item_id = '%s-%i' % (self.id, count)
            if ITitledTokenizedTerm.providedBy(term):
                translate = self.request.localizer.translate
                label = translate(term.title)
            else:
                label = to_unicode(term.value)
            yield {'id': item_id, 
             'name': self.name, 
             'value': term.token, 
             'label': label, 
             'checked': checked}

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(RadioWidget, self).update()
        add_field_class(self)

    def json_data(self):
        """Get widget data in JSON format"""
        data = super(RadioWidget, self).json_data()
        data['options'] = list(self.items)
        data['type'] = 'radio'
        return data


@adapter_config(required=(IBool, IFormLayer), provides=IFieldWidget)
def RadioFieldWidget(field, request):
    """IFieldWidget factory for RadioWidget."""
    return FieldWidget(field, RadioWidget(request))