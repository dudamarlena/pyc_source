# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/textlines.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1427 bytes
"""PyAMS_form.browser.textlines module

This module provides default textlines widget.
"""
from zope.interface import implementer, implementer_only
from pyams_form.browser.textarea import TextAreaWidget
from pyams_form.interfaces.widget import IFieldWidget, ITextLinesWidget
from pyams_form.widget import FieldWidget
__docformat__ = 'restructuredtext'

@implementer_only(ITextLinesWidget)
class TextLinesWidget(TextAreaWidget):
    __doc__ = 'Input type sequence widget implementation.'


@implementer(IFieldWidget)
def TextLinesFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return FieldWidget(field, TextLinesWidget(request))


@implementer(IFieldWidget)
def TextLinesFieldWidgetFactory(field, value_type, request):
    """IFieldWidget factory for TextLinesWidget."""
    return TextLinesFieldWidget(field, request)