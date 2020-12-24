# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/packet/browser/widget/document.py
# Compiled at: 2013-04-19 10:41:58
from z3c.form.interfaces import IObjectWidget, IFieldWidget, IMultiWidget
from z3c.form.object import ObjectConverter
from zope.component import adapter, adapts
from zope.interface import implementer, implements
from ztfy.sendit.packet.interfaces import IDocumentField, IDocumentsListField
from z3c.form.browser.object import ObjectWidget
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.widget import FieldWidget
from z3c.form.browser.multi import MultiWidget

class IDocumentFieldWidget(IObjectWidget):
    """Document widget interface"""
    pass


class DocumentFieldConverter(ObjectConverter):
    """Media document converter"""
    adapts(IDocumentField, IDocumentFieldWidget)

    def toWidgetValue(self, value):
        result = super(DocumentFieldConverter, self).toWidgetValue(value)
        result['__data__'] = value
        return result


class DocumentFieldWidget(ObjectWidget):
    """Document widget"""
    implements(IDocumentFieldWidget)


@adapter(IDocumentField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def DocumentFieldWidgetFactory(field, request):
    return FieldWidget(field, DocumentFieldWidget(request))


class IDocumentsListWidget(IMultiWidget):
    """Documents list widget interface"""
    pass


class DocumentsListWidget(MultiWidget):
    """Documents list widget"""
    implements(IDocumentsListWidget)


@adapter(IDocumentsListField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def DocumentsListWidgetFactory(field, request):
    return FieldWidget(field, DocumentsListWidget(request))