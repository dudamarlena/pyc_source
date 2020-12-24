# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/textlines.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1427 bytes
__doc__ = 'PyAMS_form.browser.textlines module\n\nThis module provides default textlines widget.\n'
from zope.interface import implementer, implementer_only
from pyams_form.browser.textarea import TextAreaWidget
from pyams_form.interfaces.widget import IFieldWidget, ITextLinesWidget
from pyams_form.widget import FieldWidget
__docformat__ = 'restructuredtext'

@implementer_only(ITextLinesWidget)
class TextLinesWidget(TextAreaWidget):
    """TextLinesWidget"""
    pass


@implementer(IFieldWidget)
def TextLinesFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return FieldWidget(field, TextLinesWidget(request))


@implementer(IFieldWidget)
def TextLinesFieldWidgetFactory(field, value_type, request):
    """IFieldWidget factory for TextLinesWidget."""
    return TextLinesFieldWidget(field, request)