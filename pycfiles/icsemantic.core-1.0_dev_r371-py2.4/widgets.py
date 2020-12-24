# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/browser/widgets.py
# Compiled at: 2008-10-06 10:31:07
"""
Clases de widgets especiales

@author: Juan Pablo Gimenez
@contact: jpg@rcom.com.ar
"""
__author__ = 'Juan Pablo Gimenez <jpg@rcom.com.ar>'
__docformat__ = 'plaintext'
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget as BaseOrderedMultiSelectWidget, MultiSelectWidget as BaseMultiSelectWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

def OrderedMultiSelectionWidgetFactory(field, request):
    """ Factory para construir OrderedMultiSelectionWidgets
    """
    vocabulary = field.value_type.vocabulary
    if not request.debug:
        widget = OrderedMultiSelectionWidget(field, vocabulary, request)
    else:
        widget = BaseMultiSelectWidget(field, vocabulary, request)
    return widget


def MultiSelectionWidgetFactory(field, request):
    """ Factory para construir MultiSelectionWidgets
    """
    vocabulary = field.value_type.vocabulary
    if not request.debug:
        widget = MultiSelectionWidget(field, vocabulary, request)
    else:
        widget = BaseMultiSelectWidget(field, vocabulary, request)
    return widget


class OrderedMultiSelectionWidget(BaseOrderedMultiSelectWidget):
    """ Widget para listas de seleccion ordenadas
    """
    __module__ = __name__
    template = ViewPageTemplateFile('templates/ordered-selection.pt')

    def selected(self):
        """Return a list of tuples (text, value) that are selected."""
        values = self._getFormValue()
        if hasattr(self.context.context, self.context.__name__):
            for value in self.context.get(self.context.context):
                if value not in values:
                    values.append(value)

        terms = [ self.vocabulary.getTerm(value) for value in values if value in self.vocabulary ]
        return [ {'text': self.textForValue(term), 'value': term.token} for term in terms ]


class MultiSelectionWidget(OrderedMultiSelectionWidget):
    """ Widget para listas de seleccion no ordenadas
    """
    __module__ = __name__
    template = ViewPageTemplateFile('templates/unordered-selection.pt')